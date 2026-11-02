"""Entry point.  python3 compute.py [--skip-validate] [--quick]

1. validation of the algorithm (validate.py)
2. exact V_f(x,y) rows (rows.py; cached in cache/*.json, so reruns are fast)
3. fits, stability cutoff, extrapolation (analyze.py)
4. results.json
"""
import json
import os
import sys
import time

import rows
import scan
import analyze
from validate import validate

HERE = os.path.dirname(os.path.abspath(__file__))
XS = {
    "k^2+1": [10 ** 5, 2 * 10 ** 5, 5 * 10 ** 5, 10 ** 6, 2 * 10 ** 6, 5 * 10 ** 6,
              10 ** 7, 2 * 10 ** 7, 5 * 10 ** 7, 10 ** 8],
    "k^3+2": [10 ** 5, 2 * 10 ** 5, 5 * 10 ** 5, 10 ** 6, 2 * 10 ** 6, 5 * 10 ** 6,
              10 ** 7, 2 * 10 ** 7, 5 * 10 ** 7, 10 ** 8],
    "2k+1": [10 ** 5, 2 * 10 ** 5, 5 * 10 ** 5, 10 ** 6, 2 * 10 ** 6, 5 * 10 ** 6, 10 ** 7],
}
SCAN_X = {"k^2+1": 10 ** 8, "k^3+2": 10 ** 8, "2k+1": 10 ** 7}
SCAN_RATIOS = sorted(set([0.0005, 0.001, 0.002, 0.003, 0.005, 0.0075] +
                         [round(0.01 * i, 4) for i in range(1, 101)]))


def main():
    t0 = time.time()
    vpath = os.path.join(HERE, "validation.json")
    if "--skip-validate" in sys.argv and os.path.exists(vpath):
        val = json.load(open(vpath))
    else:
        val = validate()
        json.dump(val, open(vpath, "w"), indent=1)
    print("validation done %.0fs" % (time.time() - t0), flush=True)
    res = {"polynomials": {}, "validation": val}
    allrows = {}
    for name, xs in XS.items():
        rws = rows.run(name, xs)
        spath = os.path.join(rows.CACHE, "scan_%s.json" % name.replace("^", "p").replace("+", "_"))
        if os.path.exists(spath):
            sc = json.load(open(spath))
        else:
            sc = scan.scan(name, SCAN_X[name], SCAN_RATIOS)
            json.dump(sc, open(spath, "w"))
        res["polynomials"][name] = analyze.analyze(name, rws, sc)
        print(name, "analysed %.0fs" % (time.time() - t0), flush=True)
    res["notes"] = analyze.NOTES
    json.dump(res, open(os.path.join(HERE, "results.json"), "w"), indent=1)
    print("wrote results.json, total %.0fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
