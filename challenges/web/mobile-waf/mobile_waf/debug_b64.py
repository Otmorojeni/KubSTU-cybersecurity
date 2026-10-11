import sys
import os
import urllib.parse
sys.path.insert(0, 'mobile_waf')
import detector

q = 'enc=base64&intro=e3sgY29uZmlnLl9fY2xhc3NfXy5fX2luaXRfXy5fX2dsb2JhbHNfX1snb3MnXS5wb3BlbignaWQnKS5yZWFkKCkgfX0%3D'
uq = urllib.parse.unquote(q)
print("uq:", uq)
decs = detector.try_b64decode(uq)
print("decs:", decs)
req = {'path': '/newsletter/preview', 'query': q, 'body': '', 'headers': {}}
print("PREDICT:", detector.predict(req))
