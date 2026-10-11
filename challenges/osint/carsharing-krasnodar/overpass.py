import requests, json, sys
sys.stdout.reconfigure(encoding='utf-8')

query = """
[out:json][timeout:30];
(
  nwr["historic"](45.01, 38.955, 45.055, 39.005);
  nwr["heritage"](45.01, 38.955, 45.055, 39.005);
);
out center tags;
"""

r = requests.post('https://overpass-api.de/api/interpreter', data=query.encode('utf-8'), headers={'User-Agent': 'Mozilla/5.0'})
print('Status:', r.status_code)
if r.status_code == 200:
    data = r.json()
    elements = data.get('elements', [])
    print('Found elements:', len(elements))
    with open('historic_buildings.json', 'w', encoding='utf-8') as f:
        json.dump(elements, f, ensure_ascii=False, indent=2)
    print('Saved to historic_buildings.json')
