import numpy as np
from PIL import Image
from scipy.fftpack import dct

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)

def get_dct(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

H, W, _ = arr.shape
n_by, n_bx = H // 8, W // 8

# Compare across channels R, G, B and Y
img_yuv = img.convert('YCbCr')
arr_yuv = np.array(img_yuv, dtype=np.float32)

for c_idx, c_name in [(0, 'R'), (1, 'G'), (2, 'B')]:
    vals_27 = []
    for by in range(n_by):
        for bx in range(n_bx):
            d = get_dct(arr[by*8:(by+1)*8, bx*8:(bx+1)*8, c_idx])
            vals_27.append(d[2, 7])
    vals_27 = np.array(vals_27)
    large = np.sum(np.abs(vals_27) > 10)
    print(f"Channel {c_name} (2,7) |val| > 10: {large} / {len(vals_27)}")

# Check Y
vals_27_y = []
for by in range(n_by):
    for bx in range(n_bx):
        d = get_dct(arr_yuv[by*8:(by+1)*8, bx*8:(bx+1)*8, 0])
        vals_27_y.append(d[2, 7])
vals_27_y = np.array(vals_27_y)
large_y = np.sum(np.abs(vals_27_y) > 10)
print(f"Channel Y (2,7) |val| > 10: {large_y} / {len(vals_27_y)}")
