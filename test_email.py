#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test email notification functionality"""

import os
import smtplib
import sys
from email.message import EmailMessage
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

# Load email configuration
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")
EMAIL_FROM = os.getenv("EMAIL_FROM", SMTP_USER)

def test_email():
    """Test email notification"""
    print("🧪 Testing Email Configuration...")
    
    # Check if all required settings are present
    required_settings = [SMTP_HOST, SMTP_USER, SMTP_PASS, EMAIL_TO]
    if not all(required_settings):
        print("❌ Missing email configuration:")
        print(f"   SMTP_HOST: {'✅' if SMTP_HOST else '❌'}")
        print(f"   SMTP_USER: {'✅' if SMTP_USER else '❌'}")
        print(f"   SMTP_PASS: {'✅' if SMTP_PASS else '❌'}")
        print(f"   EMAIL_TO: {'✅' if EMAIL_TO else '❌'}")
        return False
    
    print("✅ All email settings are configured")
    print(f"📧 From: {EMAIL_FROM}")
    print(f"📧 To: {EMAIL_TO}")
    print(f"🌐 SMTP Server: {SMTP_HOST}:{SMTP_PORT}")
    
    # Create test message
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
    message = f"🧪 This is a test message from Pokémon Center Monitor at {now}.\n\n" \
              f"If you receive this email, the notification system is working correctly!"
    
    msg = EmailMessage()
    msg["Subject"] = "[TEST] Pokemon Center Monitor - Email Test"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO.split(",")
    msg.set_content(message)
    
    try:
        print("📤 Sending test email...")
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
            print("✅ Test email sent successfully!")
            return True
    except Exception as exc:
        print(f"❌ Email test failed: {exc}")
        print("\n💡 Possible issues:")
        print("1. Check your Gmail app password (not regular password)")
        print("2. Make sure 2-factor authentication is enabled")
        print("3. Verify email addresses are correct")
        return False

if __name__ == "__main__":
    success = test_email()
    sys.exit(0 if success else 1) 
