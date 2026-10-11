import random
import numpy as np
import zlib
import hashlib

# Target sequence of first 10 blocks:
target = [(2, 6), (7, 0), (0, 4), (3, 4), (3, 7), (5, 2), (0, 5), (4, 3), (3, 0), (2, 4)]
print("Target:", target)

# Keys to test
keys = [
    "key-bro", "bro", "key_bro", "bro_stego", "bro_stego_with_hint", "stego_hint",
    "key", "factory", "zavod", "kubstu", "kubstu_ctf"
]

seeds = []
for k in keys:
    seeds.append(("str", k))
    try:
        seeds.append(("hash", hash(k)))
    except:
        pass
    seeds.append(("crc32", zlib.crc32(k.encode())))
    seeds.append(("int_be", int.from_bytes(k.encode(), 'big')))
    seeds.append(("int_le", int.from_bytes(k.encode(), 'little')))
    seeds.append(("md5_int", int(hashlib.md5(k.encode()).hexdigest()[:8], 16)))
    seeds.append(("sha1_int", int(hashlib.sha1(k.encode()).hexdigest()[:8], 16)))
    # sum of ascii
    seeds.append(("sum_ascii", sum(k.encode())))

# Also test small integer seeds (0 to 100000) just in case!
# But first test the key-derived seeds

print(f"Testing {len(seeds)} key-derived seeds...")

def test_match(seq_gen, name, seed_desc):
    try:
        for i in range(len(target)):
            val = next(seq_gen)
            if val != target[i]:
                return False
        print(f"!!! MATCH FOUND !!! Generator: {name}, Seed: {seed_desc}")
        return True
    except:
        return False

found = False
for desc, s in seeds:
    # 1. python random.randint(0, 7)
    try:
        random.seed(s)
        gen = ((random.randint(0, 7), random.randint(0, 7)) for _ in range(20))
        if test_match(gen, "random.randint(0, 7)", f"{desc}:{s}"): found = True
    except: pass

    # 1b. python random.randint(0, 7) reversed
    try:
        random.seed(s)
        gen = ((v, u) for u, v in ((random.randint(0, 7), random.randint(0, 7)) for _ in range(20)))
        if test_match(gen, "random.randint(0, 7) reversed", f"{desc}:{s}"): found = True
    except: pass

    # 2. python random.randrange(8)
    try:
        random.seed(s)
        gen = ((random.randrange(8), random.randrange(8)) for _ in range(20))
        if test_match(gen, "random.randrange(8)", f"{desc}:{s}"): found = True
    except: pass

    # 3. divmod(random.randint(0, 63), 8)
    try:
        random.seed(s)
        gen = (divmod(random.randint(0, 63), 8) for _ in range(20))
        if test_match(gen, "divmod(random.randint(0, 63), 8)", f"{desc}:{s}"): found = True
    except: pass

    # 3b. divmod reversed
    try:
        random.seed(s)
        gen = ((v, u) for u, v in (divmod(random.randint(0, 63), 8) for _ in range(20)))
        if test_match(gen, "divmod(randint) reversed", f"{desc}:{s}"): found = True
    except: pass

    # 4. numpy RandomState
    if isinstance(s, int) and 0 <= s < 2**32:
        try:
            rs = np.random.RandomState(s)
            u_arr = rs.randint(0, 8, size=20)
            v_arr = rs.randint(0, 8, size=20)
            gen = zip(u_arr, v_arr)
            if test_match(gen, "np.random.RandomState.randint(0, 8)", f"{desc}:{s}"): found = True
        except: pass

        try:
            rs = np.random.RandomState(s)
            idx_arr = rs.randint(0, 64, size=20)
            gen = (divmod(idx, 8) for idx in idx_arr)
            if test_match(gen, "np.random.RandomState divmod", f"{desc}:{s}"): found = True
        except: pass

if not found:
    print("No direct key-derived match. Testing small integer seeds 0..50000...")
    for s in range(50000):
        random.seed(s)
        gen = ((random.randint(0, 7), random.randint(0, 7)) for _ in range(5))
        if next(gen) == target[0] and next(gen) == target[1]:
            if test_match(gen, "random.randint(0, 7)", f"int:{s}"):
                found = True
                break
        
        # divmod(randint)
        random.seed(s)
        gen = (divmod(random.randint(0, 63), 8) for _ in range(5))
        if next(gen) == target[0] and next(gen) == target[1]:
            if test_match(gen, "divmod", f"int:{s}"):
                found = True
                break

if not found:
    print("Done search.")
