"""
DataForSEO API Analyzer
=======================

Lightweight integration for DataForSEO v3 endpoints used in our SEO Analyzer:
- Keyword Difficulty (Google Ads): /v3/keywords_data/google_ads/keyword_difficulty/live
- SERP Organic (Advanced): /v3/serp/google/organic/live/advanced

Authentication: Basic Auth using DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD

Environment Variables:
  DATAFORSEO_LOGIN
  DATAFORSEO_PASSWORD
  DATAFORSEO_BASE_URL (optional; default: https://api.dataforseo.com)

Notes:
- Uses "live" endpoints to avoid task polling.
- Accepts location_name and language_name directly for convenience.
"""

from __future__ import annotations

import os
import base64
import time
from typing import Any, Dict, List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


BASE_URL = os.getenv("DATAFORSEO_BASE_URL", "https://api.dataforseo.com")


def _get_auth() -> tuple[str, str]:
    login = os.getenv("DATAFORSEO_LOGIN")
    password = os.getenv("DATAFORSEO_PASSWORD")
    if not login or not password:
        raise RuntimeError("DATAFORSEO_LOGIN or DATAFORSEO_PASSWORD not configured")
    return login, password


def _session() -> requests.Session:
    s = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    return s


def _post(endpoint: str, payload: Dict[str, Any], timeout: int = 30) -> Dict[str, Any]:
    url = f"{BASE_URL}{endpoint}"
    login, password = _get_auth()
    sess = _session()
    resp = sess.post(url, json=[payload], auth=(login, password), timeout=timeout)
    if resp.status_code >= 400:
        raise RuntimeError(f"DataForSEO API error: {resp.status_code} {resp.text}")
    data = resp.json()
    if not isinstance(data, dict):
        raise RuntimeError("Unexpected DataForSEO response format")
    return data


def test_dataforseo_connection() -> Dict[str, Any]:
    """Simple connectivity test using a lightweight keyword difficulty call."""
    try:
        # If creds missing, _get_auth() will raise
        _get_auth()
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "instructions": "Set DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD"
        }

    try:
        # Use a harmless test keyword
        result = analyze_keyword_difficulty_dfs("test", location_name="United States", language_name="English")
        return {"status": "success", "message": "DataForSEO connection successful", "test_result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def analyze_keyword_difficulty_dfs(
    keyword: str,
    location_name: str = "United States",
    language_name: str = "English"
) -> Dict[str, Any]:
    """
    Keyword Difficulty (live)
    Endpoint: /v3/keywords_data/google_ads/keyword_difficulty/live
    """
    payload = {
        "keywords": [keyword],
        "location_name": location_name,
        "language_name": language_name,
    }
    raw = _post("/v3/keywords_data/google_ads/keyword_difficulty/live", payload)
    # Normalize
    tasks = raw.get("tasks") or []
    if not tasks:
        return {"keyword": keyword, "error": "No tasks returned", "raw": raw}
    result_items = tasks[0].get("result") or []
    if not result_items:
        return {"keyword": keyword, "error": "No result items", "raw": raw}
    item = result_items[0]
    difficulty = item.get("keyword_difficulty")
    competition = item.get("competition")
    cpc = item.get("cpc")
    vol = item.get("search_volume")
    return {
        "keyword": keyword,
        "difficulty": difficulty,
        "competition": competition,
        "cpc": cpc,
        "search_volume": vol,
        "location_name": location_name,
        "language_name": language_name,
        "timestamp": time.time(),
    }


def analyze_serp_results_dfs(
    keyword: str,
    location_name: str = "United States",
    language_name: str = "English",
    device: str = "desktop"
) -> Dict[str, Any]:
    """
    SERP Organic (advanced, live)
    Endpoint: /v3/serp/google/organic/live/advanced
    """
    payload = {
        "keyword": keyword,
        "location_name": location_name,
        "language_name": language_name,
        "device": device,
    }
    raw = _post("/v3/serp/google/organic/live/advanced", payload)
    tasks = raw.get("tasks") or []
    if not tasks:
        return {"keyword": keyword, "results": [], "error": "No tasks returned", "raw": raw}
    result_items = tasks[0].get("result") or []
    if not result_items:
        return {"keyword": keyword, "results": [], "error": "No result items", "raw": raw}
    # Extract organic results
    items = result_items[0].get("items") or []
    organic = []
    for it in items:
        if it.get("type") != "organic":
            continue
        organic.append({
            "position": it.get("rank_group"),
            "title": it.get("title"),
            "url": it.get("url"),
            "domain": it.get("domain"),
            "snippet": it.get("snippet") or it.get("description"),
            "sitelinks": it.get("sitelinks") or [],
        })

    return {
        "keyword": keyword,
        "location_name": location_name,
        "language_name": language_name,
        "device": device,
        "results": organic,
        "total_results": len(organic),
        "timestamp": time.time(),
    }
