import urllib.request

base_url = "http://159.194.250.157:8080"

for path in ["/internal/admin-backup", "/g/mercury-market", "/lot/13537", "/robots.txt"]:
    url = base_url + path
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            content = resp.read()
            print(f"=== {path}: {resp.status}, length={len(content)} ===")
            try:
                text = content.decode("utf-8")
                print(text[:500])
            except:
                print(f"Binary data: {content[:100]}")
    except Exception as e:
        print(f"=== {path}: error {e} ===")
