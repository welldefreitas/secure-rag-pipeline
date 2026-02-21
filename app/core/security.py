from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import get_settings


@dataclass(frozen=True)
class Principal:
    sub: str
    tenant_id: str
    scopes: list[str]


bearer = HTTPBearer(auto_error=False)


def _unauthorized(detail: str = "Unauthorized") -> HTTPException:
    return HTTPException(status_code=401, detail=detail, headers={"WWW-Authenticate": "Bearer"})


def _forbidden(detail: str = "Forbidden") -> HTTPException:
    return HTTPException(status_code=403, detail=detail)


CredsDep = Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)]


def get_principal(creds: CredsDep) -> Principal:
    """Validate JWT and return a Principal.

    MVP note:
      - uses a static shared secret from env (JWT_SECRET)
      - no JWKS / OIDC / audience enforcement

    In production: prefer OIDC + JWKS rotation, issuer/audience checks, and tighter claim validation.
    """

    if creds is None or creds.scheme.lower() != "bearer":
        raise _unauthorized()

    settings = get_settings()

    try:
        payload = jwt.decode(
            creds.credentials,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
            options={"verify_aud": False},
        )
    except jwt.PyJWTError as e:
        raise _unauthorized("Invalid token") from e

    sub = str(payload.get("sub", ""))
    tenant_id = str(payload.get("tenant_id", ""))
    scopes = payload.get("scopes") or []

    if not sub or not tenant_id:
        raise _unauthorized("Missing required claims")

    if not isinstance(scopes, list):
        scopes = []

    return Principal(sub=sub, tenant_id=tenant_id, scopes=[str(s) for s in scopes])


PrincipalDep = Annotated[Principal, Depends(get_principal)]


def require_scopes(*required: str):
    """Dependency factory enforcing OAuth-like scopes."""

    def dep(p: PrincipalDep) -> Principal:
        if not required:
            return p

        missing = [s for s in required if s not in p.scopes]
        if missing:
            raise _forbidden("Missing required scope")

        return p

    return dep


def enforce_tenant(expected_tenant_id: str, p: Principal) -> None:
    """Hard tenant ownership enforcement (deny-by-default)."""

    if expected_tenant_id != p.tenant_id:
        raise _forbidden("Tenant mismatch")
