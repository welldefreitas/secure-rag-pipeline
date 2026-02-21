from __future__ import annotations

from app.store.metadata import DocumentChunk
from app.store.vector import VectorStoreAdapter


def retrieve(
    store: VectorStoreAdapter,
    *,
    tenant_id: str,
    query: str,
    top_k: int,
) -> list[tuple[DocumentChunk, float]]:
    return store.query(tenant_id=tenant_id, text=query, top_k=top_k)
