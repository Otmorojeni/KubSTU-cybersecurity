#!/usr/bin/env python3
"""
KubSTU CTF 2026 - Solution for "Вычислительная система с сокращённым набором команд"
Architecture: RISC-V (RV32I) Firmware Analysis & Emulation / Reversal
"""

import struct

def solve():
    with open("fw.bin", "rb") as f:
        data = f.read()

    print("[*] Stage 1: Firmware Unpacker (RV32I)")
    # 1. Stage 1 integrity hash over the bootloader (0x0000 - 0x00dc)
    a5 = 0x811c9dc5  # FNV-1a offset basis
    prime = 0x01000193  # FNV-1a 32-bit prime

    for offset in range(0, 0xdc, 4):
        w = struct.unpack("<I", data[offset:offset+4])[0]
        a5 = (a5 ^ w) & 0xffffffff
        a5 = (a5 * prime) & 0xffffffff
        a6 = (a5 >> 19) & 0xffffffff
        a5 = (((a5 << 13) & 0xffffffff) + a6) & 0xffffffff

    seed = a5
    print(f"    Computed Stage 1 Hash / Seed: {hex(seed)}")

    # 2. Decrypt 16384 bytes payload using Xorshift32 PRNG
    payload = data[0x00e0:0x40e0]
    decrypted = bytearray(len(payload))
    s = seed
    for i in range(len(payload)):
        if (i & 3) == 0:
            a4 = ((s << 13) ^ s) & 0xffffffff
            a4 = ((a4 >> 17) ^ a4) & 0xffffffff
            s = ((a4 << 5) ^ a4) & 0xffffffff
        shift = (i & 3) * 8
        key_byte = (s >> shift) & 0xff
        decrypted[i] = payload[i] ^ key_byte

    print("[*] Stage 2: Loaded 'TR4P-G4T3' firmware at 0x80100000")

    # 3. Function 1: S-box generation (RC4 KSA) and 64 bytes PRGA keystream
    key1 = b"tr4p_d1sp4tch_v1"
    sbox = list(range(256))
    j = 0
    for i in range(256):
        j = (j + sbox[i] + key1[i % len(key1)]) & 0xff
        sbox[i], sbox[j] = sbox[j], sbox[i]

    keystream = []
    i = 0
    j = 0
    sbox_copy = list(sbox)
    for _ in range(64):
        i = (i + 1) & 0xff
        j = (j + sbox_copy[i]) & 0xff
        sbox_copy[i], sbox_copy[j] = sbox_copy[j], sbox_copy[i]
        keystream.append(sbox_copy[(sbox_copy[i] + sbox_copy[j]) & 0xff])

    def rol8(val, r):
        r = r % 8
        if r == 0:
            return val
        return ((val << r) | (val >> (8 - r))) & 0xff

    def rol32(val, r):
        return (((val << r) & 0xffffffff) | (val >> (32 - r))) & 0xffffffff

    def compute_F(R, k_round):
        F_out = []
        for idx in range(8):
            s_idx = (k_round[idx] + R[idx]) & 0xff
            t0 = sbox[s_idx]
            rot = (idx + 1) % 8
            val = R[rot]
            rot_val = rol8(val, rot)
            F_out.append(t0 ^ rot_val)
        return F_out

    # 4. Invert 8-round Feistel Network in Function 2
    # Expected ciphertext checked by Function 3 at 0x801008ac
    expected = decrypted[0x801008ac - 0x80100000 : 0x801008ac - 0x80100000 + 16]
    L = list(expected[:8])
    R = list(expected[8:])

    for round_idx in range(7, -1, -1):
        k_round = keystream[round_idx*8 : (round_idx+1)*8]
        prev_R = L
        F = compute_F(prev_R, k_round)
        prev_L = [R[k] ^ F[k] for k in range(8)]
        L = prev_L
        R = prev_R

    recovered_key = bytes(L + R)
    print(f"[*] Recovered 16-byte Key: {recovered_key.decode('ascii')}")

    # 5. Forward simulation to get the final 128-bit state (RC4 key)
    L = list(recovered_key[:8])
    R = list(recovered_key[8:])
    state = [
        0x811c9dc5,
        0x01000193,
        0xdeadbeef,
        0x9e3779b9
    ]

    for round_idx in range(8):
        k_round = keystream[round_idx*8 : (round_idx+1)*8]
        F = compute_F(R, k_round)
        new_R = [L[idx] ^ F[idx] for idx in range(8)]
        L = list(R)
        R = list(new_R)

        for a3 in range(8):
            # L[a3] update
            a2 = a3 & 3
            v = (state[a2] ^ L[a3]) * 0x01000193 & 0xffffffff
            state[a2] = rol32(v, 7)

            # R[a3] update
            a2 = a3 >> 1
            v = (state[a2] ^ R[a3]) * 0x01000193 & 0xffffffff
            state[a2] = rol32(v, 5)

    rc4_key = struct.pack("<4I", *state)
    print(f"[*] Derived Flag RC4 Key: {rc4_key.hex()}")

    # 6. Decrypt Flag in Function 0
    flag_ct = decrypted[0x80100884 - 0x80100000 : 0x80100884 - 0x80100000 + 39]
    sbox_rc4 = list(range(256))
    j = 0
    for i in range(256):
        j = (j + sbox_rc4[i] + rc4_key[i % 16]) & 0xff
        sbox_rc4[i], sbox_rc4[j] = sbox_rc4[j], sbox_rc4[i]

    flag_bytes = []
    i = 0
    j = 0
    for b in flag_ct:
        i = (i + 1) & 0xff
        j = (j + sbox_rc4[i]) & 0xff
        sbox_rc4[i], sbox_rc4[j] = sbox_rc4[j], sbox_rc4[i]
        k = sbox_rc4[(sbox_rc4[i] + sbox_rc4[j]) & 0xff]
        flag_bytes.append(b ^ k)

    flag = bytes(flag_bytes).decode("latin1")
    print(f"[+] Flag: {flag}")
    return flag

if __name__ == "__main__":
    solve()
