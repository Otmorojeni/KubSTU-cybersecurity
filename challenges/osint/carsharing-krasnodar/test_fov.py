import requests
from PIL import Image
import io

headers = {'User-Agent': 'Mozilla/5.0'}

# Test on tile BruxwyPDMKeO
img_id = 'BruxwyPDMKeO'
origin_yaw = 193.42

t0 = requests.get(f'https://pano.maps.yandex.net/{img_id}/3.0.0', headers=headers).content
t1 = requests.get(f'https://pano.maps.yandex.net/{img_id}/3.1.0', headers=headers).content

im0 = Image.open(io.BytesIO(t0))
im1 = Image.open(io.BytesIO(t1))

pano360 = Image.new('RGB', (512, 256))
pano360.paste(im0, (0, 0))
pano360.paste(im1, (256, 0))
pano360.save('pano360_test.jpg')

# Now let's extract 90 degrees facing East (azimuth 105)
# In pano360, x in [0, 512] corresponds to yaw [0, 360] relative to origin
rel_yaw = (105 - origin_yaw) % 360
center_x = int((rel_yaw / 360.0) * 512)

# 90 deg FOV has width 128 (64 on each side)
# Wrap around 512 if needed
fov = Image.new('RGB', (128, 256))
for i in range(128):
    src_x = (center_x - 64 + i) % 512
    # copy column
    col = pano360.crop((src_x, 0, src_x + 1, 256))
    fov.paste(col, (i, 0))

fov.save('fov_east_test.jpg')
print('Saved pano360_test.jpg and fov_east_test.jpg')
