import json

with open('krasnodar_panos.json', 'r', encoding='utf-8') as f:
    panos = json.load(f)

# Street offsets:
# Кирова: ~24.826
# Октябрьская: ~24.828
# Рашпилевская: ~24.831
# Седина: ~24.839
# Янковского: ~24.842
# Леваневского: ~24.844

target_streets = {
    'Кирова': 24.826,
    'Октябрьская': 24.828,
    'Рашпилевская': 24.831,
    'Седина': 24.839,
    'Янковского': 24.842,
    'Леваневского': 24.844,
}

for name, target_offset in target_streets.items():
    matches = []
    for pid, p in panos.items():
        lat = p['lat']
        lon = p['lon']
        offset = lon - 0.314 * lat
        if abs(offset - target_offset) < 0.001 and 45.020 <= lat <= 45.038:
            matches.append((lat, lon, pid))
    matches.sort()
    print(f"=== {name} ({len(matches)} panos) ===")
    if matches:
        # Pick 3 points (south, mid, north)
        for idx in [0, len(matches)//2, len(matches)-1]:
            lat, lon, pid = matches[idx]
            print(f"  lat: {lat:.5f}, lon: {lon:.5f}")
