import numpy as np
from PIL import Image
from scipy.fftpack import dct

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)

def get_dct(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

H, W, _ = arr.shape
n_by, n_bx = H // 8, W // 8

# Let's inspect the spikes for the first 160 blocks (row 0)
bits_pos = []
spike_info = []

for bx in range(160):
    b = arr[0:8, bx*8:(bx+1)*8, 0]
    d = get_dct(b)
    
    # Zero out low frequencies: DC and nearby
    d_clean = d.copy()
    d_clean[0, 0] = 0
    d_clean[0, 1] = 0
    d_clean[1, 0] = 0
    d_clean[1, 1] = 0
    
    # Find max absolute coefficient
    idx = np.unravel_index(np.argmax(np.abs(d_clean)), d_clean.shape)
    val = d[idx]
    bit = 1 if val > 0 else 0
    bits_pos.append(bit)
    spike_info.append((idx, val))

print("First 64 bits extracted from Row 0:")
bit_str = "".join(str(b) for b in bits_pos)
print("Bits (first 64):", bit_str[:64])

# Convert bits to ASCII: 8 bits per char
chars_msb = []
chars_lsb = []
for i in range(0, len(bits_pos) - 7, 8):
    chunk = bits_pos[i:i+8]
    val_msb = sum(b << (7 - j) for j, b in enumerate(chunk))
    val_lsb = sum(b << j for j, b in enumerate(chunk))
    chars_msb.append(chr(val_msb) if 32 <= val_msb <= 126 else '.')
    chars_lsb.append(chr(val_lsb) if 32 <= val_lsb <= 126 else '.')

print("Row 0 as ASCII (MSB):", "".join(chars_msb))
print("Row 0 as ASCII (LSB):", "".join(chars_lsb))

# Inverted bits:
bits_inv = [1 - b for b in bits_pos]
chars_inv_msb = []
chars_inv_lsb = []
for i in range(0, len(bits_inv) - 7, 8):
    chunk = bits_inv[i:i+8]
    val_msb = sum(b << (7 - j) for j, b in enumerate(chunk))
    val_lsb = sum(b << j for j, b in enumerate(chunk))
    chars_inv_msb.append(chr(val_msb) if 32 <= val_msb <= 126 else '.')
    chars_inv_lsb.append(chr(val_lsb) if 32 <= val_lsb <= 126 else '.')

print("Row 0 inverted (MSB):", "".join(chars_inv_msb))
print("Row 0 inverted (LSB):", "".join(chars_inv_lsb))
