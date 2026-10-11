import numpy as np
from PIL import Image
from scipy.fftpack import dct
import string

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

# For each block in Row 0, get candidate bits:
block_cands = []
for i in range(160):
    b = arr[0:8, i*8:(i+1)*8]
    d = get_dct(b)
    # Find all frequencies with ratio in [0.80, 1.20]
    cands = []
    for u in range(8):
        for v in range(8):
            if (u, v) != (0, 0):
                r = abs(d[u, v]) / (0.25 * Q[u, v])
                if 0.80 <= r <= 1.20:
                    bit = 0 if d[u, v] > 0 else 1
                    err = abs(r - 1.0)
                    cands.append((bit, err, (u, v), d[u, v]))
    # If no candidate found in [0.8, 1.2], pick closest to 1.0
    if len(cands) == 0:
        for u in range(8):
            for v in range(8):
                if u + v >= 2:
                    r = abs(d[u, v]) / (0.25 * Q[u, v])
                    bit = 0 if d[u, v] > 0 else 1
                    cands.append((bit, abs(r - 1.0), (u, v), d[u, v]))
        cands.sort(key=lambda x: x[1])
        cands = cands[:2]
    block_cands.append(cands)

# For each byte (8 blocks), try combinations of candidate bits that form printable ASCII or known pattern
print("Testing candidate reconstruction for Row 0 (20 bytes):")

valid_chars = set(string.ascii_letters + string.digits + "{}_-!@#$+= ")

best_text = []
for byte_idx in range(20):
    byte_blocks = block_cands[byte_idx*8 : (byte_idx+1)*8]
    
    # Try all combinations of bits (at most 2-3 per block)
    # Let's take top 2 candidates per block:
    options_per_block = []
    for blk in byte_blocks:
        # unique bits available
        bits_avail = list(set([c[0] for c in blk[:3]]))
        if len(bits_avail) == 0:
            bits_avail = [0, 1]
        options_per_block.append(bits_avail)
    
    # Generate all candidate bytes
    import itertools
    all_combos = list(itertools.product(*options_per_block))
    
    candidates_byte = []
    for bits in all_combos:
        val = 0
        for b in bits:
            val = (val << 1) | b
        ch = chr(val)
        if ch in valid_chars:
            candidates_byte.append((ch, val))
    
    # If byte_idx == 0: must be 'K' or 'k'
    if byte_idx == 0:
        print(f"Byte 0 options: {set(c[0] for c in candidates_byte)}")
    elif byte_idx == 1:
        print(f"Byte 1 options: {set(c[0] for c in candidates_byte)}")
    elif byte_idx == 2:
        print(f"Byte 2 options: {set(c[0] for c in candidates_byte)}")
    elif byte_idx == 3:
        print(f"Byte 3 options: {set(c[0] for c in candidates_byte)}")
    elif byte_idx == 4:
        print(f"Byte 4 options: {set(c[0] for c in candidates_byte)}")
    elif byte_idx == 5:
        print(f"Byte 5 options: {set(c[0] for c in candidates_byte)}")
    elif byte_idx == 6:
        print(f"Byte 6 options: {set(c[0] for c in candidates_byte)}")
    else:
        chars_set = set(c[0] for c in candidates_byte)
        print(f"Byte {byte_idx:2d} options: {chars_set}")
