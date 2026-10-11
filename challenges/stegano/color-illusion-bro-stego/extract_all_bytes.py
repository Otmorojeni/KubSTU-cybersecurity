import numpy as np
from PIL import Image
from scipy.fftpack import dct

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)

def get_dct(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

H, W, _ = arr.shape
n_by, n_bx = H // 8, W // 8

# Extract sign bit from all 25600 blocks:
# Order 1: row by row (by, then bx)
# Order 2: col by col (bx, then by)

bits_row = []
bits_col = []

# Precompute DCT for all blocks
print("Computing DCT for all 25600 blocks...")
dct_grid = np.zeros((n_by, n_bx, 8, 8), dtype=np.float32)
for by in range(n_by):
    for bx in range(n_bx):
        d = get_dct(arr[by*8:(by+1)*8, bx*8:(bx+1)*8, 0])
        dct_grid[by, bx] = d

print("Extracting bits...")
for by in range(n_by):
    for bx in range(n_bx):
        d = dct_grid[by, bx].copy()
        d[0:2, 0:2] = 0
        u, v = np.unravel_index(np.argmax(np.abs(d)), d.shape)
        val = d[u, v]
        bits_row.append(1 if val > 0 else 0)

for bx in range(n_bx):
    for by in range(n_by):
        d = dct_grid[by, bx].copy()
        d[0:2, 0:2] = 0
        u, v = np.unravel_index(np.argmax(np.abs(d)), d.shape)
        val = d[u, v]
        bits_col.append(1 if val > 0 else 0)

# Convert to bytes
def to_bytes(bits, msb=True):
    b_arr = bytearray()
    for i in range(0, len(bits) - 7, 8):
        chunk = bits[i:i+8]
        if msb:
            byte = sum(b << (7 - j) for j, b in enumerate(chunk))
        else:
            byte = sum(b << j for j, b in enumerate(chunk))
        b_arr.append(byte)
    return bytes(b_arr)

bytes_row_msb = to_bytes(bits_row, True)
bytes_row_lsb = to_bytes(bits_row, False)
bytes_col_msb = to_bytes(bits_col, True)
bytes_col_lsb = to_bytes(bits_col, False)

with open('extracted_row_msb.bin', 'wb') as f: f.write(bytes_row_msb)
with open('extracted_row_lsb.bin', 'wb') as f: f.write(bytes_row_lsb)
with open('extracted_col_msb.bin', 'wb') as f: f.write(bytes_col_msb)
with open('extracted_col_lsb.bin', 'wb') as f: f.write(bytes_col_lsb)

print(f"Extracted {len(bytes_row_msb)} bytes!")
print("Row MSB first 20 bytes:", bytes_row_msb[:20].hex())
