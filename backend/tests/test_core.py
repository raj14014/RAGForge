from pathlib import Path
from tempfile import TemporaryDirectory
from app.services.parsing import smart_chunk
from app.services.evaluation import precision_at_k, recall_at_k, hit_rate, mrr
from app.services.generation import verify_citations

def test_smart_chunk_overlap_and_metadata():
    chunks=smart_chunk([{"text":"Sentence one. Sentence two. Sentence three. "*100,"page":2}], size=100, overlap=20)
    assert len(chunks)>1
    assert all(c["page"]==2 for c in chunks)
    assert chunks[0]["position"]==0

def test_metrics():
    retrieved=["a","b","c"]; relevant=["b","d"]
    assert precision_at_k(retrieved,relevant,2)==0.5
    assert recall_at_k(retrieved,relevant,2)==0.5
    assert hit_rate(retrieved,relevant,2)==1.0
    assert mrr(retrieved,relevant)==0.5

def test_citation_verification():
    contexts=[{"chunk_id":"c1","document":"a.pdf","page":1,"text":"hello","rrf_score":.1},{"chunk_id":"c2","document":"b.pdf","page":2,"text":"world","rrf_score":.2}]
    out=verify_citations("hello [1]",contexts)
    assert out[0]["verification"]=="supported"
    assert out[1]["verification"]=="not-cited"
