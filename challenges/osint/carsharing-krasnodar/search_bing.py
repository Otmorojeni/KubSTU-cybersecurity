import urllib.request
import urllib.parse
import json
import re

# Let's search Yahoo or Bing or Google
def search_bing(query):
    url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8'
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Extract links
            matches = re.findall(r'<li class="b_algo">.*?<h2><a href="([^"]+)".*?>(.*?)</a></h2>.*?<div class="b_caption"><p>(.*?)</p>', html, re.DOTALL)
            print(f"Bing results for '{query}': {len(matches)}")
            for u, title, snippet in matches[:5]:
                print("Title:", re.sub(r'<[^>]+>', '', title))
                print("URL:", u)
                print("Snippet:", re.sub(r'<[^>]+>', '', snippet))
                print("-" * 40)
    except Exception as e:
        print("Bing error:", e)

if __name__ == '__main__':
    search_bing('steganography "8x8" "frequency"')
    search_bing('"stego_hint" "key-bro"')
    search_bing('"Look into 8x8 frequency blocks"')
    search_bing('kubstu ctf stego')
