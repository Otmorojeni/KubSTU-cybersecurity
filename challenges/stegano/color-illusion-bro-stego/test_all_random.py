import random
import numpy as np
import hashlib
import zlib

gt_coords = [
    (3, 6), (1, 5), (5, 2), (0, 5), (3, 3), (2, 4), (7, 0), (3, 3),
    (2, 0), (5, 2), (0, 5), (3, 4), (1, 5), (0, 3), (1, 7), (3, 4),
    (0, 5), (5, 3), (1, 6), (4, 2)
]
prefix_coords = [(2, 6), (7, 0), (0, 4), (3, 4), (3, 7), (5, 2), (0, 5), (4, 3)]

all_mid = [(u, v) for u in range(8) for v in range(8) if u + v >= 2 and (u, v) not in [(0, 0), (0, 1), (1, 0)]]

seeds = [
    "key-bro", "bro", "key_bro", "bro_stego", "bro_stego_with_hint", "key",
    "stego_hint", "zavod", "factory", "noise"
]

# Add integer seeds
int_seeds = []
for s in seeds:
    int_seeds.append(zlib.crc32(s.encode()))
    int_seeds.append(int(hashlib.md5(s.encode()).hexdigest()[:8], 16))
    int_seeds.append(sum(s.encode()))
    int_seeds.append(int.from_bytes(hashlib.sha256(s.encode()).digest()[:4], 'big'))

print("Testing Python random and NumPy random...")

for s in seeds + int_seeds:
    # 1. random.choice(all_mid)
    random.seed(s)
    seq = [random.choice(all_mid) for _ in range(8)]
    if seq == prefix_coords:
        print(f"!!! MATCH random.choice(all_mid) seed={s}")
    
    # 2. random.randint(0, 7)
    random.seed(s)
    seq = [(random.randint(0, 7), random.randint(0, 7)) for _ in range(8)]
    if seq == prefix_coords:
        print(f"!!! MATCH random.randint(0, 7) seed={s}")

    # 3. np.random
    if isinstance(s, int):
        np.random.seed(s)
        # randint(0, 8)
        u_arr = np.random.randint(0, 8, size=8)
        v_arr = np.random.randint(0, 8, size=8)
        if list(zip(u_arr, v_arr)) == prefix_coords:
            print(f"!!! MATCH np.random.randint seed={s}")
        
        # choice
        np.random.seed(s)
        idx = np.random.choice(len(all_mid), size=8)
        if [all_mid[i] for i in idx] == prefix_coords:
            print(f"!!! MATCH np.random.choice seed={s}")

print("Test finished.")
