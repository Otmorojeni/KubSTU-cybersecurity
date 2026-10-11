import random
import itertools

target_freqs = [
    (2, 6), (7, 0), (0, 4), (3, 4), (3, 7),
    (5, 2), (0, 5), (4, 3), (3, 0), (2, 4),
    (0, 5), (2, 0), (6, 2), (2, 6), (1, 6), (2, 7)
]

print("Target freqs (16):", target_freqs)

# Possible keys:
keys = [
    "key-bro", "bro", "key_bro", "bro_stego", "bro_stego_with_hint", "stego_hint",
    "key", "kubstu", "kubstu_ctf", "kubstu{", "factory", "zavod"
]

# Let's also test integer seeds (like crc32, hash, etc.)
seeds = []
for k in keys:
    seeds.append((f"str:{k}", k))
    try:
        seeds.append((f"hash:{k}", hash(k)))
    except:
        pass
    import zlib
    seeds.append((f"crc32:{k}", zlib.crc32(k.encode())))

# Let's test different generation patterns:
# Pattern 1: (random.randint(0, 7), random.randint(0, 7))
# Pattern 2: (random.randrange(8), random.randrange(8))
# Pattern 3: divmod(random.randint(0, 63), 8) or divmod(random.randrange(64), 8)
# Pattern 4: random.choice from mid-freq list
# Pattern 5: (random.randint(a, b), random.randint(c, d))
# Pattern 6: random.sample ...

found = False
for desc, s in seeds:
    # Pattern 1: randint(0, 7), randint(0, 7)
    random.seed(s)
    seq = [(random.randint(0, 7), random.randint(0, 7)) for _ in range(16)]
    if seq[:5] == target_freqs[:5]:
        print(f"MATCH! seed={desc}, pattern=randint(0,7), randint(0,7)")
        found = True

    # Pattern 1b: randint(0, 7) with reversed u, v
    random.seed(s)
    seq = [(v, u) for u, v in [(random.randint(0, 7), random.randint(0, 7)) for _ in range(16)]]
    if seq[:5] == target_freqs[:5]:
        print(f"MATCH! seed={desc}, pattern=randint(0,7) reversed")
        found = True

    # Pattern 2: divmod(randint(0, 63), 8)
    random.seed(s)
    seq = [divmod(random.randint(0, 63), 8) for _ in range(16)]
    if seq[:5] == target_freqs[:5]:
        print(f"MATCH! seed={desc}, pattern=divmod(randint(0,63), 8)")
        found = True

    # Pattern 3: divmod(randrange(64), 8)
    random.seed(s)
    seq = [divmod(random.randrange(64), 8) for _ in range(16)]
    if seq[:5] == target_freqs[:5]:
        print(f"MATCH! seed={desc}, pattern=divmod(randrange(64), 8)")
        found = True

if not found:
    print("Direct pattern not matched in simple seeds, let's test more patterns/candidates.")
