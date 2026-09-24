# Interview-ready explanation

### What is the project?
RAGForge is a production-oriented document intelligence platform. It retrieves relevant evidence from user documents and generates answers grounded in those sources.

### Why hybrid retrieval?
BM25 catches exact keywords, identifiers and terminology. Dense embeddings capture semantic similarity. Combining both reduces the blind spots of either method.

### Why RRF?
BM25 and vector search return different score scales. Reciprocal Rank Fusion combines their rankings without assuming the scores are directly comparable.

### Why reranking?
The first retrieval stage is optimized for recall. A Cross-Encoder then reads the query and candidate text together and improves the final relevance ordering before generation.

### Why citations?
Each answer is tied to the retrieved chunks, including document name, page and chunk ID. The verifier checks whether cited indices refer to actual retrieved sources.

### Production concerns
Authentication, per-user isolation, PostgreSQL persistence, Qdrant filtering, metrics, Docker, environment-based secrets and deployment configuration are included.
