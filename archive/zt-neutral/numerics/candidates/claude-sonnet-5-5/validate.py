"""Validation of the closed forms and the fast algorithm. Returns list of strings."""
import numpy as np
from decimal import Decimal
from fractions import Fraction
from math import gcd
import sqf
from sqf import State, g_closed, C_CONST, POLYS, finv_floor


def moebius_sieve(N):
    mu = np.ones(N + 1, dtype=np.int64)
    mu[0] = 0
    isp = np.ones(N + 1, dtype=bool)
    for p in range(2, N + 1):
        if isp[p]:
            isp[2 * p::p] = False
            mu[p::p] *= -1
            if p * p <= N:
                mu[p * p::p * p] = 0
    return mu


def g_moebius(q, l, mu, D):
    """g(q,l)/c-free: density by sum_d mu(d) [gcd(d^2,q) | l] / lcm(d^2,q); truncated at d<=D."""
    tot = 0.0
    for d in range(1, D + 1):
        if mu[d] == 0:
            continue
        d2 = d * d
        gg = gcd(d2, q)
        if l % gg == 0:
            tot += mu[d] * gg / (d2 * q)
    return tot


def brute_Q(x, q, s):
    n = np.arange(1, x + 1)
    return np.bincount(n[s[1:x + 1] == 1] % q, minlength=q)  # index = l mod q (l=q -> 0)


def run():
    msgs = []
    c = float(C_CONST)

    # 1. g(q,l) vs Moebius series (independent derivation) and brute-force counts, q<=50
    D = 4000
    mu = moebius_sieve(D)
    N = 2_000_000
    s = sqf.squarefree_indicator(N)
    worst_mob = 0.0
    worst_bf = 0.0
    for q in range(1, 51):
        cnt = brute_Q(N, q, s)
        for l in range(1, q + 1):
            gc = c * float(g_closed(q, l))
            gm = g_moebius(q, l, mu, D)
            worst_mob = max(worst_mob, abs(gc - gm) / max(gc, 1e-3 / q) if gc > 0 else abs(gm))
            bf = cnt[l % q] / N
            worst_bf = max(worst_bf, abs(bf - gc) * q)
    ok = worst_mob < 2e-3 and worst_bf < 5e-3
    msgs.append(f"g(q,l) matches Moebius-series density sum_d mu(d)[gcd(d^2,q)|l]/lcm(d^2,q) "
                f"(d<=4000) for all q<=50, all l: max rel dev {worst_mob:.2e} (tail-truncation limited); "
                f"matches brute-force densities (squarefree n<=2e6) with max |dens-g|*q = {worst_bf:.2e} "
                f"[{'PASS' if ok else 'FAIL'}]")
    assert ok

    # 1b. exact: sum_l g(q,l) = 6/pi^2, and g(q,l)=0 iff p^2|gcd(q,l) for some p
    for q in list(range(1, 400)) + [1001, 2310, 4096, 9 * 25 * 49]:
        tot = sum(g_closed(q, l) for l in range(1, q + 1))
        assert tot == 1, (q, tot)
    msgs.append("sum_{l=1}^q g(q,l) = 6/pi^2 exactly (rational check) for all q<400 and q in {1001,2310,4096,11025} [PASS]")

    # 1c. sum_l g^2 closed form T_p product vs direct sum
    for q in list(range(1, 300)) + [2310, 4096, 11025]:
        direct = sum(g_closed(q, l) ** 2 for l in range(1, q + 1))
        from sympy import factorint
        T = Fraction(1, q * q)
        for p, a in factorint(q).items():
            T *= Fraction(p * p * (p * p + p - 1), (p - 1) * (p + 1) ** 2) if a == 1 else Fraction(p ** (a + 2), p * p - 1)
        assert T == direct, q
    msgs.append("closed form sum_l g(q,l)^2 = (c/q)^2 prod T_p equals direct rational sum for q<300 and q in {2310,4096,11025} [PASS]")

    # 2. sum_l Q(x;q,l) = Q(x;1,1) and fast sum_l E^2 vs brute force
    x = 3000
    st = State(x, 4000)
    S1 = int(st.s[1:x + 1].sum())
    worst = Decimal(0)
    for q in range(2, 600):
        cnt = brute_Q(x, q, st.s)
        assert cnt.sum() == S1
        # brute force sum_l E^2 with exact g
        tot = Decimal(0)
        for l in range(1, q + 1):
            gl = C_CONST * Decimal(g_closed(q, l).numerator) / Decimal(g_closed(q, l).denominator)
            E = Decimal(int(cnt[l % q])) - gl * x
            tot += E * E
        fast = st.sumsq_E(q)
        worst = max(worst, abs(fast - tot) / max(tot, Decimal(1)))
    ok = worst < Decimal("1e-40")
    msgs.append(f"sum_l Q(x;q,l) = Q(x;1,1) for x=3000, 2<=q<600 (bincount) [PASS]")
    msgs.append(f"fast sum_l E(x;q,l)^2 (FFT autocorrelation + closed forms) equals brute-force bincount/g sum for x=3000, 2<=q<600: "
                f"max rel dev {worst:.1e} [{'PASS' if ok else 'FAIL'}]")
    assert ok

    # 3. autocorrelation exactness at a large x (spot checks against exact dot products)
    xl = 2_000_000
    sl = sqf.squarefree_indicator(xl)
    Cl, err = sqf.autocorrelation(sl, xl)
    rng = np.random.default_rng(1)
    hs = list(rng.integers(0, xl, 40)) + [0, 1, 2, 6, 30, 210, 2310, xl - 1, xl]
    for h in hs:
        h = int(h)
        exact = int(np.dot(sl[1:xl - h + 1].astype(np.int64), sl[1 + h:xl + 1].astype(np.int64))) if h < xl else 0
        assert exact == Cl[h], (h, exact, Cl[h])
    msgs.append(f"FFT autocorrelation C(h) equals exact integer dot product at 49 spot values of h, x=2e6; max |fft - round| = {err:.2e} [PASS]")

    # 4. full V_f small-x brute force for all three polynomials
    x = 5000
    st = State(x, 6000)
    for name, (f, fp) in POLYS.items():
        yv = finv_floor(name, x)
        tot_fast = Decimal(0)
        tot_bf = Decimal(0)
        for k in range(1, yv + 1):
            q = f(k)
            cnt = brute_Q(x, q, st.s)
            sq = Decimal(0)
            for l in range(1, q + 1):
                gl = g_closed(q, l)
                E = Decimal(int(cnt[l % q])) - C_CONST * Decimal(gl.numerator) / Decimal(gl.denominator) * x
                sq += E * E
            tot_bf += fp(k) * sq
            tot_fast += fp(k) * st.sumsq_E(q)
        rel = abs(tot_fast - tot_bf) / tot_bf
        assert rel < Decimal("1e-40"), (name, rel)
        msgs.append(f"V_f(x,y) for f={name}, x=5000, y={yv}: fast = brute force to rel {float(rel):.1e}; V={float(tot_bf):.6e} [PASS]")
    return msgs


if __name__ == "__main__":
    for m in run():
        print(m)
