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

target = "KubSTU{"
for blk_idx in range(7):
    b = arr[0:8, blk_idx*8:(blk_idx+1)*8]
    d = get_dct(b)
    spikes = []
    for u in range(8):
        for v in range(8):
            if (u, v) != (0, 0):
                step = 0.25 * Q[u, v]
                k = d[u, v] / step
                if abs(k) >= 0.8:
                    spikes.append(((u, v), d[u, v], step, k))
    ch = target[blk_idx]
    print(f"=== BLOCK {blk_idx} (target char: '{ch}', ascii={ord(ch)}, bin={ord(ch):08b}) ===")
    for s in spikes:
        print(f"  freq={s[0]}: val={s[1]:+6.2f}, step={s[2]:5.2f}, k={s[3]:+5.2f}")
