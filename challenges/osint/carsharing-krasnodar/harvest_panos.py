import requests, json, time, sys
sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0'}

# Grid of points across central Krasnodar:
# Lats: from 45.015 to 45.045 with step 0.005 (7 steps)
# Lons: from 38.960 to 38.995 with step 0.005 (8 steps)
lats = [45.015 + i * 0.005 for i in range(7)]
lons = [38.960 + i * 0.005 for i in range(8)]

panos = {}

for lat in lats:
    for lon in lons:
        url = f'https://api-maps.yandex.ru/services/panoramas/1.x/?l=stv&lang=ru_RU&ll={lon:.5f}%2C{lat:.5f}&origin=userAction&provider=streetview'
        try:
            r = requests.get(url, headers=headers, timeout=5)
            if r.status_code == 200:
                d = r.json()
                if 'data' in d and 'Annotation' in d['data'] and 'Graph' in d['data']['Annotation']:
                    nodes = d['data']['Annotation']['Graph'].get('Nodes', [])
                    for n in nodes:
                        pid = n.get('panoid')
                        if pid and pid not in panos:
                            panos[pid] = {
                                'lat': n.get('lat'),
                                'lon': n.get('lon'),
                                'href': n.get('href')
                            }
            time.sleep(0.05)
        except Exception as e:
            pass

print(f"Total unique panoramas found: {len(panos)}")
with open('krasnodar_panos.json', 'w', encoding='utf-8') as f:
    json.dump(panos, f, indent=2)
