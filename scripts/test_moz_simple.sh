#!/bin/bash

# Simple MOZ API test using curl

echo "🔍 MOZ API Test Script"
echo "======================================"
echo ""

# Load .env
export $(cat .env | grep -v '^#' | xargs)

echo "Testing MOZ API with curl..."
echo ""
echo "Access ID: $MOZ_ACCESS_ID"
echo "Secret Key: ${MOZ_SECRET_KEY:0:20}..."
echo ""

# Create Basic Auth header
AUTH=$(echo -n "$MOZ_ACCESS_ID:$MOZ_SECRET_KEY" | base64)

echo "Making request to MOZ API..."
echo ""

# Test with moz.com
RESPONSE=$(curl -s -X POST "https://lsapi.seomoz.com/v2/url_metrics" \
  -H "Authorization: Basic $AUTH" \
  -H "Content-Type: application/json" \
  -d '{"targets": ["https://moz.com"]}')

echo "Response:"
echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
echo ""

# Check if successful
if echo "$RESPONSE" | grep -q '"domain_authority"'; then
    echo "✅ MOZ API test successful!"
    echo ""
    DA=$(echo "$RESPONSE" | grep -o '"domain_authority":[0-9]*' | grep -o '[0-9]*')
    PA=$(echo "$RESPONSE" | grep -o '"page_authority":[0-9]*' | grep -o '[0-9]*')
    echo "Domain Authority: $DA"
    echo "Page Authority: $PA"
else
    echo "❌ MOZ API test failed"
    echo ""
    echo "Please check:"
    echo "  1. MOZ_ACCESS_ID is correct"
    echo "  2. MOZ_SECRET_KEY is correct"
    echo "  3. API credentials are active"
fi

echo ""
echo "======================================"
