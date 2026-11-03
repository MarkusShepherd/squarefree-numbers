"""Exact computation of V_f(x,y) = sum_{k<=y} f'(k) sum_{l mod f(k)} E(x;f(k),l)^2.

Method (all counts are exact integers; g-dependent parts are exact rationals
evaluated in 50-digit Decimal arithmetic, times the constant c = 6/pi^2 which
is also taken to 50 digits).

For a modulus q, with s(n) the squarefree indicator on 1..x,

  sum_l Q(x;q,l)^2 = #{(m,n) squarefree <= x : m = n mod q}
                   = C(0) + 2 * sum_{j>=1} C(j q),
  C(h) = sum_{n<=x-h} s(n) s(n+h)        (autocorrelation, ONE FFT for all q)

  sum_l g(q,l) Q(x;q,l) = sum_{n sqfree <= x} g(q, n mod q)
  g(q,l) = (c/q) prod_{p | q} u_p(l),
        p^2 | q :  u_p = 0 if p^2 | l else p^2/(p^2-1)
        p || q  :  u_p = p/(p+1) if p | l else p^2/(p^2-1)
  (the factor c/q * prod_{p|q} p^2/(p^2-1) is the density of squarefree numbers
   coprime-adjusted; checked against Moebius series and brute force in validate.py)
  For squarefree n only p||q, p|n changes u_p, giving
     sum_n s(n) g(q,n) = (c/q) R_q sum_{e | q*} mu(e)/e * S_e(x),
  R_q = prod_{p|q} p^2/(p^2-1), q* = prod_{p || q} p, S_e = #{n<=x sqfree, e | n}.

  sum_l g(q,l)^2 = (c/q)^2 prod_{p^a || q} T_p,
     a=1 : T_p = p^2 (p^2+p-1) / ((p-1)(p+1)^2),     a>=2 : T_p = p^(a+2)/(p^2-1).

  sum_l E^2 = sum_l Q^2 - 2x sum_l g Q + x^2 sum_l g^2.
"""
import numpy as np
from decimal import Decimal, getcontext
from scipy import fft as sfft
import mpmath

getcontext().prec = 50
mpmath.mp.dps = 60
C_CONST = Decimal(str(mpmath.mpf(6) / mpmath.pi ** 2))  # 6/pi^2 to 50 digits

# ---------------------------------------------------------------- polynomials
POLYS = {
    "k^2+1": (lambda k: k * k + 1, lambda k: 2 * k),
    "k^3+2": (lambda k: k ** 3 + 2, lambda k: 3 * k * k),
    "2k+1": (lambda k: 2 * k + 1, lambda k: 2),
}


def finv_floor(name, X):
    """largest k >= 0 with f(k) <= X (X real)."""
    f = POLYS[name][0]
    if name == "k^2+1":
        k = int(max(X - 1, 0) ** 0.5) + 2
    elif name == "k^3+2":
        k = int(max(X - 2, 0) ** (1 / 3)) + 2
    else:
        k = int(max((X - 1) / 2, 0)) + 2
    while k > 0 and f(k) > X:
        k -= 1
    return k


# ---------------------------------------------------------------- sieves
def squarefree_indicator(N):
    """uint8 array s[0..N], s[n]=1 iff n squarefree (s[0]=0)."""
    s = np.ones(N + 1, dtype=np.uint8)
    s[0] = 0
    p = 2
    while p * p <= N:
        s[p * p::p * p] = 0
        p += 1
    return s


def spf_sieve(N):
    spf = np.zeros(N + 1, dtype=np.int32)
    p = 2
    while p * p <= N:
        if spf[p] == 0:
            seg = spf[p * p::p]
            seg[seg == 0] = p
        p += 1
    idx = spf == 0
    idx[:2] = False
    spf[idx] = np.nonzero(idx)[0].astype(np.int32)
    return spf


def autocorrelation(s, x):
    """C[h] = #{1<=n<=x-h : s[n] s[n+h]} for h=0..x, exact int64 (FFT + rounding).
    s has length >= x+1."""
    a = s[:x + 1].astype(np.float64)
    n = sfft.next_fast_len(2 * (x + 1), real=True)
    F = sfft.rfft(a, n, workers=-1)
    F = F.real ** 2 + F.imag ** 2
    c = sfft.irfft(F, n, workers=-1)[:x + 1]
    Ci = np.rint(c).astype(np.int64)
    err = float(np.max(np.abs(c - Ci)))
    return Ci, err


# ---------------------------------------------------------------- per-state
class State:
    """Everything needed for one value of x."""

    def __init__(self, x, qmax):
        self.x = x
        self.s = squarefree_indicator(max(x, 1))
        self.C, self.fft_err = autocorrelation(self.s, x)
        self.qmax = max(qmax, 2)
        self.spf = spf_sieve(self.qmax)
        self.Scache = {}
        self.Cm = None

    def S(self, e):
        v = self.Scache.get(e)
        if v is None:
            v = int(np.count_nonzero(self.s[e::e])) if e <= self.x else 0
            self.Scache[e] = v
        return v

    def factor(self, q):
        spf = self.spf
        out = []
        while q > 1:
            p = int(spf[q])
            a = 0
            while q % p == 0:
                q //= p
                a += 1
            out.append((p, a))
        return out

    def sumsq_E(self, q):
        """exact (to 50 digits) sum_{l=1}^q E(x;q,l)^2."""
        x = self.x
        A = int(self.C[0]) + 2 * int(self.C[q::q].sum())  # sum_l Q^2 (integer)
        fac = self.factor(q)
        Rn = Rd = 1
        Tn = Td = 1
        divs = [(1, 1)]
        qstar = 1
        for p, a in fac:
            Rn *= p * p
            Rd *= p * p - 1
            if a == 1:
                Tn *= p * p * (p * p + p - 1)
                Td *= (p - 1) * (p + 1) ** 2
                qstar *= p
                divs = divs + [(e * p, -m) for e, m in divs]
            else:
                Tn *= p ** (a + 2)
                Td *= p * p - 1
        M = 0
        for e, m in divs:
            M += m * self.S(e) * (qstar // e)
        Bp = Decimal(Rn * M) / Decimal(Rd * q * qstar)       # sum_l g Q = c * Bp
        Dp = Decimal(Tn) / Decimal(Td * q * q)               # sum_l g^2 = c^2 * Dp
        c = C_CONST
        return Decimal(A) - 2 * x * c * Bp + x * x * c * c * Dp


# ---------------------------------------------------------------- g closed form
def g_closed(q, l):
    """g(q,l) / c as an exact Fraction (c = 6/pi^2)."""
    from fractions import Fraction
    from sympy import factorint
    r = Fraction(1, q)
    for p, a in factorint(q).items():
        if a >= 2:
            r *= 0 if l % (p * p) == 0 else Fraction(p * p, p * p - 1)
        else:
            r *= Fraction(p, p + 1) if l % p == 0 else Fraction(p * p, p * p - 1)
    return r
