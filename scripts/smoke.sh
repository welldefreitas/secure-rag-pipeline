#!/usr/bin/env bash
set -euo pipefail

BASE_URL=${BASE_URL:-http://127.0.0.1:8000}

curl -fsS "$BASE_URL/health" >/dev/null
curl -fsS "$BASE_URL/ready"  >/dev/null

echo "OK: smoke checks passed ($BASE_URL)"
