import requests
import re
import hashlib
import json
import time

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

# 2. Get checkout
r_co = s.get(f"{base_url}/checkout/13537")
cid = re.search(r'meta name=["\']mk-c["\'] content=["\']([^"\']+)["\']', r_co.text).group(1)
print("cid:", cid)

# 3. Bootstrap
r_boot = s.get(f"{base_url}/api/bootstrap?c={cid}").json()
print("Boot:", r_boot)

# 4. Calculate a
# Extract the math from p
# e.g.: var _jhrz=21620;_jhrz=(_jhrz^61115)&65535;...return _jhrz;
code = r_boot["p"]
# Run code in Python or Node
import subprocess
node_cmd = f"node -e \"{code}\""
try:
    a_val = int(subprocess.check_output(node_cmd, shell=True).strip())
except Exception as e:
    # If node fails, calculate via regex
    lines = code.split(";")
    val = 0
    for l in lines:
        if "=" in l and ("+" in l or "^" in l or "*" in l or "|" in l):
            pass
    print("Node error:", e)
    a_val = 0

print("Computed a:", a_val)

# 5. PoW
seed = r_boot["s"]
diff = r_boot["d"]
prefix = "0" * diff
n = 0
while True:
    h = hashlib.sha256(f"{seed}:{n}".encode()).hexdigest()
    if h.startswith(prefix):
        break
    n += 1

print(f"Solved PoW: n={n}, hash={h[:10]}")

# 6. Signals
sig = {
    "wd": False,
    "aut": [],
    "ua": ua,
    "lang": 2,
    "plug": 5,
    "chr": True,
    "uad": True,
    "ow": 1920, "oh": 1080,
    "iw": 1920, "ih": 950,
    "sw": 1920, "sh": 1080, "dpr": 1,
    "hc": 8, "dm": 8,
    "tz": "Europe/Moscow",
    "gl": "Google Inc. (NVIDIA) / ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0 ps_5_0)",
    "jit": 0.123456,
    "ev": 15,
    "t": 1250
}

# 7. Handshake
hs_data = {
    "s": seed,
    "g": r_boot["g"],
    "n": str(n),
    "c": cid,
    "a": a_val,
    "f": sig
}

r_hs = s.post(f"{base_url}/api/hs", json=hs_data).json()
print("Handshake resp:", r_hs)

if r_hs.get("ok"):
    k = r_hs["k"]
    # 8. Mount widget
    r_w = s.get(f"{base_url}/api/w/co?e=15&t=1300").json()
    print("Widget resp ok:", r_w.get("ok"))
    
    # Unpack widget
    import base64
    kh = hashlib.sha256(k.encode()).digest()
    b64_data = base64.b64decode(r_w["b"])
    unpacked = bytes([b ^ kh[i % 32] for i, b in enumerate(b64_data)]).decode("utf-8")
    print("=== UNPACKED WIDGET ===")
    print(unpacked[:1000])
    with open("widget_co.html", "w", encoding="utf-8") as f:
        f.write(unpacked)
