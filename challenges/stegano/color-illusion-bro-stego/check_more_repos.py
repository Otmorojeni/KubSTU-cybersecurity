import urllib.request, json, re

# Search PyPI by simple index or search query
# We can search Google: site:pypi.org/project "dct" "steganography"
# Or search github for repositories
repos_to_check = [
    'bwm', 'blind-watermark', 'invisible-watermark', 'stegpy',
    'stegano', 'stego-lsb', 'dct-steganography', 'image-steganography',
    'watermark', 'dctstego', 'dct-watermark', 'py-stego',
    'openstego', 'jsteg', 'f5', 'outguess', 'steghide'
]

# Let's search GitHub code for "Look into 8x8" or "key-bro" or "stego_hint"
# We have search_web tool!
