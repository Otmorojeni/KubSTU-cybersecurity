import numpy as np
from PIL import Image
from scipy.fftpack import dct

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)

def get_dct(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

H, W, _ = arr.shape
n_by, n_bx = H // 8, W // 8

# Let's inspect the values of (4, 3) and (3, 4) and (5, 2)
# Across all blocks!
freqs_to_check = [(4, 3), (3, 4), (5, 2), (2, 5), (1, 7), (2, 7), (3, 7)]

dct_all = np.zeros((n_by, n_bx, 8, 8))
for by in range(n_by):
    for bx in range(n_bx):
        dct_all[by, bx] = get_dct(arr[by*8:(by+1)*8, bx*8:(bx+1)*8, 0])

for u, v in freqs_to_check:
    vals = dct_all[:, :, u, v].flatten()
    print(f"\nFreq ({u},{v}):")
    # Non-zero values or large values
    large_vals = vals[np.abs(vals) > 5]
    print(f"Total |val| > 5: {len(large_vals)} / {len(vals)}")
    print(f"Large vals percentiles: 5%={np.percentile(large_vals, 5):.2f}, 50%={np.percentile(large_vals, 50):.2f}, 95%={np.percentile(large_vals, 95):.2f}")
    # Are values clustered around specific constants? E.g. +12, -12, etc.?
    hist, edges = np.histogram(large_vals, bins=20)
    for h, e1, e2 in zip(hist, edges[:-1], edges[1:]):
        if h > 50:
            print(f"  [{e1:6.1f}, {e2:6.1f}]: count={h}")
