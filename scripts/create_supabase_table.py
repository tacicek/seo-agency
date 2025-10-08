#!/usr/bin/env python3
"""
Script to create the seo_reports table in Supabase via REST API
"""
import os
import sys

# Add parent directory to path to use the API's requests module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'apps', 'api'))

try:
    import requests
except ImportError:
    print("❌ requests module not found. Please run from Docker or install: pip install requests")
    sys.exit(1)

# Supabase credentials from .env
SUPABASE_URL = "https://pjmwbwxuwinvstpvbrxf.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBqbXdid3h1d2ludnN0cHZicnhmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1OTg2NTc2NywiZXhwIjoyMDc1NDQxNzY3fQ.tyUoea0gG7tbvU_-9LKw_KXuYt09mZXfQA1z-gsorWI"

def create_table_via_sql():
    """Create table using Supabase SQL endpoint"""
    print("🔨 Creating seo_reports table in Supabase...")
    
    # SQL to create the table
    sql = """
    CREATE TABLE IF NOT EXISTS public.seo_reports (
        id text PRIMARY KEY,
        payload jsonb NOT NULL,
        created_at timestamp with time zone DEFAULT now()
    );
    """
    
    # Use PostgREST RPC or Management API
    # Note: Direct SQL execution requires Management API or SQL Editor
    print("\n⚠️  Tabelle muss manuell erstellt werden.")
    print("\nBitte folgen Sie diesen Schritten:\n")
    print("1️⃣  Öffnen Sie: https://supabase.com/dashboard/project/pjmwbwxuwinvstpvbrxf/sql/new")
    print("\n2️⃣  Fügen Sie dieses SQL ein:\n")
    print("-" * 70)
    print(sql.strip())
    print("-" * 70)
    print("\n3️⃣  Klicken Sie auf 'RUN' oder 'AUSFÜHREN'\n")
    
    return False

def test_table_exists():
    """Test if the table exists by trying to query it"""
    print("\n🔍 Prüfe, ob Tabelle existiert...")
    
    url = f"{SUPABASE_URL}/rest/v1/seo_reports?limit=1"
    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Tabelle 'seo_reports' existiert!")
            return True
        elif response.status_code == 404 or "relation" in response.text.lower():
            print("❌ Tabelle 'seo_reports' existiert noch nicht")
            return False
        else:
            print(f"⚠️  Unerwartete Antwort: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Fehler beim Testen: {e}")
        return False

def insert_test_record():
    """Insert a test record to verify everything works"""
    print("\n🧪 Füge Test-Record ein...")
    
    url = f"{SUPABASE_URL}/rest/v1/seo_reports"
    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    
    test_data = {
        "id": "test-" + str(int(__import__('time').time() * 1000)),
        "payload": {
            "url": "https://example.com",
            "test": True,
            "onpage": {"title": "Test"},
            "keywords": {"total_words": 0},
            "performance": {"note": "test"}
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=test_data, timeout=10)
        
        if response.status_code in [200, 201]:
            print("✅ Test-Record erfolgreich eingefügt!")
            print(f"   Record ID: {test_data['id']}")
            return True
        else:
            print(f"❌ Fehler beim Einfügen: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("🚀 Supabase Table Setup Script")
    print("=" * 70)
    
    # Test if table exists
    if test_table_exists():
        print("\n✨ Tabelle ist bereits vorhanden!")
        
        # Try to insert test record
        if insert_test_record():
            print("\n🎉 Alles funktioniert! System ist bereit.")
        else:
            print("\n⚠️  Tabelle existiert, aber Insert hat nicht funktioniert.")
            print("   Prüfen Sie die Berechtigungen.")
    else:
        # Table doesn't exist - show instructions
        create_table_via_sql()
        print("\n💡 Nachdem Sie die Tabelle erstellt haben, führen Sie dieses Script erneut aus:")
        print("   python3 scripts/create_supabase_table.py")
    
    print("\n" + "=" * 70)
