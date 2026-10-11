import numpy as np
from PIL import Image
from scipy.fftpack import dct

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)[:, :, 0]
def get_dct(b): return dct(dct(b.T, norm='ortho').T, norm='ortho')

Q = np.array([
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99],
])

freqs_of_char0 = [(2, 6), (7, 0), (0, 6), (3, 4), (3, 7), (5, 2), (0, 5), (4, 3)]

print("Checking if freqs_of_char0 repeat for each byte:")
for byte_idx in range(7):
    print(f"\n--- Byte {byte_idx} ---")
    for bit_idx in range(8):
        block_idx = byte_idx * 8 + bit_idx
        b = arr[0:8, block_idx*8:(block_idx+1)*8]
        d = get_dct(b)
        f = freqs_of_char0[bit_idx]
        val = d[f[0], f[1]]
        ratio = abs(val) / (0.25 * Q[f[0], f[1]])
        sign = '+' if val > 0 else '-'
        bit = 0 if val > 0 else 1
        print(f"  Bit {7-bit_idx} (block {block_idx:2d}): at {f} -> val={val:+6.2f}, ratio={ratio:.2f}, sign={sign}, bit={bit}")
