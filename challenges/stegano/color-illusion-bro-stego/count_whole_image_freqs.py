import numpy as np
from PIL import Image
from scipy.fftpack import dct
from collections import Counter

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)

def get_dct(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

H, W, _ = arr.shape
n_by, n_bx = H // 8, W // 8

total_counts = Counter()
for by in range(n_by):
    for bx in range(n_bx):
        d = get_dct(arr[by*8:(by+1)*8, bx*8:(bx+1)*8, 0])
        # Find all (u, v) with |d[u, v]| > 12.5 (excluding (0,0), (0,1), (1,0))
        for u in range(8):
            for v in range(8):
                if (u, v) not in [(0, 0), (0, 1), (1, 0)] and abs(d[u, v]) > 12.5:
                    total_counts[(u, v)] += 1

print("Total blocks:", n_by * n_bx)
print(f"Number of unique frequencies with |val| > 12.5: {len(total_counts)}")
print("Frequencies with |val| > 12.5 across whole image:")
for f, cnt in total_counts.most_common():
    print(f"  Freq {f}: count={cnt}")
