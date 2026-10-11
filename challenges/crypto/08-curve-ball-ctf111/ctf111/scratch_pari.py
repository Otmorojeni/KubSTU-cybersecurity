import urllib.request, re

url = 'https://pari.math.u-bordeaux.fr/pub/pari/windows/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')
links = re.findall(r'href="([^"]+)"', html)
for l in links:
    if any(ext in l for ext in ['.exe', '.zip', '.7z']):
        print(l)
