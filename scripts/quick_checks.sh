#!/usr/bin/env bash
set -euo pipefail

# Quick API sanity checks and examples (uses local dev URLs)

API_BASE_URL="${API_BASE_URL:-http://localhost:8000}"

echo "[1/3] DFS connection test"
curl -s "$API_BASE_URL/dfs/test" | jq . || true

echo "[2/3] DFS SERP live example"
curl -s -X POST "$API_BASE_URL/dfs/serp" \
  -H 'Content-Type: application/json' \
  -d '{"keyword":"umzug zürich", "location_name":"Switzerland", "language_name":"German", "device":"desktop"}' | jq . || true

TARGET_URL="${TARGET_URL:-}"
if [[ -n "${TARGET_URL}" ]]; then
  echo "[3/3] Screaming Frog crawl via env TARGET_URL=$TARGET_URL"
  TARGET_URL="$TARGET_URL" python apps/api/crawl_and_ingest.py || true
else
  echo "[3/3] Screaming Frog crawl (from data/target_url.txt or default)"
  python apps/api/crawl_and_ingest.py || true
fi
