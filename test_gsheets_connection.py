#!/usr/bin/env python3
"""
Test script to check Google Sheets connection status
"""

import os
import sys
import pandas as pd
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

try:
    from streamlit_gsheets import GSheetsConnection
    import gspread
    from google.oauth2.service_account import Credentials
    print("✅ Required packages are installed")
except ImportError as e:
    print(f"❌ Missing package: {e}")
    print("Run: pip install streamlit-gsheets gspread google-auth-oauthlib google-auth-httplib2")
    sys.exit(1)

def check_secrets_config():
    """Check if .streamlit/secrets.toml exists and has gsheets config"""
    secrets_path = project_root / ".streamlit" / "secrets.toml"
    
    if not secrets_path.exists():
        print("❌ .streamlit/secrets.toml not found")
        return False
    
    try:
        with open(secrets_path, 'r') as f:
            content = f.read()
            if 'gsheets' in content and 'connections' in content:
                print("✅ .streamlit/secrets.toml has gsheets configuration")
                return True
            else:
                print("❌ .streamlit/secrets.toml exists but no gsheets config found")
                return False
    except Exception as e:
        print(f"❌ Error reading secrets.toml: {e}")
        return False

def check_service_account():
    """Check if service account file exists"""
    service_account_path = project_root / "service-account.json"
    
    if service_account_path.exists():
        print("✅ service-account.json found")
        return True
    else:
        print("❌ service-account.json not found")
        return False

def test_manual_connection():
    """Test manual Google Sheets connection"""
    service_account_path = project_root / "service-account.json"
    
    if not service_account_path.exists():
        print("❌ Cannot test manual connection without service-account.json")
        return False
    
    try:
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = Credentials.from_service_account_file(
            str(service_account_path), scopes=scopes
        )
        client = gspread.authorize(creds)
        
        # Try to open a sheet by URL or create one
        print("🔍 Testing Google Sheets connection...")
        
        # List available spreadsheets
        spreadsheets = client.list_spreadsheet_files()
        if spreadsheets:
            print(f"✅ Connected! Found {len(spreadsheets)} spreadsheets")
            for sheet in spreadsheets[:3]:  # Show first 3
                print(f"   - {sheet['name']} (ID: {sheet['id']})")
            return True
        else:
            print("⚠️ Connected but no spreadsheets found")
            return False
            
    except Exception as e:
        print(f"❌ Manual connection failed: {e}")
        return False

def main():
    print("🔍 Google Sheets Connection Diagnostic Tool")
    print("=" * 50)
    
    # Check packages
    print("\n📦 Checking required packages...")
    
    # Check configuration
    print("\n⚙️ Checking configuration...")
    secrets_ok = check_secrets_config()
    service_account_ok = check_service_account()
    
    # Check manual connection
    print("\n🔗 Testing connection...")
    manual_ok = test_manual_connection()
    
    # Summary
    print("\n📊 Summary:")
    print(f"   Secrets.toml configured: {'✅' if secrets_ok else '❌'}")
    print(f"   Service account file: {'✅' if service_account_ok else '❌'}")
    print(f"   Manual connection: {'✅' if manual_ok else '❌'}")
    
    if secrets_ok or manual_ok:
        print("\n🎉 Google Sheets connection is working!")
        print("\n📋 Next steps:")
        print("1. Update your .streamlit/secrets.toml with the spreadsheet ID")
        print("2. Run: streamlit run streamlit_ui.py")
        print("3. Login as admin and check the storage type")
    else:
        print("\n❌ Google Sheets connection is not working")
        print("\n📋 Follow the setup guide: GOOGLE_SHEETS_SETUP_GUIDE.md")

if __name__ == "__main__":
    main()
