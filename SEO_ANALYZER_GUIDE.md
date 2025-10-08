# 🚀 Advanced SEO Analyzer - Complete Guide

## Overview

Der **Advanced SEO Analyzer** ist ein hochmodernes Python-Tool, das maschinelles Lernen und NLP verwendet, um tiefgreifende SEO-Analysen durchzuführen.

## 🎯 Hauptfunktionen

### 1. **Topical Analysis (Thematische Analyse)**
- Nutzt **BERTopic** für intelligentes Topic Clustering
- Identifiziert Hauptthemen Ihrer Website automatisch
- Berechnet thematische Konsistenz und semantische Relevanz

### 2. **Semantic Keyword Extraction**
- **KeyBERT** extrahiert die semantisch relevantesten Keywords
- Top 10 Keywords pro Topic mit Relevanz-Scores
- Berücksichtigt Kontext und Bedeutung, nicht nur Häufigkeit

### 3. **Domain Authority Estimation**
- Integration mit **Moz API** für echte DA/PA-Werte
- Backlink-Profil-Analyse
- WHOIS-Daten für Domain-Alter und Registrierungsinformationen

### 4. **Custom Topical Authority Score**
Berechnet einen gewichteten Score aus:
- **Semantic Relevance** (33.3%) - Wie zusammenhängend sind die Inhalte?
- **Topical Consistency** (33.3%) - Wie fokussiert sind die Themen?
- **Backlink Quality** (33.3%) - Wie autoritativ sind die Backlinks?
- **Domain Age Bonus** (bis zu 10 Bonuspunkte)

### 5. **Visual Reports**
- Interaktive HTML-Berichte
- Topic Distribution Charts
- Authority Score Breakdown
- Professionelle Visualisierungen

## 📋 Anforderungen

### Python-Bibliotheken

```bash
# NLP & Topic Modeling
sentence-transformers==2.7.0  # Sentence embeddings
bertopic==0.16.0              # Topic clustering
keybert==0.8.4                # Keyword extraction
umap-learn==0.5.5             # Dimensionality reduction
hdbscan==0.8.33               # Clustering algorithm

# Domain Analysis
python-whois==0.9.4           # WHOIS lookups
tldextract==5.1.2             # Domain parsing

# Visualization
matplotlib==3.9.0             # Static charts
plotly==5.22.0                # Interactive plots
kaleido==0.2.1                # Export plots

# Core Data Science
numpy==1.26.4
pandas==2.2.2
scikit-learn==1.5.1
scipy==1.13.1

# Web Scraping
requests==2.32.3
beautifulsoup4==4.12.3
```

### Umgebungsvariablen

```bash
export MOZ_ACCESS_ID="your-moz-access-id"
export MOZ_SECRET_KEY="your-moz-secret-key"
```

Oder in `.env` Datei:
```
MOZ_ACCESS_ID=mozscape-8u2uAjdQpV
MOZ_SECRET_KEY=MCeFg5jtmrLGcpNlNOUfOrX0G7RLttZC
```

## 🚀 Verwendung

### Methode 1: Kommandozeile

```bash
# Im Docker-Container
docker exec -it seo-api python seo_analyzer.py https://example.com

# Oder direkt (wenn Python lokal installiert)
cd apps/api
python seo_analyzer.py https://example.com
```

### Methode 2: Als Python-Modul

```python
from seo_analyzer import SEOAnalyzer

# Initialisieren
analyzer = SEOAnalyzer(
    moz_access_id="your-id",
    moz_secret_key="your-key"
)

# Website crawlen
pages = analyzer.crawl_website("https://example.com", max_pages=20)

# Topics extrahieren
topics = analyzer.extract_topics(pages)

# Domain analysieren
domain_metrics = analyzer.analyze_domain("example.com")

# Topical Authority Score berechnen
score = analyzer.calculate_topical_authority_score(topics, domain_metrics)

# Report generieren
analyzer.generate_report(
    url="https://example.com",
    pages_data=pages,
    topic_data=topics,
    domain_metrics=domain_metrics,
    authority_score=score
)
```

## 📊 Output-Dateien

Nach der Analyse werden folgende Dateien erstellt:

### 1. `topics.json`
```json
{
  "url": "https://example.com",
  "analysis_date": "2025-10-07T10:30:00",
  "total_pages_analyzed": 15,
  "topics": [
    {
      "topic_id": 0,
      "document_count": 8,
      "keybert_keywords": [
        {"keyword": "machine learning", "score": 0.7234},
        {"keyword": "artificial intelligence", "score": 0.6891}
      ],
      "bertopic_keywords": ["ai", "ml", "data", "model"],
      "sample_urls": ["https://example.com/page1"]
    }
  ],
  "metrics": {
    "total_topics": 3,
    "topical_consistency": 0.78,
    "semantic_relevance": 0.82
  }
}
```

### 2. `domain_metrics.json`
```json
{
  "domain": "example.com",
  "timestamp": "2025-10-07T10:35:00",
  "moz": {
    "domain_authority": 93,
    "page_authority": 83,
    "spam_score": 47,
    "root_domains_linking": 499901
  },
  "whois": {
    "registrar": "MarkMonitor Inc.",
    "creation_date": "1995-08-14",
    "domain_age_years": 30.15
  }
}
```

### 3. `report.html`
Umfassender HTML-Report mit:
- Executive Summary
- Topical Authority Score Card
- Score Component Breakdown
- Domain Metrics Dashboard
- Topic Distribution Visualizations
- Detailed Topic Analysis
- Crawled Pages Summary
- Actionable Recommendations

### 4. `topic_distribution.png`
Pie Chart der Topic-Verteilung + Top Keywords

### 5. `authority_breakdown.png`
Bar Chart der Score-Komponenten

## 🧮 Score-Berechnung

### Topical Authority Score Formel:

```
Base Score = (Semantic Relevance + Topical Consistency + Backlink Quality) / 3

Final Score = Base Score + Domain Age Bonus (max 10 points)
```

### Komponenten:

#### 1. Semantic Relevance (0-100)
- Durchschnittliche Cosinus-Ähnlichkeit innerhalb von Topics
- Misst, wie semantisch zusammenhängend die Inhalte sind
- Höher = Inhalte sind thematisch kohärent

#### 2. Topical Consistency (0-100)
- Basiert auf Shannon-Entropie der Topic-Verteilung
- Misst, wie fokussiert die Website ist
- Höher = Wenige, gut definierte Topics statt vieler zersplitterter Themen

#### 3. Backlink Quality (0-100)
```
Backlink Quality = (DA * 0.5) + (Spam Penalty * 0.2) + (Backlink Score * 0.3)

Wobei:
- DA = Domain Authority (0-100)
- Spam Penalty = 100 - (Spam Score * 2)
- Backlink Score = min(log(root_domains) * 10, 100)
```

#### 4. Domain Age Bonus (0-10)
```
Age Bonus = min(domain_age_years * 2, 10)
```

### Score-Interpretation:

| Score | Grade | Bedeutung |
|-------|-------|-----------|
| 90-100 | A+ | Exceptional - Top-Tier Authority |
| 80-89 | A | Strong Authority |
| 70-79 | B | Good Authority |
| 60-69 | C | Moderate Authority |
| 50-59 | D | Fair - Needs Work |
| 0-49 | F | Weak - Major Improvements Needed |

## 🎨 Visualisierung Features

### Topic Distribution Chart
- Pie Chart zeigt prozentuale Verteilung der Topics
- Farbcodiert für einfache Identifikation
- Includes document counts

### Authority Breakdown
- Horizontales Bar Chart
- Zeigt alle 4 Score-Komponenten
- Farbcodiert nach Wert
- Mit numerischen Labels

### HTML Report
- Responsive Design
- Gradient Color Schemes
- Interactive Elements
- Professional Layout
- Print-Friendly

## 🔧 Konfiguration

### Anpassbare Parameter:

```python
# In seo_analyzer.py:

MAX_PAGES = 20              # Maximale Anzahl zu crawlender Seiten
REQUEST_TIMEOUT = 10        # Timeout für HTTP-Requests (Sekunden)
USER_AGENT = "..."          # Custom User-Agent

# BERTopic-Parameter:
min_topic_size = 2          # Minimum Dokumente pro Topic
n_neighbors = 15            # UMAP neighbors
n_components = 5            # UMAP dimensions

# KeyBERT-Parameter:
top_n = 10                  # Top N Keywords
keyphrase_ngram_range = (1, 3)  # Unigrams bis Trigrams
diversity = 0.5             # Keyword Diversity (0-1)
```

## 📈 Best Practices

### 1. Optimal Page Count
- **Minimum**: 10 Seiten für aussagekräftige Ergebnisse
- **Empfohlen**: 20-50 Seiten
- **Maximum**: 100+ Seiten (aber langsam)

### 2. Rate Limiting
- Skript wartet 0.5s zwischen Requests
- Bei großen Sites: Erhöhen Sie die Wartezeit
- Respektieren Sie `robots.txt`

### 3. Moz API Limits
- Free Tier: 2,500 Rows/Monat
- Verwenden Sie Caching für häufige Domains
- Batch-Analysen für Effizienz

### 4. Model Performance
- Sentence Transformer lädt beim ersten Start (~90MB)
- Nutzen Sie GPU für schnellere Embeddings (optional)
- BERTopic benötigt min. 10 Dokumente für gute Ergebnisse

## 🐛 Troubleshooting

### Fehler: "No pages could be crawled"
**Lösung:**
- Überprüfen Sie Robots.txt
- Erhöhen Sie `REQUEST_TIMEOUT`
- Prüfen Sie User-Agent-Blocking

### Fehler: "BERTopic failed - not enough documents"
**Lösung:**
- Erhöhen Sie `MAX_PAGES`
- Reduzieren Sie `min_topic_size`
- Website hat möglicherweise zu wenig Inhalt

### Fehler: "Moz API error"
**Lösung:**
- Überprüfen Sie Credentials
- Checken Sie API-Limits
- Verwenden Sie korrekte Domain-Format

### Fehler: "WHOIS lookup failed"
**Lösung:**
- Manche Domains blockieren WHOIS
- Private Registrations zeigen keine Daten
- Skript läuft trotzdem weiter

## 🔬 Wissenschaftliche Grundlagen

### BERTopic
- **Paper**: "BERTopic: Neural topic modeling with a class-based TF-IDF procedure"
- **Methode**: BERT embeddings → UMAP → HDBSCAN → c-TF-IDF
- **Vorteil**: Berücksichtigt semantische Bedeutung, nicht nur Worthäufigkeit

### KeyBERT
- **Basis**: BERT sentence transformers
- **Methode**: Cosine similarity zwischen document und candidate keywords
- **Vorteil**: Extrahiert semantisch relevante Keywords, auch Synonyme

### Sentence Transformers
- **Model**: all-MiniLM-L6-v2
- **Dimension**: 384
- **Performance**: Fast, accurate, lightweight
- **Use Case**: Perfekt für SEO-Text-Analyse

## 📚 Beispiel-Workflow

```python
#!/usr/bin/env python3
import os
from seo_analyzer import SEOAnalyzer

# Setup
os.environ['MOZ_ACCESS_ID'] = 'your-id'
os.environ['MOZ_SECRET_KEY'] = 'your-key'

# Initialize
analyzer = SEOAnalyzer()

# Analyze
url = "https://yourwebsite.com"
pages = analyzer.crawl_website(url, max_pages=30)
topics = analyzer.extract_topics(pages, min_topic_size=3)
domain = analyzer.analyze_domain("yourwebsite.com")
score = analyzer.calculate_topical_authority_score(topics, domain)

# Generate reports
analyzer.generate_report(url, pages, topics, domain, score)

print(f"✅ Score: {score['topical_authority_score']} ({score['grade']})")
print(f"📊 Topics: {topics['total_topics']}")
print(f"🔗 DA: {domain['moz']['domain_authority']}")
```

## 🌟 Use Cases

1. **Competitor Analysis**: Vergleichen Sie Ihre Topical Authority mit Konkurrenten
2. **Content Strategy**: Identifizieren Sie Content Gaps und Opportunities
3. **SEO Audits**: Umfassende technische und thematische SEO-Analyse
4. **Topic Clustering**: Verstehen Sie die Content-Struktur Ihrer Website
5. **Keyword Research**: Entdecken Sie semantisch relevante Keywords
6. **Authority Building**: Messen Sie die Auswirkung von Content und Backlinks

## 📞 Support & Dokumentation

- **GitHub**: [Ihre GitHub URL]
- **Dokumentation**: Diese README
- **Issues**: GitHub Issues
- **Moz API Docs**: https://moz.com/api
- **BERTopic Docs**: https://maartengr.github.io/BERTopic/

## 📄 Lizenz

MIT License - Frei verwendbar für kommerzielle und private Projekte.

---

**Created by**: SEO Analysis Team  
**Last Updated**: Oktober 2025  
**Version**: 1.0.0
