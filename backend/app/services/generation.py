import re
from app.core.config import settings

def build_context(contexts):
    return "\n\n".join(f"[{i}] {c['document']} | page {c.get('page') or 'N/A'}\n{c['text']}" for i,c in enumerate(contexts,1))

def generate_answer(question:str,contexts:list[dict]):
    if not contexts:return "I could not find supporting information in the uploaded documents.",None
    context=build_context(contexts)
    if settings.llm_provider.lower()=="openai" and settings.openai_api_key:
        from openai import OpenAI
        client=OpenAI(api_key=settings.openai_api_key)
        response=client.chat.completions.create(model=settings.openai_model,temperature=0.1,messages=[
            {"role":"system","content":"You are a grounded document QA assistant. Answer only from the supplied context. Do not invent facts. Cite every material claim with [n]. If the context does not support the answer, say so."},
            {"role":"user","content":f"Question: {question}\n\nContext:\n{context}"}
        ])
        return response.choices[0].message.content or "", getattr(response.usage,"total_tokens",None)
    return f"Based on the retrieved documents: {contexts[0]['text'][:900]} [1]", None

def verify_citations(answer:str,contexts:list[dict]):
    ids=[int(x) for x in re.findall(r"\[(\d+)\]",answer)]
    valid=set(range(1,len(contexts)+1))
    cited=sorted(set(x for x in ids if x in valid))
    citations=[]
    for i,c in enumerate(contexts,1):
        citations.append({"citation_id":f"[{i}]","document":c["document"],"page":c.get("page"),"section":c.get("section"),"chunk_id":c["chunk_id"],"score":c.get("reranker_score",c.get("rrf_score",0)),"verification":"supported" if i in cited else "not-cited"})
    return citations
