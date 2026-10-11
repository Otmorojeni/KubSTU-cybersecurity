import urllib.request
import urllib.parse
import re

def search(q):
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            titles = re.findall(r'<a class="result__url"[^>]*href="([^"]+)"', html)
            snippets = re.findall(r'<a class="result__snippet[^>]*>(.*?)</a>', html)
            for u, s in zip(titles[:5], snippets[:5]):
                print('URL:', u)
                print('Snippet:', re.sub(r'<[^>]+>', '', s))
                print('-'*40)
    except Exception as e:
        print('Error:', e)

if __name__ == '__main__':
    search('каршеринг Ситидрайв Краснодар зона')
