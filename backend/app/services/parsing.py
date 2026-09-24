from pathlib import Path

def extract_pages(path: Path, suffix: str) -> list[dict]:
    suffix = suffix.lower()
    if suffix == ".pdf":
        from pypdf import PdfReader
        return [{"text": page.extract_text() or "", "page": i + 1} for i, page in enumerate(PdfReader(str(path)).pages)]
    if suffix == ".docx":
        from docx import Document as DocxDocument
        doc = DocxDocument(str(path))
        return [{"text": "\n".join(p.text for p in doc.paragraphs), "page": None}]
    if suffix == ".txt":
        return [{"text": path.read_text(encoding="utf-8", errors="ignore"), "page": None}]
    raise ValueError("Unsupported document type")

def smart_chunk(pages: list[dict], size: int = 900, overlap: int = 150) -> list[dict]:
    if overlap >= size: raise ValueError("chunk overlap must be smaller than chunk size")
    chunks=[]
    position=0
    for page in pages:
        text=" ".join(page["text"].split())
        if not text: continue
        start=0
        while start < len(text):
            end=min(len(text), start+size)
            if end < len(text):
                boundary=max(text.rfind(". ", start, end), text.rfind("\n", start, end), text.rfind(" ", start, end))
                if boundary > start + size//2: end=boundary+1
            piece=text[start:end].strip()
            if piece:
                chunks.append({"text":piece,"page":page.get("page"),"position":position})
                position += 1
            if end >= len(text): break
            start=max(0, end-overlap)
    return chunks
