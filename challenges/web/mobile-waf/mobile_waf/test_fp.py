import sys
sys.path.insert(0, 'mobile_waf')
import detector

b = '{"content":"UNION ALL keeps duplicates while UNION removes them; measure both on your data."}'
for comp in detector.normalize_variants(b):
    for name in dir(detector):
        if name.startswith('check_'):
            fn = getattr(detector, name)
            if fn(comp):
                print(name, 'on', repr(comp))
