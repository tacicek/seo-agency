# SerpAPI Integration Guide

Complete guide to using SerpAPI integration in the SEO Analyzer system.

## Overview

SerpAPI integration provides comprehensive Google Search results analysis including:
- **Organic search results** (Top 100 positions)
- **Featured Snippets** (Position 0)
- **People Also Ask** questions
- **Knowledge Graph** data
- **Related Searches**
- **Local Pack** results
- **SERP Features** detection
- **Keyword Difficulty** scoring
- **Ranking Opportunities** analysis

## Setup

### 1. Get SerpAPI API Key

1. Visit [https://serpapi.com/](https://serpapi.com/)
2. Create a free account
3. Get your API key from dashboard

**Free Tier**: 100 searches/month  
**Paid Plans**: Starting at $50/month for 5,000 searches

### 2. Configure Environment

Add your API key to `.env` file:

```bash
SERPAPI_API_KEY=your_api_key_here
```

### 3. Verify Installation

Test the connection:

```bash
curl http://localhost:8000/serp/test
```

Expected response:
```json
{
  "status": "success",
  "message": "SerpAPI connection successful",
  "test_result": {
    "keyword": "test query",
    "difficulty_score": 45.2,
    "difficulty_level": "Medium"
  }
}
```

## API Endpoints

### 1. Full SERP Analysis

**Endpoint**: `POST /serp/analyze`

Analyze complete Google search results for a keyword.

**Request**:
```json
{
  "keyword": "python programming",
  "location": "United States"
}
```

**Response**:
```json
{
  "query": "python programming",
  "location": "United States",
  "organic_results": [
    {
      "position": 1,
      "title": "Welcome to Python.org",
      "link": "https://www.python.org/",
      "snippet": "The official home of the Python Programming Language...",
      "sitelinks": [...]
    }
  ],
  "featured_snippet": {
    "type": "paragraph",
    "title": "What is Python?",
    "snippet": "Python is an interpreted, high-level programming language...",
    "link": "https://..."
  },
  "people_also_ask": [
    {
      "question": "What is Python used for?",
      "snippet": "Python is commonly used for...",
      "link": "https://..."
    }
  ],
  "knowledge_graph": {
    "title": "Python",
    "type": "Programming language",
    "description": "...",
    "website": "https://www.python.org"
  },
  "related_searches": [
    "python tutorial",
    "python download",
    "python for beginners"
  ],
  "serp_metrics": {
    "total_organic_results": 100,
    "unique_domains_top_10": 8,
    "serp_features_present": [
      "featured_snippet",
      "people_also_ask",
      "knowledge_graph"
    ],
    "serp_features_count": 3,
    "competition_level": "Medium - Competitive"
  },
  "ranking_opportunities": {
    "total_opportunities": 4,
    "opportunities": [
      {
        "type": "featured_snippet",
        "priority": "high",
        "recommendation": "Featured snippet occupied by python.org - analyze their content format",
        "current_holder": "https://www.python.org"
      },
      {
        "type": "content_expansion",
        "priority": "high",
        "recommendation": "Create content answering 8 related questions to increase topical authority",
        "questions": [
          "What is Python used for?",
          "Is Python easy to learn?",
          ...
        ]
      }
    ]
  }
}
```

### 2. Keyword Difficulty Analysis

**Endpoint**: `POST /serp/difficulty`

Calculate keyword difficulty score (0-100).

**Request**:
```json
{
  "keyword": "seo tools",
  "location": "United States"
}
```

**Response**:
```json
{
  "keyword": "seo tools",
  "difficulty_score": 67.5,
  "difficulty_level": "Hard",
  "color": "orange",
  "factors": {
    "unique_domains_top_10": 7,
    "serp_features_count": 4,
    "domain_diversity_impact": 21.0,
    "serp_features_penalty": 40
  },
  "recommendations": [
    "⚠️ High competition - Requires strong SEO strategy",
    "Focus on topical authority and high-quality backlinks",
    "⚡ Only 7 unique domains in top 10 - some sites have multiple positions",
    "⚠️ 4 SERP features present - organic CTR may be lower"
  ]
}
```

**Difficulty Levels**:
- **0-30**: Easy (Green) - Great opportunity for quick rankings
- **30-50**: Medium (Yellow) - Achievable with consistent effort
- **50-70**: Hard (Orange) - Requires strong SEO strategy
- **70-100**: Very Hard (Red) - Long-term strategy needed

### 3. Batch Keyword Analysis

**Endpoint**: `POST /serp/batch`

Analyze multiple keywords at once.

**Request**:
```json
{
  "keywords": [
    "seo tools",
    "keyword research",
    "backlink checker",
    "site audit",
    "rank tracker"
  ],
  "location": "United States"
}
```

**Response**:
```json
{
  "total_keywords": 5,
  "average_difficulty": 52.3,
  "distribution": {
    "easy": 1,
    "medium": 2,
    "hard": 2,
    "very_hard": 0
  },
  "keywords": [
    {
      "keyword": "seo tools",
      "difficulty_score": 67.5,
      "difficulty_level": "Hard",
      ...
    },
    ...
  ],
  "recommendation": "📊 Balanced keyword set - mix of quick wins and medium-term targets"
}
```

### 4. Integrated Analysis with SERP

**Endpoint**: `POST /analyze`

Include SERP analysis in main SEO analysis.

**Request**:
```json
{
  "url": "https://example.com",
  "include_serp": true,
  "keyword": "target keyword"
}
```

**Response**: Complete SEO report with SERP data included.

## Python Integration

### Direct Usage

```python
from analyzers.serpapi import (
    analyze_serp_results,
    analyze_keyword_difficulty,
    batch_keyword_analysis
)

# Full SERP analysis
serp_data = analyze_serp_results("python programming")
print(f"Organic Results: {len(serp_data['organic_results'])}")
print(f"SERP Features: {serp_data['serp_metrics']['serp_features_present']}")

# Keyword difficulty
difficulty = analyze_keyword_difficulty("seo tools")
print(f"Difficulty: {difficulty['difficulty_level']} ({difficulty['difficulty_score']})")

# Batch analysis
results = batch_keyword_analysis(["seo", "marketing", "analytics"])
print(f"Average Difficulty: {results['average_difficulty']}")
```

### Example: Find Easy Keywords

```python
from analyzers.serpapi import batch_keyword_analysis

keywords = [
    "on page seo",
    "technical seo",
    "local seo",
    "seo audit",
    "backlink analysis",
    "keyword research tools",
    "seo reporting software"
]

results = batch_keyword_analysis(keywords)

# Filter easy keywords
easy_keywords = [
    kw for kw in results['keywords']
    if kw['difficulty_score'] < 30
]

print(f"Found {len(easy_keywords)} easy keywords:")
for kw in easy_keywords:
    print(f"- {kw['keyword']}: {kw['difficulty_score']}")
```

### Example: Competitor Analysis

```python
from analyzers.serpapi import analyze_serp_results

# Analyze your target keyword
serp = analyze_serp_results("best seo tools 2024")

# Get top 10 competitors
competitors = []
for result in serp['organic_results'][:10]:
    competitors.append({
        'position': result['position'],
        'domain': result['displayed_link'],
        'title': result['title'],
        'has_sitelinks': len(result.get('sitelinks', [])) > 0,
        'has_rich_snippet': bool(result.get('rich_snippet'))
    })

print("Top 10 Competitors:")
for comp in competitors:
    print(f"{comp['position']}. {comp['domain']}")
    print(f"   Sitelinks: {'Yes' if comp['has_sitelinks'] else 'No'}")
    print(f"   Rich Snippet: {'Yes' if comp['has_rich_snippet'] else 'No'}")
```

## Understanding SERP Metrics

### Organic Results

```python
{
  "position": 1,
  "title": "Page Title",
  "link": "https://example.com/page",
  "displayed_link": "example.com › page",
  "snippet": "Meta description or page excerpt...",
  "rich_snippet": {
    "rated": {
      "rating": 4.5,
      "votes": 150
    }
  },
  "sitelinks": [
    {
      "title": "About",
      "link": "https://example.com/about"
    }
  ]
}
```

### Featured Snippet (Position 0)

```python
{
  "type": "paragraph",  # or "list", "table", "video"
  "title": "What is SEO?",
  "snippet": "SEO is the practice of optimizing...",
  "link": "https://source.com",
  "extensions": ["3 min read"]
}
```

### People Also Ask

```python
[
  {
    "question": "What is on-page SEO?",
    "snippet": "On-page SEO refers to...",
    "link": "https://answer-source.com"
  }
]
```

### SERP Features Detection

The system automatically detects:
- ✅ Featured Snippet
- ✅ Knowledge Graph
- ✅ People Also Ask
- ✅ Local Pack (Map results)
- ✅ News Results
- ✅ Shopping Results
- ✅ Image Pack
- ✅ Video Carousel

## Keyword Difficulty Algorithm

```
Base Score = 70 (starting point)

Domain Diversity Impact:
  - unique_domains / 10 * 30 (max 30 points reduction)
  
SERP Features Penalty:
  - Each feature adds +10 to difficulty
  
Final Score = max(0, min(100, Base - Domain Diversity + Feature Penalty))

Classification:
  0-30:   Easy (Green)
  30-50:  Medium (Yellow)
  50-70:  Hard (Orange)
  70-100: Very Hard (Red)
```

**Example Calculation**:
- Keyword: "seo tools"
- Unique domains in top 10: 7
- SERP features: 4 (Featured Snippet, PAA, Knowledge Graph, Shopping)

```
Domain Impact = (7/10) * 30 = 21
Feature Penalty = 4 * 10 = 40
Score = 70 - 21 + 40 = 89 (Very Hard)
```

## Rate Limits

### Free Tier
- **100 searches/month**
- ~3 searches/day
- Best for: Testing and small projects

### Paid Plans
- **Starter**: $50/month = 5,000 searches
- **Professional**: $100/month = 15,000 searches
- **Advanced**: $250/month = 40,000 searches

### Rate Limit Handling

```python
from analyzers.serpapi import analyze_keyword_difficulty

result = analyze_keyword_difficulty("test keyword")

if 'error' in result:
    if 'rate limit' in result['error'].lower():
        print("⚠️ Rate limit reached. Wait until next month or upgrade plan.")
    elif 'api key' in result['error'].lower():
        print("❌ Invalid API key. Check SERPAPI_API_KEY in .env")
    else:
        print(f"Error: {result['error']}")
```

## Best Practices

### 1. Optimize API Usage

**❌ Don't**:
```python
# Wasteful - uses 100 API calls
for keyword in keywords:
    result = analyze_serp_results(keyword)
```

**✅ Do**:
```python
# Efficient - uses 1 API call per keyword
results = batch_keyword_analysis(keywords)
```

### 2. Cache Results

```python
import json
from datetime import datetime

def get_cached_serp(keyword):
    cache_file = f"cache/serp_{keyword.replace(' ', '_')}.json"
    
    try:
        with open(cache_file, 'r') as f:
            cached = json.load(f)
            # Use cache if less than 7 days old
            if (datetime.now() - datetime.fromisoformat(cached['timestamp'])).days < 7:
                return cached['data']
    except:
        pass
    
    # Fetch fresh data
    data = analyze_serp_results(keyword)
    
    # Save to cache
    with open(cache_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'data': data
        }, f)
    
    return data
```

### 3. Handle Errors Gracefully

```python
def safe_serp_analysis(keyword):
    try:
        result = analyze_keyword_difficulty(keyword)
        
        if 'error' in result:
            return {
                'keyword': keyword,
                'status': 'error',
                'message': result['error']
            }
        
        return result
        
    except Exception as e:
        return {
            'keyword': keyword,
            'status': 'error',
            'message': str(e)
        }
```

## Use Cases

### 1. Keyword Research

Find easy keywords in your niche:
```python
keywords = ["your", "keyword", "list"]
results = batch_keyword_analysis(keywords)

easy = [k for k in results['keywords'] if k['difficulty_score'] < 30]
print(f"Found {len(easy)} easy keywords to target")
```

### 2. Content Gap Analysis

Find questions your competitors aren't answering:
```python
serp = analyze_serp_results("your topic")
questions = serp['people_also_ask']

for q in questions:
    print(f"📝 Content idea: {q['question']}")
```

### 3. SERP Feature Opportunities

Identify features you can target:
```python
serp = analyze_serp_results("your keyword")
features = serp['serp_metrics']['serp_features_present']

if 'featured_snippet' not in features:
    print("🎯 Featured snippet opportunity - no one owns position 0!")

if 'people_also_ask' in features:
    print(f"📚 Create FAQ content for {len(serp['people_also_ask'])} questions")
```

### 4. Competitor Tracking

Monitor competitor rankings:
```python
def track_competitor(competitor_domain, keyword):
    serp = analyze_serp_results(keyword)
    
    for result in serp['organic_results']:
        if competitor_domain in result['link']:
            return {
                'keyword': keyword,
                'position': result['position'],
                'title': result['title'],
                'has_featured_snippet': bool(serp['featured_snippet'])
            }
    
    return {'keyword': keyword, 'position': None}
```

## Troubleshooting

### Error: "SERPAPI_API_KEY not set"

**Solution**: Add API key to `.env`:
```bash
SERPAPI_API_KEY=your_actual_api_key_here
```

### Error: "Invalid API key"

**Solution**: Verify your API key at [https://serpapi.com/dashboard](https://serpapi.com/dashboard)

### Error: "Rate limit exceeded"

**Solution**: 
1. Wait until next month (free tier resets monthly)
2. Upgrade to paid plan
3. Implement caching to reduce API calls

### Empty Results

**Issue**: No organic results returned

**Solution**:
```python
result = analyze_serp_results("keyword", location="Global")
# Try different locations if results are empty
```

## Advanced Features

### Custom Location Targeting

```python
# Target specific countries
us_serp = analyze_serp_results("seo tools", location="United States")
uk_serp = analyze_serp_results("seo tools", location="United Kingdom")
de_serp = analyze_serp_results("seo tools", location="Germany")

# Compare difficulty by location
print(f"US Difficulty: {us_difficulty}")
print(f"UK Difficulty: {uk_difficulty}")
print(f"DE Difficulty: {de_difficulty}")
```

### Language-Specific Analysis

```python
# English
en_serp = analyze_serp_results("seo tools", language="en")

# German
de_serp = analyze_serp_results("seo werkzeuge", language="de")

# Turkish
tr_serp = analyze_serp_results("seo araçları", language="tr")
```

## Resources

- **SerpAPI Docs**: https://serpapi.com/search-api
- **Pricing**: https://serpapi.com/pricing
- **API Playground**: https://serpapi.com/playground
- **Status Page**: https://status.serpapi.com/

## Next Steps

1. ✅ Get API key from serpapi.com
2. ✅ Add to `.env` file
3. ✅ Test connection: `curl http://localhost:8000/serp/test`
4. 📊 Start analyzing keywords
5. 🎯 Find ranking opportunities
6. 📈 Track competitors

## Support

For issues or questions:
- SerpAPI Support: support@serpapi.com
- Documentation: https://serpapi.com/docs

---

**Integration Complete!** 🎉

Your SEO analyzer now has powerful Google SERP analysis capabilities.
