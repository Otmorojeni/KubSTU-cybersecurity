import hashlib
import hmac
import struct

target = [(2, 6), (7, 0), None, (3, 4), (3, 7), (5, 2), (0, 5), (4, 3)]
# Block 2 could be (0, 6), (6, 0), (0, 4), (5, 0)

keys = ["key-bro", "bro", "key_bro", "bro_stego", "key", "stego_hint"]

def test_match(seq_gen, name):
    seq = [seq_gen(i) for i in range(8)]
    # Check if matches target where not None
    m = True
    for t, s in zip(target, seq):
        if t is not None and t != s:
            m = False
            break
    if m:
        print(f"!!! MATCH FOUND: {name} -> {seq}")
        return True
    
    # Also check transposed
    m_tr = True
    for t, s in zip(target, seq):
        if t is not None and (t[1], t[0]) != s:
            m_tr = False
            break
    if m_tr:
        print(f"!!! MATCH FOUND (transposed): {name} -> {seq}")
        return True
    return False

print("Testing Hash-based PRNGs...")

for k in keys:
    # 1. md5(key + str(i))
    for hname in ['md5', 'sha1', 'sha256']:
        hfn = getattr(hashlib, hname)
        
        # Test direct (u, v) from first 2 bytes or 1 byte
        for sep in ['', '_', '-', ':', ' ']:
            # u = b0 % 8, v = b1 % 8
            test_match(lambda i, sep=sep, hfn=hfn, k=k: (
                hfn(f"{k}{sep}{i}".encode()).digest()[0] % 8,
                hfn(f"{k}{sep}{i}".encode()).digest()[1] % 8
            ), f"{hname}('{k}{sep}{{i}}') % 8")
            
            # u = b0 // 8, v = b0 % 8
            test_match(lambda i, sep=sep, hfn=hfn, k=k: (
                (hfn(f"{k}{sep}{i}".encode()).digest()[0] % 64) // 8,
                (hfn(f"{k}{sep}{i}".encode()).digest()[0] % 64) % 8
            ), f"{hname}('{k}{sep}{{i}}') % 64")

            # struct.pack i
            for fmt in ['<I', '>I', '<H', '>H', 'B']:
                try:
                    test_match(lambda i, fmt=fmt, hfn=hfn, k=k: (
                        hfn(k.encode() + struct.pack(fmt, i)).digest()[0] % 8,
                        hfn(k.encode() + struct.pack(fmt, i)).digest()[1] % 8
                    ), f"{hname}(key + pack({fmt}))")
                except:
                    pass

print("Hash tests done.")
