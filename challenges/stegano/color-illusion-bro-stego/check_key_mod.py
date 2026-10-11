import numpy as np
from PIL import Image
from scipy.fftpack import dct

key = "key-bro"
print(f"Key: {key}, length: {len(key)}")

# What was observed in sky blocks?
# In find_ground_truth.py:
# Row 12, Col 10..29 (idx = 1930..1949):
# 1930 % 7 = 5 ('r')
# 1931 % 7 = 6 ('o')
# 1932 % 7 = 0 ('k')
# 1933 % 7 = 1 ('e')
# 1934 % 7 = 2 ('y')
# 1935 % 7 = 3 ('-')
# 1936 % 7 = 4 ('b')
# 1937 % 7 = 5 ('r')
# ...
gt = [
    (3, 6), (1, 5), (5, 2), (0, 5), (3, 3), (2, 4), (7, 0), (3, 3),
    (2, 0), (5, 2), (0, 5), (3, 4), (1, 5), (0, 3), (1, 7), (3, 4),
    (0, 5), (5, 3), (1, 6), (4, 2)
]

for i, f in enumerate(gt):
    idx = 1930 + i
    kchar = key[idx % len(key)]
    print(f"Block {idx} (mod 7 = {idx % 7}, '{kchar}'): freq={f}")
