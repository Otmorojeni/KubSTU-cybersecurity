from PIL import Image
import numpy as np
from scipy.fftpack import dct

stego = Image.open('bro_stego_with_hint.png')
orig = Image.open('orig_meme.jpg').resize((1280, 1280), Image.Resampling.LANCZOS)

arr_s = np.array(stego, dtype=np.float32)
arr_o = np.array(orig, dtype=np.float32)

def get_dct(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

# Compare block (10, 10) in both
ds = get_dct(arr_s[10*8:11*8, 10*8:11*8, 0])
do = get_dct(arr_o[10*8:11*8, 10*8:11*8, 0])

diff_d = ds - do
print("Stego DCT:\n", np.round(ds, 2))
print("Orig DCT:\n", np.round(do, 2))
print("Diff DCT (Stego - Orig):\n", np.round(diff_d, 2))
