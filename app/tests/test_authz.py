from __future__ import annotations

from app.tests.conftest import make_token


def test_requires_auth(client):
    r = client.post("/chat", json={"tenant_id": "t1", "question": "hi"})
    assert r.status_code == 401


def test_tenant_mismatch_forbidden(client):
    token = make_token(tenant_id="t1", scopes=["chat"])
    r = client.post(
        "/chat",
        headers={"Authorization": f"Bearer {token}"},
        json={"tenant_id": "t2", "question": "hi"},
    )
    assert r.status_code == 403


def test_ingest_requires_scope(client):
    token = make_token(tenant_id="t1", scopes=["chat"])  # missing ingest:write
    r = client.post(
        "/ingest",
        headers={"Authorization": f"Bearer {token}"},
        json={"tenant_id": "t1", "source": "confluence", "text": "hello"},
    )
    assert r.status_code == 403
