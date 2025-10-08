import os, requests

def analyze_performance(url: str) -> dict:
    api_key = os.getenv("PAGESPEED_API_KEY", "")
    if not api_key:
        return {"note": "PAGESPEED_API_KEY not set; skipping", "score": None}
    endpoint = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={api_key}"
    try:
        data = requests.get(endpoint, timeout=60).json()
        lighthouse = data.get("lighthouseResult", {}).get("categories", {})
        perf = lighthouse.get("performance", {}).get("score", None)
        seo = lighthouse.get("seo", {}).get("score", None)
        return {"performance": perf, "seo": seo, "raw": data.get("loadingExperience", {})}
    except Exception as e:
        return {"error": str(e)}
