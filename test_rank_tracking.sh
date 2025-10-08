#!/bin/bash

###############################################################################
# Rank Tracking & Competitor Analysis Test Script
# Tests the new SERP API endpoints
###############################################################################

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║     🎯 RANK TRACKING & COMPETITOR ANALYSIS TEST 🎯              ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

API_BASE="http://localhost:8000"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

###############################################################################
# Test 1: Rank Tracking
###############################################################################

echo -e "${BLUE}═══════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}TEST 1: Rank Tracking${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════${NC}"
echo ""

echo "Testing rank tracking for bs-company.ch..."
echo ""

RANK_RESPONSE=$(curl -s -X POST "${API_BASE}/serp/rank-tracking" \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "bs-company.ch",
    "keywords": ["umzug zürich", "umzugsfirma zürich", "transport zürich"],
    "location": "Switzerland",
    "language": "de"
  }')

echo "$RANK_RESPONSE" | jq '{
  summary: .summary,
  sample_ranking: .rankings[0],
  recommendations: .recommendations
}'

echo ""
echo -e "${YELLOW}✅ Rank Tracking Test Complete${NC}"
echo ""

###############################################################################
# Test 2: Competitor Analysis
###############################################################################

echo -e "${BLUE}═══════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}TEST 2: Competitor Analysis${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════${NC}"
echo ""

echo "Analyzing top competitors for umzug zürich..."
echo ""

COMP_RESPONSE=$(curl -s -X POST "${API_BASE}/serp/competitor-analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "bs-company.ch",
    "keywords": ["umzug zürich", "umzugsfirma zürich", "möbeltransport zürich"],
    "location": "Switzerland",
    "language": "de"
  }')

echo "$COMP_RESPONSE" | jq '{
  your_domain: .your_domain,
  keywords_analyzed: .keywords_analyzed,
  total_competitors: .total_competitors_found,
  top_5_competitors: .top_competitors[:5] | map({
    domain,
    visibility,
    avg_position,
    appearances,
    best_position
  }),
  competitive_landscape: .competitive_landscape,
  recommendations: .recommendations
}'

echo ""
echo -e "${YELLOW}✅ Competitor Analysis Test Complete${NC}"
echo ""

###############################################################################
# Test 3: Example.com Rank Tracking (English)
###############################################################################

echo -e "${BLUE}═══════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}TEST 3: English Keywords Rank Tracking${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════${NC}"
echo ""

echo "Testing English keywords for example.com..."
echo ""

EXAMPLE_RANK=$(curl -s -X POST "${API_BASE}/serp/rank-tracking" \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "example.com",
    "keywords": ["example", "example domain"],
    "location": "United States",
    "language": "en"
  }')

echo "$EXAMPLE_RANK" | jq '{
  summary: .summary,
  rankings: .rankings | map({
    keyword,
    position,
    status,
    page
  })
}'

echo ""
echo -e "${YELLOW}✅ English Keywords Test Complete${NC}"
echo ""

###############################################################################
# Summary
###############################################################################

echo -e "${BLUE}═══════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}🎉 ALL TESTS COMPLETE!${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════════${NC}"
echo ""

echo "Available Endpoints:"
echo "  1. POST /serp/rank-tracking       - Track keyword rankings"
echo "  2. POST /serp/competitor-analysis - Analyze top competitors"
echo "  3. POST /serp/difficulty          - Keyword difficulty"
echo "  4. POST /serp/batch               - Batch keyword analysis"
echo "  5. POST /serp/analyze             - Full SERP analysis"
echo ""

echo "Next Steps:"
echo "  • Check your actual rankings for target keywords"
echo "  • Analyze your top competitors' strategies"
echo "  • Monitor ranking changes over time"
echo "  • Optimize content based on recommendations"
echo ""
