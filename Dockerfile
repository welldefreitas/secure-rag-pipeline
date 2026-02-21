# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Security: minimal OS deps + non-root user
# hadolint ignore=DL3008
RUN apt-get update \
  && apt-get install -y --no-install-recommends ca-certificates curl \
  && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 10001 appuser
WORKDIR /app

# Copy source first (needed for packaging install)
COPY pyproject.toml README.md LICENSE ./
COPY app ./app

# Install as a regular package (production-style)
# hadolint ignore=DL3013,DL3042
RUN python -m pip install --no-cache-dir -U pip \
  && python -m pip install --no-cache-dir .

USER appuser
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -fsS http://127.0.0.1:8000/health || exit 1

# Use app factory to avoid import side-effects (tests/env overrides)
CMD ["uvicorn", "app.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
