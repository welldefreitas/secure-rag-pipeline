# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Security: minimal OS deps + non-root user
RUN apt-get update \
  && apt-get install -y --no-install-recommends ca-certificates curl \
  && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 10001 appuser
WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
RUN python -m pip install --no-cache-dir -U pip \
  && python -m pip install --no-cache-dir -e .

COPY app ./app

USER appuser
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -fsS http://127.0.0.1:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
