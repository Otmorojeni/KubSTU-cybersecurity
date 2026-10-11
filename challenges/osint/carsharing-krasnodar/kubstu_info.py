import requests, re, sys
sys.stdout.reconfigure(encoding='utf-8')

r = requests.get('https://kubstu.ru/s-8', headers={'User-Agent': 'Mozilla/5.0'}, verify=False)
text = r.text
lines = [l for l in text.split('\n') if any(w in l for w in ['Красная', 'Московская', 'Старокубанская', 'Красина', 'корпус'])]
for l in lines[:20]:
    clean = re.sub(r'<[^>]+>', ' ', l).strip()
    if clean:
        print(clean)
