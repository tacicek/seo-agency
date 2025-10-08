#!/usr/bin/env python3
"""
Script to set up Supabase database tables and test connection
"""
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
NEXT_PUBLIC_SUPABASE_ANON_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")

def test_connection():
    """Test Supabase connection"""
    print("🔍 Testing Supabase connection...")
    
    if not SUPABASE_URL or not NEXT_PUBLIC_SUPABASE_ANON_KEY:
        print("❌ Missing SUPABASE_URL or NEXT_PUBLIC_SUPABASE_ANON_KEY")
        return False
    
    # Test with anon key (read-only operations)
    url = f"{SUPABASE_URL}/rest/v1/"
    headers = {
        "apikey": NEXT_PUBLIC_SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {NEXT_PUBLIC_SUPABASE_ANON_KEY}"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            print("✅ Supabase connection successful!")
            return True
        else:
            print(f"⚠️  Connection returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def check_table_exists():
    """Check if seo_reports table exists"""
    print("\n🔍 Checking if 'seo_reports' table exists...")
    
    if not SUPABASE_URL or not NEXT_PUBLIC_SUPABASE_ANON_KEY:
        print("❌ Missing credentials")
        return False
    
    url = f"{SUPABASE_URL}/rest/v1/seo_reports?limit=1"
    headers = {
        "apikey": NEXT_PUBLIC_SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {NEXT_PUBLIC_SUPABASE_ANON_KEY}"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            print("✅ Table 'seo_reports' exists and is accessible!")
            return True
        elif response.status_code == 404:
            print("⚠️  Table 'seo_reports' not found. Please create it using the SQL Editor in Supabase.")
            return False
        else:
            print(f"⚠️  Unexpected status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error checking table: {e}")
        return False

def print_setup_instructions():
    """Print instructions for manual setup"""
    print("\n" + "="*60)
    print("📋 SETUP INSTRUCTIONS")
    print("="*60)
    print("\n1️⃣  Go to your Supabase Dashboard:")
    print(f"   {SUPABASE_URL.replace('/rest/v1', '')}")
    
    print("\n2️⃣  Navigate to: SQL Editor")
    
    print("\n3️⃣  Run this SQL query to create the table:")
    print("\n" + "-"*60)
    with open("infra/supabase/schema.sql", "r") as f:
        print(f.read())
    print("-"*60)
    
    print("\n4️⃣  Enable Row Level Security (RLS) if needed:")
    print("   - Go to Authentication → Policies")
    print("   - Add policies for your use case")
    
    print("\n5️⃣  Get your Service Role Key:")
    print("   - Go to Settings → API")
    print("   - Copy the 'service_role' key (NOT the anon key)")
    print("   - Add it to .env as SUPABASE_SERVICE_KEY")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    print("🚀 Supabase Setup Script")
    print("="*60 + "\n")
    
    # Test connection
    if test_connection():
        # Check if table exists
        table_exists = check_table_exists()
        
        if not table_exists:
            print_setup_instructions()
        else:
            print("\n✨ Your Supabase database is ready to use!")
            
            if not SUPABASE_SERVICE_KEY:
                print("\n⚠️  Note: SUPABASE_SERVICE_KEY is not set.")
                print("   This is needed for write operations from the API.")
                print("   You can find it in: Settings → API → service_role key")
    else:
        print("\n❌ Failed to connect to Supabase.")
        print("   Please check your credentials in .env file.")
