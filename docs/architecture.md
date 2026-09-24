# Architecture

```text
React/Vite
   |
FastAPI REST API
   |
   +--> PostgreSQL: users, documents, chunks, conversations, messages, evaluations
   |
   +--> Ingestion: PDF/DOCX/TXT -> cleaning -> smart chunks -> embeddings
   |                                      |
   |                                      +--> Qdrant
   |                                      +--> BM25 index
   |
   +--> Query -> BM25 + dense vector -> RRF -> Cross-Encoder -> context
   |                                      |
   |                                      v
   |                                  Grounded LLM
   |                                      |
   |                              Citation verification
   |                                      |
   |                                   Answer
```

## Security boundary
Every document, chunk and conversation is scoped by authenticated `owner_id`. Qdrant payload filters apply the same owner boundary to dense retrieval.
