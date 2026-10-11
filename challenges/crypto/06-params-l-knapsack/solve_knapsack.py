"""
Solver for Knapsack / Subset Sum cryptosystem from params.txt
Task: "Перехвачены зашифрованные передачи L. Открытый ключ один, сообщение разбито на блоки."
"""

def solve():
    with open('params.txt') as f:
        data = f.read()
    scope = {}
    exec(data, scope)
    w = scope['w']
    ciphertexts = scope['ciphertexts']

    # Recovered blocks
    blocks = [
        b'KubSTU{y',
        b'0u_n33d_',
        b'70_6e_4_',
        b're41_d37',
        b'3ct1ve_7',
        b'o_5o1v3_',
        b'7h15}\x00\x00\x00',
    ]

    print("Verifying blocks:")
    for idx, (blk, c_target) in enumerate(zip(blocks, ciphertexts)):
        bits = []
        for byte in blk:
            for b in range(8):
                bits.append((byte >> (7 - b)) & 1)
        s = sum(bi * wi for bi, wi in zip(bits, w))
        assert s == c_target, f"Block {idx} mismatch"
        print(f"  Block {idx}: {blk} -> {s == c_target}")

    flag = b''.join(blocks).rstrip(b'\x00').decode('ascii')
    print("\nRecovered Flag:", flag)
    return flag

if __name__ == '__main__':
    solve()
