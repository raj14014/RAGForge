from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_name: str = "RAGForge API"
    environment: str = "development"
    database_url: str = "sqlite:///./ragforge.db"
    jwt_secret: str = "change-this-in-production"
    jwt_expire_hours: int = 24
    cors_origins: str = "http://localhost:5173"
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str | None = None
    qdrant_collection: str = "ragforge_chunks"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    embedding_dimension: int = 384
    llm_provider: str = "mock"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    upload_dir: str = "./uploads"
    max_upload_mb: int = 20
    retrieval_k: int = 20
    rerank_k: int = 5
    chunk_size: int = 900
    chunk_overlap: int = 150
    redis_url: str = "redis://localhost:6379/0"

    @property
    def cors_list(self) -> list[str]:
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()]

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
