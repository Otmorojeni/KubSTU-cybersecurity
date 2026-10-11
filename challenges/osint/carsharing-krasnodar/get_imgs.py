import re

with open(r'C:\Users\maksi\.gemini\antigravity\brain\f1c75ae7-cc66-4f77-aa9c-290803fdb9a9\.system_generated\steps\339\content.md', 'r', encoding='utf-8') as f:
    text = f.read()

imgs = re.findall(r'https?://[^\s"\'<>]+\.(?:jpg|png|webp)', text)
for img in set(imgs):
    print("Found image:", img)
