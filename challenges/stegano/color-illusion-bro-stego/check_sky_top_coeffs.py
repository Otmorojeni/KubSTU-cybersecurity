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

# In the smooth sky area, natural image AC is near 0
# Let's inspect the top 3 peak frequencies in each sky block!
sky_peaks = []
for by in range(5, 25):
    for bx in range(5, 25):
        d = get_dct(arr[by*8:(by+1)*8, bx*8:(bx+1)*8, 0])
        # Look at all (u, v) != (0, 0)
        d_no_dc = d.copy()
        d_no_dc[0, 0] = 0
        
        # Sort coefficients by absolute value
        flat_indices = np.argsort(np.abs(d_no_dc).flatten())[::-1]
        top_coeffs = []
        for idx in flat_indices[:5]:
            u, v = divmod(idx, 8)
            val = d_no_dc[u, v]
            if abs(val) > 7:
                top_coeffs.append(((u, v), val))
        sky_peaks.append(((by, bx), top_coeffs))

print("Sky blocks top coeffs (> 7):")
for coord, tc in sky_peaks[:20]:
    print(f"Block {coord}: {tc}")
