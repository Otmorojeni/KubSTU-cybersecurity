import json
import sys
sys.path.insert(0, 'mobile_waf')
import detector

with open("mobile_waf/dataset.jsonl", "r", encoding="utf-8") as f:
    seen = set()
    for line in f:
        item = json.loads(line)
        gt = item.get("ground_truth")
        if not gt: continue
        pred = detector.predict(item)
        if pred != gt:
            key = (item.get("path"), item.get("query"), item.get("body")[:50])
            if key in seen:
                continue
            seen.add(key)
            print("="*60)
            print(f"ROUND {item.get('round')} | GT: {gt} | PRED: {pred} | CAT: {item.get('category')}")
            print(f"METHOD: {item.get('method')} PATH: {item.get('path')} QUERY: {item.get('query')}")
            print(f"HEADERS: {item.get('headers')}")
            print(f"BODY: {item.get('body')}")
