import requests
import re
import sys
sys.stdout.reconfigure(encoding="utf-8")

base_url = "http://155.212.216.201:8080"
s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})

# Fetch games list
r_games = s.get(f"{base_url}/games")
game_links = re.findall(r'href="(/g/[^"]+)"', r_games.text)
print("Games found:", len(game_links))

cheap_lots = []

for g in game_links[:10]:
    r = s.get(f"{base_url}{g}")
    # find rows: onclick="location='/lot/(\d+)'" and price
    rows = re.findall(r'onclick="location=\'(/lot/\d+)\'"[\s\S]*?<td class="price">([^<]+)</td>', r.text)
    for lot_url, price_str in rows:
        # parse price
        p = float(re.sub(r'[^\d.]', '', price_str.replace(',', '.')))
        if p <= 500:
            cheap_lots.append((lot_url, p))
            print(f"Found cheap lot: {lot_url} -> {p} ₽")

print(f"Total cheap lots <= 500: {len(cheap_lots)}")
