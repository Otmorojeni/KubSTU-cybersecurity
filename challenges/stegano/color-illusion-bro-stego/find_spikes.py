import numpy as np
from PIL import Image
from scipy.fftpack import dct
import random

img = Image.open('bro_stego_with_hint.png')
arr = np.array(img, dtype=np.float32)

def get_dct(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

# Find the spike position for the first 30 blocks (row 0, cols 0..29)
spikes = []
for bx in range(30):
    b = arr[0:8, bx*8:(bx+1)*8, 0]
    d = get_dct(b)
    # Exclude low frequencies (0, 0), (0, 1), (1, 0) because natural gradients can be large there
    # Find position with largest magnitude in mid/high frequencies
    d_search = d.copy()
    d_search[0, 0] = 0
    d_search[0, 1] = 0
    d_search[1, 0] = 0
    d_search[1, 1] = 0
    max_pos = np.unravel_index(np.argmax(np.abs(d_search)), d_search.shape)
    spikes.append((max_pos, d[max_pos]))

print("Spikes in first 30 blocks:")
for i, (pos, val) in enumerate(spikes):
    print(f"Block {i:2d}: {pos} -> {val:.2f}")
