#!/usr/bin/env python3
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# =========================================================
# Already verified secrets
# =========================================================
k1 = 103679294682318394632116352245965931281672926926560836357672813757452869481740
k2 = 216894608825153064084224188982807740771782288278332095102457164300855345783429

# C2 parameters recovered from encrypted C2 JSON
p2 = 304732685256240877660545254824778203315272896065737311763863423689411782396127
A2 = 1
B2 = 0

G2x = 113305118657633137168829735832803890548319735139787407710539440768833013717894
G2y = 115366654191285916179579653496826898962967550021959208925921633507591202256276

P2x = 271445483459170488072443917148063230572292331340468548884831886421049081014671
P2y = 47405794374250452027489159873348810051097262050781514973353824851952254142956

# C2 encrypted blob, used to recover exact C2 plaintext JSON
c2_iv = bytes.fromhex("96dd8a4293d3dd5b4d8069c2c47f0f6b")
c2_ct = bytes.fromhex(
    "4da0cfd5b52911ccecff14ccd4f567170f8b4070aa17aa928fd1a57d6db922be"
    "bd21da930e212ec681fb5fb8dbabe20dd9a73362e140f289850c965085637733"
    "8400c260f028976c3fb0925980f87e9a37541086e89761542fd7d0de7a092061"
    "ef8ebddc6b295ce8103b010dfbb43f8f93be9850efd4718f106aa1fee8e1c874"
    "b9c064636633d54c76bd108b549cbbb0bb9f6e0b479110cd603b90ccbf983d72"
    "6e67811f84862e7bfd1872813ba60977dd07d3d2c99a0655d2717ca53ee8b69a"
    "91c9e3e4ae059725101fde94d26ff503a8ec7fe5c858ec7fbbae8db484d3d4a1"
    "4ba29958944daf80d67ff0662f306b48a055139fe178546b9c9b4e35002e5b92"
    "38565d7811007e9004cd43b9cc2ecfdbdc4d10676d20f31948838786299f9f13"
    "6c658167595dbb790ddf42742a34ea676c6c4298fcb555500f4f59065a76d838"
    "2a60d7238dd883b6c5d0d3d124ba17d883609d8cc42136e20b86112e1d817b96"
    "495114f1ba91f69b217da6986b448e177d8bd0b22e6e9c5ae19c4aebca07a967"
    "33f912d96af91627eb12041d2e7a1f101340f66d743320f980c754a8cc5eacd5"
    "24cce09840976fc03d38f0d96c8062a98aeefdaece289e5d8157b19ddd6348d5"
)

# Flag encrypted blob
flag_iv = bytes.fromhex("ef399b2910c055cb1894ce3f8ade3b72")
flag_ct = bytes.fromhex(
    "c4d4a558aa9518172a3327c615815f349fdcd7cb212e8f8b0113046670247741"
    "d5fb3d6c1b4e1ce4f5e8a9cbac1598cd89672fd0e3f99886d434f2c6746ae55b"
    "072a15fa98478d6bd90d8e25cecc6fe8e291131dc83c9e57a3a772bc237b33eb"
    "145ee5ecb27d383134bb3357fcb9be36"
)

# Candidate plaintext found earlier
flag_clean_str = "KubSTU{45_f0r_311ip71c_curv3_g30m37ry_4nd_cryp70gr4phy_1n_g3ner41_1_63l13v3_y0u_w3re_46l3_70_501ve_i7}"
flag_clean = flag_clean_str.encode()
flag_raw = flag_clean + b"\n" * 10

# =========================================================
# Recover exact C2 plaintext JSON
# =========================================================
key_c2 = hashlib.sha256(b"C1->C2:" + str(k1).encode()).digest()
pt_c2 = AES.new(key_c2, AES.MODE_CBC, c2_iv).decrypt(c2_ct)
pad_len = pt_c2[-1]
if not (1 <= pad_len <= 16 and all(x == pad_len for x in pt_c2[-pad_len:])):
    raise SystemExit("[-] C2 padding invalid, something is wrong")
c2_plain = pt_c2[:-pad_len]

print("[+] C2 plaintext recovered")
print(c2_plain[:120], b"...")

# =========================================================
# Helpers
# =========================================================
def dedup_bytes(seq):
    seen = set()
    out = []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out

def int_forms(n):
    """
    Generate realistic byte representations of an integer.
    """
    n = int(n)
    forms = []

    forms.append(str(n).encode())
    forms.append(hex(n).encode())
    forms.append(hex(n)[2:].encode())
    forms.append(hex(n)[2:].upper().encode())

    bitlen = n.bit_length()
    min_len = max(1, (bitlen + 7) // 8)

    lengths = sorted({min_len, 32, 33, 40, 64})
    for L in lengths:
        if bitlen <= L * 8:
            b = n.to_bytes(L, "big")
            forms.append(b)
            forms.append(b[::-1])

    # lower 256 bits, often used by lazy implementations
    low = n & ((1 << 256) - 1)
    b32 = low.to_bytes(32, "big")
    forms.append(b32)
    forms.append(b32[::-1])

    # base64 of minimal big-endian encoding
    try:
        mb = n.to_bytes(min_len, "big")
        forms.append(base64.b64encode(mb))
        forms.append(base64.b64encode(mb).lower())
    except Exception:
        pass

    return dedup_bytes(forms)

def derive_keys(mat):
    """
    Given raw key material, yield possible AES keys.
    """
    out = []

    h = hashlib.sha256(mat).digest()
    out.append((h, "sha256(material)"))

    hx = hashlib.sha256(mat).hexdigest().encode()
    out.append((hx[:32], "sha256_hex(material)[:32]"))
    out.append((hx[:16], "sha256_hex(material)[:16]"))
    out.append((hx[:24], "sha256_hex(material)[:24]"))

    if len(mat) in (16, 24, 32):
        out.append((mat, "raw material"))

    m = hashlib.md5(mat).digest()
    out.append((m, "md5(material)"))

    s512 = hashlib.sha512(mat).digest()
    out.append((s512[:32], "sha512(material)[:32]"))
    out.append((s512[:16], "sha512(material)[:16]"))
    out.append((s512[:24], "sha512(material)[:24]"))

    return dedup_bytes_list(out)

def dedup_bytes_list(seq):
    seen = set()
    out = []
    for item in seq:
        key = item[0]
        if key not in seen:
            seen.add(key)
            out.append(item)
    return out

# =========================================================
# Build secret byte candidates
# =========================================================
secret_items = []

for label, value in [
    ("k1", k1),
    ("k2", k2),
    ("p2", p2),
    ("G2x", G2x),
    ("G2y", G2y),
    ("P2x", P2x),
    ("P2y", P2y),
]:
    for i, b in enumerate(int_forms(value)):
        secret_items.append((f"{label}[{i}]", b))

secret_items.append(("key_c2", key_c2))
secret_items.append(("key_c2_hex", key_c2.hex().encode()))
secret_items.append(("key_c2_hex_upper", key_c2.hex().upper().encode()))
secret_items.append(("c2_plain", c2_plain))
secret_items.append(("sha256_c2_plain", hashlib.sha256(c2_plain).digest()))
secret_items.append(("sha256_c2_plain_hex", hashlib.sha256(c2_plain).hexdigest().encode()))

# =========================================================
# Prefixes / separators / suffixes
# =========================================================
prefixes = [
    b"",
    b"flag:",
    b"FLAG:",
    b"Flag:",
    b"flag",
    b"flag{",
    b"k1:",
    b"k2:",
    b"k3:",
    b"k1=",
    b"k2=",
    b"key:",
    b"key",
    b"secret:",
    b"secret",
    b"password:",
    b"pass:",
    b"KubSTU:",
    b"KubSTU",
    b"kubstu:",
    b"kubstu",
    b"Curve Ball:",
    b"Curve Ball",
    b"curve_ball:",
    b"C1->C2:",
    b"C1->c2:",
    b"C2->flag:",
    b"C2->FLAG:",
    b"c2->flag:",
    b"C2->flag",
    b"C2->flag: ",
    b"C1->flag:",
    b"C1->flag",
    b"C3->flag:",
    b"C3->FLAG:",
    b"c3->flag:",
    b"C3->flag",
    b"C2->C3:",
    b"C1->C2->flag:",
]

suffixes = [
    b"",
    b":flag",
    b"->flag",
    b"flag",
]

separators = [
    b"",
    b":",
    b"|",
    b"-",
    b"_",
    b",",
    b";",
    b" ",
    b"->",
    b"=>",
    b"\n",
]

# =========================================================
# Materials: single secret with prefix/suffix
# =========================================================
materials = []

for pre in prefixes:
    for label, sec in secret_items:
        materials.append((f"{pre!r} + {label}", pre + sec))
        materials.append((f"{label} + {pre!r}", sec + pre))

for suf in suffixes:
    if suf == b"":
        continue
    for label, sec in secret_items:
        materials.append((f"{label} + {suf!r}", sec + suf))
        materials.append((f"{suf!r} + {label}", suf + sec))

# =========================================================
# Materials: pairs, mostly k1/k2/digest/c2_plain
# =========================================================
pair_label_filter = {
    "k1",
    "k2",
    "key_c2",
    "key_c2_hex",
    "c2_plain",
    "sha256_c2_plain",
    "P2x",
    "P2y",
    "G2x",
    "G2y",
}

pair_items = [(label, b) for label, b in secret_items if label.split("[")[0] in pair_label_filter]

pair_prefixes = [
    b"",
    b"flag:",
    b"k2:",
    b"C2->flag:",
    b"C1->C2->flag:",
    b"KubSTU:",
    b"secret:",
    b"key:",
]

for pre in pair_prefixes:
    for lab1, b1 in pair_items:
        for lab2, b2 in pair_items:
            if lab1 == lab2:
                continue
            for sep in separators:
                for suf in suffixes:
                    mat = pre + b1 + sep + b2 + suf
                    materials.append((f"{pre!r}+{lab1}+{sep!r}+{lab2}+{suf!r}", mat))

# Deduplicate materials by bytes, keep first description
seen_mat = set()
unique_materials = []
for desc, mat in materials:
    if mat not in seen_mat:
        seen_mat.add(mat)
        unique_materials.append((desc, mat))

materials = unique_materials
print(f"[*] Generated {len(materials)} key materials")

# =========================================================
# Plaintext candidates
# =========================================================
plaintext_candidates = [
    ("raw_with_10_newlines", flag_raw),
    ("pkcs7_clean", pad(flag_clean, 16)),
    ("zero_padded_clean", flag_clean + b"\x00" * (112 - len(flag_clean))),
    ("space_padded_clean", flag_clean + b" " * (112 - len(flag_clean))),
    ("newline_padded_clean", flag_clean + b"\n" * (112 - len(flag_clean))),
]

iv_candidates = [
    ("flag_iv", flag_iv),
    ("c2_iv", c2_iv),
    ("zero_iv", b"\x00" * 16),
]

# =========================================================
# Checker
# =========================================================
def test_key(key, desc, mat, key_mode):
    # CBC with different IVs
    for iv_name, iv in iv_candidates:
        try:
            pt = AES.new(key, AES.MODE_CBC, iv).decrypt(flag_ct)
        except Exception:
            continue

        if pt == flag_raw:
            print()
            print("[+] EXACT MATCH: raw plaintext with 10 newline padding bytes")
            print(f"    material desc = {desc}")
            print(f"    material repr = {mat!r}")
            print(f"    material hex  = {mat.hex()}")
            print(f"    key mode      = {key_mode}")
            print(f"    key hex       = {key.hex()}")
            print(f"    IV            = {iv_name} ({iv.hex()})")
            print(f"    mode          = AES-CBC")
            print()
            print(flag_clean_str)
            return True

        if pt.startswith(flag_clean):
            print()
            print("[+] PARTIAL MATCH: plaintext starts with candidate flag")
            print(f"    material desc = {desc}")
            print(f"    material repr = {mat!r}")
            print(f"    material hex  = {mat.hex()}")
            print(f"    key mode      = {key_mode}")
            print(f"    key hex       = {key.hex()}")
            print(f"    IV            = {iv_name} ({iv.hex()})")
            print(f"    raw pt repr   = {pt!r}")
            print()
            print(flag_clean_str)
            return True

        # If some other readable plaintext appears, show it too
        try:
            txt = pt.decode("utf-8")
            if txt.isprintable() and len(txt) > 20:
                print()
                print("[!] Readable plaintext found, but not the expected flag")
                print(f"    material desc = {desc}")
                print(f"    key mode      = {key_mode}")
                print(f"    key hex       = {key.hex()}")
                print(f"    IV            = {iv_name}")
                print(f"    text          = {txt}")
        except Exception:
            pass

    # ECB fallback
    try:
        pt = AES.new(key, AES.MODE_ECB).decrypt(flag_ct)
        if pt == flag_raw or pt.startswith(flag_clean):
            print()
            print("[+] MATCH in AES-ECB")
            print(f"    material desc = {desc}")
            print(f"    key mode      = {key_mode}")
            print(f"    key hex       = {key.hex()}")
            print(f"    raw pt repr   = {pt!r}")
            print()
            print(flag_clean_str)
            return True
    except Exception:
        pass

    return False

# =========================================================
# First test very explicit high-priority candidates
# =========================================================
explicit = [
    (b"C2->flag:" + str(k2).encode(), "C2->flag: + str(k2)"),
    (b"C2->flag:" + hex(k2).encode(), "C2->flag: + hex(k2)"),
    (b"C2->flag:" + hex(k2)[2:].encode(), "C2->flag: + hex(k2)[2:]"),
    (b"flag:" + str(k2).encode(), "flag: + str(k2)"),
    (str(k2).encode(), "str(k2)"),
    (hex(k2).encode(), "hex(k2)"),
    (hex(k2)[2:].encode(), "hex(k2)[2:]"),
    (b"C1->flag:" + str(k1).encode(), "C1->flag: + str(k1)"),
    (b"C2->C3:" + str(k2).encode(), "C2->C3: + str(k2)"),
    (b"C2->flag:" + k2.to_bytes(33, "big"), "C2->flag: + k2 33-byte big endian"),
    (b"C2->flag:" + (k2 & ((1 << 256) - 1)).to_bytes(32, "big"), "C2->flag: + lower 32 bytes of k2"),
]

print("[*] Testing explicit high-priority candidates...")
for mat, desc in explicit:
    for key, key_mode in derive_keys(mat):
        if test_key(key, desc, mat, key_mode):
            raise SystemExit(0)

print("[*] Testing generated materials...")
for desc, mat in materials:
    for key, key_mode in derive_keys(mat):
        if test_key(key, desc, mat, key_mode):
            raise SystemExit(0)

print()
print("[-] Exact derivation for this plaintext was not found in the searched space.")
print("    This means one of the following:")
print("    1) The plaintext is a decoy, and real flag needs k3 from C3.")
print("    2) The key derivation is outside this search space.")
print("    3) The challenge instance on the platform does not match this challenge.txt.")