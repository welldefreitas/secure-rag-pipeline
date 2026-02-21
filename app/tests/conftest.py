from __future__ import annotations

import os

import jwt
import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture(autouse=True)
def _env(monkeypatch: pytest.MonkeyPatch):
    # deterministic demo secret for tests
    monkeypatch.setenv("JWT_SECRET", "test-secret")
    monkeypatch.setenv("JWT_ALGORITHM", "HS256")


@pytest.fixture()
def client() -> TestClient:
    app = create_app()
    return TestClient(app)


def make_token(*, tenant_id: str, scopes: list[str]) -> str:
    secret = os.environ.get("JWT_SECRET", "test-secret")
    payload = {"sub": "tester", "tenant_id": tenant_id, "scopes": scopes}
    return jwt.encode(payload, secret, algorithm="HS256")
