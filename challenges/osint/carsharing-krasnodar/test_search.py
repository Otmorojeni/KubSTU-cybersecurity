import urllib.request
import urllib.parse
import json
import re

def search_duckduckgo_lite(query):
    url = "https://lite.duckduckgo.com/lite/"
    data = urllib.parse.urlencode({'q': query}).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            # Extract links and snippets from lite results
            # Results are in td.result-snippet or links with class result-link
            links = re.findall(r'<a[^>]+href="([^"]+)"[^>]*class="result-link"', content)
            snippets = re.findall(r'<td class="result-snippet">\s*(.*?)\s*</td>', content, re.DOTALL)
            print(f"Results for '{query}': {len(links)} links")
            for l, s in zip(links[:5], snippets[:5]):
                clean_s = re.sub(r'<[^>]+>', '', s).strip()
                print(" Link:", l)
                print(" Snippet:", clean_s)
                print("-" * 30)
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    search_duckduckgo_lite('python dct steganography "8x8"')
    search_duckduckgo_lite('github python dct steganography')
    search_duckduckgo_lite('"key-bro"')
