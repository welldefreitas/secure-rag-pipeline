from __future__ import annotations

from app.store.metadata import Evidence


def build_evidence(doc_id: str, chunk_id: str, source: str, score: float, text: str) -> Evidence:
    excerpt = text.strip().replace("\n", " ")
    if len(excerpt) > 240:
        excerpt = excerpt[:240] + "…"
    return Evidence(
        doc_id=doc_id, chunk_id=chunk_id, source=source, score=round(score, 4), excerpt=excerpt
    )
