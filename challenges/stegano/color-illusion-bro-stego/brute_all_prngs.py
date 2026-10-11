import random
import zlib
import hashlib
import numpy as np
import struct

# The target sequence of frequencies for the first 8 blocks:
# (u, v) pairs
target = [(2, 6), (7, 0), (0, 4), (3, 4), (3, 7), (5, 2), (0, 5), (4, 3)]
target_transposed = [(v, u) for u, v in target]
target_idx_rc = [u * 8 + v for u, v in target]
target_idx_cr = [v * 8 + u for u, v in target]

print("Target (u, v):", target)
print("Target transposed (v, u):", target_transposed)
print("Target idx (u*8+v):", target_idx_rc)
print("Target idx (v*8+u):", target_idx_cr)

keys = [
    "key-bro", "bro", "key_bro", "bro_stego", "bro_stego_with_hint",
    "key-bro\n", "key-bro\0", "key", "bro!"
]

def check_seq(seq, name):
    s = list(seq)[:8]
    if len(s) < 8:
        return
    if s == target or s == target_transposed:
        print(f"!!! MATCH FOUND (pairs): {name}")
        return True
    if s == target_idx_rc or s == target_idx_cr:
        print(f"!!! MATCH FOUND (indices): {name}")
        return True
    return False

# 1. Java Random
class JavaRandom:
    def __init__(self, seed):
        self.seed = (seed ^ 0x5DEECE66D) & ((1 << 48) - 1)
    def next(self, bits):
        self.seed = (self.seed * 0x5DEECE66D + 0xB) & ((1 << 48) - 1)
        return self.seed >> (48 - bits)
    def nextInt(self, bound=None):
        if bound is None:
            val = self.next(32)
            return val if val < (1 << 31) else val - (1 << 32)
        r = self.next(31)
        m = bound - 1
        if (bound & m) == 0:
            return (bound * r) >> 31
        u = r
        r = u % bound
        while (u - r + m) < 0:
            u = self.next(31)
            r = u % bound
        return r

# Test Java Random
for k in keys:
    # Hash variants
    md5_long = int(hashlib.md5(k.encode()).hexdigest()[:15], 16)
    seeds = [
        md5_long,
        zlib.crc32(k.encode()),
        int.from_bytes(hashlib.sha256(k.encode()).digest()[:8], 'big'),
        sum(k.encode())
    ]
    for s in seeds:
        jr = JavaRandom(s)
        # nextInt(8), nextInt(8)
        seq = [(jr.nextInt(8), jr.nextInt(8)) for _ in range(8)]
        check_seq(seq, f"JavaRandom.nextInt(8) key={k} seed={s}")
        
        jr = JavaRandom(s)
        seq = [jr.nextInt(64) for _ in range(8)]
        check_seq(seq, f"JavaRandom.nextInt(64) key={k} seed={s}")

        # OpenStego style: Math.abs(rand.nextInt()) % 62 + 1
        jr = JavaRandom(s)
        seq = []
        for _ in range(8):
            while True:
                c = (abs(jr.nextInt()) % 62) + 1
                # is mid freq?
                if c in [3, 10, 17, 24, 4, 11, 18, 25, 32, 5, 12, 19, 26, 33, 40, 13, 20, 27, 34, 41, 28, 35]:
                    seq.append(c)
                    break
        check_seq(seq, f"JavaRandom OpenStego midfreq key={k} seed={s}")

# 2. Python random
for k in keys:
    for s in [k, zlib.crc32(k.encode()), hashlib.md5(k.encode()).hexdigest(), sum(k.encode())]:
        random.seed(s)
        seq = [(random.randint(0, 7), random.randint(0, 7)) for _ in range(8)]
        check_seq(seq, f"Python randint(0, 7) key={k} seed={s}")
        
        random.seed(s)
        seq = [random.randint(0, 63) for _ in range(8)]
        check_seq(seq, f"Python randint(0, 63) key={k} seed={s}")

        random.seed(s)
        seq = [(random.randrange(8), random.randrange(8)) for _ in range(8)]
        check_seq(seq, f"Python randrange(8) key={k} seed={s}")

        random.seed(s)
        seq = [random.randrange(64) for _ in range(8)]
        check_seq(seq, f"Python randrange(64) key={k} seed={s}")

# 3. C / C++ rand() (MSVC and glibc)
def msvc_rand(seed):
    state = seed & 0xFFFFFFFF
    while True:
        state = (state * 214013 + 2531011) & 0xFFFFFFFF
        yield (state >> 16) & 0x7FFF

def glibc_rand(seed):
    state = seed & 0xFFFFFFFF
    while True:
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        yield state

for name, rgen in [("MSVC", msvc_rand), ("glibc", glibc_rand)]:
    for k in keys:
        for s in [zlib.crc32(k.encode()), sum(k.encode()), int.from_bytes(k.encode()[:4], 'little')]:
            g = rgen(s)
            seq = [(next(g) % 8, next(g) % 8) for _ in range(8)]
            check_seq(seq, f"{name} % 8 key={k} seed={s}")

            g = rgen(s)
            seq = [next(g) % 64 for _ in range(8)]
            check_seq(seq, f"{name} % 64 key={k} seed={s}")

print("Brute-force check complete.")
