# 03 — Security controls library

A “controls library” you can point to during consulting engagements.

## Deny-by-default gates

- **Prompt gate**: rejects suspicious prompts.
- **Chunk gate**: retrieved content is treated as *data*, not instructions.

## Tenant isolation

- `tenant_id` is mandatory.
- API enforces JWT `tenant_id` **matches** request `tenant_id`.
- Store queries are always scoped by tenant.

## PII & secrets safety

- Redaction patterns cover common identifiers and credential shapes.
- Logging is structured JSON and intentionally avoids raw prompts/chunks.

## CI security gates

- Lint + format check
- Unit tests
- Dependency audit (pip-audit)
- Static analysis (bandit)
