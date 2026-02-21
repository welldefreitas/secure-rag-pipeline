from __future__ import annotations

import hashlib
import math
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Dict, List, Tuple

from app.store.metadata import DocumentChunk


def _hash_embedding(text: str, dims: int = 64) -> List[float]:
    """Deterministic toy embedding for MVP.

    This avoids external model downloads while enabling repeatable retrieval behavior.
    DO NOT use in production.
    """

    h = hashlib.sha256(text.encode("utf-8")).digest()
    vec = [0.0] * dims
    for i in range(dims):
        vec[i] = h[i % len(h)] / 255.0
    return vec


def _cosine(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


class VectorStoreAdapter(ABC):
    @abstractmethod
    def upsert(self, chunk: DocumentChunk) -> None:
        raise NotImplementedError

    @abstractmethod
    def query(self, *, tenant_id: str, text: str, top_k: int) -> List[Tuple[DocumentChunk, float]]:
        raise NotImplementedError


class InMemoryVectorStore(VectorStoreAdapter):
    """Tenant-scoped in-memory store for local dev + tests."""

    def __init__(self) -> None:
        self._by_tenant: Dict[str, List[DocumentChunk]] = defaultdict(list)

    def upsert(self, chunk: DocumentChunk) -> None:
        self._by_tenant[chunk.metadata.tenant_id].append(chunk)

    def query(self, *, tenant_id: str, text: str, top_k: int) -> List[Tuple[DocumentChunk, float]]:
        qv = _hash_embedding(text)
        scored: List[Tuple[DocumentChunk, float]] = []
        for c in self._by_tenant.get(tenant_id, []):
            cv = _hash_embedding(c.text)
            scored.append((c, _cosine(qv, cv)))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[: max(1, top_k)]
