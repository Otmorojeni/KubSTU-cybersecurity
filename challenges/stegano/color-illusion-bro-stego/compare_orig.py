from PIL import Image
import numpy as np

orig = Image.open('orig_meme.jpg')
stego = Image.open('bro_stego_with_hint.png')

print("Orig size:", orig.size)
print("Stego size:", stego.size)

# If we resize orig to 1280x1280:
orig_1280 = orig.resize((1280, 1280), Image.Resampling.LANCZOS)
arr_orig = np.array(orig_1280, dtype=np.float32)
arr_stego = np.array(stego, dtype=np.float32)

diff = np.abs(arr_stego - arr_orig)
print("Mean diff (LANCZOS):", diff.mean())

for resample, name in [
    (Image.Resampling.NEAREST, 'NEAREST'),
    (Image.Resampling.BILINEAR, 'BILINEAR'),
    (Image.Resampling.BICUBIC, 'BICUBIC'),
    (Image.Resampling.LANCZOS, 'LANCZOS'),
    (Image.Resampling.BOX, 'BOX')
]:
    o = orig.resize((1280, 1280), resample)
    d = np.abs(arr_stego - np.array(o, dtype=np.float32))
    print(f"Mean diff ({name}):", d.mean())
