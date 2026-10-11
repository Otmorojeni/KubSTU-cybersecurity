import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from PIL import Image
import numpy as np
from scipy import ndimage
from collections import Counter
import random
import os

p = 4003
N = 30
eta = 1

def recover_terminal_curve(image_path: str) -> tuple[int, int]:
    """Recovers (a_N, b_N) from the noisy curve.png using RANSAC / pair voting."""
    im = Image.open(image_path)
    arr = (np.array(im) == 0)

    labeled, num_features = ndimage.label(arr)
    slices = ndimage.find_objects(labeled)

    pts = []
    for s in slices:
        if arr[s].shape == (3, 3):
            cy = s[0].start + 1
            cx = s[1].start + 1
            pts.append((cx, cy))

    pair_counts = Counter()
    random.seed(42)
    n = len(pts)
    for _ in range(5000):
        i, j = random.sample(range(n), 2)
        x1, y1 = pts[i]
        x2, y2 = pts[j]
        dx = (x1 - x2) % p
        if dx == 0:
            continue
        dy = ((y1**2 - x1**3) - (y2**2 - x2**3)) % p
        a = (dy * pow(dx, -1, p)) % p
        b = (y1**2 - x1**3 - a * x1) % p
        pair_counts[(a, b)] += 1

    (a_N, b_N), _ = pair_counts.most_common(1)[0]
    return a_N, b_N

def ricci_step(a: int, b: int) -> tuple[int, int]:
    K = (4 * pow(a, 3, p) + 27 * pow(b, 2, p)) % p
    a_new = (a - 12 * eta * pow(a, 2, p) * K) % p
    b_new = (b - 54 * eta * b * K) % p
    return a_new, b_new

def invert_cascade(a_target: int, b_target: int, depth: int = 30) -> set[tuple[int, int]]:
    inv24 = pow(24, -1, p)
    inv_table = [0] + [pow(i, -1, p) for i in range(1, p)]
    sqrt_table = {}
    for i in range(p):
        sq = (i * i) % p
        if sq not in sqrt_table:
            sqrt_table[sq] = i

    def invert_step(a_cur: int, b_cur: int) -> list[tuple[int, int]]:
        preimages = []
        if (4 * pow(a_cur, 3, p) + 27 * pow(b_cur, 2, p)) % p == 0:
            preimages.append((a_cur, b_cur))

        for K in range(1, p):
            denom_b = (1 - 54 * K) % p
            if denom_b == 0:
                continue
            b = (b_cur * inv_table[denom_b]) % p

            disc = (1 - 48 * K * a_cur) % p
            if disc not in sqrt_table:
                continue
            sqrt_disc = sqrt_table[disc]
            inv_24K = (inv24 * inv_table[K]) % p

            a_cand1 = ((1 + sqrt_disc) * inv_24K) % p
            if (4 * pow(a_cand1, 3, p) + 27 * pow(b, 2, p)) % p == K:
                if ricci_step(a_cand1, b) == (a_cur, b_cur):
                    preimages.append((a_cand1, b))

            if sqrt_disc != 0:
                a_cand2 = ((1 - sqrt_disc) * inv_24K) % p
                if (4 * pow(a_cand2, 3, p) + 27 * pow(b, 2, p)) % p == K:
                    if ricci_step(a_cand2, b) == (a_cur, b_cur):
                        preimages.append((a_cand2, b))

        return list(set(preimages))

    current = {(a_target, b_target)}
    for step in range(1, depth + 1):
        next_level = set()
        for pt in current:
            for pre in invert_step(*pt):
                next_level.add(pre)
        current = next_level

    return current

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(base_dir, "What do you know about Perelman", "curve.png")
    if not os.path.exists(img_path):
        img_path = os.path.join(base_dir, "curve.png")

    print("[*] Identifying terminal curve (a_N, b_N)...")
    a_N, b_N = recover_terminal_curve(img_path)
    print(f"[+] Found terminal curve: a_{N} = {a_N}, b_{N} = {b_N}")

    print(f"[*] Inverting Ricci flow {N} steps backwards...")
    candidates = invert_cascade(a_N, b_N, depth=N)
    print(f"[+] Found {len(candidates)} candidate (a_0, b_0) pairs")

    iv = bytes.fromhex("abdbe020fcdadc18a039b090e837c10f")
    ct = bytes.fromhex(
        "ad6190e8d4447e45a9b06e2c182eff8329d14ee0df89ed5e84754c46e93bb2c7"
        "aaff0e43ab8ccb0e8c6f813da6131e40acef2b96676a8ca4ef72878748bbdb0b"
        "12271a06e3688dfd349f745f3874ebd26930cb3103ad1acc6a74339dd3d96f7b"
        "eed461ce5721bfa0b9f7f8422fd90857"
    )

    print("[*] Decrypting ciphertext with candidates...")
    for a0, b0 in candidates:
        pwd = a0.to_bytes(4, "big") + b0.to_bytes(4, "big")
        key = hashlib.scrypt(
            pwd, salt=b"perelman/ricci/v2", n=65536, r=8, p=1, dklen=32, maxmem=128 * 1024 * 1024
        )
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = cipher.decrypt(ct)
        try:
            pt_unpadded = unpad(pt, 16)
            flag = pt_unpadded.decode("utf-8")
            print(f"\n[+] SUCCESS!")
            print(f"[*] Initial curve: a_0 = {a0}, b_0 = {b0}")
            print(f"[*] Flag: {flag}")
            break
        except Exception:
            continue

if __name__ == "__main__":
    main()
