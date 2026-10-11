import urllib.request
import urllib.parse
import re

# Let's search Bing for github repositories with spread spectrum steganography
def search_repos(q):
    url = f"https://www.bing.com/search?q={urllib.parse.quote(q)}"
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Extract github.com URLs
            gh_links = set(re.findall(r'https?://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', html))
            print(f"Query '{q}': found {len(gh_links)} repos")
            for link in list(gh_links)[:10]:
                print(" ", link)
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    search_repos('site:github.com "dct" "steganography" "key"')
    search_repos('site:github.com "dct" "watermark" "8x8"')
    search_repos('site:github.com "stego_hint"')
    search_repos('site:github.com "key-bro"')
