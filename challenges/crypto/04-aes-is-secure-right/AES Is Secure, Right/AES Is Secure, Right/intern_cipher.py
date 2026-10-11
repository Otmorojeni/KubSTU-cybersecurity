from Crypto.Cipher import AES
from hashlib import sha256


def prepare(data: bytes, n: int = 16) -> bytes:
    r = n - len(data) % n

    if r == 0:
        r = n

    k = (len(data) + r) // n
    return data + bytes([k]) * r


def transform(data: bytes, pin: str) -> bytes:
    key = sha256(pin.encode()).digest()[:16]
    cipher = AES.new(key, AES.MODE_ECB)

    data = prepare(data)

    blocks = [
        data[i:i + 16]
        for i in range(0, len(data), 16)
    ]

    shift = sum(int(x) for x in pin) % len(blocks)

    blocks = blocks[shift:] + blocks[:shift]
    blocks = blocks[::-1]

    return b''.join(cipher.encrypt(block) for block in blocks)


def encrypt(data: bytes, pin: str) -> bytes:
    return transform(data, pin)


if __name__ == "__main__":
    with open("secret.txt", "rb") as f:
        secret = f.read().strip()

    with open("pin.txt", "r", encoding="utf-8") as f:
        pin = f.read().strip()

    result = encrypt(secret, pin)

    print(result.hex())
