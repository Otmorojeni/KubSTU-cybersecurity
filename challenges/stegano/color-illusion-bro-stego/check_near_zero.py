import numpy as np
from PIL import Image
from scipy.fftpack import dct

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)

def get_dct(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

H, W, _ = arr.shape
n_by, n_bx = H // 8, W // 8

# Check across the entire image:
# How many coefficients are < 0.01? < 0.1? < 0.5?
small_counts = []
for by in range(n_by):
    for bx in range(n_bx):
        d = get_dct(arr[by*8:(by+1)*8, bx*8:(bx+1)*8, 0])
        # exclude (0, 0)
        d[0, 0] = 0
        small_counts.append(np.sum(np.abs(d) < 0.5))

print("Average number of near-zero coefficients (< 0.5) per block:", np.mean(small_counts))
print("Max near-zero coefficients in any block:", np.max(small_counts))
print("Min near-zero coefficients in any block:", np.min(small_counts))
