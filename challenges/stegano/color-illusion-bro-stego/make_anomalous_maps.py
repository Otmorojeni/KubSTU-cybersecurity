import numpy as np
from PIL import Image
from scipy.fftpack import dct

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)

def get_dct(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

H, W, _ = arr.shape
n_by, n_bx = H // 8, W // 8

grid_pos = np.zeros((n_by, n_bx), dtype=np.uint8)
grid_neg = np.zeros((n_by, n_bx), dtype=np.uint8)
grid_abs = np.zeros((n_by, n_bx), dtype=np.uint8)

for by in range(n_by):
    for bx in range(n_bx):
        d = get_dct(arr[by*8:(by+1)*8, bx*8:(bx+1)*8, 0])
        val = d[2, 7]
        if val > 8:
            grid_pos[by, bx] = 255
        elif val < -8:
            grid_neg[by, bx] = 255
        if abs(val) > 8:
            grid_abs[by, bx] = 255

Image.fromarray(grid_pos).save('map_2_7_pos.png')
Image.fromarray(grid_neg).save('map_2_7_neg.png')
Image.fromarray(grid_abs).save('map_2_7_abs.png')
print("Saved maps for (2, 7)")
