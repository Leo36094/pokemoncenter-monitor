#!/usr/bin/env python3
"""Monitor https://www.pokemoncenter-online.com and notify via LINE Notify or e‑mail

Usage:
  1. Create a virtualenv and install dependencies:
       pip install requests python-dotenv

  2. Copy .env.example to .env and fill in the credentials you need.
     (Only the channel you want is required.)

  3. Run once to make sure it works, then schedule it (cron, GitHub Actions, systemd‑timer, etc.).

The script keeps a tiny state file (pco_state.txt) next to itself so it only sends
notifications when the status changes from *DOWN* to *UP*.
"""
import os
import re
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

import requests
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Configuration (via environment variables)
# ---------------------------------------------------------------------------

load_dotenv()

URL = os.getenv("PCO_URL", "https://www.pokemoncenter-online.com")

# --- E‑mail (optional) -----------------------------------------------------
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")  # Comma‑separated list
EMAIL_FROM = os.getenv("EMAIL_FROM", SMTP_USER)

# ---------------------------------------------------------------------------
# Internal constants
# ---------------------------------------------------------------------------
STATE_FILE = Path(__file__).with_name("pco_state.txt")
MAINTENANCE_PATTERNS = [
    re.compile(r"maintenance", re.I),
    re.compile(r"メンテナンス"),
]
TIMEOUT = int(os.getenv("TIMEOUT", "10"))  # seconds for HTTP request

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def is_site_up() -> bool:
    """Return True if the shop page is reachable and not a maintenance stub."""
    try:
        resp = requests.get(URL, timeout=TIMEOUT, allow_redirects=True)
    except requests.RequestException as exc:
        print(f"[WARN] Request failed: {exc}")
        return False

    # Check if redirected to maintenance page (common pattern)
    if 'maintenance' in resp.url.lower():
        print(f"[INFO] Redirected to maintenance page: {resp.url} → DOWN")
        return False

    if resp.status_code != 200:
        print(f"[INFO] HTTP status {resp.status_code}")
        return False

    # Heuristic: if any known maintenance phrase is present, still DOWN.
    for pattern in MAINTENANCE_PATTERNS:
        if pattern.search(resp.text):
            print("[INFO] Maintenance phrase still present → DOWN")
            return False

    return True

def notify_email(message: str) -> None:
    if not (SMTP_HOST and SMTP_USER and SMTP_PASS and EMAIL_TO):
        return  # Not configured

    import smtplib
    from email.message import EmailMessage

    msg = EmailMessage()
    msg["Subject"] = "[PCO] Pokémon Center Online is back!"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO.split(",")
    msg.set_content(message)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
            print("[OK] E‑mail sent")
    except Exception as exc:
        print(f"[ERROR] E‑mail failed: {exc}")


# ---------------------------------------------------------------------------
# Main routine
# ---------------------------------------------------------------------------

def main():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
    up = is_site_up()
    prev_state = STATE_FILE.read_text().strip() if STATE_FILE.exists() else "DOWN"
    current_state = "UP" if up else "DOWN"

    if prev_state != current_state:
        STATE_FILE.write_text(current_state)
        if current_state == "UP":
            msg = f"✅ Pokémon Center Online ({URL}) seems to be back online as of {now}."
            notify_email(msg)
        else:
            print("[INFO] Site went DOWN (no notification sent)")
    else:
        print(f"[INFO] No change ({current_state}) at {now}")


if __name__ == "__main__":
    sys.exit(main())
