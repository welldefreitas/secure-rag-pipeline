from __future__ import annotations

from dataclasses import dataclass

from app.core.config import get_settings
from app.core.redaction import redact_text
from app.rag.citations import build_evidence
from app.rag.guardrails import deny_by_default_user_prompt, filter_retrieved_chunks
from app.rag.retrieval import retrieve
from app.store.metadata import ChatResponse, Evidence
from app.store.vector import VectorStoreAdapter


@dataclass
class RagPipeline:
    store: VectorStoreAdapter

    def answer(self, *, tenant_id: str, question: str) -> ChatResponse:
        settings = get_settings()

        # 1) User prompt gate
        deny_by_default_user_prompt(question, max_chars=settings.max_prompt_chars)

        # 2) Retrieval (tenant-bound)
        hits = retrieve(self.store, tenant_id=tenant_id, query=question, top_k=settings.top_k)

        # 3) Drop malicious retrieved chunks + enforce allowlist boundaries
        safe_pairs = filter_retrieved_chunks([(h.metadata.source, h.text) for h, _ in hits])

        # Align safe_pairs back to original hits for evidence building
        safe_evidence: list[Evidence] = []
        safe_context: list[str] = []
        for chunk, score in hits:
            if (chunk.metadata.source, chunk.text) not in safe_pairs:
                continue
            safe_evidence.append(
                build_evidence(
                    doc_id=chunk.metadata.doc_id,
                    chunk_id=chunk.metadata.chunk_id,
                    source=chunk.metadata.source,
                    score=score,
                    text=chunk.text,
                )
            )
            safe_context.append(chunk.text)

        # 4) Assemble answer (mock LLM for MVP)
        # IMPORTANT: redact before any output or logging.
        answer = self._mock_llm_answer(question=question, context=safe_context)
        answer = redact_text(answer)

        return ChatResponse(tenant_id=tenant_id, answer=answer, evidence=safe_evidence)

    def _mock_llm_answer(self, *, question: str, context: list[str]) -> str:
        if not context:
            return (
                "I don't have enough tenant-scoped evidence to answer safely. "
                "Please ingest relevant documents for this tenant."
            )

        # "Secure" behavior: never follow instructions in context. Treat it as data only.
        # Provide a short, conservative synthesis.
        snippet = " ".join(c.strip().replace("\n", " ") for c in context[:2])
        if len(snippet) > 600:
            snippet = snippet[:600] + "…"

        return (
            "Answer (evidence-based, tenant-scoped):\n"
            f"Question: {question}\n\n"
            "Relevant evidence excerpt(s):\n"
            f"- {snippet}\n\n"
            "Note: this MVP uses a mock LLM. Plug in your preferred local/managed model behind the same guardrails."
        )
