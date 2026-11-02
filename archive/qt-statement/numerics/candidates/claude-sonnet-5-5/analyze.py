"""Stage 2: fits, stability cutoff and extrapolation of N = V/(x^{1/2} f(y)^{3/2})."""
import math

import numpy as np

TOL = 0.01          # stability tolerance between the two largest x
XMIN_FIT = 10 ** 6  # smallest x used in the exponent fits

NOTES = (
    "All V values are computed exactly up to final rounding: the counts sum_l Q(x;q,l)^2 are exact integers "
    "(FFT autocorrelation of the squarefree indicator; rounding error < 1e-7 << 0.5, checked against bincount), "
    "g is (6/pi^2)*exact rational; the combination A - 2x sum gQ + x^2 sum g^2 is done in 50-digit mpmath for "
    "q <= 3000 and in float64 for q > 3000 (measured max relative difference to the exact path 3.5e-10 per modulus, "
    "see validation).  rows[].V is therefore correct to >= 9 significant digits (V_str: 25 printed digits, "
    "meaningful to ~10).  Fitted exponents, the extrapolated constants and their uncertainties are NOT exact. "
    "y for a nominal ratio rho is the largest k with f(k) <= rho*x; the normalisation uses the actual f(y). "
    "KEY CAVEAT: the normalised value N(x,rho)=V/(x^{1/2} f(y)^{3/2}) is not a smooth function of rho: "
    "it oscillates with rho (see diagnostic_scan; local maxima/minima at scales ~0.02-0.1 and a "
    "broad hump with maximum near rho~0.85 for 2k+1, for all three f) so a low-order polynomial in rho "
    "describes the 8-point grid only roughly and the extrapolation to rho->0 carries a model uncertainty that "
    "is not captured by the fit SE (for k^2+1 the sqrt(r)-model gives 0.1346 against 0.1419 for the quadratic; the "
    "uncertainty reported includes such variants).  The scan at the smallest ratios actually computed (r=5e-4..0.01) "
    "gives mean N = 0.1403 (k^2+1, x=1e8), 0.1421 (k^3+2, x=1e8), 0.1439 (2k+1, x=1e7), i.e. all three constants "
    "are ~0.14 and lie within the stated uncertainties of the extrapolations.  At fixed rho, N is stable in x to ~1e-4 relative for 2k+1 and k^2+1 "
    "(rho >= 0.05) but for k^3+2 it still drifts down slowly with x (about 0.2-0.4% per doubling of x at "
    "rho >= 0.7 at x=1e8) and y-rounding is coarse (only 46..464 moduli).  For small rho the residual "
    "N(x,rho)-N(infty,rho) does decay with x (e.g. 2k+1, rho=0.01: 0.1418, 0.1436, 0.1442, 0.1444, 0.1444, 0.1446, "
    "0.1446 for x=1e5..1e7), as the task statement anticipates.  The exponent fits are biased by the rho-dependence of N: "
    "at fixed x the slope of ln V against ln f(y) is 3/2 + d ln N/d ln rho, which is slightly above 3/2 over rho in [0.01,1]."
)


def ols(X, y):
    X = np.asarray(X, float)
    y = np.asarray(y, float)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    dof = len(y) - X.shape[1]
    if dof > 0:
        s2 = float(res @ res) / dof
        cov = s2 * np.linalg.inv(X.T @ X)
        se = np.sqrt(np.diag(cov))
    else:
        se = np.full(X.shape[1], float("nan"))
    return beta, se


def N_of(r):
    return r["V"] / (r["x"] ** 0.5 * r["fy"] ** 1.5)


def extrap(pts, model):
    """pts: list of (r_actual, N). Returns N0, se."""
    r = np.array([p[0] for p in pts])
    N = np.array([p[1] for p in pts])
    if model == "quad":
        cols = [np.ones_like(r), r, r ** 2]
    elif model == "sqrt":
        cols = [np.ones_like(r), np.sqrt(r), r]
    else:
        raise ValueError(model)
    if len(pts) < 4:
        cols = cols[:2]
    b, se = ols(np.column_stack(cols), N)
    return float(b[0]), float(se[0])


def analyze(name, rows, scan):
    xs = sorted(set(r["x"] for r in rows))
    ratios = sorted(set(r["ratio_nominal"] for r in rows))
    by = {(r["x"], r["ratio_nominal"]): r for r in rows}
    x1, x2 = xs[-2], xs[-1]

    normalised = []
    for x in xs:
        for rt in ratios:
            r = by[(x, rt)]
            normalised.append({"x": x, "ratio": rt, "ratio_actual": r["fy"] / x,
                               "y": r["y"], "fy": r["fy"], "V_over_x12_fy32": N_of(r)})

    # ---- stability test between the two largest x
    delta = {rt: abs(N_of(by[(x1, rt)]) / N_of(by[(x2, rt)]) - 1) for rt in ratios}
    passing = [rt for rt in ratios if all(delta[s] < TOL for s in ratios if s >= rt)]
    out = {"rows": [{k: r[k] for k in ("x", "y", "fy", "V", "V_str", "ratio_nominal")} for r in rows],
           "normalised": normalised,
           "stability": {"x_pair": [x1, x2], "rel_change": {str(k): v for k, v in delta.items()},
                         "tolerance": TOL}}
    if not passing:
        out["constant_extrapolated"] = {
            "value": None, "uncertainty": None, "method": "no ratio passes the 1% stability test",
            "ratio_cutoff": None, "cutoff_sensitivity": "n/a"}
        i0 = 0
    else:
        i0 = ratios.index(min(passing))
    cutoff = ratios[i0]
    use = [rt for rt in ratios if rt >= cutoff]
    out["stability"]["cutoff"] = cutoff

    # ---- fit at fixed x
    per_x = []
    for x in xs:
        rr = [by[(x, rt)] for rt in use]
        b, se = ols(np.column_stack([np.ones(len(rr)), np.log([r["fy"] for r in rr])]),
                    np.log([r["V"] for r in rr]))
        per_x.append({"x": x, "beta": float(b[1]), "beta_se": float(se[1])})
    out["fit_fixed_x"] = {"beta": per_x[-1]["beta"], "beta_se": per_x[-1]["beta_se"], "x": x2,
                          "rows_used": "ratio >= %g" % cutoff, "per_x": per_x}
    beta_hat = per_x[-1]["beta"]

    # ---- fit at fixed ratio (x >= XMIN_FIT), y-rounding corrected with beta_hat
    xsel = [x for x in xs if x >= XMIN_FIT]
    per_r = []
    for rt in use:
        rr = [by[(x, rt)] for x in xsel]
        yv = [math.log(r["V"]) - beta_hat * math.log(r["fy"] / (rt * r["x"])) for r in rr]
        b, se = ols(np.column_stack([np.ones(len(rr)), np.log([r["x"] for r in rr])]), yv)
        per_r.append({"ratio": rt, "alpha_plus_beta": float(b[1]), "se": float(se[1])})
    s = np.array([p["alpha_plus_beta"] for p in per_r])
    ses = np.array([p["se"] for p in per_r])
    comb_se = math.sqrt(float(np.mean(ses ** 2)) + float(np.var(s, ddof=1)) / len(s)) if len(s) > 1 \
        else float(ses[0])
    out["fit_fixed_ratio"] = {"alpha_plus_beta": float(s.mean()), "se": comb_se,
                              "x_used": "x >= %d" % XMIN_FIT,
                              "se_definition": "sqrt(mean OLS se^2 + var_between_ratios/n)",
                              "per_ratio": per_r}

    # ---- joint fit ln V = lnC + alpha ln x + beta ln f(y)
    rr = [r for r in rows if r["x"] >= XMIN_FIT and r["ratio_nominal"] >= cutoff]
    b, se = ols(np.column_stack([np.ones(len(rr)), np.log([r["x"] for r in rr]),
                                 np.log([r["fy"] for r in rr])]),
                np.log([r["V"] for r in rr]))
    out["fit_joint"] = {"C": float(math.exp(b[0])), "ln_C_se": float(se[0]),
                        "alpha": float(b[1]), "alpha_se": float(se[1]),
                        "beta": float(b[2]), "beta_se": float(se[2]),
                        "rows_used": "x >= %d, ratio >= %g" % (XMIN_FIT, cutoff)}

    # ---- extrapolation to ratio -> 0
    if passing:
        def pts_for(x, c):
            return [(by[(x, rt)]["fy"] / x, N_of(by[(x, rt)])) for rt in ratios if rt >= c]
        base, base_se = extrap(pts_for(x2, cutoff), "quad")
        variants = {}
        if i0 + 1 < len(ratios) - 3:
            variants["cutoff up one step (%g)" % ratios[i0 + 1]] = extrap(pts_for(x2, ratios[i0 + 1]), "quad")[0]
        if i0 + 2 < len(ratios) - 3:
            variants["cutoff up two steps (%g)" % ratios[i0 + 2]] = extrap(pts_for(x2, ratios[i0 + 2]), "quad")[0]
        if i0 - 1 >= 0:
            variants["cutoff down one step (%g)" % ratios[i0 - 1]] = extrap(pts_for(x2, ratios[i0 - 1]), "quad")[0]
        else:
            variants["cutoff down one step"] = "not available (cutoff is the smallest grid ratio)"
        variants["model N0+a*sqrt(r)+b*r"] = extrap(pts_for(x2, cutoff), "sqrt")[0]
        variants["x=%d instead of %d" % (x1, x2)] = extrap(pts_for(x1, cutoff), "quad")[0]
        devs = [abs(v - base) for v in variants.values() if isinstance(v, float)]
        spread = max(devs)
        unc = math.sqrt(base_se ** 2 + spread ** 2)
        out["constant_extrapolated"] = {
            "value": base, "uncertainty": unc,
            "method": "least squares N(r)=N0+a r+b r^2 (r = f(y)/x actual) on the grid rows with ratio >= cutoff at "
                      "x=%d; uncertainty = sqrt(OLS se^2 + (max deviation over variants)^2)" % x2,
            "ols_se": base_se, "ratio_cutoff": cutoff,
            "cutoff_sensitivity": {k: v for k, v in variants.items()},
            "max_variant_deviation": spread}
        small = [o["N"] for o in scan if o["ratio_nominal"] <= 0.01]
        out["constant_extrapolated"]["diagnostic_small_ratio_scan"] = {
            "x": scan[0]["x"], "ratios": "0.0005..0.01 (%d points)" % len(small),
            "mean_N": float(np.mean(small)), "std_N": float(np.std(small, ddof=1)),
            "comment": "not used in the value; shows N(r) at the smallest ratios actually computed"}
    # ---- diagnostic scan (compact)
    out["diagnostic_scan"] = {"x": scan[0]["x"] if scan else None,
                              "points": [[o["fy"] / o["x"], o["N"]] for o in scan]}
    return out
