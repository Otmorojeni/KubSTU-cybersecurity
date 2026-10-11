import urllib.request, urllib.parse, json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for query in ['bro_stego', 'bro-stego', '"key-bro"', 'stego "8x8 frequency"', 'dct stego "key"']:
    url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read().decode('utf-8'))
            print(f"Query '{query}': Abstract = {data.get('Abstract')}")
            for t in data.get('RelatedTopics', [])[:3]:
                if 'Text' in t:
                    print(f"  Topic: {t['Text']}")
    except Exception as e:
        print(f"Error {query}: {e}")
