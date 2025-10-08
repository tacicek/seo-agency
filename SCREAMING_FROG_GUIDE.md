# Screaming Frog SEO Spider Automation

## 🎯 Overview

Production-ready Python system that integrates **Screaming Frog SEO Spider CLI** to automatically crawl websites, normalize data with pandas, and upload to Supabase for analysis.

### Features

✅ **Headless Crawling** - Automated website crawling with Screaming Frog CLI  
✅ **Data Normalization** - Clean and structured data with pandas  
✅ **Supabase Integration** - Automatic data upload to cloud database  
✅ **Timestamped Reports** - Organized output in dated directories  
✅ **Error Handling** - Robust logging and error recovery  
✅ **Cross-Platform** - Works on macOS, Windows, and Linux  
✅ **Automation Ready** - Compatible with cron, Task Scheduler, and n8n  

---

## 📦 Prerequisites

### 1. Screaming Frog SEO Spider

**Download**: https://www.screamingfrog.co.uk/seo-spider/

#### Installation Paths:

- **macOS**: `/Applications/Screaming Frog SEO Spider.app/Contents/MacOS/ScreamingFrogSEOSpiderCli`
- **Windows**: `C:\Program Files\Screaming Frog SEO Spider\ScreamingFrogSEOSpiderCli.exe`
- **Linux**: `/usr/local/bin/ScreamingFrogSEOSpiderCli`

**License Required**: CLI mode requires a paid license ($259/year)

### 2. Python Dependencies

```bash
pip install pandas requests urllib3
```

Or add to `requirements.txt`:
```
pandas>=2.0.0
requests>=2.31.0
urllib3>=2.0.0
```

---

## ⚙️ Setup

### Step 1: Configuration

Copy the environment template:
```bash
cp .env.screamingfrog .env.screamingfrog.local
```

Edit `.env.screamingfrog.local` with your settings:

```bash
# Target website
TARGET_URL=https://bs-company.ch

# Screaming Frog binary path
SF_BIN=/Applications/Screaming Frog SEO Spider.app/Contents/MacOS/ScreamingFrogSEOSpiderCli

# Reports directory
REPORTS_DIR=./reports

# Crawl settings
MAX_CRAWL_DEPTH=3
MAX_PAGES=1000

# Supabase (optional)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_service_role_key
SUPABASE_TABLE=seo_crawl_pages
```

### Central TARGET_URL resolution (global)

The system resolves the crawl target dynamically with a single, global policy:

Priority order:

1. CLI argument: `--target-url https://example.com`
2. Environment variable: `TARGET_URL=https://example.com`
3. File fallback: first line of `data/target_url.txt`
4. Built-in default: `https://bs-company.ch`

Examples:

- Use CLI flag (highest priority):
  - macOS/Linux: `python apps/api/crawl_and_ingest.py --target-url https://example.com`
  - Windows: `python apps\\api\\crawl_and_ingest.py --target-url https://example.com`

- Use environment variable:
  - `export TARGET_URL=https://example.com && python apps/api/crawl_and_ingest.py`

- Use file fallback (no arg/env needed):
  - Put your domain into `data/target_url.txt` (first line only)
  - Run: `python apps/api/crawl_and_ingest.py`

### Step 2: Create Supabase Table (Optional)

If using Supabase, create the table:

```sql
CREATE TABLE seo_crawl_pages (
  id BIGSERIAL PRIMARY KEY,
  url TEXT NOT NULL,
  status_code INTEGER,
  title TEXT,
  description TEXT,
  h1 TEXT,
  word_count INTEGER,
  content_type TEXT,
  indexability TEXT,
  crawl_timestamp TIMESTAMPTZ DEFAULT NOW(),
  source_domain TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for better performance
CREATE INDEX idx_seo_crawl_url ON seo_crawl_pages(url);
CREATE INDEX idx_seo_crawl_status ON seo_crawl_pages(status_code);
CREATE INDEX idx_seo_crawl_timestamp ON seo_crawl_pages(crawl_timestamp);

-- Enable RLS (optional)
ALTER TABLE seo_crawl_pages ENABLE ROW LEVEL SECURITY;
```

Save as `infra/supabase/seo_crawl_pages.sql`

---

## 🚀 Usage

### Basic Usage

```bash
# Set environment variables
export TARGET_URL=https://bs-company.ch

# Run crawl
python apps/api/crawl_and_ingest.py
```

### With Environment File

```bash
# Load variables from file
source .env.screamingfrog.local

# Run crawl
python apps/api/crawl_and_ingest.py
```

### Docker Usage

```bash
# Add to existing docker-compose.yml
docker exec -it seo-api python crawl_and_ingest.py
```

---

## 📊 Output Structure

Each crawl creates a timestamped directory:

```
reports/
└── 20251007_213045/
    ├── crawl.log                      # Detailed logs
    ├── internal_all.csv               # Raw Screaming Frog export
    ├── page_titles_all.csv            # Page titles
    ├── meta_description_all.csv       # Meta descriptions
    ├── h1_all.csv                     # H1 tags
    ├── h2_all.csv                     # H2 tags
    ├── images_all.csv                 # Images
    ├── normalized_pages.csv           # ✨ Cleaned & merged data
    └── summary.json                   # ✨ Statistics
```

### Normalized CSV Columns

```csv
url,status_code,title,description,h1,word_count,content_type,indexability,crawl_timestamp,source_domain
https://bs-company.ch/,200,"Home Page","Welcome to BS Company","Main Heading",450,text/html,Indexable,2025-10-07T21:30:45,https://bs-company.ch
```

### Summary JSON

```json
{
  "crawl_timestamp": "2025-10-07T21:30:45",
  "target_url": "https://bs-company.ch",
  "total_pages": 245,
  "pages_by_status": {
    "200": 240,
    "301": 3,
    "404": 2
  },
  "pages_200": 240,
  "indexable_pages": 238,
  "pages_with_titles": 245,
  "pages_with_descriptions": 230,
  "avg_word_count": 487.5
}
```

---

## 🤖 Automation

### Cron (macOS/Linux)

```bash
# Edit crontab
crontab -e

# Add daily crawl at 2 AM
0 2 * * * cd /path/to/seo-analyzer-starter && source .env.screamingfrog.local && python apps/api/crawl_and_ingest.py >> logs/cron.log 2>&1
```

### Task Scheduler (Windows)

Create `run_crawl.bat`:
```batch
@echo off
cd C:\path\to\seo-analyzer-starter
call .env.screamingfrog.local
python apps\api\crawl_and_ingest.py >> logs\cron.log 2>&1
```

Schedule in Task Scheduler:
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily at 2:00 AM
4. Action: Start a program → `run_crawl.bat`

### n8n Workflow

```json
{
  "nodes": [
    {
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.scheduleTrigger",
      "parameters": {
        "rule": {
          "interval": [{ "field": "cronExpression", "expression": "0 2 * * *" }]
        }
      }
    },
    {
      "name": "Execute Python Script",
      "type": "n8n-nodes-base.executeCommand",
      "parameters": {
        "command": "cd /path/to/seo-analyzer-starter && python apps/api/crawl_and_ingest.py"
      }
    },
    {
      "name": "Send Notification",
      "type": "n8n-nodes-base.emailSend",
      "parameters": {
        "subject": "SEO Crawl Completed",
        "text": "Crawl finished successfully!"
      }
    }
  ]
}
```

---

## 🔧 Advanced Configuration

### Custom Export Types

Edit `run_screaming_frog()` function to customize exports:

```python
'--export-tabs', 'Internal:All,PageTitles:All,MetaDescription:All,H1:All,H2:All,Images:All,Canonicals:All,Hreflang:All'
```

Available exports:
- Internal/External/All
- PageTitles
- MetaDescription
- H1/H2
- Images
- Canonicals
- Hreflang
- URIs
- Custom Extraction

### Crawl Settings

```python
# Maximum crawl depth
MAX_CRAWL_DEPTH=5

# Maximum pages to crawl
MAX_PAGES=5000

# Additional CLI options
--respect-nofollow
--respect-robots-txt
--user-agent "CustomBot/1.0"
--config /path/to/config.seospiderconfig
```

### Batch Upload Optimization

```python
# Increase batch size for faster uploads
BATCH_SIZE=1000

# Or use direct database connection (faster)
# Instead of REST API, use psycopg2 for bulk insert
```

---

## 📈 Data Analysis Examples

### Load Crawl Data

```python
import pandas as pd
import json

# Load normalized data
df = pd.read_csv('reports/20251007_213045/normalized_pages.csv')

# Load summary
with open('reports/20251007_213045/summary.json') as f:
    summary = json.load(f)

print(f"Total pages: {summary['total_pages']}")
print(f"200 status: {summary['pages_200']}")
```

### Find Issues

```python
# Pages without titles
no_titles = df[df['title'] == '']
print(f"Missing titles: {len(no_titles)}")

# Pages without descriptions
no_desc = df[df['description'] == '']
print(f"Missing descriptions: {len(no_desc)}")

# Thin content (< 300 words)
thin_content = df[df['word_count'] < 300]
print(f"Thin content pages: {len(thin_content)}")

# 404 errors
errors = df[df['status_code'] == 404]
print(f"404 errors: {len(errors)}")
```

### Query Supabase

```sql
-- Find pages with issues
SELECT url, title, description, word_count
FROM seo_crawl_pages
WHERE status_code = 200
  AND (title IS NULL OR title = '')
  OR (description IS NULL OR description = '')
  OR word_count < 300;

-- Status code distribution
SELECT status_code, COUNT(*) as count
FROM seo_crawl_pages
GROUP BY status_code
ORDER BY count DESC;

-- Recent crawls
SELECT 
  source_domain,
  crawl_timestamp,
  COUNT(*) as total_pages
FROM seo_crawl_pages
GROUP BY source_domain, crawl_timestamp
ORDER BY crawl_timestamp DESC;
```

---

## 🔍 Troubleshooting

### Error: "Screaming Frog CLI not found"

**Solution**: Set correct path in environment variable:
```bash
export SF_BIN="/Applications/Screaming Frog SEO Spider.app/Contents/MacOS/ScreamingFrogSEOSpiderCli"
```

### Error: "License required"

**Solution**: CLI mode requires paid license. Purchase at:
https://www.screamingfrog.co.uk/seo-spider/pricing/

### Error: "No export files found"

**Possible causes**:
1. Crawl failed - check `crawl.log`
2. Wrong export folder - verify `REPORTS_DIR`
3. Export settings incorrect - check CLI command

### Slow Crawls

**Optimize**:
```bash
# Reduce crawl depth
MAX_CRAWL_DEPTH=2

# Limit page count
MAX_PAGES=500

# Use crawl config file
--config fast_crawl.seospiderconfig
```

### Supabase Upload Fails

**Common issues**:
1. Invalid API key - check `SUPABASE_KEY`
2. Table doesn't exist - run SQL schema
3. Rate limiting - reduce `BATCH_SIZE`

---

## 🎯 Next Steps

### 1. Add Topical Analysis

```python
from keybert import KeyBERT
from bertopic import BERTopic

# Extract keywords
kw_model = KeyBERT()
keywords = kw_model.extract_keywords(df['description'], top_n=10)

# Topic modeling
topic_model = BERTopic()
topics, probs = topic_model.fit_transform(df['description'])

# Add to DataFrame
df['topics'] = topics
```

### 2. Monitor Changes

```python
# Compare with previous crawl
df_old = pd.read_csv('reports/20251006_210000/normalized_pages.csv')
df_new = pd.read_csv('reports/20251007_210000/normalized_pages.csv')

# Find new pages
new_pages = set(df_new['url']) - set(df_old['url'])

# Find removed pages
removed_pages = set(df_old['url']) - set(df_new['url'])

# Find title changes
merged = df_old.merge(df_new, on='url', suffixes=('_old', '_new'))
title_changes = merged[merged['title_old'] != merged['title_new']]
```

### 3. Create Dashboard

```python
import plotly.express as px

# Status code distribution
fig = px.bar(
    df['status_code'].value_counts(),
    title='Status Code Distribution'
)

# Word count distribution
fig = px.histogram(
    df, x='word_count',
    title='Word Count Distribution'
)
```

---

## 📚 References

- **Screaming Frog CLI Docs**: https://www.screamingfrog.co.uk/seo-spider/user-guide/general/#cli
- **Pandas Documentation**: https://pandas.pydata.org/docs/
- **Supabase REST API**: https://supabase.com/docs/guides/api

---

## 🤝 Contributing

Improvements welcome! Areas for enhancement:

- [ ] Parallel crawling for multiple domains
- [ ] Real-time progress monitoring
- [ ] Email notifications
- [ ] Slack/Discord webhooks
- [ ] Automated issue detection
- [ ] Historical trend analysis
- [ ] A/B testing for SEO changes

---

## 📄 License

MIT License - Use freely for personal and commercial projects.

---

**Created by**: SEO Automation Engineer  
**Version**: 1.0.0  
**Last Updated**: 2025-10-07
