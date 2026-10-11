import requests, json

headers = {'User-Agent': 'Mozilla/5.0'}

# Test on Krasnoarmeyskaya
lat, lon = 45.02508, 38.97279
url = f'https://api-maps.yandex.ru/services/panoramas/1.x/?l=stv&lang=ru_RU&ll={lon}%2C{lat}&origin=userAction&provider=streetview'
r = requests.get(url, headers=headers).json()
d = r['data']['Data']
img_id = d['Images']['imageId']
origin_yaw = d['EquirectangularProjection']['Origin'][0]

print('imageId:', img_id)
print('origin_yaw:', origin_yaw)

# East is azimuth ~105 degrees.
# Heading relative to origin: (105 - origin_yaw) % 360
rel_yaw = (105 - origin_yaw) % 360
# In equirectangular image, x in [0, 1] is rel_yaw / 360
# At zoom 2, there are 7 columns: x_tile = int((rel_yaw / 360) * 7)
x_tile = int((rel_yaw / 360) * 7)
print('Relative yaw:', rel_yaw, 'x_tile:', x_tile)

# Row y=1 (around horizon/eye level, looking slightly down/level)
tile_url = f'https://pano.maps.yandex.net/{img_id}/2.{x_tile}.1'
r_tile = requests.get(tile_url, headers=headers)
print('Tile status:', r_tile.status_code)
with open('test_east_tile.jpg', 'wb') as f:
    f.write(r_tile.content)
print('Saved test_east_tile.jpg')
