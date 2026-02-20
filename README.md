<div align="center">

# 🔒 Enterprise Secure RAG Pipeline
### Zero-Leakage Retrieval-Augmented Generation with FastAPI, Tenant Isolation, and OWASP LLM Top 10 Guardrails.

[![CI Pipeline](https://img.shields.io/github/actions/workflow/status/welldefreitas/secure-rag-pipeline/ci.yml?style=for-the-badge)](https://github.com/welldefreitas/secure-rag-pipeline/actions)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Security](https://img.shields.io/badge/OWASP-LLM_Top_10-E4405F?style=for-the-badge)

**Goal:** Build a production-ready, secure-by-design AI pipeline that reads corporate documents without leaking sensitive data (PII) or falling victim to Prompt Injections.

</div>

---

## 🎯 Business Value (Why this repo exists)

Organizations want the power of Generative AI, but cannot risk uploading confidential PDFs to public APIs or mixing department data. This repository demonstrates a **Consulting-Grade RAG Architecture** that provides:

1. **Tenant Isolation (AuthZ):** Vector database access controls prevent cross-contamination (e.g., HR cannot query Finance documents).
2. **PII & Secrets Redaction:** Automatically masks Personally Identifiable Information *before* logging or LLM processing.
3. **Prompt Guard (Injection Defense):** Heuristic and pattern-based filters to block malicious inputs and poisoned RAG chunks.
4. **Deny-by-Default Architecture:** Strict data boundaries and structured, PII-safe audit logging.

---

## 🏗️ Architecture & Security Flow

```text
[ User Prompt (JWT Auth) ] 
      │
      ▼
[ FastAPI Gateway ] ── (AuthZ / Tenant Enforcement / PII Redaction)
      │
      ▼
[ RAG Core Filters ] ── (Prompt Injection Checks / Red Team Defenses)
      │
      ▼
[ Vector DB (Qdrant) ] ── (Retrieval constrained by Tenant ID)
      │
      ▼
[ Local/Secure LLM ] ── (Generates answer with strict Citations)
```

---

## 🚀 Quickstart

**1) Clone and setup environment**
```bash
git clone https://github.com/welldefreitas/secure-rag-pipeline.git
cd secure-rag-pipeline
cp .env.example .env
```

**2) Start the Infrastructure (API + Vector DB)**
```bash
make up
```

**3) Run the Security Red-Team Suite**
Validates that prompt injections and tenant boundaries are actively defended:
```bash
make redteam
```

---

## 📦 Repository Structure

```text
secure-rag-pipeline/
├── .github/workflows/ci.yml       # CI: lint, tests, security checks
├── docs/                          # Architecture, Threat Models & OWASP Mapping
├── app/                           # FastAPI Backend & LangChain Core
│   ├── api/                       # Chat & Ingestion Endpoints
│   ├── core/                      # Auth, PII Redaction, Structured Logging
│   ├── rag/                       # Guardrails, Prompt Filters, Citations
│   └── store/                     # Tenant-bound Vector DB adapters
├── tests/                         # Security Regression (Red Team, AuthZ)
├── scripts/                       # Local Dev & Smoke Tests
├── docker-compose.yml             # Local Vector DB & App Orchestration
└── Makefile                       # Operator commands (run/test/lint)
```

---

## 📜 License
MIT — see `LICENSE` for details.

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
