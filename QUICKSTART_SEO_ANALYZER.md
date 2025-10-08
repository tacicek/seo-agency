# 🚀 Advanced SEO Analyzer - Quick Start

## Was ist das?

Ein hochmodernes Python-Tool für **Topical Analysis** und **Domain Authority Estimation** mit:

- 🧠 **BERTopic** für Topic Clustering
- 🔑 **KeyBERT** für semantische Keywords
- 📊 **Moz API** für Domain Authority
- 📈 **Custom Scoring** Algorithm
- 📄 **HTML Reports** mit Visualisierungen

## 📦 Installation

### 1. Starte Docker Container (mit allen NLP-Bibliotheken)

```bash
cd /Users/tuncaycicek/Desktop/seo-analyzer-starter
docker compose up --build -d
```

⏱️ **Erster Build dauert 5-10 Minuten** (lädt Torch, Transformers, etc.)

### 2. Teste die Installation

```bash
./test_seo_analyzer.sh
```

Dieser Test prüft:
- ✅ Alle Packages installiert
- ✅ Skript ohne Syntax-Fehler
- ✅ Funktionale Mini-Analyse

## 🎯 Verwendung

### Methode 1: Direkt (Einfachste)

```bash
docker exec -it seo-api python seo_analyzer.py https://example.com
```

**Output:**
- `topics.json` - Alle Topics mit Keywords
- `domain_metrics.json` - DA, PA, Spam Score, Domain Age
- `report.html` - Vollständiger HTML-Report
- `topic_distribution.png` - Pie Chart
- `authority_breakdown.png` - Score Breakdown

### Methode 2: Quick Start Skript

```bash
# Einzelne URL
docker exec -it seo-api python example_usage.py https://example.com

# Mehrere URLs (Batch)
docker exec -it seo-api python example_usage.py \
  https://site1.com \
  https://site2.com \
  https://site3.com

# Competitive Analysis
docker exec -it seo-api python example_usage.py --compare \
  https://yoursite.com \
  https://competitor1.com \
  https://competitor2.com
```

### Methode 3: Als Python-Modul

```python
from seo_analyzer import SEOAnalyzer

# Initialize
analyzer = SEOAnalyzer()

# Crawl
pages = analyzer.crawl_website("https://example.com", max_pages=20)

# Analyze Topics
topics = analyzer.extract_topics(pages)

# Analyze Domain
metrics = analyzer.analyze_domain("example.com")

# Calculate Score
score = analyzer.calculate_topical_authority_score(topics, metrics)

# Generate Reports
analyzer.generate_report("https://example.com", pages, topics, metrics, score)
```

## 📊 Was bekommst du?

### 1. Topical Authority Score (0-100)

Gewichtete Berechnung aus:
- **33.3%** Semantic Relevance (Wie zusammenhängend sind die Inhalte?)
- **33.3%** Topical Consistency (Wie fokussiert sind die Themen?)
- **33.3%** Backlink Quality (DA, Spam Score, Root Domains)
- **+Bonus** Domain Age (bis zu 10 Punkte)

**Grading:**
- 90-100: A+ (Exceptional)
- 80-89: A (Strong)
- 70-79: B (Good)
- 60-69: C (Moderate)
- 50-59: D (Fair)
- 0-49: F (Weak)

### 2. Topic Analysis

Für jedes identifizierte Topic:
- 📝 Document Count
- 🔑 Top 10 Keywords (mit Scores)
- 📄 Sample URLs
- 💬 Representative Text

### 3. Domain Metrics

- **Moz Metrics**: DA, PA, Spam Score, Backlinks
- **WHOIS Data**: Domain Age, Registrar, Creation Date
- **Structure**: Subdomain, TLD Category

### 4. Visual Reports

- **HTML Report**: Professioneller Report mit allen Details
- **Charts**: Topic Distribution, Score Breakdown
- **Tables**: Crawled Pages, Keywords, Recommendations

## 📈 Beispiel-Output

```
🚀 ADVANCED SEO ANALYZER
========================================

🕷️  Crawling website: https://example.com
  📄 Crawling: https://example.com/
  📄 Crawling: https://example.com/about
✅ Crawled 15 pages successfully!

🧠 Performing topical analysis...
  🔢 Generating sentence embeddings...
  🔍 Clustering topics with BERTopic...
  🔑 Extracting semantic keywords with KeyBERT...
✅ Found 3 distinct topics!

🔍 Analyzing domain: example.com
  📊 Fetching Moz metrics...
  🔎 Fetching WHOIS data...
✅ Domain analysis complete!

🎯 Calculating Topical Authority Score...
✅ Topical Authority Score: 58.30 (D)

📊 Generating reports...
  ✅ Saved topics.json
  ✅ Saved domain_metrics.json
  ✅ Saved topic_distribution.png
  ✅ Saved authority_breakdown.png
  ✅ Saved report.html
✅ All reports generated successfully!

========================================
   ✅ ANALYSIS COMPLETE!
========================================

📊 TOPICAL AUTHORITY SCORE: 58.30 (D)

📝 Total Pages Analyzed: 15
🧠 Topics Identified: 3
🔗 Domain Authority: 93
📅 Domain Age: 30.15 years

💡 Interpretation:
   Fair topical authority; significant improvements 
   needed in multiple areas
```

## 🔧 Konfiguration

### Environment Variables

```bash
export MOZ_ACCESS_ID="your-moz-access-id"
export MOZ_SECRET_KEY="your-moz-secret-key"
```

Oder in `.env` Datei (bereits vorhanden):
```
MOZ_ACCESS_ID=mozscape-8u2uAjdQpV
MOZ_SECRET_KEY=MCeFg5jtmrLGcpNlNOUfOrX0G7RLttZC
```

### Parameter anpassen

In `seo_analyzer.py`:
```python
MAX_PAGES = 20              # Anzahl zu crawlender Seiten
REQUEST_TIMEOUT = 10        # HTTP Timeout
min_topic_size = 2          # Min. Dokumente pro Topic
```

## 📚 Dokumentation

- **`SEO_ANALYZER_GUIDE.md`** - Vollständige technische Dokumentation
- **`IMPLEMENTATION_SUMMARY.md`** - Implementation Details
- **`seo_analyzer.py`** - Haupt-Skript (1000+ Zeilen, voll dokumentiert)
- **`example_usage.py`** - Beispiel-Verwendungen

## 🧪 Testing

```bash
# Vollständiger Test
./test_seo_analyzer.sh

# Schneller Test (nur 5 Seiten)
docker exec seo-api python -c "
from seo_analyzer import SEOAnalyzer
analyzer = SEOAnalyzer()
pages = analyzer.crawl_website('https://example.com', max_pages=5)
print(f'✅ Crawled {len(pages)} pages')
"
```

## 💡 Use Cases

1. **SEO Audit**: Vollständige Analyse Ihrer Website
2. **Competitor Analysis**: Vergleichen Sie sich mit Konkurrenz
3. **Content Strategy**: Identifizieren Sie Themenlücken
4. **Topic Research**: Verstehen Sie Ihre Content-Struktur
5. **Authority Building**: Messen Sie Fortschritt über Zeit

## ⚡ Performance

- **Crawling**: ~0.5-1s pro Seite
- **Topic Analysis**: ~5-10s für 20 Seiten
- **Total Time**: ~30-60s für komplette Analyse

## 🐛 Troubleshooting

### "No pages could be crawled"
- Prüfen Sie robots.txt der Website
- Erhöhen Sie REQUEST_TIMEOUT
- Website könnte Bots blockieren

### "Moz API error"
- Überprüfen Sie MOZ_ACCESS_ID und MOZ_SECRET_KEY
- Checken Sie Ihr monatliches API-Limit (Free: 2,500 rows)

### "Not enough documents for topics"
- Erhöhen Sie MAX_PAGES
- Reduzieren Sie min_topic_size
- Website hat möglicherweise zu wenig Content

### "Import error"
- Container neu builden: `docker compose up --build -d`
- Alle Dependencies sollten automatisch installiert werden

## 📞 Support

Bei Fragen oder Problemen:
1. Prüfen Sie die Dokumentation in `SEO_ANALYZER_GUIDE.md`
2. Lesen Sie `IMPLEMENTATION_SUMMARY.md` für technische Details
3. Schauen Sie sich `example_usage.py` für Beispiele an

## 🎉 Quick Start Checklist

- [ ] Docker Container gebaut (`docker compose up --build -d`)
- [ ] Test ausgeführt (`./test_seo_analyzer.sh`)
- [ ] MOZ API Credentials gesetzt (in `.env`)
- [ ] Erste Analyse durchgeführt
- [ ] HTML Report geöffnet

## 🚀 Jetzt starten!

```bash
# 1. Container starten
docker compose up -d

# 2. Erste Analyse
docker exec -it seo-api python seo_analyzer.py https://yourwebsite.com

# 3. Report öffnen
open report.html
```

---

**Viel Erfolg mit Ihrer SEO-Analyse!** 🎯
