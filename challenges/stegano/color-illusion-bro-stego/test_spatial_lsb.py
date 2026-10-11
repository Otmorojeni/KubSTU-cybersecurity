from PIL import Image
import numpy as np

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img)

# Let's extract LSB from R, G, B, RGB, BGR
for c, name in enumerate(['R', 'G', 'B']):
    bits = arr[:, :, c] & 1
    bits_flat = bits.flatten()
    bytes_data = np.packbits(bits_flat)
    s = bytes(bytes_data[:100])
    print(f"LSB {name} first 50 bytes: {s[:50]}")
    # Search for flag
    full_bytes = bytes(bytes_data)
    if b'kubstu' in full_bytes.lower() or b'flag' in full_bytes.lower() or b'{' in full_bytes:
        print(f"FOUND IN LSB {name}!")

# RGB interleaved
bits_rgb = (arr & 1).flatten()
bytes_rgb = bytes(np.packbits(bits_rgb))
print(f"LSB RGB interleaved first 50 bytes: {bytes_rgb[:50]}")
if b'kubstu' in bytes_rgb.lower() or b'flag' in bytes_rgb.lower():
    print("FOUND IN LSB RGB!")
