from pydantic import BaseModel, Field
from typing import List


class ChatRequest(BaseModel):
    query: str = Field(..., example="What is maternity leave policy?")
    role: str = Field(..., example="hr")


class SourceChunk(BaseModel):
    source: str
    role: str
    content: str


class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]
