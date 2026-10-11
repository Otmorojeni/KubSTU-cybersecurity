"""
Discrete Ricci flow on the moduli space of elliptic curves over F_p.
===================================================================

Following Hamilton's programme and Perelman's subsequent refinements,
we consider a discrete analogue of the classical Ricci flow

                        ∂g/∂t = -2 · Ric(g)

adapted to the finite-field setting.  The ambient object is the family
of Weierstrass elliptic curves

                E_{a,b}: y² = x³ + a·x + b     (over F_p)

parameterised by (a, b) ∈ F_p² away from the discriminant locus
Δ = { (a, b) : 4a³ + 27b² ≡ 0 mod p }.

The "curvature functional" is the (mod-p reduction of the) discriminant
proxy

                    K(a, b) := 4a³ + 27b²   (mod p)

which encodes the singularity behaviour of E_{a,b}.  We evolve the pair
(a, b) by discrete gradient descent on ½ K²:

    a_{n+1} = a_n - η · K(a_n, b_n) · ∂K/∂a  (mod p)
            = a_n - 12·η · a_n² · K(a_n, b_n)

    b_{n+1} = b_n - η · K(a_n, b_n) · ∂K/∂b  (mod p)
            = b_n - 54·η · b_n · K(a_n, b_n)

Iterating N times yields the cascade E_0 ⟶ E_1 ⟶ … ⟶ E_N.

By analogy with Perelman's Ricci flow with surgery, one may attempt to
recover the initial data (a_0, b_0) from the terminal data (a_N, b_N)
via backward reconstruction. Formally this requires inverting the flow
map Φ_N : F_p² → F_p², which is a well-posed problem on the smooth
locus.  In the discrete setting the flow is degenerate and the moduli
space of preimages carries a non-trivial fibration.
"""

p   = 4003    # prime characteristic
N   = 30      # cascade depth
eta = 1       # flow step size


def ricci_step(a: int, b: int) -> tuple[int, int]:
    K = (4 * pow(a, 3, p) + 27 * pow(b, 2, p)) % p
    a_new = (a - 12 * eta * pow(a, 2, p) * K) % p
    b_new = (b - 54 * eta * b * K) % p
    return a_new, b_new


def cascade(a0: int, b0: int) -> tuple[int, int]:
    a, b = a0, b0
    for _ in range(N):
        a, b = ricci_step(a, b)
    return a, b
