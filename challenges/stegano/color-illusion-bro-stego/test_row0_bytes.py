import numpy as np
from PIL import Image
from scipy.fftpack import dct

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)[:, :, 0]
def get_dct(b): return dct(dct(b.T, norm='ortho').T, norm='ortho')

bits = []
coords = []
for bx in range(160):
    b = arr[0:8, bx*8:(bx+1)*8]
    d = get_dct(b)
    d_clean = d.copy()
    d_clean[0:2, 0:2] = 0
    u, v = np.unravel_index(np.argmax(np.abs(d_clean)), d_clean.shape)
    val = d[u, v]
    bit = 0 if val > 0 else 1
    bits.append(bit)
    coords.append((u, v, val))

bytes_val = []
for i in range(0, 160, 8):
    v = 0
    for bit in bits[i:i+8]:
        v = (v << 1) | bit
    bytes_val.append(v)

print('Bytes hex:', [hex(x) for x in bytes_val])
print('Bytes char:', ''.join(chr(x) if 32 <= x <= 126 else '.' for x in bytes_val))
for byte_idx in range(len(bytes_val)):
    blk_info = ' '.join(f'({coords[i][0]},{coords[i][1]}):{coords[i][2]:+5.1f}' for i in range(byte_idx*8, (byte_idx+1)*8))
    ch = chr(bytes_val[byte_idx]) if 32 <= bytes_val[byte_idx] <= 126 else '.'
    print(f'Byte {byte_idx:2d}: {ch} (0x{bytes_val[byte_idx]:02x}) -> {blk_info}')
