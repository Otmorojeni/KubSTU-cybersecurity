import numpy as np
from PIL import Image
from scipy.fftpack import dct
from collections import Counter

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

counts = Counter()
total_blocks = 0
for by in range(5, 25):
    for bx in range(5, 45):
        total_blocks += 1
        b = arr[by*8:(by+1)*8, bx*8:(bx+1)*8]
        d = get_dct(b)
        # Find which (u, v) has ratio between 0.85 and 1.15
        for u in range(8):
            for v in range(8):
                if u + v >= 3:
                    ratio = abs(d[u, v]) / (0.25 * Q[u, v])
                    if 0.88 <= ratio <= 1.12:
                        counts[(u, v)] += 1

print(f"Total sky blocks checked: {total_blocks}")
print("Frequency occurrences with ratio in [0.88, 1.12]:")
for f, cnt in counts.most_common():
    print(f"  {f}: count={cnt} ({cnt/total_blocks*100:.1f}%), Q={Q[f]}, 0.25*Q={0.25*Q[f]:.2f}")
