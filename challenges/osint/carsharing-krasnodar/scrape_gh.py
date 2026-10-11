import urllib.request
import urllib.parse
import re

def search_gh(query, qtype="code"):
    url = f"https://github.com/search?q={urllib.parse.quote(query)}&type={qtype}"
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Extract repository and file paths or items
            # GitHub search results have JSON or HTML links
            # Look for href="/.../blob/..."
            blobs = set(re.findall(r'href="(/[^\s"\'<>]+/blob/[^\s"\'<>]+)"', html))
            repos = set(re.findall(r'href="(/[^/\s"\'<>]+/[^/\s"\'<>]+)"', html))
            # Also search for code snippets
            text_matches = re.findall(rf'.{{0,50}}{re.escape(query)}.{{0,50}}', html, re.IGNORECASE)
            print(f"=== Query: {query} (type={qtype}) ===")
            print(f"Found {len(blobs)} blob links, {len(text_matches)} text matches")
            for b in list(blobs)[:5]:
                print("  Blob:", b)
            for m in text_matches[:3]:
                print("  Text:", m)
    except Exception as e:
        print(f"Error for {query}:", e)

if __name__ == '__main__':
    search_gh('"key-bro"')
    search_gh('"stego_hint"')
    search_gh('"Look into 8x8 frequency blocks"')
    search_gh('bro_stego')
    search_gh('"Look into 8x8"')
