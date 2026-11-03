"""Independent, local-only checks for assembly.md; run with python3."""
import json
import math

import mpmath as mp
import numpy as np
from sympy import factorint


mp.mp.dps = 60
LIMIT = 10_000_000
CHECKPOINTS = (1_000, 10_000, 100_000, 1_000_000, LIMIT)
NAMES = ("k^2+1", "k^3+2")


def primes_to(n):
    sieve = np.ones(n + 1, dtype=bool)
    sieve[:2] = False
    for p in range(2, math.isqrt(n) + 1):
        if sieve[p]:
            sieve[p * p::p] = False
    return np.flatnonzero(sieve)


def root_counts(name, p):
    if name == "k^2+1":
        return (1, 0) if p == 2 else ((2, 2) if p % 4 == 1 else (0, 0))
    if p in (2, 3):
        return 1, 0
    r = 1 if p % 3 == 2 else (3 if pow(p - 2, (p - 1) // 3, p) == 1 else 0)
    return r, r


def compute_constants(primes):
    out = {}
    prefactor = float(mp.mpf(2) / 3 * (-4 * mp.zeta(-mp.mpf(1) / 2)))
    for name in NAMES:
        # Check exceptional primes and the residue criteria independently.
        for p0 in primes[primes <= 100]:
            p = int(p0)
            power, shift = (2, 1) if name == "k^2+1" else (3, 2)
            brute = tuple(sum((pow(a, power, mod) + shift) % mod == 0
                              for a in range(mod)) for mod in (p, p * p))
            assert brute == root_counts(name, p), (name, p, brute)
        logs = []
        for p0 in primes:
            p = int(p0)
            r1, r2 = root_counts(name, p)
            t = 1.0 / p
            A = 1 - 3 * t**2 + 2 * t**3
            # Differences avoid cancellation of the leading constant.
            BA = -t + t**2 + t**1.5 - t**2.5
            DB = (1 - t) * (t**2 - t**1.5)
            tau_minus_one = (-3 * t**2 + 2 * t**3
                             + BA * r1 * t + DB * r2 * t**2)
            assert A > 0 and 1 + tau_minus_one > 0
            logs.append(math.log1p(tau_minus_one))
        logs = np.asarray(logs)
        partials = {str(n): prefactor * math.exp(math.fsum(
            logs[:np.searchsorted(primes, n, side="right")])) for n in CHECKPOINTS}
        d = 2 if name == "k^2+1" else 3
        # P8: |tau_p-1| <= (3+2d)/p^2. For p>LIMIT, tau_p<1
        # and -log(tau_p) <= |tau_p-1|/(1-(3+2d)/LIMIT^2).
        # All tail primes are coprime to 30. In each of its eight reduced
        # residue classes, a decreasing-integral bound gives at most
        # LIMIT^-2 + (30*LIMIT)^-1 for the sum of reciprocal squares.
        K = 3 + 2 * d
        prime_tail_bound = 8 * (1 / LIMIT**2 + 1 / (30 * LIMIT))
        tail_log_bound = K * prime_tail_bound / (1 - K / LIMIT**2)
        C = partials[str(LIMIT)]
        out[name] = {"partial_products": partials,
                     "constant_interval": [C * math.exp(-tail_log_bound), C],
                     "prime_cutoff": LIMIT, "tail_log_bound": tail_log_bound}
    return out


def check_fits_and_rows(data, constants):
    out = {}
    for name in NAMES:
        p = data["polynomials"][name]
        c = p["constant_extrapolated"]
        fit = c["primary_fit"]
        rows = [r for r in p["rows"] if r["x"] == fit["x"]
                and r["ratio_target"] >= c["ratio_cutoff"]
                and r["ratio_target"] <= fit["upper_ratio"]]
        r = np.array([row["ratio_actual"] for row in rows])
        v = np.array([row["normalised"] for row in rows])
        M = np.column_stack((np.ones(len(r)), np.sqrt(r), r))
        coefficients = np.linalg.lstsq(M, v, rcond=None)[0]
        residual = v - M @ coefficients
        variance = np.dot(residual, residual) / (len(r) - 3)
        se = math.sqrt(variance * np.linalg.inv(M.T @ M)[0, 0])
        assert np.max(np.abs(coefficients - fit["coefficients"])) < 1e-12
        assert abs(se - fit["intercept_se"]) < 1e-12
        C = constants[name]["partial_products"][str(LIMIT)]
        relative_interval = [(a / c["value"] - 1)
                             for a in constants[name]["constant_interval"]]
        out[name] = {"extrapolated": c["value"], "heuristic_uncertainty": c["uncertainty"],
                     "relative_discrepancy_predicted_minus_observed_over_observed":
                         C / c["value"] - 1,
                     "relative_discrepancy_interval": relative_interval,
                     "absolute_discrepancy_over_heuristic_uncertainty":
                         abs(C - c["value"]) / c["uncertainty"],
                     "recomputed_fit_coefficients": coefficients.tolist(),
                     "recomputed_intercept_se": se,
                     "max_normalisation_relative_error": max(
                         abs(row["V"] / (math.sqrt(row["x"]) * row["fy"]**1.5)
                             / row["normalised"] - 1) for row in p["rows"])}
    return out


def direct_count_check(data, primes):
    x = min(row["x"] for name in NAMES for row in data["polynomials"][name]["rows"])
    sf = np.ones(x + 1, dtype=bool)
    sf[0] = False
    for p0 in primes[primes <= math.isqrt(x)]:
        p = int(p0)
        sf[p * p::p * p] = False
    integers = np.flatnonzero(sf)
    c = np.longdouble(str(6 / mp.pi**2))
    out = {}
    for name in NAMES:
        rows = [r for r in data["polynomials"][name]["rows"] if r["x"] == x]
        cumulative_V = np.longdouble(0)
        cumulative_Q2 = 0
        comparisons = []
        by_y = {r["y"]: r for r in rows}
        for k in range(1, max(by_y) + 1):
            q, weight = (k * k + 1, 2 * k) if name == "k^2+1" else (k**3 + 2, 3 * k * k)
            counts = np.bincount(integers % q, minlength=q)
            g = np.full(q, c / q, dtype=np.longdouble)
            for p0, a in factorint(q).items():
                p = int(p0)
                g /= (1 - np.longdouble(1) / (p * p))
                if a == 1:
                    g[::p] *= (1 - np.longdouble(1) / p)
                else:
                    g[::p * p] = 0
            error = counts.astype(np.longdouble) - x * g
            cumulative_V += weight * np.sum(error * error)
            cumulative_Q2 += weight * int(np.dot(counts, counts))
            if k in by_y:
                row = by_y[k]
                assert cumulative_Q2 == row["sum_Q_squared_weighted"]
                exact_V = np.longdouble(row["V_decimal"])
                rel = float(cumulative_V / exact_V - 1)
                assert abs(rel) < 1e-12
                comparisons.append({"y": k, "fy": q, "V_recomputed": str(cumulative_V),
                                    "relative_difference": rel,
                                    "weighted_Q_squared_exact_match": True})
        out[name] = {"x": x, "rows_checked": len(comparisons), "comparisons": comparisons}
    return out


if __name__ == "__main__":
    data = json.load(open("results.json"))
    primes = primes_to(LIMIT)
    constants = compute_constants(primes)
    result = {"I": str(-4 * mp.zeta(-mp.mpf(1) / 2)), "constants": constants,
              "comparison_and_extrapolation_audit": check_fits_and_rows(data, constants),
              "independent_direct_variance_counts": direct_count_check(data, primes)}
    with open("numerics_audit.json", "w") as fh:
        json.dump(result, fh, indent=2)
        fh.write("\n")
    print(json.dumps({"constants": constants,
                      "comparison": result["comparison_and_extrapolation_audit"],
                      "direct_count_checks": {k: {"x": v["x"], "rows_checked": v["rows_checked"],
                          "max_relative_difference": max(abs(a["relative_difference"])
                                                         for a in v["comparisons"])}
                                              for k, v in result["independent_direct_variance_counts"].items()}},
                     indent=2))
