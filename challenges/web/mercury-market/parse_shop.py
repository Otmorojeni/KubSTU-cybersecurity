import re

with open("shop_index.html", "r", encoding="utf-8") as f:
    html = f.read()

print("Title:", re.findall(r"<title>(.*?)</title>", html, re.I))

# Extract links
links = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', html, re.DOTALL)
print("\n--- Links ---")
for href, text in links:
    clean_text = " ".join(text.split())
    if clean_text:
        print(f"{href}: {clean_text}")

# Extract forms
forms = re.findall(r'<form\s+[^>]*>(.*?)</form>', html, re.DOTALL | re.I)
print(f"\n--- Forms ({len(forms)}) ---")
for i, f in enumerate(forms):
    inputs = re.findall(r'<input\s+[^>]*>', f)
    buttons = re.findall(r'<button\s+[^>]*>(.*?)</button>', f, re.DOTALL)
    print(f"Form {i}: inputs={inputs}, buttons={buttons}")

# Extract cards/products
items = re.findall(r'class="[^"]*card[^"]*"[\s\S]*?</div>\s*</div>', html)
print(f"\n--- Cards/Products ({len(items)}) ---")
for item in items[:5]:
    print("--- Item ---")
    print("\n".join([line.strip() for line in item.split("\n") if line.strip()][:10]))
