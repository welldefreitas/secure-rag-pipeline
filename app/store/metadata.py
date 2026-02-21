from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ChunkMetadata(BaseModel):
    tenant_id: str
    source: str = Field(default="unknown")
    doc_id: str
    chunk_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class DocumentChunk(BaseModel):
    metadata: ChunkMetadata
    text: str
    # Optional future fields: embedding vector, access labels, etc.


class IngestRequest(BaseModel):
    tenant_id: str
    source: str = "unknown"
    text: str
    doc_id: Optional[str] = None


class ChatRequest(BaseModel):
    tenant_id: str
    question: str


class Evidence(BaseModel):
    doc_id: str
    chunk_id: str
    source: str
    score: float
    excerpt: str


class ChatResponse(BaseModel):
    tenant_id: str
    answer: str
    evidence: list[Evidence]
