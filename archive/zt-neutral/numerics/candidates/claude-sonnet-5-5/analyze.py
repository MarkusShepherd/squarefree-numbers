"""Analysis of the exact V_f(x,y) values in raw/ -> results.json, details.json."""
import json
import os
import numpy as np
from decimal import Decimal

from sqf import POLYS, finv_floor

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
RATIOS = [0.01, 0.02, 0.05, 0.1, 0.2, 0.4, 0.7, 1.0]
STAB = 0.01          # stability threshold between the two largest x
XFIT_MIN = 1_000_000  # x range used for the fixed-ratio / joint exponent fits


def ols(X, y):
    """returns beta, se (se=nan if no dof)."""
    X = np.asarray(X, float)
    y = np.asarray(y, float)
    n, p = X.shape
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    if n > p:
        r = y - X @ beta
        s2 = r @ r / (n - p)
        se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    else:
        se = np.full(p, np.nan)
    return beta, se


def load(name, x):
    r = json.load(open(os.path.join(RAW, f"{name}_{x}.json")))
    return np.array(r["ks"]), np.array(r["fk"], float), [Decimal(v) for v in r["V"]]


def norm_at_nominal(name, x, fk, V, r):
    """N = V/(x^1/2 f^3/2) at f = r x: linear interpolation in log f along the dense curve
    (k^2+1, k^3+2); for 2k+1 the checkpoint at f(y) <= r x (|f(y)/x - r| < 3e-5)."""
    N = np.array([float(v) for v in V]) / (x ** 0.5 * fk ** 1.5)
    t = r * x
    if name == "2k+1":
        i = int(np.argmin(abs(fk - t)))
        return N[i]
    j = int(np.searchsorted(fk, t, side="right")) - 1
    j = min(max(j, 0), len(fk) - 2)
    w = (np.log(t) - np.log(fk[j])) / (np.log(fk[j + 1]) - np.log(fk[j]))
    return N[j] * (1 - w) + N[j + 1] * w


DESIGNS = {
    "poly1": lambda r: np.column_stack([np.ones_like(r), r]),
    "poly2": lambda r: np.column_stack([np.ones_like(r), r, r ** 2]),
    "poly3": lambda r: np.column_stack([np.ones_like(r), r, r ** 2, r ** 3]),
    "sqrt2": lambda r: np.column_stack([np.ones_like(r), np.sqrt(r)]),
    "sqrt3": lambda r: np.column_stack([np.ones_like(r), np.sqrt(r), r]),
}


def fit_models(rs, Ns):
    """intercept (=value at r=0), OLS se and leave-one-out rms for each model that has >=2 dof-spare points."""
    rs = np.asarray(rs, float)
    Ns = np.asarray(Ns, float)
    out = {}
    for m, d in DESIGNS.items():
        X = d(rs)
        if len(rs) < X.shape[1] + 1:
            continue
        b, se = ols(X, Ns)
        loo = []
        for i in range(len(rs)):
            keep = np.arange(len(rs)) != i
            bb, _ = ols(X[keep], Ns[keep])
            loo.append(Ns[i] - X[i] @ bb)
        out[m] = {"value": float(b[0]), "se": float(se[0]), "loo_rms": float(np.sqrt(np.mean(np.square(loo)))),
                  "rms": float(np.sqrt(np.mean((Ns - X @ b) ** 2)))}
    return out


def best_model(fm):
    return min(fm, key=lambda m: fm[m]["loo_rms"])


def analyse_poly(name, xs):
    f, fp = POLYS[name]
    xs = [x for x in xs if os.path.exists(os.path.join(RAW, f"{name}_{x}.json"))]
    data = {x: load(name, x) for x in xs}
    rows, normalised = [], []
    Vnom = {}   # (x, r) -> V at the nominal ratio (log-log interpolated), for fixed-ratio fits
    Nnom = {}
    for x in xs:
        ks, fk, V = data[x]
        for r in RATIOS:
            y = finv_floor(name, r * x)
            i = int(np.where(ks == y)[0][0])
            fy = int(fk[i])
            Vy = V[i]
            rows.append({"x": x, "ratio": r, "y": int(y), "fy": fy, "V": float(Vy), "V_exact": str(Vy)})
            Na = float(Vy) / (x ** 0.5 * fy ** 1.5)
            Nn = norm_at_nominal(name, x, fk, V, r)
            Nnom[(x, r)] = Nn
            Vnom[(x, r)] = Nn * x ** 0.5 * (r * x) ** 1.5
            normalised.append({"x": x, "ratio": r, "V_over_x12_fy32": Nn,
                               "ratio_actual": fy / x, "V_over_x12_fy32_actual": Na})
    xbig, xprev = xs[-1], xs[-2]

    # ---- stability test between the two largest x
    drift = {r: Nnom[(xbig, r)] / Nnom[(xprev, r)] - 1 for r in RATIOS}
    cutoff_idx = None
    for i in range(len(RATIOS) - 1, -1, -1):
        if abs(drift[RATIOS[i]]) < STAB:
            cutoff_idx = i
        else:
            break
    # ---- fit 1: fixed x, varying y
    fits_fixed_x = {}
    for x in xs:
        rr = [q for q in rows if q["x"] == x]
        X = np.column_stack([np.ones(len(rr)), np.log([q["fy"] for q in rr])])
        b, se = ols(X, np.log([q["V"] for q in rr]))
        fits_fixed_x[x] = {"beta": float(b[1]), "beta_se": float(se[1]), "ln_prefactor": float(b[0])}
    # same, restricted to rows above the cutoff (largest x)
    if cutoff_idx is not None:
        rr = [q for q in rows if q["x"] == xbig and q["ratio"] >= RATIOS[cutoff_idx]]
        X = np.column_stack([np.ones(len(rr)), np.log([q["fy"] for q in rr])])
        b, se = ols(X, np.log([q["V"] for q in rr]))
        fixed_x_cut = {"beta": float(b[1]), "beta_se": float(se[1])}
    else:
        fixed_x_cut = None

    # ---- fit 2: fixed ratio, varying x (ratio fixed effects), x >= XFIT_MIN, ratios >= cutoff (all if none)
    rs_use = RATIOS[cutoff_idx:] if cutoff_idx is not None else RATIOS
    xs_fit = [x for x in xs if x >= XFIT_MIN]
    Xm, yv = [], []
    for ir, r in enumerate(rs_use):
        for x in xs_fit:
            row = [1.0 if j == ir else 0.0 for j in range(len(rs_use))] + [np.log(x)]
            Xm.append(row)
            yv.append(np.log(Vnom[(x, r)]))
    b, se = ols(Xm, yv)
    fixed_ratio = {"alpha_plus_beta": float(b[-1]), "se": float(se[-1])}
    per_ratio = {}
    for r in RATIOS:
        xx = np.log(xs_fit)
        yy = np.log([Vnom[(x, r)] for x in xs_fit])
        bb, ss = ols(np.column_stack([np.ones(len(xx)), xx]), yy)
        per_ratio[r] = [float(bb[1]), float(ss[1])]
    # joint fit V = C x^alpha f^beta (all x >= XFIT_MIN, ratios >= cutoff)
    Xj, yj = [], []
    for r in rs_use:
        for x in xs_fit:
            Xj.append([1.0, np.log(x), np.log(r * x)])
            yj.append(np.log(Vnom[(x, r)]))
    bj, sj = ols(Xj, yj)
    joint = {"C": float(np.exp(bj[0])), "ln_C": float(bj[0]), "ln_C_se": float(sj[0]),
             "alpha": float(bj[1]), "alpha_se": float(sj[1]),
             "beta": float(bj[2]), "beta_se": float(sj[2]),
             "note": "free-exponent fit over x>=1e6 and ratios>=cutoff; alpha,beta strongly anti-correlated, C is not the asymptotic constant"}

    # ---- extrapolation of N(x_big, r) to r -> 0
    const = None
    detail_extrap = {}
    if cutoff_idx is not None and len(RATIOS) - cutoff_idx >= 4:
        def models_at(ci, x):
            rs = RATIOS[ci:]
            return fit_models(rs, [Nnom[(x, r)] for r in rs])
        fm = models_at(cutoff_idx, xbig)
        mbest = best_model(fm)
        v0, se0 = fm[mbest]["value"], fm[mbest]["se"]
        variants = {}
        for lab, ci in (("cutoff-1", cutoff_idx - 1), ("cutoff+1", cutoff_idx + 1)):
            if 0 <= ci and len(RATIOS) - ci >= 4:
                f2 = models_at(ci, xbig)
                if mbest in f2:
                    variants[lab] = f2[mbest]["value"]
        v_prev = models_at(cutoff_idx, xprev)[mbest]["value"]
        spread_cut = max([abs(v - v0) for v in variants.values()] + [0.0])
        close = [m for m in fm if fm[m]["loo_rms"] <= 2 * fm[mbest]["loo_rms"]]
        spread_model = max(abs(fm[m]["value"] - v0) for m in close)
        xdrift = abs(v0 - v_prev)
        unc = float(np.sqrt(np.nan_to_num(se0) ** 2 + spread_cut ** 2 + spread_model ** 2 + xdrift ** 2))
        # supplementary: same models on ~40 log-spaced ratios in [cutoff,1] (interpolated curve), x_big
        supp = {}
        rd = np.geomspace(RATIOS[cutoff_idx], 1.0, 40)
        for xx in (xprev, xbig):
            ks_, fk_, V_ = data[xx]
            Nd = [norm_at_nominal(name, xx, fk_, V_, r) for r in rd]
            fd = fit_models(rd, Nd)
            supp[str(xx)] = {m: fd[m] for m in fd}
        const = {
            "value": v0, "uncertainty": unc,
            "method": (f"model for N(x,r)=V/(x^(1/2) f(y)^(3/2)) chosen by leave-one-out among a+b r, a+b r+c r^2, cubic, "
                       f"a+b sqrt(r), a+b sqrt(r)+c r, fitted by least squares to the grid rows r>={RATIOS[cutoff_idx]} at "
                       f"x={xbig}; selected '{mbest}'; constant = intercept at r=0. Uncertainty = quadrature sum of OLS intercept se "
                       f"({se0:.2e}), max shift when the cutoff moves one grid step ({spread_cut:.2e}), max spread over models whose "
                       f"LOO rms <= 2x best ({spread_model:.2e}, models {close}), and shift of the extrapolated constant between "
                       f"x={xprev} and x={xbig} ({xdrift:.2e})."),
            "ratio_cutoff": RATIOS[cutoff_idx],
            "cutoff_sensitivity": {**{k: float(v) for k, v in variants.items()}, "x_prev_constant": float(v_prev),
                                   "fit_intercept_se": se0, "selected_model": mbest,
                                   "all_models_x_big": fm,
                                   "spread_cutoff": float(spread_cut), "spread_model": float(spread_model),
                                   "x_drift": float(xdrift)},
        }
        detail_extrap = {**const["cutoff_sensitivity"], "supplementary_dense_fits": supp}
    stab_table = {str(r): drift[r] for r in RATIOS}
    entry = {
        "rows": rows,
        "fit_fixed_x": {"beta": fits_fixed_x[xbig]["beta"], "beta_se": fits_fixed_x[xbig]["beta_se"],
                        "x": xbig, "ln_prefactor": fits_fixed_x[xbig]["ln_prefactor"]},
        "fit_fixed_ratio": {**fixed_ratio, "x_range": [xs_fit[0], xs_fit[-1]], "ratios_used": rs_use},
        "normalised": normalised,
        "constant_extrapolated": const if const is not None else
        {"value": None, "uncertainty": None, "method": "no ratio passes the stability test (<1% change between the two largest x)",
         "ratio_cutoff": None, "cutoff_sensitivity": None},
    }
    det = {"fit_fixed_x_all_x": {str(k): v for k, v in fits_fixed_x.items()},
           "fit_fixed_x_ratio_ge_cutoff_largest_x": fixed_x_cut,
           "fit_fixed_ratio_per_ratio_slope_se": {str(k): v for k, v in per_ratio.items()},
           "joint_fit": joint, "stability_rel_change_xprev_to_xbig": stab_table,
           "xprev": xprev, "xbig": xbig, "extrapolation": detail_extrap}
    return entry, det


def main(xs, validation):
    results = {"polynomials": {}, "validation": validation, "notes": ""}
    details = {}
    for name in POLYS:
        entry, det = analyse_poly(name, xs)
        results["polynomials"][name] = entry
        details[name] = det
    results["notes"] = make_notes(results, details)
    json.dump(results, open(os.path.join(HERE, "results.json"), "w"), indent=1)
    json.dump(details, open(os.path.join(HERE, "details.json"), "w"), indent=1)
    # human-readable summary
    for name in POLYS:
        e = results["polynomials"][name]
        print(f"== {name}")
        print("  fit_fixed_x:", e["fit_fixed_x"])
        print("  fit_fixed_ratio:", e["fit_fixed_ratio"])
        print("  constant:", {k: e["constant_extrapolated"][k] for k in ("value", "uncertainty", "ratio_cutoff")})
        cs = e["constant_extrapolated"]["cutoff_sensitivity"]
        print("  sensitivity:", {k: v for k, v in cs.items() if k != "all_models_x_big"})
        print("  models:", {m: (round(v["value"], 4), round(v["loo_rms"], 4)) for m, v in cs["all_models_x_big"].items()})
        sp = details[name]["extrapolation"]["supplementary_dense_fits"][str(details[name]["xbig"])]
        print("  dense fits:", {m: (round(v["value"], 4), round(v["loo_rms"], 4)) for m, v in sp.items()})
        print("  stability:", {k: round(v, 5) for k, v in details[name]["stability_rel_change_xprev_to_xbig"].items()})


def make_notes(results, details):
    parts = []
    parts.append("All V values are exact: sum_l Q^2 is an exact integer (FFT autocorrelation of the squarefree indicator, "
                 "rounding residual < 4e-8, spot-checked against integer dot products); g-parts are exact rationals times "
                 "6/pi^2, evaluated to 50 digits. 'V' in rows is the float of the 50-digit 'V_exact'. "
                 "Normalised values at nominal ratio r are log-f-interpolated along the full curve in k (k^2+1, k^3+2: step "
                 "in f(y) is not small for small y, so the actual ratio fy/x differs from nominal); 'ratio_actual' and "
                 "'V_over_x12_fy32_actual' give the raw ratio at the grid y. For 2k+1 nominal and actual ratios agree to <3e-5.")
    for name in POLYS:
        c = results["polynomials"][name]["constant_extrapolated"]
        d = details[name]
        if c["value"] is None:
            parts.append(f"{name}: no ratio passes the 1% stability test; no constant reported.")
        else:
            parts.append(f"{name}: cutoff r>={c['ratio_cutoff']}, constant {c['value']:.5f} +- {c['uncertainty']:.5f}; "
                         f"rel. change of N between x={d['xprev']} and x={d['xbig']} by ratio: "
                         + ", ".join(f"{k}:{v*100:+.2f}%" for k, v in d["stability_rel_change_xprev_to_xbig"].items()) + ".")
    parts.append(
        "N(r)=V/(x^(1/2) f(y)^(3/2)) is NOT constant in r: it rises with r from ~0.14 (r=0.01) to 0.167-0.184 (r=1). "
        "Stability in x at fixed r (grid rows, two largest x): 2k+1 changes by <=0.01% at every ratio (x-independent to 4 digits "
        "for x>=3e6); k^2+1 by <=0.1%; k^3+2 by -0.2%..-0.4% at r>=0.05 (-0.57% at r=0.02, -1.6% at r=0.01) per factor 3.16 in x, "
        "i.e. the k^3+2 values still drift downward with x (so its constant is probably slightly overestimated; only ~100-465 moduli). "
        "Small ratios are NOT the most informative: lower-order terms depend on the absolute size of f(y) as well. E.g. for 2k+1 "
        "N = 0.0993 (f=1e2), 0.137 (f=1e3), 0.1426 (f=1e4) at x=1e7, and 0.1357 (f=1e3), 0.1422 (f=1e4), 0.1430 (f=1e5) at x=1e8, "
        "so N depends on f at small f, not on r. "
        "For 2k+1, N(r) also has non-smooth wiggles of size ~0.002-0.003 (dense checkpoints in raw/2k+1_*.json: a dip near r~0.25-0.35, "
        "a maximum 0.1871 near r~0.85) that no low-order polynomial in r or sqrt(r) captures. "
        "EXTRAPOLATION IS MODEL DEPENDENT: polynomial-in-r models give 0.1408-0.1454 (k^2+1), 0.142-0.146 (k^3+2), 0.147-0.149 (2k+1) "
        "while models containing sqrt(r) (preferred by leave-one-out cross-validation for all three f) give 0.135-0.139, 0.139-0.140, "
        "0.141-0.144. The reported 'uncertainty' includes this model spread, hence it is large (0.004-0.008); the OLS intercept "
        "errors alone are only ~0.001-0.002. A sqrt(r) leading correction (relative size ~ (Y/x)^(1/2)) is suggested by the data "
        "but not proven. "
        "SUPPLEMENTARY direct readings at the largest x=1e8, outside the stability-tested fit (use as a cross-check only): "
        "k^2+1: N is ~0.1395 (range 0.1390-0.1403, 217 values of k) for 1e4<=f(y)<1e5, i.e. r<=1e-3, and 0.1405 for 1e5<=f<1e6, "
        "i.e. N flattens at ~0.1395 as r->0 (and is lower, 0.129 mean, for f<1e3 where the f-dependent corrections dominate); "
        "2k+1: N ~ 0.1422-0.1430 for 1e-4<=r<=1e-3; "
        "k^3+2: N ~ 0.141 mean (0.1394-0.1438) for 1e5<=f<1e6, still drifting down with x. "
        "Exponent fits: at fixed x, d ln V/d ln f(y) is 1.53-1.55 over the whole grid (not 1.5) because N(r) rises with r; "
        "the fixed-ratio exponent alpha+beta is 2.000 (2k+1), 1.9993 (k^2+1), 1.994 (k^3+2); its quoted OLS se does not include the "
        "systematic x-drift (k^3+2 drift is the reason for 1.994). "
        "The single-modulus sum_l E^2 includes q > x moduli only in the interpolation tail (k with f(k)>x) used for log-f interpolation of N; "
        "rows with f(y)<=x never use them except at ratio 1.0 where the nominal value is interpolated.")
    return " ".join(parts)
