import urllib.request, urllib.parse, re

phrase = '"На заводе стих шум"'
url = 'https://yandex.ru/search/?text=' + urllib.parse.quote(phrase)
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = resp.read().decode('utf-8', errors='ignore')
        print("Yandex data len:", len(data))
        # check if robot captcha
        if "captcha" in data.lower():
            print("Yandex captcha")
        else:
            snippets = re.findall(r'<div class="OrganicTextContent[^"]*">(.*?)</div>', data)
            print("Snippets found:", len(snippets))
            for s in snippets:
                print(" ", re.sub(r'<[^>]+>', '', s))
except Exception as e:
    print("Error:", e)
