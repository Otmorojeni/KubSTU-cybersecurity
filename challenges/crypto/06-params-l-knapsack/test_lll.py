from fractions import Fraction
import random

def gram_schmidt(B):
    n = len(B)
    dim = len(B[0])
    B_star = [[Fraction(x) for x in b] for b in B]
    mu = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(i):
            num = sum(B[i][d] * B_star[j][d] for d in range(dim))
            den = sum(B_star[j][d] * B_star[j][d] for d in range(dim))
            mu[i][j] = num / den
            for d in range(dim):
                B_star[i][d] -= mu[i][j] * B_star[j][d]
    return B_star, mu

def dot(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))

def lll_exact(B, delta=Fraction(3, 4)):
    n = len(B)
    dim = len(B[0])
    B = [list(b) for b in B]
    
    def recompute():
        B_star = [[Fraction(x) for x in b] for b in B]
        mu = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        B_sq = [Fraction(0) for _ in range(n)]
        for i in range(n):
            for j in range(i):
                num = sum(B[i][d] * B_star[j][d] for d in range(dim))
                den = B_sq[j]
                mu[i][j] = num / den
                for d in range(dim):
                    B_star[i][d] -= mu[i][j] * B_star[j][d]
            B_sq[i] = sum(B_star[i][d] * B_star[i][d] for d in range(dim))
        return B_star, mu, B_sq

    B_star, mu, B_sq = recompute()
    k = 1
    steps = 0
    while k < n:
        steps += 1
        # Size reduction
        for j in range(k - 1, -1, -1):
            if abs(mu[k][j]) > Fraction(1, 2):
                q = round(mu[k][j])
                for d in range(dim):
                    B[k][d] -= q * B[j][d]
                # Recompute Gram-Schmidt when basis changes
                B_star, mu, B_sq = recompute()
                
        # Lovasz condition
        if B_sq[k] >= (delta - mu[k][k - 1]**2) * B_sq[k - 1]:
            k += 1
        else:
            B[k], B[k - 1] = B[k - 1], B[k]
            B_star, mu, B_sq = recompute()
            k = max(k - 1, 1)
            
    print(f"Finished in {steps} steps")
    return B

# Test with a small subset sum
w_test = [random.randint(10**5, 10**6) for _ in range(10)]
x_test = [random.choice([0, 1]) for _ in range(10)]
s_test = sum(x * w for x, w in zip(x_test, w_test))
print("Target x:", x_test)

# Build lattice (CLOS style or Lagarias-Odlyzko)
# Lagarias-Odlyzko:
# b_i = (0, ..., 1, ..., 0, w_i)
# b_{n} = (0, ..., 0, s_test)
lattice = []
for i in range(10):
    row = [0] * 11
    row[i] = 1
    row[10] = w_test[i]
    lattice.append(row)
row_s = [0] * 11
row_s[10] = s_test
lattice.append(row_s)

reduced = lll_exact(lattice)
for r in reduced:
    if r[-1] == 0 and set(r[:-1]).issubset({-1, 0, 1}):
        print("Found vector:", r)
