# 🚀 Screaming Frog Automation - Quick Start

Get up and running with Screaming Frog automation in 5 minutes!

---

## ⚡ Prerequisites

1. **Screaming Frog SEO Spider** (with CLI license)
   - Download: https://www.screamingfrog.co.uk/seo-spider/
   - License: $259/year for CLI access

2. **Python Dependencies**
   ```bash
   pip install pandas requests urllib3
   ```

---

## 🎯 Quick Setup (3 Steps)

### Step 1: Configure Environment

Copy the template:
```bash
cp .env.screamingfrog .env.screamingfrog.local
```

Edit `.env.screamingfrog.local`:
```bash
# Required
TARGET_URL=https://bs-company.ch

# Auto-detected (verify path)
SF_BIN=/Applications/Screaming Frog SEO Spider.app/Contents/MacOS/ScreamingFrogSEOSpiderCli

# Optional: Supabase upload
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_service_role_key
```

### Step 2: Create Supabase Table (Optional)

```bash
# Run the SQL schema
psql your_database < infra/supabase/seo_crawl_pages.sql

# Or in Supabase dashboard:
# 1. Go to SQL Editor
# 2. Paste contents of seo_crawl_pages.sql
# 3. Run
```

### Step 3: Run Your First Crawl

```bash
# Load environment
source .env.screamingfrog.local

# Run crawl
python apps/api/crawl_and_ingest.py
```

Tip: TARGET_URL is resolved with priority: `--target-url` flag > `TARGET_URL` env > `data/target_url.txt` > default.
Examples:

```bash
# Highest priority: CLI flag
python apps/api/crawl_and_ingest.py --target-url https://example.com

# From env
TARGET_URL=https://example.com python apps/api/crawl_and_ingest.py

# From file (first line)
echo "https://example.com" > data/target_url.txt
python apps/api/crawl_and_ingest.py
```

---

## 📊 What You Get

After running, check the `reports/` directory:

```
reports/20251007_213045/
├── crawl.log                  # Detailed execution log
├── internal_all.csv           # Raw Screaming Frog data
├── page_titles_all.csv        # Page titles
├── meta_description_all.csv   # Meta descriptions
├── normalized_pages.csv       # ✨ Clean merged data
└── summary.json              # ✨ Statistics
```

### View Summary

```bash
cat reports/20251007_213045/summary.json | python -m json.tool
```

Output:
```json
{
  "total_pages": 245,
  "pages_200": 240,
  "indexable_pages": 238,
  "pages_with_titles": 245,
  "pages_with_descriptions": 230,
  "avg_word_count": 487.5
}
```

---

## 🤖 Automate It

### Cron (macOS/Linux)

```bash
# Edit crontab
crontab -e

# Add daily crawl at 2 AM
0 2 * * * cd /path/to/seo-analyzer-starter && ./scripts/run_screaming_frog_crawl.sh
```

### Task Scheduler (Windows)

1. Open Task Scheduler
2. Create Basic Task
3. Schedule: Daily at 2:00 AM
4. Action: `scripts\run_screaming_frog_crawl.bat`

### n8n

Import workflow:
```bash
# Import the JSON file in n8n
infra/n8n/screaming_frog_workflow.json
```

---

## 🔧 Common Commands

```bash
# Manual crawl with custom URL
TARGET_URL=https://example.com python apps/api/crawl_and_ingest.py

# Crawl with higher depth
MAX_CRAWL_DEPTH=5 python apps/api/crawl_and_ingest.py

# Crawl more pages
MAX_PAGES=5000 python apps/api/crawl_and_ingest.py

# Skip Supabase upload
SUPABASE_URL="" python apps/api/crawl_and_ingest.py

# View latest crawl summary
cat reports/$(ls -t reports | head -1)/summary.json
```

---

## 📈 Analyze Your Data

### Load in Python

```python
import pandas as pd

# Load latest crawl
df = pd.read_csv('reports/20251007_213045/normalized_pages.csv')

# Find issues
print(f"Missing titles: {(df['title'] == '').sum()}")
print(f"Missing descriptions: {(df['description'] == '').sum()}")
print(f"Thin content (<300 words): {(df['word_count'] < 300).sum()}")
print(f"404 errors: {(df['status_code'] == 404).sum()}")
```

### Query in Supabase

```sql
-- Find pages with issues
SELECT url, title, description, word_count
FROM seo_crawl_pages
WHERE status_code = 200
  AND (title = '' OR description = '' OR word_count < 300);

-- Status distribution
SELECT status_code, COUNT(*) as count
FROM seo_crawl_pages
GROUP BY status_code;
```

---

## ❓ Troubleshooting

### "Screaming Frog CLI not found"

```bash
# Find your installation
# macOS
find /Applications -name "ScreamingFrogSEOSpiderCli" 2>/dev/null

# Update SF_BIN in .env file
SF_BIN=/path/to/ScreamingFrogSEOSpiderCli
```

### "License required"

CLI mode requires paid license:
- Visit: https://www.screamingfrog.co.uk/seo-spider/pricing/
- Purchase: CLI license ($259/year)
- Activate: Enter license in Screaming Frog GUI

### "No export files found"

Check the crawl log:
```bash
tail -f reports/$(ls -t reports | head -1)/crawl.log
```

Common causes:
- Invalid URL
- Network issues
- Insufficient permissions
- CLI path incorrect

---

## 📚 Next Steps

1. **Read Full Guide**: See `SCREAMING_FROG_GUIDE.md` for complete documentation
2. **Setup Automation**: Use cron/Task Scheduler for daily crawls
3. **Create Dashboard**: Build visualizations with your crawl data
4. **Add Topical Analysis**: Integrate KeyBERT/BERTopic
5. **Monitor Changes**: Compare crawls over time

---

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| Run crawl | `python apps/api/crawl_and_ingest.py` |
| Custom URL | `TARGET_URL=https://example.com python apps/api/crawl_and_ingest.py` |
| View summary | `cat reports/$(ls -t reports \| head -1)/summary.json` |
| Load data | `df = pd.read_csv('reports/latest/normalized_pages.csv')` |
| Automate | `./scripts/run_screaming_frog_crawl.sh` |

---

## 📞 Support

- **Screaming Frog Docs**: https://www.screamingfrog.co.uk/seo-spider/user-guide/
- **Full Guide**: See `SCREAMING_FROG_GUIDE.md`
- **Issues**: Check logs in `reports/*/crawl.log`

---

**Ready?** Run your first crawl:
```bash
source .env.screamingfrog.local && python apps/api/crawl_and_ingest.py
```

Happy crawling! 🕷️✨
