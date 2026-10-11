from fractions import Fraction
import random

def lll_incremental(B_orig, delta=Fraction(3, 4)):
    n = len(B_orig)
    dim = len(B_orig[0])
    B = [[Fraction(x) for x in b] for b in B_orig]
    
    # Initial Gram-Schmidt
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

    def size_reduce(k, l):
        if abs(mu[k][l]) > Fraction(1, 2):
            q = round(mu[k][l])
            for d in range(dim):
                B[k][d] -= q * B[l][d]
            for j in range(l):
                mu[k][j] -= q * mu[l][j]
            mu[k][l] -= q

    k = 1
    steps = 0
    while k < n:
        steps += 1
        size_reduce(k, k - 1)
        
        # Lovasz condition
        if B_sq[k] >= (delta - mu[k][k - 1]**2) * B_sq[k - 1]:
            for l in range(k - 2, -1, -1):
                size_reduce(k, l)
            k += 1
        else:
            u = mu[k][k - 1]
            B_prev = B_sq[k - 1]
            B_curr = B_sq[k]
            B_new = B_curr + u * u * B_prev
            
            u_new = u * B_prev / B_new
            factor = B_curr / B_new
            
            B_sq[k - 1] = B_new
            B_sq[k] = B_prev * factor
            
            # Swap vectors B[k] and B[k-1]
            B[k], B[k - 1] = B[k - 1], B[k]
            
            # Update mu for columns j < k - 1
            for j in range(k - 1):
                mu[k - 1][j], mu[k][j] = mu[k][j], mu[k - 1][j]
                
            mu[k][k - 1] = u_new
            
            # Update mu for subsequent rows i > k
            for i in range(k + 1, n):
                t = mu[i][k - 1]
                mu[i][k - 1] = t * u_new + mu[i][k] * factor
                mu[i][k] = t - u * mu[i][k]
                
            k = max(k - 1, 1)

    return [[int(x) for x in b] for b in B]

# Test with a small subset sum
w_test = [random.randint(10**5, 10**6) for _ in range(10)]
x_test = [random.choice([0, 1]) for _ in range(10)]
s_test = sum(x * w for x, w in zip(x_test, w_test))
print("Target x:", x_test)

lattice = []
for i in range(10):
    row = [0] * 11
    row[i] = 1
    row[10] = w_test[i]
    lattice.append(row)
row_s = [0] * 11
row_s[10] = s_test
lattice.append(row_s)

reduced = lll_incremental(lattice)
for r in reduced:
    if r[-1] == 0 and set(r[:-1]).issubset({-1, 0, 1}) and any(r[:-1]):
        print("Found vector:", r)
