import requests, re, sys
sys.stdout.reconfigure(encoding='utf-8')

r = requests.get('https://t.me/s/kubCTF', headers={'User-Agent': 'Mozilla/5.0'})
posts = re.findall(r'<div class="tgme_widget_message_text[^>]*>(.*?)</div>', r.text, re.DOTALL)
print(f"Total posts found: {len(posts)}")
for i, p in enumerate(posts[-10:]):
    clean = re.sub(r'<[^>]+>', ' ', p).strip()
    print(f"--- POST {i+1} ---")
    print(clean)
