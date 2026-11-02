"""Core routines: exact V_f(x,y) for squarefree numbers in progressions.

Method (all counts are exact integers):

  sum_l Q(x;q,l)^2 = #{(n,m) squarefree <= x : n = m mod q}
                   = S0 + 2 * sum_{j>=1} C(jq),
  C(h) = #{n <= x-h : n and n+h both squarefree}   (autocorrelation, one FFT per x)

so A_q := sum_l Q^2 costs x/q operations instead of x.

Closed form of g.  With c = 6/pi^2 = prod_p (1-p^-2) and p^a || q,
  g(q,l) = (c/q) prod_{p|q} (1-p^-2)^-1 * c_p(l),
  c_p(l) = 1            if p does not divide l,
           1 - 1/p      if p | l and a = 1,
           1            if p || l and a >= 2,
           0            if p^2 | l and a >= 2.
Hence (for squarefree n, so that v_p(n) <= 1)
  sum_l g(q,l) Q(x;q,l) = sum_{n sf <= x} g(q,n)
       = (c/q) W_q sum_{e | q1} mu(e)/e * S(e),
  W_q = prod_{p|q} p^2/(p^2-1), q1 = prod_{p || q} p, S(e) = #{n<=x sf : e | n},
and  sum_l g(q,l)^2 = (c/q)^2 W_q^2 T_q,  T_q = prod t(p^a),
  t(p) = (p-1) + (1-1/p)^2,  t(p^a) = p^a - p^(a-2)  (a >= 2).
Then  sum_l E^2 = A_q - 2 x sum_l g Q + x^2 sum_l g^2.
"""
import math
from fractions import Fraction

import numpy as np
import mpmath as mp
from scipy import fft as sfft

mp.mp.dps = 50
C_SQ = mp.mpf(6) / mp.pi ** 2          # 1/zeta(2)


# ---------------------------------------------------------------- sieves
def primes_upto(n):
    if n < 2:
        return []
    s = np.ones(n + 1, dtype=bool)
    s[:2] = False
    for p in range(2, math.isqrt(n) + 1):
        if s[p]:
            s[p * p::p] = False
    return np.nonzero(s)[0].tolist()


def sieve_sf(N):
    """int8 indicator of squarefree n, index 0..N (sf[0]=0)."""
    s = np.ones(N + 1, dtype=np.int8)
    s[0] = 0
    for p in primes_upto(math.isqrt(N)):
        s[p * p::p * p] = 0
    return s


def spf_sieve(M):
    spf = np.zeros(M + 1, dtype=np.int32)
    for p in range(2, math.isqrt(M) + 1):
        if spf[p] == 0:
            seg = spf[p * p::p]
            seg[seg == 0] = p
    idx = np.nonzero(spf == 0)[0]
    spf[idx] = idx
    return spf


class Factorer:
    def __init__(self, spf=None, primes=None):
        self.spf = spf
        self.primes = primes or []

    def __call__(self, q):
        fac = {}
        if self.spf is not None and q < len(self.spf):
            spf = self.spf
            while q > 1:
                p = int(spf[q])
                fac[p] = fac.get(p, 0) + 1
                q //= p
            return fac
        for p in self.primes:
            if p * p > q:
                break
            if q % p == 0:
                a = 0
                while q % p == 0:
                    q //= p
                    a += 1
                fac[p] = a
        if q > 1:
            fac[q] = fac.get(q, 0) + 1
        return fac


# ---------------------------------------------------------------- g(q,l)
def g_rational_part(q, l, fac):
    """g(q,l) = (6/pi^2) * result  (exact Fraction)."""
    r = Fraction(1, q)
    for p, a in fac.items():
        r /= (1 - Fraction(1, p * p))
        if l % p:
            cp = Fraction(1)
        elif a == 1:
            cp = 1 - Fraction(1, p)
        elif l % (p * p):
            cp = Fraction(1)
        else:
            cp = Fraction(0)
        r *= cp
    return r


# ---------------------------------------------------------------- per-x data
def autocorr_int(s):
    n = len(s)
    L = sfft.next_fast_len(2 * n, real=True)
    F = sfft.rfft(s.astype(np.float64), L, workers=-1)
    P = F.real ** 2 + F.imag ** 2
    del F
    r = sfft.irfft(P, L, workers=-1)[:n]
    ri = np.rint(r)
    err = float(np.abs(r - ri).max())
    return ri.astype(np.int64), err


class XData:
    """Everything that depends on x only."""

    def __init__(self, x, sf_full):
        self.x = x
        self.sf = sf_full[:x + 1]
        self.S0 = int(self.sf.sum(dtype=np.int64))
        self.C, self.fft_err = autocorr_int(self.sf[1:])   # C[h], h=0..x-1
        assert self.C[0] == self.S0
        self.Scache = {}

    def S(self, e):
        v = self.Scache.get(e)
        if v is None:
            v = int(self.sf[e:self.x + 1:e].sum(dtype=np.int64))
            self.Scache[e] = v
        return v

    def A(self, q):
        """sum_l Q(x;q,l)^2, exact integer."""
        return self.S0 + 2 * int(self.C[q::q].sum(dtype=np.int64))

    def terms(self, q, fac):
        """Exact Fractions P, R with sum_l gQ = c*P, sum_l g^2 = c^2*R."""
        W = Fraction(1)
        T = Fraction(1)
        divs = [(1, 1)]
        for p, a in fac.items():
            W *= Fraction(p * p, p * p - 1)
            if a == 1:
                T *= Fraction((p - 1) * p * p + (p - 1) ** 2, p * p)
                divs += [(e * p, -m) for e, m in divs]
            else:
                T *= p ** a - p ** (a - 2)
        Bp = sum(Fraction(m * self.S(e), e) for e, m in divs)
        return W * Bp / q, W * W * T / (q * q)

    def terms_float(self, q, fac):
        W = 1.0
        T = 1.0
        divs = [(1, 1)]
        for p, a in fac.items():
            W *= p * p / (p * p - 1.0)
            if a == 1:
                pm = p - 1.0
                T *= (pm * p * p + pm * pm) / (p * p)
                divs += [(e * p, -m) for e, m in divs]
            else:
                T *= float(p ** a - p ** (a - 2))
        Bp = 0.0
        for e, m in divs:
            Bp += m * self.S(e) / e
        return W * Bp / q, W * W * T / (q * q)

    def V_modulus_exact(self, q, fac):
        """sum_l E(x;q,l)^2 as mpf (50 digits)."""
        P, R = self.terms(q, fac)
        x = self.x
        A = self.A(q)
        Pm = mp.mpf(P.numerator) / P.denominator
        Rm = mp.mpf(R.numerator) / R.denominator
        return A - 2 * x * C_SQ * Pm + x * x * C_SQ ** 2 * Rm

    def V_modulus_float(self, q, fac):
        P, R = self.terms_float(q, fac)
        x = self.x
        c = float(C_SQ)
        return self.A(q) - 2 * x * c * P + x * x * c * c * R
