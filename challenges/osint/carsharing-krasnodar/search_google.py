import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re

def google_search(query):
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Extract search result items
            soup = BeautifulSoup(html, 'html.parser')
            print(f"=== Query: {query} ===")
            results = []
            for g in soup.find_all('div', class_='g'):
                a = g.find('a')
                h3 = g.find('h3')
                if a and h3:
                    title = h3.get_text()
                    link = a.get('href')
                    snippet_elem = g.find('div', class_=['VwiC3b', 'yXK7lf', 'MUxGbd'])
                    snippet = snippet_elem.get_text() if snippet_elem else ""
                    results.append((title, link, snippet))
            print(f"Found {len(results)} results")
            for t, l, s in results[:5]:
                print(f"Title: {t}\nURL: {l}\nSnippet: {s}\n---")
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    google_search('"Look into 8x8 frequency blocks"')
    google_search('"key-bro"')
    google_search('steganography "8x8" frequency blocks')
    google_search('"На заводе стих шум"')
