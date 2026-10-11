import numpy as np
from PIL import Image
from scipy.fftpack import dct
from collections import Counter

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)[:, :, 0]
def get_dct(b): return dct(dct(b.T, norm='ortho').T, norm='ortho')

# Collect 200 consecutive sky blocks:
# Row 10..15, Col 10..40
seq = []
for by in range(12, 16):
    for bx in range(10, 40):
        b = arr[by*8:(by+1)*8, bx*8:(bx+1)*8]
        d = get_dct(b)
        d_clean = d.copy()
        d_clean[0:2, 0:2] = 0
        u, v = np.unravel_index(np.argmax(np.abs(d_clean)), d_clean.shape)
        seq.append((int(u), int(v)))

print(f"Collected sequence of {len(seq)} sky blocks.")

# Test periods from 1 to 50:
for period in range(1, 51):
    matches = 0
    total = 0
    for i in range(len(seq) - period):
        total += 1
        if seq[i] == seq[i + period]:
            matches += 1
    acc = matches / total * 100
    if acc > 15: # if much higher than random (1/20 = 5%)
        print(f"Period {period:2d}: matches = {matches}/{total} ({acc:.1f}%)")
