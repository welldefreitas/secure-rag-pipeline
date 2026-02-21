from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.core.security import Principal, enforce_tenant, require_scopes
from app.deps import get_pipeline
from app.rag.pipeline import RagPipeline
from app.store.metadata import ChatRequest, ChatResponse

router = APIRouter(tags=["chat"])

# FastAPI DI (enterprise style): use Annotated + Depends to avoid "call in default" lint noise.
ChatPrincipalDep = Annotated[Principal, Depends(require_scopes("chat"))]
PipelineDep = Annotated[RagPipeline, Depends(get_pipeline)]


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, p: ChatPrincipalDep, pipeline: PipelineDep) -> ChatResponse:
    """Secure chat endpoint.

    Enforces:
      - AuthN/AuthZ (JWT + scope)
      - tenant ownership
      - prompt injection filters + deny-by-default gates (in pipeline)
    """

    enforce_tenant(req.tenant_id, p)

    try:
        return pipeline.answer(tenant_id=req.tenant_id, question=req.question)
    except ValueError as e:
        # Secure-by-default: suspicious prompts are blocked.
        raise HTTPException(status_code=400, detail=str(e)) from e
