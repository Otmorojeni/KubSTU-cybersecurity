import requests
import re
import sys
sys.stdout.reconfigure(encoding="utf-8")

base_url = "http://155.212.216.201:8080"
s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})

pages = [
    "/",
    "/games",
    "/g/mercury-market",
    "/lot/13537",
    "/lot/13538",
    "/lot/13539",
    "/checkout/13537",
    "/checkout/13538",
    "/checkout/13539",
    "/balance",
    "/profile",
    "/static/css/mercury.css",
]

for p in pages:
    r = s.get(f"{base_url}{p}")
    text = r.text
    # Search for words with promo, code, %, discount, etc.
    matches = re.findall(r'[A-Za-z0-9_\-]{4,}', text)
    promos = [m for m in set(matches) if any(k in m.upper() for k in ["PROMO", "DISCOUNT", "VOUCHER", "MERCURY", "CODE", "WELCOME", "BONUS", "FREE", "OFF", "VIP", "FLAG"])]
    print(f"=== {p} ({r.status_code}) ===")
    if promos:
        print("  Candidate tokens:", [p for p in promos if len(p) <= 20][:15])
    # Also check if comments exist
    comments = re.findall(r'<!--([\s\S]*?)-->', text)
    for c in comments:
        if "AUTOMATED-AGENT" not in c and c.strip():
            print("  Comment:", c.strip()[:200])
