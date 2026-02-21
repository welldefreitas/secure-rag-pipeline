from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any, Dict, Optional


class JsonFormatter(logging.Formatter):
    """Minimal JSON logs (stdout), PII-safe by design.

    IMPORTANT: never log raw prompts or raw retrieved chunks.
    """

    def format(self, record: logging.LogRecord) -> str:
        base: Dict[str, Any] = {
            "ts": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }

        # Extra fields (best effort)
        for k in ("request_id", "tenant_id", "path", "method", "status_code"):
            v = getattr(record, k, None)
            if v is not None:
                base[k] = v

        if record.exc_info:
            base["exc"] = self.formatException(record.exc_info)

        return json.dumps(base, ensure_ascii=False)


def configure_logging(level: str = "INFO") -> None:
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(level.upper())

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root.addHandler(handler)

    # Reduce noisy loggers
    logging.getLogger("uvicorn").setLevel(level.upper())
    logging.getLogger("uvicorn.error").setLevel(level.upper())
    logging.getLogger("uvicorn.access").setLevel(level.upper())


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
