import numpy as np
from PIL import Image
from scipy.fftpack import dct

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)

# Check all 3 channels
# Let's inspect the 8x8 DCT of blocks
# Specifically, let's see which frequencies (u, v) have unusual values or non-zero high frequencies!
def get_dct(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

H, W, _ = arr.shape
n_blocks_y = H // 8
n_blocks_x = W // 8

for c, cname in enumerate(['R', 'G', 'B']):
    channel = arr[:, :, c]
    # compute full dct grid
    dct_cube = np.zeros((n_blocks_y, n_blocks_x, 8, 8))
    for by in range(n_blocks_y):
        for bx in range(n_blocks_x):
            dct_cube[by, bx] = get_dct(channel[by*8:(by+1)*8, bx*8:(bx+1)*8])
            
    print(f"\nChannel {cname}:")
    # For each frequency (u, v), print how many blocks have non-zero or specific values
    # Or average magnitude of (u, v)
    avg_mag = np.mean(np.abs(dct_cube), axis=(0, 1))
    print("Average magnitude 8x8 grid:")
    for u in range(8):
        row_str = " ".join(f"{avg_mag[u, v]:6.2f}" for v in range(8))
        print(f" u={u}: {row_str}")
