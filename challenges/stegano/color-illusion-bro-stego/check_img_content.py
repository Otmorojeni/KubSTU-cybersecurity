from PIL import Image
import numpy as np

img = Image.open('bro_stego_with_hint.png')
print("Format:", img.format, "Size:", img.size, "Mode:", img.mode)

# Save a downscaled thumbnail or inspect some crops
arr = np.array(img)
print("Channels min/max/mean:")
for c, name in enumerate(['R', 'G', 'B']):
    print(f"{name}: min={arr[:,:,c].min()}, max={arr[:,:,c].max()}, mean={arr[:,:,c].mean():.2f}, std={arr[:,:,c].std():.2f}")

# Check if channels are identical (grayscale saved as RGB)
print("Is R == G?", np.array_equal(arr[:,:,0], arr[:,:,1]))
print("Is G == B?", np.array_equal(arr[:,:,1], arr[:,:,2]))

# Check unique values
print("Unique values in R:", len(np.unique(arr[:,:,0])))

# Check if there is text in the image visually
thumb = img.resize((320, 320))
thumb.save('thumb.png')
print("Saved thumb.png")
