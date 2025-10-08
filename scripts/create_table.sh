#!/bin/bash

# Script to create the seo_reports table in Supabase

echo "🔨 Creating seo_reports table in Supabase..."
echo ""

# Supabase credentials
SUPABASE_PROJECT_REF="pjmwbwxuwinvstpvbrxf"
SUPABASE_URL="https://pjmwbwxuwinvstpvbrxf.supabase.co"
SERVICE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBqbXdid3h1d2ludnN0cHZicnhmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1OTg2NTc2NywiZXhwIjoyMDc1NDQxNzY3fQ.tyUoea0gG7tbvU_-9LKw_KXuYt09mZXfQA1z-gsorWI"

# Check if table exists
echo "🔍 Checking if table exists..."
RESPONSE=$(curl -s -X GET "$SUPABASE_URL/rest/v1/seo_reports?limit=1" \
  -H "apikey: $SERVICE_KEY" \
  -H "Authorization: Bearer $SERVICE_KEY")

if echo "$RESPONSE" | grep -q "PGRST205"; then
    echo "❌ Table does not exist yet"
    echo ""
    echo "⚠️  Die Tabelle muss über das Supabase Dashboard erstellt werden."
    echo ""
    echo "📋 ANLEITUNG:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "1️⃣  Öffnen Sie diesen Link in Ihrem Browser:"
    echo ""
    echo "    https://supabase.com/dashboard/project/$SUPABASE_PROJECT_REF/editor"
    echo ""
    echo "2️⃣  Klicken Sie links auf 'SQL Editor' oder öffnen Sie:"
    echo ""
    echo "    https://supabase.com/dashboard/project/$SUPABASE_PROJECT_REF/sql/new"
    echo ""
    echo "3️⃣  Fügen Sie dieses SQL ein und klicken auf 'RUN':"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    cat infra/supabase/schema.sql
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "4️⃣  Nach dem Ausführen, testen Sie erneut mit:"
    echo ""
    echo "    ./scripts/create_table.sh"
    echo ""
elif echo "$RESPONSE" | grep -q "\[\]"; then
    echo "✅ Table exists! (empty)"
    echo ""
    echo "🧪 Testing with a sample insert..."
    
    # Try to insert a test record
    TEST_ID="test-$(date +%s)000"
    INSERT_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$SUPABASE_URL/rest/v1/seo_reports" \
      -H "apikey: $SERVICE_KEY" \
      -H "Authorization: Bearer $SERVICE_KEY" \
      -H "Content-Type: application/json" \
      -H "Prefer: return=representation" \
      -d "{
        \"id\": \"$TEST_ID\",
        \"payload\": {
          \"url\": \"https://example.com\",
          \"test\": true,
          \"onpage\": {\"title\": \"Test\"},
          \"keywords\": {\"total_words\": 0},
          \"performance\": {\"note\": \"test\"}
        }
      }")
    
    HTTP_CODE=$(echo "$INSERT_RESPONSE" | tail -n1)
    RESPONSE_BODY=$(echo "$INSERT_RESPONSE" | head -n-1)
    
    if [ "$HTTP_CODE" = "201" ] || [ "$HTTP_CODE" = "200" ]; then
        echo "✅ Test-Record erfolgreich eingefügt!"
        echo "   Record ID: $TEST_ID"
        echo ""
        echo "🎉 Supabase ist vollständig konfiguriert und bereit!"
        echo ""
        echo "Sie können jetzt das System starten:"
        echo "  ./scripts/start.sh"
        echo ""
        echo "Oder mit Docker Compose:"
        echo "  docker compose up --build"
    else
        echo "⚠️  Insert fehlgeschlagen (HTTP $HTTP_CODE)"
        echo "Response: $RESPONSE_BODY"
    fi
else
    echo "✅ Table exists and has data!"
    echo ""
    echo "🎉 Supabase ist vollständig konfiguriert!"
    echo ""
    echo "Sie können das System jetzt starten:"
    echo "  ./scripts/start.sh"
fi
