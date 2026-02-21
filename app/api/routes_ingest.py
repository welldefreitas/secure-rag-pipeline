from __future__ import annotations

import hashlib
import uuid

from fastapi import APIRouter, Depends, HTTPException

from app.core.security import Principal, enforce_tenant, require_scopes
from app.deps import get_store
from app.store.metadata import ChunkMetadata, DocumentChunk, IngestRequest
from app.store.vector import VectorStoreAdapter

router = APIRouter(tags=["ingest"])


def _split(text: str, *, max_chars: int = 900) -> list[str]:
    text = text.strip()
    if not text:
        return []
    out: list[str] = []
    buf: list[str] = []
    size = 0
    for line in text.splitlines():
        if size + len(line) + 1 > max_chars and buf:
            out.append("\n".join(buf).strip())
            buf, size = [], 0
        buf.append(line)
        size += len(line) + 1
    if buf:
        out.append("\n".join(buf).strip())
    return [c for c in out if c]


@router.post("/ingest", status_code=201)
def ingest(
    req: IngestRequest,
    p: Principal = Depends(require_scopes("ingest:write")),
    store: VectorStoreAdapter = Depends(get_store),
):
    enforce_tenant(req.tenant_id, p)

    doc_id = req.doc_id or hashlib.sha1(req.text.encode("utf-8")).hexdigest()[:12]
    chunks = _split(req.text)
    if not chunks:
        raise HTTPException(status_code=400, detail="empty_document")

    for i, c in enumerate(chunks):
        chunk_id = f"{uuid.uuid4().hex[:8]}-{i}"
        meta = ChunkMetadata(
            tenant_id=req.tenant_id, source=req.source, doc_id=doc_id, chunk_id=chunk_id
        )
        store.upsert(DocumentChunk(metadata=meta, text=c))

    return {"status": "ingested", "doc_id": doc_id, "chunks": len(chunks)}
