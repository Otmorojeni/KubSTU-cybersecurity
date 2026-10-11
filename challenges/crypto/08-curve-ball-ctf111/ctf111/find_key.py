import solve1
from Crypto.Cipher import AES

with open('solve1.py', encoding='utf-8') as f:
    text = f.read()

target = 'clean = res.strip()'
replacement = '''print("MATCHED KEY HEX:", key[:lk].hex())
                clean = res.strip()'''
text = text.replace(target, replacement, 1)

with open('solve1_mod.py', 'w', encoding='utf-8') as f:
    f.write(text)

import solve1_mod
solve1_mod.main()
