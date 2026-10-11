import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("profile.html", "r", encoding="utf-8") as f:
    prof = f.read()

with open("balance.html", "r", encoding="utf-8") as f:
    bal = f.read()

print("--- PROFILE SUMMARY ---")
lines = [l.strip() for l in prof.split("\n") if l.strip()]
for l in lines:
    if any(k in l.lower() for k in ["balance", "rub", "user", "order", "purchase", "lot", "id", "role", "0"]):
        print(" ", l[:100])

print("\n--- BALANCE SUMMARY ---")
lines = [l.strip() for l in bal.split("\n") if l.strip()]
for l in lines:
    if any(k in l.lower() for k in ["top up", "balance", "rub", "sbp", "form", "action", "amount", "method", "pay", "<form"]):
        print(" ", l[:100])
