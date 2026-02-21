# 01 — Architecture

This repo demonstrates a **secure-by-default RAG** that focuses on:

- **Tenant isolation** (no cross-tenant retrieval)
- **Prompt-injection defenses** (user + retrieved content)
- **PII/secrets redaction** (before logs and before model calls)
- **Evidence-first answers** (citations always returned)
- **Security gates in CI** (lint + tests + dependency audit)

## Diagram

The canonical diagram is stored in `diagrams/architecture.mmd`.

> Tip: GitHub renders Mermaid inside Markdown. You can also copy the `.mmd` contents into this doc if you want it inline.

## Trust boundaries

**External Zone (Untrusted)**
- User prompts and admin ingestion inputs are untrusted.

**API Boundary (FastAPI)**
- Where we enforce **AuthN**, **AuthZ**, and **tenant ownership**.
- Where we apply **redaction** and **guardrails**.

**Data Zone (Tenant-scoped)**
- Vector store queries are always bound to a `tenant_id`.
- Metadata stores the `tenant_id`, `source`, `doc_id`, and `chunk_id`.

**Model Zone**
- The MVP uses a mock model adapter.
- Production deployments should use the **same gates** with a real local/managed model.

## Data flow (happy path)

1. Client calls `POST /chat` with JWT.
2. API validates token, extracts `tenant_id`, enforces `tenant_id` match.
3. **Deny-by-default** checks on prompt.
4. Tenant-bound retrieval.
5. Chunk filters remove malicious instructions.
6. Answer is assembled with **evidence**.

## What is *not* logged

- Raw prompts
- Raw retrieved chunks
- Secrets/PII (redaction is applied before logging)
