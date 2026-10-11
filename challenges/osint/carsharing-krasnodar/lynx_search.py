import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re

def google_text_search(query):
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'Lynx/2.8.9rel.1 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/1.0.2k'
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.get_text()
            # Clean up whitespace
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            print(f"=== Query: {query} ===")
            for line in lines[:30]:
                print(" ", line)
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    google_text_search('"На заводе стих шум"')
    google_text_search('"Look into 8x8 frequency blocks"')
    google_text_search('"key-bro"')
