import sys
import re
sys.path.insert(0, 'mobile_waf')
import detector

b = '------FormBoundaryAv1\\r\\nContent-Disposition: form-data; name="avatar"; filename="profile.png"\\r\\nContent-Type: image/png\\r\\n\\r\\n\\x89PNG IHDR 256x256 image data\\r\\n------FormBoundaryAv1--'

lines = [
    ("proto", lambda t: '__proto__' in t or 'constructor.prototype' in t),
    ("percent_crlf", lambda t: bool(re.search(r'%0[da]', t, re.I))),
    ("crlf_inject", lambda t: bool(re.search(r'(?:\\r\\n|\\r|\\n|[\r\n])\s*(?:Set-Cookie|Location|Content-Length|X-[\w-]+):\s*', t, re.I))),
    ("cd_inject", lambda t: bool(re.search(r'(?:\\r\\n|\\r|\\n|[\r\n])\s*Content-Disposition:\s*(?!form-data)', t, re.I))),
    ("http1", lambda t: bool(re.search(r'(?:%0d%0a|%0d|%0a|\\r\\n|\\r|\\n|[\r\n])\s*HTTP/1\.[01]', t, re.I))),
    ("redir", lambda t: bool(re.search(r'(?:redirect_uri|redirect|next|url)=https?://[^/]+@[^/]+', t, re.I))),
    ("null", lambda t: '%00' in t or '\x00' in t),
    ("smuggle", lambda t: bool(re.search(r'(?:GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\s+/[A-Za-z0-9_/.-]*\s+HTTP/1\.[01]', t))),
]

for comp in detector.normalize_variants(b):
    for name, fn in lines:
        if fn(comp):
            print(f"MATCH: {name} on {repr(comp[:70])}")
