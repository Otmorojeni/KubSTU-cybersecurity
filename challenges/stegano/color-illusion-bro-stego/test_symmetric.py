import cv2 as cv
import numpy as np
from PIL import Image

src = "bro_stego_with_hint.png"

# Test both BGR and RGB to YUV:
img_bgr = cv.imread(src)
img_rgb = cv.cvtColor(img_bgr, cv.COLOR_BGR2RGB)

for colorspace, wmyuv in [('RGB2YUV', cv.cvtColor(img_rgb, cv.COLOR_RGB2YUV)),
                          ('BGR2YUV', cv.cvtColor(img_bgr, cv.COLOR_BGR2YUV))]:
    wmf = wmyuv.astype('float32')
    h, w = wmf.shape[:2]
    n_by = h // 8
    n_bx = w // 8
    
    # In each 8x8 block:
    # 1. Compare (3, 4) vs (4, 3)
    img_34 = np.zeros((n_by, n_bx), dtype=np.uint8)
    # 2. Compare (2, 5) vs (5, 2)
    img_25 = np.zeros((n_by, n_bx), dtype=np.uint8)
    # 3. For the max spike (rx, ry), compare part[rx, ry] vs part[7-rx, 7-ry]
    img_spike = np.zeros((n_by, n_bx), dtype=np.uint8)
    
    for by in range(n_by):
        for bx in range(n_bx):
            block = cv.dct(wmf[by*8:(by+1)*8, bx*8:(bx+1)*8, 0])
            
            # (3, 4) vs (4, 3)
            if block[3, 4] > block[4, 3]:
                img_34[by, bx] = 255
                
            # (2, 5) vs (5, 2)
            if block[2, 5] > block[5, 2]:
                img_25[by, bx] = 255
                
            # Spike vs its center symmetric
            b_clean = block.copy()
            b_clean[0:2, 0:2] = 0
            u, v = np.unravel_index(np.argmax(np.abs(b_clean)), b_clean.shape)
            if block[u, v] > block[7 - u, 7 - v]:
                img_spike[by, bx] = 255

    Image.fromarray(img_34).save(f'test_sym_34_{colorspace}.png')
    Image.fromarray(img_25).save(f'test_sym_25_{colorspace}.png')
    Image.fromarray(img_spike).save(f'test_sym_spike_{colorspace}.png')

print("Saved symmetric test images!")
