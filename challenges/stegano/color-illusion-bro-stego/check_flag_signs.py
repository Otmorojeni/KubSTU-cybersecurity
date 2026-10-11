import numpy as np
from PIL import Image
from scipy.fftpack import dct

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)[:, :, 0]

def get_dct(b):
    return dct(dct(b.T, norm='ortho').T, norm='ortho')

vals = []
for by in range(160):
    for bx in range(160):
        b = arr[by*8:(by+1)*8, bx*8:(bx+1)*8]
        d = get_dct(b)
        d_clean = d.copy()
        d_clean[0:2, 0:2] = 0
        u, v = np.unravel_index(np.argmax(np.abs(d_clean)), d_clean.shape)
        vals.append((d[u, v], (int(u), int(v))))

print("First 16 blocks:")
for i in range(16):
    print(f"Block {i:2d}: {vals[i][0]:+6.2f} at {vals[i][1]}")

print("\nTrying to decode bytes (row-major):")
for byte_idx in range(30):
    byte_vals = vals[byte_idx*8 : (byte_idx+1)*8]
    b_msb = 0
    b_lsb = 0
    b_inv_msb = 0
    b_inv_lsb = 0
    for i, (v, _) in enumerate(byte_vals):
        bit = 0 if v > 0 else 1
        b_msb = (b_msb << 1) | bit
        b_lsb = b_lsb | (bit << i)
        
        bit_inv = 1 if v > 0 else 0
        b_inv_msb = (b_inv_msb << 1) | bit_inv
        b_inv_lsb = b_inv_lsb | (bit_inv << i)
        
    c_msb = chr(b_msb) if 32 <= b_msb <= 126 else '.'
    c_inv_msb = chr(b_inv_msb) if 32 <= b_inv_msb <= 126 else '.'
    c_lsb = chr(b_lsb) if 32 <= b_lsb <= 126 else '.'
    c_inv_lsb = chr(b_inv_lsb) if 32 <= b_inv_lsb <= 126 else '.'
    print(f"Byte {byte_idx:2d}: msb={b_msb:02x} ({c_msb}) | inv_msb={b_inv_msb:02x} ({c_inv_msb}) | lsb={b_lsb:02x} ({c_lsb}) | inv_lsb={b_inv_lsb:02x} ({c_inv_lsb})")
