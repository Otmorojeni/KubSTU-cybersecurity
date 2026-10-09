---
name: ctf-crypto
description: >-
  Expert CTF cryptanalyst for analyzing and solving cryptography challenges.
  Covers classical ciphers, RSA attacks, elliptic curves (ECC), AES and block cipher
  modes, discrete logarithms, PRNG predictability, hash attacks, and automated
  solver scripting using Python (pycryptodome, gmpy2, sympy) and SageMath.
---

# CTF Cryptography Challenge Solver

This skill provides checklists, attack vectors, and solver templates for Jeopardy-style CTF cryptography challenges.

## 1. Initial Triage & Identification

When given a crypto challenge:
1. **Analyze Given Artifacts:**
   - Source code provided (`challenge.py`, `server.py`) vs black-box network service (`nc host port`).
   - Public parameters: moduli ($N$), public exponents ($e$), ciphertexts ($c$), IVs, elliptic curve parameters.
2. **Identify the Core Primitive:**
   - Asymmetric: RSA, ECC, Diffie-Hellman, DSA/ECDSA, Paillier.
   - Symmetric: AES (ECB, CBC, CTR, GCM), DES, custom Feistel networks.
   - Hash & MAC: MD5, SHA-1, HMAC, Length Extension.
   - Classical / Encoding: Base64/32/85, Caesar, Vigenère, Affine, Substitution, multi-byte XOR.
   - Random / PRNG: Python `random` (MT19937), LCG, seed reuse, weak timestamp seeds.

---

## 2. RSA Attack Vectors Checklist

- **Small $e$:**
  - $e = 3$ and no padding: $m^3 < N \implies m = \sqrt[3]{c}$.
  - Hastad's Broadcast Attack: same message encrypted under 3+ different moduli with small $e$ (use Chinese Remainder Theorem).
- **Factorization of $N$:**
  - Check [FactorDB](http://factordb.com): query $N$ for known prime factors.
  - Close primes ($|p - q| < N^{1/4}$): Fermat's factorization method.
  - Smooth primes ($p - 1$ or $q - 1$ is smooth): Pollard's $p-1$ algorithm.
- **Small private exponent $d$:**
  - $d < \frac{1}{3} N^{1/4}$: Wiener's continued fraction attack.
  - $d < N^{0.292}$: Boneh-Durfee lattice attack.
- **Common Modulus Attack:**
  - Same message encrypted with $e_1, e_2$ where $\gcd(e_1, e_2) = 1$ under identical $N$.
  - Use Extended Euclidean Algorithm: $a e_1 + b e_2 = 1 \implies c_1^a \cdot c_2^b \equiv m \pmod N$.
- **Franklin-Reiter Related Message Attack:**
  - Two messages with known polynomial relation: $m_2 = f(m_1) \pmod N$.
- **Coppersmith's Theorem:**
  - Partial key exposure, stereotyping (known prefix/suffix of message with small unknown part).

---

## 3. Symmetric & Block Cipher Attacks

- **AES-ECB:**
  - Identical plaintext blocks produce identical ciphertext blocks (look for repeated 16-byte blocks).
  - Byte-at-a-time ECB decryption when oracle appends secret flag to user-controlled prefix: `oracle(prefix + flag)`.
- **AES-CBC:**
  - **Padding Oracle Attack:** Server leaks padding validity (valid vs invalid PKCS#7 padding). Decrypt byte-by-byte from right to left.
  - **Bit-Flipping Attack:** Modifying ciphertext block $C_{i-1}$ directly flips bits in plaintext block $P_i$ after decryption: $P'_i = P_i \oplus C_{i-1} \oplus C'_{i-1}$.
  - **IV = Key:** If $IV = Key$, decrypting $C_1 || 0^{16} || C_1$ leaks $Key = P_1 \oplus P_3$.
- **XOR / Stream Ciphers:**
  - Single-byte XOR: Frequency analysis on printable ASCII letters.
  - Repeating-key XOR: Hamming distance / index of coincidence to find key length, then solve each slice as single-byte XOR.
  - Crib Dragging: When two plaintexts are XORed with the same keystream ($C_1 \oplus C_2 = P_1 \oplus P_2$), drag known words ("flag{", "http", "the ") across the XOR stream.

---

## 4. PRNG & State Recovery

- **Python `random` (MT19937 - Mersenne Twister):**
  - Not cryptographically secure!
  - 624 32-bit consecutive outputs reveal the entire internal state.
  - Use `randcrack` Python library to predict all past and future outputs.
- **Linear Congruential Generator (LCG):**
  - $X_{n+1} = (a X_n + c) \bmod m$.
  - Given 6+ consecutive values with unknown $(a, c, m)$, parameters can be recovered via GCD and modular arithmetic.

---

## 5. Python Solver Template

```python
import sys
from pwn import *
from Crypto.Util.number import long_to_bytes, bytes_to_long, inverse, GCD

def solve_rsa(n, e, c):
    # Example template
    pass

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "remote":
        io = remote("challenge.domain", 1337)
    else:
        # local test
        pass
```
