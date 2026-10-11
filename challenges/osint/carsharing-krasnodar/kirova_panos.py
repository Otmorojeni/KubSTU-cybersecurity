import json

with open('krasnodar_panos.json', 'r', encoding='utf-8') as f:
    panos = json.load(f)

kirova = []
for pid, p in panos.items():
    lat = p['lat']
    lon = p['lon']
    offset = lon - 0.314 * lat
    if 24.8255 <= offset <= 24.8275 and 45.015 <= lat <= 45.042:
        kirova.append((lat, lon, pid))

kirova.sort()
print(f"Total panoramas on Kirova: {len(kirova)}")
for lat, lon, pid in kirova:
    print(f"lat: {lat:.5f}, lon: {lon:.5f}, pid: {pid}")
