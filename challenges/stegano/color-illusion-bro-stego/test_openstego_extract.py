import hashlib
import numpy as np
from PIL import Image

class JavaRandom:
    def __init__(self, seed):
        self.seed = (seed ^ 0x5DEECE66D) & ((1 << 48) - 1)

    def next(self, bits):
        self.seed = (self.seed * 0x5DEECE66D + 0xB) & ((1 << 48) - 1)
        return self.seed >> (48 - bits)

    def nextInt(self):
        val = self.next(32)
        if val >= (1 << 31):
            val -= (1 << 32)
        return val

def java_abs(val):
    if val == -2147483648:
        return -2147483648
    return abs(val)

def get_password_seed(password):
    if not password:
        return 98234782
    md5_bytes = hashlib.md5(password.encode('utf-8')).digest()
    hex_str = md5_bytes.hex()[:15]
    return int(hex_str, 16)

def is_mid_freq(coeff):
    if coeff in [3, 10, 17, 24]:
        return 1
    if coeff in [4, 11, 18, 25, 32]:
        return 2
    if coeff in [5, 12, 19, 26, 33, 40]:
        return 3
    if coeff in [13, 20, 27, 34, 41]:
        return 4
    if coeff in [28, 35]:
        return 5
    return 0

JPEG_LUMIN_QUANT_TBL = np.array([
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]
], dtype=np.int32)

def init_quantum(quality=75):
    if quality < 50:
        q = 5000 // quality
    else:
        q = 200 - quality * 2
    
    Quantum = np.zeros((8, 8), dtype=np.int32)
    for i in range(8):
        for j in range(8):
            if q != 0:
                Quantum[i, j] = (JPEG_LUMIN_QUANT_TBL[i, j] * q + 50) // 100
            else:
                Quantum[i, j] = JPEG_LUMIN_QUANT_TBL[i, j]
    return Quantum

# Precompute C matrix
C = np.zeros((8, 8), dtype=np.float64)
sqJpeg = np.sqrt(8.0)
sqJpeg2 = np.sqrt(2.0 / 8.0)
for j in range(8):
    C[0, j] = 1.0 / sqJpeg
for i in range(1, 8):
    for j in range(8):
        C[i, j] = sqJpeg2 * np.cos(np.pi * (2 * j + 1) * i / 16.0)

def fwd_dct_8x8(block):
    # block is 8x8 int
    # temp = (block - 128) @ C.T
    # output = C @ temp
    temp = np.dot(block.astype(np.float64) - 128.0, C.T)
    out = np.dot(C, temp)
    return out

def round_java(a):
    return int(a - 0.5) if a < 0 else int(a + 0.5)

def extract_with_key(password, img_path, transpose_y=False):
    seed = get_password_seed(password)
    rand = JavaRandom(seed)
    
    img = Image.open(img_path).convert('RGB')
    w, h = img.size
    w_blk = w - (w % 8)
    h_blk = h - (h % 8)
    
    # RGB to Y
    arr = np.array(img, dtype=np.float64)
    # y = (int) (0.299 * r + 0.587 * g + 0.114 * b)
    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]
    y_img = np.floor(0.299 * r + 0.587 * g + 0.114 * b).astype(np.int32)
    # Note: in OpenStego ImageUtil:
    # y = new int[height][width]
    # y[i][j] where i is y (0..h-1), j is x (0..w-1)
    
    Quantum = init_quantum(75)
    
    coord_set = set()
    total_blocks_x = w_blk // 8
    total_blocks_y = h_blk // 8
    
    extracted_bytes = bytearray()
    curr_byte = 0
    bit_count = 0
    
    # We want to extract at least 500 bytes to see header
    for byte_idx in range(1000):
        for bit_in_byte in range(8):
            while True:
                xb = java_abs(rand.nextInt()) % total_blocks_x
                yb = java_abs(rand.nextInt()) % total_blocks_y
                key = f"{xb},{yb}"
                if key not in coord_set:
                    coord_set.add(key)
                    break
            
            while True:
                coeffNum = (java_abs(rand.nextInt()) % 62) + 1
                if is_mid_freq(coeffNum) != 0:
                    break
            
            # Now block coordinates:
            # OpenStego DctLSBInputStream:
            # fwdDctBlock8x8(this.y, xb * 8, yb * 8, this.dcts)
            # In fwdDctBlock8x8:
            # System.arraycopy(input[col + i], row, tmpIntArray[i], 0, 8)
            # where col = xb * 8, row = yb * 8.
            # If input is y[height][width]:
            # input[col + i] is accessing row (xb*8 + i)!
            # and copying elements from column (yb*8)!
            if not transpose_y:
                block = y_img[xb*8 : (xb+1)*8, yb*8 : (yb+1)*8]
            else:
                block = y_img[yb*8 : (yb+1)*8, xb*8 : (xb+1)*8]
                
            dcts = fwd_dct_8x8(block)
            
            # Quantize
            ci = coeffNum // 8
            cj = coeffNum % 8
            q_val = round_java(dcts[ci, cj] / Quantum[ci, cj])
            bit = q_val & 1
            curr_byte = (curr_byte << 1) | bit
            bit_count += 1
            
        extracted_bytes.append(curr_byte)
        curr_byte = 0
        
        # Check if header matches OSDCT
        if len(extracted_bytes) == 5:
            print(f"[{password}] First 5 bytes: {bytes(extracted_bytes)}")
            if bytes(extracted_bytes) == b'OSDCT':
                print(f"!!! MATCH FOUND WITH PASSWORD {password} !!!")
                
    return bytes(extracted_bytes)

print("Testing password 'key-bro'...")
res1 = extract_with_key("key-bro", "bro_stego_with_hint.png", transpose_y=False)
print("Result 1 (transpose=False) first 32 bytes:", res1[:32])

res2 = extract_with_key("key-bro", "bro_stego_with_hint.png", transpose_y=True)
print("Result 2 (transpose=True) first 32 bytes:", res2[:32])
