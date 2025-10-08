# 🎨 AI Content Generator - Vollständige Anleitung

## 📋 Überblick

Der **AI Content Generator** ist ein leistungsstarkes Tool, das E-E-A-T-optimierte, topische und holistische SEO-Inhalte generiert, die zu 100% menschlich wirken. Es nutzt fortschrittliche KI-Modelle (GPT-4 und Claude 3.5 Sonnet) für die Erstellung von SEO-optimiertem Content.

---

## ✨ Features

### 🎯 Kernfunktionen
- ✅ **E-E-A-T Optimierung** (Experience, Expertise, Authoritativeness, Trustworthiness)
- ✅ **Topische SEO-Strategie** mit semantischer Keyword-Integration
- ✅ **Holistische User Intent Coverage** für alle Phasen der Customer Journey
- ✅ **100% menschlich wirkende Inhalte** durch fortschrittliches Prompt Engineering
- ✅ **Mehrsprachige Unterstützung** (Deutsch, Englisch, Türkisch, etc.)
- ✅ **Flexible Page Types**: Service Page, Blog Post, Landing Page

### 🤖 KI-Provider
- **OpenAI GPT-4 Turbo Preview** - Hauptmodell für hochwertige Content-Generierung
- **Anthropic Claude 3.5 Sonnet** - Alternative mit exzellenter Sprachqualität

---

## 🚀 Quick Start

### 1. Frontend-Zugriff
1. Öffne das Dashboard: `http://localhost:3000`
2. Navigiere zur Section **"Content Generator"** in der Sidebar
3. Fülle das Formular mit deinen Content-Anforderungen aus
4. Klicke auf **"Generate SEO Content"**

### 2. API-Zugriff

**Endpoint:** `POST /ai/generate-content`

**Beispiel Request:**
```bash
curl -X POST http://localhost:8000/ai/generate-content \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Umzug nach Zürich - Professionelle Umzugsfirma",
    "page_type": "SERVICE",
    "main_keyword": "umzug zürich",
    "secondary_keywords": ["umzugsfirma zürich", "umzugsservice", "möbeltransport"],
    "target_location": "Zürich, Switzerland",
    "target_audience": "Families and professionals moving to Zürich",
    "language": "German",
    "tone": "professional but friendly",
    "word_count": 1500,
    "competitor_urls": ["https://competitor1.ch", "https://competitor2.ch"],
    "local_context": "Zürich city center, Limmat river, ETH Zürich area",
    "provider": "openai"
  }'
```

---

## 📝 Formularfelder

### Pflichtfelder (*)
| Feld | Beschreibung | Beispiel |
|------|--------------|----------|
| **Topic*** | Das Hauptthema deines Contents | "Umzug nach Zürich - Professionelle Umzugsfirma" |
| **Main Keyword*** | Primäres Keyword für SEO | "umzug zürich" |

### Optionale Felder
| Feld | Beschreibung | Standard | Beispiel |
|------|--------------|----------|----------|
| **Page Type** | Art der Seite | SERVICE | SERVICE / BLOG / LANDING PAGE |
| **Secondary Keywords** | Zusätzliche Keywords (kommagetrennt) | - | "umzugsfirma zürich, möbeltransport" |
| **Target Location** | Geografischer Fokus | - | "Zürich, Switzerland" |
| **Target Audience** | Zielgruppe | - | "Families and professionals" |
| **Language** | Sprache des Contents | Turkish | German / English / Turkish |
| **Tone** | Tonalität | professional but friendly | formal / casual / technical |
| **Word Count** | Ziel-Wortanzahl | 1200 | 800-3000 |
| **Competitor URLs** | URLs von Wettbewerbern | - | "https://competitor1.ch, https://competitor2.ch" |
| **Local Context** | Lokale Details | - | "Zürich city center, Limmat river" |
| **AI Provider** | KI-Modell Auswahl | openai | openai / anthropic |

---

## 🎨 Generierter Content - Struktur

Der generierte Content enthält:

### 1. **Meta Tags**
- Meta Title (55-60 Zeichen)
- Meta Description (150-160 Zeichen)

### 2. **Heading-Struktur**
- H1 (Hauptüberschrift)
- H2 (Abschnittsüberschriften)
- H3 (Unterabschnitte)

### 3. **Content-Sections**
- **Einleitung**: Problembeschreibung und Nutzenversprechen
- **Hauptteil**: Topische Abdeckung mit semantischen Keywords
- **FAQ**: Häufig gestellte Fragen (5-7 Fragen)
- **Call-to-Action (CTA)**: Conversion-optimierter Abschluss

### 4. **SEO-Optimierung**
- Keyword-Dichte: 1-2% für Hauptkeyword
- Semantische Variationen der Keywords
- Internal Linking Suggestions
- LSI Keywords Integration
- E-E-A-T Signale

---

## 🔧 Technische Details

### Backend-Implementierung

**Datei:** `apps/api/analyzers/content_generator.py`

```python
from analyzers.content_generator import generate_seo_content

result = generate_seo_content(
    topic="Your Topic",
    page_type="SERVICE",
    main_keyword="your keyword",
    secondary_keywords=["keyword1", "keyword2"],
    target_location="Location",
    target_audience="Audience",
    language="German",
    tone="professional but friendly",
    word_count=1200,
    competitor_urls=["https://competitor.com"],
    local_context="Local details",
    provider="openai"
)
```

### Response-Format

```json
{
  "success": true,
  "content": "# Hauptüberschrift\n\nContent in Markdown...",
  "provider": "openai",
  "model": "gpt-4-turbo-preview",
  "tokens_used": 1588,
  "metadata": {
    "topic": "Your Topic",
    "page_type": "SERVICE",
    "main_keyword": "your keyword",
    "secondary_keywords": ["keyword1", "keyword2"],
    "language": "German",
    "target_word_count": 1200
  }
}
```

---

## 🎯 Best Practices

### 1. Topic-Formulierung
✅ **Gut:** "Umzug nach Zürich - Professionelle Umzugsfirma mit 20 Jahren Erfahrung"
❌ **Schlecht:** "Umzug"

### 2. Keywords
✅ **Gut:** Hauptkeyword + 3-5 semantisch verwandte Secondary Keywords
❌ **Schlecht:** Nur ein Keyword ohne Variationen

### 3. Target Audience
✅ **Gut:** "Families with children, professionals relocating for work, students"
❌ **Schlecht:** "everyone"

### 4. Local Context
✅ **Gut:** "Zürich city center, neighborhoods like Oerlikon, Wiedikon, proximity to ETH"
❌ **Schlecht:** "Switzerland"

### 5. Competitor URLs
✅ **Gut:** 2-3 hochwertige Competitor-URLs für Kontext
❌ **Schlecht:** 10+ URLs oder keine URLs

---

## 🔐 API-Schlüssel Konfiguration

Die Content-Generierung benötigt API-Schlüssel:

### `.env` Datei (Backend)
```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-your-key-here

# Anthropic Configuration (optional)
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

---

## 📊 Performance

| Metrik | Wert |
|--------|------|
| Durchschnittliche Generierungszeit | 15-30 Sekunden |
| Token Usage (GPT-4) | 1200-2000 Tokens |
| Token Usage (Claude 3.5) | 1500-2500 Tokens |
| Max Word Count | 3000 Worte |
| Sprachen | 50+ Sprachen |

---

## 🐛 Troubleshooting

### Problem: "API Key Missing"
**Lösung:** Stelle sicher, dass `OPENAI_API_KEY` oder `ANTHROPIC_API_KEY` in der `.env` Datei gesetzt ist.

### Problem: "Content Too Short"
**Lösung:** Erhöhe `word_count` oder füge mehr `secondary_keywords` hinzu.

### Problem: "Generic Content"
**Lösung:** 
- Füge detaillierten `local_context` hinzu
- Definiere präzisere `target_audience`
- Nutze `competitor_urls` für Kontext

### Problem: "Timeout Error"
**Lösung:** 
- Reduziere `word_count` unter 2000
- Wechsle zu einem anderen `provider`

---

## 🎓 Beispiele

### Beispiel 1: Service Page (Deutsch)
```json
{
  "topic": "SEO-Beratung für KMU in der Schweiz",
  "page_type": "SERVICE",
  "main_keyword": "seo beratung schweiz",
  "secondary_keywords": ["seo agentur", "suchmaschinenoptimierung", "google ranking"],
  "target_location": "Zürich, Schweiz",
  "target_audience": "Kleine und mittlere Unternehmen",
  "language": "German",
  "word_count": 1500,
  "provider": "openai"
}
```

### Beispiel 2: Blog Post (Englisch)
```json
{
  "topic": "The Ultimate Guide to Technical SEO in 2025",
  "page_type": "BLOG",
  "main_keyword": "technical seo guide",
  "secondary_keywords": ["site speed", "core web vitals", "structured data"],
  "target_audience": "SEO professionals and web developers",
  "language": "English",
  "tone": "educational but engaging",
  "word_count": 2000,
  "provider": "anthropic"
}
```

### Beispiel 3: Landing Page (Türkisch)
```json
{
  "topic": "İstanbul'da Profesyonel Web Tasarım Hizmetleri",
  "page_type": "LANDING PAGE",
  "main_keyword": "web tasarım istanbul",
  "secondary_keywords": ["kurumsal web sitesi", "e-ticaret", "responsive tasarım"],
  "target_location": "İstanbul, Türkiye",
  "target_audience": "Küçük ve orta ölçekli işletmeler",
  "language": "Turkish",
  "tone": "professional but friendly",
  "word_count": 1200,
  "local_context": "Kadıköy, Beşiktaş, Şişli bölgeleri",
  "provider": "openai"
}
```

---

## 🚀 Nächste Schritte

1. **Teste verschiedene Prompts** im Frontend
2. **Experimentiere mit verschiedenen AI-Providern** (OpenAI vs. Anthropic)
3. **Optimiere die Parameter** basierend auf deinen Ergebnissen
4. **Integriere die API** in deine Content-Workflows
5. **Füge Custom Prompts** in `content_generator.py` hinzu

---

## 📞 Support

Bei Fragen oder Problemen:
- Überprüfe die Backend-Logs: `docker compose logs api`
- Teste den Endpoint direkt: `curl http://localhost:8000/ai/generate-content`
- Prüfe die API-Dokumentation: `http://localhost:8000/docs`

---

**Viel Erfolg mit deinem AI Content Generator! 🎉**
