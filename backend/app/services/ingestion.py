from pathlib import Path
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models import Document, Chunk
from app.services.parsing import extract_pages, smart_chunk
from app.services.embeddings import encode
from app.services.vector_store import vector_store
from app.services.retrieval import rebuild_bm25

def ingest_document(db:Session, document:Document, path:Path):
    pages=extract_pages(path,path.suffix)
    pieces=smart_chunk(pages,settings.chunk_size,settings.chunk_overlap)
    vectors=encode([p["text"] for p in pieces])
    for i,(piece,vec) in enumerate(zip(pieces,vectors)):
        cid=f"doc-{document.id}-chunk-{i}"
        db.add(Chunk(document_id=document.id,chunk_id=cid,text=piece["text"],page=piece.get("page"),position=piece["position"]))
        vector_store.upsert([{"id":document.id*1000000+i,"vector":vec,"payload":{"owner_id":document.owner_id,"document_id":document.id,"chunk_id":cid,"text":piece["text"],"page":piece.get("page"),"section":None,"document":document.filename}}])
    document.chunk_count=len(pieces); document.status="completed"; document.error_message=None
    db.commit(); db.refresh(document)
    all_chunks=db.query(Chunk).join(Document).filter(Document.owner_id==document.owner_id).all()
    rebuild_bm25(document.owner_id,all_chunks)
    return document
