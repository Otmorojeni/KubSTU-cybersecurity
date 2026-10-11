from Crypto.Cipher import AES, ARC4
from hashlib import sha256, md5
import random
import itertools

keys_str = ["key-bro", "bro", "key_bro", "bro_stego", "bro_stego_with_hint", "stego_hint"]

files = [
    ('row_msb', 'extracted_row_msb.bin'),
    ('row_lsb', 'extracted_row_lsb.bin'),
    ('col_msb', 'extracted_col_msb.bin'),
    ('col_lsb', 'extracted_col_lsb.bin'),
]

found = False

for fname, fpath in files:
    with open(fpath, 'rb') as f:
        data = f.read()
    
    # Also test inverted data
    data_inv = bytes(b ^ 0xff for b in data)
    
    for d, is_inv in [(data, False), (data_inv, True)]:
        # 1. Check raw data
        if b'kubstu' in d.lower() or b'ctf' in d.lower() or b'flag' in d.lower():
            print(f"RAW MATCH in {fname} (inv={is_inv})!")
            found = True
            
        for k in keys_str:
            kb = k.encode()
            # 2. XOR repeating key
            xored = bytes(b ^ kb[i % len(kb)] for i, b in enumerate(d))
            if b'kubstu' in xored.lower() or b'flag' in xored.lower():
                print(f"XOR MATCH with key '{k}' in {fname} (inv={is_inv})!")
                print("Text:", xored[:200])
                found = True

            # 3. RC4
            try:
                rc4 = ARC4.new(kb).decrypt(d)
                if b'kubstu' in rc4.lower() or b'flag' in rc4.lower():
                    print(f"RC4 MATCH with key '{k}' in {fname} (inv={is_inv})!")
                    print("Text:", rc4[:200])
                    found = True
            except:
                pass

            # 4. XOR with random stream (random.randint(0, 255))
            for seed in [k, hash(k)]:
                try:
                    random.seed(seed)
                    stream = bytes(random.randint(0, 255) for _ in range(len(d)))
                    prng_xor = bytes(b1 ^ b2 for b1, b2 in zip(d, stream))
                    if b'kubstu' in prng_xor.lower() or b'flag' in prng_xor.lower():
                        print(f"PRNG XOR MATCH with seed '{seed}' in {fname} (inv={is_inv})!")
                        print("Text:", prng_xor[:200])
                        found = True
                except:
                    pass

            # 5. AES ECB
            for h in [sha256(kb).digest()[:16], md5(kb).digest(), kb.ljust(16, b'\0')[:16]]:
                try:
                    cipher = AES.new(h, AES.MODE_ECB)
                    dec = cipher.decrypt(d)
                    if b'kubstu' in dec.lower() or b'flag' in dec.lower():
                        print(f"AES ECB MATCH with key '{k}' in {fname} (inv={is_inv})!")
                        print("Text:", dec[:200])
                        found = True
                except:
                    pass

if not found:
    print("No simple stream/cipher match found on full 3200 bytes.")
