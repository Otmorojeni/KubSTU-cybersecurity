import sys
sys.path.insert(0, 'mobile_waf')
import detector

test_req = {
    'path': '/api/v1/support/tickets',
    'query': '',
    'headers': {},
    'body': '------FormBoundaryTk7\\r\\nContent-Disposition: form-data; name="subject"\\r\\n\\r\\nGrinder arrived with chipped burrs\\r\\n------FormBoundaryTk7\\r\\nContent-Disposition: form-data; name="description"\\r\\n\\r\\nPlease advise on replacement burr set.\\r\\n------FormBoundaryTk7--'
}

for name in dir(detector):
    if name.startswith('check_'):
        fn = getattr(detector, name)
        for comp in detector.normalize_variants(test_req['body']):
            if fn(comp):
                print('TRIGGERED BY:', name, 'on', repr(comp))
