# Security summary

This repository is designed as a **demonstrable security baseline** for RAG.

## Secure-by-default behaviors

- Blocks obvious prompt injection patterns.
- Rejects cross-tenant access (tenant mismatch returns 403).
- Does not log raw prompts or raw documents.
- Returns answers with evidence; if no evidence is available, it refuses to speculate.

## Reporting

If you find an issue, open a GitHub issue with:

- Steps to reproduce
- Expected behavior
- Actual behavior
- Suggested mitigation
