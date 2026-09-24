# Deployment

## Docker
`docker compose up --build` starts PostgreSQL, Redis, Qdrant, API and frontend.

## Backend
Use Render or another Docker platform. Required production variables:
- DATABASE_URL
- JWT_SECRET
- CORS_ORIGINS
- QDRANT_URL
- QDRANT_API_KEY
- LLM_PROVIDER=openai
- OPENAI_API_KEY
- OPENAI_MODEL

## Frontend
Deploy `frontend` to Vercel and set `VITE_API_URL` to the public API URL plus `/api`.

## Qdrant
Create a collection with cosine distance and dimension 384 for `all-MiniLM-L6-v2`.

## Production hardening
- Use a managed PostgreSQL database.
- Store uploads in object storage rather than local disk for horizontally scaled deployments.
- Move ingestion to Celery workers for large files.
- Rotate JWT secrets and provider keys.
- Restrict CORS to the production domain.
- Configure HTTPS, backups and monitoring.
