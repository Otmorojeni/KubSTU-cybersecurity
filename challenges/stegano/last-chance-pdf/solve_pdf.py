import re
import io
import base64
import hashlib
from PIL import Image
import numpy as np
import cv2
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def solve(pdf_path: str):
    with open(pdf_path, 'rb') as f:
        pdf_data = f.read()

    # 1. Extract QR parts from metadata in 9 0 obj
    m_p1 = re.search(rb'QR_PART1:([A-Za-z0-9+/=]+)', pdf_data)
    m_p2 = re.search(rb'QR_PART2:([A-Za-z0-9+/=]+)', pdf_data)
    
    if not m_p1 or not m_p2:
        raise ValueError("Could not find QR parts in metadata")

    im1 = Image.open(io.BytesIO(base64.b64decode(m_p1.group(1))))
    im2 = Image.open(io.BytesIO(base64.b64decode(m_p2.group(1))))

    # Stitch QR code vertically: 145x72 + 145x73 = 145x145
    qr_img = Image.new('RGB', (145, 145))
    qr_img.paste(im1, (0, 0))
    qr_img.paste(im2, (0, 72))

    # Decode QR Code
    detector = cv2.QRCodeDetector()
    cv_img = cv2.cvtColor(np.array(qr_img), cv2.COLOR_RGB2BGR)
    decoded_text, _, _ = detector.detectAndDecode(cv_img)
    print(f"[*] Decoded QR text: {decoded_text}") # salt=7f3c92a1b4e5

    salt = decoded_text.split('salt=')[1].encode('utf-8')

    # 2. Extract password / IV candidate from 100 0 obj
    # stream: ff0400000000ff05020010 61316232633364346535663637383930 ff0300000001
    m_100 = re.search(rb'100 0 obj.*?stream\r?\n([0-9a-fA-F]+)\r?\nendstream', pdf_data, re.DOTALL)
    raw_100_hex = m_100.group(1).decode('ascii')
    # 61316232633364346535663637383930 in hex is 'a1b2c3d4e5f67890'
    key_pwd = bytes.fromhex('61316232633364346535663637383930') # b'a1b2c3d4e5f67890'
    iv = key_pwd
    print(f"[*] Extracted key/IV: {key_pwd.decode('ascii')}")

    # 3. Extract ciphertext from 102 0 obj
    m_102 = re.search(rb'102 0 obj.*?stream\r?\n([0-9a-fA-F]+)\r?\nendstream', pdf_data, re.DOTALL)
    ct = bytes.fromhex(m_102.group(1).decode('ascii'))
    print(f"[*] Ciphertext length: {len(ct)} bytes")

    # 4. Decrypt AES-256-CBC with key = sha256(salt + password)
    derived_key = hashlib.sha256(salt + key_pwd).digest()
    cipher = AES.new(derived_key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), 16)
    flag = pt.decode('utf-8')
    print(f"\n[+] Flag successfully decrypted: {flag}")
    return flag

if __name__ == '__main__':
    solve(r'C:\Users\maksi\OneDrive\Рабочий стол\otmorojeni\KubSTU-cybersecurity\last chance.pdf')
