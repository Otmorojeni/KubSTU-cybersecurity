from PIL import Image
import numpy as np
from scipy.fftpack import dct

stego = Image.open('bro_stego_with_hint.png')
orig = Image.open('orig_meme.jpg').resize((1280, 1280), Image.Resampling.LANCZOS)
arr_s = np.array(stego, dtype=np.float32)
arr_o = np.array(orig, dtype=np.float32)

def get_dct(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

# Let's inspect 10 sky blocks
for bx in range(5, 15):
    ds = get_dct(arr_s[10*8:11*8, bx*8:(bx+1)*8, 0])
    do = get_dct(arr_o[10*8:11*8, bx*8:(bx+1)*8, 0])
    diff = ds - do
    # Zero out DC
    diff[0, 0] = 0
    # Which frequencies in diff have |diff| > 10?
    large_diffs = []
    for u in range(8):
        for v in range(8):
            if abs(diff[u, v]) > 8:
                large_diffs.append(((u, v), round(diff[u, v], 2)))
    print(f"Block (10, {bx:2d}): large diffs = {large_diffs}")
