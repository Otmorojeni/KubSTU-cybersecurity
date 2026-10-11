import requests
import re

base_url = "http://155.212.216.201:8080"
s = requests.Session()
s.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
})

# 1. Get register page
r = s.get(f"{base_url}/register")
print("Register page status:", r.status_code)
# Find inputs in register form
inputs = re.findall(r'<input\s+[^>]*>', r.text)
for inp in inputs:
    print("  inp:", inp)
action = re.findall(r'<form\s+[^>]*action=["\']([^"\']*)["\']', r.text)
print("Register form action:", action)
