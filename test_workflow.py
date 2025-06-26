#!/usr/bin/env python3
"""Simple test script for GitHub Actions - no email required"""

import os
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("PCO_URL", "https://www.pokemoncenter-online.com")
TIMEOUT = int(os.getenv("TIMEOUT") or "10")

def check_site():
    """Check if site is up or in maintenance"""
    try:
        resp = requests.get(URL, timeout=TIMEOUT, allow_redirects=True)
        
        # Check if redirected to maintenance page
        if 'maintenance' in resp.url.lower():
            print(f"🔧 Site is in maintenance: {resp.url}")
            return False
            
        if resp.status_code == 200:
            print(f"✅ Site is UP: {URL}")
            return True
        else:
            print(f"❌ Site returned HTTP {resp.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking site: {e}")
        return False

def main():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
    print(f"🕐 Checking at {now}")
    
    # Check email configuration
    email_configured = all([
        os.getenv("SMTP_HOST"),
        os.getenv("SMTP_USER"), 
        os.getenv("SMTP_PASS"),
        os.getenv("EMAIL_TO")
    ])
    
    print(f"📧 Email notification: {'✅ Configured' if email_configured else '❌ Not configured'}")
    
    # Check site status
    is_up = check_site()
    
    if is_up:
        print("🎉 Pokemon Center Online is available!")
        if email_configured:
            print("📧 Would send notification email (if status changed)")
    else:
        print("⏳ Pokemon Center Online is still in maintenance")

if __name__ == "__main__":
    main() 
