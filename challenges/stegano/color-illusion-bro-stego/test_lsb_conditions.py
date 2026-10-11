import numpy as np
from PIL import Image
from scipy.fftpack import dct
import zigzag as zz

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

quant_blocks = []
for by in range(160):
    for bx in range(160):
        b = arr[by*8:(by+1)*8, bx*8:(bx+1)*8]
        d = get_dct(b)
        q = np.round(d / (0.25 * Q)).astype(int)
        quant_blocks.append(q)

def decode_bits(bits):
    res_msb = bytearray()
    res_lsb = bytearray()
    res_inv_msb = bytearray()
    for i in range(0, len(bits) - 7, 8):
        b_chunk = bits[i:i+8]
        v_m = 0
        v_l = 0
        v_im = 0
        for j, b in enumerate(b_chunk):
            v_m = (v_m << 1) | b
            v_l |= (b << j)
            v_im = (v_im << 1) | (1 - b)
        res_msb.append(v_m)
        res_lsb.append(v_l)
        res_inv_msb.append(v_im)
    return bytes(res_msb), bytes(res_lsb), bytes(res_inv_msb)

for condition_name, cond_fn in [
    ("all_ac", lambda c: True),
    ("nonzero", lambda c: c != 0),
    ("nonzero_not_one", lambda c: c not in [0, 1, -1]),
    ("gt_one", lambda c: c > 1),
    ("abs_gt_one", lambda c: abs(c) > 1),
]:
    bits = []
    for q in quant_blocks[:500]:
        zz_coeffs = zz.zigzag(q)
        for c in zz_coeffs[1:]:
            c_int = int(c)
            if cond_fn(c_int):
                bits.append(c_int & 1)
    
    for d, mode in zip(decode_bits(bits), ["msb", "lsb", "inv_msb"]):
        if b'kubstu' in d.lower() or b'ctf' in d.lower():
            print(f"!!! MATCH ({condition_name}, {mode}) !!!: {d[:100]}")
        elif d.startswith(b'K') or d.startswith(b'k'):
            print(f"Partial match ({condition_name}, {mode}): {d[:20]}")

print("Test complete.")
