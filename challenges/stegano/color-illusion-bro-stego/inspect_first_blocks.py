import numpy as np
from PIL import Image
from scipy.fftpack import dct

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)

def get_dct(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

H, W, _ = arr.shape

# Let's inspect the first 20 blocks in row 0
print("--- Row 0 blocks (0, 0) to (0, 15) ---")
for bx in range(16):
    b = arr[0:8, bx*8:(bx+1)*8, 0]
    d = get_dct(b)
    # Print max AC coefficient, and any unusual values
    ac = d.copy()
    ac[0, 0] = 0
    max_idx = np.unravel_index(np.argmax(np.abs(ac)), ac.shape)
    print(f"Block (0, {bx:2d}): max AC at {max_idx} = {ac[max_idx]:.2f}, sum(|AC|)={np.sum(np.abs(ac)):.1f}")
