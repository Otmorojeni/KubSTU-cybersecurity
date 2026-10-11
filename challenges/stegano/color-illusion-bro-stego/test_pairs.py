import numpy as np
from PIL import Image
from scipy.fftpack import dct

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)

def get_dct(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

H, W, _ = arr.shape
n_by, n_bx = H // 8, W // 8

pairs_to_test = [
    ((4, 3), (3, 4)),
    ((5, 2), (2, 5)),
    ((1, 7), (2, 7)),
    ((1, 7), (7, 1)),
    ((2, 6), (6, 2)),
    ((3, 4), (4, 3)),
    ((2, 5), (5, 2))
]

for (u1, v1), (u2, v2) in pairs_to_test:
    diffs = []
    abs_diffs = []
    bits_diff = []
    bits_abs = []
    
    for by in range(n_by):
        for bx in range(n_bx):
            d = get_dct(arr[by*8:(by+1)*8, bx*8:(bx+1)*8, 0])
            c1 = d[u1, v1]
            c2 = d[u2, v2]
            diff = c1 - c2
            adiff = abs(c1) - abs(c2)
            bits_diff.append(1 if diff > 0 else 0)
            bits_abs.append(1 if adiff > 0 else 0)
    
    # Check if there is ASCII or flag
    for btype, blist in [('diff', bits_diff), ('abs', bits_abs)]:
        for msb in [True, False]:
            byte_arr = bytearray()
            for i in range(0, min(len(blist), 800), 8):
                ch = blist[i:i+8]
                val = sum(b << (7 - j) for j, b in enumerate(ch)) if msb else sum(b << j for j, b in enumerate(ch))
                byte_arr.append(val)
            s = bytes(byte_arr)
            # Check for printable or flag
            ascii_chars = sum(1 for b in s if 32 <= b <= 126)
            if b'kubstu' in s.lower() or b'flag' in s.lower() or ascii_chars > len(s) * 0.7:
                print(f"MATCH on pair {((u1, v1), (u2, v2))} ({btype}, msb={msb}): {s[:50]}")
