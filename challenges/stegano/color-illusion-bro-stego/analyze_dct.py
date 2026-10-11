import numpy as np
from PIL import Image
from scipy.fftpack import dct, idct

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)

H, W, C = arr.shape
print(f"Dimensions: {H}x{W}, Channels: {C}")

# Let's inspect 8x8 blocks
# Number of blocks: (H // 8) x (W // 8) = 160 x 160 = 25600
def get_dct_2d(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

# Let's test on channel 0 (R), channel 1 (G), channel 2 (B)
# Also Y channel (YCbCr)
img_ycbcr = img.convert('YCbCr')
arr_ycbcr = np.array(img_ycbcr, dtype=np.float32)

# Check block DCT values
dct_blocks_r = np.zeros((H // 8, W // 8, 8, 8))
dct_blocks_y = np.zeros((H // 8, W // 8, 8, 8))

for i in range(H // 8):
    for j in range(W // 8):
        block_r = arr[i*8:(i+1)*8, j*8:(j+1)*8, 0]
        dct_blocks_r[i, j] = get_dct_2d(block_r)
        
        block_y = arr_ycbcr[i*8:(i+1)*8, j*8:(j+1)*8, 0]
        dct_blocks_y[i, j] = get_dct_2d(block_y)

print("Computed DCT for all blocks.")

# Let's check statistics of each coefficient (u, v) across all blocks
# Look for coefficients that are integers, or have specific parity, or unusual distributions
for u in range(8):
    for v in range(8):
        vals_r = dct_blocks_r[:, :, u, v].flatten()
        vals_y = dct_blocks_y[:, :, u, v].flatten()
        
        # Check if values are close to integers
        diff_int_r = np.abs(vals_r - np.round(vals_r)).max()
        diff_int_y = np.abs(vals_y - np.round(vals_y)).max()
        
        # Check fraction of exact zeros or parity
        # Also check variance, min, max
        if u < 4 and v < 4:
            print(f"({u},{v}): R mean={vals_r.mean():.2f}, std={vals_r.std():.2f} | Y mean={vals_y.mean():.2f}, std={vals_y.std():.2f}")
