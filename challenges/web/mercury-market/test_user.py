import requests
import re

base_url = "http://155.212.216.201:8080"
s = requests.Session()
s.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Origin": base_url,
    "Referer": f"{base_url}/register"
})

# Register
username = "player_test42"
password = "SuperPassword123!"

r = s.post(f"{base_url}/register", data={"username": username, "password": password})
print("Register post status:", r.status_code, "url:", r.url)
print("Cookies:", s.cookies.get_dict())

# Check /profile
r_prof = s.get(f"{base_url}/profile")
print("Profile status:", r_prof.status_code)
with open("profile.html", "w", encoding="utf-8") as f:
    f.write(r_prof.text)

# Check /balance
r_bal = s.get(f"{base_url}/balance")
print("Balance status:", r_bal.status_code)
with open("balance.html", "w", encoding="utf-8") as f:
    f.write(r_bal.text)

print("Profile length:", len(r_prof.text), "Balance length:", len(r_bal.text))
