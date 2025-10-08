import os, json, time, requests

DATA_DIR = os.path.abspath(os.path.join(os.getcwd(), "..", "..", "data"))
os.makedirs(DATA_DIR, exist_ok=True)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

def save_report(report: dict) -> str:
    report_id = str(int(time.time() * 1000))
    # Try Supabase (optional)
    if SUPABASE_URL and SUPABASE_SERVICE_KEY:
        try:
            # Assumes a table 'seo_reports' with columns: id (text), payload (jsonb), created_at (timestamp default now())
            url = f"{SUPABASE_URL}/rest/v1/seo_reports"
            headers = {
                "apikey": SUPABASE_SERVICE_KEY,
                "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=representation"
            }
            payload = {"id": report_id, "payload": report}
            r = requests.post(url, headers=headers, json=payload, timeout=20)
            r.raise_for_status()
            return report_id
        except Exception as e:
            # fallback to file
            pass
    # Fallback: store to file
    path = os.path.join(DATA_DIR, f"report-{report_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    return report_id
