#!/bin/bash

# Supabase Setup Script
# This script helps you set up your Supabase database

echo "🚀 Supabase Setup Helper"
echo "============================================================"
echo ""

# Load .env file
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Check if credentials are set
if [ -z "$NEXT_PUBLIC_SUPABASE_URL" ]; then
    echo "❌ NEXT_PUBLIC_SUPABASE_URL is not set in .env"
    exit 1
fi

echo "✅ Supabase URL: $NEXT_PUBLIC_SUPABASE_URL"
echo ""

# Print instructions
echo "📋 SETUP INSTRUCTIONS"
echo "============================================================"
echo ""
echo "1️⃣  Open your Supabase Dashboard:"
echo "   $NEXT_PUBLIC_SUPABASE_URL"
echo ""
echo "2️⃣  Navigate to: SQL Editor (left sidebar)"
echo ""
echo "3️⃣  Click 'New Query' and paste the following SQL:"
echo ""
echo "------------------------------------------------------------"
cat infra/supabase/schema.sql
echo "------------------------------------------------------------"
echo ""
echo "4️⃣  Click 'Run' to create the table"
echo ""
echo "5️⃣  Get your Service Role Key:"
echo "   - Go to Settings → API"
echo "   - Find 'service_role' key (under 'Project API keys')"
echo "   - Copy it and add to .env:"
echo "     SUPABASE_SERVICE_KEY=your_service_key_here"
echo ""
echo "6️⃣  (Optional) Configure Row Level Security (RLS):"
echo "   - Go to Authentication → Policies"
echo "   - Add policies for the seo_reports table"
echo ""
echo "============================================================"
echo ""
echo "After completing these steps, restart your Docker containers:"
echo "  docker-compose down"
echo "  docker-compose up --build"
echo ""
