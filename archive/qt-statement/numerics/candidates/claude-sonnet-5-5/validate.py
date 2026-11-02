"""Validation of the fast algorithm against brute force.  Returns list of strings."""
import math
from fractions import Fraction

import numpy as np
import mpmath as mp

from sqfcore import (C_SQ, Factorer, XData, g_rational_part, primes_upto,
                     sieve_sf)

POLYS = {
    "k^2+1": (lambda k: k * k + 1, lambda k: 2 * k),
    "k^3+2": (lambda k: k ** 3 + 2, lambda k: 3 * k * k),
    "2k+1": (lambda k: 2 * k + 1, lambda k: 2),
}


def bf_Q(sf, x, q):
    """Q(x;q,l), l = 0..q-1 (index l mod q), brute force."""
    n = np.nonzero(sf[:x + 1])[0]
    return np.bincount(n % q, minlength=q)


def bf_Vq(sf, x, q, fac):
    Q = bf_Q(sf, x, q)
    c = float(C_SQ)
    tot = 0.0
    for l in range(q):
        ll = l if l else q          # residue class representative in 1..q
        g = c * float(g_rational_part(q, ll, fac))
        tot += (Q[l] - g * x) ** 2
    return tot


def validate(log=print):
    out = []
    fact = Factorer(primes=primes_upto(2000))

    # 1. g exact vs periodic brute force, q <= 50
    ok = True
    for q in range(1, 51):
        fac = fact(q)
        M = 1
        for p in fac:
            M *= p * p
        period = q * M
        denom = Fraction(1)
        for p in fac:
            denom *= 1 - Fraction(1, p * p)
        tot = Fraction(0)
        for l in range(1, q + 1):
            cnt = 0
            for n in range(l, period + 1, q):
                if all(n % (p * p) for p in fac):
                    cnt += 1
            brute = Fraction(cnt, period) / denom
            g = g_rational_part(q, l, fac)
            if brute != g:
                ok = False
                log("MISMATCH g", q, l, brute, g)
            tot += g
        if tot != 1:
            ok = False
            log("sum_l g != c", q, tot)
    out.append("g(q,l) (exact rationals times 6/pi^2) equals the exact periodic-density "
               "brute force (period q*prod p^2, prod_{p not| q}(1-p^-2) factored out) for all "
               "q <= 50 and all l: " + ("PASS" if ok else "FAIL"))
    out.append("sum_{l mod q} g(q,l) = 6/pi^2 exactly for q <= 50: " + ("PASS" if ok else "FAIL"))

    # 2. g vs empirical densities at x = 2e6
    X = 2_000_000
    sf = sieve_sf(X)
    worst = 0.0
    for q in list(range(1, 51)) + [97, 100, 210]:
        fac = fact(q)
        Q = bf_Q(sf, X, q)
        for l in range(1, q + 1):
            g = float(C_SQ) * float(g_rational_part(q, l, fac))
            worst = max(worst, abs(Q[l % q] - g * X))
    out.append("g(q,l)*x vs Q(x;q,l), x=2e6, q<=50 and q in {97,100,210}: max |Q - g x| = "
               "%.2f (consistent with square-root cancellation)" % worst)

    # 3. sum_l Q = Q(x;1,1) and sum_l Q^2 (FFT) vs bincount
    ok3 = ok4 = True
    maxerr = 0
    for x in (997, 5000, 123456):
        xd = XData(x, sf)
        maxerr = max(maxerr, xd.fft_err)
        for q in list(range(1, 120)) + [x - 1, x, 500, 777]:
            if q > x:
                continue
            Q = bf_Q(sf, x, q)
            if int(Q.sum()) != xd.S0:
                ok3 = False
            if int((Q.astype(np.int64) ** 2).sum()) != xd.A(q):
                ok4 = False
                log("A mismatch", x, q)
    out.append("sum_l Q(x;q,l) = Q(x;1,1) for x in {997,5000,123456}, q<120 and q in "
               "{x-1,x,500,777}: " + ("PASS" if ok3 else "FAIL"))
    out.append("sum_l Q(x;q,l)^2 from the FFT autocorrelation formula equals bincount brute force "
               "(exact integers), same x,q: " + ("PASS" if ok4 else "FAIL")
               + "; max FFT rounding error %.2e" % maxerr)

    # 4. sum_l g^2 closed form vs enumeration
    ok5 = True
    xd = XData(1000, sf)
    for q in range(1, 301):
        fac = fact(q)
        _, R = xd.terms(q, fac)
        s = sum(g_rational_part(q, l, fac) ** 2 for l in range(1, q + 1))
        if s != R:
            ok5 = False
            log("R mismatch", q)
    out.append("sum_l g(q,l)^2 closed form (W^2 T / q^2) equals enumeration for q <= 300: "
               + ("PASS" if ok5 else "FAIL"))

    # 5. per-modulus sum_l E^2: exact path, float path vs brute force
    rel_e = rel_f = 0.0
    for x in (3000, 50000):
        xd = XData(x, sf)
        for q in list(range(1, 150)) + [199, 360, 1001, 2310]:
            if q > x:
                continue
            fac = fact(q)
            b = bf_Vq(sf, x, q, fac)
            e = float(xd.V_modulus_exact(q, fac))
            f_ = xd.V_modulus_float(q, fac)
            rel_e = max(rel_e, abs(e - b) / b)
            rel_f = max(rel_f, abs(f_ - b) / b)
    out.append("sum_l E(x;q,l)^2: fast exact-rational path vs float64 brute force (x=3000,50000; "
               "q<150 and some larger): max rel. diff %.2e; fast float path %.2e" % (rel_e, rel_f))

    # 6. full V_f for the three polynomials, small x
    for name, (f, fp) in POLYS.items():
        for x, ymax in ((20000, 10 ** 9), (200000, 10 ** 9)):
            xd = XData(x, sf)
            tot_fast = mp.mpf(0)
            tot_bf = 0.0
            k = 1
            while f(k) <= x:
                q = f(k)
                fac = fact(q)
                tot_fast += fp(k) * xd.V_modulus_exact(q, fac)
                tot_bf += fp(k) * bf_Vq(sf, x, q, fac)
                k += 1
                if k > 120:      # keep brute force cheap
                    break
            out.append("V_f(x,y) %s, x=%d, y=%d: fast %.10e, brute force %.10e, rel diff %.1e" % (
                name, x, k - 1, float(tot_fast), tot_bf, abs(float(tot_fast) - tot_bf) / tot_bf))
    # 7. float path (used for q > 3000) vs exact path at large x
    import random
    random.seed(1)
    X7 = 10 ** 7
    sf7 = sieve_sf(X7)
    xd = XData(X7, sf7)
    fact7 = Factorer(primes=primes_upto(4000))
    qs = list(range(3001, 3060)) + [random.randrange(3001, X7 + 1) for _ in range(300)]
    worst = 0.0
    for q in qs:
        fac = fact7(q)
        e = xd.V_modulus_exact(q, fac)
        f_ = xd.V_modulus_float(q, fac)
        worst = max(worst, float(abs(f_ - e) / e))
    out.append("float64 path (used only for q > 3000) vs 50-digit exact path at x=1e7, %d moduli "
               "q in (3000, 1e7]: max rel. diff %.2e" % (len(qs), worst))
    return out


if __name__ == "__main__":
    for s in validate():
        print(s)
