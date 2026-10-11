import random

target_prefix = [(2, 6), (7, 0), None, (3, 4), (3, 7), (5, 2), (0, 5), (4, 3)]

order = [
    (0,0),
    (0,1),(1,0),
    (2,0),(1,1),(0,2),
    (0,3),(1,2),(2,1),(3,0),
    (4,0),(3,1),(2,2),(1,3),(0,4),
    (0,5),(1,4),(2,3),(3,2),(4,1),(5,0),
    (6,0),(5,1),(4,2),(3,3),(2,4),(1,5),(0,6),
    (0,7),(1,6),(2,5),(3,4),(4,3),(5,2),(6,1),(7,0),
    (7,1),(6,2),(5,3),(4,4),(3,5),(2,6),(1,7),
    (2,7),(3,6),(4,5),(5,4),(6,3),(7,2),
    (7,3),(6,4),(5,5),(4,6),(3,7),
    (4,7),(5,6),(6,5),(7,4),
    (7,5),(6,6),(5,7),
    (6,7),(7,6),
    (7,7)
]

candidates = {}

# 1. Zigzag ranges:
for start in range(0, 30):
    for end in range(start + 8, 64):
        candidates[f"zz_{start}_{end}"] = order[start:end]

# 2. u + v ranges:
for min_s in range(1, 6):
    for max_s in range(min_s + 1, 14):
        candidates[f"sum_{min_s}_{max_s}"] = [
            (u, v) for u in range(8) for v in range(8) if min_s <= u + v <= max_s
        ]

# 3. No axis (u >= 1, v >= 1):
for min_s in range(2, 6):
    for max_s in range(min_s + 1, 14):
        candidates[f"noaxis_{min_s}_{max_s}"] = [
            (u, v) for u in range(1, 8) for v in range(1, 8) if min_s <= u + v <= max_s
        ]

# 4. Standard OpenStego mid-frequencies:
candidates["openstego_mid"] = [
    (0, 3), (1, 2), (2, 1), (3, 0),
    (0, 4), (1, 3), (2, 2), (3, 1), (4, 0),
    (0, 5), (1, 4), (2, 3), (3, 2), (4, 1), (5, 0),
    (1, 5), (2, 4), (3, 3), (4, 2), (5, 1),
    (3, 4), (4, 3)
]

keys = ["key-bro", "bro", "key_bro", "bro_stego", "key", "stego_hint"]

print(f"Generated {len(candidates)} candidate lists. Testing random.choice...")

found = False
for k in keys:
    for name, clist in candidates.items():
        if len(clist) < 2:
            continue
        random.seed(k)
        seq = [random.choice(clist) for _ in range(8)]
        # Check match with target_prefix:
        match = True
        for t, s in zip(target_prefix, seq):
            if t is not None and t != s:
                match = False
                break
        if match:
            print(f"!!! MATCH FOUND: key='{k}', list='{name}', seq={seq}")
            found = True
            break
    if found:
        break

if not found:
    print("No match found in sweep.")
