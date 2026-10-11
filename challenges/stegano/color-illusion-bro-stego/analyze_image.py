import numpy as np
from PIL import Image

img = Image.open('bro_stego_with_hint.png')
print("Image size:", img.size)
print("Image mode:", img.mode)
print("Image info:", img.info)

arr = np.array(img)
print("Array shape:", arr.shape)

# Let's check 8x8 blocks!
# 1280 x 1280 = exactly 160 x 160 blocks of 8x8!
print("1280 / 8 =", 1280 // 8)
