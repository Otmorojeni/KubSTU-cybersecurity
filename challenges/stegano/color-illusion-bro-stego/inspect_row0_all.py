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

row0_spikes = []
for i in range(160):
    b = arr[0:8, i*8:(i+1)*8]
    d = get_dct(b)
    cands = []
    for u in range(8):
        for v in range(8):
            if (u, v) != (0, 0):
                r = abs(d[u, v]) / (0.25 * Q[u, v])
                if 0.85 <= r <= 1.15 and abs(d[u, v]) >= 6.0:
                    cands.append(((u, v), d[u, v], r))
    cands.sort(key=lambda x: abs(x[1]), reverse=True)
    row0_spikes.append(cands)

for byte_idx in range(20):
    byte_blocks = row0_spikes[byte_idx*8 : (byte_idx+1)*8]
    # For each block, show top candidate
    line = []
    for bi, blk in enumerate(byte_blocks):
        if len(blk) > 0:
            top = blk[0]
            sign = '+' if top[1] > 0 else '-'
            line.append(f"{sign}({top[0][0]},{top[0][1]})")
        else:
            line.append("?(?,?)")
    print(f"Byte {byte_idx:2d}: " + " ".join(line))
