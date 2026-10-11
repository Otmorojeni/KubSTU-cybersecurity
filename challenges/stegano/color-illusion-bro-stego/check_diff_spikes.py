from PIL import Image
import numpy as np
from scipy.fftpack import dct

stego = Image.open('bro_stego_with_hint.png')
orig = Image.open('orig_meme.jpg').resize((1280, 1280), Image.Resampling.LANCZOS)

arr_s = np.array(stego, dtype=np.float32)
arr_o = np.array(orig, dtype=np.float32)

def get_dct(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

# Let's inspect blocks (10, 10) to (10, 25)
print("Block differences:")
for bx in range(10, 26):
    ds = get_dct(arr_s[10*8:11*8, bx*8:(bx+1)*8, 0])
    do = get_dct(arr_o[10*8:11*8, bx*8:(bx+1)*8, 0])
    diff = ds - do
    
    # In diff, find max absolute difference in high/mid frequencies (excluding DC and top-left 2x2)
    diff_ac = diff.copy()
    diff_ac[0:2, 0:2] = 0
    max_pos = np.unravel_index(np.argmax(np.abs(diff_ac)), diff_ac.shape)
    print(f"Block (10, {bx:2d}): spike at {max_pos} = {diff_ac[max_pos]:6.2f} (stego={ds[max_pos]:6.2f}, orig={do[max_pos]:6.2f})")
