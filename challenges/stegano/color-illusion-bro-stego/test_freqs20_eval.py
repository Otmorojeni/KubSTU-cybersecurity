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

freqs20 = [
    (2, 4), (0, 5), (1, 7), (3, 4), (4, 3), (2, 7), (1, 6), (3, 7),
    (2, 5), (5, 3), (6, 0), (0, 6), (5, 2), (4, 4), (0, 7), (1, 5),
    (7, 0), (2, 6), (6, 1), (4, 7)
]

print("Testing argmax over freqs20:")
for i in range(16):
    b = arr[0:8, i*8:(i+1)*8]
    d = get_dct(b)
    # 1. max abs(d) in freqs20
    best_f = max(freqs20, key=lambda f: abs(d[f]))
    val = d[best_f]
    bit = 0 if val > 0 else 1
    
    # 2. best ratio to 1.0 in freqs20
    best_f_r = min(freqs20, key=lambda f: abs(abs(d[f]) / (0.25 * Q[f]) - 1.0))
    val_r = d[best_f_r]
    bit_r = 0 if val_r > 0 else 1
    
    print(f"Block {i:2d}: [max_abs] {best_f} val={val:+6.2f} bit={bit} | [best_r] {best_f_r} val={val_r:+6.2f} bit={bit_r}")
