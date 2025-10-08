"""
SerpAPI Integration Module

Provides Google Search Results Analysis including:
- Organic search results
- Featured snippets
- People Also Ask
- Related searches
- Knowledge graph
- Local pack results
- Shopping results
- News results

Requires: SERPAPI_API_KEY environment variable
Get your API key from: https://serpapi.com/
"""

import os
from typing import Dict, Any, List, Optional
from serpapi import GoogleSearch


def analyze_serp_results(query: str, location: str = "United States", 
                        language: str = "en") -> Dict[str, Any]:
    """
    Analyze Google Search results for a given query
    
    Args:
        query: Search query/keyword
        location: Geographic location for search
        language: Language code (en, de, tr, etc.)
        
    Returns:
        Dictionary with comprehensive SERP data
    """
    api_key = os.getenv('SERPAPI_API_KEY')
    
    if not api_key:
        return {
            'error': 'SERPAPI_API_KEY not set',
            'message': 'Please set SERPAPI_API_KEY environment variable'
        }
    
    try:
        # Configure search parameters
        params = {
            "q": query,
            "location": location,
            "hl": language,
            "gl": language[:2] if len(language) > 2 else language,
            "api_key": api_key,
            "num": 100  # Get top 100 results
        }
        
        # Perform search
        search = GoogleSearch(params)
        results = search.get_dict()
        
        # Extract and structure data
        analysis = {
            'query': query,
            'location': location,
            'language': language,
            'organic_results': extract_organic_results(results),
            'featured_snippet': extract_featured_snippet(results),
            'knowledge_graph': extract_knowledge_graph(results),
            'people_also_ask': extract_people_also_ask(results),
            'related_searches': extract_related_searches(results),
            'local_pack': extract_local_pack(results),
            'serp_metrics': calculate_serp_metrics(results),
            'ranking_opportunities': analyze_ranking_opportunities(results)
        }
        
        return analysis
        
    except Exception as e:
        return {
            'error': str(e),
            'message': 'Failed to fetch SERP data'
        }


def extract_organic_results(results: Dict) -> List[Dict[str, Any]]:
    """Extract organic search results"""
    organic = results.get('organic_results', [])
    
    extracted = []
    for idx, result in enumerate(organic, 1):
        extracted.append({
            'position': idx,
            'title': result.get('title', ''),
            'link': result.get('link', ''),
            'displayed_link': result.get('displayed_link', ''),
            'snippet': result.get('snippet', ''),
            'rich_snippet': result.get('rich_snippet', {}),
            'sitelinks': result.get('sitelinks', []),
            'cached_page_link': result.get('cached_page_link', ''),
            'favicon': result.get('favicon', '')
        })
    
    return extracted


def extract_featured_snippet(results: Dict) -> Optional[Dict[str, Any]]:
    """Extract featured snippet (position 0)"""
    snippet = results.get('featured_snippet')
    
    if snippet:
        return {
            'type': snippet.get('type', 'unknown'),
            'title': snippet.get('title', ''),
            'link': snippet.get('link', ''),
            'snippet': snippet.get('snippet', ''),
            'thumbnail': snippet.get('thumbnail', ''),
            'extensions': snippet.get('extensions', [])
        }
    
    return None


def extract_knowledge_graph(results: Dict) -> Optional[Dict[str, Any]]:
    """Extract knowledge graph data"""
    kg = results.get('knowledge_graph')
    
    if kg:
        return {
            'title': kg.get('title', ''),
            'type': kg.get('type', ''),
            'description': kg.get('description', ''),
            'source': kg.get('source', {}),
            'image': kg.get('image', ''),
            'website': kg.get('website', ''),
            'profiles': kg.get('profiles', []),
            'attributes': kg.get('attributes', {}),
            'people_also_search_for': kg.get('people_also_search_for', [])
        }
    
    return None


def extract_people_also_ask(results: Dict) -> List[Dict[str, Any]]:
    """Extract People Also Ask questions"""
    paa = results.get('related_questions', [])
    
    extracted = []
    for question in paa:
        extracted.append({
            'question': question.get('question', ''),
            'snippet': question.get('snippet', ''),
            'title': question.get('title', ''),
            'link': question.get('link', ''),
            'displayed_link': question.get('displayed_link', '')
        })
    
    return extracted


def extract_related_searches(results: Dict) -> List[str]:
    """Extract related search queries"""
    related = results.get('related_searches', [])
    return [r.get('query', '') for r in related]


def extract_local_pack(results: Dict) -> Optional[Dict[str, Any]]:
    """Extract local pack results"""
    local = results.get('local_results')
    
    if local:
        places = local.get('places', [])
        return {
            'total_results': len(places),
            'places': [
                {
                    'position': idx + 1,
                    'title': place.get('title', ''),
                    'rating': place.get('rating', 0),
                    'reviews': place.get('reviews', 0),
                    'address': place.get('address', ''),
                    'hours': place.get('hours', ''),
                    'type': place.get('type', ''),
                    'phone': place.get('phone', ''),
                    'website': place.get('website', '')
                }
                for idx, place in enumerate(places)
            ]
        }
    
    return None


def calculate_serp_metrics(results: Dict) -> Dict[str, Any]:
    """Calculate key SERP metrics"""
    organic = results.get('organic_results', [])
    
    # Count domains in top 10
    top_10_domains = set()
    for result in organic[:10]:
        link = result.get('link', '')
        if link:
            from urllib.parse import urlparse
            domain = urlparse(link).netloc
            top_10_domains.add(domain)
    
    # Detect SERP features
    features = []
    if results.get('featured_snippet'):
        features.append('featured_snippet')
    if results.get('knowledge_graph'):
        features.append('knowledge_graph')
    if results.get('related_questions'):
        features.append('people_also_ask')
    if results.get('local_results'):
        features.append('local_pack')
    if results.get('top_stories'):
        features.append('news_results')
    if results.get('shopping_results'):
        features.append('shopping_results')
    if results.get('inline_images'):
        features.append('image_pack')
    
    return {
        'total_organic_results': len(organic),
        'unique_domains_top_10': len(top_10_domains),
        'serp_features_present': features,
        'serp_features_count': len(features),
        'has_featured_snippet': 'featured_snippet' in features,
        'has_knowledge_graph': 'knowledge_graph' in features,
        'has_local_pack': 'local_pack' in features,
        'competition_level': classify_competition_level(len(top_10_domains), len(features))
    }


def classify_competition_level(unique_domains: int, features_count: int) -> str:
    """Classify keyword competition level"""
    if unique_domains >= 9 and features_count <= 2:
        return 'Low - Good opportunity'
    elif unique_domains >= 7 and features_count <= 4:
        return 'Medium - Competitive'
    else:
        return 'High - Very competitive'


def analyze_ranking_opportunities(results: Dict) -> Dict[str, Any]:
    """Analyze ranking opportunities and recommendations"""
    organic = results.get('organic_results', [])
    featured = results.get('featured_snippet')
    paa = results.get('related_questions', [])
    
    opportunities = []
    
    # Featured snippet opportunity
    if not featured:
        opportunities.append({
            'type': 'featured_snippet',
            'priority': 'high',
            'recommendation': 'No featured snippet present - opportunity to capture position 0 with well-structured content'
        })
    else:
        opportunities.append({
            'type': 'featured_snippet',
            'priority': 'medium',
            'recommendation': f"Featured snippet occupied by {featured.get('link', 'unknown')} - analyze their content format",
            'current_holder': featured.get('link', '')
        })
    
    # People Also Ask opportunity
    if paa:
        opportunities.append({
            'type': 'content_expansion',
            'priority': 'high',
            'recommendation': f'Create content answering {len(paa)} related questions to increase topical authority',
            'questions': [q.get('question', '') for q in paa[:5]]
        })
    
    # Domain diversity
    top_10_links = [r.get('link', '') for r in organic[:10]]
    domains = set()
    for link in top_10_links:
        from urllib.parse import urlparse
        domains.add(urlparse(link).netloc)
    
    if len(domains) >= 8:
        opportunities.append({
            'type': 'low_competition',
            'priority': 'high',
            'recommendation': 'High domain diversity in top 10 indicates lower competition - good ranking opportunity'
        })
    
    # Rich snippets
    rich_snippet_count = sum(1 for r in organic[:10] if r.get('rich_snippet'))
    if rich_snippet_count < 5:
        opportunities.append({
            'type': 'rich_snippets',
            'priority': 'medium',
            'recommendation': 'Few rich snippets in top 10 - implement schema markup to stand out'
        })
    
    return {
        'total_opportunities': len(opportunities),
        'opportunities': opportunities
    }


def analyze_keyword_difficulty(query: str, location: str = "United States") -> Dict[str, Any]:
    """
    Comprehensive keyword difficulty analysis
    
    Args:
        query: Keyword to analyze
        location: Geographic location
        
    Returns:
        Keyword difficulty score and analysis
    """
    api_key = os.getenv('SERPAPI_API_KEY')
    
    if not api_key:
        return {'error': 'SERPAPI_API_KEY not set'}
    
    try:
        params = {
            "q": query,
            "location": location,
            "api_key": api_key,
            "num": 100
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        
        organic = results.get('organic_results', [])
        
        # Calculate difficulty factors
        top_domains = []
        for result in organic[:10]:
            link = result.get('link', '')
            if link:
                from urllib.parse import urlparse
                domain = urlparse(link).netloc
                top_domains.append(domain)
        
        unique_domains = len(set(top_domains))
        
        # Count SERP features
        features_count = 0
        if results.get('featured_snippet'):
            features_count += 1
        if results.get('knowledge_graph'):
            features_count += 1
        if results.get('local_results'):
            features_count += 1
        if results.get('shopping_results'):
            features_count += 1
        
        # Calculate difficulty score (0-100)
        domain_diversity_score = (unique_domains / 10) * 30  # Max 30 points
        feature_penalty = features_count * 10  # -10 per feature
        
        difficulty_score = max(0, min(100, 70 - domain_diversity_score + feature_penalty))
        
        # Classify difficulty
        if difficulty_score < 30:
            difficulty = 'Easy'
            color = 'green'
        elif difficulty_score < 50:
            difficulty = 'Medium'
            color = 'yellow'
        elif difficulty_score < 70:
            difficulty = 'Hard'
            color = 'orange'
        else:
            difficulty = 'Very Hard'
            color = 'red'
        
        return {
            'keyword': query,
            'difficulty_score': round(difficulty_score, 1),
            'difficulty_level': difficulty,
            'color': color,
            'factors': {
                'unique_domains_top_10': unique_domains,
                'serp_features_count': features_count,
                'domain_diversity_impact': round(domain_diversity_score, 1),
                'serp_features_penalty': feature_penalty
            },
            'recommendations': generate_difficulty_recommendations(difficulty_score, unique_domains, features_count)
        }
        
    except Exception as e:
        return {'error': str(e)}


def generate_difficulty_recommendations(score: float, domains: int, features: int) -> List[str]:
    """Generate recommendations based on difficulty"""
    recommendations = []
    
    if score < 30:
        recommendations.append("✅ Low competition - Great opportunity for quick rankings")
        recommendations.append("Focus on quality content and basic on-page SEO")
    elif score < 50:
        recommendations.append("📊 Medium competition - Achievable with consistent effort")
        recommendations.append("Build quality backlinks and create comprehensive content")
    elif score < 70:
        recommendations.append("⚠️ High competition - Requires strong SEO strategy")
        recommendations.append("Focus on topical authority and high-quality backlinks")
    else:
        recommendations.append("🔴 Very high competition - Long-term strategy needed")
        recommendations.append("Target long-tail variations and build domain authority first")
    
    if domains < 7:
        recommendations.append(f"⚡ Only {domains} unique domains in top 10 - some sites have multiple positions")
    
    if features > 3:
        recommendations.append(f"⚠️ {features} SERP features present - organic CTR may be lower")
    
    return recommendations


def batch_keyword_analysis(keywords: List[str], location: str = "United States") -> Dict[str, Any]:
    """
    Analyze multiple keywords in batch
    
    Args:
        keywords: List of keywords to analyze
        location: Geographic location
        
    Returns:
        Batch analysis results
    """
    results = []
    
    for keyword in keywords:
        analysis = analyze_keyword_difficulty(keyword, location)
        if 'error' not in analysis:
            results.append(analysis)
    
    # Calculate summary statistics
    if results:
        scores = [r['difficulty_score'] for r in results]
        avg_difficulty = sum(scores) / len(scores)
        
        easy = sum(1 for r in results if r['difficulty_score'] < 30)
        medium = sum(1 for r in results if 30 <= r['difficulty_score'] < 50)
        hard = sum(1 for r in results if 50 <= r['difficulty_score'] < 70)
        very_hard = sum(1 for r in results if r['difficulty_score'] >= 70)
        
        return {
            'total_keywords': len(results),
            'average_difficulty': round(avg_difficulty, 1),
            'distribution': {
                'easy': easy,
                'medium': medium,
                'hard': hard,
                'very_hard': very_hard
            },
            'keywords': results,
            'recommendation': generate_batch_recommendation(easy, medium, hard, very_hard)
        }
    
    return {'error': 'No keywords analyzed successfully'}


def generate_batch_recommendation(easy: int, medium: int, hard: int, very_hard: int) -> str:
    """Generate overall recommendation for keyword batch"""
    total = easy + medium + hard + very_hard
    
    if easy / total > 0.5:
        return "🎯 Great keyword set! Majority are easy targets - focus on these for quick wins"
    elif (easy + medium) / total > 0.6:
        return "📊 Balanced keyword set - mix of quick wins and medium-term targets"
    elif hard / total > 0.4:
        return "⚠️ Challenging keyword set - requires strong SEO foundation"
    else:
        return "🔴 Very competitive keywords - consider targeting long-tail variations first"


def track_keyword_ranking(domain: str, keywords: List[str], 
                         location: str = "United States",
                         language: str = "en") -> Dict[str, Any]:
    """
    Track domain's ranking positions for multiple keywords
    
    Args:
        domain: Your domain to track (e.g., "bs-company.ch")
        keywords: List of keywords to check rankings for
        location: Geographic location
        language: Language code
        
    Returns:
        Dictionary with ranking data for each keyword
    """
    api_key = os.getenv('SERPAPI_API_KEY')
    
    if not api_key:
        return {
            'error': 'SERPAPI_API_KEY not set',
            'message': 'Please set SERPAPI_API_KEY environment variable'
        }
    
    # Clean domain (remove protocol and trailing slash)
    from urllib.parse import urlparse
    clean_domain = urlparse(domain if '://' in domain else f'https://{domain}').netloc
    
    rankings = []
    
    for keyword in keywords:
        try:
            params = {
                "q": keyword,
                "location": location,
                "hl": language,
                "gl": language[:2] if len(language) > 2 else language,
                "api_key": api_key,
                "num": 100
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            organic = results.get('organic_results', [])
            
            # Find domain position
            position = None
            url = None
            title = None
            snippet = None
            
            for idx, result in enumerate(organic, 1):
                result_url = result.get('link', '')
                if clean_domain in result_url:
                    position = idx
                    url = result_url
                    title = result.get('title', '')
                    snippet = result.get('snippet', '')
                    break
            
            # Get top 3 competitors
            competitors = []
            for idx, result in enumerate(organic[:3], 1):
                result_domain = urlparse(result.get('link', '')).netloc
                if result_domain != clean_domain:
                    competitors.append({
                        'position': idx,
                        'domain': result_domain,
                        'title': result.get('title', ''),
                        'url': result.get('link', '')
                    })
            
            ranking_data = {
                'keyword': keyword,
                'position': position,
                'url': url,
                'title': title,
                'snippet': snippet,
                'status': 'ranking' if position else 'not_found',
                'page': (position - 1) // 10 + 1 if position else None,
                'top_competitors': competitors[:3],
                'total_results': len(organic),
                'serp_features': calculate_serp_metrics(results).get('serp_features_count', 0)
            }
            
            rankings.append(ranking_data)
            
        except Exception as e:
            rankings.append({
                'keyword': keyword,
                'error': str(e),
                'status': 'error'
            })
    
    # Calculate summary stats
    ranked_keywords = [r for r in rankings if r.get('position')]
    total_keywords = len(keywords)
    visibility_score = 0
    
    for r in ranked_keywords:
        pos = r['position']
        if pos == 1:
            visibility_score += 100
        elif pos <= 3:
            visibility_score += 80
        elif pos <= 10:
            visibility_score += 50
        elif pos <= 20:
            visibility_score += 25
        else:
            visibility_score += 10
    
    avg_position = sum(r['position'] for r in ranked_keywords) / len(ranked_keywords) if ranked_keywords else None
    
    summary = {
        'domain': clean_domain,
        'total_keywords_tracked': total_keywords,
        'keywords_ranking': len(ranked_keywords),
        'keywords_not_ranking': total_keywords - len(ranked_keywords),
        'average_position': round(avg_position, 1) if avg_position else None,
        'visibility_score': round(visibility_score / total_keywords, 1) if total_keywords > 0 else 0,
        'rankings_by_position': {
            'top_3': sum(1 for r in ranked_keywords if r['position'] <= 3),
            'top_10': sum(1 for r in ranked_keywords if r['position'] <= 10),
            'top_20': sum(1 for r in ranked_keywords if r['position'] <= 20),
            'top_50': sum(1 for r in ranked_keywords if r['position'] <= 50),
            'top_100': sum(1 for r in ranked_keywords if r['position'] <= 100)
        }
    }
    
    return {
        'summary': summary,
        'rankings': rankings,
        'recommendations': generate_ranking_recommendations(summary, rankings)
    }


def analyze_competitors(domain: str, keywords: List[str], 
                       location: str = "United States",
                       language: str = "en") -> Dict[str, Any]:
    """
    Analyze top competitors for given keywords
    
    Args:
        domain: Your domain
        keywords: Keywords to analyze competition for
        location: Geographic location
        language: Language code
        
    Returns:
        Comprehensive competitor analysis
    """
    api_key = os.getenv('SERPAPI_API_KEY')
    
    if not api_key:
        return {
            'error': 'SERPAPI_API_KEY not set',
            'message': 'Please set SERPAPI_API_KEY environment variable'
        }
    
    from urllib.parse import urlparse
    clean_domain = urlparse(domain if '://' in domain else f'https://{domain}').netloc
    
    # Track competitor appearances
    competitor_data = {}
    
    for keyword in keywords:
        try:
            params = {
                "q": keyword,
                "location": location,
                "hl": language,
                "gl": language[:2] if len(language) > 2 else language,
                "api_key": api_key,
                "num": 20  # Top 20 results
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            organic = results.get('organic_results', [])
            
            for idx, result in enumerate(organic[:10], 1):
                result_domain = urlparse(result.get('link', '')).netloc
                
                if result_domain != clean_domain:
                    if result_domain not in competitor_data:
                        competitor_data[result_domain] = {
                            'domain': result_domain,
                            'appearances': 0,
                            'avg_position': 0,
                            'positions': [],
                            'keywords': [],
                            'urls': set(),
                            'titles': []
                        }
                    
                    competitor_data[result_domain]['appearances'] += 1
                    competitor_data[result_domain]['positions'].append(idx)
                    competitor_data[result_domain]['keywords'].append(keyword)
                    competitor_data[result_domain]['urls'].add(result.get('link', ''))
                    competitor_data[result_domain]['titles'].append(result.get('title', ''))
        
        except Exception as e:
            continue
    
    # Calculate averages and rank competitors
    competitors = []
    for domain_name, data in competitor_data.items():
        data['avg_position'] = round(sum(data['positions']) / len(data['positions']), 1)
        data['visibility_score'] = round((data['appearances'] / len(keywords)) * 100, 1)
        data['urls'] = list(data['urls'])
        
        competitors.append({
            'domain': domain_name,
            'appearances': data['appearances'],
            'visibility': data['visibility_score'],
            'avg_position': data['avg_position'],
            'keywords_ranking': data['keywords'],
            'best_position': min(data['positions']),
            'sample_urls': data['urls'][:3],
            'sample_titles': data['titles'][:3]
        })
    
    # Sort by visibility score
    competitors.sort(key=lambda x: (-x['visibility'], x['avg_position']))
    
    # Get top 10 competitors
    top_competitors = competitors[:10]
    
    return {
        'your_domain': clean_domain,
        'keywords_analyzed': len(keywords),
        'total_competitors_found': len(competitors),
        'top_competitors': top_competitors,
        'competitive_landscape': analyze_competitive_landscape(top_competitors),
        'recommendations': generate_competitor_recommendations(clean_domain, top_competitors, keywords)
    }


def analyze_competitive_landscape(competitors: List[Dict]) -> Dict[str, Any]:
    """Analyze overall competitive landscape"""
    if not competitors:
        return {'message': 'No competitors found'}
    
    total = len(competitors)
    
    # Market dominance
    top_3_visibility = sum(c['visibility'] for c in competitors[:3]) / 3 if len(competitors) >= 3 else 0
    
    # Average metrics
    avg_visibility = sum(c['visibility'] for c in competitors) / total
    avg_position = sum(c['avg_position'] for c in competitors) / total
    
    return {
        'market_concentration': 'High' if top_3_visibility > 60 else 'Medium' if top_3_visibility > 40 else 'Low',
        'average_competitor_visibility': round(avg_visibility, 1),
        'average_competitor_position': round(avg_position, 1),
        'competition_level': 'Very High' if avg_visibility > 70 else 'High' if avg_visibility > 50 else 'Medium' if avg_visibility > 30 else 'Low',
        'top_3_dominance': round(top_3_visibility, 1)
    }


def generate_ranking_recommendations(summary: Dict, rankings: List[Dict]) -> List[str]:
    """Generate recommendations based on ranking data"""
    recommendations = []
    
    visibility = summary.get('visibility_score', 0)
    avg_pos = summary.get('average_position')
    top_10 = summary.get('rankings_by_position', {}).get('top_10', 0)
    not_ranking = summary.get('keywords_not_ranking', 0)
    
    if visibility < 30:
        recommendations.append("🚨 Low visibility score - urgent SEO improvements needed")
        recommendations.append("Focus on on-page optimization and building quality backlinks")
    elif visibility < 50:
        recommendations.append("⚠️ Below average visibility - improve content and technical SEO")
    elif visibility < 70:
        recommendations.append("📊 Good visibility - push for higher positions with content updates")
    else:
        recommendations.append("✅ Excellent visibility - maintain momentum and expand keyword targeting")
    
    if avg_pos and avg_pos > 10:
        recommendations.append(f"📍 Average position {avg_pos:.1f} - target top 10 for better CTR")
    elif avg_pos and avg_pos > 5:
        recommendations.append(f"📍 Average position {avg_pos:.1f} - push for top 3 positions")
    
    if not_ranking > 0:
        recommendations.append(f"🔍 {not_ranking} keywords not ranking in top 100 - create targeted content")
    
    if top_10 > 0:
        recommendations.append(f"🎯 {top_10} keywords in top 10 - optimize for featured snippets")
    
    return recommendations


def generate_competitor_recommendations(domain: str, competitors: List[Dict], keywords: List[str]) -> List[str]:
    """Generate recommendations based on competitor analysis"""
    recommendations = []
    
    if not competitors:
        recommendations.append("✅ Low competition - great opportunity to dominate this space")
        return recommendations
    
    top_competitor = competitors[0]
    top_visibility = top_competitor['visibility']
    
    if top_visibility > 80:
        recommendations.append(f"🔴 Strong competitor: {top_competitor['domain']} (visibility: {top_visibility}%)")
        recommendations.append("Study their content strategy and backlink profile")
        recommendations.append("Consider targeting long-tail variations and niche topics")
    elif top_visibility > 60:
        recommendations.append(f"⚠️ Moderate competition from: {top_competitor['domain']}")
        recommendations.append("Create more comprehensive content to compete")
    else:
        recommendations.append(f"📊 Balanced competition - opportunity to rank with good content")
    
    # Check if multiple competitors dominate
    if len(competitors) >= 3 and sum(c['visibility'] for c in competitors[:3]) / 3 > 60:
        recommendations.append("⚠️ Top 3 competitors dominate the space - requires strong SEO strategy")
        recommendations.append("Build topical authority with content clusters")
    
    # Analyze competitor keywords
    common_keywords = set()
    for comp in competitors[:3]:
        common_keywords.update(comp['keywords_ranking'])
    
    if len(common_keywords) > len(keywords) * 0.7:
        recommendations.append(f"💡 Competitors rank for {len(common_keywords)} common keywords")
        recommendations.append("Analyze their content to find gaps and opportunities")
    
    return recommendations


if __name__ == "__main__":
    # Example usage
    print("SerpAPI Integration Test")
    print("=" * 50)
    
    # Test keyword analysis
    result = analyze_keyword_difficulty("python programming")
    print(f"\nKeyword: {result.get('keyword')}")
    print(f"Difficulty: {result.get('difficulty_level')} ({result.get('difficulty_score')})")
    print(f"Unique Domains: {result.get('factors', {}).get('unique_domains_top_10')}")
    
    # Test SERP analysis
    serp = analyze_serp_results("best seo tools")
    print(f"\n\nSERP Analysis for: {serp.get('query')}")
    print(f"Organic Results: {serp.get('serp_metrics', {}).get('total_organic_results')}")
    print(f"SERP Features: {serp.get('serp_metrics', {}).get('serp_features_count')}")
