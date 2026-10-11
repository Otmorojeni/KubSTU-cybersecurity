import urllib.request, urllib.parse, re, sys

q = sys.argv[1]
url = 'https://ya.ru/search/?text=' + urllib.parse.quote(q)
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        html = r.read().decode('utf-8', errors='ignore')
        print('Ya results len:', len(html))
        snippets = re.findall(r'<span[^>]*class="[^"]*OrganicText[^"]*"[^>]*>(.*?)</span>', html)
        print('Snippets found:', len(snippets))
        for s in snippets[:5]:
            print(re.sub(r'<[^>]+>', '', s))
except Exception as e:
    print('Error:', e)
