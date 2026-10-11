import urllib.request
import re

url = "http://159.194.250.157:8080/"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req, timeout=5) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
        print("Status:", resp.status)
        print("Headers:", dict(resp.headers))
        print("Title:", re.findall(r"<title>(.*?)</title>", html, re.I))
        
        # Save HTML to inspect
        with open("shop_index.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("Saved HTML, length:", len(html))
except Exception as e:
    print("Error:", e)
