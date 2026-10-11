import numpy as np
from PIL import Image
from scipy.fftpack import dct

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)

def get_dct(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

H, W, _ = arr.shape
n_by, n_bx = H // 8, W // 8

# Find 5 sky blocks with (1, 7) > 8, and 5 sky blocks with (1, 7) < -8, and 5 with near 0
sky_pos = []
sky_neg = []
sky_zero = []

for by in range(5, 40):
    for bx in range(5, 50):
        d = get_dct(arr[by*8:(by+1)*8, bx*8:(bx+1)*8, 0])
        val = d[1, 7]
        if val > 8 and len(sky_pos) < 3:
            sky_pos.append(((by, bx), d))
        elif val < -8 and len(sky_neg) < 3:
            sky_neg.append(((by, bx), d))
        elif abs(val) < 0.5 and len(sky_zero) < 3:
            sky_zero.append(((by, bx), d))

print("=== SKY ZERO BLOCKS (normal background) ===")
for coord, d in sky_zero:
    print(f"Block {coord}:\n", np.round(d, 2))

print("\n=== SKY POS BLOCKS ((1, 7) > 8) ===")
for coord, d in sky_pos:
    print(f"Block {coord}:\n", np.round(d, 2))

print("\n=== SKY NEG BLOCKS ((1, 7) < -8) ===")
for coord, d in sky_neg:
    print(f"Block {coord}:\n", np.round(d, 2))
