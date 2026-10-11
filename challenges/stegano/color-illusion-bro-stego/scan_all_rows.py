import numpy as np
from PIL import Image
from scipy.fftpack import dct

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)[:, :, 0]
def get_dct(b): return dct(dct(b.T, norm='ortho').T, norm='ortho')

print("Scanning all 160 rows for flag strings...")

all_rows_text = []
for by in range(160):
    bits = []
    for bx in range(160):
        b = arr[by*8:(by+1)*8, bx*8:(bx+1)*8]
        d = get_dct(b)
        d_clean = d.copy()
        d_clean[0:2, 0:2] = 0
        u, v = np.unravel_index(np.argmax(np.abs(d_clean)), d_clean.shape)
        val = d[u, v]
        # bit: 0 if val > 0 else 1 (inverted MSB)
        bits.append(0 if val > 0 else 1)
    
    # Decode 20 bytes
    row_bytes = bytearray()
    for i in range(0, 160, 8):
        v = 0
        for bit in bits[i:i+8]:
            v = (v << 1) | bit
        row_bytes.append(v)
    
    row_str = "".join(chr(c) if 32 <= c <= 126 else '.' for c in row_bytes)
    all_rows_text.append(row_bytes)
    
    # Check for keywords
    row_lower = bytes(row_bytes).lower()
    if b'kubstu' in row_lower or b'ctf' in row_lower or b'flag' in row_lower:
        print(f"!!! MATCH in Row {by}: {row_str}")
    elif row_str.startswith('K') or row_str.startswith('k'):
        print(f"Row {by:3d}: {row_str}")

print("\nFirst 10 rows:")
for by in range(10):
    row_str = "".join(chr(c) if 32 <= c <= 126 else '.' for c in all_rows_text[by])
    print(f"Row {by:2d}: {row_str}")
