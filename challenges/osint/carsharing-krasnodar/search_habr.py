import urllib.request
import urllib.parse
import re

# Search Habr via Habr search or Google
def search_habr():
    url = "https://habr.com/ru/search/?q=" + urllib.parse.quote("стеганография DCT 8x8")
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            articles = re.findall(r'<a[^>]+href="(/ru/articles/\d+/)"[^>]*>(.*?)</a>', html)
            print("Habr articles found:", len(articles))
            for link, title in articles[:10]:
                print(link, "->", re.sub(r'<[^>]+>', '', title).strip())
    except Exception as e:
        print("Habr search error:", e)

if __name__ == '__main__':
    search_habr()
