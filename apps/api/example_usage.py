#!/usr/bin/env python3
"""
Quick Start Example for SEO Analyzer

This script demonstrates how to use the SEO Analyzer in the simplest way possible.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from seo_analyzer import SEOAnalyzer


def quick_analyze(url: str):
    """
    Quick analysis with default settings
    
    Args:
        url: Website URL to analyze
    """
    
    print("🚀 Starting Quick SEO Analysis...")
    print(f"📊 Target: {url}\n")
    
    # Initialize analyzer (reads from env variables)
    analyzer = SEOAnalyzer()
    
    # Crawl (20 pages max by default)
    print("🕷️  Step 1/4: Crawling website...")
    pages = analyzer.crawl_website(url, max_pages=20)
    
    if not pages:
        print("❌ No pages found. Exiting.")
        return
    
    print(f"✅ Found {len(pages)} pages\n")
    
    # Extract topics
    print("🧠 Step 2/4: Extracting topics...")
    topics = analyzer.extract_topics(pages, min_topic_size=2)
    print(f"✅ Identified {topics.get('total_topics', 0)} topics\n")
    
    # Analyze domain
    print("🔍 Step 3/4: Analyzing domain...")
    from urllib.parse import urlparse
    domain = urlparse(url).netloc
    metrics = analyzer.analyze_domain(domain)
    
    moz = metrics.get('moz', {})
    if moz.get('status') == 'success':
        print(f"✅ DA: {moz.get('domain_authority', 'N/A')} | PA: {moz.get('page_authority', 'N/A')}\n")
    else:
        print("⚠️  Moz data unavailable\n")
    
    # Calculate score
    print("🎯 Step 4/4: Calculating Topical Authority Score...")
    score = analyzer.calculate_topical_authority_score(topics, metrics)
    
    # Display results
    print("\n" + "="*70)
    print("   ANALYSIS RESULTS")
    print("="*70)
    print(f"\n🏆 TOPICAL AUTHORITY SCORE: {score['topical_authority_score']} ({score['grade']})")
    print(f"\n💡 {score['interpretation']}")
    
    print("\n📊 Score Breakdown:")
    for component, value in score['components'].items():
        bar = '█' * int(value / 5)
        print(f"   {component:.<30} {value:>5.1f} {bar}")
    
    print("\n🧠 Topic Summary:")
    for topic in topics.get('topics', [])[:3]:
        keywords = [kw['keyword'] for kw in topic['keybert_keywords'][:5]]
        print(f"   Topic {topic['topic_id']}: {', '.join(keywords)}")
    
    # Generate reports
    print("\n📝 Generating reports...")
    analyzer.generate_report(url, pages, topics, metrics, score)
    
    print("\n✅ COMPLETE! Check these files:")
    print("   - report.html")
    print("   - topics.json")
    print("   - domain_metrics.json")
    print("   - topic_distribution.png")
    print("   - authority_breakdown.png")
    print("\n" + "="*70)


def batch_analyze(urls: list):
    """
    Analyze multiple URLs and compare results
    
    Args:
        urls: List of URLs to analyze
    """
    print(f"🚀 Batch Analysis: {len(urls)} URLs\n")
    
    analyzer = SEOAnalyzer()
    results = []
    
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] Analyzing: {url}")
        print("-" * 60)
        
        try:
            # Crawl
            pages = analyzer.crawl_website(url, max_pages=15)
            if not pages:
                print("❌ No pages found, skipping...\n")
                continue
            
            # Topics
            topics = analyzer.extract_topics(pages, min_topic_size=2)
            
            # Domain
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
            metrics = analyzer.analyze_domain(domain)
            
            # Score
            score = analyzer.calculate_topical_authority_score(topics, metrics)
            
            results.append({
                'url': url,
                'score': score['topical_authority_score'],
                'grade': score['grade'],
                'topics': topics.get('total_topics', 0),
                'da': metrics.get('moz', {}).get('domain_authority', 0)
            })
            
            print(f"✅ Score: {score['topical_authority_score']} ({score['grade']})")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            continue
    
    # Display comparison
    print("\n" + "="*70)
    print("   BATCH RESULTS COMPARISON")
    print("="*70)
    print(f"\n{'URL':<40} {'Score':<10} {'Grade':<8} {'Topics':<8} {'DA':<5}")
    print("-" * 70)
    
    # Sort by score
    results.sort(key=lambda x: x['score'], reverse=True)
    
    for r in results:
        url_short = r['url'][:37] + '...' if len(r['url']) > 40 else r['url']
        print(f"{url_short:<40} {r['score']:<10.1f} {r['grade']:<8} {r['topics']:<8} {r['da']:<5}")
    
    print("\n" + "="*70)


def compare_competitors(your_url: str, competitor_urls: list):
    """
    Compare your site with competitors
    
    Args:
        your_url: Your website URL
        competitor_urls: List of competitor URLs
    """
    print("⚔️  COMPETITIVE ANALYSIS")
    print("="*70)
    print(f"Your Site: {your_url}")
    print(f"Competitors: {len(competitor_urls)}\n")
    
    all_urls = [your_url] + competitor_urls
    batch_analyze(all_urls)


if __name__ == "__main__":
    # Example usage based on command line args
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Single analysis:    python example_usage.py <url>")
        print("  Batch analysis:     python example_usage.py <url1> <url2> <url3>...")
        print("  Competitive:        python example_usage.py --compare <your-url> <comp1> <comp2>...")
        print("\nExample:")
        print("  python example_usage.py https://example.com")
        sys.exit(1)
    
    if sys.argv[1] == "--compare":
        if len(sys.argv) < 4:
            print("❌ Need at least 2 URLs for comparison")
            sys.exit(1)
        your_site = sys.argv[2]
        competitors = sys.argv[3:]
        compare_competitors(your_site, competitors)
    
    elif len(sys.argv) == 2:
        # Single URL
        quick_analyze(sys.argv[1])
    
    else:
        # Multiple URLs
        batch_analyze(sys.argv[1:])
