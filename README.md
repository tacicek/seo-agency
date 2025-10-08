# Seo Analyzer — Self‑Hosted (Lovable Starter)

Monorepo starter to build a SeoBotX‑style self‑hosted SEO analyzer.

## Stack
- **Frontend**: Next.js (App Router) + Tailwind + TypeScript + shadcn/ui (optional)
- **Backend**: FastAPI (Python) + BeautifulSoup + Requests
- **DB**: Supabase (Postgres) via REST (optional; falls back to local JSON)
- **Automation**: n8n webhook (optional)
- **Containers**: Docker / docker-compose

## Quick Start
```bash
# 1) Copy envs
cp .env.sample .env

# 2) Start everything
docker-compose up --build

# Web: http://localhost:3000
# API: http://localhost:8000/health
```

## Environment Variables
See **.env.sample**. If you do not have Supabase keys, API will store reports to `./data` as JSON files.

## Development (without Docker)
Backend:
```bash
cd apps/api
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Frontend:
```bash
cd apps/web
pnpm i # or npm i
pnpm dev # or npm run dev
```

## Endpoints
- `POST /analyze` → `{ url }` → returns on-page, keyword, performance (PageSpeed optional)
- `GET /health`
- `POST /export/pdf` → `{ domain, score, summary }` → PDF bytes

## Supabase Schema (optional)
See `infra/supabase/schema.sql`. Create the tables, then set `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` in `.env`.

## n8n
Create a workflow that POSTs to `API_BASE_URL/webhooks/scan` with `{ websiteId, url }` to trigger scheduled scans.

---
MIT © Tuncay Cicek
