import requests
import re
import hashlib
import json
import subprocess
import sys
sys.stdout.reconfigure(encoding="utf-8")

base_url = "http://155.212.216.201:8080"
s = requests.Session()
ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
s.headers.update({
    "User-Agent": ua,
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
})

# 1. Login
s.post(f"{base_url}/login", data={"username": "player_test42", "password": "SuperPassword123!"})

lot_id = 13099
r_co = s.get(f"{base_url}/checkout/{lot_id}")
print(f"Checkout {lot_id} status:", r_co.status_code)

cid = re.search(r'meta name=["\']mk-c["\'] content=["\']([^"\']+)["\']', r_co.text).group(1)
html_tag = re.search(r'<html\s+([^>]+)>', r_co.text).group(1)
html_attrs = dict(re.findall(r'([\w\-]+)=["\']([^"\']*)["\']', html_tag))
body_tag = re.search(r'<body\s+([^>]+)>', r_co.text).group(1)
body_attrs = dict(re.findall(r'([\w\-]+)=["\']([^"\']*)["\']', body_tag))
style_match = re.search(r'<style[^>]*>([\s\S]*?)</style>', r_co.text)
css_vars = dict(re.findall(r'(--[\w\-]+)\s*:\s*([^;]+);', style_match.group(1))) if style_match else {}
all_attrs = dict(re.findall(r'([\w\-]+)=["\']([^"\']*)["\']', r_co.text))

r_boot = s.get(f"{base_url}/api/bootstrap?c={cid}").json()
p_code = r_boot["p"]
js_eval = f"""
const html_attrs = {json.dumps(html_attrs)};
const body_attrs = {json.dumps(body_attrs)};
const css_vars = {json.dumps(css_vars)};
const all_attrs = {json.dumps(all_attrs)};
const document = {{
  documentElement: {{ getAttribute: (attr) => html_attrs[attr] || 0 }},
  body: {{ getAttribute: (attr) => body_attrs[attr] || 0 }},
  querySelector: (sel) => {{
    const m = sel.match(/\\[([\\w\\-]+)\\]/);
    if (m) {{
      const attr = m[1];
      if (all_attrs[attr] !== undefined) return {{ getAttribute: () => all_attrs[attr] }};
    }}
    return null;
  }}
}};
const getComputedStyle = () => ({{ getPropertyValue: (prop) => css_vars[prop] || '' }});
const fn = new Function({json.dumps(p_code)});
console.log(fn());
"""
a_val = int(subprocess.check_output(["node", "-e", js_eval]).decode().strip())
seed = r_boot["s"]
diff = r_boot["d"]
n = 0
prefix = "0" * diff
while True:
    h = hashlib.sha256(f"{seed}:{n}".encode()).hexdigest()
    if h.startswith(prefix):
        break
    n += 1

sig = {
    "wd": False, "aut": [], "ua": ua, "lang": 2, "plug": 5, "chr": True, "uad": True,
    "ow": 1920, "oh": 1080, "iw": 1920, "ih": 950, "sw": 1920, "sh": 1080, "dpr": 1,
    "hc": 8, "dm": 8, "tz": "Europe/Moscow",
    "gl": "Google Inc. (NVIDIA) / ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0 ps_5_0)",
    "jit": 0.123456, "ev": 15, "t": 1250
}
hs_data = { "s": seed, "g": r_boot["g"], "n": str(n), "c": cid, "a": a_val, "f": sig }
r_hs = s.post(f"{base_url}/api/hs", json=hs_data).json()
print("Handshake ok:", r_hs.get("ok"))

s.get(f"{base_url}/api/w/co?e=15&t=1300")

s.headers.update({"X-Requested-With": "mk"})
r_pay = s.post(f"{base_url}/api/v2/checkout/pay", json={"lot": lot_id}).json()
print("Pay response:", r_pay)

if r_pay.get("ok"):
    url = r_pay["url"]
    print("Redirect URL:", url)
    r_order = s.get(f"{base_url}{url}")
    print(f"Order page status {r_order.status_code}, len {len(r_order.text)}")
    with open("order.html", "w", encoding="utf-8") as f:
        f.write(r_order.text)
