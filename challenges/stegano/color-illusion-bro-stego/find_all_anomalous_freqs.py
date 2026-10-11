import numpy as np
from PIL import Image
from scipy.fftpack import dct

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)

def get_dct(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

H, W, _ = arr.shape
n_by, n_bx = H // 8, W // 8

dct_all = np.zeros((n_by, n_bx, 8, 8))
for by in range(n_by):
    for bx in range(n_bx):
        dct_all[by, bx] = get_dct(arr[by*8:(by+1)*8, bx*8:(bx+1)*8, 0])

print("Checking all (u, v) for peaks around +/- 10..20:")
anomalies = []
for u in range(8):
    for v in range(8):
        vals = dct_all[:, :, u, v].flatten()
        # count how many values are in [10, 20] and [-20, -10]
        pos_peak = np.sum((vals >= 8) & (vals <= 25))
        neg_peak = np.sum((vals <= -8) & (vals >= -25))
        # in natural smooth areas (like sky/smoke), high frequencies are close to 0 (-1..1)
        # Check in the smooth sky area: by in [5, 40], bx in [5, 50]
        sky_vals = dct_all[5:40, 5:50, u, v].flatten()
        sky_pos = np.sum(sky_vals > 5)
        sky_neg = np.sum(sky_vals < -5)
        sky_zero = np.sum(np.abs(sky_vals) < 2)
        
        if sky_pos > 50 or sky_neg > 50:
            print(f"ANOMALY at ({u},{v}): total pos={pos_peak}, neg={neg_peak} | sky pos={sky_pos}, neg={sky_neg}, near_zero={sky_zero} (out of {len(sky_vals)})")
            anomalies.append((u, v))

print("\nAll anomaly frequencies:", anomalies)
