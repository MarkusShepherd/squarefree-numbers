"""Stage 1: exact V_f(x,y) rows for one polynomial and a list of x.  Cached in cache/."""
import json
import math
import os
import sys
import time
from fractions import Fraction

import mpmath as mp
import numpy as np

from sqfcore import Factorer, XData, primes_upto, sieve_sf, spf_sieve

RATIOS = [Fraction(1, 100), Fraction(2, 100), Fraction(5, 100), Fraction(1, 10),
          Fraction(2, 10), Fraction(4, 10), Fraction(7, 10), Fraction(1)]
POLYS = {
    "k^2+1": (lambda k: k * k + 1, lambda k: 2 * k),
    "k^3+2": (lambda k: k ** 3 + 2, lambda k: 3 * k * k),
    "2k+1": (lambda k: 2 * k + 1, lambda k: 2),
}
EXACT_Q = 3000          # moduli q <= EXACT_Q always use the exact-rational path
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")


def y_of(f, x, ratio):
    """largest k with f(k) <= ratio*x."""
    lim = ratio * x
    lo, hi = 0, 1
    while f(hi) <= lim:
        hi *= 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if f(mid) <= lim:
            lo = mid
        else:
            hi = mid
    return lo


def rows_for(name, x, sf_full, spf, fact, log=print):
    f, fp = POLYS[name]
    t0 = time.time()
    xd = XData(x, sf_full)
    ys = {}
    for r in RATIOS:
        ys.setdefault(y_of(f, x, r), []).append(r)
    ymax = max(ys)
    total = mp.mpf(0)
    ftot = 0.0
    rows = []
    for k in range(1, ymax + 1):
        q = f(k)
        fac = fact(q)
        if q <= EXACT_Q:
            total += fp(k) * xd.V_modulus_exact(q, fac)
        else:
            ftot += fp(k) * xd.V_modulus_float(q, fac)
        if k in ys:
            V = total + mp.mpf(ftot)
            for r in ys[k]:
                rows.append({"x": x, "y": k, "fy": q, "ratio_nominal": float(r),
                             "V": float(V), "V_str": mp.nstr(V, 25)})
    log("  %s x=%d: ymax=%d, %d moduli, fft_err=%.1e, %.1fs" % (
        name, x, ymax, ymax, xd.fft_err, time.time() - t0))
    return rows


def run(name, xs, log=print):
    os.makedirs(CACHE, exist_ok=True)
    todo = []
    for x in xs:
        path = os.path.join(CACHE, "%s_%d.json" % (name.replace("^", "p").replace("+", "_"), x))
        if not os.path.exists(path):
            todo.append((x, path))
    if todo:
        xmax = max(x for x, _ in todo)
        f, _ = POLYS[name]
        spf = spf_sieve(xmax) if name == "2k+1" else None
        fact = Factorer(spf=spf, primes=primes_upto(math.isqrt(xmax) + 10))
        sf_full = sieve_sf(xmax)
        for x, path in todo:
            rows = rows_for(name, x, sf_full, spf, fact, log)
            with open(path, "w") as fh:
                json.dump(rows, fh)
    out = []
    for x in xs:
        path = os.path.join(CACHE, "%s_%d.json" % (name.replace("^", "p").replace("+", "_"), x))
        out += json.load(open(path))
    return out


if __name__ == "__main__":
    name = sys.argv[1]
    xs = [int(float(a)) for a in sys.argv[2:]]
    run(name, xs)
