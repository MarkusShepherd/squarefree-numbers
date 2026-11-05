#!/usr/bin/env python3
"""Regenerate every number in the manuscript's numerical tables and plots.

Invoke from the workspace root:

    python3 manuscript/reproduce.py

What it does (details in manuscript/README.md):

1. Copies the accepted snapshot's ``compute.py`` and ``counts.cpp`` from
   ``source/numerics/snapshot`` into a scratch work directory (after checking
   their SHA-256 against ``source/numerics/accepted.json``) and runs
   ``compute.py`` there unchanged.  That script compiles ``counts.cpp`` with
   clang++, re-runs its validations, recomputes V_f(x, y) on the full grid
   x = 2.5e5, ..., 2.56e8, and redoes the empirical fits.  The archived
   executable is not used.
2. Compares the regenerated ``results.json`` with the archived one.
3. Computes, with code in this file, the quantities of the theorem that are
   not part of the snapshot: the constant C_f (Euler product over p <= 1e7,
   with a rigorous bound for the omitted primes), Vaughan's constant c_2,
   the sums  sum_k f'(k) MT(x; f(k))  and  sum_k F(k) h(f(k))  at selected rows,
   and a self-test of the exact identity of Proposition 4.1 (P2).
4. Writes LaTeX table fragments and PGFPlots data files to
   ``manuscript/generated/`` and the index ``manuscript/reproduction.json``.

No value is copied from proof prose or from the archived results; the
archived ``results.json`` is read only for the agreement check in step 2.
"""
import argparse
import hashlib
import itertools
import json
import math
import pathlib
import shutil
import subprocess
import sys
import time
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR

import numpy as np
import mpmath as mp
import sympy

HERE = pathlib.Path(__file__).resolve().parent
WS = HERE.parent
SNAP = WS / 'source' / 'numerics' / 'snapshot'
ACCEPTED = WS / 'source' / 'numerics' / 'accepted.json'
GEN = HERE / 'generated'
DEFAULT_WORK = WS / 'scratch' / 'reproduce-work'
MARKER = '.reproduce-work'

NAMES = ['k^2+1', 'k^3+2', '2k+1']
TEXNAME = {'k^2+1': '$k^2+1$', 'k^3+2': '$k^3+2$', '2k+1': '$2k+1$', 't': '$t$ (formal)'}
POLY = {'k^2+1': (lambda k: k * k + 1, lambda k: 2 * k, 2),
        'k^3+2': (lambda k: k ** 3 + 2, lambda k: 3 * k * k, 3),
        '2k+1': (lambda k: 2 * k + 1, lambda k: 2, 1),
        't': (lambda k: k, lambda k: 1, 1)}
RATIOS = [.01, .02, .05, .1, .2, .4, .7, 1.]
PRIME_CUTOFFS = [10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7]
# Rows of the exact-shape comparison (Table 5).  The linear polynomial has
# about x/2 moduli, so it is restricted to the two smallest sizes.
SHAPE_XS = {'k^2+1': [1000000, 16000000, 256000000],
            'k^3+2': [1000000, 16000000, 256000000],
            '2k+1': [250000, 1000000]}

mp.mp.dps = 80
I_CONST = -4 * mp.zeta(mp.mpf(-1) / 2)          # I = -4 zeta(-1/2)
SIX_PI2 = 6 / mp.pi ** 2


def sha256(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


# ----------------------------------------------------------------------------
# 1. Snapshot re-run
# ----------------------------------------------------------------------------

def run_snapshot(work, reuse):
    accepted = json.loads(ACCEPTED.read_text())['artifacts']
    for name in ['compute.py', 'counts.cpp']:
        if sha256(SNAP / name) != accepted[name]:
            raise RuntimeError(f'{name} does not match the accepted snapshot hash')
    elapsed = None
    if not (reuse and (work / 'results.json').exists()):
        if work.exists():
            # Only ever delete a directory that this script created itself.
            if any(work.iterdir()) and not (work / MARKER).exists():
                raise RuntimeError(f'{work} is not empty and was not created by reproduce.py; '
                                   'choose another --work directory')
            shutil.rmtree(work)
        work.mkdir(parents=True)
        (work / MARKER).write_text('scratch directory of manuscript/reproduce.py; safe to delete\n')
        for name in ['compute.py', 'counts.cpp']:
            shutil.copy2(SNAP / name, work / name)
        t0 = time.monotonic()
        subprocess.run([sys.executable, str(work / 'compute.py')], cwd=work, check=True)
        elapsed = time.monotonic() - t0
    for name in ['compute.py', 'counts.cpp']:
        if sha256(work / name) != accepted[name]:
            raise RuntimeError(f'work copy of {name} differs from the snapshot')
    results = json.loads((work / 'results.json').read_text())
    return results, elapsed


def all_rows(res, name):
    p = res['polynomials'][name]
    return p['rows'] + p['diagnostic_rows']


def compare_with_archive(new):
    old = json.loads((SNAP / 'results.json').read_text())
    out = {}
    for name in NAMES:
        o = {(r['x'], r['ratio_target']): r for r in all_rows(old, name)}
        n = {(r['x'], r['ratio_target']): r for r in all_rows(new, name)}
        if set(o) != set(n):
            raise RuntimeError(f'row sets differ for {name}')
        exact = all(o[k]['sum_Q_squared_weighted'] == n[k]['sum_Q_squared_weighted']
                    and o[k]['y'] == n[k]['y'] for k in o)
        dv = max(abs(Decimal(o[k]['V_decimal']) / Decimal(n[k]['V_decimal']) - 1) for k in o)
        po, pn = old['polynomials'][name], new['polynomials'][name]
        ce_o, ce_n = po['constant_extrapolated'], pn['constant_extrapolated']
        out[name] = dict(rows=len(o), integer_counts_identical=exact,
                         max_relative_difference_V=float(dv),
                         extrapolated_constant_difference=abs(ce_o['value'] - ce_n['value']),
                         envelope_difference=abs(ce_o['uncertainty'] - ce_n['uncertainty']),
                         fixed_ratio_slope_difference=abs(po['fit_fixed_ratio']['alpha_plus_beta']
                                                          - pn['fit_fixed_ratio']['alpha_plus_beta']))
    return out


# ----------------------------------------------------------------------------
# 2. Arithmetic helpers
# ----------------------------------------------------------------------------

def primes_upto(n):
    s = np.ones(n + 1, dtype=bool)
    s[:2] = False
    for p in range(2, math.isqrt(n) + 1):
        if s[p]:
            s[p * p::p] = False
    return np.nonzero(s)[0]


def powmod_vec(base, exp, mod):
    """Elementwise base**exp % mod for int64 arrays with mod < 3e9."""
    base = base % mod
    result = np.ones_like(mod)
    exp = exp.copy()
    while np.any(exp > 0):
        odd = (exp & 1) == 1
        result = np.where(odd, (result * base) % mod, result)
        base = (base * base) % mod
        exp >>= 1
    return result


def rho_formula(name, P):
    """(rho(p), rho(p^2)) for each prime in P, from the closed forms listed in
    Section 10.2.  They are checked against brute force by rho_bruteforce_check."""
    P = P.astype(np.int64)
    if name == 'k^2+1':
        r1 = np.where(P == 2, 1, np.where(P % 4 == 1, 2, 0))
        r2 = np.where(P == 2, 0, r1)
    elif name == 'k^3+2':
        cube = powmod_vec(np.full_like(P, -2), (P - 1) // 3, P) == 1
        r1 = np.where((P == 2) | (P == 3) | (P % 3 == 2), 1, np.where(cube, 3, 0))
        r2 = np.where((P == 2) | (P == 3), 0, r1)
    elif name == '2k+1':
        r1 = np.where(P == 2, 0, 1)
        r2 = r1.copy()
    elif name == 't':
        r1 = np.ones_like(P)
        r2 = np.ones_like(P)
    return r1.astype(np.float64), r2.astype(np.float64)


def rho_bruteforce_check(name, bound=1000):
    f = POLY[name][0]
    P = primes_upto(bound)
    r1, r2 = rho_formula(name, P)
    for i, p in enumerate(P):
        p = int(p)
        for m, expect in [(p, r1[i]), (p * p, r2[i])]:
            a = np.arange(m, dtype=np.int64)
            val = f(a) % m if name != 'k^3+2' else ((a * a % m) * a + 2) % m
            if int(np.count_nonzero(val == 0)) != int(expect):
                raise RuntimeError(f'rho mismatch for {name} at {m}')
    return len(P)


def local_factors(p):
    p = p.astype(np.float64)
    a_m1 = -3 / p ** 2 + 2 / p ** 3                                  # a_p - 1
    ba = -1 / p + p ** -1.5 + p ** -2 - p ** -2.5                     # b_p - a_p
    cb = -p ** -1.5 * (1 - p ** -0.5) * (1 - 1 / p)                  # c_p - b_p
    return a_m1, ba, cb


def euler_constant(name, P):
    """Partial values (2/3) I prod_{p<=N} sigma_p and a rigorous interval for
    the full product (tail bound of Section 10.2)."""
    r1, r2 = rho_formula(name, P)
    xp, zp = r1 / P, r2 / (P.astype(np.float64) ** 2)
    a_m1, ba, cb = local_factors(P)
    s_m1 = a_m1 + ba * xp + cb * zp                                   # sigma_p - 1
    if np.any(1 + s_m1 <= 0):
        raise RuntimeError('nonpositive local factor')
    logs = np.log1p(s_m1)
    pref = 2 * float(I_CONST) / 3
    partial = {}
    for N in PRIME_CUTOFFS:
        partial[N] = pref * math.exp(math.fsum(logs[P <= N]))
    d = POLY[name][2]
    K = 3 + 2 * d
    N = PRIME_CUTOFFS[-1]
    # |log prod_{p>N} sigma_p| <= K/(1-K/N^2) * sum_{p>N} p^-2, and every prime
    # p > N >= 30 lies in one of 8 classes mod 30, each contributing at most
    # N^-2 + 1/(30N).
    tail = K / (1 - K / N ** 2) * 8 * (1 / N ** 2 + 1 / (30 * N))
    val = partial[N]
    return dict(partial=partial, value=val, lower=val * math.exp(-tail),
                upper=val * math.exp(tail), tail_log_bound=tail, K=K)


def vaughan_c2(P):
    """c_2 = 8 C_1 (-zeta(-1/2)) / (3 zeta(2)^2), Vaughan (2005), (1.14)-(1.15)
    with k = 2; C_1 truncated to p <= N."""
    p = P.astype(np.float64)
    term = ((p - 1) ** 2 * p ** 1.5 - 2 * p ** 4 + 3 * p ** 3 - p) / (p ** 2 * (p ** 2 - 1) ** 2)
    logs = np.log1p(term)
    pref = float(8 * (-mp.zeta(mp.mpf(-1) / 2)) / (3 * mp.zeta(2) ** 2))
    return {N: pref * math.exp(math.fsum(logs[P <= N])) for N in PRIME_CUTOFFS}


def round_out(v, nd, up):
    """Round the float v to nd decimals, downwards (up=False) or upwards (up=True).
    Used for interval endpoints, so that the printed interval contains the
    computed one."""
    q = Decimal(1).scaleb(-nd)
    return Decimal(v).quantize(q, rounding=ROUND_CEILING if up else ROUND_FLOOR)


def up(v, nd):
    """v rounded upwards to nd decimals: for upper bounds quoted in the text."""
    return str(round_out(v, nd, True))


def down(v, nd):
    """v rounded downwards to nd decimals: for lower bounds quoted in the text."""
    return str(round_out(v, nd, False))


def certified_digits(lower, upper, maxdigits=12):
    """Longest decimal truncation shared by every number in [lower, upper]
    (0 < lower <= upper < 1); these digits are fixed by the interval."""
    best = None
    for nd in range(1, maxdigits + 1):
        a = round_out(lower, nd, False)
        b = round_out(upper, nd, False)
        if a != b:
            break
        best = a
    return str(best)


def euler_float_check(name, N=10 ** 5, dps=40):
    """Recompute (2/3) I prod_{p<=N} sigma_p with mpmath at dps digits, to
    gauge the floating-point rounding of euler_constant (not a certification)."""
    P = primes_upto(N)
    r1, r2 = rho_formula(name, P)
    with mp.workdps(dps):
        tot = mp.mpf(0)
        for p, a1, a2 in zip(P.tolist(), r1.tolist(), r2.tolist()):
            p = mp.mpf(p)
            a = 1 - 3 / p ** 2 + 2 / p ** 3
            b = (p - 1) * (p ** 2 - 2 + mp.sqrt(p)) / p ** 3
            c = (p - 1) ** 2 * (p + 1) / p ** 3
            xp, zp = mp.mpf(int(a1)) / p, mp.mpf(int(a2)) / p ** 2
            tot += mp.log(a * (1 - xp) + b * (xp - zp) + c * zp)
        return 2 * (-4 * mp.zeta(mp.mpf(-1) / 2)) / 3 * mp.exp(tot)


def eligibility(results, name):
    """For the rows at the largest x: the largest delta for which the row lies in
    the range x^(7/9+delta) <= f(y) <= x^(1-delta) of Theorem 1.1(iii), computed
    from the actual ratio f(y)/x (negative: outside the range for every delta)."""
    rows = all_rows(results, name)
    xl = max(r['x'] for r in rows)
    out = []
    for r in sorted([r for r in rows if r['x'] == xl], key=lambda r: r['ratio_target']):
        lr = math.log(r['fy']) / math.log(xl)
        out.append(dict(x=xl, ratio_target=r['ratio_target'], ratio_actual=r['ratio_actual'],
                        delta_max=min(lr - 7 / 9, 1 - lr)))
    return out


def symbolic_local_identity():
    p = sympy.symbols('p', positive=True)
    r = sympy.sqrt(p)
    a = 1 - 3 / p ** 2 + 2 / p ** 3
    b = (p - 1) * (p ** 2 - 2 + r) / p ** 3
    c = (p - 1) ** 2 * (p + 1) / p ** 3
    sig = a * (1 - 1 / p) + b * (1 / p - 1 / p ** 2) + c / p ** 2
    C1p = 1 + ((p - 1) ** 2 * p ** sympy.Rational(3, 2) - 2 * p ** 4 + 3 * p ** 3 - p) / (p ** 2 * (p ** 2 - 1) ** 2)
    checks = {
        'sigma_p(rho=1) == C_{1,p} (1-p^-2)^2': sympy.simplify(sig - C1p * (1 - p ** -2) ** 2) == 0,
        'a_p == (p-1)^2(p+2)/p^3': sympy.simplify(a - (p - 1) ** 2 * (p + 2) / p ** 3) == 0,
        'b_p - a_p == -1/p + p^-3/2 + p^-2 - p^-5/2': sympy.simplify(b - a - (-1 / p + p ** sympy.Rational(-3, 2) + p ** -2 - p ** sympy.Rational(-5, 2))) == 0,
        'c_p - b_p == -p^-3/2 (1-p^-1/2)(1-p^-1)': sympy.simplify(c - b + p ** sympy.Rational(-3, 2) * (1 - 1 / r) * (1 - 1 / p)) == 0,
        'zeta(-1/2) == -zeta(3/2)/(4 pi)': abs(mp.zeta(-0.5) + mp.zeta(1.5) / (4 * mp.pi)) < mp.mpf(10) ** -70,
    }
    if not all(checks.values()):
        raise RuntimeError(f'symbolic check failed: {checks}')
    return {k: bool(v) for k, v in checks.items()}


def A0_mp():
    """A_0 = prod_p (1 - 2/p^2) to ~40 digits."""
    P0 = 1000
    small = [int(p) for p in primes_upto(P0)]
    head = mp.fsum(mp.log(1 - mp.mpf(2) / p ** 2) for p in small)
    tail = mp.mpf(0)
    for k in range(1, 30):
        pz = mp.primezeta(2 * k) - mp.fsum(mp.mpf(p) ** (-2 * k) for p in small)
        tail -= mp.mpf(2) ** k / k * pz
    return mp.exp(head + tail)


def Ah_mp():
    """A_h = prod_p (1 - 3/p^2 + 2/p^3) to ~40 digits."""
    P0 = 1000
    small = [int(p) for p in primes_upto(P0)]
    head = mp.fsum(mp.log(1 - mp.mpf(3) / p ** 2 + mp.mpf(2) / p ** 3) for p in small)
    tail = mp.mpf(0)
    for k in range(2, 30):
        ck = -(2 + mp.mpf(-2) ** k) / k
        pz = mp.primezeta(k) - mp.fsum(mp.mpf(p) ** (-k) for p in small)
        tail += ck * pz
    return mp.exp(head + tail)


# ----------------------------------------------------------------------------
# 3. MT(x; q) and h(q)
# ----------------------------------------------------------------------------

class Arithmetic:
    """eta(t) for t <= tmax and the constants entering MT and h."""
    TSTAR = 64     # head of the eta-sums evaluated in 80-digit arithmetic

    def __init__(self, tmax):
        tmax = max(tmax, self.TSTAR + 1)
        self.tmax = tmax
        eta = np.ones(tmax + 1)
        eta[0] = 0.
        for p in primes_upto(tmax):
            p = int(p)
            eta[p::p] /= (p * p - 2)
            eta[p * p::p * p] = 0.
        self.eta = eta
        self.t = np.arange(tmax + 1, dtype=np.float64)
        self.kappa = eta * self.t ** 2
        self.eta_t2 = np.divide(eta, self.t ** 2, out=np.zeros_like(eta), where=self.t > 0)
        self.A0mp = A0_mp()
        self.A0 = float(self.A0mp)
        self.Ahmp = Ah_mp()
        self.head_cache = {}
        self.eta_mp = [mp.mpf(0)] + [mp.mpf(1) for _ in range(self.TSTAR)]
        for t in range(1, self.TSTAR + 1):
            fac = sympy.factorint(t)
            if any(e > 1 for e in fac.values()):
                self.eta_mp[t] = mp.mpf(0)
            else:
                self.eta_mp[t] = mp.fprod(mp.mpf(1) / (p * p - 2) for p in fac)

    def heads(self, qprimes, th):
        """80-digit A_0 * sum_{t<=th,(t,q)=1} eta(t) and eta(t)/t^2."""
        small = tuple(p for p in qprimes if p <= self.TSTAR)
        key = (small, th)
        if key not in self.head_cache:
            s2 = s4 = mp.mpf(0)
            for t in range(1, th + 1):
                if self.eta_mp[t] and all(t % p for p in small):
                    s2 += self.eta_mp[t]
                    s4 += self.eta_mp[t] / t ** 2
            self.head_cache[key] = (self.A0mp * s2, self.A0mp * s4)
        return self.head_cache[key]

    def MT(self, x, q, fac):
        """MT(x; q) for integer x, q with q <= x; fac = factorisation of q.

        Uses the factorisation t = t0 t1 t2 of the proof of Proposition 6.2:
        for t0 > sqrt(Z),
        B(Z/t0^2) = Z/t0^2 - Z^2/t0^4, and the complete eta-sums over t0 coprime
        to q are known in closed form, so the infinite t0-sum is evaluated
        exactly up to rounding."""
        S1 = [p for p, e in fac.items() if e == 1]
        S2 = [p for p, e in fac.items() if e >= 2]
        qprimes = list(fac)
        E2 = math.prod(1 + 1 / (p * p - 2) for p in S2)
        full2 = SIX_PI2 * mp.fprod(mp.mpf(p * p - 2) / (p * p - 1) for p in qprimes)
        full4 = SIX_PI2 ** 2 * mp.fprod(mp.mpf(p * p) * (p * p - 2) / (p * p - 1) ** 2 for p in qprimes)
        Tmax = math.isqrt(x // q)
        if Tmax > self.tmax:
            raise RuntimeError('tmax too small')
        ts = np.arange(1, Tmax + 1)
        cop = (self.eta[1:Tmax + 1] > 0) & (np.gcd(ts, q) == 1)
        total = 0.
        for r in range(len(S1) + 1):
            for sub in itertools.combinations(S1, r):
                t1 = math.prod(sub)
                eta1 = math.prod(1 / (p * p - 2) for p in sub)
                Z = x / (q * t1)
                T = math.isqrt(x // (q * t1))
                if T >= 1:
                    u = Z / self.t[1:T + 1] ** 2
                    fr = u - np.floor(u)
                    SB = float(np.sum((self.kappa[1:T + 1] * fr * (1 - fr))[cop[:T]]))
                else:
                    SB = 0.
                th = min(T, self.TSTAR)
                h2, h4 = self.heads(qprimes, th)
                br2, br4 = float(full2 - h2), float(full4 - h4)
                if T > self.TSTAR:
                    m = cop[self.TSTAR:T]
                    br2 -= self.A0 * float(np.sum(self.eta[self.TSTAR + 1:T + 1][m]))
                    br4 -= self.A0 * float(np.sum(self.eta_t2[self.TSTAR + 1:T + 1][m]))
                total += eta1 * t1 * (self.A0 * SB + Z * br2 - Z * Z * br4)
        return q * E2 * total

    def h(self, fac):
        """h(q) = I prod_{p not | q} a_p prod_{p||q} b_p prod_{p^2|q} c_p."""
        val = self.Ahmp * I_CONST
        for p, e in fac.items():
            p = mp.mpf(p)
            a = 1 - 3 / p ** 2 + 2 / p ** 3
            lam = (p - 1) * (p ** 2 - 2 + mp.sqrt(p)) / p ** 3 if e == 1 else (p - 1) ** 2 * (p + 1) / p ** 3
            val *= lam / a
        return float(val)


def factor_table(values):
    vmax = max(values)
    if vmax <= 2 * 10 ** 7:
        spf = np.zeros(vmax + 1, dtype=np.int32)
        for p in primes_upto(math.isqrt(vmax) + 1):
            p = int(p)
            blk = spf[p * p::p]
            blk[blk == 0] = p
        out = []
        for v in values:
            fac = {}
            while v > 1:
                p = int(spf[v]) or v
                while v % p == 0:
                    v //= p
                    fac[p] = fac.get(p, 0) + 1
            out.append(fac)
        return out
    return [{int(p): int(e) for p, e in sympy.factorint(v).items()} for v in values]


def identity_selftest(ar):
    """Check the exact identity of Proposition 4.1 (P2) at x = 3000 for
    q <= 40, with every term computed by brute force except MT, which uses
    Arithmetic.MT.  Returns the largest relative discrepancy."""
    x = 3000
    sf = np.ones(x + 1, dtype=np.int64)
    sf[0] = 0
    for d in range(2, math.isqrt(x) + 1):
        sf[d * d::d * d] = 0
    c6 = float(SIX_PI2)
    Qx = int(sf.sum())
    worst = 0.
    for q in range(1, 41):
        fac = {int(p): int(e) for p, e in sympy.factorint(q).items()}
        g = np.empty(q)
        for l in range(q):
            v = c6 / q * math.prod(1 / (1 - p ** -2) for p in fac)
            for p, e in fac.items():
                if e == 1 and l % p == 0:
                    v *= 1 - 1 / p
                if e >= 2 and l % (p * p) == 0:
                    v = 0.
            g[l] = v
        n = np.arange(1, x + 1)
        counts = np.bincount(n % q, weights=sf[1:], minlength=q)
        E = counts - g * x
        V = float(np.sum(E ** 2))
        Dsum = 0.
        for hh in range(1, x // q + 1):
            m = hh * q
            C = int(np.sum(sf[1:x - m + 1] * sf[1 + m:x + 1]))
            A = ar.A0 * sum(ar.eta[t] for t in range(1, math.isqrt(m) + 1) if m % (t * t) == 0)
            Dsum += C - A * (x - m)
        rhs_wo_MT = 2 * Dsum + (Qx - c6 * x) - 2 * x * float(np.sum(g * E))
        mt = ar.MT(x, q, fac)
        worst = max(worst, abs(V - (mt + rhs_wo_MT)) / max(1., abs(V)))
    return worst


def shape_rows(results, ar):
    """For selected rows: V (snapshot), sum f'(k) MT(x;f(k)) and sum F(k) h(f(k))."""
    out = []
    for name in NAMES:
        f, fp, _ = POLY[name]
        rows = all_rows(results, name)
        for x in SHAPE_XS[name]:
            rr = sorted([r for r in rows if r['x'] == x], key=lambda r: r['y'])
            ymax = rr[-1]['y']
            qs = [f(k) for k in range(1, ymax + 1)]
            facs = factor_table(qs)
            mt = np.array([fp(k) * ar.MT(x, q, fa) for k, q, fa in zip(range(1, ymax + 1), qs, facs)])
            hf = np.array([fp(k) * math.sqrt(q) * ar.h(fa) for k, q, fa in zip(range(1, ymax + 1), qs, facs)])
            cmt, ch = np.cumsum(mt), np.cumsum(hf)
            for r in rr:
                y, Y = r['y'], r['fy']
                V = float(Decimal(r['V_decimal']))
                norm = math.sqrt(x) * Y ** 1.5
                out.append(dict(poly=name, x=x, ratio_target=r['ratio_target'], ratio_actual=r['ratio_actual'],
                                y=y, N_data=V / norm, N_MT=float(cmt[y - 1]) / norm,
                                V_over_sumMT=V / float(cmt[y - 1]), N_h=float(ch[y - 1]) / Y ** 1.5))
    return out


# ----------------------------------------------------------------------------
# 4. Output
# ----------------------------------------------------------------------------

def fmt(v, nd):
    return f'{v:.{nd}f}'


def sci(x):
    e = int(round(math.log10(x)))
    m = x / 10 ** e
    if abs(m - round(m)) < 1e-9 and round(m) == 1:
        return f'$10^{{{e}}}$'
    mant = f'{x / 10 ** int(math.floor(math.log10(x))):g}'
    return f'${mant}\\cdot 10^{{{int(math.floor(math.log10(x)))}}}$'


def tex_sci(v):
    if v == 0:
        return '0'
    e = int(math.floor(math.log10(abs(v))))
    return f'{v / 10 ** e:.1f}\\cdot 10^{{{e}}}'


def tex_sci_up(v):
    """Like tex_sci for v >= 0, but with the mantissa rounded upwards, so that
    the printed number is an upper bound for v."""
    if v < 0:
        raise ValueError('tex_sci_up expects v >= 0')
    if v == 0:
        return '0'
    e = int(math.floor(math.log10(v)))
    m = Decimal(v).scaleb(-e).quantize(Decimal('0.1'), rounding=ROUND_CEILING)
    if m >= 10:
        m, e = (m / 10).quantize(Decimal('0.1'), rounding=ROUND_CEILING), e + 1
    return f'{m}\\cdot 10^{{{e}}}'


def sci_value(tex):
    """Numerical value of a string produced by tex_sci / tex_sci_up."""
    if tex == '0':
        return Decimal(0)
    m, e = tex.split('\\cdot 10^{')
    return Decimal(m).scaleb(int(e.rstrip('}')))


def write(path, text):
    path.write_text(text)
    return str(path.relative_to(HERE))


def make_outputs(results, compare, consts, c2, shape, selftest, symb, rho_checked, elapsed, floatcheck, elig):
    GEN.mkdir(exist_ok=True)
    arts = []
    # Table: constants
    lines = [r'\begin{tabular}{l' + 'r' * len(PRIME_CUTOFFS) + 'l}', r'\toprule',
             r'$f$ & ' + ' & '.join(f'$N=10^{{{int(math.log10(N))}}}$' for N in PRIME_CUTOFFS)
             + r' & interval for $C_f$ \\', r'\midrule']
    for name in NAMES + ['t']:
        c = consts[name]
        lines.append(TEXNAME[name] + ' & ' + ' & '.join(fmt(c['partial'][N], 9) for N in PRIME_CUTOFFS)
                     + f" & $[{round_out(c['lower'], 9, False)},\\,{round_out(c['upper'], 9, True)}]$ \\\\")
    lines.append(r'Vaughan $c_2$ & ' + ' & '.join(fmt(c2[N], 9) for N in PRIME_CUTOFFS) + r' & \\')
    lines += [r'\bottomrule', r'\end{tabular}', '']
    arts.append(write(GEN / 'tab_constants.tex', '\n'.join(lines)))

    # Table: largest-x normalised values and stability
    lines = [r'\begin{tabular}{l' + 'r' * (len(RATIOS) + 1) + '}', r'\toprule',
             r'$r$ & $0.005$ & ' + ' & '.join(f'${r:g}$' for r in RATIOS) + r' \\', r'\midrule']
    for name in NAMES:
        p = results['polynomials'][name]
        xs = sorted({r['x'] for r in p['rows']})
        xl = xs[-1]
        last = {r['ratio_target']: r for r in all_rows(results, name) if r['x'] == xl}
        lines.append(TEXNAME[name] + ' & ' + ' & '.join(fmt(last[r]['normalised'], 5) for r in [.005] + RATIOS) + r' \\')
        st = {s['ratio']: s['relative_change'] for s in p['stability']}
        dst = {s['ratio']: s['relative_change'] for s in p['diagnostic_stability']}
        ch = [dst.get(.005)] + [st[r] for r in RATIOS]
        lines.append(r'\quad change (\%) & ' + ' & '.join(f'${100 * c:+.4f}$' for c in ch) + r' \\')
    lines += [r'\bottomrule', r'\end{tabular}', '']
    arts.append(write(GEN / 'tab_largest.tex', '\n'.join(lines)))

    # Table: fits versus C_f
    lines = [r'\begin{tabular}{lrrrrrr}', r'\toprule',
             r'$f$ & $\alpha+\beta$ (fixed $r$) & $\beta$ (fixed $x$) & $C_{\mathrm{extr}}\pm$ envelope & $C_f$ & $\frac{C_{\mathrm{extr}}-C_f}{C_f}$ & $\frac{C_{\mathrm{extr}}-C_f}{\mathrm{envelope}}$ \\',
             r'\midrule']
    fitsum = {}
    for name in NAMES:
        p = results['polynomials'][name]
        fr, fx, ce = p['fit_fixed_ratio'], p['fit_fixed_x'], p['constant_extrapolated']
        Cf = consts[name]['value']
        rel = (ce['value'] - Cf) / Cf
        units = (ce['value'] - Cf) / ce['uncertainty']
        fitsum[name] = dict(alpha_plus_beta=fr['alpha_plus_beta'], alpha_plus_beta_se=fr['se'],
                            beta_fixed_x=fx['beta'], beta_se=fx['beta_se'], C_extrapolated=ce['value'],
                            envelope=ce['uncertainty'], C_f=Cf, relative_difference=rel,
                            difference_in_envelopes=units,
                            fit_coefficients=ce['primary_fit']['coefficients'],
                            cutoff_fits={str(v['ratio_cutoff']): v['value'] for v in ce['cutoff_fits']},
                            alternative_models={v['model']: v['value'] for v in ce['alternative_models']},
                            upper_window_fits={str(v['upper_ratio']): v['value'] for v in ce['upper_ratio_window_fits']},
                            previous_x_fit=ce['previous_x_fit']['value'],
                            joint_fit={k: p['fit_joint'][k] for k in ['alpha', 'alpha_se', 'beta', 'beta_se', 'C']})
        lines.append(TEXNAME[name] + f" & ${fr['alpha_plus_beta']:.4f}\\pm{fr['se']:.4f}$ & ${fx['beta']:.3f}\\pm{fx['beta_se']:.3f}$"
                     f" & ${ce['value']:.4f}\\pm{ce['uncertainty']:.4f}$ & ${Cf:.5f}$ & ${100 * rel:+.2f}\\%$ & ${units:+.2f}$ \\\\")
    lines += [r'\bottomrule', r'\end{tabular}', '']
    arts.append(write(GEN / 'tab_fits.tex', '\n'.join(lines)))

    # Table: model sensitivity of the extrapolation
    lines = [r'\begin{tabular}{lrrrrrr}', r'\toprule',
             r'$f$ & primary & $C+a\sqrt r$ & $C+a\sqrt r+br+cr^{3/2}$ & $r\le 0.1$ & cutoff $0.005$ & previous $x$ \\', r'\midrule']
    for name in NAMES:
        fs = fitsum[name]
        lines.append(TEXNAME[name] + f" & {fs['C_extrapolated']:.5f} & {fs['alternative_models']['sqrt']:.5f}"
                     f" & {fs['alternative_models']['sqrt+linear+threehalves']:.5f} & {fs['upper_window_fits']['0.1']:.5f}"
                     f" & {fs['cutoff_fits']['0.005']:.5f} & {fs['previous_x_fit']:.5f} \\\\")
    lines += [r'\bottomrule', r'\end{tabular}', '']
    arts.append(write(GEN / 'tab_sensitivity.tex', '\n'.join(lines)))

    # Table: exact shape
    lines = [r'\begin{tabular}{llrrrrrr}', r'\toprule',
             r'$f$ & $x$ & $r$ & $y$ & $N_{\mathrm{data}}$ & $N_{\mathrm{MT}}$ & $V_f/\Sigma_{\mathrm{MT}}$ & $N_h$ \\', r'\midrule']
    prev = None
    for row in shape:
        if row['ratio_target'] not in (.005, .01, .1, 1.):
            continue
        key = (row['poly'], row['x'])
        if prev is not None and key[0] != prev[0]:
            lines.append(r'\midrule')
        lab = TEXNAME[row['poly']] if (prev is None or key[0] != prev[0]) else ''
        xl = sci(row['x']) if key != prev else ''
        prev = key
        lines.append(f"{lab} & {xl} & ${row['ratio_target']:g}$ & {row['y']} & {row['N_data']:.5f} & {row['N_MT']:.5f}"
                     f" & {row['V_over_sumMT']:.5f} & {row['N_h']:.5f} \\\\")
    lines += [r'\bottomrule', r'\end{tabular}', '']
    arts.append(write(GEN / 'tab_shape.tex', '\n'.join(lines)))

    # Appendix tables: all normalised values
    for i, name in enumerate(NAMES):
        p = results['polynomials'][name]
        xs = sorted({r['x'] for r in p['rows']})
        lines = [r'\begin{tabular}{l' + 'r' * len(RATIOS) + '}', r'\toprule',
                 r'$x$ & ' + ' & '.join(f'${r:g}$' for r in RATIOS) + r' \\', r'\midrule']
        for x in xs:
            vals = [next(r['normalised'] for r in p['rows'] if r['x'] == x and r['ratio_target'] == rt) for rt in RATIOS]
            lines.append(sci(x) + ' & ' + ' & '.join(fmt(v, 6) for v in vals) + r' \\')
        lines += [r'\bottomrule', r'\end{tabular}', '']
        arts.append(write(GEN / f'tab_full_{i}.tex', '\n'.join(lines)))

    # Plot data
    for i, name in enumerate(NAMES):
        p = results['polynomials'][name]
        xs = sorted({r['x'] for r in p['rows']})
        last = sorted([r for r in all_rows(results, name) if r['x'] == xs[-1]], key=lambda r: r['ratio_actual'])
        txt = 'r sqrtr N\n' + ''.join(f"{r['ratio_actual']:.10g} {math.sqrt(r['ratio_actual']):.10g} {r['normalised']:.10g}\n" for r in last)
        arts.append(write(GEN / f'fig_ratio_{i}.dat', txt))
        C, a, b = fitsum[name]['fit_coefficients']
        grid = np.linspace(0, 1, 101)
        txt = 'r sqrtr N\n' + ''.join(f'{r:.6g} {math.sqrt(r):.6g} {C + a * math.sqrt(r) + b * r:.10g}\n' for r in grid)
        arts.append(write(GEN / f'fig_fit_{i}.dat', txt))
        txt = 'sqrtr N\n0 ' + f"{consts[name]['value']:.10g}\n"
        arts.append(write(GEN / f'fig_cf_{i}.dat', txt))
        for rt, tag in [(.01, 'a'), (1., 'b')]:
            rr = sorted([r for r in p['rows'] if r['ratio_target'] == rt], key=lambda r: r['x'])
            txt = 'x N\n' + ''.join(f"{r['x']} {r['normalised']:.10g}\n" for r in rr)
            arts.append(write(GEN / f'fig_x_{i}{tag}.dat', txt))
    for name in ['k^2+1', 'k^3+2']:
        i = NAMES.index(name)
        rr = sorted([s for s in shape if s['poly'] == name and s['x'] == SHAPE_XS[name][-1]], key=lambda s: s['ratio_actual'])
        txt = 'sqrtr Ndata NMT Nh\n' + ''.join(f"{math.sqrt(s['ratio_actual']):.8g} {s['N_data']:.10g} {s['N_MT']:.10g} {s['N_h']:.10g}\n" for s in rr)
        arts.append(write(GEN / f'fig_shape_{i}.dat', txt))

    # Numbers quoted in the prose of Section 10, with checks of the qualitative
    # statements made there (the script stops if one of them fails).
    xl = max(r['x'] for r in results['polynomials']['k^2+1']['rows'])
    lastrow = {name: {r['ratio_target']: r for r in all_rows(results, name) if r['x'] == xl} for name in NAMES}
    stab = {name: max(abs(s_['relative_change']) for s_ in results['polynomials'][name]['stability']) for name in NAMES}
    ndiag = [lastrow[n][.005]['normalised'] for n in NAMES]
    none_ = [lastrow[n][1.]['normalised'] for n in NAMES]
    betas = [fitsum[n]['beta_fixed_x'] for n in NAMES]
    sens_q = [fitsum['k^2+1'][k] for k in ['C_extrapolated', 'previous_x_fit']] + \
             [fitsum['k^2+1']['alternative_models'][k] for k in ['sqrt', 'sqrt+linear+threehalves']] + \
             [fitsum['k^2+1']['upper_window_fits']['0.1'], fitsum['k^2+1']['cutoff_fits']['0.005']]
    cutoffs = {results['polynomials'][n]['constant_extrapolated']['ratio_cutoff'] for n in NAMES}
    all_elig = [e for n in NAMES for e in elig[n]]
    best = max(all_elig, key=lambda e: e['delta_max'])
    claims = {
        'stability below 1% at every ratio': max(stab.values()) < 0.01,
        'k^2+1 and 2k+1 change much less than k^3+2': max(stab['k^2+1'], stab['2k+1']) < stab['k^3+2'] / 10,
        'one common stable cutoff': len(cutoffs) == 1,
        'extrapolations within their envelopes': all(abs(fitsum[n]['difference_in_envelopes']) <= 1 for n in NAMES),
        'k^2+1 sensitivity range brackets C_f': min(sens_q) < consts['k^2+1']['value'] < max(sens_q),
        'rows with r <= 0.01 outside the range for every delta': all(e['delta_max'] < 0 for e in all_elig if e['ratio_target'] <= .01),
        'C_t and Vaughan c_2 agree to 1e-8 at N=1e7': abs(consts['t']['value'] - c2[PRIME_CUTOFFS[-1]]) < 1e-8,
    }
    if not all(claims.values()):
        raise RuntimeError(f'a statement of Section 10 is not supported by the data: {claims}')
    pct = lambda v: f'{100 * v:+.2f}'

    # Macros for numbers quoted in the text.  Numbers that the text states as
    # bounds ("at most", "between", "lies in") are rounded outwards: upper
    # bounds upwards, lower bounds downwards.  Numbers stated as approximate
    # values ("about", "approximately", "\approx") are rounded to nearest.
    float_max = max(floatcheck.values())
    shape_vals = [s['V_over_sumMT'] for s in shape]
    shape_dev = max(abs(s['V_over_sumMT'] - 1) for s in shape if s['x'] == xl)
    delta_one = max(e['delta_max'] for e in all_elig if e['ratio_target'] == 1.)
    rerun_max = max(c['max_relative_difference_V'] for c in compare.values())
    stab_other = max(stab['k^2+1'], stab['2k+1'])
    i_trunc = mp.floor(I_CONST * 10 ** 12) / 10 ** 12     # I truncated (followed by \ldots)
    macros = {
        'CfQuadCert': certified_digits(consts['k^2+1']['lower'], consts['k^2+1']['upper']),
        'CfCubicCert': certified_digits(consts['k^3+2']['lower'], consts['k^3+2']['upper']),
        'CfLinCert': certified_digits(consts['2k+1']['lower'], consts['2k+1']['upper']),
        'CfTCert': certified_digits(consts['t']['lower'], consts['t']['upper']),
        'FloatCheck': tex_sci_up(float_max),                                   # "at most"
        'StabCubic': up(100 * stab['k^3+2'], 2),                               # "at most"
        'StabOther': up(100 * stab_other, 2),                                  # "at most"
        'NDiagMin': down(min(ndiag), 3), 'NDiagMax': up(max(ndiag), 3),        # "between"
        'NOneMin': down(min(none_), 3), 'NOneMax': up(max(none_), 3),          # "between"
        'BetaMin': down(min(betas), 3), 'BetaMax': up(max(betas), 3),          # "between"
        'StableCutoff': f'{cutoffs.pop():g}',
        'RelQuad': pct(fitsum['k^2+1']['relative_difference']),               # "approximately"
        'RelCubic': pct(fitsum['k^3+2']['relative_difference']),
        'RelLin': pct(fitsum['2k+1']['relative_difference']),
        'SensQuadMin': down(min(sens_q), 3), 'SensQuadMax': up(max(sens_q), 3),  # range bracketing C_f
        'XLargeInvCubeSmall': f'{xl ** (-1 / 3) * .01 ** -1.5:.1f}',           # "about"
        'XLargeInvCubeOne': tex_sci(xl ** (-1 / 3)),                           # "about"
        'XTwoNinths': f'{xl ** (-2 / 9):.4f}',                                 # "\approx"
        'DeltaRowOneMax': tex_sci_up(delta_one),                               # "\le"
        'DeltaRowMax': f"{best['delta_max']:.3f}",                             # "about"
        'DeltaRowMaxR': f"{best['ratio_target']:g}",
        'CfQuad': f"{consts['k^2+1']['value']:.8f}", 'CfCubic': f"{consts['k^3+2']['value']:.8f}",
        'CfLin': f"{consts['2k+1']['value']:.8f}", 'CfT': f"{consts['t']['value']:.8f}",   # "\approx"
        'VaughanCtwo': f"{c2[PRIME_CUTOFFS[-1]]:.8f}",                         # "\approx"
        'IConst': mp.nstr(i_trunc, 12, strip_zeros=False),                     # truncated, then "\ldots"
        'ShapeMin': down(min(shape_vals), 4), 'ShapeMax': up(max(shape_vals), 4),  # "lies in"
        'ShapeRows': str(len(shape)),
        'ShapeDevLargest': tex_sci_up(shape_dev),                              # "at most"
        'SelfTest': tex_sci_up(selftest),                                      # "at most"
        'RerunMaxRelV': tex_sci_up(rerun_max),                                 # "at most"
        'RhoBound': str(1000),
    }
    # Check that every printed bound bounds the computed quantity, and that the
    # truncated value of I is a prefix of its decimal expansion.
    bound_checks = {
        'FloatCheck >= max float discrepancy': sci_value(macros['FloatCheck']) >= Decimal(float_max),
        'StabCubic >= 100 * max change (k^3+2)': Decimal(macros['StabCubic']) >= Decimal(100 * stab['k^3+2']),
        'StabOther >= 100 * max change (k^2+1, 2k+1)': Decimal(macros['StabOther']) >= Decimal(100 * stab_other),
        'NDiag range contains the values': Decimal(macros['NDiagMin']) <= Decimal(min(ndiag))
                                            and Decimal(macros['NDiagMax']) >= Decimal(max(ndiag)),
        'NOne range contains the values': Decimal(macros['NOneMin']) <= Decimal(min(none_))
                                           and Decimal(macros['NOneMax']) >= Decimal(max(none_)),
        'Beta range contains the values': Decimal(macros['BetaMin']) <= Decimal(min(betas))
                                           and Decimal(macros['BetaMax']) >= Decimal(max(betas)),
        'SensQuad range contains the values': Decimal(macros['SensQuadMin']) <= Decimal(min(sens_q))
                                               and Decimal(macros['SensQuadMax']) >= Decimal(max(sens_q)),
        'DeltaRowOneMax >= max delta_row at r=1': sci_value(macros['DeltaRowOneMax']) >= Decimal(delta_one),
        'Shape interval contains all ratios': Decimal(macros['ShapeMin']) <= Decimal(min(shape_vals))
                                               and Decimal(macros['ShapeMax']) >= Decimal(max(shape_vals)),
        'ShapeDevLargest >= max |V/Sigma_MT - 1| at largest x': sci_value(macros['ShapeDevLargest']) >= Decimal(shape_dev),
        'SelfTest >= identity self-test discrepancy': sci_value(macros['SelfTest']) >= Decimal(selftest),
        'RerunMaxRelV >= max relative difference of V': sci_value(macros['RerunMaxRelV']) >= Decimal(rerun_max),
        'IConst is a prefix of I': mp.nstr(I_CONST, 30).startswith(macros['IConst']),
    }
    if not all(bound_checks.values()):
        raise RuntimeError(f'a printed bound does not hold: {bound_checks}')
    claims.update(bound_checks)
    tex = ''.join(f'\\newcommand{{\\{k}}}{{{v}}}\n' for k, v in macros.items())
    arts.append(write(GEN / 'macros.tex', tex))

    (GEN / 'snapshot_rerun_results.json').write_text(json.dumps(results, indent=1) + '\n')
    arts.append('generated/snapshot_rerun_results.json')

    repro = dict(
        description='All tables and plot data in the manuscript are generated by manuscript/reproduce.py; '
                    'see the per-artifact provenance below.',
        artifacts=arts,
        artifact_sources={
            'generated/tab_largest.tex': 'snapshot compute.py re-run: results.json rows at the largest x, '
                                         'diagnostic ratio 0.005 rows, and stability (relative change between the two largest x).',
            'generated/tab_fits.tex': 'snapshot compute.py re-run: fit_fixed_ratio, fit_fixed_x, constant_extrapolated; '
                                      'C_f from reproduce.py euler_constant (primes <= 1e7).',
            'generated/tab_sensitivity.tex': 'snapshot compute.py re-run: constant_extrapolated alternative_models, '
                                             'upper_ratio_window_fits, cutoff_fits, previous_x_fit.',
            'generated/tab_constants.tex': 'reproduce.py euler_constant and vaughan_c2 (not part of the snapshot); '
                                           'partial products rounded to 9 decimals, interval endpoints rounded outwards.',
            'generated/tab_shape.tex': 'V from the snapshot re-run; sum f\'(k) MT(x;f(k)) and sum F(k) h(f(k)) '
                                       'from reproduce.py Arithmetic.MT / Arithmetic.h.',
            'generated/tab_full_*.tex': 'snapshot compute.py re-run: normalised values of all primary rows.',
            'generated/fig_ratio_*.dat, fig_x_*.dat': 'snapshot compute.py re-run rows.',
            'generated/fig_fit_*.dat': 'snapshot primary fit N(r)=C+a sqrt(r)+b r (coefficients from the re-run).',
            'generated/fig_cf_*.dat': 'reproduce.py euler_constant.',
            'generated/fig_shape_*.dat': 'as tab_shape.tex, at the largest x.',
            'generated/macros.tex': 'numbers quoted in the text, from the computations above (C_f digits fixed by the '
                                    'intervals, stability, fit and sensitivity ranges, eligibility of rows for Theorem 1.1(iii), '
                                    'self-test and shape statistics); see text_claim_checks.',
            'generated/snapshot_rerun_results.json': 'results.json written by the re-run of the snapshot compute.py (all rows and fits).',
        },
        snapshot_rerun=dict(seconds=elapsed, total_seconds_of_reproduce_py=None, comparison_with_archived_results=compare,
                            note='compute.py and counts.cpp copied unchanged (SHA-256 checked); counts.cpp compiled locally by compute.py.'),
        constants={name: dict(partial={str(N): v for N, v in c['partial'].items()}, value=c['value'],
                              interval=[c['lower'], c['upper']], tail_log_bound=c['tail_log_bound'], K=c['K'])
                   for name, c in consts.items()},
        vaughan_c2={str(N): v for N, v in c2.items()},
        I=mp.nstr(I_CONST, 20), A0=mp.nstr(A0_mp(), 25),
        constants_float_check=dict(note='relative difference between the double-precision partial product '
                                        'for p <= 1e5 and a 40-digit mpmath recomputation; not a certified bound',
                                   values=floatcheck),
        constants_certified_digits={n: certified_digits(consts[n]['lower'], consts[n]['upper']) for n in consts},
        eligibility_at_largest_x=elig,
        text_claim_checks=claims,
        rho_formulas_checked_by_brute_force_for_primes_below=1000, rho_primes_checked=rho_checked,
        symbolic_checks=symb,
        identity_selftest_max_relative_discrepancy=selftest,
        fits=fitsum,
        exact_shape_rows=shape,
        parameters=dict(prime_cutoffs=PRIME_CUTOFFS, shape_xs=SHAPE_XS, ratios=RATIOS,
                        MT_head_terms_in_80_digit_arithmetic=Arithmetic.TSTAR),
        caveats='Fitted constants and their envelopes come from the snapshot code; the envelopes are heuristic '
                'sensitivity ranges, not confidence intervals. C_f intervals bound only the omitted primes; '
                'floating-point rounding is not included (see constants_float_check for an uncertified check).',
    )
    return repro


def write_reproduction(repro, total):
    repro['snapshot_rerun']['total_seconds_of_reproduce_py'] = total
    (HERE / 'reproduction.json').write_text(json.dumps(repro, indent=2) + '\n')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--work', type=pathlib.Path, default=DEFAULT_WORK,
                    help='scratch directory for the snapshot re-run (default: scratch/reproduce-work)')
    ap.add_argument('--reuse-work', action='store_true',
                    help='reuse results.json already present in the work directory instead of re-running the snapshot')
    args = ap.parse_args()
    t0 = time.monotonic()
    results, elapsed = run_snapshot(args.work.resolve(), args.reuse_work)
    print(f'snapshot results ready ({elapsed if elapsed is not None else "reused"})', flush=True)
    compare = compare_with_archive(results)
    print('comparison with archived results:', json.dumps(compare), flush=True)
    P = primes_upto(PRIME_CUTOFFS[-1])
    rho_checked = {name: rho_bruteforce_check(name) for name in NAMES + ['t']}
    consts = {name: euler_constant(name, P) for name in NAMES + ['t']}
    c2 = vaughan_c2(P)
    symb = symbolic_local_identity()
    xmax = max(max(v) for v in SHAPE_XS.values())
    ar = Arithmetic(math.isqrt(xmax) + 2)
    selftest = identity_selftest(ar)
    print(f'identity self-test: max relative discrepancy {selftest:.2e}', flush=True)
    if selftest > 1e-8:
        raise RuntimeError('identity self-test failed')
    shape = shape_rows(results, ar)
    floatcheck = {}
    for name in NAMES + ['t']:
        exact = euler_float_check(name)
        floatcheck[name] = float(abs(consts[name]['partial'][10 ** 5] / exact - 1))
    print('float check of the Euler products:', floatcheck, flush=True)
    elig = {name: eligibility(results, name) for name in NAMES}
    repro = make_outputs(results, compare, consts, c2, shape, selftest, symb, rho_checked, elapsed, floatcheck, elig)
    write_reproduction(repro, time.monotonic() - t0)
    print(f'done in {time.monotonic() - t0:.1f}s; wrote {HERE / "reproduction.json"}', flush=True)


if __name__ == '__main__':
    main()
