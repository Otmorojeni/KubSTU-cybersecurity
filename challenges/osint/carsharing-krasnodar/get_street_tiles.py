import requests, json, os, time, sys

headers = {'User-Agent': 'Mozilla/5.0'}

with open('krasnodar_panos.json', 'r', encoding='utf-8') as f:
    panos = json.load(f)

def download_street(street_name, target_offset, lat_min=45.015, lat_max=45.042):
    folder = f'tiles_{street_name}'
    os.makedirs(folder, exist_ok=True)
    
    matches = []
    for pid, p in panos.items():
        lat = p['lat']
        lon = p['lon']
        offset = lon - 0.314 * lat
        if abs(offset - target_offset) < 0.001 and lat_min <= lat <= lat_max:
            matches.append((lat, lon, pid))
    
    matches.sort()
    print(f"[{street_name}] Found {len(matches)} panos. Downloading...")
    
    for i, (lat, lon, pid) in enumerate(matches):
        fn = f'{folder}/{lat:.5f}_{lon:.5f}_{pid}.jpg'
        if os.path.exists(fn): continue
        try:
            url = f'https://api-maps.yandex.ru/services/panoramas/1.x/?l=stv&lang=ru_RU&ll={lon:.5f}%2C{lat:.5f}&origin=userAction&provider=streetview'
            r = requests.get(url, headers=headers, timeout=5)
            if r.status_code != 200: continue
            d = r.json().get('data', {}).get('Data', {})
            img_id = d.get('Images', {}).get('imageId')
            origin_yaw = d.get('EquirectangularProjection', {}).get('Origin', [0])[0]
            if not img_id: continue

            rel_yaw = (105 - origin_yaw) % 360
            x_tile = int((rel_yaw / 360) * 7)

            tile_url = f'https://pano.maps.yandex.net/{img_id}/2.{x_tile}.2'
            tr = requests.get(tile_url, headers=headers, timeout=5)
            if tr.status_code == 200:
                with open(fn, 'wb') as tf:
                    tf.write(tr.content)
            time.sleep(0.04)
        except Exception:
            pass
            
    print(f"[{street_name}] Done ({len(os.listdir(folder))} saved)")

if __name__ == '__main__':
    if len(sys.argv) > 2:
        name = sys.argv[1]
        offset = float(sys.argv[2])
        download_street(name, offset)
