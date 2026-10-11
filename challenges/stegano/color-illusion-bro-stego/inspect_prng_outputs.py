import random

random.seed("key-bro")
# What if random generated 100 pairs of (u, v)?
pairs = [(random.randint(0, 7), random.randint(0, 7)) for _ in range(200)]
print("First 20 pairs of randint(0, 7):", pairs[:20])

# What if random generated integers in range(64)?
random.seed("key-bro")
nums64 = [random.randint(0, 63) for _ in range(20)]
print("First 20 randint(0, 63):", nums64)

# What if random generated integers in range(25600)?
random.seed("key-bro")
blocks = [random.randint(0, 25599) for _ in range(20)]
print("First 20 block indices:", blocks)

# What if random.sample(range(25600), ...)?
random.seed("key-bro")
sample_blocks = random.sample(range(25600), 20)
print("First 20 sample blocks:", sample_blocks)
