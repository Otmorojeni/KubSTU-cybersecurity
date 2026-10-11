import requests, json, os, time

headers = {'User-Agent': 'Mozilla/5.0'}
os.makedirs('kirova_tiles', exist_ok=True)

with open('krasnodar_panos.json', 'r', encoding='utf-8') as f:
    panos = json.load(f)

kirova = []
for pid, p in panos.items():
    lat = p['lat']
    lon = p['lon']
    offset = lon - 0.314 * lat
    if 24.8255 <= offset <= 24.8275 and 45.020 <= lat <= 45.038:
        kirova.append((lat, lon, pid))

kirova.sort()
print(f"Checking {len(kirova)} points on Kirova...")

for i, (lat, lon, pid) in enumerate(kirova):
    try:
        url = f'https://api-maps.yandex.ru/services/panoramas/1.x/?l=stv&lang=ru_RU&ll={lon:.5f}%2C{lat:.5f}&origin=userAction&provider=streetview'
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code != 200: continue
        d = r.json().get('data', {}).get('Data', {})
        if not d: continue
        img_id = d.get('Images', {}).get('imageId')
        origin_yaw = d.get('EquirectangularProjection', {}).get('Origin', [0])[0]
        if not img_id: continue

        # East is azimuth 105 degrees:
        rel_yaw = (105 - origin_yaw) % 360
        x_tile = int((rel_yaw / 360) * 7)

        tile_url = f'https://pano.maps.yandex.net/{img_id}/2.{x_tile}.2'
        tr = requests.get(tile_url, headers=headers, timeout=5)
        if tr.status_code == 200:
            fn = f'kirova_tiles/{lat:.5f}_{lon:.5f}_{pid}.jpg'
            with open(fn, 'wb') as tf:
                tf.write(tr.content)
        time.sleep(0.05)
    except Exception as e:
        pass

print("Finished downloading Kirova tiles")
