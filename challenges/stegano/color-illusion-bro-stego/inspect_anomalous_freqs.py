import numpy as np
from PIL import Image
from scipy.fftpack import dct

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)
H, W, _ = arr.shape
n_by = H // 8
n_bx = W // 8

def get_dct(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

# Check channel 0 (R)
dct_cube = np.zeros((n_by, n_bx, 8, 8))
for by in range(n_by):
    for bx in range(n_bx):
        dct_cube[by, bx] = get_dct(arr[by*8:(by+1)*8, bx*8:(bx+1)*8, 0])

print("DCT cube shape:", dct_cube.shape)

# Let's inspect the distribution of values at each (u, v)
# Print min, max, mean, std, and number of non-zero or unique values
for u in range(8):
    for v in range(8):
        vals = dct_cube[:, :, u, v]
        # Check if any (u, v) has discrete values, or binary values, or bimodal distribution!
        hist, bin_edges = np.histogram(vals, bins=10)
        # Check standard deviation or anomalies
        if (u, v) in [(1,7), (2,7), (3,7), (4,7), (7,1), (7,2), (7,3), (7,4)]:
            print(f"({u},{v}): min={vals.min():.2f}, max={vals.max():.2f}, mean={vals.mean():.2f}, std={vals.std():.2f}")
            print(f"       quantiles: 10%={np.percentile(vals, 10):.2f}, 50%={np.percentile(vals, 50):.2f}, 90%={np.percentile(vals, 90):.2f}")
