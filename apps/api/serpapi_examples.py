"""
SerpAPI Integration Examples

This script demonstrates how to use the SerpAPI integration
for keyword research, competitor analysis, and SERP feature detection.
"""

import os
import sys
from typing import List, Dict

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analyzers.serpapi import (
    analyze_serp_results,
    analyze_keyword_difficulty,
    batch_keyword_analysis
)


def example_1_keyword_difficulty():
    """Example 1: Check keyword difficulty for a single keyword"""
    print("=" * 60)
    print("Example 1: Keyword Difficulty Analysis")
    print("=" * 60)
    print()
    
    keyword = "python programming"
    print(f"Analyzing: {keyword}")
    print()
    
    result = analyze_keyword_difficulty(keyword)
    
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
        return
    
    print(f"Keyword: {result['keyword']}")
    print(f"Difficulty Score: {result['difficulty_score']}/100")
    print(f"Difficulty Level: {result['difficulty_level']} ({result['color']})")
    print()
    print("Factors:")
    print(f"  • Unique domains in top 10: {result['factors']['unique_domains_top_10']}")
    print(f"  • SERP features count: {result['factors']['serp_features_count']}")
    print(f"  • Domain diversity impact: {result['factors']['domain_diversity_impact']}")
    print(f"  • SERP features penalty: {result['factors']['serp_features_penalty']}")
    print()
    print("Recommendations:")
    for rec in result['recommendations']:
        print(f"  {rec}")
    print()


def example_2_batch_analysis():
    """Example 2: Analyze multiple keywords at once"""
    print("=" * 60)
    print("Example 2: Batch Keyword Analysis")
    print("=" * 60)
    print()
    
    keywords = [
        "seo tools",
        "keyword research",
        "backlink checker",
        "site audit",
        "rank tracker"
    ]
    
    print(f"Analyzing {len(keywords)} keywords:")
    for kw in keywords:
        print(f"  • {kw}")
    print()
    
    results = batch_keyword_analysis(keywords)
    
    if 'error' in results:
        print(f"❌ Error: {results['error']}")
        return
    
    print(f"Total Keywords Analyzed: {results['total_keywords']}")
    print(f"Average Difficulty: {results['average_difficulty']}/100")
    print()
    print("Distribution:")
    print(f"  • Easy (0-30): {results['distribution']['easy']}")
    print(f"  • Medium (30-50): {results['distribution']['medium']}")
    print(f"  • Hard (50-70): {results['distribution']['hard']}")
    print(f"  • Very Hard (70-100): {results['distribution']['very_hard']}")
    print()
    print(f"Recommendation: {results['recommendation']}")
    print()
    print("Individual Keywords:")
    for kw in results['keywords']:
        emoji = "🟢" if kw['difficulty_score'] < 30 else "🟡" if kw['difficulty_score'] < 50 else "🟠" if kw['difficulty_score'] < 70 else "🔴"
        print(f"  {emoji} {kw['keyword']}: {kw['difficulty_level']} ({kw['difficulty_score']})")
    print()


def example_3_find_easy_keywords():
    """Example 3: Find easy keywords from a list"""
    print("=" * 60)
    print("Example 3: Find Easy Keywords")
    print("=" * 60)
    print()
    
    keywords = [
        "on page seo",
        "technical seo",
        "local seo tips",
        "seo audit checklist",
        "free backlink checker",
        "keyword research tools",
        "seo reporting software",
        "website speed optimization"
    ]
    
    print(f"Searching {len(keywords)} keywords for easy targets...")
    print()
    
    results = batch_keyword_analysis(keywords)
    
    if 'error' in results:
        print(f"❌ Error: {results['error']}")
        return
    
    # Filter easy keywords (difficulty < 30)
    easy_keywords = [
        kw for kw in results['keywords']
        if kw['difficulty_score'] < 30
    ]
    
    print(f"🎯 Found {len(easy_keywords)} easy keywords:")
    print()
    for kw in easy_keywords:
        print(f"  ✅ {kw['keyword']}")
        print(f"     Difficulty: {kw['difficulty_score']}/100")
        print(f"     Unique domains: {kw['factors']['unique_domains_top_10']}")
        print()
    
    if not easy_keywords:
        print("No easy keywords found. Consider:")
        print("  • Targeting long-tail variations")
        print("  • Adding location modifiers")
        print("  • Using question keywords")
        print()


def example_4_serp_features():
    """Example 4: Analyze SERP features and opportunities"""
    print("=" * 60)
    print("Example 4: SERP Features & Opportunities")
    print("=" * 60)
    print()
    
    keyword = "best seo tools"
    print(f"Analyzing SERP for: {keyword}")
    print()
    
    serp = analyze_serp_results(keyword)
    
    if 'error' in serp:
        print(f"❌ Error: {serp['error']}")
        return
    
    # SERP Metrics
    metrics = serp.get('serp_metrics', {})
    print("SERP Metrics:")
    print(f"  • Total organic results: {metrics.get('total_organic_results', 0)}")
    print(f"  • Unique domains in top 10: {metrics.get('unique_domains_top_10', 0)}")
    print(f"  • SERP features count: {metrics.get('serp_features_count', 0)}")
    print(f"  • Competition level: {metrics.get('competition_level', 'Unknown')}")
    print()
    
    # SERP Features
    features = metrics.get('serp_features_present', [])
    print("SERP Features Present:")
    if features:
        for feature in features:
            print(f"  ✅ {feature.replace('_', ' ').title()}")
    else:
        print("  (None detected)")
    print()
    
    # Featured Snippet
    snippet = serp.get('featured_snippet')
    if snippet:
        print("Featured Snippet:")
        print(f"  • Type: {snippet.get('type', 'Unknown')}")
        print(f"  • Title: {snippet.get('title', 'N/A')}")
        print(f"  • Source: {snippet.get('link', 'N/A')}")
    else:
        print("Featured Snippet: None (Opportunity! 🎯)")
    print()
    
    # People Also Ask
    paa = serp.get('people_also_ask', [])
    if paa:
        print(f"People Also Ask ({len(paa)} questions):")
        for i, q in enumerate(paa[:5], 1):
            print(f"  {i}. {q.get('question', '')}")
    print()
    
    # Ranking Opportunities
    opportunities = serp.get('ranking_opportunities', {})
    print(f"Ranking Opportunities ({opportunities.get('total_opportunities', 0)}):")
    for opp in opportunities.get('opportunities', []):
        priority_emoji = "🔥" if opp['priority'] == 'high' else "📊"
        print(f"  {priority_emoji} {opp['type'].replace('_', ' ').title()}")
        print(f"     {opp['recommendation']}")
        print()


def example_5_competitor_analysis():
    """Example 5: Analyze top 10 competitors"""
    print("=" * 60)
    print("Example 5: Competitor Analysis")
    print("=" * 60)
    print()
    
    keyword = "seo tools"
    print(f"Finding competitors for: {keyword}")
    print()
    
    serp = analyze_serp_results(keyword)
    
    if 'error' in serp:
        print(f"❌ Error: {serp['error']}")
        return
    
    organic = serp.get('organic_results', [])[:10]
    
    print(f"Top 10 Competitors:\n")
    for result in organic:
        position = result.get('position', 0)
        title = result.get('title', 'N/A')
        link = result.get('displayed_link', 'N/A')
        has_sitelinks = len(result.get('sitelinks', [])) > 0
        has_rich = bool(result.get('rich_snippet'))
        
        print(f"#{position}: {link}")
        print(f"  Title: {title}")
        if has_sitelinks:
            print(f"  ✅ Sitelinks present ({len(result.get('sitelinks', []))} links)")
        if has_rich:
            print(f"  ✅ Rich snippet")
        print()


def example_6_content_gap_analysis():
    """Example 6: Find content gaps from People Also Ask"""
    print("=" * 60)
    print("Example 6: Content Gap Analysis")
    print("=" * 60)
    print()
    
    keyword = "python programming"
    print(f"Finding content gaps for: {keyword}")
    print()
    
    serp = analyze_serp_results(keyword)
    
    if 'error' in serp:
        print(f"❌ Error: {serp['error']}")
        return
    
    paa = serp.get('people_also_ask', [])
    
    if not paa:
        print("No People Also Ask questions found.")
        return
    
    print(f"📚 Content Ideas from People Also Ask ({len(paa)} questions):\n")
    
    for i, question_data in enumerate(paa, 1):
        question = question_data.get('question', '')
        print(f"{i}. {question}")
        print(f"   Content Type: Blog post or FAQ entry")
        print(f"   Target: Answer this question comprehensively")
        print()
    
    print("💡 Strategy:")
    print("  • Create a comprehensive FAQ page answering all questions")
    print("  • Structure content with proper H2/H3 headings for each question")
    print("  • Add schema markup (FAQPage) for better SERP appearance")
    print("  • Target featured snippet with concise, direct answers")
    print()


def example_7_location_comparison():
    """Example 7: Compare keyword difficulty across locations"""
    print("=" * 60)
    print("Example 7: Location-Based Difficulty Comparison")
    print("=" * 60)
    print()
    
    keyword = "seo services"
    locations = ["United States", "United Kingdom", "Germany"]
    
    print(f"Comparing keyword difficulty for: {keyword}")
    print(f"Across {len(locations)} locations\n")
    
    for location in locations:
        result = analyze_keyword_difficulty(keyword, location)
        
        if 'error' in result:
            print(f"❌ {location}: {result['error']}")
            continue
        
        print(f"📍 {location}:")
        print(f"   Difficulty: {result['difficulty_level']} ({result['difficulty_score']}/100)")
        print(f"   Unique domains: {result['factors']['unique_domains_top_10']}")
        print(f"   SERP features: {result['factors']['serp_features_count']}")
        print()
    
    print("💡 Strategy:")
    print("  • Target locations with lower difficulty first")
    print("  • Create location-specific content")
    print("  • Use local SEO tactics for geo-targeted keywords")
    print()


def main():
    """Run all examples"""
    # Check API key
    api_key = os.getenv('SERPAPI_API_KEY')
    if not api_key:
        print("❌ SERPAPI_API_KEY not set in environment")
        print()
        print("Please add to .env file:")
        print("SERPAPI_API_KEY=your_api_key_here")
        print()
        print("Get your API key from: https://serpapi.com/")
        return
    
    print()
    print("=" * 60)
    print("SerpAPI Integration Examples")
    print("=" * 60)
    print()
    print("API Key configured ✅")
    print()
    
    examples = [
        ("1", "Keyword Difficulty Analysis", example_1_keyword_difficulty),
        ("2", "Batch Keyword Analysis", example_2_batch_analysis),
        ("3", "Find Easy Keywords", example_3_find_easy_keywords),
        ("4", "SERP Features & Opportunities", example_4_serp_features),
        ("5", "Competitor Analysis", example_5_competitor_analysis),
        ("6", "Content Gap Analysis", example_6_content_gap_analysis),
        ("7", "Location Comparison", example_7_location_comparison),
    ]
    
    print("Available examples:")
    for num, name, _ in examples:
        print(f"  {num}. {name}")
    print()
    
    choice = input("Enter example number (1-7) or 'all' to run all: ").strip().lower()
    print()
    
    if choice == 'all':
        for _, _, func in examples:
            func()
            print()
    else:
        for num, _, func in examples:
            if choice == num:
                func()
                break
        else:
            print("Invalid choice. Please enter a number between 1-7 or 'all'.")


if __name__ == "__main__":
    main()
