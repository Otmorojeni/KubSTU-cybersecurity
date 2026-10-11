import json

with open('krasnodar_panos.json', 'r', encoding='utf-8') as f:
    panos = json.load(f)

krasnoarm = []
for pid, p in panos.items():
    lat = p['lat']
    lon = p['lon']
    offset = lon - 0.314 * lat
    if 24.8345 <= offset <= 24.8365 and 45.015 <= lat <= 45.042:
        krasnoarm.append((lat, lon, pid))

krasnoarm.sort()

# Group by 0.002 latitude (~1 block)
blocks = {}
for lat, lon, pid in krasnoarm:
    block_id = round(lat, 3)
    if block_id not in blocks:
        blocks[block_id] = (lat, lon, pid)

print("Krasnoarmeyskaya blocks:")
for b in sorted(blocks.keys()):
    lat, lon, pid = blocks[b]
    print(f"lat: {lat:.5f}, lon: {lon:.5f}")
