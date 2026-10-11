import numpy as np
from PIL import Image
from scipy.fftpack import dct

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)

def get_dct(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

# Extract spike (u, v) and sign for first 100 blocks
spikes = []
for by in range(10):
    for bx in range(10):
        b = arr[by*8:(by+1)*8, bx*8:(bx+1)*8, 0]
        d = get_dct(b)
        d_clean = d.copy()
        d_clean[0:2, 0:2] = 0
        u, v = np.unravel_index(np.argmax(np.abs(d_clean)), d_clean.shape)
        val = d[u, v]
        spikes.append(((by, bx), (u, v), u*8+v, val))

print("First 40 blocks spikes:")
for coord, (u, v), idx, val in spikes[:40]:
    sign = "+" if val > 0 else "-"
    print(f"Block {coord}: ({u},{v}) [idx={idx:2d}] val={val:6.2f} ({sign})")
