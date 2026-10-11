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

# For each block in Row 0, find all frequencies with 0.25*Q >= 9.0 and abs(d) >= 7.0
print("Row 0 blocks 0..55 (filtered by 0.25*Q >= 9.0 and abs(d) >= 7.0):")
for i in range(56):
    b = arr[0:8, i*8:(i+1)*8]
    d = get_dct(b)
    spikes = []
    for u in range(8):
        for v in range(8):
            if 0.25 * Q[u, v] >= 9.0 and abs(d[u, v]) >= 7.0:
                ratio = abs(d[u, v]) / (0.25 * Q[u, v])
                if 0.7 <= ratio <= 1.3:
                    spikes.append(((u, v), round(d[u, v], 1), round(ratio, 2)))
    spikes.sort(key=lambda x: abs(x[1]), reverse=True)
    print(f"Block {i:2d}: {spikes}")
