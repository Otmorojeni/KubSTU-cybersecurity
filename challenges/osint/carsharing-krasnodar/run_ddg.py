import urllib.request, urllib.parse, re

q = 'На заводе стих шум'
url = f'https://html.duckduckgo.com/html/?q={urllib.parse.quote(q)}'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req) as r:
        html = r.read().decode('utf-8', errors='ignore')
    snippets = re.findall(r'class="result__snippet[^"]*">(.*?)</a>', html)
    print(f'Found {len(snippets)} snippets:')
    for s in snippets[:10]:
        s_clean = re.sub('<[^<]+?>', '', s)
        print('-', s_clean)
except Exception as e:
    print('Error:', e)
