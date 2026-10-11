import hashlib, zlib, struct

# Target sequence of (u, v)
target_uv = [
    (2, 6), (7, 0), (0, 6), (3, 4), (3, 7), (5, 2), (0, 5), (4, 3),
    (4, 2), (2, 4), (0, 5), (3, 1), (6, 0), (2, 6), (1, 6), (2, 7)
]
target_idx = [u * 8 + v for u, v in target_uv]

# All standard LCGs:
lcg_params = [
    ("ANSI C / GCC", 1103515245, 12345, 2**31, 16, 0x7FFF),
    ("Borland C", 22695477, 1, 2**32, 16, 0x7FFF),
    ("MSVC", 214013, 2531011, 2**32, 16, 0x7FFF),
    ("Java", 0x5DEECE66D, 0xB, 2**48, 16, 0x7FFFFFFF),
    ("glibc", 1103515245, 12345, 2**31, 0, 2**31 - 1),
    ("POSIX rand48", 0x5DEECE66D, 0xB, 2**48, 0, 2**48 - 1),
    ("Turbo Pascal", 134775813, 1, 2**32, 0, 2**32 - 1),
    ("ZX Spectrum", 75, 0, 65537, 0, 65536),
    ("Numerical Recipes", 1664525, 1013904223, 2**32, 0, 2**32 - 1),
    ("MinGW", 214013, 2531011, 2**32, 16, 0x7FFF),
    ("Delphi", 134775813, 1, 2**32, 0, 2**32 - 1)
]

keys = ["key-bro", "bro", "key_bro", "bro_stego", "key", "stego_hint", "1337", "42"]

print("Searching LCGs...")
for name, a, c, m, shift, mask in lcg_params:
    for k in keys:
        seeds = [
            zlib.crc32(k.encode()),
            sum(k.encode()),
            int.from_bytes(k.encode()[:4], 'little'),
            int.from_bytes(k.encode()[:4], 'big'),
            int(hashlib.md5(k.encode()).hexdigest()[:8], 16),
            int(hashlib.sha256(k.encode()).digest()[:4].hex(), 16)
        ]
        for s in seeds:
            state = s % m
            out_uv = []
            for _ in range(8):
                state = (a * state + c) % m
                val = (state >> shift) & mask
                # Check mod 64
                idx = val % 64
                out_uv.append((idx // 8, idx % 8))
            if out_uv[:4] == target_uv[:4]:
                print(f"!!! MATCH LCG ({name}) k={k} s={s}: {out_uv[:8]}")

print("LCG search finished.")
