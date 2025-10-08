#!/bin/bash

echo "================================================"
echo "SerpAPI Integration Test"
echo "================================================"
echo ""

# Check if API key is set
if [ -z "$SERPAPI_API_KEY" ]; then
    echo "❌ SERPAPI_API_KEY not set in environment"
    echo ""
    echo "Please add to .env file:"
    echo "SERPAPI_API_KEY=your_api_key_here"
    echo ""
    echo "Get your API key from: https://serpapi.com/"
    exit 1
fi

echo "✅ SERPAPI_API_KEY is set"
echo ""

# Check if Docker container is running
if ! docker ps | grep -q seo-api; then
    echo "❌ Docker container 'seo-api' is not running"
    echo ""
    echo "Start with: docker compose up -d"
    exit 1
fi

echo "✅ Docker container is running"
echo ""

# Test 1: API Connection
echo "Test 1: Testing SerpAPI connection..."
response=$(curl -s http://localhost:8000/serp/test)

if echo "$response" | grep -q '"status":"success"'; then
    echo "✅ SerpAPI connection successful"
else
    echo "❌ SerpAPI connection failed"
    echo "Response: $response"
fi

echo ""

# Test 2: Keyword Difficulty
echo "Test 2: Testing keyword difficulty analysis..."
response=$(curl -s -X POST http://localhost:8000/serp/difficulty \
  -H "Content-Type: application/json" \
  -d '{"keyword":"python programming","location":"United States"}')

if echo "$response" | grep -q '"difficulty_score"'; then
    difficulty=$(echo "$response" | grep -o '"difficulty_score":[0-9.]*' | cut -d':' -f2)
    level=$(echo "$response" | grep -o '"difficulty_level":"[^"]*"' | cut -d'"' -f4)
    echo "✅ Keyword difficulty analysis working"
    echo "   Keyword: python programming"
    echo "   Difficulty: $level ($difficulty)"
else
    echo "❌ Keyword difficulty analysis failed"
    echo "Response: $response"
fi

echo ""

# Test 3: Batch Analysis
echo "Test 3: Testing batch keyword analysis..."
response=$(curl -s -X POST http://localhost:8000/serp/batch \
  -H "Content-Type: application/json" \
  -d '{"keywords":["seo","marketing","analytics"],"location":"United States"}')

if echo "$response" | grep -q '"total_keywords"'; then
    total=$(echo "$response" | grep -o '"total_keywords":[0-9]*' | cut -d':' -f2)
    avg=$(echo "$response" | grep -o '"average_difficulty":[0-9.]*' | cut -d':' -f2)
    echo "✅ Batch analysis working"
    echo "   Keywords analyzed: $total"
    echo "   Average difficulty: $avg"
else
    echo "❌ Batch analysis failed"
    echo "Response: $response"
fi

echo ""

# Test 4: Full SERP Analysis
echo "Test 4: Testing full SERP analysis..."
response=$(curl -s -X POST http://localhost:8000/serp/analyze \
  -H "Content-Type: application/json" \
  -d '{"keyword":"best seo tools","location":"United States"}')

if echo "$response" | grep -q '"organic_results"'; then
    organic_count=$(echo "$response" | grep -o '"position":[0-9]*' | wc -l)
    features=$(echo "$response" | grep -o '"serp_features_count":[0-9]*' | cut -d':' -f2)
    echo "✅ Full SERP analysis working"
    echo "   Organic results: $organic_count"
    echo "   SERP features: $features"
else
    echo "❌ SERP analysis failed"
    echo "Response: $response"
fi

echo ""
echo "================================================"
echo "Test Summary"
echo "================================================"
echo ""
echo "All tests completed! Check results above."
echo ""
echo "Next steps:"
echo "1. Try the API endpoints manually"
echo "2. Check SERPAPI_INTEGRATION.md for usage examples"
echo "3. Monitor your API usage at: https://serpapi.com/dashboard"
echo ""
