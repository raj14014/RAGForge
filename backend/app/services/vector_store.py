import logging
from app.core.config import settings

log=logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        self.client=None
        try:
            from qdrant_client import QdrantClient
            self.client=QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key or None, timeout=3)
            from qdrant_client.models import Distance, VectorParams
            names={c.name for c in self.client.get_collections().collections}
            if settings.qdrant_collection not in names:
                self.client.create_collection(settings.qdrant_collection, vectors_config=VectorParams(size=settings.embedding_dimension, distance=Distance.COSINE))
        except Exception as exc:
            log.warning("Qdrant unavailable; vector search will be unavailable until Qdrant is configured: %s", exc)
            self.client=None

    def upsert(self, points):
        if not self.client: return False
        from qdrant_client.models import PointStruct
        self.client.upsert(settings.qdrant_collection, [PointStruct(id=p["id"], vector=p["vector"], payload=p["payload"]) for p in points])
        return True

    def search(self, vector, owner_id, limit):
        if not self.client: return []
        from qdrant_client.models import FieldCondition, Filter, MatchValue
        result=self.client.query_points(settings.qdrant_collection, query=vector, query_filter=Filter(must=[FieldCondition(key="owner_id", match=MatchValue(value=owner_id))]), limit=limit, with_payload=True)
        return [{"score":float(p.score), **(p.payload or {})} for p in result.points]

    def delete_document(self, document_id: int):
        if not self.client: return
        from qdrant_client.models import FieldCondition, Filter, MatchValue
        self.client.delete(settings.qdrant_collection, points_selector=Filter(must=[FieldCondition(key="document_id", match=MatchValue(value=document_id))]))

vector_store=VectorStore()
