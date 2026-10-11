import socket
import json
import os
import sys
import re
import time

sys.stdout.reconfigure(line_buffering=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import detector

DATASET_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset.jsonl")
HOST = "193.168.46.146"
PORT = 32222

def attempt_solve():
    print(f"\n[+] Connecting to {HOST}:{PORT}...")
    s = socket.socket()
    s.settimeout(10.0)
    s.connect((HOST, PORT))
    f = s.makefile('rw', encoding='utf-8')
    
    rounds_history = []
    round_count = 0
    
    try:
        while True:
            line = f.readline()
            if not line:
                print("[-] Connection closed by server.")
                break
            line = line.strip()
            if not line:
                continue
                
            if '"round"' in line:
                if round_count % 10 == 0 or round_count == 0 or round_count > 90:
                    print(f"[SRV] {line[:100]}...")
            else:
                print(f"[SRV] {line}")
            
            # Check for flag anywhere in any line
            if any(kw in line.lower() for kw in ["kubstu{", "flag{", "kubstu"]):
                print("\n" + "="*50)
                print(f"[!!!] FLAG RECEIVED: {line}")
                print("="*50 + "\n")
                with open("flag.txt", "w", encoding="utf-8") as fl:
                    fl.write(line + "\n")
                return True

            if line.startswith('#'):
                if "wrong at round" in line:
                    m = re.search(r'wrong at round (\d+): expected (\w+)(?: \(([^)]+)\))?', line)
                    if m and rounds_history:
                        r_num = int(m.group(1))
                        expected = m.group(2)
                        cat = m.group(3) or "unknown"
                        # All rounds before the last one were correct
                        for r_item, verd in rounds_history[:-1]:
                            r_item['ground_truth'] = verd
                            with open(DATASET_FILE, 'a', encoding='utf-8') as out:
                                out.write(json.dumps(r_item) + '\n')
                        # The last round was wrong
                        last_req, my_verd = rounds_history[-1]
                        last_req['ground_truth'] = expected
                        last_req['category'] = cat
                        with open(DATASET_FILE, 'a', encoding='utf-8') as out:
                            out.write(json.dumps(last_req) + '\n')
                        print(f"[-] FAILED at Round {r_num} (my verdict: {my_verd}, expected: {expected}, category: {cat})")
                    return False
            elif line.startswith('{'):
                req = json.loads(line)
                if 'flag' in req:
                    print("\n" + "="*50)
                    print(f"[!!!] FLAG FOUND IN JSON: {req}")
                    print("="*50 + "\n")
                    with open("flag.txt", "w", encoding="utf-8") as fl:
                        fl.write(str(req) + "\n")
                    return True

                r_num = req.get('round')
                if r_num is None:
                    print(f"[?] Unknown JSON received after rounds: {req}")
                    continue

                round_count = r_num
                verdict = detector.predict(req)
                rounds_history.append((req, verdict))
                if r_num % 10 == 0 or r_num == 1 or r_num > 90:
                    print(f"[*] Round {r_num:3d}/100 -> {verdict}")
                f.write(verdict + '\n')
                f.flush()
                
        # If connection loop ended, check remaining
        time.sleep(1)
        while True:
            rem = f.readline()
            if not rem:
                break
            rem = rem.strip()
            print(f"[SRV_REM] {rem}")
            if any(kw in rem.lower() for kw in ["kubstu", "ctf", "flag{", "}"]):
                print("\n" + "="*50)
                print(f"[!!!] FLAG RECEIVED: {rem}")
                print("="*50 + "\n")
                with open("flag.txt", "w", encoding="utf-8") as fl:
                    fl.write(rem + "\n")
                return True
                
    except Exception as e:
        print(f"[-] Exception: {e}")
        return False
    finally:
        s.close()
    return False

if __name__ == '__main__':
    max_tries = 5
    for t in range(1, max_tries + 1):
        print(f"\n==========================================")
        print(f"           SOLVE ATTEMPT {t}/{max_tries}")
        print(f"==========================================")
        success = attempt_solve()
        if success:
            print("[+] Solved successfully!")
            break
        time.sleep(1)
