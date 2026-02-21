from __future__ import annotations

import logging

from app.core.logging import JsonFormatter


def test_json_formatter_has_message():
    rec = logging.LogRecord(
        name="x",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="hello",
        args=(),
        exc_info=None,
    )
    out = JsonFormatter().format(rec)
    assert "hello" in out
    assert '"level"' in out
