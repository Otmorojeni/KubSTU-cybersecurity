import random

observed = [
    (2, 6), (7, 0), (0, 4), (3, 4), (3, 7),
    (5, 2), (0, 5), (4, 3), (3, 0), (2, 4),
    (0, 5), (2, 0), (6, 2), (2, 6), (1, 6), (2, 7)
]

print("Observed first 10:", observed[:10])

# Collect all (u, v) that ever appear in our observed set
all_observed_set = set(observed)
print("Observed set:", all_observed_set)

# Let's generate different candidate lists of frequencies:
candidate_lists = {}

# 1. All frequencies except (0,0)
candidate_lists["all_except_dc"] = [(u, v) for u in range(8) for v in range(8) if (u, v) != (0, 0)]

# 2. All frequencies except top-left (u+v <= 1 or 2)
for min_sum in [1, 2, 3]:
    for max_sum in [6, 7, 8, 9, 10, 14]:
        candidate_lists[f"sum_{min_sum}_{max_sum}"] = [
            (u, v) for u in range(8) for v in range(8) if min_sum <= u + v <= max_sum
        ]

# 3. Zig-zag indices range: e.g. zz from 1..63 or 5..50
from check_zigzag import get_zigzag_matrix
zz = get_zigzag_matrix()
for zz_min in [1, 2, 3, 5, 10]:
    for zz_max in [30, 40, 50, 60, 63]:
        candidate_lists[f"zz_{zz_min}_{zz_max}"] = [
            (u, v) for u in range(8) for v in range(8) if zz_min <= zz[u, v] <= zz_max
        ]

# 4. Standard 8x8 mid-frequency coordinates often cited in literature:
# e.g. [(u,v) for u,v in ... if u+v in [3,4,5,6,7]]
# 5. Exactly the unique observed frequencies:
candidate_lists["observed_unique"] = sorted(list(all_observed_set))

seeds = [
    "key-bro", "bro", "key_bro", "bro_stego", "bro_stego_with_hint",
    "key", "kubstu", "kubstu_ctf", "zavod"
]

found = False
for s in seeds:
    for name, flist in candidate_lists.items():
        # Test random.choice
        random.seed(s)
        try:
            gen = [random.choice(flist) for _ in range(len(observed))]
            if gen[:4] == observed[:4]:
                print(f"MATCH! seed={s}, list={name}, method=random.choice")
                found = True
        except:
            pass

if not found:
    print("No simple random.choice match found.")
