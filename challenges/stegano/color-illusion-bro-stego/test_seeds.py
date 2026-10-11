import random

for seed in ["key-bro", "bro", "key_bro", "bro_stego"]:
    print(f"\n--- Testing seed: '{seed}' ---")
    random.seed(seed)
    # What could it generate?
    # 1. A pair of frequencies (u, v)?
    freqs = [(random.randint(0, 7), random.randint(0, 7)) for _ in range(10)]
    print("random (u, v) pairs:", freqs)
    
    # 2. Or sample from 8x8 = 64 frequencies?
    random.seed(seed)
    sample_freqs = random.sample(range(64), 10)
    print("sample freqs (divmod 8):", [(f // 8, f % 8) for f in sample_freqs])
    
    # 3. Or permutation of blocks?
    random.seed(seed)
    blocks_perm = random.sample(range(160 * 160), 10)
    print("first 10 block indices:", blocks_perm)
