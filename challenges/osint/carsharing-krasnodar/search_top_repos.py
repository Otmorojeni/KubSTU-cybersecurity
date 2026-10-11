import urllib.request, json

queries = [
    'dct steganography language:python',
    'dct watermark language:python',
    'dct stego language:python',
    'frequency steganography language:python'
]

for q in queries:
    url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(q)}&sort=stars"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read().decode())
            print(f"=== Query: {q} (Total: {data.get('total_count')}) ===")
            for item in data.get('items', [])[:5]:
                print(f"  {item.get('full_name')} ({item.get('stargazers_count')} stars): {item.get('description')}")
    except Exception as e:
        print(f"Error for {q}:", e)
