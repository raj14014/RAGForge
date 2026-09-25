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

RAGForge — Production RAG Intelligence Platform

RAGForge is a production-oriented Retrieval-Augmented Generation (RAG) platform that transforms uploaded documents into searchable, grounded, and citation-aware AI answers.

🚀 Live Demo

Frontend: RAGForge Live Website

Backend API: RAGForge API

✨ Features
🔐 JWT-based authentication
📄 PDF, TXT and DOCX document ingestion
✂️ Smart overlap-aware document chunking
🔎 Hybrid search using BM25 + dense vector retrieval
🔀 Reciprocal Rank Fusion (RRF)
🎯 Cross-encoder reranking
🤖 Grounded RAG-based question answering
📚 Citation extraction and verification
📊 Retrieval evaluation
📈 Precision@K, Recall@K, Hit Rate and MRR
🛡️ Unsupported-claim tracking
⚡ React + FastAPI production architecture
🧠 RAG Pipeline
Document Upload
      ↓
Document Parsing
      ↓
Smart Chunking
      ↓
 ┌───────────────┐
 │ BM25 Search   │
 │ Vector Search │
 └───────┬───────┘
         ↓
   Hybrid RRF
         ↓
    Reranking
         ↓
   Context Selection
         ↓
       LLM
         ↓
Citation Verification
         ↓
  Grounded Answer
🛠️ Tech Stack
Frontend
React
TypeScript
Vite
Axios
React Router
CSS
Backend
Python
FastAPI
JWT Authentication
REST APIs
AI / RAG
RAG
BM25
Dense Vector Search
Embeddings
Reciprocal Rank Fusion
Cross-Encoder Reranking
LLM-based Answer Generation
Citation Verification
Deployment
Frontend: Vercel
Backend: Render
📂 Project Structure
RAGForge/
│
├── backend/
│   ├── app/
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── vite.config.ts
│   └── vercel.json
│
├── .gitignore
├── README.md
└── ...
🔐 Authentication Flow

RAGForge uses JWT-based authentication.

User
 ↓
Login / Register
 ↓
FastAPI Authentication API
 ↓
JWT Access Token
 ↓
Frontend localStorage
 ↓
Axios Authorization Header
 ↓
Protected API Endpoints

Example:

Authorization: Bearer <JWT_TOKEN>
📄 Document Processing

Users can upload:

PDF
TXT
DOCX

The backend processes the document and converts it into overlapping chunks containing metadata such as:

Document name
Page number
Chunk ID
Text content

These chunks are then indexed for retrieval.

🔎 Hybrid Search

Instead of depending on only one retrieval technique, RAGForge combines:

BM25

Useful for exact keyword matching.

Dense Vector Search

Useful for semantic similarity.

RRF

Combines rankings from both retrieval methods to produce a unified ranking.

BM25 Results
      +
Vector Results
      ↓
     RRF
      ↓
Better candidate ranking
🎯 Reranking

Retrieved candidates are passed through a reranker to improve relevance before sending context to the LLM.

Initial Retrieval
       ↓
Top Candidates
       ↓
Cross Encoder
       ↓
Relevant Context

This reduces the chance of irrelevant chunks being included in the final context.

🤖 Grounded RAG Chat

Users can ask questions about their uploaded documents.

RAGForge retrieves relevant document chunks and provides them as context to the LLM.

The system then returns:

Grounded answer
Retrieval latency
Number of retrieved sources
Citations
Source document
Page number
Citation verification status
📚 Citation Verification

RAGForge doesn't only generate an answer.

It also tracks the sources used to generate the answer.

Question
   ↓
Retrieval
   ↓
Relevant Chunks
   ↓
LLM Answer
   ↓
Citation Mapping
   ↓
Verification

This makes the generated response easier to inspect and verify.

📊 Evaluation

RAGForge includes an evaluation module for measuring retrieval quality.

Metrics include:

Precision@K
Recall@K
Hit Rate
MRR
Citation Accuracy
Unsupported Claim Rate

This helps evaluate the RAG pipeline rather than relying only on subjective answer quality.

🚀 Run Locally
1. Clone Repository
git clone https://github.com/raj14014/RAGForge.git
cd RAGForge
2. Backend
cd backend

python -m venv .venv

.\.venv\Scripts\activate

pip install -r requirements.txt

Configure the required backend environment variables in:
backend/.env

Then start the API:
uvicorn app.main:app --reload

Backend:
http://localhost:8000
3. Frontend
Open another terminal:
cd frontend
npm install

Create:
frontend/.env

Add:
VITE_API_URL=http://localhost:8000/api

Run:
npm run dev

Frontend:
http://localhost:5173
🌐 Production Configuration

For the deployed frontend, the API URL is configured through the Vercel environment variable:

VITE_API_URL=https://ragforge-api-6prx.onrender.com/api

Frontend deployment:

Vercel

Backend deployment:

Render

🔗 Project Links
Resource	Link
🌐 Live Website	RAGForge
💻 GitHub Repository	RAGForge GitHub
⚙️ Backend API	RAGForge API
🎯 Why RAGForge?

Traditional LLM applications can generate answers without providing reliable evidence.

RAGForge focuses on retrieval quality, grounded generation, and source traceability.

The complete pipeline is:

Documents
   ↓
Smart Chunking
   ↓
BM25 + Vector Retrieval
   ↓
RRF
   ↓
Reranking
   ↓
Grounded LLM
   ↓
Citation Verification
   ↓
Inspectable Answer
👨‍💻 Author

Dhanraj Kumar Sahu

B.Tech — Computer Science & Engineering (AI/ML)

GitHub: raj14014

⭐ If you find this project useful

Consider giving the repository a ⭐ on GitHub.
