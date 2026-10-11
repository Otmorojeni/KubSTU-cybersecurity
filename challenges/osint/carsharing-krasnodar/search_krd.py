import requests, re, sys
sys.stdout.reconfigure(encoding='utf-8')

r = requests.get('https://krd.ru/poisk/?q=обследование+аварийных+деревьев', headers={'User-Agent': 'Mozilla/5.0'}, verify=False)
print('Status:', r.status_code)
links = re.findall(r'href="(/novosti/[^"]+)"', r.text)
for l in set(links)[:10]:
    print('Link:', l)
