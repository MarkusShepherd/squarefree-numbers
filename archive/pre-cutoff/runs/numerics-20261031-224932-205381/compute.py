#!/usr/bin/env python3
"""Driver: exact V_f(x,y) for f = k^2+1, k^3+2, 2k+1; fits; results.json.

   python3 compute.py            # build ./sqf if needed, run everything (cached in raw_data.json), write results.json
   python3 compute.py --fresh    # ignore cache

All counting is done exactly by the C program sqf.c (integers), and the combination
sum_l E^2 = T - 2uM/q' + u^2 S is done in double-double arithmetic (~32 digits).
Only the python stdlib is used (no numpy available).  Validation lives in validate.py.
"""
import json, math, os, subprocess, sys, time
from decimal import Decimal, getcontext
getcontext().prec = 40

HERE = os.path.dirname(os.path.abspath(__file__))
RATIOS = [0.01, 0.02, 0.05, 0.1, 0.2, 0.4, 0.7, 1.0]
XS_QC = [10**4, 2 * 10**4, 5 * 10**4, 10**5, 2 * 10**5, 5 * 10**5, 10**6, 2 * 10**6, 5 * 10**6, 10**7]
XS_LIN = [10**4, 2 * 10**4, 5 * 10**4, 10**5, 2 * 10**5, 5 * 10**5, 10**6, 2 * 10**6, 5 * 10**6]
POLYS = {  # name: (id, f, f', inverse real root, x list, method, dense)
    "k^2+1": (0, lambda k: k * k + 1, lambda t: math.sqrt(max(t - 1, 0)), XS_QC, "direct", True),
    "k^3+2": (1, lambda k: k ** 3 + 2, lambda t: max(t - 2, 0) ** (1 / 3), XS_QC, "direct", True),
    "2k+1": (2, lambda k: 2 * k + 1, lambda t: (t - 1) / 2, XS_LIN, "fft", False),
}
XMIN_FIT = 10**6          # rows with x >= XMIN_FIT used for the fixed-ratio / joint exponent fits

# ------------------------------------------------------------------ running the C code
def run_c(poly, x, method, ys):
    out = subprocess.run([os.path.join(HERE, "sqf"), str(poly), str(x), method, "0"] + [str(y) for y in ys],
                         capture_output=True, text=True, check=True).stdout
    res = {}
    for line in out.splitlines():
        if line.startswith("Y"):
            _, y, fy, h, l = line.split()
            res[int(y)] = (int(fy), str(Decimal(h) + Decimal(l)))
    return res

def grid_ys(name, x):
    pid, f, finv, _, _, _ = POLYS[name]
    ys = {}
    for r in RATIOS:
        t = r * x
        y = max(1, round(finv(t)))
        while f(y) > x: y -= 1          # f(y) <= x always
        ys[r] = y
    return ys

DENSE_R = [i * 0.0025 for i in range(1, 401)]      # supplementary dense ratio grid 0.0025 .. 1.0

def collect(fresh):
    cache = os.path.join(HERE, "raw_data.json")
    raw = {} if fresh or not os.path.exists(cache) else json.load(open(cache))
    for name, (pid, f, finv, xs, method, dense) in POLYS.items():
        for x in xs:
            key = f"{name}|{x}"
            if key in raw: continue
            gy = grid_ys(name, x)
            if dense:
                ymax = max(gy.values()); ys = list(range(1, ymax + 1))
            else:
                ys = sorted(set(gy.values()))
            t0 = time.time()
            res = run_c(pid, x, method, ys)
            raw[key] = {str(y): list(v) for y, v in res.items()}
            print(f"{key}: {len(ys)} checkpoints, {time.time()-t0:.1f}s", flush=True)
            json.dump(raw, open(cache, "w"))
    # supplementary dense profile for the linear control (the other two have all y stored)
    for x in XS_LIN[-2:]:
        key = f"2k+1|dense|{x}"
        if key in raw: continue
        ys = sorted({min(max(1, round((r * x - 1) / 2)), (x - 1) // 2) for r in DENSE_R})
        res = run_c(2, x, "fft", ys)
        raw[key] = {str(y): list(v) for y, v in res.items()}
        print(f"{key}: {len(ys)} checkpoints", flush=True)
        json.dump(raw, open(cache, "w"))
    return raw

# ------------------------------------------------------------------ small linear algebra
def solve(A, b):
    n = len(A); M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c])); M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c:
                fac = M[r][c] / M[c][c]
                for k in range(c, n + 1): M[r][k] -= fac * M[c][k]
    return [M[i][n] / M[i][i] for i in range(n)]

def inv(A):
    n = len(A); cols = [solve(A, [1.0 if i == j else 0.0 for i in range(n)]) for j in range(n)]
    return [[cols[j][i] for j in range(n)] for i in range(n)]

def ols(X, y):
    """returns coef, se (nan if dof=0), rss, dof"""
    n, p = len(X), len(X[0])
    XtX = [[sum(X[k][i] * X[k][j] for k in range(n)) for j in range(p)] for i in range(p)]
    Xty = [sum(X[k][i] * y[k] for k in range(n)) for i in range(p)]
    beta = solve(XtX, Xty)
    rss = sum((y[k] - sum(X[k][i] * beta[i] for i in range(p))) ** 2 for k in range(n))
    dof = n - p
    if dof > 0:
        s2 = rss / dof; I = inv(XtX); se = [math.sqrt(s2 * I[i][i]) for i in range(p)]
    else:
        se = [float("nan")] * p
    return beta, se, rss, dof

# ------------------------------------------------------------------ analysis
def analyse(raw):
    out = {}
    for name, (pid, f, finv, xs, method, dense) in POLYS.items():
        rows, norm = [], []
        Ntab = {}   # (x, r) -> (N_actual, ratio_actual, N_at_nominal_ratio)
        for x in xs:
            data = {int(y): (v[0], float(Decimal(v[1]))) for y, v in raw[f"{name}|{x}"].items()}
            gy = grid_ys(name, x)
            def Nfun(y):
                fy, V = data[y]; return V / (x ** 0.5 * fy ** 1.5)
            for r in RATIOS:
                y = gy[r]; fy, V = data[y]
                N = Nfun(y); ra = fy / x
                # N at exactly the nominal ratio: linear interpolation in fy between adjacent y (dense data only)
                Nn = N
                if dense:
                    t = r * x
                    lo = max(k for k in data if data[k][0] <= t) if any(data[k][0] <= t for k in data) else None
                    if lo is not None and lo + 1 in data and data[lo][0] < t:
                        a, b = data[lo][0], data[lo + 1][0]; w = (t - a) / (b - a)
                        Nn = (1 - w) * Nfun(lo) + w * Nfun(lo + 1)
                    elif lo is not None and data[lo][0] == t:
                        Nn = Nfun(lo)
                rows.append({"x": x, "y": y, "fy": fy, "V": V, "V_exact": raw[f"{name}|{x}"][str(y)][1]})
                norm.append({"x": x, "ratio": r, "ratio_actual": ra, "V_over_x12_fy32": N,
                             "V_over_x12_fy32_at_nominal_ratio": Nn})
                Ntab[(x, r)] = (N, ra, Nn)
        res = {"rows": rows, "normalised": norm}
        # ---- fixed x, vary y
        fx = {}
        for x in xs:
            rr = [rw for rw in rows if rw["x"] == x]
            X = [[1.0, math.log(rw["fy"])] for rw in rr]; yv = [math.log(rw["V"]) for rw in rr]
            b, se, _, _ = ols(X, yv)
            fx[x] = {"beta": b[1], "beta_se": se[1], "logC_at_alpha_free": b[0]}
        xl = xs[-1]
        res["fit_fixed_x"] = {"x": xl, "beta": fx[xl]["beta"], "beta_se": fx[xl]["beta_se"],
                              "all_x": {str(x): {"beta": v["beta"], "beta_se": v["beta_se"]} for x, v in fx.items()},
                              "note": "OLS of log V on log f(y) over the 8 grid ratios (ratio range 0.01..1); first fields are for the largest x"}
        # ---- fixed ratio, vary x : pooled with ratio fixed effects (x >= XMIN_FIT)
        sel = [nm for nm in norm if nm["x"] >= XMIN_FIT]
        rowmap = {(rw["x"], rw["y"]): rw for rw in rows}
        lx, lv, gid = [], [], []
        for rw, nm in zip(rows, norm):
            if rw["x"] >= XMIN_FIT:
                lx.append(math.log(rw["x"])); lv.append(math.log(rw["V"])); gid.append(nm["ratio"])
        # demean within ratio group
        dx, dv = [], []
        for r in RATIOS:
            idx = [i for i, g in enumerate(gid) if g == r]
            mx = sum(lx[i] for i in idx) / len(idx); mv = sum(lv[i] for i in idx) / len(idx)
            for i in idx: dx.append(lx[i] - mx); dv.append(lv[i] - mv)
        sxx = sum(a * a for a in dx); slope = sum(a * b for a, b in zip(dx, dv)) / sxx
        rss = sum((b - slope * a) ** 2 for a, b in zip(dx, dv)); dof = len(dx) - len(RATIOS) - 1
        se = math.sqrt(rss / dof / sxx)
        per = {}
        for r in RATIOS:
            pts = [(math.log(nm["x"]), math.log(rw["V"])) for rw, nm in zip(rows, norm) if nm["ratio"] == r and nm["x"] >= XMIN_FIT]
            b, s, _, _ = ols([[1.0, a] for a, _ in pts], [c for _, c in pts]); per[str(r)] = {"slope": b[1], "se": s[1]}
        res["fit_fixed_ratio"] = {"alpha_plus_beta": slope, "se": se,
                                  "method": f"pooled OLS of log V on log x with a separate intercept per ratio, rows with x>={XMIN_FIT}",
                                  "per_ratio": per}
        # ---- joint fit log V = logC + alpha log x + beta log fy
        X = [[1.0, math.log(rw["x"]), math.log(rw["fy"])] for rw in rows if rw["x"] >= XMIN_FIT]
        yv = [math.log(rw["V"]) for rw in rows if rw["x"] >= XMIN_FIT]
        b, s, _, _ = ols(X, yv)
        res["fit_joint"] = {"C": math.exp(b[0]), "logC": b[0], "logC_se": s[0], "alpha": b[1], "alpha_se": s[1],
                            "beta": b[2], "beta_se": s[2], "rows": f"x>={XMIN_FIT}, all 8 ratios",
                            "note": "free-exponent fit; C is correlated with the exponents, see constant_extrapolated for the real constant"}
        # ---- stability and extrapolation
        res["constant_extrapolated"] = extrapolate(name, xs, Ntab)
        res["constant_extrapolated"]["dense_grid_check"] = dense_check(name, xs, raw)
        out[name] = res
    return out

def profile_sampler(name, x, raw):
    """returns function r -> N(r)=V/(x^1/2 f(y)^3/2) at (interpolated to) the exact ratio r."""
    if name == "2k+1":
        data = {int(y): (v[0], float(Decimal(v[1]))) for y, v in raw[f"{name}|dense|{x}"].items()}
        def N(r):
            y = min(max(1, round((r * x - 1) / 2)), (x - 1) // 2); fy, V = data[y]
            return V / (x ** 0.5 * fy ** 1.5)
        return N
    data = {int(y): (v[0], float(Decimal(v[1]))) for y, v in raw[f"{name}|{x}"].items()}
    ks = sorted(data)
    def Nk(k):
        fy, V = data[k]; return V / (x ** 0.5 * fy ** 1.5)
    def N(r):
        t = r * x
        lo = max((k for k in ks if data[k][0] <= t), default=None)
        if lo is None: return None
        if lo + 1 not in data or data[lo][0] == t: return Nk(lo)
        a, b = data[lo][0], data[lo + 1][0]; w = (t - a) / (b - a)
        return (1 - w) * Nk(lo) + w * Nk(lo + 1)
    return N

def dense_check(name, xs, raw):
    x1, x2 = xs[-2], xs[-1]
    S1, S2 = profile_sampler(name, x1, raw), profile_sampler(name, x2, raw)
    rs = [r for r in DENSE_R if S1(r) is not None and S2(r) is not None]
    rel = {r: S1(r) / S2(r) - 1 for r in rs}
    cut = None
    for i, r in enumerate(rs):
        if all(abs(rel[q]) < 0.01 for q in rs[i:]): cut = r; break
    out = {"grid": "r = 0.0025*i, i=1..400 (linear interpolation of N in f(y) between adjacent y for the polynomial cases)",
           "x_pair": [x1, x2], "dense_stability_cutoff_1pct": cut}
    tab = {}
    for a in (0.01, 0.02, 0.05):
        for b in (0.1, 0.15, 0.2):
            w = [r for r in rs if a - 1e-12 <= r <= b + 1e-12]
            if len(w) < 6: continue
            for m in ("1+r", "1+r+r^2"):
                bb, se, _, _ = ols([MODELS[m](r) for r in w], [S2(r) for r in w])
                tab[f"[{a},{b}]|{m}"] = {"N0": bb[0], "ols_se": se[0]}
    vals = sorted(v["N0"] for v in tab.values())
    out["N0_by_window_and_model"] = tab
    out["N0_median"] = vals[len(vals) // 2]; out["N0_min"] = vals[0]; out["N0_max"] = vals[-1]
    out["N_profile_largest_x"] = {f"{r:.4f}": S2(r) for r in rs[3::4]}
    return out

MODELS = {
    "1+r": lambda r: [1.0, r],
    "1+r+r^2": lambda r: [1.0, r, r * r],
    "1+sqrt(r)": lambda r: [1.0, math.sqrt(r)],
    "1+sqrt(r)+r": lambda r: [1.0, math.sqrt(r), r],
}

def extrapolate(name, xs, Ntab):
    x1, x2 = xs[-2], xs[-1]
    rel = {r: Ntab[(x1, r)][2] / Ntab[(x2, r)][2] - 1 for r in RATIOS}
    # cutoff: smallest ratio such that every grid ratio >= it changes by < 1% (|N(x1)/N(x2)-1| < 0.01)
    cut = None
    for i, r in enumerate(RATIOS):
        if all(abs(rel[rr]) < 0.01 for rr in RATIOS[i:]): cut = i; break
    info = {"stability_x_pair": [x1, x2],
            "stability_rel_change_by_ratio": {str(r): rel[r] for r in RATIOS}}
    if cut is None:
        info.update({"value": None, "uncertainty": None, "method": "no ratio passes the 1% stability test; no extrapolation reported",
                     "ratio_cutoff": None, "cutoff_sensitivity": "n/a"})
        return info
    def fit(ci, model):
        rs = RATIOS[ci:]
        X = [MODELS[model](r) for r in rs]; yv = [Ntab[(x2, r)][2] for r in rs]
        if len(rs) < len(X[0]): return None
        b, s, rss, dof = ols(X, yv)
        return b[0], s[0], dof, len(rs)
    primary = None
    table = {}
    for ci in (cut - 1, cut, cut + 1):
        if ci < 0 or ci >= len(RATIOS): continue
        for m in MODELS:
            r_ = fit(ci, m)
            if r_: table[(ci, m)] = r_
    # primary model: smallest leave-one-out RMS error, see choose_primary
    primary = choose_primary(table, cut, Ntab, x2)
    v = table[(cut, primary)]
    rs_ = RATIOS[cut:]
    b_, _, rss_, _ = ols([MODELS[primary](r) for r in rs_], [Ntab[(x2, r)][2] for r in rs_])
    resid_rms = math.sqrt(rss_ / len(rs_))
    vals_cut = [table[(ci, primary)][0] for ci in (cut - 1, cut, cut + 1) if (ci, primary) in table]
    vals_models = [table[(cut, m)][0] for m in MODELS if (cut, m) in table and table[(cut, m)][2] >= 1]
    spread_cut = max(vals_cut) - min(vals_cut)
    spread_mod = max(vals_models) - min(vals_models) if len(vals_models) > 1 else 0.0
    unc = math.sqrt(v[1] ** 2 + spread_cut ** 2 + spread_mod ** 2) if not math.isnan(v[1]) else math.sqrt(spread_cut ** 2 + spread_mod ** 2)
    info.update({
        "value": v[0], "uncertainty": unc, "ratio_cutoff": RATIOS[cut],
        "method": f"least squares of N(r)=V/(x^(1/2) f(y)^(3/2)) at x={x2} (interpolated to the nominal ratio) on rows r>={RATIOS[cut]}, model N=N0+... with basis [{primary}]; N0 is the r->0 limit. "
                  f"uncertainty = quadrature sum of the OLS s.e. ({v[1]:.2e}), the spread over cutoff-1/+1 grid step ({spread_cut:.2e}) and over the 4 model forms ({spread_mod:.2e})",
        "cutoff_sensitivity": ("primary model [%s]: N0 at cutoff %s = %s; " % (primary, ", ".join(str(RATIOS[ci]) for ci in (cut - 1, cut, cut + 1) if (ci, primary) in table),
                               ", ".join("%.4f" % table[(ci, primary)][0] for ci in (cut - 1, cut, cut + 1) if (ci, primary) in table))
                               + "spread over cutoffs %.4f; spread over the 4 model forms at the chosen cutoff %.4f (cutoff cannot move lower if it is already the smallest grid ratio)" % (spread_cut, spread_mod)),
        "cutoff_sensitivity_detail": {"N0_by_cutoff_and_model": {str(RATIOS[ci]): {m: table[(ci, m)][0] for m in MODELS if (ci, m) in table}
                                           for ci in (cut - 1, cut, cut + 1) if 0 <= ci < len(RATIOS)},
                               "ols_se": {f"{RATIOS[ci]}|{m}": table[(ci, m)][1] for (ci, m) in table},
                               "spread_over_cutoffs_primary_model": spread_cut, "spread_over_models_at_cutoff": spread_mod},
        "primary_model": primary, "fit_residual_rms": resid_rms, "n_rows_fitted": len(rs_)})
    return info

def choose_primary(table, cut, Ntab=None, x2=None):
    """Model with the smallest leave-one-out RMS error among models that leave >=1 dof; ties -> fewer parameters."""
    rs = RATIOS[cut:]
    best, bestv = None, None
    for m in MODELS:
        p = len(MODELS[m](1.0))
        if len(rs) - 1 < p + 0: continue
        err = 0.0
        for i in range(len(rs)):
            rr = rs[:i] + rs[i + 1:]
            b, _, _, _ = ols([MODELS[m](r) for r in rr], [Ntab[(x2, r)][2] for r in rr])
            err += (sum(c * v for c, v in zip(b, MODELS[m](rs[i]))) - Ntab[(x2, rs[i])][2]) ** 2
        err = math.sqrt(err / len(rs))
        if bestv is None or err < bestv - 1e-12: best, bestv = m, err
    return best

def main():
    fresh = "--fresh" in sys.argv
    if not os.path.exists(os.path.join(HERE, "sqf")):
        subprocess.run(["clang", "-O2", "-o", os.path.join(HERE, "sqf"), os.path.join(HERE, "sqf.c"), "-lm"], check=True)
    t0 = time.time()
    raw = collect(fresh)
    polys = analyse(raw)
    validation = json.load(open(os.path.join(HERE, "validation.json"))) if os.path.exists(os.path.join(HERE, "validation.json")) else []
    notes = open(os.path.join(HERE, "notes.txt")).read() if os.path.exists(os.path.join(HERE, "notes.txt")) else ""
    json.dump({"polynomials": polys, "validation": validation, "notes": notes}, open(os.path.join(HERE, "results.json"), "w"), indent=1)
    print(f"done in {time.time()-t0:.1f}s")

if __name__ == "__main__":
    main()
