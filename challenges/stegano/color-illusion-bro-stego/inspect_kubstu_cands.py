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

target_flag_prefix = "KubSTU{"
target_bits = []
for c in target_flag_prefix:
    v = ord(c)
    for b in range(7, -1, -1):
        target_bits.append((v >> b) & 1)

print(f"Target bits ({len(target_bits)}): {target_bits}")

for i in range(len(target_bits)):
    b = arr[0:8, i*8:(i+1)*8]
    d = get_dct(b)
    bit = target_bits[i]
    needed_sign = 1 if bit == 0 else -1
    char_name = target_flag_prefix[i // 8]
    bit_pos = 7 - (i % 8)
    
    # Find all frequencies (u, v) where sign matches needed_sign and abs(val) > 3.0
    cands = []
    for u in range(8):
        for v in range(8):
            if (u, v) != (0, 0):
                val = d[u, v]
                ratio = abs(val) / (0.25 * Q[u, v])
                if (val * needed_sign) > 0:
                    cands.append(((u, v), val, ratio, abs(ratio - 1.0)))
    
    cands.sort(key=lambda x: x[3]) # closest ratio to 1.0
    top_cands = [(c[0], f"{c[1]:+.1f}", f"r={c[2]:.2f}") for c in cands[:3]]
    print(f"Block {i:2d} ('{char_name}' b{bit_pos}={bit}): {top_cands}")
