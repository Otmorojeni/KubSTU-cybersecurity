import numpy as np
from PIL import Image
from scipy.fftpack import dct

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)[:, :, 0]

def get_dct(b):
    return dct(dct(b.T, norm='ortho').T, norm='ortho')

# Let's inspect rows 10 to 25, cols 5 to 35 (pure sky/smoke, very smooth)
ground_truth = []
for by in range(12, 16):
    for bx in range(10, 30):
        b = arr[by*8:(by+1)*8, bx*8:(bx+1)*8]
        d = get_dct(b)
        d_clean = d.copy()
        d_clean[0:2, 0:2] = 0
        u, v = np.unravel_index(np.argmax(np.abs(d_clean)), d_clean.shape)
        val = d[u, v]
        block_idx_rowmajor = by * 160 + bx
        block_idx_colmajor = bx * 160 + by
        ground_truth.append((by, bx, block_idx_rowmajor, block_idx_colmajor, (int(u), int(v)), float(val)))

print(f"Collected {len(ground_truth)} ground truth sky blocks:")
for gt in ground_truth[:25]:
    print(f"Row {gt[0]}, Col {gt[1]} (idx_rm={gt[2]}): freq={gt[4]}, val={gt[5]:+.2f}")
