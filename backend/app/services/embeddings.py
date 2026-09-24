from functools import lru_cache
from app.core.config import settings

@lru_cache
def model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(settings.embedding_model)

def encode(texts: list[str]) -> list[list[float]]:
    if not texts: return []
    return model().encode(texts, normalize_embeddings=True).tolist()

def dimension() -> int:
    return int(model().get_sentence_embedding_dimension())
