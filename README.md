<div align="center">

# 🔒 Enterprise Secure RAG Pipeline
### Secure-by-design Retrieval-Augmented Generation with FastAPI, tenant isolation, and OWASP LLM Top 10 guardrails.

[![CI Pipeline](https://img.shields.io/github/actions/workflow/status/welldefreitas/secure-rag-pipeline/ci.yml?style=for-the-badge)](https://github.com/welldefreitas/secure-rag-pipeline/actions)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Security](https://img.shields.io/badge/OWASP-LLM_Top_10-000000?style=for-the-badge&logo=owasp&logoColor=white)

**Goal:** Demonstrate a **consulting-grade** RAG architecture that can ingest internal documents and answer questions **without tenant leakage**, **without logging PII**, and **with prompt-injection defenses**.

</div>

---

## Why this repo exists

Most RAG demos stop at “it answers questions”. Enterprises need proof that it answers **safely**:

- ✅ **Tenant isolation** (ownership enforced at API boundary + storage query)
- ✅ **Prompt injection defenses** (user input + retrieved chunks)
- ✅ **PII/secrets redaction** (before logging and before model calls)
- ✅ **Evidence-first answers** (citations returned; no evidence → refuse)
- ✅ **Security gates in CI** (lint + tests + dependency audit + static analysis)

---

## Architecture

- Mermaid diagram: `diagrams/architecture.mmd`
- Deep dive docs:
  - `docs/01-architecture.md`
  - `docs/02-threat-model.md` (OWASP LLM Top 10 mapping)
  - `docs/05-red-team-tests.md`

---

## API (MVP)

### `POST /ingest` (admin/protected)
Ingests raw text into a tenant-scoped store.

### `POST /chat`
Returns an evidence-based answer scoped to the tenant.

### `GET /health` and `GET /ready`
Basic liveness/readiness.

---

## Quickstart (local)

### 1) Clone + env
```bash
git clone https://github.com/welldefreitas/secure-rag-pipeline.git
cd secure-rag-pipeline
cp .env.example .env
```

### 2) Run locally
Option A — Docker:
```bash
make up
```

Option B — Python:
```bash
make install
make run
```

### 3) Generate a demo JWT
This repo uses a simple HS256 JWT for the public MVP.

```bash
python - <<'PY'
import jwt
secret = "change-me"  # must match JWT_SECRET in .env
payload = {"sub": "demo", "tenant_id": "tenant-a", "scopes": ["chat", "ingest:write"]}
print(jwt.encode(payload, secret, algorithm="HS256"))
PY
```

### 4) Ingest + chat
```bash
TOKEN="<paste-token>"

curl -sS -X POST http://127.0.0.1:8000/ingest \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tenant_id":"tenant-a","source":"confluence","text":"Policy: never share secrets. Contact: alice@example.com"}'

curl -sS -X POST http://127.0.0.1:8000/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tenant_id":"tenant-a","question":"What does the policy say?"}'
```

---

## Red-team suite

Runs a small set of attack prompts and validates secure behavior (block/deny where appropriate).

```bash
make redteam
```

Extend the suite in `docs/05-red-team-tests.md`.

---

## Repo structure

```text
secure-rag-pipeline/
├── .github/workflows/ci.yml          # CI: lint, tests, security gates
├── docs/                             # Architecture, threat model, controls library
├── diagrams/                         # Mermaid diagram
├── app/
│   ├── api/                          # /chat, /ingest, /health
│   ├── core/                         # config, logging, security, redaction
│   ├── rag/                          # retrieval, guardrails, citations
│   ├── store/                        # vector adapter + tenant metadata
│   └── tests/                        # authz/injection/redaction/logging tests
├── scripts/                          # smoke + redteam helpers
├── docker-compose.yml                # local stack (qdrant optional)
├── Dockerfile                        # non-root container
├── Makefile                          # operator commands
├── .env.example                      # env template
├── security.md                       # short security summary
└── LICENSE
```

---

## Notes (MVP trade-offs)

- The default vector store is **in-memory** for fast demos and deterministic tests.
- The LLM adapter is **mocked** in the MVP to keep the repo self-contained.
- Production implementations should:
  - use OIDC/JWKS validation
  - use a durable vector store with server-side ACL
  - implement stronger injection defenses (classifiers + policy engines)

---

## License
MIT — see `LICENSE`.

<br>

<p align="center">
  <b>Developed by Wellington de Freitas</b> | <i>Cloud Security & AI Architect</i>
  <br><br>
  <a href="https://linkedin.com/in/welldefreitas" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
  </a>
  <a href="https://github.com/welldefreitas" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
  </a>
</p>
