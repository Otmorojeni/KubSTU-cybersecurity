import cv2
import struct
import bitstring
import numpy as np
import zigzag as zz
import data_embedding as stego
import image_preparation as img

stego_image = cv2.imread("bro_stego_with_hint.png", flags=cv2.IMREAD_COLOR)
stego_image_f32 = np.float32(stego_image)
stego_image_YCC = img.YCC_Image(cv2.cvtColor(stego_image_f32, cv2.COLOR_BGR2YCrCb))

print("Channels shape:", len(stego_image_YCC.channels[0]))

dct_blocks = [cv2.dct(block) for block in stego_image_YCC.channels[0]]
dct_quants = [np.around(np.divide(item, img.JPEG_STD_LUM_QUANT_TABLE)) for item in dct_blocks]
sorted_coefficients = [zz.zigzag(block) for block in dct_quants]

recovered_data = stego.extract_encoded_data_from_DCT(sorted_coefficients)
print("Recovered data length in bits:", len(recovered_data))

recovered_data.pos = 0
try:
    data_len = int(recovered_data.read('uint:32') / 8)
    print("Data len from header:", data_len)
    extracted_data = bytes()
    for _ in range(min(data_len, 200)):
        extracted_data += struct.pack('>B', recovered_data.read('uint:8'))
    print("Extracted data:", extracted_data)
except Exception as e:
    print("Error:", e)

# Also inspect first 200 bits of recovered_data
recovered_data.pos = 0
bits_sample = recovered_data.read('bin:64')
print("First 64 bits:", bits_sample)
