import requests, re, sys
sys.stdout.reconfigure(encoding='utf-8')

r = requests.get('https://photobuildings.com/search.php?query=Краснодар', headers={'User-Agent': 'Mozilla/5.0'})
links = re.findall(r'href="([^"]+)"[^>]*>([^<]*Краснодар[^<]*)</a>', r.text)
for l, t in links:
    print(l, t)
