with open('solve1_mod.py', encoding='utf-8') as f:
    text = f.read()

text = 'mat_map = {}\n' + text
text = text.replace('candidate_keys.add(hashlib.sha256(mat).digest())', 
                    'd = hashlib.sha256(mat).digest(); candidate_keys.add(d); mat_map[d] = mat')
text = text.replace('clean = res.strip()',
                    'print("MATCHED MAT:", repr(mat_map.get(key[:lk]))); clean = res.strip()')

with open('solve1_mod2.py', 'w', encoding='utf-8') as f:
    f.write(text)

import solve1_mod2
solve1_mod2.main()
