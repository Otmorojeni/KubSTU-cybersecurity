import numpy as np
from PIL import Image
from scipy.fftpack import dct

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)

def get_dct(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

H, W, _ = arr.shape
n_by, n_bx = H // 8, W // 8

# Let's check for each block:
# Zero out (0,0), (0,1), (1,0), (1,1)
# What is the max absolute value in the remaining frequencies?
max_vals = []
for by in range(n_by):
    for bx in range(n_bx):
        d = get_dct(arr[by*8:(by+1)*8, bx*8:(bx+1)*8, 0])
        d[0, 0] = 0
        d[0, 1] = 0
        d[1, 0] = 0
        d[1, 1] = 0
        max_vals.append(np.max(np.abs(d)))

max_vals = np.array(max_vals)
print(f"Total blocks: {len(max_vals)}")
print(f"Blocks with max > 10: {np.sum(max_vals > 10)}")
print(f"Blocks with max > 8:  {np.sum(max_vals > 8)}")
print(f"Blocks with max > 12: {np.sum(max_vals > 12)}")
print(f"Blocks with max < 5:  {np.sum(max_vals < 5)}")
print(f"Min of max_vals: {np.min(max_vals):.2f}, Median: {np.median(max_vals):.2f}, 10%: {np.percentile(max_vals, 10):.2f}")
