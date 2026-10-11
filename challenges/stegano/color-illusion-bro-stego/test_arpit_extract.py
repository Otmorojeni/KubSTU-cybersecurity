import numpy as np
from scipy.fftpack import dct
from PIL import Image
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

DCT_BLOCK_SIZE = 8
QIM_DELTA = 5
MIN_COEFF_INDEX = 5
MAX_COEFF_INDEX = 20

ZIGZAG_INDICES = [
    0, 1, 8, 16, 9, 2, 3, 10,
    17, 24, 32, 25, 18, 11, 4, 5,
    12, 19, 26, 33, 40, 48, 41, 34,
    27, 20, 13, 6, 7, 14, 21, 28,
    35, 42, 49, 56, 57, 50, 43, 36,
    29, 22, 15, 23, 30, 37, 44, 51,
    58, 59, 52, 45, 38, 31, 39, 46,
    53, 60, 61, 54, 47, 55, 62, 63
]

ZIGZAG_TO_RC = {index: (row, col) 
    for index, (row, col) in enumerate(
        (r, c) for r in range(DCT_BLOCK_SIZE) for c in range(DCT_BLOCK_SIZE)
    )
}

EMBED_COEFFS = []
for i in range(MIN_COEFF_INDEX, MAX_COEFF_INDEX + 1): 
    if i < len(ZIGZAG_INDICES):
        rc_index = ZIGZAG_INDICES[i]
        EMBED_COEFFS.append(ZIGZAG_TO_RC[rc_index])

TERMINATION_SEQUENCE = b'\xAA\xAA\xAA\xAA' 
TERMINATION_BITS = []
for byte in TERMINATION_SEQUENCE:
    TERMINATION_BITS.extend([(byte >> i) & 1 for i in range(7, -1, -1)])
TERMINATION_BITS_COUNT = len(TERMINATION_BITS)

def _apply_dct(block):
    return dct(dct(block - 128, axis=0, norm='ortho'), axis=1, norm='ortho')

def _qim_extract(coefficient, delta=5):
    k_delta = np.round(coefficient / delta)
    return int(k_delta) % 2

img = Image.open('bro_stego_with_hint.png').convert("RGB")
width, height = img.size
img_array = np.array(img, dtype=np.float32)

print(f"Image size: {width}x{height}")

for delta in [5, 10, 15, 20, 25, 30]:
    for channel_idx in [0, 1, 2]:
        channel_array = img_array[:, :, channel_idx].copy()
        num_blocks_w = width // DCT_BLOCK_SIZE
        num_blocks_h = height // DCT_BLOCK_SIZE
        
        extracted_bits = []
        is_finished = False

        for r_block in range(num_blocks_h):
            r_start = r_block * DCT_BLOCK_SIZE
            r_end = r_start + DCT_BLOCK_SIZE
            
            for c_block in range(num_blocks_w):
                c_start = c_block * DCT_BLOCK_SIZE
                c_end = c_start + DCT_BLOCK_SIZE
                block = channel_array[r_start:r_end, c_start:c_end]
                dct_block = _apply_dct(block)
                
                for r, c in EMBED_COEFFS:
                    extracted_bit = _qim_extract(dct_block[r, c], delta)
                    extracted_bits.append(extracted_bit)
                    
                    if len(extracted_bits) >= TERMINATION_BITS_COUNT:
                        if extracted_bits[-TERMINATION_BITS_COUNT:] == TERMINATION_BITS:
                            is_finished = True
                            break
                if is_finished:
                    break
            if is_finished:
                break

        if is_finished:
            final_bits = extracted_bits[:-TERMINATION_BITS_COUNT]
            raw_bytes = bytearray()
            for i in range(0, len(final_bits) - (len(final_bits) % 8), 8):
                byte = 0
                for j in range(8):
                    byte = (byte << 1) | final_bits[i + j]
                raw_bytes.append(byte)
            data = bytes(raw_bytes)
            print(f"FOUND TERMINATION! delta={delta}, channel={channel_idx}, bytes={len(data)}")
            print("Hex:", data[:64].hex())
            # Try to decrypt with key-bro
            # Header: SALT (16), IV (16), LENGTH (4), CIPHERTEXT
            try:
                salt = data[:16]
                iv = data[16:32]
                msg_len = int.from_bytes(data[32:36], 'big')
                ciphertext = data[36:]
                print(f"msg_len={msg_len}, ciphertext len={len(ciphertext)}")
                
                for k in ["key-bro", "bro", "key_bro"]:
                    kdf = PBKDF2HMAC(
                        algorithm=hashes.SHA256(),
                        length=32,
                        salt=salt,
                        iterations=480000,
                        backend=default_backend()
                    )
                    key_bytes = kdf.derive(k.encode())
                    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
                    decryptor = cipher.decryptor()
                    padded = decryptor.update(ciphertext) + decryptor.finalize()
                    print(f"Key {k} decrypted:", padded[:msg_len])
            except Exception as e:
                print("Decryption error:", e)
