import urllib.request

url = "http://159.194.250.157:8080/.env.example"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as r:
    print(r.read().decode("utf-8"))
