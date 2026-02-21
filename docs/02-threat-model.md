# 02 — Threat model

This repo is intentionally scoped to the controls most likely to matter in real enterprise RAG deployments.

## Assets

- Tenant documents (confidential PDFs, wiki pages, tickets)
- User prompts (often sensitive)
- Access tokens / credentials
- Vector store contents and metadata

## Primary threat actors

- External users attempting prompt injection / jailbreak
- Malicious or compromised tenants attempting cross-tenant access
- Insider mistakes (logging sensitive data)
- Supply-chain risks (dependencies, model artifacts)

## OWASP LLM Top 10 (2025) mapping

| OWASP Risk | Typical impact in RAG | Control in this repo | Enforcement points |
|---|---|---|---|
| LLM01 Prompt Injection | Override instructions, data exfil, policy bypass | Deny-by-default prompt filter | `app/rag/filters.py`, `app/rag/guardrails.py` |
| LLM02 Sensitive Information Disclosure | PII/secrets leak via logs or model output | Redaction + PII-safe logging | `app/core/redaction.py`, `app/core/logging.py` |
| LLM03 Supply Chain | Compromised deps/models/data | CI audit + pinned deps (starter) | `.github/workflows/ci.yml`, `Makefile security` |
| LLM04 Data & Model Poisoning | Poisoned docs/chunks, backdoors | Chunk filters + source allowlist | `app/rag/guardrails.py` |
| LLM05 Improper Output Handling | Unsafe content forwarded to other systems | Evidence-first answers + mock adapter pattern | `app/rag/pipeline.py` |
| LLM06 Excessive Agency | Tool abuse, unintended actions | No autonomous tools in MVP; scope-gated endpoints | `app/core/security.py` |
| LLM07 System Prompt Leakage | Leaks of hidden instructions | Filters block “reveal system prompt” attempts | `app/rag/filters.py` |
| LLM08 Vector/Embedding Weaknesses | Tenant mixing, adversarial retrieval | Tenant-bound query + metadata ownership | `app/store/vector.py`, `app/core/security.py` |
| LLM09 Misinformation | Hallucinations | Evidence required; no answer without tenant evidence | `app/rag/pipeline.py` |
| LLM10 Unbounded Consumption | Cost/resource DoS | Prompt length cap + top_k cap | `app/core/config.py`, `app/rag/guardrails.py` |

## Residual risks (MVP)

- In-memory store is single-process; production should use a durable store with server-side ACL.
- Filters are heuristic; add model-based classifiers and better policy engines for high assurance.
- JWT validation is symmetric for demo; production should use OIDC/JWKS.
