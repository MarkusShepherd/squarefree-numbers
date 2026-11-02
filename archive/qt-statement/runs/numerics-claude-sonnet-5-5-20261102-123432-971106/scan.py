"""Diagnostic: normalised V on a fine ratio grid at a single x (cumulative pass)."""
import json, math, os, sys
from fractions import Fraction
import mpmath as mp
import numpy as np
from rows import POLYS, y_of, EXACT_Q, CACHE
from sqfcore import Factorer, XData, primes_upto, sieve_sf, spf_sieve

def scan(name, x, ratios):
    f, fp = POLYS[name]
    spf = spf_sieve(x) if name == "2k+1" else None
    fact = Factorer(spf=spf, primes=primes_upto(math.isqrt(x) + 10))
    xd = XData(x, sieve_sf(x))
    ys = {}
    for r in ratios:
        ys.setdefault(y_of(f, x, Fraction(r).limit_denominator(10**6)), []).append(r)
    total = mp.mpf(0); ftot = 0.0; out = []
    for k in range(1, max(ys) + 1):
        q = f(k); fac = fact(q)
        if q <= EXACT_Q: total += fp(k) * xd.V_modulus_exact(q, fac)
        else: ftot += fp(k) * xd.V_modulus_float(q, fac)
        if k in ys:
            V = float(total + mp.mpf(ftot))
            for r in ys[k]:
                out.append({"x": x, "y": k, "fy": q, "ratio_nominal": r, "V": V,
                            "N": V / (x ** .5 * q ** 1.5)})
    return out

if __name__ == "__main__":
    name = sys.argv[1]; x = int(float(sys.argv[2]))
    ratios = sorted(set([round(0.005 * i, 6) for i in range(1, 201)]))
    out = scan(name, x, ratios)
    json.dump(out, open(os.path.join(CACHE, "scan_%s_%d.json" % (name.replace("^","p").replace("+","_"), x)), "w"))
    for o in out:
        print("%.3f %.5f %.5f" % (o["ratio_nominal"], o["fy"] / x, o["N"]))
