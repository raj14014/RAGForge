# RAGForge — Production RAG Intelligence Platform

RAGForge is a placement-ready full-stack RAG system demonstrating an inspectable production pipeline:

**Documents → Smart Chunking → BM25 + Vector Search → Hybrid RRF → Cross-Encoder Reranker → Grounded LLM → Citation Verification → Answer**

## Stack
- React + TypeScript + Vite
- FastAPI + Pydantic + SQLAlchemy
- PostgreSQL / SQLite local fallback
- Qdrant vector database
- Sentence Transformers embeddings
- BM25 lexical retrieval
- Reciprocal Rank Fusion
- Cross-Encoder reranking
- OpenAI-compatible generation abstraction
- Redis/Celery infrastructure ready
- Prometheus metrics endpoint
- Docker Compose
- Render + Vercel deployment configuration

## Local setup
### Backend
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```
Open `http://127.0.0.1:8000/docs`.

### Frontend
```powershell
cd frontend
npm install
copy .env.example .env
npm run dev
```
Open `http://localhost:5173`.

### Full infrastructure
```powershell
docker compose up --build
```

## Production
1. Create managed PostgreSQL.
2. Create Qdrant Cloud collection with the configured embedding dimension.
3. Set `LLM_PROVIDER=openai` and a production API key.
4. Generate a long random `JWT_SECRET`.
5. Deploy `backend` using `render.yaml` or any Docker host.
6. Set `CORS_ORIGINS` to the deployed frontend URL.
7. Deploy `frontend` to Vercel with `VITE_API_URL=https://YOUR-API/api`.
8. Never commit `.env` or secrets.

## API
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`
- `POST /api/documents/upload`
- `GET /api/documents`
- `DELETE /api/documents/{id}`
- `POST /api/search`
- `POST /api/chat`
- `GET /api/evaluation/results`
- `POST /api/evaluation/run`
- `GET /health`
- `GET /metrics`

## Placement explanation
The project demonstrates why a production RAG system needs both lexical and semantic retrieval, rank fusion, reranking, source attribution, verification, evaluation, authentication, persistence and observability instead of a simple vector-search chatbot.
