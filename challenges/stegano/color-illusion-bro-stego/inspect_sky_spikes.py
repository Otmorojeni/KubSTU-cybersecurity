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

# Let's inspect Row 10, Col 10..40
print("Inspecting Row 10, Col 10..40:")
for bx in range(10, 30):
    b = arr[10*8:11*8, bx*8:(bx+1)*8]
    d = get_dct(b)
    # List all coefficients with |val| > 7.0 and u+v >= 3
    spikes = []
    for u in range(8):
        for v in range(8):
            if u + v >= 3 and abs(d[u, v]) > 7.0:
                spikes.append(((u, v), round(d[u, v], 2), round(abs(d[u, v]) / (0.25 * Q[u, v]), 2)))
    spikes.sort(key=lambda x: abs(x[1]), reverse=True)
    print(f"Col {bx:2d}: spikes = {spikes}")
