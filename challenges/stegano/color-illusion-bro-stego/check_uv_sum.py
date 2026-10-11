import numpy as np
from PIL import Image
from scipy.fftpack import dct
import random

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)

def get_dct(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

# Find the spike position for first 20 blocks in row 0
row0_spikes = []
for bx in range(20):
    b = arr[0:8, bx*8:(bx+1)*8, 0]
    d = get_dct(b)
    d_clean = d.copy()
    d_clean[0:2, 0:2] = 0
    u, v = np.unravel_index(np.argmax(np.abs(d_clean)), d_clean.shape)
    row0_spikes.append(((u, v), u + v, d[u, v]))

print("Row 0 spikes (u, v), u+v, val:")
for bx, ((u, v), uv_sum, val) in enumerate(row0_spikes):
    print(f"bx={bx:2d}: ({u}, {v}) sum={uv_sum:2d} val={val:6.2f}")
