import numpy as np
from PIL import Image
from scipy.fftpack import dct
from collections import Counter

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)

def get_dct(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

H, W, _ = arr.shape
n_by, n_bx = H // 8, W // 8

# In sky blocks:
spike_coords = []
for by in range(5, 35):
    for bx in range(5, 55):
        d = get_dct(arr[by*8:(by+1)*8, bx*8:(bx+1)*8, 0])
        d_clean = d.copy()
        d_clean[0:2, 0:2] = 0
        u, v = np.unravel_index(np.argmax(np.abs(d_clean)), d_clean.shape)
        if abs(d[u, v]) > 8:
            spike_coords.append((u, v))

c = Counter(spike_coords)
print("Unique spike coordinates in sky:", len(c))
print("Most common spike coordinates:")
for coord, count in c.most_common(20):
    print(f"  {coord}: {count}")

print("Least common spike coordinates:")
for coord, count in c.most_common()[-10:]:
    print(f"  {coord}: {count}")
