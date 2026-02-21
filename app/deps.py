from __future__ import annotations

from fastapi import Request

from app.rag.pipeline import RagPipeline
from app.store.vector import VectorStoreAdapter


def get_store(request: Request) -> VectorStoreAdapter:
    return request.app.state.store


def get_pipeline(request: Request) -> RagPipeline:
    return request.app.state.pipeline
