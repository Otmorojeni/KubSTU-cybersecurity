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
target_bits = []
for c in target_prefix:
    v = ord(c)
    for b in range(7, -1, -1):
        target_bits.append((v >> b) & 1)

# Active mid/high frequencies:
active_candidates = [
    (0, 5), (0, 6), (0, 7),
    (1, 4), (1, 5), (1, 6), (1, 7),
    (2, 4), (2, 5), (2, 6), (2, 7),
    (3, 4), (3, 7),
    (4, 3), (4, 4), (4, 7),
    (5, 1), (5, 2), (5, 3),
    (6, 0), (6, 1),
    (7, 0)
]

print(f"Testing {len(active_candidates)} active frequencies...")

correct = 0
chosen_seq = []
for i in range(56):
    b = arr[0:8, i*8:(i+1)*8]
    d = get_dct(b)
    
    # Pick candidate with ratio closest to 1.0
    cands = []
    for (u, v) in active_candidates:
        val = d[u, v]
        ratio = abs(val) / (0.25 * Q[u, v])
        cands.append(((u, v), val, ratio, abs(ratio - 1.0)))
    
    cands.sort(key=lambda x: x[3])
    best = cands[0]
    
    # Extracted bit: 0 if val > 0 else 1
    extracted_bit = 0 if best[1] > 0 else 1
    if extracted_bit == target_bits[i]:
        correct += 1
        status = "OK"
    else:
        status = "MISMATCH"
    
    chosen_seq.append(best[0])
    char_name = target_prefix[i // 8]
    bit_pos = 7 - (i % 8)
    print(f"Block {i:2d} ('{char_name}' b{bit_pos}={target_bits[i]}): got {extracted_bit} ({status}) from {best[0]} val={best[1]:+.2f} r={best[2]:.2f}")

print(f"\nTotal correct: {correct}/56 ({correct/56*100:.1f}%)")
