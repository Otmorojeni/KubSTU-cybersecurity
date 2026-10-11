import numpy as np
from PIL import Image
import random

sign_img = Image.open('spike_sign_map.png')
sign_arr = np.array(sign_img).flatten()

print("Sign array shape:", sign_arr.shape)

keys_to_test = ["key-bro", "bro", "key_bro", "bro_stego", "bro_stego_with_hint"]

for key in keys_to_test:
    # Pattern 1: random.shuffle on indices
    indices = list(range(len(sign_arr)))
    random.seed(key)
    random.shuffle(indices)
    
    # Unshuffle: unperm[indices[i]] = sign_arr[i] or unperm[i] = sign_arr[indices[i]]
    unperm1 = np.zeros_like(sign_arr)
    unperm2 = np.zeros_like(sign_arr)
    for i, idx in enumerate(indices):
        unperm1[idx] = sign_arr[i]
        unperm2[i] = sign_arr[idx]
        
    im1 = Image.fromarray(unperm1.reshape((160, 160)))
    im2 = Image.fromarray(unperm2.reshape((160, 160)))
    
    im1.save(f'unshuffle_{key}_1.png')
    im2.save(f'unshuffle_{key}_2.png')

print("Saved unshuffle images for all keys!")
