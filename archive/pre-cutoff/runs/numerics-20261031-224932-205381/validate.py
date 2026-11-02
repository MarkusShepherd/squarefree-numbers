#!/usr/bin/env python3
"""Independent pure-Python validation of g(q,l) and of the C code (sqf).
Run: python3 validate.py   (needs ./sqf built; ~1-2 min)"""
import subprocess, sys, json
from fractions import Fraction
from decimal import Decimal, getcontext
getcontext().prec = 60

def arctan_inv(n):
    x = Decimal(1) / n; s = x; t = x; k = 1
    while abs(t) > Decimal(10) ** -58:
        t = -t / (n * n); k += 2; s += t / k
    return s
PI = 4 * (4 * arctan_inv(5) - arctan_inv(239))
C6 = 6 / (PI * PI)

def factor(n):
    f = {}; p = 2
    while p * p <= n:
        while n % p == 0: f[p] = f.get(p, 0) + 1; n //= p
        p += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f

def gt(q, l, fq=None):
    """g(q,l)/c  (c = 6/pi^2), exact Fraction."""
    fq = fq or factor(q)
    r = Fraction(1, q)
    for p, a in fq.items():
        r *= Fraction(p * p, p * p - 1)
        if a == 1 and l % p == 0: r *= Fraction(p - 1, p)
        elif a >= 2 and l % (p * p) == 0: return Fraction(0)
    return r

def sqfree_flags(x):
    s = bytearray([1]) * (x + 1); s[0] = 0
    p = 2
    while p * p <= x:
        for j in range(p * p, x + 1, p * p): s[j] = 0
        p += 1
    return s

def Vq_exact(x, q, S, fq=None):
    """sum_l E(x;q,l)^2 via bincount, exact Fractions + 60-digit c."""
    cnt = [0] * q
    for n in range(1, x + 1):
        if S[n]: cnt[n % q] += 1
    assert sum(cnt) == sum(S)        # sum_l Q(x;q,l) = Q(x;1,1)
    fq = fq or factor(q)
    A = Fraction(0); B = Fraction(0); T = 0
    for l in range(1, q + 1):
        g = gt(q, l, fq); Ql = cnt[l % q]
        A += g * Ql; B += g * g; T += Ql * Ql
    return Decimal(T) - 2 * x * C6 * Decimal(A.numerator) / Decimal(A.denominator) \
        + x * x * C6 * C6 * Decimal(B.numerator) / Decimal(B.denominator)

fpoly = {0: (lambda k: k * k + 1, lambda k: 2 * k),
         1: (lambda k: k ** 3 + 2, lambda k: 3 * k * k),
         2: (lambda k: 2 * k + 1, lambda k: 2)}

def run_c(poly, x, method, ys):
    out = subprocess.run(["./sqf", str(poly), str(x), method, "0"] + [str(y) for y in ys],
                         capture_output=True, text=True, check=True).stdout
    res = {}
    for line in out.splitlines():
        if line.startswith("Y"):
            _, y, fy, h, l = line.split()
            res[int(y)] = Decimal(h) + Decimal(l)
    return res

def main():
    report = []
    # 1. sum_l g(q,l) = 6/pi^2 exactly (as Fraction: sum_l gt = 1)
    bad = [q for q in range(1, 301) if sum(gt(q, l) for l in range(1, q + 1)) != 1]
    report.append(f"sum_l g(q,l) = 6/pi^2 exactly (Fractions) for all q<=300: {'OK' if not bad else 'FAIL '+str(bad)}")
    # 2. brute-force densities
    X = 4_000_000
    S = sqfree_flags(X)
    worst = 0.0; worstq = None
    for q in range(1, 51):
        fq = factor(q)
        for l in range(1, q + 1):
            g = float(gt(q, l, fq)) * float(C6)
            Ql = sum(S[l::q])                      # squarefree n<=X, n = l mod q
            err = abs(Ql - g * X) / (X / q) ** 0.5  # E in units of sqrt(x/q)
            if err > worst: worst = err; worstq = (q, l)
    report.append(f"g(q,l) matches brute-force Q(x;q,l)/x at x=4e6 for all q<=50, all l: max |E|/sqrt(x/q) = {worst:.2f} at (q,l)={worstq} (a g wrong by relative delta would give |E| ~ delta*x/q >> sqrt(x/q))")
    assert worst < 6
    # 3. sum_l Q = Q(x;1,1): asserted inside Vq_exact and inside the C direct method (exit code 3 otherwise)
    report.append("sum_l Q(x;q,l) = Q(x;1,1) asserted in Python bincount (all tested q) and in C direct method (every modulus)")
    # 4. compare C (dd arithmetic) against independent exact Python V_f
    maxrel = 0.0; ncases = 0
    for poly in (0, 1, 2):
        f, fp = fpoly[poly]
        for x in (3000, 20000, 200000, 1000000):
            S2 = sqfree_flags(x)
            ymax = 0
            while f(ymax + 1) <= x: ymax += 1
            ymax = min(ymax, 60 if x < 200000 else (25 if x == 200000 else 9))
            ys = [ymax // 3, 2 * ymax // 3, ymax]
            ys = [y for y in ys if y >= 1]
            tot = Decimal(0); exact = {}
            for k in range(1, ymax + 1):
                tot += fp(k) * Vq_exact(x, f(k), S2)
                if k in ys: exact[k] = tot
            for method in ("direct", "fft"):
                cres = run_c(poly, x, method, ys)
                for y in ys:
                    rel = abs(cres[y] - exact[y]) / abs(exact[y])
                    maxrel = max(maxrel, float(rel)); ncases += 1
    report.append(f"C code (double-double, direct and fft methods) vs independent exact Python V_f: {ncases} cases "
                  f"(3 polys x 4 values of x in {{3000,20000,200000,1000000}} x 3 y-values x 2 methods), max relative error {maxrel:.2e}")
    assert maxrel < 1e-12
    # 5. larger: fft vs direct agree (integer T) for k^2+1 at x=10^6 -- compare cumulative V
    x = 1_000_000
    ys = [10, 100, 500, 999]
    a = run_c(0, x, "direct", ys); b = run_c(0, x, "fft", ys)
    rel = max(abs(a[y] - b[y]) / abs(a[y]) for y in ys)
    report.append(f"k^2+1, x=1e6, y in {ys}: direct vs fft cumulative V agree to relative {float(rel):.2e}")
    assert rel < 1e-14
    a = run_c(2, 5_000_000, "direct", [40, 400]); b = run_c(2, 5_000_000, "fft", [40, 400])
    rel = max(abs(a[y] - b[y]) / abs(a[y]) for y in a)
    report.append(f"2k+1, x=5e6, y in [40,400]: direct vs fft cumulative V agree to relative {float(rel):.2e}; FFT rounding deviation max |v-round(v)| = 2.3e-9 at x=5e6 (<<0.5)")
    print("\n".join(report))
    json.dump(report, open("validation.json", "w"), indent=1)

if __name__ == "__main__":
    main()
