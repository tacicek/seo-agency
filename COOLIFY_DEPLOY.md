# Coolify Deployment Guide

This repository is ready for deployment on Coolify using Docker Compose.

## Services
- API (FastAPI, Python 3.11) — port 8000
- Web (Next.js 14, production build) — port 3000

## Compose file
Use `docker-compose.coolify.yml` as your stack definition.

## Environment variables
Set these in Coolify (Stack → Environment):

Required for Web:
- NEXT_PUBLIC_API_BASE_URL=http://api:8000

Optional (API providers):
- DATAFORSEO_LOGIN, DATAFORSEO_PASSWORD
- SERPAPI_API_KEY
- OPENAI_API_KEY, GEMINI_API_KEY, ANTHROPIC_API_KEY, MISTRAL_API_KEY
- MOZ_ACCESS_ID, MOZ_SECRET_KEY
- SUPABASE_URL, SUPABASE_SERVICE_KEY
- PAGESPEED_API_KEY

Optional (Crawl target fallback file):
- Mount a persistent volume on `/data` and place `target_url.txt` inside; or set TARGET_URL as env.

## Steps in Coolify
1. Create → Docker Compose → Connect your Git repository
2. Select branch, choose `docker-compose.coolify.yml`
3. Add environment variables as needed (see above)
4. Deploy

## Health & URLs
- API health: `GET http://<host>:8000/health` (exposed)
- Web UI: `http://<host>:3000`

Note: Web calls API via `http://api:8000` (Docker service name). If you expose API publicly with a domain, you may set `NEXT_PUBLIC_API_BASE_URL` accordingly.

## Persistence
- `./data` is mounted to `/data` in the API container. Use it for `target_url.txt` or other artifacts you want to persist.

## Troubleshooting
- Check service logs in Coolify if build fails (node or python dependency issues)
- Ensure provider API keys are correct; verify via `/ai/test` (AI), `/dfs/test` (DataForSEO)
- If API starts slowly, the Web will wait; a healthcheck is configured for the API
