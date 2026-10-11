import numpy as np
from PIL import Image
from scipy.fftpack import dct

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)[:, :, 0]
def get_dct(b): return dct(dct(b.T, norm='ortho').T, norm='ortho')

prefix = 'KubSTU{'
bits = []
for c in prefix:
    val = ord(c)
    for b in range(7, -1, -1):
        bits.append((val >> b) & 1)

print(f'Prefix length: {len(prefix)} chars, {len(bits)} bits.')

for i, bit in enumerate(bits):
    by = i // 160
    bx = i % 160
    b = arr[by*8:(by+1)*8, bx*8:(bx+1)*8]
    d = get_dct(b)
    req_sign = 1 if bit == 0 else -1
    sign_ch = '+' if req_sign > 0 else '-'
    matches = []
    for u in range(8):
        for v in range(8):
            if u + v >= 2 and abs(d[u, v]) > 6.0:
                if d[u, v] * req_sign > 0:
                    matches.append(((u, v), d[u, v]))
    matches.sort(key=lambda x: abs(x[1]), reverse=True)
    m_str = str([(m[0], round(m[1], 1)) for m in matches[:4]])
    print(f"Block {i:2d} ('{prefix[i//8]}' bit {i%8}={bit}, need {sign_ch}): top = {m_str}")
