import numpy as np
from PIL import Image
from scipy.fftpack import dct
import hashlib
import zlib
import random
import struct

# Ground truth sequence from Row 12, Col 10..29 (idx = 12*160 + c = 1930..1949)
gt_coords = [
    (3, 6), (1, 5), (5, 2), (0, 5), (3, 3), (2, 4), (7, 0), (3, 3),
    (2, 0), (5, 2), (0, 5), (3, 4), (1, 5), (0, 3), (1, 7), (3, 4),
    (0, 5), (5, 3), (1, 6), (4, 2)
]

# Prefix sequence from Row 0, Col 0..7 (idx = 0..7)
prefix_coords = [(2, 6), (7, 0), (0, 4), (3, 4), (3, 7), (5, 2), (0, 5), (4, 3)]

print("Testing PRNG matching for both prefix (idx 0..7) and sky (idx 1930..1949)...")

keys = ["key-bro", "bro", "key_bro", "bro_stego", "bro_stego_with_hint", "key", "stego_hint"]

# What if the PRNG generates (u, v) pairs directly?
# What if it generates an index into an active list?
active_list = [
    (2, 7), (2, 5), (1, 7), (5, 2), (4, 3), (3, 7), (1, 6), (1, 5),
    (5, 3), (0, 7), (6, 1), (7, 0), (4, 4), (2, 6), (4, 7), (1, 1),
    (3, 6), (7, 1), (6, 2), (3, 4), (5, 4), (6, 0), (3, 5), (0, 6),
    (6, 3), (0, 2), (7, 5), (2, 3), (2, 0), (1, 3), (5, 0), (0, 4),
    (3, 3), (3, 0), (2, 1), (7, 3), (4, 6), (2, 4), (7, 7), (5, 7)
]

print("Total candidate frequencies:", len(active_list))

def check_generator(gen_fn, name):
    try:
        # Generate 2000 elements
        seq = [gen_fn(i) for i in range(2000)]
        # Check prefix:
        if seq[:8] == prefix_coords or seq[:8] == [(v, u) for u, v in prefix_coords]:
            print(f"!!! MATCH ON PREFIX: {name} !!!")
            return True
        # Check sky at 1930:
        if seq[1930:1930+10] == gt_coords[:10]:
            print(f"!!! MATCH ON SKY: {name} !!!")
            return True
        # Check sky at offset 0 (if PRNG was only used for blocks with message):
        for offset in range(0, 1000):
            if seq[offset:offset+8] == prefix_coords:
                print(f"!!! MATCH ON PREFIX with offset {offset}: {name} !!!")
                return True
    except Exception as e:
        pass
    return False

# 1. RC4
def rc4_stream(key_bytes):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key_bytes[i % len(key_bytes)]) % 256
        S[i], S[j] = S[j], S[i]
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        yield S[(S[i] + S[j]) % 256]

for k in keys:
    for kb in [k.encode(), k.encode() + b'\x00', hashlib.md5(k.encode()).digest(), hashlib.sha256(k.encode()).digest()]:
        # Generator: (b1 % 8, b2 % 8)
        rc = rc4_stream(kb)
        stream_bytes = [next(rc) for _ in range(4000)]
        
        # Method 1: two bytes per block
        check_generator(lambda i: (stream_bytes[2*i] % 8, stream_bytes[2*i+1] % 8), f"RC4 two bytes k={k}")
        check_generator(lambda i: (stream_bytes[2*i] % 7 + 1, stream_bytes[2*i+1] % 7 + 1), f"RC4 two bytes 1..7 k={k}")
        
        # Method 2: one byte per block: u = (b >> 3) & 7, v = b & 7
        check_generator(lambda i: ((stream_bytes[i] >> 3) & 7, stream_bytes[i] & 7), f"RC4 bitshift k={k}")
        check_generator(lambda i: (stream_bytes[i] // 8, stream_bytes[i] % 8), f"RC4 divmod k={k}")
        
        # Method 3: index into active_list
        for n_cand in [16, 20, 24, 32, len(active_list)]:
            check_generator(lambda i: active_list[stream_bytes[i] % n_cand], f"RC4 active_list[{n_cand}] k={k}")

print("RC4 check done.")
