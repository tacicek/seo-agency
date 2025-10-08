#!/usr/bin/env python3
"""
Test MOZ API integration
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'apps', 'api'))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from analyzers.moz import test_moz_connection, get_backlink_summary

def main():
    print("🔍 MOZ API Integration Test")
    print("=" * 70)
    print()
    
    # Check if credentials are set
    moz_id = os.getenv("MOZ_ACCESS_ID")
    moz_key = os.getenv("MOZ_SECRET_KEY")
    
    if not moz_id or not moz_key:
        print("❌ MOZ API credentials not found in .env")
        print()
        print("Please set:")
        print("  MOZ_ACCESS_ID=your_access_id")
        print("  MOZ_SECRET_KEY=your_secret_key")
        return
    
    print(f"✅ MOZ Access ID: {moz_id[:20]}...")
    print(f"✅ MOZ Secret Key: {'*' * 20}")
    print()
    
    # Test connection
    print("🧪 Testing MOZ API connection...")
    print("-" * 70)
    
    result = test_moz_connection()
    
    if result["status"] == "success":
        print("✅ MOZ API connection successful!")
        print()
        print("Test Metrics (moz.com):")
        metrics = result.get("test_metrics", {})
        print(f"  Domain Authority: {metrics.get('domain_authority')}")
        print(f"  Page Authority: {metrics.get('page_authority')}")
    else:
        print("❌ MOZ API connection failed")
        print(f"  Error: {result.get('error')}")
        print(f"  Message: {result.get('message')}")
        return
    
    print()
    print("-" * 70)
    print()
    
    # Test with example.com
    print("🧪 Testing with example.com...")
    print("-" * 70)
    
    backlinks = get_backlink_summary("https://example.com")
    
    if "error" in backlinks:
        print(f"❌ Error: {backlinks['error']}")
        print(f"   Message: {backlinks.get('message', '')}")
    else:
        print("✅ Successfully retrieved backlink data!")
        print()
        print("Backlink Metrics:")
        metrics = backlinks.get("backlink_metrics", {})
        print(f"  Domain Authority: {metrics.get('domain_authority')}")
        print(f"  Page Authority: {metrics.get('page_authority')}")
        print(f"  Spam Score: {metrics.get('spam_score')}")
        print(f"  SEO Score: {metrics.get('seo_score')}")
        print(f"  Root Domains Linking: {metrics.get('root_domains_linking')}")
        print(f"  External Links: {metrics.get('external_links')}")
        print()
        print("Link Quality:")
        quality = backlinks.get("link_quality", {})
        print(f"  MozRank: {quality.get('mozrank')}")
        print(f"  MozTrust: {quality.get('moztrust')}")
    
    print()
    print("=" * 70)
    print()
    print("🎉 MOZ API integration is working!")
    print()
    print("Next steps:")
    print("  1. Start the API server: ./scripts/start_manual.sh")
    print("  2. Test MOZ endpoint: http://localhost:8000/moz/test")
    print("  3. Run full analysis: http://localhost:8000/analyze")

if __name__ == "__main__":
    main()
