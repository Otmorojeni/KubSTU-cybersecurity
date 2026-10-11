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

target_prefix = "KubSTU{"
bits = []
for c in target_prefix:
    v = ord(c)
    for b in range(7, -1, -1):
        bits.append((v >> b) & 1)

matched_freqs = []
for i in range(56):
    b = arr[0:8, i*8:(i+1)*8]
    d = get_dct(b)
    req_sign = 1 if bits[i] == 0 else -1
    
    # Find all frequencies with ratio close to 1.0 having req_sign
    cands = []
    for u in range(8):
        for v in range(8):
            if (u, v) != (0, 0):
                val = d[u, v]
                if val * req_sign > 0:
                    r = abs(val) / (0.25 * Q[u, v])
                    cands.append(((u, v), val, r, abs(r - 1.0)))
    cands.sort(key=lambda x: x[3])
    best = cands[0]
    matched_freqs.append(best[0])
    char_name = target_prefix[i // 8]
    print(f"Block {i:2d} ('{char_name}' bit={bits[i]}): freq={best[0]}, val={best[1]:+6.2f}, ratio={best[2]:.2f}")

print("\nMatched frequency sequence for first 56 blocks:")
print(matched_freqs)
