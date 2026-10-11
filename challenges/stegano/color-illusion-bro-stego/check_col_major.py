import numpy as np
from PIL import Image
from scipy.fftpack import dct

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)[:, :, 0]
def get_dct(b): return dct(dct(b.T, norm='ortho').T, norm='ortho')

vals_col = []
for bx in range(160):
    for by in range(160):
        b = arr[by*8:(by+1)*8, bx*8:(bx+1)*8]
        d = get_dct(b)
        d_clean = d.copy()
        d_clean[0:2, 0:2] = 0
        u, v = np.unravel_index(np.argmax(np.abs(d_clean)), d_clean.shape)
        vals_col.append((d[u, v], (int(u), int(v))))

print("Column-major first 30 bytes:")
for byte_idx in range(30):
    byte_vals = vals_col[byte_idx*8 : (byte_idx+1)*8]
    b_msb = 0
    b_inv_msb = 0
    for v, _ in byte_vals:
        bit = 0 if v > 0 else 1
        b_msb = (b_msb << 1) | bit
        bit_inv = 1 if v > 0 else 0
        b_inv_msb = (b_inv_msb << 1) | bit_inv
    c1 = chr(b_msb) if 32 <= b_msb <= 126 else '.'
    c2 = chr(b_inv_msb) if 32 <= b_inv_msb <= 126 else '.'
    print(f"Byte {byte_idx:2d}: msb={b_msb:02x} ({c1}) | inv={b_inv_msb:02x} ({c2})")
