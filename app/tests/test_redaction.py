from __future__ import annotations

from app.core.redaction import redact_text


def test_redacts_email_and_card():
    raw = "Contact alice@example.com and use card 4111 1111 1111 1111"
    red = redact_text(raw)
    assert "alice@example.com" not in red
    assert "4111" not in red
