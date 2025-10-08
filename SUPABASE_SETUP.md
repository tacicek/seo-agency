# Supabase Integration Setup ✨

## Status: Teilweise konfiguriert ⚠️

### ✅ Bereits erledigt:
- Supabase URL hinzugefügt
- Anon Key konfiguriert
- Setup-Script erstellt

### 🔧 Noch zu erledigen:

#### 1. Datenbank-Tabelle erstellen

Öffnen Sie Ihr [Supabase Dashboard](https://pjmwbwxuwinvstpvbrxf.supabase.co) und:

1. Gehen Sie zum **SQL Editor** (linke Seitenleiste)
2. Klicken Sie auf **"New Query"**
3. Fügen Sie folgendes SQL ein:

```sql
-- Minimal tables for storing reports
create table if not exists public.seo_reports (
  id text primary key,
  payload jsonb not null,
  created_at timestamp with time zone default now()
);
```

4. Klicken Sie auf **"Run"**

#### 2. Service Role Key hinzufügen

1. Gehen Sie zu **Settings → API** im Supabase Dashboard
2. Finden Sie den **"service_role"** Key unter "Project API keys"
3. Kopieren Sie den Key
4. Fügen Sie ihn zur `.env`-Datei hinzu:

```env
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3...
```

⚠️ **Wichtig**: Der Service Role Key hat volle Zugriffsrechte - teilen Sie ihn niemals öffentlich!

#### 3. (Optional) Row Level Security (RLS) konfigurieren

Falls Sie RLS aktivieren möchten:

1. Gehen Sie zu **Authentication → Policies**
2. Wählen Sie die Tabelle `seo_reports`
3. Erstellen Sie Policies basierend auf Ihren Anforderungen

**Beispiel-Policy** (alle können lesen, nur Service Role kann schreiben):

```sql
-- Enable RLS
ALTER TABLE public.seo_reports ENABLE ROW LEVEL SECURITY;

-- Allow public read access
CREATE POLICY "Allow public read access" ON public.seo_reports
  FOR SELECT USING (true);

-- Allow service role to insert
CREATE POLICY "Allow service role insert" ON public.seo_reports
  FOR INSERT WITH CHECK (true);
```

#### 4. System neu starten

Nach dem Hinzufügen des Service Role Keys:

```bash
docker-compose down
docker-compose up --build
```

### 🧪 Testen der Integration

Sobald alles konfiguriert ist:

1. Starten Sie das System
2. Gehen Sie zu http://localhost:3000
3. Führen Sie eine SEO-Analyse durch
4. Überprüfen Sie in Supabase → Table Editor → seo_reports, ob der Report gespeichert wurde

### 📝 Hilfreiche Befehle

```bash
# Setup-Anweisungen anzeigen
./scripts/setup_supabase.sh

# System starten
docker-compose up --build

# System stoppen
docker-compose down

# Logs anzeigen
docker-compose logs -f api
```

### 🔍 Troubleshooting

**Problem**: Reports werden nicht in Supabase gespeichert
- ✅ Überprüfen Sie, ob `SUPABASE_SERVICE_KEY` gesetzt ist
- ✅ Prüfen Sie die API-Logs: `docker-compose logs api`
- ✅ Testen Sie die Verbindung im Supabase Dashboard

**Problem**: "Table not found" Fehler
- ✅ Stellen Sie sicher, dass die Tabelle erstellt wurde (siehe Schritt 1)
- ✅ Überprüfen Sie den Tabellennamen: `public.seo_reports`

**Fallback**: Wenn Supabase nicht verfügbar ist, speichert das System automatisch in `./data` als JSON-Dateien.

---

**Erstellt am**: 7. Oktober 2025
