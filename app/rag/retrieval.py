from __future__ import annotations

from typing import List, Tuple

from app.store.vector import VectorStoreAdapter
from app.store.metadata import DocumentChunk


def retrieve(
    store: VectorStoreAdapter,
    *,
    tenant_id: str,
    query: str,
    top_k: int,
) -> List[Tuple[DocumentChunk, float]]:
    return store.query(tenant_id=tenant_id, text=query, top_k=top_k)
