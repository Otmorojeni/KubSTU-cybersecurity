import numpy as np
from PIL import Image
from scipy.fftpack import dct

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)

def get_dct(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

H, W, _ = arr.shape
n_by, n_bx = H // 8, W // 8

# Let's count across ALL 25600 blocks:
# For each (u, v), how many blocks have |d[u, v]| > 4?
# Also what is the standard deviation and average absolute value for each (u, v)?

# And let's check in the SKY region (where natural noise is definitely zero):
# Sky region: by in range(5, 35), bx in range(5, 55) (total 30 x 50 = 1500 blocks)
sky_active_counts = np.zeros((8, 8), dtype=int)
for by in range(5, 35):
    for bx in range(5, 55):
        d = get_dct(arr[by*8:(by+1)*8, bx*8:(bx+1)*8, 0])
        for u in range(8):
            for v in range(8):
                if abs(d[u, v]) > 4:
                    sky_active_counts[u, v] += 1

print("Sky active counts (|d| > 4 out of 1500 sky blocks):")
for u in range(8):
    print(f"u={u}: " + " ".join(f"{sky_active_counts[u, v]:4d}" for v in range(8)))
