import requests
import re

base_url = "http://155.212.216.201:8080"
s = requests.Session()
s.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
})

# Login
s.post(f"{base_url}/login", data={"username": "player_test42", "password": "SuperPassword123!"})

# Get checkout page to get meta mk-c
r_co = s.get(f"{base_url}/checkout/13537")
cid_match = re.search(r'meta name=["\']mk-c["\'] content=["\']([^"\']+)["\']', r_co.text)
if cid_match:
    cid = cid_match.group(1)
    print("Found cid:", cid)
    
    # Get bootstrap
    r_boot = s.get(f"{base_url}/api/bootstrap?c={cid}")
    print("Bootstrap status:", r_boot.status_code)
    print("Bootstrap json:", r_boot.text)
else:
    print("No cid found in checkout page!")
