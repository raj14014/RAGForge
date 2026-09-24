from rank_bm25 import BM25Okapi
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Chunk, Document
from app.services.embeddings import encode
from app.services.vector_store import vector_store


_bm25_cache = {}


def _chunk_record(chunk):
    return {
        "chunk_id": chunk.chunk_id,
        "text": chunk.text,
        "page": chunk.page,
        "section": chunk.section,
        "document": chunk.document.filename,
    }


def rebuild_bm25(owner_id: int, chunks):
    records = [_chunk_record(c) for c in chunks]
    corpus = [r["text"].lower().split() for r in records]

    if corpus:
        _bm25_cache[owner_id] = (BM25Okapi(corpus), records)
    else:
        _bm25_cache[owner_id] = (None, records)


def invalidate_bm25(owner_id: int):
    _bm25_cache.pop(owner_id, None)


def hybrid_search(
    db: Session,
    owner_id: int,
    query: str,
    top_k: int = 20,
):
    if owner_id not in _bm25_cache:
        chunks = db.scalars(
            select(Chunk)
            .options(selectinload(Chunk.document))
            .join(Document)
            .where(Document.owner_id == owner_id)
            .order_by(Chunk.id)
        ).all()

        rebuild_bm25(owner_id, chunks)

    dense = []

    try:
        dense = vector_store.search(
            encode([query])[0],
            owner_id,
            top_k,
        )
    except Exception:
        dense = []

    bm25, corpus = _bm25_cache.get(
        owner_id,
        (None, []),
    )

    lexical = []

    if bm25:
        scores = bm25.get_scores(
            query.lower().split()
        )

        ranked = sorted(
            zip(corpus, scores),
            key=lambda x: x[1],
            reverse=True,
        )[:top_k]

        lexical = [
            {
                **record,
                "bm25_score": float(score),
            }
            for record, score in ranked
        ]

    merged = {}

    for rank, item in enumerate(dense, 1):
        merged.setdefault(
            item["chunk_id"],
            {
                "item": item,
                "rrf": 0.0,
            },
        )["rrf"] += 1 / (60 + rank)

    for rank, item in enumerate(lexical, 1):
        merged.setdefault(
            item["chunk_id"],
            {
                "item": item,
                "rrf": 0.0,
            },
        )["rrf"] += 1 / (60 + rank)

    results = []

    for value in sorted(
        merged.values(),
        key=lambda x: x["rrf"],
        reverse=True,
    )[:top_k]:
        results.append(
            {
                **value["item"],
                "rrf_score": value["rrf"],
            }
        )

    return results