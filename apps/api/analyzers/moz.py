"""
MOZ API Analyzer
Provides backlink analysis, domain authority, and SEO metrics using MOZ API
"""
import os
import base64
import hmac
import hashlib
import time
import requests
from typing import Optional, Dict, Any

MOZ_ACCESS_ID = os.getenv("MOZ_ACCESS_ID", "")
MOZ_SECRET_KEY = os.getenv("MOZ_SECRET_KEY", "")
MOZ_API_ENDPOINT = "https://lsapi.seomoz.com/v2/url_metrics"
MOZ_LINKS_ENDPOINT = "https://lsapi.seomoz.com/v2/links"


def generate_moz_auth() -> Optional[Dict[str, str]]:
    """
    Generate MOZ API authentication headers
    Returns headers dict or None if credentials are missing
    """
    if not MOZ_ACCESS_ID or not MOZ_SECRET_KEY:
        return None
    
    # MOZ uses Basic Auth
    credentials = f"{MOZ_ACCESS_ID}:{MOZ_SECRET_KEY}"
    encoded = base64.b64encode(credentials.encode()).decode()
    
    return {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json"
    }


def analyze_moz_metrics(url: str) -> Dict[str, Any]:
    """
    Analyze URL using MOZ API
    
    Metrics provided:
    - Domain Authority (DA)
    - Page Authority (PA)
    - Spam Score
    - Root Domains Linking
    - External Links
    - MozRank
    - MozTrust
    
    Args:
        url: The URL to analyze
        
    Returns:
        Dict with MOZ metrics or error message
    """
    headers = generate_moz_auth()
    
    if not headers:
        return {
            "error": "MOZ_ACCESS_ID or MOZ_SECRET_KEY not configured",
            "note": "Set these in .env to enable MOZ metrics"
        }
    
    try:
        # Request payload for URL Metrics API v2
        payload = {
            "targets": [url]
        }
        
        response = requests.post(
            MOZ_API_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract results
            if "results" in data and len(data["results"]) > 0:
                result = data["results"][0]
                
                return {
                    "url": url,
                    "domain_authority": result.get("domain_authority"),
                    "page_authority": result.get("page_authority"),
                    "spam_score": result.get("spam_score"),
                    "root_domains_to_root_domain": result.get("root_domains_to_root_domain"),
                    "external_links_to_root_domain": result.get("external_links_to_root_domain"),
                    "external_links_to_page": result.get("external_links_to_page"),
                    "mozrank_url": result.get("url_mozrank"),
                    "moztrust_url": result.get("url_moztrust"),
                    "timestamp": int(time.time()),
                    "raw_data": result
                }
            else:
                return {
                    "error": "No results returned",
                    "response": data
                }
        
        elif response.status_code == 401:
            return {
                "error": "Authentication failed",
                "message": "Invalid MOZ API credentials",
                "status_code": 401
            }
        
        elif response.status_code == 429:
            return {
                "error": "Rate limit exceeded",
                "message": "MOZ API rate limit reached. Try again later.",
                "status_code": 429
            }
        
        else:
            return {
                "error": f"API request failed with status {response.status_code}",
                "message": response.text[:200],
                "status_code": response.status_code
            }

    except requests.exceptions.Timeout:
        return {
            "error": "Request timeout",
            "message": "MOZ API request timed out after 30 seconds"
        }

    except Exception as e:
        return {
            "error": "Unexpected error",
            "message": str(e)
        }


def fetch_backlinks(url: str, limit: int = 15) -> Dict[str, Any]:
    """Fetch top backlinks for a URL using MOZ Link Explorer API"""

    headers = generate_moz_auth()

    if not headers:
        return {
            "error": "MOZ_ACCESS_ID or MOZ_SECRET_KEY not configured",
            "note": "Set these in .env to enable MOZ backlink listings"
        }

    payload = {
        "target": url,
        "scope": "page_to_page",
        "filter": "external",
        "sort": "domain_authority",
        "limit": limit,
    }

    try:
        response = requests.post(
            MOZ_LINKS_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])

            backlinks = []
            for item in results:
                backlinks.append({
                    "source_url": item.get("source_url"),
                    "source_title": item.get("source_title"),
                    "target_url": item.get("target_url"),
                    "anchor_text": item.get("anchor_text"),
                    "domain_authority": item.get("domain_authority"),
                    "page_authority": item.get("page_authority"),
                    "spam_score": item.get("spam_score"),
                    "link_flags": item.get("link_flags"),
                    "first_seen": item.get("first_seen"),
                    "last_seen": item.get("last_seen"),
                })

            return {
                "backlinks": backlinks,
                "total_results": data.get("total_results"),
                "limit": payload["limit"],
            }

        elif response.status_code == 401:
            return {
                "error": "Authentication failed",
                "message": "Invalid MOZ API credentials",
                "status_code": 401
            }

        elif response.status_code == 429:
            return {
                "error": "Rate limit exceeded",
                "message": "MOZ API rate limit reached while fetching backlinks. Try again later.",
                "status_code": 429
            }

        return {
            "error": f"Backlink request failed with status {response.status_code}",
            "message": response.text[:200],
            "status_code": response.status_code
        }

    except requests.exceptions.Timeout:
        return {
            "error": "Request timeout",
            "message": "MOZ backlink request timed out after 30 seconds"
        }

    except Exception as exc:  # pragma: no cover - safeguard
        return {
            "error": "Unexpected error",
            "message": str(exc)
        }


def get_backlink_summary(url: str) -> Dict[str, Any]:
    """
    Get backlink summary for a URL
    
    Args:
        url: The URL to analyze
        
    Returns:
        Dict with backlink metrics
    """
    metrics = analyze_moz_metrics(url)
    
    if "error" in metrics:
        return metrics
    
    # Calculate a simple SEO score based on MOZ metrics
    da = metrics.get("domain_authority", 0) or 0
    pa = metrics.get("page_authority", 0) or 0
    spam = metrics.get("spam_score", 0) or 0
    
    # Simple scoring algorithm
    seo_score = ((da + pa) / 2) * (1 - (spam / 100))
    
    backlinks_data = fetch_backlinks(url)
    backlinks = backlinks_data.get("backlinks") if isinstance(backlinks_data, dict) else []
    backlink_error = backlinks_data if isinstance(backlinks_data, dict) and "error" in backlinks_data else None

    return {
        "backlink_metrics": {
            "domain_authority": da,
            "page_authority": pa,
            "spam_score": spam,
            "seo_score": round(seo_score, 2),
            "root_domains_linking": metrics.get("root_domains_to_root_domain", 0),
            "external_links": metrics.get("external_links_to_page", 0)
        },
        "link_quality": {
            "mozrank": metrics.get("mozrank_url", 0),
            "moztrust": metrics.get("moztrust_url", 0)
        },
        "backlinks": backlinks or [],
        "backlinks_overview": None if backlink_error else {
            "total_results": backlinks_data.get("total_results"),
            "limit": backlinks_data.get("limit")
        } if isinstance(backlinks_data, dict) else None,
        "backlinks_error": backlink_error,
        "full_metrics": metrics
    }


def test_moz_connection() -> Dict[str, Any]:
    """
    Test MOZ API connection with a simple request
    
    Returns:
        Dict with connection status
    """
    test_url = "https://moz.com"
    result = analyze_moz_metrics(test_url)
    
    if "error" in result:
        return {
            "status": "failed",
            "error": result.get("error"),
            "message": result.get("message", "")
        }
    
    return {
        "status": "success",
        "message": "MOZ API connection successful",
        "test_metrics": {
            "domain_authority": result.get("domain_authority"),
            "page_authority": result.get("page_authority")
        }
    }


if __name__ == "__main__":
    # Test the MOZ API integration
    print("🔍 Testing MOZ API Connection...")
    print("=" * 60)
    
    test_result = test_moz_connection()
    
    if test_result["status"] == "success":
        print("✅ MOZ API is working!")
        print(f"   Test metrics: {test_result['test_metrics']}")
    else:
        print("❌ MOZ API connection failed")
        print(f"   Error: {test_result.get('error')}")
        print(f"   Message: {test_result.get('message')}")
    
    print("\n" + "=" * 60)
    print("\n🧪 Testing with example.com...")
    
    result = get_backlink_summary("https://example.com")
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
    else:
        print("✅ Success!")
        print(f"   Domain Authority: {result['backlink_metrics']['domain_authority']}")
        print(f"   Page Authority: {result['backlink_metrics']['page_authority']}")
        print(f"   SEO Score: {result['backlink_metrics']['seo_score']}")
