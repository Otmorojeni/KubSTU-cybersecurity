from PIL import Image
import numpy as np
from scipy.fftpack import dct

stego = Image.open('bro_stego_with_hint.png')
# How should orig be resized or aligned?
orig = Image.open('orig_meme.jpg')
print(f"Stego size: {stego.size}, Orig size: {orig.size}")

def get_dct(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

# Try different resizes and alignments of orig to find the exact cover image
# orig is 1206x1206, stego is 1280x1280
# What if orig was resized to 1280x1280, or padded, or cropped?
for resample, rname in [(Image.Resampling.LANCZOS, 'LANCZOS'), (Image.Resampling.BILINEAR, 'BILINEAR'), (Image.Resampling.BICUBIC, 'BICUBIC')]:
    orig_1280 = orig.resize((1280, 1280), resample)
    arr_s = np.array(stego, dtype=np.float32)[:, :, 0]
    arr_o = np.array(orig_1280, dtype=np.float32)[:, :, 0]
    
    # Check block 0 diff DCT:
    ds = get_dct(arr_s[0:8, 0:8])
    do = get_dct(arr_o[0:8, 0:8])
    diff = ds - do
    
    # Find max absolute difference for u+v >= 3
    max_d = 0
    max_pt = None
    for u in range(8):
        for v in range(8):
            if u + v >= 3 and abs(diff[u, v]) > max_d:
                max_d = abs(diff[u, v])
                max_pt = (u, v)
    print(f"[{rname}] Block 0 max diff at {max_pt}: {diff[max_pt[0], max_pt[1]]:+.2f}")
