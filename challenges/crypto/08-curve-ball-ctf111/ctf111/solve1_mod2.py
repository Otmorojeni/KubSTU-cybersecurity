mat_map = {}
#!/usr/bin/env python3
import hashlib
import json
import math
import base64
from math import isqrt
from Crypto.Cipher import AES

# =========================================================
# Данные из challenge.txt
# =========================================================

p1 = 318428245402619537414820208773891746650767495354401236030916605907128136239369
a1 = 108620435174389634112113673518213075602275545623531184675747067353450096044209
a2 = 291848496494850736646873509046985800803095256965982889112919469328942383520745
a3 = 73032488072778263333266323422601579336898807417217410472944889244293435141358
a4 = 280183993196378234014968775252200865859664535599341587881283703952201820028306
a6 = 119678007635170787162487494714420262867493495555728821931762472093368708431108

G1 = (
    222341296145310091723504511342188707135845292770149322137448425397070617705535,
    223665394076581383410427926494785195064315391986845619384592650445758335539966,
)
P1 = (
    262455612829307412919032917075162247105068203848077042831221438318023824117168,
    124171721592965649429610674354978243940820800527405505321255135047676589916034,
)

p3 = 115792089237316196275616121189559184590969122206767713959943689392442706417673
c1 = 71265293299717771883798387058118597809584749802270533394901201910983626376258
c2 = 69571399483760146292671071195379788636190567782968108857394500862151716487058
c3 = 10045000482310543026641992807939524639298570626326265501764807441840790465347
c4 = 105552733552974323836076801773112344453798917640134142861353136173007316243868
c6 = 71049214526452535502755747511237958734660085707191776174375124318257517876178

G3 = (
    50757482523172514141592967119215026716428260442562501095500506444662456584757,
    76185377023309760904991264561286078444353955955053899812269171211243318210387,
)
P3 = (
    100076091983897006476695354799375462856129465686228333745954151093956552901898,
    61284794136931225887168223125830152379474204858165162385258610873699465911316,
)

c2_iv_hex = "96dd8a4293d3dd5b4d8069c2c47f0f6b"
c2_ct_hex = (
    "4da0cfd5b52911ccecff14ccd4f567170f8b4070aa17aa928fd1a57d6db922be"
    "bd21da930e212ec681fb5fb8dbabe20dd9a73362e140f289850c965085637733"
    "8400c260f028976c3fb0925980f87e9a37541086e89761542fd7d0de7a092061"
    "ef8ebddc6b295ce8103b010dfbb43f8f93be9850efd4718f106aa1fee8e1c874"
    "b9c064636633d54c76bd108b549cbbb0bb9f6e0b479110cd603b90ccbf983d72"
    "6e67811f84862e7bfd1872813ba60977dd07d3d2c99a0655d2717ca53ee8b69a"
    "91c9e3e4ae059725101fde94d26ff503a8ec7fe5c858ec7fbbae8db484d3d4a1"
    "4ba29958944daf80d67ff0662f306b48a055139fe178546b9c9b4e35002e5b92"
    "38565d7811007e9004cd43b9cc2ecfdbdc4d10676d20f31948838786299f9f13"
    "6c658167595dbb790ddf42742a34ea676c6c4298fcb555500f4f59065a76d838"
    "2a60d7238dd883b6c5d0d3d124ba17d883609d8cc42136e20b86112e1d817b96"
    "495114f1ba91f69b217da6986b448e177d8bd0b22e6e9c5ae19c4aebca07a967"
    "33f912d96af91627eb12041d2e7a1f101340f66d743320f980c754a8cc5eacd5"
    "24cce09840976fc03d38f0d96c8062a98aeefdaece289e5d8157b19ddd6348d5"
)

flag_iv_hex = "ef399b2910c055cb1894ce3f8ade3b72"
flag_ct_hex = (
    "c4d4a558aa9518172a3327c615815f349fdcd7cb212e8f8b0113046670247741"
    "d5fb3d6c1b4e1ce4f5e8a9cbac1598cd89672fd0e3f99886d434f2c6746ae55b"
    "072a15fa98478d6bd90d8e25cecc6fe8e291131dc83c9e57a3a772bc237b33eb"
    "145ee5ecb27d383134bb3357fcb9be36"
)

# =========================================================
# Уже проверенные секреты C1 и C2
# =========================================================

# C1: аномальная кривая, решена Smart's attack.
k1 = 103679294682318394632116352245965931281672926926560836357672813757452869481740

# C2: суперсингулярная y^2 = x^3 + x, порядок p2+1 гладкий, решена Pohlig-Hellman.
k2 = 216894608825153064084224188982807740771782288278332095102457164300855345783429

# =========================================================
# Малые утилиты
# =========================================================

def modinv(a, m):
    a %= m
    if a == 0:
        raise ZeroDivisionError("zero inverse")
    return pow(a, -1, m)


def legendre(a, p):
    a %= p
    return pow(a, (p - 1) // 2, p)


def sqrt_mod(a, p):
    a %= p
    if a == 0:
        return 0
    if p == 2:
        return a
    if legendre(a, p) != 1:
        return None
    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)

    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1

    z = 2
    while legendre(z, p) != p - 1:
        z += 1

    m = s
    c = pow(z, q, p)
    t = pow(a, q, p)
    r = pow(a, (q + 1) // 2, p)

    while t != 1:
        t2 = pow(t, 2, p)
        i = 1
        while t2 != 1:
            t2 = pow(t2, 2, p)
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        m = i
        c = pow(b, 2, p)
        t = (t * c) % p
        r = (r * b) % p

    return r


def crt(rems, mods):
    x = 0
    m = 1
    for r, mi in zip(rems, mods):
        g = math.gcd(m, mi)
        if (r - x) % g:
            return None
        mm = mi // g
        if mm == 1:
            t = 0
        else:
            t = (((r - x) // g) * modinv(m // g, mm)) % mm
        x = (x + m * t) % (m * mm)
        m *= mm
    return x % m


def factor_smooth(n, limit=1_000_000):
    """
    Полностью факторизует n, если все простые множители <= limit.
    Иначе возвращает None.
    """
    n = int(n)
    fac = {}

    cnt = 0
    while n % 2 == 0:
        cnt += 1
        n //= 2
    if cnt:
        fac[2] = cnt

    d = 3
    while d <= limit and d * d <= n:
        cnt = 0
        while n % d == 0:
            cnt += 1
            n //= d
        if cnt:
            fac[d] = cnt
        d += 2

    if n > 1:
        if n <= limit:
            fac[n] = fac.get(n, 0) + 1
        else:
            return None

    return fac


# =========================================================
# Арифметика общих эллиптических кривых Вейерштрасса
# y^2 + a1*x*y + a3*y = x^3 + a2*x^2 + a4*x + a6
# =========================================================

def gen_on_curve(P, p, a1, a2, a3, a4, a6):
    if P is None:
        return True
    x, y = P
    lhs = (y * y + a1 * x * y + a3 * y) % p
    rhs = (x * x * x + a2 * x * x + a4 * x + a6) % p
    return lhs == rhs


def gen_add(P, Q, p, a1, a2, a3, a4, a6):
    if P is None:
        return Q
    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q

    if x1 == x2:
        if (y1 + y2 + a1 * x2 + a3) % p == 0:
            return None
        num = (3 * x1 * x1 + 2 * a2 * x1 + a4 - a1 * y1) % p
        den = (2 * y1 + a1 * x1 + a3) % p
    else:
        num = (y2 - y1) % p
        den = (x2 - x1) % p

    if den == 0:
        return None

    lam = num * modinv(den, p) % p
    x3 = (lam * lam + a1 * lam - a2 - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1 - a3 - a1 * x3) % p
    return (x3, y3)


def gen_mul(k, P, p, a1, a2, a3, a4, a6):
    k %= p  # безопасно для проверки; для реального порядка лучше передавать нужный модуль снаружи
    R = None
    Q = P
    while k:
        if k & 1:
            R = gen_add(R, Q, p, a1, a2, a3, a4, a6)
        Q = gen_add(Q, Q, p, a1, a2, a3, a4, a6)
        k >>= 1
    return R


def gen_mul_exact(k, P, p, a1, a2, a3, a4, a6):
    """Умножение без автоматического взятия k mod p."""
    R = None
    Q = P
    k = int(k)
    while k:
        if k & 1:
            R = gen_add(R, Q, p, a1, a2, a3, a4, a6)
        Q = gen_add(Q, Q, p, a1, a2, a3, a4, a6)
        k >>= 1
    return R


# =========================================================
# DLP в F_p^* при гладком порядке
# =========================================================

def bsgs_ff(g, h, q, p):
    if q == 1:
        return 0
    m = isqrt(q) + 1
    if m > 2_000_000:
        return None

    table = {}
    cur = 1
    for j in range(m):
        if cur not in table:
            table[cur] = j
        cur = (cur * g) % p

    gm = pow(g, m, p)
    inv_gm = modinv(gm, p)

    cur = h
    for i in range(m):
        if cur in table:
            ans = i * m + table[cur]
            if ans < q and pow(g, ans, p) == h:
                return ans
        cur = (cur * inv_gm) % p

    return None


def dlog_ff_smooth(g, h, p, M):
    """
    Решает h = g^x в F_p^*, предполагая, что порядок делит M и M гладкий.
    """
    g %= p
    h %= p
    if h == 1:
        return 0
    if g == 1:
        return None

    fac = factor_smooth(M)
    if fac is None:
        return None

    rems = []
    mods = []

    for q, e in fac.items():
        qe = q ** e
        coeff = M // qe

        gq = pow(g, coeff, p)
        hq = pow(h, coeff, p)

        if gq == 1:
            if hq != 1:
                return None
            kq = 0
        else:
            kq = bsgs_ff(gq, hq, qe, p)
            if kq is None:
                return None

        rems.append(kq)
        mods.append(qe)

    x = crt(rems, mods)
    if x is None:
        return None
    if pow(g, x, p) == h:
        return x
    return None


# =========================================================
# DLP на эллиптической кривой при гладком порядке
# =========================================================

def bsgs_group(G, P, q, p, params):
    if q == 1:
        return 0
    m = isqrt(q) + 1
    if m > 2_000_000:
        return None

    a1, a2, a3, a4, a6 = params

    table = {}
    cur = None
    for j in range(m):
        if cur not in table:
            table[cur] = j
        cur = gen_add(cur, G, p, a1, a2, a3, a4, a6)

    # шаг гигантских ступеней: -m*G = (q-m)*G
    step = gen_mul_exact(q - m, G, p, a1, a2, a3, a4, a6)

    cur = P
    for i in range(m):
        if cur in table:
            ans = i * m + table[cur]
            if ans < q and gen_mul_exact(ans, G, p, a1, a2, a3, a4, a6) == P:
                return ans
        cur = gen_add(cur, step, p, a1, a2, a3, a4, a6)

    return None


def dlog_elliptic_smooth(G, P, M, p, params):
    """
    Решает P = k*G, если порядок G делит гладкое M.
    """
    a1, a2, a3, a4, a6 = params

    if P is None:
        return 0
    if G is None:
        return None

    fac = factor_smooth(M)
    if fac is None:
        return None

    rems = []
    mods = []

    for q, e in fac.items():
        qe = q ** e
        coeff = M // qe

        Gq = gen_mul_exact(coeff, G, p, a1, a2, a3, a4, a6)
        Pq = gen_mul_exact(coeff, P, p, a1, a2, a3, a4, a6)

        if Gq is None:
            if Pq is not None:
                return None
            kq = 0
        else:
            kq = bsgs_group(Gq, Pq, qe, p, params)
            if kq is None:
                return None

        rems.append(kq)
        mods.append(qe)

    x = crt(rems, mods)
    if x is None:
        return None
    if gen_mul_exact(x, G, p, a1, a2, a3, a4, a6) == P:
        return x
    return None


# =========================================================
# Сингулярная кривая: сводим ECDLP к DLP в поле
# =========================================================

def solve_singular(p, a1, a2, a3, a4, a6, G, P):
    """
    Возвращает (k, order) или None.
    """
    inv2 = modinv(2, p)
    inv12 = modinv(12, p)

    # 6*x^2 + (a1^2 + 4*a2)*x + (a1*a3 + 2*a4) = 0
    B = (a1 * a1 + 4 * a2) % p
    C = (a1 * a3 + 2 * a4) % p
    D = (B * B - 24 * C) % p

    roots = []
    if D == 0:
        roots.append((-B) * inv12 % p)
    else:
        sD = sqrt_mod(D, p)
        if sD is None:
            return None
        roots.append((-B + sD) * inv12 % p)
        roots.append((-B - sD) * inv12 % p)

    params = (a1, a2, a3, a4, a6)

    for xs in roots:
        ys = (-(a1 * xs + a3) * inv2) % p

        if not gen_on_curve((xs, ys), p, *params):
            continue

        # Дискриминант касательных в особой точке
        dq = (a1 * a1 + 4 * (3 * xs * xs + 2 * a2 * xs + a4)) % p

        if dq == 0:
            # Cusp -> аддитивная группа F_p^+
            half_a1 = a1 * inv2 % p

            def phi(Q):
                x, y = Q
                dx = (x - xs) % p
                if dx == 0:
                    return None
                return ((y - ys) * modinv(dx, p) + half_a1) % p

            tG = phi(G)
            tP = phi(P)
            if tG is None or tP is None or tG == 0:
                continue

            k = tP * modinv(tG, p) % p

            # На всякий случай проверяем прямым умножением.
            if gen_mul_exact(k, G, p, *params) == P:
                return k, p

            # Если формула дала знак с минусом, brute-force ниже всё равно попробует -k.
            return k, p

        else:
            # Node -> мультипликативная группа F_p^*
            sdq = sqrt_mod(dq, p)
            if sdq is None:
                continue

            m1 = (-a1 + sdq) * inv2 % p
            m2 = (-a1 - sdq) * inv2 % p

            def psi(Q):
                x, y = Q
                dx = (x - xs) % p
                if dx == 0:
                    return None
                t = (y - ys) * modinv(dx, p) % p
                den = (t - m2) % p
                if den == 0:
                    return None
                return (t - m1) * modinv(den, p) % p

            uG = psi(G)
            uP = psi(P)
            if uG is None or uP is None:
                continue

            k = dlog_ff_smooth(uG, uP, p, p - 1)
            if k is not None:
                return k, p - 1

    return None


# =========================================================
# Smart's attack для аномальных кривых (#E = p)
# =========================================================

def jac_add_short(P, Q, n, A):
    if P is None:
        return Q
    if Q is None:
        return P

    X1, Y1, Z1 = P
    X2, Y2, Z2 = Q

    U1 = X1 * Z2 % n * Z2 % n
    U2 = X2 * Z1 % n * Z1 % n
    S1 = Y1 * Z2 % n * Z2 % n * Z2 % n
    S2 = Y2 * Z1 % n * Z1 % n * Z1 % n

    if U1 == U2:
        if S1 == S2:
            S = 4 * X1 % n * Y1 % n * Y1 % n
            M = (3 * X1 % n * X1 % n + A * Z1 % n * Z1 % n * Z1 % n * Z1 % n) % n
            X3 = (M * M - 2 * S) % n
            Y3 = (M * (S - X3) - 8 * Y1 % n * Y1 % n * Y1 % n * Y1 % n) % n
            Z3 = 2 * Y1 % n * Z1 % n
            return (X3, Y3, Z3)
        return None

    H = (U2 - U1) % n
    R = (S2 - S1) % n
    H2 = H * H % n
    H3 = H2 * H % n
    U1H2 = U1 * H2 % n

    X3 = (R * R - H3 - 2 * U1H2) % n
    Y3 = (R * (U1H2 - X3) - S1 * H3) % n
    Z3 = H * Z1 % n * Z2 % n
    return (X3, Y3, Z3)


def jac_mul_short(k, P, n, A):
    R = None
    Q = P
    k = int(k)
    while k:
        if k & 1:
            R = jac_add_short(R, Q, n, A)
        Q = jac_add_short(Q, Q, n, A)
        k >>= 1
    return R


def smart_general(p, a1, a2, a3, a4, a6, G, P):
    """
    Возвращает (k, p) или None.
    """
    inv2 = modinv(2, p)
    inv4 = modinv(4, p)
    inv3 = modinv(3, p)

    # Приводим к короткой форме Вейерштрасса
    a2p = (a2 + a1 * a1 * inv4) % p
    a4p = (a4 + a1 * a3 * inv2) % p
    a6p = (a6 + a3 * a3 * inv4) % p

    c = a2p * inv3 % p
    A = (3 * c * c - 2 * a2p * c + a4p) % p
    B = (-c * c * c + a2p * c * c - a4p * c + a6p) % p

    def tr(Q):
        x, y = Q
        X = (x + c) % p
        Y = (y + (a1 * x + a3) * inv2) % p
        return X, Y

    Gs = tr(G)
    Ps = tr(P)

    p2 = p * p
    params = (a1, a2, a3, a4, a6)

    def lift(Q):
        x, y = Q
        f = y * y - x * x * x - A * x - B
        cval = ((f % p2) // p) % p
        dy = (2 * y) % p
        if dy == 0:
            return None
        t = (-cval * modinv(dy, p)) % p
        return (x, y + p * t, 1)

    Gl = lift(Gs)
    Pl = lift(Ps)
    if Gl is None or Pl is None:
        return None

    pG = jac_mul_short(p, Gl, p2, A)
    pP = jac_mul_short(p, Pl, p2, A)
    if pG is None or pP is None:
        return None

    for sign in (-1, 1):
        def ratio(R):
            X, Y, Z = R
            if Y % p2 == 0:
                return None
            return (sign * X * Z * modinv(Y, p2)) % p2

        rG = ratio(pG)
        rP = ratio(pP)
        if rG is None or rP is None:
            continue

        LG = (rG // p) % p
        LP = (rP // p) % p
        if LG == 0:
            continue

        k = LP * modinv(LG, p) % p

        for kk in (k, (-k) % p):
            if gen_mul_exact(kk, G, p, *params) == P:
                return kk, p

    return None


# =========================================================
# Попытка сломать C3
# =========================================================

def solve_c3():
    params = (c1, c2, c3, c4, c6)

    # 1) Сингулярность
    res = solve_singular(p3, c1, c2, c3, c4, c6, G3, P3)
    if res is not None:
        return res

    # 2) Аномальность: p*G == O
    if gen_mul_exact(p3, G3, p3, *params) is None:
        res = smart_general(p3, c1, c2, c3, c4, c6, G3, P3)
        if res is not None:
            return res

    # 3) Гладкий порядок, делящий p+1
    M = p3 + 1
    if gen_mul_exact(M, G3, p3, *params) is None:
        k = dlog_elliptic_smooth(G3, P3, M, p3, params)
        if k is not None:
            return k, M

    # 4) Гладкий порядок, делящий p-1
    M = p3 - 1
    if gen_mul_exact(M, G3, p3, *params) is None:
        k = dlog_elliptic_smooth(G3, P3, M, p3, params)
        if k is not None:
            return k, M

    # Если C3 действительно крепкая приманка — выходим без k3.
    return None


# =========================================================
# Расшифровка C2 и подготовка кандидатов для флага
# =========================================================

def unpad_pkcs7(pt):
    if not pt:
        return None
    pad = pt[-1]
    if 1 <= pad <= 16 and all(x == pad for x in pt[-pad:]):
        return pt[:-pad]
    return None


def byte_variants(n):
    n = int(n)
    out = set()

    out.add(str(n).encode())
    out.add(hex(n).encode())
    out.add(hex(n)[2:].encode())
    out.add(hex(n)[2:].upper().encode())

    # минимальные big-endian / little-endian
    bl = max(1, (n.bit_length() + 7) // 8)
    try:
        mb = n.to_bytes(bl, "big")
        out.add(mb)
        out.add(mb[::-1])
        out.add(base64.b64encode(mb))
        out.add(base64.b64encode(mb).lower())
    except Exception:
        pass

    # 32 байта: либо точно, либо младшие 256 бит
    low32 = n & ((1 << 256) - 1)
    out.add(low32.to_bytes(32, "big"))
    out.add(low32.to_bytes(32, "little"))

    # 33 байта часто хватает для 257-битных чисел
    if n.bit_length() <= 8 * 33:
        try:
            out.add(n.to_bytes(33, "big"))
            out.add(n.to_bytes(33, "little"))
        except Exception:
            pass

    # 64 байта с ведущими нулями
    if n.bit_length() <= 8 * 64:
        try:
            out.add(n.to_bytes(64, "big"))
            out.add(n.to_bytes(64, "little"))
        except Exception:
            pass

    return out


def scalar_variants(n, mod=None):
    vals = {int(n)}
    if mod:
        mod = int(mod)
        vals.add(n % mod)
        vals.add((-n) % mod)
        if mod % 2 == 0:
            vals.add(n % (mod // 2))
            vals.add((-n) % (mod // 2))
    return vals


def looks_like_plaintext(b):
    if not b:
        return None

    markers = (
        b"KubSTU{",
        b"KubSTU",
        b"flag{",
        b"FLAG{",
        b"Flag{",
        b"ctf{",
        b"CTF{",
    )

    for m in markers:
        if b.startswith(m):
            try:
                return b.decode()
            except Exception:
                return b.decode("latin1", errors="replace")

    # Если весь текст печатный и внятный
    if len(b) >= 20:
        ok = True
        for ch in b:
            if not (32 <= ch <= 126 or ch in (9, 10, 13)):
                ok = False
                break
        if ok:
            try:
                return b.decode()
            except Exception:
                pass

    return None


def evaluate_aes_pt(pt):
    # Сначала как есть
    res = looks_like_plaintext(pt)
    if res:
        return res

    # Затем с PKCS#7
    body = unpad_pkcs7(pt)
    if body is not None:
        res = looks_like_plaintext(body)
        if res:
            return res

    return None


def main():
    print("[*] Проверяю k1 на C1...")
    # Быстрая проверка k1 на исходной C1
    if gen_mul_exact(k1, G1, p1, a1, a2, a3, a4, a6) != P1:
        raise SystemExit("[-] k1 не проходит проверку")
    print("[+] k1 OK")

    print("[*] Расшифровываю C2...")
    key_c2 = hashlib.sha256(b"C1->C2:" + str(k1).encode()).digest()
    cipher_c2 = AES.new(key_c2, AES.MODE_CBC, bytes.fromhex(c2_iv_hex))
    pt_c2 = cipher_c2.decrypt(bytes.fromhex(c2_ct_hex))
    body_c2 = unpad_pkcs7(pt_c2)
    if body_c2 is None:
        raise SystemExit("[-] C2: неверный паддинг")
    c2 = json.loads(body_c2.decode())

    p2 = int(c2["p2"])
    A2 = int(c2["a"])
    B2 = int(c2["b"])
    G2 = (int(c2["G2"][0]), int(c2["G2"][1]))
    P2 = (int(c2["P2"][0]), int(c2["P2"][1]))
    N2 = p2 + 1

    print("[+] C2 JSON получен")
    print(f"    p2 = {p2}")
    print(f"    curve: y^2 = x^3 + {A2}*x + {B2}")

    # Проверка k2 на C2 (короткая форма)
    def short_add(P, Q, p, A, B):
        if P is None:
            return Q
        if Q is None:
            return P
        x1, y1 = P
        x2, y2 = Q
        if x1 == x2 and (y1 + y2) % p == 0:
            return None
        if x1 != x2:
            lam = (y2 - y1) * modinv(x2 - x1, p) % p
        else:
            lam = (3 * x1 * x1 + A) * modinv(2 * y1, p) % p
        x3 = (lam * lam - x1 - x2) % p
        y3 = (lam * (x1 - x3) - y1) % p
        return (x3, y3)

    def short_mul(k, P, p, A, B):
        R = None
        Q = P
        k = int(k)
        while k:
            if k & 1:
                R = short_add(R, Q, p, A, B)
            Q = short_add(Q, Q, p, A, B)
            k >>= 1
        return R

    print("[*] Проверяю k2 на C2...")
    if short_mul(k2, G2, p2, A2, B2) != P2:
        raise SystemExit("[-] k2 не проходит проверку")
    print("[+] k2 OK")

    print("[*] Пытаюсь сломать C3...")
    c3_res = solve_c3()
    if c3_res is None:
        print("[-] C3 не сломана стандартными глубокими атаками (возможно, это действительно приманка)")
        k3 = None
        ord3 = None
    else:
        k3, ord3 = c3_res
        print(f"[+] k3 = {k3}")
        print(f"[+] order3 candidate = {ord3}")

    # =====================================================
    # Перебор ключа флага
    # =====================================================
    print("[*] Перебираю варианты ключа флага...")

    secret_bytes = set()

    def add_scalar(n, mod=None):
        for v in scalar_variants(n, mod):
            for b in byte_variants(v):
                secret_bytes.add(b)

    # Основные скаляры
    add_scalar(k1, p1)
    add_scalar(k2, N2)
    if k3 is not None:
        add_scalar(k3, ord3)

    # Координаты тоже могут быть использованы автором
    add_scalar(P2[0])
    add_scalar(P2[1])
    add_scalar(G2[0])
    add_scalar(G2[1])
    add_scalar(P3[0])
    add_scalar(P3[1])
    add_scalar(G3[0])
    add_scalar(G3[1])

    # Конкатенации
    base_ints = [k1, k2]
    if k3 is not None:
        base_ints.append(k3)

    seps = ["", ":", "|", "-", "_", ",", ";", " "]
    for i in range(len(base_ints)):
        for j in range(len(base_ints)):
            if i == j:
                continue
            for sep in seps:
                s = str(base_ints[i]) + sep + str(base_ints[j])
                secret_bytes.add(s.encode())

    # Прямые digest'и / hex digest'и
    secret_bytes.add(key_c2)
    secret_bytes.add(key_c2.hex().encode())
    secret_bytes.add(key_c2.hex().upper().encode())

    if k3 is not None:
        key_c3_candidate = hashlib.sha256(b"C2->C3:" + str(k2).encode()).digest()
        secret_bytes.add(key_c3_candidate)
        secret_bytes.add(key_c3_candidate.hex().encode())

    prefixes = [
        b"",
        b"C1->C2:",
        b"C1->c2:",
        b"C2->flag:",
        b"C2->FLAG:",
        b"c2->flag:",
        b"C2->flag",
        b"C2->flag: ",
        b"C3->flag:",
        b"C3->FLAG:",
        b"c3->flag:",
        b"C3->flag",
        b"C3->flag: ",
        b"flag:",
        b"FLAG:",
        b"Flag:",
        b"flag",
        b"flag{",
        b"k1:",
        b"k2:",
        b"k3:",
        b"k1=",
        b"k2=",
        b"k3=",
        b"key:",
        b"key",
        b"secret:",
        b"secret",
        b"password:",
        b"pass:",
        b"KubSTU:",
        b"KubSTU",
        b"Curve Ball:",
        b"Curve Ball",
        b"CurveBall:",
        b"curve_ball:",
        b"C2->C3:",
        b"C1->flag:",
        b"C1->flag",
        b"scalar:",
        b"scalar2:",
        b"scalar3:",
        b"iv:",
        b"ct:",
    ]

    materials = set()
    for pre in prefixes:
        for sec in secret_bytes:
            materials.add(pre + sec)
            materials.add(sec + pre)

    candidate_keys = set()
    for mat in materials:
        d = hashlib.sha256(mat).digest(); candidate_keys.add(d); mat_map[d] = mat
        if len(mat) in (16, 24, 32):
            candidate_keys.add(mat)

    # Дополнительно: сами digest'и от простых строк
    for x in (k1, k2, k3):
        if x is None:
            continue
        for s in (str(x), hex(x), hex(x)[2:]):
            d = hashlib.sha256(s.encode()).digest()
            candidate_keys.add(d)
            candidate_keys.add(d[:16])
            candidate_keys.add(d[:24])

    flag_iv = bytes.fromhex(flag_iv_hex)
    flag_ct = bytes.fromhex(flag_ct_hex)

    tried = 0
    for key in candidate_keys:
        for lk in (32, 16, 24):
            if len(key) < lk:
                continue
            try:
                cipher = AES.new(key[:lk], AES.MODE_CBC, flag_iv)
                pt = cipher.decrypt(flag_ct)
            except Exception:
                continue

            tried += 1
            res = evaluate_aes_pt(pt)
            if res:
                print("MATCHED KEY HEX:", key[:lk].hex())
                print("MATCHED MAT:", repr(mat_map.get(key[:lk]))); clean = res.strip()
                print()
                print("[+] ФЛАГ НАЙДЕН")
                print(f"    key length = {lk}")
                print(f"    tried variants = {tried}")
                print(f"    raw repr = {repr(pt)}")
                print(f"    clean repr = {repr(clean)}")
                print(f"    clean hex = {clean.encode().hex()}")
                print()
                print(clean)
                return

    print("[-] Не удалось подобрать флаг автоматическим перебором.")
    print("    Но k1/k2 проверены, C3 обработана, переключатели ключей широкие.")
    print("    Если флаг не найден, скорее всего автор использовал экзотический префикс.")


if __name__ == "__main__":
    main()