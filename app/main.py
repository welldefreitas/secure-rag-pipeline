from __future__ import annotations

import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_chat import router as chat_router
from app.api.routes_health import router as health_router
from app.api.routes_ingest import router as ingest_router
from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger
from app.rag.pipeline import RagPipeline
from app.store.vector import InMemoryVectorStore, VectorStoreAdapter


def _build_store(settings) -> VectorStoreAdapter:
    # MVP: use in-memory store by default.
    # Future: switch by settings.vector_backend.
    return InMemoryVectorStore()


def _build_pipeline(store: VectorStoreAdapter) -> RagPipeline:
    return RagPipeline(store=store)


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(title=settings.app_name)

    # CORS for demos; tighten for production.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # State (single-process). For multi-worker, use a real store backend.
    app.state.store = _build_store(settings)
    app.state.pipeline = _build_pipeline(app.state.store)

    logger = get_logger(__name__)

    @app.middleware("http")
    async def correlation_middleware(request: Request, call_next):
        request_id = request.headers.get("X-Request-Id") or uuid.uuid4().hex
        request.state.request_id = request_id

        response = await call_next(request)

        # Minimal access log without prompts/body
        logger.info(
            "request",
            extra={
                "request_id": request_id,
                "path": request.url.path,
                "method": request.method,
                "status_code": response.status_code,
            },
        )

        response.headers["X-Request-Id"] = request_id
        return response

    app.include_router(health_router)
    app.include_router(chat_router)
    app.include_router(ingest_router)

    return app


app = create_app()
