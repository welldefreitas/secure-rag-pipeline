# 04 — Tenant isolation

## Tenant model

- Every request is bound to a `tenant_id`.
- JWT contains a `tenant_id` claim.
- API rejects any request where `tenant_id` (request) != `tenant_id` (JWT).

## Enforcement points

- API layer: `app/core/security.py` (`enforce_tenant`)
- Storage layer: `app/store/vector.py` queries are always `tenant_id` scoped

## Tests

See `app/tests/test_authz.py`.
