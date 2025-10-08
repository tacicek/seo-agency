import os
import time
import uuid
import json
import hashlib
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Rate limiting helpers
def sleep_with_jitter(base: float = 0.5, factor: float = 2.0, attempt: int = 0, max_sleep: float = 10.0):
    sleep = min(max_sleep, base * (factor ** attempt))
    time.sleep(sleep)


def hash_id(*parts: str) -> str:
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:16]


def build_gsc_service(gcp_credentials_json: str):
    # Service Account JSON is passed; never log it
    creds = service_account.Credentials.from_service_account_info(
        json.loads(gcp_credentials_json),
        scopes=["https://www.googleapis.com/auth/webmasters.readonly"],
    )
    return build("searchconsole", "v1", credentials=creds, cache_discovery=False)


def fetch_gsc_search_analytics(
    service,
    site_url: str,
    start_date: str,
    end_date: str,
    dimensions: List[str],
    search_type: str = "web",
    row_limit: int = 5000,
    qps: int = 3,
) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    start_row = 0
    attempt = 0
    while True:
        body = {
            "startDate": start_date,
            "endDate": end_date,
            "dimensions": dimensions,
            "rowLimit": row_limit,
            "startRow": start_row,
            "type": search_type,
        }
        try:
            resp = (
                service.searchanalytics()
                .query(siteUrl=site_url, body=body)
                .execute()
            )
            rows = resp.get("rows", [])
            if not rows:
                break
            for r in rows:
                rec = {"clicks": r.get("clicks"), "impressions": r.get("impressions"), "ctr": r.get("ctr"), "position": r.get("position")}
                keys = r.get("keys", [])
                for i, dim in enumerate(dimensions):
                    rec[dim] = keys[i] if i < len(keys) else None
                # If date is not in dimensions, add per-request date range marker (we will normalize later)
                if "date" not in rec:
                    rec["date"] = None
                results.append(rec)
            start_row += len(rows)
            attempt = 0
            time.sleep(max(0, 1.0 / max(1, qps)))
        except HttpError as e:
            status = getattr(e, "status_code", None) or getattr(e, "resp", {}).get("status")
            if status in [429, 500, 502, 503, 504] and attempt < 5:
                sleep_with_jitter(attempt=attempt)
                attempt += 1
                continue
            raise
    return results


def fetch_gsc_url_inspection(service, site_url: str, urls: List[str]) -> List[Dict[str, Any]]:
    # URL Inspection API is part of index.inspect method on searchconsole URL Testing Tools
    # Using "urlInspection" API (webmasters v1) via searchconsole python client is not always available; keep optional
    out: List[Dict[str, Any]] = []
    try:
        url_inspection = service.urlInspection()
    except Exception:
        return out
    for u in urls:
        try:
            body = {"inspectionUrl": u, "siteUrl": site_url}
            data = url_inspection.index().inspect(body=body).execute()
            result = data.get("inspectionResult", {})
            index_status_result = result.get("indexStatusResult", {})
            mobile_usability = result.get("mobileUsabilityResult", {})
            out.append({
                "url": u,
                "index_status": index_status_result.get("indexingState"),
                "last_crawl_time": index_status_result.get("lastCrawlTime"),
                "page_fetch_state": index_status_result.get("pageFetchState"),
                "robots_txt_state": index_status_result.get("robotsTxtState"),
                "canonical": {
                    "user_declared": index_status_result.get("userCanonical"),
                    "google_selected": index_status_result.get("googleCanonical"),
                },
                "mobile_usability": "PASS" if mobile_usability.get("verdict") == "PASS" else "FAIL" if mobile_usability.get("verdict") else None,
            })
            time.sleep(0.2)
        except HttpError as e:
            status = getattr(e, "status_code", None) or getattr(e, "resp", {}).get("status")
            if status in [429, 500, 502, 503, 504]:
                sleep_with_jitter()
                continue
        except Exception:
            continue
    return out


def fetch_psi(api_key: str, url: str, strategy: str = "mobile") -> Optional[Dict[str, Any]]:
    endpoint = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    params = {"url": url, "strategy": strategy, "key": api_key, "category": ["PERFORMANCE", "SEO"]}
    try:
        r = requests.get(endpoint, params=params, timeout=60)
        if r.status_code == 429 or r.status_code >= 500:
            return None
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def normalize_gsc_row(row: Dict[str, Any], dims: List[str], day: Optional[str]) -> Dict[str, Any]:
    date = row.get("date") or day
    page = row.get("page")
    query = row.get("query")
    country = row.get("country")
    device = row.get("device")
    return {
        "date": date,
        "page": page,
        "query": query,
        "country": country,
        "device": device,
        "clicks": float(row.get("clicks")) if row.get("clicks") is not None else None,
        "impressions": float(row.get("impressions")) if row.get("impressions") is not None else None,
        "ctr": float(row.get("ctr")) if row.get("ctr") is not None else None,
        "position": round(float(row.get("position")), 2) if row.get("position") is not None else None,
    }


def normalize_psi(doc: Dict[str, Any], url: str, strategy: str) -> Optional[Dict[str, Any]]:
    if not doc:
        return None
    lh = doc.get("lighthouseResult", {})
    categories = lh.get("categories", {})
    audits = lh.get("audits", {})
    perf = categories.get("performance", {}).get("score")
    seo = categories.get("seo", {}).get("score")
    def audit_num(audit_id: str) -> Optional[float]:
        a = audits.get(audit_id, {})
        v = a.get("numericValue")
        return float(v) if v is not None else None
    lcp_ms = audit_num("largest-contentful-paint")
    inp_ms = audit_num("interactive-next-paint") or audit_num("experimental-interaction-to-next-paint")
    cls = audit_num("cumulative-layout-shift")
    # Opportunities
    opps = []
    for k, v in audits.items():
        if v.get("details", {}).get("type") == "opportunity":
            est = v.get("details", {}).get("overallSavingsMs")
            if est is not None:
                opps.append({"id": k, "estimated_ms": float(est)})
    diagnostics = {
        "total_byte_weight_kb": (audit_num("total-byte-weight") or 0) / 1024.0 if audit_num("total-byte-weight") else None,
        "mainthread_work_ms": audit_num("mainthread-work-breakdown"),
        "network_requests": audits.get("network-requests", {}).get("details", {}).get("items")
    }
    if isinstance(diagnostics["network_requests"], list):
        diagnostics["network_requests"] = float(len(diagnostics["network_requests"]))
    else:
        diagnostics["network_requests"] = None
    return {
        "url": url,
        "strategy": strategy,
        "lighthouse": {"performance": float(perf) if perf is not None else None, "seo": float(seo) if seo is not None else None},
        "cwv": {"lcp_ms": lcp_ms, "inp_ms": inp_ms, "cls": cls},
        "opportunities": opps,
        "diagnostics": diagnostics,
    }


def compute_deltas(current: Dict[str, Any], prev: Dict[str, Any]) -> Dict[str, Any]:
    def pct(a: Optional[float], b: Optional[float]) -> Optional[float]:
        if a is None or b is None or b == 0:
            return None
        return round((a - b) / b, 4)
    return {
        "clicks_pct": pct(current.get("clicks_total"), prev.get("clicks_total")),
        "impressions_pct": pct(current.get("impr_total"), prev.get("impr_total")),
        "avg_position_diff": round((current.get("pos_avg") - prev.get("pos_avg")), 2) if current.get("pos_avg") is not None and prev.get("pos_avg") is not None else None,
        "lcp_ms_diff": (current.get("lcp_ms_avg") - prev.get("lcp_ms_avg")) if current.get("lcp_ms_avg") is not None and prev.get("lcp_ms_avg") is not None else None,
        "cls_diff": (current.get("cls_avg") - prev.get("cls_avg")) if current.get("cls_avg") is not None and prev.get("cls_avg") is not None else None,
    }


def aggregate_gsc(rows: List[Dict[str, Any]]) -> Dict[str, float]:
    clicks = [r.get("clicks") for r in rows if r.get("clicks") is not None]
    impr = [r.get("impressions") for r in rows if r.get("impressions") is not None]
    pos = [r.get("position") for r in rows if r.get("position") is not None]
    return {
        "clicks_total": sum(clicks) if clicks else None,
        "impr_total": sum(impr) if impr else None,
        "pos_avg": round(sum(pos) / len(pos), 2) if pos else None,
    }


def aggregate_psi(rows: List[Dict[str, Any]]) -> Dict[str, float]:
    lcp = [r.get("cwv", {}).get("lcp_ms") for r in rows if r.get("cwv", {}).get("lcp_ms") is not None]
    cls = [r.get("cwv", {}).get("cls") for r in rows if r.get("cwv", {}).get("cls") is not None]
    return {
        "lcp_ms_avg": sum(lcp) / len(lcp) if lcp else None,
        "cls_avg": sum(cls) / len(cls) if cls else None,
    }


def run_ingestion(payload: Dict[str, Any], storage_cb) -> Dict[str, Any]:
    try:
        project_id = payload.get("project_id")
        gcp_credentials = payload.get("gcp_credentials")
        gsc_cfg = payload.get("gsc", {})
        psi_cfg = payload.get("psi", {})
        rate_limits = payload.get("rate_limits", {"gsc_qps": 3, "psi_qps": 1})

        if not project_id:
            return {"error": {"message": "project_id required", "hint": "Provide project_id", "stage": "auth"}}
        if not gcp_credentials:
            return {"error": {"message": "gcp_credentials required", "hint": "Pass Service Account JSON", "stage": "auth"}}

        site_url = gsc_cfg.get("site_url")
        start_date = gsc_cfg.get("start_date")
        end_date = gsc_cfg.get("end_date")
        dimensions = gsc_cfg.get("dimensions", ["date", "query", "page", "country", "device"]) 
        search_type = gsc_cfg.get("search_type", "web")
        row_limit = int(gsc_cfg.get("row_limit", 5000))

        psi_strategy = psi_cfg.get("strategy", "mobile")
        psi_urls = psi_cfg.get("urls", [])
        psi_key = os.getenv("PSI_API_KEY")
        if psi_urls and not psi_key:
            return {"error": {"message": "PSI_API_KEY not configured", "hint": "Set PSI_API_KEY in environment", "stage": "auth"}}

        # Build services
        service = build_gsc_service(gcp_credentials)

        # Validate property by a small call (e.g., zero-row query)
        _ = fetch_gsc_search_analytics(service, site_url, start_date, end_date, dimensions[:1], search_type, 1, rate_limits.get("gsc_qps", 3))

        # Fetch GSC
        gsc_rows_raw = fetch_gsc_search_analytics(
            service, site_url, start_date, end_date, dimensions, search_type, row_limit, rate_limits.get("gsc_qps", 3)
        )

        # If date is not among dimensions, we'll expand dates by day for the range
        sa_norm: List[Dict[str, Any]] = []
        date_range_days: List[str] = []
        if "date" in dimensions:
            for r in gsc_rows_raw:
                sa_norm.append(normalize_gsc_row(r, dimensions, None))
        else:
            s = datetime.fromisoformat(start_date)
            e = datetime.fromisoformat(end_date)
            date_range_days = [(s + timedelta(days=i)).date().isoformat() for i in range((e - s).days + 1)]
            # We cannot distribute clicks by day without date dimension; we will set date to start_date for now
            for r in gsc_rows_raw:
                sa_norm.append(normalize_gsc_row(r, dimensions, start_date))

        # URL Inspection (optional)
        url_inspection = []
        if gsc_cfg.get("enable_url_inspection") and sa_norm:
            # pick top URLs by clicks
            top_pages = {}
            for r in sa_norm:
                p = r.get("page")
                c = r.get("clicks") or 0
                if not p:
                    continue
                top_pages[p] = top_pages.get(p, 0) + c
            top_urls = [u for u, _ in sorted(top_pages.items(), key=lambda x: x[1], reverse=True)[:50]]
            url_inspection = fetch_gsc_url_inspection(service, site_url, top_urls)

        # PSI fetch with QPS + basic backoff; cache same-day per URL+strategy
        psi_results: List[Dict[str, Any]] = []
        seen_cache: Dict[str, Dict[str, Any]] = {}
        qps_interval = max(1.0 / max(1, int(payload.get("rate_limits", {}).get("psi_qps", 1))), 0.0)
        for u in psi_urls:
            cache_key = f"{u}|{psi_strategy}|{datetime.utcnow().date().isoformat()}"
            if cache_key in seen_cache:
                psi_results.append(seen_cache[cache_key])
                continue
            doc = fetch_psi(psi_key, u, psi_strategy)
            if doc is None:
                # Retry once with backoff
                sleep_with_jitter()
                doc = fetch_psi(psi_key, u, psi_strategy)
            norm = normalize_psi(doc, u, psi_strategy) if doc else None
            if norm:
                seen_cache[cache_key] = norm
                psi_results.append(norm)
            time.sleep(qps_interval)

        # Aggregations & deltas
        agg_current = aggregate_gsc(sa_norm)
        agg_psi = aggregate_psi(psi_results)
        # previous period (same length before start_date)
        try:
            s = datetime.fromisoformat(start_date)
            e = datetime.fromisoformat(end_date)
            delta_days = (e - s).days + 1
            prev_end = s - timedelta(days=1)
            prev_start = prev_end - timedelta(days=delta_days - 1)
            prev_rows = fetch_gsc_search_analytics(service, site_url, prev_start.date().isoformat(), prev_end.date().isoformat(), dimensions, search_type, row_limit, rate_limits.get("gsc_qps", 3))
            prev_norm = [normalize_gsc_row(r, dimensions, prev_start.date().isoformat()) for r in prev_rows]
            agg_prev = aggregate_gsc(prev_norm)
            deltas = compute_deltas({**agg_current, **agg_psi}, {**agg_prev, **{}})
        except Exception:
            deltas = {"clicks_pct": None, "impressions_pct": None, "avg_position_diff": None, "lcp_ms_diff": None, "cls_diff": None}

        # Lightweight anomalies (example: CTR drop 7d)
        anomalies: List[Dict[str, Any]] = []
        # This is a simple placeholder based on CTR if present
        # You can extend with rolling averages and thresholds per page/query

        # Persist via callback (e.g., Supabase)
        run_id = str(uuid.uuid4())
        result_payload = {
            "project_id": project_id,
            "period": {"start": start_date, "end": end_date},
            "gsc": {"search_analytics": sa_norm, "url_inspection": url_inspection},
            "psi": {"results": psi_results},
            "deltas": deltas,
            "anomalies": anomalies,
            "meta": {
                "run_id": run_id,
                "generated_at": datetime.utcnow().isoformat() + "Z",
                "source": ["gsc_search_analytics"] + (["psi_v5"] if psi_results else []),
                "notes": "Ingestion run",
            },
        }

        # Idempotent keying (example key per row); real persistence should upsert using unique keys
        storage_cb(result_payload)
        return result_payload
    except HttpError as e:
        return {"error": {"message": str(e), "hint": "Check GSC permissions and site ownership", "stage": "fetch"}}
    except Exception as e:
        return {"error": {"message": str(e), "hint": "See server logs for details", "stage": "normalize"}}
