import numpy as np
from PIL import Image
from scipy.fftpack import dct

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)

H, W, C = arr.shape
n_by = H // 8
n_bx = W // 8

def get_dct(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

# Let's compute 160x160 map for all (u, v) for R, G, B, and Gray (or Y)
gray = 0.299 * arr[:,:,0] + 0.587 * arr[:,:,1] + 0.114 * arr[:,:,2]

maps = np.zeros((8, 8, n_by, n_bx), dtype=np.float32)

for by in range(n_by):
    for bx in range(n_bx):
        b = gray[by*8:(by+1)*8, bx*8:(bx+1)*8]
        d = get_dct(b)
        for u in range(8):
            for v in range(8):
                maps[u, v, by, bx] = d[u, v]

print("Computed all frequency maps!")

# Let's save thumbnails or check variance / patterns of each (u, v) map
# Especially for higher frequencies where the image content should be almost zero (noise subsided!)
import os
os.makedirs('freq_maps', exist_ok=True)

for u in range(8):
    for v in range(8):
        m = maps[u, v]
        # Normalize to 0-255
        m_min, m_max = m.min(), m.max()
        if m_max > m_min:
            norm_m = ((m - m_min) / (m_max - m_min) * 255).astype(np.uint8)
        else:
            norm_m = np.zeros_like(m, dtype=np.uint8)
        
        # Check standard deviation and statistics
        print(f"Freq ({u},{v}): min={m_min:.2f}, max={m_max:.2f}, std={m.std():.2f}")
        
        # Save as image
        im = Image.fromarray(norm_m)
        im.save(f'freq_maps/freq_{u}_{v}.png')

print("Saved all 64 frequency maps to freq_maps/")
