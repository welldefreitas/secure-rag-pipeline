from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import get_settings


@dataclass(frozen=True)
class Principal:
    sub: str
    tenant_id: str
    scopes: List[str]


bearer = HTTPBearer(auto_error=False)


def _unauthorized(detail: str = "Unauthorized") -> HTTPException:
    return HTTPException(status_code=401, detail=detail, headers={"WWW-Authenticate": "Bearer"})


def _forbidden(detail: str = "Forbidden") -> HTTPException:
    return HTTPException(status_code=403, detail=detail)


def get_principal(
    creds: Optional[HTTPAuthorizationCredentials] = Depends(bearer),
) -> Principal:
    """Validate JWT and return a Principal.

    This is intentionally simple for a public repo MVP.
    In production, prefer OIDC (JWKS), rotation, audiences, and stricter claims.
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
    except jwt.PyJWTError:
        raise _unauthorized("Invalid token")

    sub = str(payload.get("sub", ""))
    tenant_id = str(payload.get("tenant_id", ""))
    scopes = payload.get("scopes") or []

    if not sub or not tenant_id:
        raise _unauthorized("Missing required claims")

    if not isinstance(scopes, list):
        scopes = []

    return Principal(sub=sub, tenant_id=tenant_id, scopes=[str(s) for s in scopes])


def require_scopes(*required: str):
    def dep(p: Principal = Depends(get_principal)) -> Principal:
        if not required:
            return p
        missing = [s for s in required if s not in p.scopes]
        if missing:
            raise _forbidden("Missing required scope")
        return p

    return dep


def enforce_tenant(expected_tenant_id: str, p: Principal) -> None:
    if expected_tenant_id != p.tenant_id:
        raise _forbidden("Tenant mismatch")
