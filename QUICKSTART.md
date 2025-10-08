# 🎯 Schnell-Links - SEO Analyzer Setup

## 📌 Wichtige Links

### Supabase Dashboard
- **Hauptseite**: https://supabase.com/dashboard/project/pjmwbwxuwinvstpvbrxf
- **SQL Editor**: https://supabase.com/dashboard/project/pjmwbwxuwinvstpvbrxf/sql/new
- **Table Editor**: https://supabase.com/dashboard/project/pjmwbwxuwinvstpvbrxf/editor
- **API Settings**: https://supabase.com/dashboard/project/pjmwbwxuwinvstpvbrxf/settings/api

### Nach dem Start
- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 🚀 Schnellstart

### 1. Tabelle erstellen (nur einmal nötig)

**Automatische Anleitung:**
```bash
./scripts/create_table.sh
```

**Oder manuell:**
1. Öffnen: https://supabase.com/dashboard/project/pjmwbwxuwinvstpvbrxf/sql/new
2. SQL einfügen:
   ```sql
   create table if not exists public.seo_reports (
     id text primary key,
     payload jsonb not null,
     created_at timestamp with time zone default now()
   );
   ```
3. "RUN" klicken

### 2. System starten

```bash
# Einfachster Weg
./scripts/start.sh

# Oder direkt mit Docker
docker compose up --build
```

### 3. Testen

1. Browser öffnen: http://localhost:3000
2. URL eingeben: `https://example.com`
3. "Analyze" klicken
4. Ergebnis ansehen (wird in Supabase gespeichert)

---

## 📚 Dokumentation

- **Vollständige Anleitung**: [SETUP_COMPLETE.md](SETUP_COMPLETE.md)
- **Supabase Setup**: [SUPABASE_SETUP.md](SUPABASE_SETUP.md)
- **Tabelle erstellen**: [CREATE_TABLE_GUIDE.md](CREATE_TABLE_GUIDE.md)
- **Projekt README**: [README.md](README.md)

---

## ⚙️ Konfiguration

### Aktuelle .env Einstellungen:

```env
✅ API_BASE_URL=http://localhost:8000
✅ NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
✅ SUPABASE_URL=https://pjmwbwxuwinvstpvbrxf.supabase.co
✅ SUPABASE_SERVICE_KEY=[konfiguriert]
✅ NEXT_PUBLIC_SUPABASE_URL=https://pjmwbwxuwinvstpvbrxf.supabase.co
✅ NEXT_PUBLIC_SUPABASE_ANON_KEY=[konfiguriert]
```

### Optional (noch nicht konfiguriert):
- `PAGESPEED_API_KEY` - Google PageSpeed Insights
- `MOZ_ACCESS_ID` / `MOZ_SECRET_KEY` - Moz API
- `AHREFS_API_KEY` - Ahrefs API
- `SMTP_*` - E-Mail-Versand

---

## 🔧 Hilfreiche Befehle

### Docker
```bash
# Starten
docker compose up --build

# Im Hintergrund starten
docker compose up -d

# Stoppen
docker compose down

# Logs ansehen (alle Services)
docker compose logs -f

# Logs ansehen (nur API)
docker compose logs -f api

# Logs ansehen (nur Web)
docker compose logs -f web

# Container neu bauen
docker compose build --no-cache

# Alles aufräumen (inkl. Volumes)
docker compose down -v
```

### Scripts
```bash
# Tabelle erstellen/testen
./scripts/create_table.sh

# Supabase Setup-Anleitung
./scripts/setup_supabase.sh

# System starten
./scripts/start.sh
```

### Entwicklung (ohne Docker)

**Backend:**
```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Frontend:**
```bash
cd apps/web
npm install
npm run dev
```

---

## ✅ Checkliste

- [x] .env Datei konfiguriert
- [x] Supabase URL hinzugefügt
- [x] Supabase Keys konfiguriert
- [ ] **Tabelle in Supabase erstellt** ← NÄCHSTER SCHRITT
- [ ] Docker installiert
- [ ] System gestartet
- [ ] Erste Analyse durchgeführt

---

## 🆘 Hilfe & Support

### Häufige Probleme

**"Table not found"**
→ Führen Sie aus: `./scripts/create_table.sh`

**"Docker not found"**
→ Installieren Sie Docker Desktop: https://www.docker.com/products/docker-desktop

**"Port already in use"**
→ Stoppen Sie andere Services auf Port 3000/8000 oder ändern Sie die Ports in docker-compose.yml

**API funktioniert nicht**
→ Prüfen Sie Logs: `docker compose logs api`

---

**Erstellt**: 7. Oktober 2025  
**Nächster Schritt**: Tabelle erstellen mit `./scripts/create_table.sh`
