import requests
import re
import sys
sys.stdout.reconfigure(encoding="utf-8")

base_url = "http://155.212.216.201:8080"
s = requests.Session()
s.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
})

# Login / register user
r = s.post(f"{base_url}/login", data={"username": "player_test42", "password": "SuperPassword123!"})
print("Login status:", r.status_code)

# Check /g/mercury-market
r_vip = s.get(f"{base_url}/g/mercury-market")
print("VIP status:", r_vip.status_code)

# Extract lots
lots = re.findall(r'<a\s+[^>]*href=["\'](/lot/\d+)["\'][^>]*>([\s\S]*?)</a>', r_vip.text)
print(f"VIP lots found: {len(lots)}")
for href, content in lots:
    clean = " ".join(content.split())
    print(f"  {href}: {clean[:150]}")

# If no lots found with that pattern, search all links to /lot/
all_lot_links = re.findall(r'href=["\'](/lot/\d+)["\']', r_vip.text)
print("All lot links:", set(all_lot_links))
