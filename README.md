# 🚀 RAGForge — Production RAG Intelligence Platform

### 🔗 Live Demo
👉 **https://rag-forge-ochre.vercel.app/**

### 💻 GitHub Repository
👉 **https://github.com/raj14014/RAGForge**

---

## 📌 Overview

**RAGForge** is a production-oriented **Retrieval-Augmented Generation (RAG)** platform that allows users to upload documents and ask questions using grounded AI responses with source citations.

It implements a complete RAG pipeline instead of relying on simple vector search.

### 🔄 RAG Pipeline

**Documents → Smart Chunking → BM25 + Vector Search → Hybrid RRF → Cross-Encoder Reranker → LLM → Citation Verification → Answer**

---

## ✨ Key Features

- 📄 Document/PDF upload and processing
- 🔍 Hybrid BM25 + Vector retrieval
- 🔗 Reciprocal Rank Fusion (RRF)
- 🎯 Cross-Encoder reranking
- 🤖 Grounded LLM responses
- 📚 Citation/source verification
- 🔐 JWT-based authentication
- 📊 Evaluation and metrics
- 🗄️ PostgreSQL / SQLite support
- ⚡ Qdrant vector database
- 🐳 Docker-ready architecture
- 📈 Prometheus metrics
- ☁️ Vercel + Render deployment

---

## 🛠️ Tech Stack

**Frontend**
- React
- TypeScript
- Vite

**Backend**
- Python
- FastAPI
- Pydantic
- SQLAlchemy

**AI / RAG**
- Sentence Transformers
- BM25
- Vector Search
- Reciprocal Rank Fusion
- Cross-Encoder Reranker
- LLM Integration

**Database & Infrastructure**
- PostgreSQL
- SQLite
- Qdrant
- Redis/Celery
- Docker
- Prometheus

---

## 🏗️ Architecture

```text
                ┌──────────────┐
                │   Documents  │
                └──────┬───────┘
                       ↓
                Smart Chunking
                       ↓
          ┌────────────┴────────────┐
          ↓                         ↓
     BM25 Search              Vector Search
          └────────────┬────────────┘
                       ↓
                Hybrid RRF
                       ↓
              Cross-Encoder
                Reranking
                       ↓
                    LLM
                       ↓
             Citation Verification
                       ↓
              Grounded Answer


🚀 Local Setup
Backend
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload

Backend:

http://127.0.0.1:8000/docs
Frontend
cd frontend
npm install
npm run dev

Frontend:

http://localhost:5173
🔑 Environment Variables

Create .env files locally and configure:

VITE_API_URL=http://localhost:8000/api

Production environment variables should be configured through the deployment platform.

Never commit secrets or .env files.

📡 Main API Endpoints
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me

POST /api/documents/upload
GET  /api/documents
DELETE /api/documents/{id}

POST /api/search
POST /api/chat

GET  /api/evaluation/results
POST /api/evaluation/run

GET  /health
GET  /metrics
🎯 Why RAGForge?

Unlike a basic RAG chatbot that directly performs vector search and sends results to an LLM, RAGForge uses:

Lexical + semantic retrieval for broader search coverage
RRF to combine multiple retrieval strategies
Reranking to improve document relevance
Citation verification for grounded responses
Evaluation & metrics for measuring system performance
Authentication & persistence for application-level usage
Production deployment architecture for real-world use
💼 Placement Highlights

This project demonstrates practical experience with:

Full-Stack Development • RAG • LLMs • Information Retrieval • Vector Databases • REST APIs • Authentication • Database Design • Docker • Cloud Deployment • System Architecture

🌐 Try It
👉 Live Application

https://rag-forge-ochre.vercel.app/

👉 Source Code

https://github.com/raj14014/RAGForge

👨‍💻 Author

Dhanraj Kumar Sahu

Computer Science Engineering — AI/ML

GitHub: https://github.com/raj14014
