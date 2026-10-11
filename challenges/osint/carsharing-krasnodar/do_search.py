import search_ddg

queries = [
    'Look into 8x8 frequency blocks',
    'key-bro stego',
    'stego "key-bro"',
    'На заводе стих шум но кое-что всё ещё работает на своих частотах',
    'bro_stego'
]

for q in queries:
    print("=== Query:", q)
    search_ddg.search(q)
