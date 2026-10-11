import numpy as np
from PIL import Image
import os

# Check all 64 frequency maps in freq_maps/
# For each map, check:
# 1. Is there text or patterns?
# 2. Variance, edge count, or histogram
scores = []
for u in range(8):
    for v in range(8):
        fn = f'freq_maps/freq_{u}_{v}.png'
        im = Image.open(fn)
        arr = np.array(im)
        # Check standard deviation of arr
        # Check number of pixels far from mean
        mean = arr.mean()
        std = arr.std()
        num_bright = np.sum(arr > 200)
        num_dark = np.sum(arr < 50)
        scores.append(((u, v), std, num_bright, num_dark))

# Sort by std or interestingness
scores.sort(key=lambda x: x[1], reverse=True)
print("Top 15 frequency maps by standard deviation:")
for (u, v), std, nb, nd in scores[:15]:
    print(f"Freq ({u},{v}): std={std:.2f}, bright={nb}, dark={nd}")
