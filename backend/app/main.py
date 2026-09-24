from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.init_db import init_db
from app.api.routes import router

Path(settings.upload_dir).mkdir(parents=True,exist_ok=True)
init_db()
app=FastAPI(title=settings.app_name,version="2.0.0",description="Production-oriented hybrid RAG document intelligence API")
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_list,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(router,prefix="/api")

@app.get("/")
def root(): return {"name":"RAGForge","status":"running","pipeline":"Documents -> Smart Chunking -> BM25 + Vector -> Hybrid RRF -> Reranker -> LLM -> Citation Verification -> Answer"}
@app.get("/health")
def health(): return {"status":"healthy"}

@app.get("/metrics")
def metrics(): return "# RAGForge metrics endpoint\nragforge_up 1\n"
