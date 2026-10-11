import numpy as np
from PIL import Image
from scipy.fftpack import dct
import random
import zlib
import hashlib

print("Loading image...")
img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)[:, :, 0]

def get_dct(b):
    return dct(dct(b.T, norm='ortho').T, norm='ortho')

# Precompute DCT for the first 500 blocks (row-major)
# 500 blocks = 62.5 bytes (enough for any CTF flag)
print("Precomputing DCTs for first 500 blocks...")
dct_blocks = []
for i in range(500):
    by = i // 160
    bx = i % 160
    b = arr[by*8:(by+1)*8, bx*8:(bx+1)*8]
    dct_blocks.append(get_dct(b))

print("DCTs precomputed.")

def decode_bits(bits, msb_first=True, invert=False):
    byte_arr = bytearray()
    for i in range(0, len(bits) - 7, 8):
        byte_bits = bits[i:i+8]
        if invert:
            byte_bits = [1 - b for b in byte_bits]
        val = 0
        if msb_first:
            for b in byte_bits:
                val = (val << 1) | b
        else:
            for j, b in enumerate(byte_bits):
                val |= (b << j)
        byte_arr.append(val)
    return bytes(byte_arr)

# Test 1: What if the bit is defined by sign of d[u, v]?
# Let's test a sequence of (u, v) for each block i:
def test_freq_sequence(freq_seq, name):
    bits_pos = [] # 1 if d > 0 else 0
    bits_neg = [] # 1 if d < 0 else 0
    for i, (u, v) in enumerate(freq_seq):
        val = dct_blocks[i][u, v]
        bits_pos.append(1 if val > 0 else 0)
        bits_neg.append(1 if val < 0 else 0)
        
    for msb in [True, False]:
        for b_name, b_list in [('pos', bits_pos), ('neg', bits_neg)]:
            res = decode_bits(b_list, msb_first=msb)
            if b'kubstu' in res.lower() or b'ctf' in res.lower():
                print(f"!!! MATCH FOUND ({name}, msb={msb}, {b_name}) !!!: {res[:50]}")
                return True
            # Check if starts with K
            if res.startswith(b'K') or res.startswith(b'k'):
                print(f"Partial match ({name}, msb={msb}, {b_name}): {res[:15]}")
    return False

# List of candidate frequency sets:
freq_sets = [
    # Anti-diagonal u+v=7
    [(0, 7), (1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1), (7, 0)],
    # All common frequencies found earlier:
    [(2, 7), (2, 5), (1, 7), (5, 2), (4, 3), (3, 7), (1, 6), (1, 5), (5, 3), (0, 7), (6, 1), (7, 0), (4, 4), (2, 6)],
    # Mid-frequency band from OpenStego:
    [(0, 3), (1, 2), (2, 1), (3, 0), (0, 4), (1, 3), (2, 2), (3, 1), (4, 0),
     (0, 5), (1, 4), (2, 3), (3, 2), (4, 1), (5, 0), (1, 5), (2, 4), (3, 3),
     (4, 2), (5, 1), (3, 4), (4, 3)]
]

keys = ["key-bro", "bro", "key_bro", "bro_stego", "key", "stego_hint"]

# Test Python random.choice
print("\n--- Testing Python random.choice ---")
for k in keys:
    for s in [k, zlib.crc32(k.encode()), sum(k.encode()), int(hashlib.md5(k.encode()).hexdigest()[:8], 16)]:
        for fset_idx, fset in enumerate(freq_sets):
            random.seed(s)
            seq = [random.choice(fset) for _ in range(500)]
            test_freq_sequence(seq, f"py random.choice fset{fset_idx} k={k}")

            random.seed(s)
            seq = [fset[random.randint(0, len(fset)-1)] for _ in range(500)]
            test_freq_sequence(seq, f"py random.randint fset{fset_idx} k={k}")

# Test Python random.randint(0, 7) for u, v
print("\n--- Testing Python random.randint(0, 7) ---")
for k in keys:
    for s in [k, zlib.crc32(k.encode())]:
        random.seed(s)
        seq = [(random.randint(0, 7), random.randint(0, 7)) for _ in range(500)]
        test_freq_sequence(seq, f"py randint(0, 7) k={k}")

        random.seed(s)
        seq = [(random.randint(1, 7), random.randint(1, 7)) for _ in range(500)]
        test_freq_sequence(seq, f"py randint(1, 7) k={k}")

print("Initial PRNG sweep finished.")
