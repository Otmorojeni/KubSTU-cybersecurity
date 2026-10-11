import numpy as np

# Standard JPEG Zig-Zag order for 8x8
def get_zigzag_matrix():
    zz = np.zeros((8, 8), dtype=int)
    index = 0
    for s in range(15):
        if s % 2 == 0:
            for i in range(s, -1, -1):
                j = s - i
                if i < 8 and j < 8:
                    zz[i, j] = index
                    index += 1
        else:
            for j in range(s, -1, -1):
                i = s - j
                if i < 8 and j < 8:
                    zz[i, j] = index
                    index += 1
    return zz

zz = get_zigzag_matrix()
print("Zig-Zag Matrix:\n", zz)

target_freqs = [
    (2, 6), (7, 0), (0, 4), (3, 4), (3, 7),
    (5, 2), (0, 5), (4, 3), (3, 0), (2, 4),
    (0, 5), (2, 0), (6, 2), (2, 6), (1, 6), (2, 7)
]

print("\nZig-Zag indices of target freqs:")
zz_indices = [zz[u, v] for u, v in target_freqs]
print(zz_indices)
