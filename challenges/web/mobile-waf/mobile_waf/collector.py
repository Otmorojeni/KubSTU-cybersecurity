import socket
import json
import os
import sys
import re

# Flush immediately
sys.stdout.reconfigure(line_buffering=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import detector

DATASET_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset.jsonl")

def run_collector(num_attempts=15):
    for attempt in range(num_attempts):
        print(f"=== Running attempt {attempt+1}/{num_attempts} ===")
        try:
            s = socket.socket()
            s.settimeout(5.0)
            s.connect(('193.168.46.146', 32222))
            f = s.makefile('rw', encoding='utf-8')
            
            history = []
            flag_found = None
            
            while True:
                line = f.readline()
                if not line:
                    break
                line = line.strip()
                if not line:
                    continue
                if line.startswith('#'):
                    print("SRV:", line)
                    if "wrong at round" in line:
                        m = re.search(r'wrong at round (\d+): expected (\w+)(?: \(([^)]+)\))?', line)
                        if m and history:
                            r_num = int(m.group(1))
                            expected = m.group(2)
                            cat = m.group(3) or "unknown"
                            # All rounds before the last one were correct
                            for req, verd in history[:-1]:
                                req['ground_truth'] = verd
                                with open(DATASET_FILE, 'a', encoding='utf-8') as out:
                                    out.write(json.dumps(req) + '\n')
                            # The last round was wrong, so ground truth is expected
                            last_req, _ = history[-1]
                            last_req['ground_truth'] = expected
                            last_req['category'] = cat
                            with open(DATASET_FILE, 'a', encoding='utf-8') as out:
                                out.write(json.dumps(last_req) + '\n')
                            print(f"Recorded failure at round {r_num}: expected {expected} ({cat})")
                        break
                    elif "flag" in line.lower() or "kubstu" in line.lower() or "ctf" in line.lower():
                        print("FLAG!!!", line)
                        flag_found = line
                        break
                elif line.startswith('{'):
                    req = json.loads(line)
                    verdict = detector.predict(req)
                    print(f"R{req.get('round')}: predicted {verdict}")
                    history.append((req, verdict))
                    f.write(verdict + '\n')
                    f.flush()
            s.close()
            if flag_found:
                print("FOUND FLAG:", flag_found)
                break
        except Exception as e:
            print("Conn error:", e)

if __name__ == '__main__':
    run_collector()

