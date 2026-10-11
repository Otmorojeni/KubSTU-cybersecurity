import urllib.request
import urllib.parse
import json

# Let's search using Qwant or Brave or Yandex or Mojeek or Startpage
def search_mojeek(q):
    url = f"https://www.mojeek.com/search?q={urllib.parse.quote(q)}"
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            import re
            titles = re.findall(r'<a class="title"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html)
            snippets = re.findall(r'<p class="s">(.*?)</p>', html)
            print(f"Mojeek results for '{q}': {len(titles)}")
            for (u, t), s in zip(titles[:5], snippets[:5]):
                print("Title:", re.sub(r'<[^>]+>', '', t))
                print("URL:", u)
                print("Snippet:", re.sub(r'<[^>]+>', '', s))
                print("-" * 30)
    except Exception as e:
        print("Mojeek error:", e)

if __name__ == '__main__':
    search_mojeek('steganography "8x8" frequency blocks')
    search_mojeek('"key-bro"')
    search_mojeek('CTF "Look into 8x8 frequency blocks"')
    search_mojeek('python dct stego key')
