import numpy as np
from PIL import Image
from scipy.fftpack import dct

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)

def get_dct(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

H, W, _ = arr.shape
n_by, n_bx = H // 8, W // 8

# Let's inspect 10 consecutive sky blocks: (10, 10), (10, 11), ..., (10, 19)
# In each block, which (u, v) have |val| > 8?
for bx in range(10, 20):
    b = arr[10*8:11*8, bx*8:(bx+1)*8, 0]
    d = get_dct(b)
    # Find all (u, v) with |d[u, v]| > 5 (excluding DC (0, 0))
    large_coeffs = []
    for u in range(8):
        for v in range(8):
            if (u, v) != (0, 0) and abs(d[u, v]) > 5:
                large_coeffs.append(((u, v), round(d[u, v], 1)))
    print(f"Block (10, {bx}): {len(large_coeffs)} large coeffs -> {large_coeffs}")
