import urllib.request, urllib.parse, re

def search(q):
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req) as r:
            html = r.read().decode('utf-8', errors='ignore')
            links = re.findall(r'<a class="result__url" href="([^"]+)"', html)
            snippets = re.findall(r'<a class="result__snippet[^"]*"[^>]*>(.*?)</a>', html)
            print(f"=== Search: {q} ===")
            for l, s in zip(links[:4], snippets[:4]):
                s_clean = re.sub(r'<[^<]+?>', '', s)
                print(f"URL: {l.strip()}\n  {s_clean.strip()}")
    except Exception as e:
        print("Error:", e)

search('site:habr.com стеганография dct python')
search('site:habr.com "dct" "стеганография"')
search('site:github.com "dct" "steganography" "key" python')
