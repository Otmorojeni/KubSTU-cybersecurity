import urllib.request, json

for q in ['bro_stego', 'bro-stego', 'brostego', 'key-bro']:
    url = f'https://api.github.com/search/repositories?q={q}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read().decode())
            print(f"Query {q}: total={data.get('total_count')}")
            for item in data.get('items', [])[:3]:
                print('  ', item.get('full_name'), '->', item.get('description'))
    except Exception as e:
        print(f"Query {q}: error", e)
