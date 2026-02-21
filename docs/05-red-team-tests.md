# 05 — Red-team tests

This suite is intentionally small but practical.

## What we test

1. **User prompt injection**
   - "Ignore previous instructions…"
   - "Reveal system prompt…"

2. **Poisoned retrieval chunk**
   - Malicious text stored in vector DB should be dropped during retrieval filtering.

## How to run

- Local: `make up` then `make redteam`
- CI: Unit tests include injection regression.

## Extend the suite

Add more cases as you discover relevant attack strings:

- Indirect prompt injection patterns from your corp docs
- Encoded payloads (ROT13/base64)
- Attempts to override tenant boundaries
- Token/secret extraction attempts
