"""Entry point.  python3 compute.py [--skip-validate] [--xs 100000,316228,...]

Stages: validate -> exact V_f(x,y) (cached in raw/*.json) -> analysis -> results.json
"""
import json
import os
import sys
import time
import multiprocessing as mp
from decimal import Decimal

import numpy as np

import sqf
from sqf import POLYS, State, finv_floor

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
RATIOS = [0.01, 0.02, 0.05, 0.1, 0.2, 0.4, 0.7, 1.0]
# extra y checkpoints for the linear case (diagnostics of the r-dependence only; rows use RATIOS)
RATIOS_DENSE = sorted(set(RATIOS) | {round(float(v), 6) for v in np.geomspace(1e-5, 1.0, 81)}
                      | {round(0.05 * i, 6) for i in range(1, 21)})
XS = [100000, 316228, 1000000, 3162278, 10000000, 31622777, 100000000]
XS_LINEAR_MAX = int(os.environ.get("LINEAR_XMAX", 100000000))

ST = None  # module-global state shared with forked workers


def _work(args):
    name, k0, k1, keep = args
    f, fp = POLYS[name]
    out = []
    tot = Decimal(0)
    for k in range(k0, k1 + 1):
        t = fp(k) * ST.sumsq_E(f(k))
        if keep:
            out.append(str(t))
        else:
            tot += t
    return (str(tot), out)


def compute_poly(name, x, pool):
    """Returns dict with exact cumulative V at required y values.
    k^2+1, k^3+2: every k up to first k with f(k) > x (for interpolation);
    2k+1: only the grid y's."""
    f, fp = POLYS[name]
    if name != "2k+1":
        ymax = finv_floor(name, x) + 1
        chunks = [(name, k, min(k + 19, ymax), True) for k in range(1, ymax + 1, 20)]
        terms = []
        for _, out in pool.map(_work, chunks):
            terms.extend(Decimal(t) for t in out)
        cum = []
        run = Decimal(0)
        for t in terms:
            run += t
            cum.append(run)
        return {"ks": list(range(1, ymax + 1)), "fk": [f(k) for k in range(1, ymax + 1)],
                "V": [str(v) for v in cum]}
    ys = sorted({finv_floor(name, r * x) for r in RATIOS_DENSE} - {0})
    chunks = []
    prev = 0
    for y in ys:
        for k in range(prev + 1, y + 1, 20000):
            chunks.append((name, k, min(k + 19999, y), False))
        prev = y
    res = pool.map(_work, chunks)
    # accumulate sums per checkpoint
    cum = {}
    run = Decimal(0)
    i = 0
    prev = 0
    for y in ys:
        n = len(range(prev + 1, y + 1, 20000))
        for j in range(n):
            run += Decimal(res[i][0])
            i += 1
        cum[y] = run
        prev = y
    return {"ks": ys, "fk": [f(y) for y in ys], "V": [str(cum[y]) for y in ys]}


def run_all(xs, force=False):
    global ST
    os.makedirs(RAW, exist_ok=True)
    for x in xs:
        names = [n for n in POLYS if (n != "2k+1" or x <= XS_LINEAR_MAX)]
        todo = [n for n in names if force or not os.path.exists(os.path.join(RAW, f"{n}_{x}.json"))]
        if not todo:
            continue
        t0 = time.time()
        qmax = max(POLYS[n][0](finv_floor(n, x) + 1) for n in todo)
        ST = State(x, qmax)
        print(f"x={x}: state built in {time.time()-t0:.1f}s (fft max |c-round|={ST.fft_err:.1e})", flush=True)
        assert ST.fft_err < 1e-3
        ctx = mp.get_context("fork")
        with ctx.Pool(11) as pool:
            for n in todo:
                t1 = time.time()
                r = compute_poly(n, x, pool)
                r.update({"x": x, "name": n, "fft_err": ST.fft_err})
                with open(os.path.join(RAW, f"{n}_{x}.json"), "w") as fh:
                    json.dump(r, fh)
                print(f"  {n}: {len(r['ks'])} y-values, {time.time()-t1:.1f}s", flush=True)
        ST = None


def main():
    args = sys.argv[1:]
    xs = XS
    if "--xs" in args:
        xs = [int(v) for v in args[args.index("--xs") + 1].split(",")]
    validation = []
    vfile = os.path.join(HERE, "validation.json")
    if "--skip-validate" not in args:
        import validate
        validation = validate.run()
        json.dump(validation, open(vfile, "w"), indent=1)
    elif os.path.exists(vfile):
        validation = json.load(open(vfile))
    run_all(xs)
    import analyze
    analyze.main(xs, validation)


if __name__ == "__main__":
    main()
