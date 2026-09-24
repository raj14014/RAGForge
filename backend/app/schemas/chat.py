from pydantic import BaseModel, Field
class ChatRequest(BaseModel):
    question: str = Field(min_length=2, max_length=5000)
    top_k: int = Field(default=5, ge=1, le=20)
class SearchRequest(BaseModel):
    query: str = Field(min_length=2, max_length=5000)
    top_k: int = Field(default=10, ge=1, le=50)
