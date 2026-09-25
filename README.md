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
