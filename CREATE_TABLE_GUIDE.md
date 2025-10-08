# 🗄️ Supabase Tabelle Erstellen

## ❌ Status: Tabelle existiert noch nicht

Die Tabelle `seo_reports` wurde noch nicht in Ihrer Supabase-Datenbank erstellt.

---

## 📋 Schritt-für-Schritt-Anleitung

### **Schritt 1: Supabase Dashboard öffnen**

Klicken Sie auf diesen Link oder kopieren Sie ihn in Ihren Browser:

```
https://supabase.com/dashboard/project/pjmwbwxuwinvstpvbrxf/editor
```

### **Schritt 2: SQL Editor öffnen**

Auf der linken Seite:
1. Klicken Sie auf **"SQL Editor"** Icon (📝)
2. Oder gehen Sie direkt zu:
   ```
   https://supabase.com/dashboard/project/pjmwbwxuwinvstpvbrxf/sql/new
   ```

### **Schritt 3: SQL-Code einfügen**

Kopieren Sie diesen SQL-Code:

```sql
-- Minimal tables for storing reports
create table if not exists public.seo_reports (
  id text primary key,
  payload jsonb not null,
  created_at timestamp with time zone default now()
);
```

### **Schritt 4: SQL ausführen**

1. Fügen Sie den Code in den SQL Editor ein
2. Klicken Sie auf den **"RUN"** oder **"▶"** Button (oben rechts)
3. Warten Sie auf die Bestätigung: `Success. No rows returned`

---

## ✅ Überprüfung

Nach dem Erstellen der Tabelle:

### **Option A: Im Terminal**
```bash
./scripts/create_table.sh
```

Wenn erfolgreich, sehen Sie:
```
✅ Table exists! (empty)
🎉 Supabase ist vollständig konfiguriert!
```

### **Option B: Im Supabase Dashboard**
1. Gehen Sie zu **"Table Editor"** (linke Seitenleiste)
2. Sie sollten die Tabelle **`seo_reports`** sehen
3. Spalten:
   - `id` (text, primary key)
   - `payload` (jsonb)
   - `created_at` (timestamp)

---

## 🚀 Nach erfolgreicher Erstellung

Starten Sie das System:

```bash
# Mit Docker Compose
docker compose up --build

# Oder mit dem Start-Script
./scripts/start.sh
```

Dann testen Sie:
1. Frontend öffnen: http://localhost:3000
2. URL eingeben: `https://example.com`
3. Auf **"Analyze"** klicken
4. Report wird automatisch in Supabase gespeichert!

---

## 🔍 Troubleshooting

### Problem: "Table not found" nach Erstellung

**Lösung:**
- Warten Sie 10-30 Sekunden (Schema-Cache-Refresh)
- Führen Sie erneut aus: `./scripts/create_table.sh`

### Problem: SQL-Editor nicht gefunden

**Lösung:**
- Stellen Sie sicher, dass Sie eingeloggt sind
- Überprüfen Sie die Projekt-URL
- Alternativ: Dashboard → SQL Editor (linke Seitenleiste)

### Problem: "Permission denied" beim SQL ausführen

**Lösung:**
- Sie benötigen Admin-Rechte für das Supabase-Projekt
- Überprüfen Sie, ob Sie der Owner sind
- Falls Team-Mitglied: Bitten Sie den Owner, die Tabelle zu erstellen

---

## 📸 Visual Guide

```
┌─────────────────────────────────────────────────────────┐
│ Supabase Dashboard                                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [📊 Table Editor]  ← Hier sehen Sie die Tabellen     │
│  [📝 SQL Editor]    ← HIER KLICKEN!                    │
│  [🔧 Database]                                          │
│  [🔐 Authentication]                                    │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  SQL Editor                                             │
│  ┌───────────────────────────────────────────────┐    │
│  │ create table if not exists...                 │    │
│  │                                                │    │
│  └───────────────────────────────────────────────┘    │
│                                           [▶ RUN]      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

**Tipp**: Speichern Sie diese Anleitung. Sie können sie später für andere Tabellen verwenden!
