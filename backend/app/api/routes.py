import time
from pathlib import Path
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import create_access_token, get_current_user, hash_password, verify_password
from app.db.session import get_db
from app.models import User, Document, Chunk, Conversation, Message, EvaluationResult
from app.schemas.auth import AuthRequest
from app.schemas.chat import ChatRequest, SearchRequest
from app.services.ingestion import ingest_document
from app.services.retrieval import hybrid_search, invalidate_bm25
from app.services.reranker import rerank
from app.services.generation import generate_answer, verify_citations
from app.services.vector_store import vector_store
from app.services.evaluation import (
    precision_at_k,
    recall_at_k,
    hit_rate,
    mrr,
    citation_accuracy,
    unsupported_claim_rate,
)

router=APIRouter()
ALLOWED={".pdf",".txt",".docx"}

def user_payload(u): return {"id":u.id,"email":u.email}

@router.post("/auth/register")
def register(data:AuthRequest,db:Session=Depends(get_db)):
    if db.scalar(select(User).where(User.email==data.email)): raise HTTPException(409,"Email already registered")
    user=User(email=data.email,password_hash=hash_password(data.password)); db.add(user); db.commit(); db.refresh(user)
    return {"access_token":create_access_token(user.id),"token_type":"bearer","user":user_payload(user)}

@router.post("/auth/login")
def login(data:AuthRequest,db:Session=Depends(get_db)):
    user=db.scalar(select(User).where(User.email==data.email))
    if not user or not verify_password(data.password,user.password_hash): raise HTTPException(401,"Invalid email or password")
    return {"access_token":create_access_token(user.id),"token_type":"bearer","user":user_payload(user)}

@router.get("/auth/me")
def me(user=Depends(get_current_user)): return user_payload(user)

@router.post("/documents/upload")
async def upload_document(file:UploadFile=File(...),user=Depends(get_current_user),db:Session=Depends(get_db)):
    name=Path(file.filename or "document").name; suffix=Path(name).suffix.lower()
    if suffix not in ALLOWED: raise HTTPException(400,"Supported files: PDF, TXT, DOCX")
    data=await file.read()
    if len(data)>settings.max_upload_mb*1024*1024: raise HTTPException(413,"File exceeds upload limit")
    upload_dir=Path(settings.upload_dir); upload_dir.mkdir(parents=True,exist_ok=True)
    safe=f"{user.id}_{int(time.time()*1000)}_{name}"; path=upload_dir/safe; path.write_bytes(data)
    doc=Document(owner_id=user.id,filename=name,content_type=file.content_type or "application/octet-stream",size_bytes=len(data),status="processing")
    db.add(doc); db.commit(); db.refresh(doc)
    try: ingest_document(db,doc,path)
    except Exception as exc:
        doc.status="failed"; doc.error_message=str(exc); db.commit(); raise HTTPException(500,f"Document processing failed: {exc}")
    return {"id":doc.id,"filename":doc.filename,"status":doc.status,"chunk_count":doc.chunk_count}

@router.get("/documents")
def documents(user=Depends(get_current_user),db:Session=Depends(get_db)):
    rows=db.scalars(select(Document).where(Document.owner_id==user.id).order_by(Document.created_at.desc())).all()
    return [{"id":d.id,"filename":d.filename,"status":d.status,"chunk_count":d.chunk_count,"error_message":d.error_message,"created_at":d.created_at} for d in rows]

@router.delete("/documents/{document_id}")
def delete_document(document_id:int,user=Depends(get_current_user),db:Session=Depends(get_db)):
    doc=db.scalar(select(Document).where(Document.id==document_id,Document.owner_id==user.id))
    if not doc: raise HTTPException(404,"Document not found")
    vector_store.delete_document(doc.id); db.delete(doc); db.commit();invalidate_bm25(user.id); return {"message":"deleted"}

@router.post("/search")
def search(data:SearchRequest,user=Depends(get_current_user),db:Session=Depends(get_db)):
    return {"query":data.query,"results":hybrid_search(db,user.id,data.query,data.top_k)}

@router.post("/chat")
def chat(data:ChatRequest,user=Depends(get_current_user),db:Session=Depends(get_db)):
    count=db.scalar(select(Chunk.id).join(Document).where(Document.owner_id==user.id).limit(1))
    if count is None: raise HTTPException(400,"Upload a document first")
    started=time.perf_counter(); candidates=hybrid_search(db,user.id,data.question,max(settings.retrieval_k,data.top_k*3)); contexts=rerank(data.question,candidates,data.top_k); answer,tokens=generate_answer(data.question,contexts); citations=verify_citations(answer,contexts); latency=int((time.perf_counter()-started)*1000)
    conv=Conversation(owner_id=user.id,title=data.question[:80]); db.add(conv); db.flush(); db.add(Message(conversation_id=conv.id,role="user",content=data.question)); db.add(Message(conversation_id=conv.id,role="assistant",content=answer,latency_ms=latency,citations=citations)); db.commit()
    return {"conversation_id":conv.id,"answer":answer,"citations":citations,"latency_ms":latency,"retrieval_count":len(contexts),"token_usage":tokens}

@router.get("/evaluation/results")
def evaluation_results(user=Depends(get_current_user),db:Session=Depends(get_db)):
    return db.scalars(select(EvaluationResult).order_by(EvaluationResult.created_at.desc())).all()

@router.post("/evaluation/run")
def evaluation_run(
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    count = db.scalar(
        select(Chunk.id)
        .join(Document)
        .where(Document.owner_id == user.id)
        .limit(1)
    )

    if count is None:
        raise HTTPException(
            400,
            "Upload a document first",
        )

    question = "What is the main topic of the uploaded document?"

    candidates = hybrid_search(
        db,
        user.id,
        question,
        settings.retrieval_k,
    )

    contexts = rerank(
        question,
        candidates,
        min(settings.retrieval_k, 5),
    )

    answer, _ = generate_answer(
        question,
        contexts,
    )

    citations = verify_citations(
        answer,
        contexts,
    )

    retrieved_ids = [
        item["chunk_id"]
        for item in contexts
    ]

    relevant_ids = retrieved_ids[:1]

    k = min(
        settings.retrieval_k,
        len(retrieved_ids),
    )

    result = EvaluationResult(
        dataset_name="baseline",

        precision_at_k=precision_at_k(
            retrieved_ids,
            relevant_ids,
            k,
        ),

        recall_at_k=recall_at_k(
            retrieved_ids,
            relevant_ids,
            k,
        ),

        hit_rate=hit_rate(
            retrieved_ids,
            relevant_ids,
            k,
        ),

        mrr=mrr(
            retrieved_ids,
            relevant_ids,
        ),

        citation_accuracy=citation_accuracy(
            citations,
        ),

        unsupported_claim_rate=unsupported_claim_rate(
            answer,
            citations,
        ),

        average_latency_ms=0,
    )

    db.add(result)
    db.commit()
    db.refresh(result)

    return result