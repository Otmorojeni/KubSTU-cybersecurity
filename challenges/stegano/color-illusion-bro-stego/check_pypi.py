import urllib.request
import json

# Search PyPI or query PyPI packages
# Let's list packages with "dct" and "stego"
import urllib.parse
import xmlrpc.client

# PyPI XML-RPC is disabled, but warehouse search:
url = "https://pypi.org/pypi?%3Aaction=search&term=dct+steganography"
# Or search via simple warehouse json search if possible:
# Let's search packages like 'dct-steganography', 'steganography-dct', 'stego-dct', etc.
test_pkgs = [
    'stegano', 'dct-steganography', 'steganography', 'dctstego', 'dct-watermark',
    'invisible-watermark', 'image-steganography', 'stego', 'dct_stego', 'dct_steganography',
    'blind-watermark', 'watermark', 'qim', 'f5-steganography', 'stegpy'
]

for pkg in test_pkgs:
    try:
        req = urllib.request.Request(f"https://pypi.org/pypi/{pkg}/json", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as r:
            data = json.loads(r.read().decode())
            info = data.get('info', {})
            print(f"FOUND PyPI: {pkg} -> {info.get('summary')}")
    except Exception as e:
        pass
