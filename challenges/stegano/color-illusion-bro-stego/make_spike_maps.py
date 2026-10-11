import numpy as np
from PIL import Image
from scipy.fftpack import dct

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)

def get_dct(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

H, W, _ = arr.shape
n_by, n_bx = H // 8, W // 8

sign_map = np.zeros((n_by, n_bx), dtype=np.uint8)
freq_u_map = np.zeros((n_by, n_bx), dtype=np.uint8)
freq_v_map = np.zeros((n_by, n_bx), dtype=np.uint8)
freq_idx_map = np.zeros((n_by, n_bx), dtype=np.uint8)

for by in range(n_by):
    for bx in range(n_bx):
        d = get_dct(arr[by*8:(by+1)*8, bx*8:(bx+1)*8, 0])
        # Mask out DC and low AC
        d_clean = d.copy()
        d_clean[0, 0] = 0
        d_clean[0, 1] = 0
        d_clean[1, 0] = 0
        d_clean[1, 1] = 0
        
        u, v = np.unravel_index(np.argmax(np.abs(d_clean)), d_clean.shape)
        val = d[u, v]
        
        sign_map[by, bx] = 255 if val > 0 else 0
        freq_u_map[by, bx] = int(u * 32)
        freq_v_map[by, bx] = int(v * 32)
        freq_idx_map[by, bx] = int((u * 8 + v) * 4)

Image.fromarray(sign_map).save('spike_sign_map.png')
Image.fromarray(freq_u_map).save('spike_freq_u.png')
Image.fromarray(freq_v_map).save('spike_freq_v.png')
Image.fromarray(freq_idx_map).save('spike_freq_idx.png')
print("Saved spike maps: spike_sign_map.png, etc.")
