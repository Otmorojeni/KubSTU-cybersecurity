import base64
import codecs
import io
import os
import zipfile


def solve():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    level02_path = os.path.join(base_dir, "level02.zip")

    # Layer 1: The comment from level01 (found in the original matryoshka.zip archive)
    pwd_level02 = b"5ox5iae8pv05"
    print(f"[Layer 1 -> 2] Password for level02.zip: {pwd_level02.decode()}")

    # Layer 2
    with zipfile.ZipFile(level02_path) as z2:
        z2.setpassword(pwd_level02)
        pwd_level03 = base64.b64decode(z2.comment)
        print(f"[Layer 2 -> 3] Comment (Base64): {z2.comment.decode()} -> Password: {pwd_level03.decode()}")
        l3_data = z2.read("level03.zip")

    # Layer 3
    z3 = zipfile.ZipFile(io.BytesIO(l3_data))
    z3.setpassword(pwd_level03)
    pwd_level04 = bytes.fromhex(z3.comment.decode())
    print(f"[Layer 3 -> 4] Comment (Hex): {z3.comment.decode()} -> Password: {pwd_level04.decode()}")
    l4_data = z3.read("level04.zip")

    # Layer 4
    z4 = zipfile.ZipFile(io.BytesIO(l4_data))
    z4.setpassword(pwd_level04)
    pwd_level05 = codecs.decode(z4.comment.decode(), "rot_13").encode()
    print(f"[Layer 4 -> 5] Comment (ROT13): {z4.comment.decode()} -> Password: {pwd_level05.decode()}")
    l5_data = z4.read("level05.zip")

    # Layer 5
    z5 = zipfile.ZipFile(io.BytesIO(l5_data))
    z5.setpassword(pwd_level05)
    note_lines = z5.read("note.txt").decode().strip().splitlines()
    pwd_level06 = note_lines[-1].strip().encode()
    print(f"[Layer 5 -> 6] Found in note.txt -> Password: {pwd_level06.decode()}")
    l6_data = z5.read("level06.zip")

    # Layer 6
    z6 = zipfile.ZipFile(io.BytesIO(l6_data))
    z6.setpassword(pwd_level06)
    pwd_level07 = z6.comment.decode()[::-1].encode()
    print(f"[Layer 6 -> 7] Comment (Reversed): {z6.comment.decode()} -> Password: {pwd_level07.decode()}")
    l7_data = z6.read("level07.zip")

    # Layer 7
    z7 = zipfile.ZipFile(io.BytesIO(l7_data))
    z7.setpassword(pwd_level07)
    pwd_level08 = "".join(chr(int(x)) for x in z7.comment.decode().split()).encode()
    print(f"[Layer 7 -> 8] Comment (Decimal ASCII): {z7.comment.decode()} -> Password: {pwd_level08.decode()}")
    l8_data = z7.read("level08.zip")

    # Layer 8
    z8 = zipfile.ZipFile(io.BytesIO(l8_data))
    z8.setpassword(pwd_level08)
    candidates = [c.strip().encode() for c in z8.read("candidates.txt").decode().strip().splitlines()]
    l9_data = z8.read("level09.zip")
    pwd_level09 = None
    for cand in candidates:
        try:
            test_z = zipfile.ZipFile(io.BytesIO(l9_data))
            test_z.setpassword(cand)
            test_z.read(test_z.namelist()[0])
            pwd_level09 = cand
            break
        except Exception:
            continue
    print(f"[Layer 8 -> 9] Candidates tested -> Working Password: {pwd_level09.decode()}")

    # Layer 9
    z9 = zipfile.ZipFile(io.BytesIO(l9_data))
    z9.setpassword(pwd_level09)
    pwd_level10 = base64.b32decode(z9.comment)
    print(f"[Layer 9 -> 10] Comment (Base32): {z9.comment.decode()} -> Password: {pwd_level10.decode()}")
    l10_data = z9.read("level10.zip")

    # Layer 10
    z10 = zipfile.ZipFile(io.BytesIO(l10_data))
    z10.setpassword(pwd_level10)
    flag = z10.read("flag.txt").decode().strip()
    print(f"\n[Layer 10] FLAG: {flag}")
    return flag


if __name__ == "__main__":
    solve()
