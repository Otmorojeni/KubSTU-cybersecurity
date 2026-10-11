import json
import sys
sys.path.insert(0, 'mobile_waf')
import detector

with open('mobile_waf/dataset.jsonl', encoding='utf-8') as f:
    total = 0
    correct = 0
    mismatches = []
    for line in f:
        data = json.loads(line)
        truth = data.get('ground_truth')
        if not truth:
            continue
        total += 1
        pred = detector.predict(data)
        if pred == truth:
            correct += 1
        else:
            mismatches.append((data.get('round'), data.get('category'), truth, pred, data))

print(f"Accuracy on all samples: {correct}/{total} ({correct/total*100:.1f}%)")
for r, cat, t, p, d in mismatches:
    print(f"MISMATCH Round {r} cat={cat} ground_truth={t} my_pred={p}")
    print("  path:", d.get('path'))
    print("  query:", d.get('query'))
    print("  body:", d.get('body')[:100] if d.get('body') else '')
