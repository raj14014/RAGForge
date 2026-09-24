from functools import lru_cache
from app.core.config import settings
@lru_cache
def model():
    from sentence_transformers import CrossEncoder
    return CrossEncoder(settings.reranker_model)

def rerank(query:str,candidates:list[dict],top_k:int=5):
    if not candidates:return []
    try:
        scores=model().predict([(query,x["text"]) for x in candidates])
        ranked=sorted(zip(candidates,scores),key=lambda x:float(x[1]),reverse=True)[:top_k]
        return [{**item,"reranker_score":float(score)} for item,score in ranked]
    except Exception:
        return candidates[:top_k]
