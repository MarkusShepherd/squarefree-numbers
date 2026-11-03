# Exact numerics for the sparse squarefree variance V_f(x,y)

Computes `V_f(x,y) = sum_{k<=y} f'(k) sum_{l<=f(k)} E(x;f(k),l)^2` for f = k^2+1, k^3+2, 2k+1,
x in {1e5, 316228, 1e6, 3162278, 1e7, 31622777, 1e8}, at f(y)/x in {0.01,...,1}.

## Rerun
    python3 compute.py                 # validation + exact computation (cached in raw/) + analysis -> results.json, details.json
    python3 compute.py --skip-validate # reuse validation.json
Needs numpy, scipy, mpmath, sympy (validation only). Uses 11 forked worker processes.
Runtime on a 12-core, 32 GB Mac: validation ~40 s; exact computation of all x/all f ~2.5 min
(x=1e8 dominates: FFT ~5 s, k^2+1/k^3+2 ~2 s, 2k+1 ~55 s for 5e7 moduli); analysis ~2 s. Peak memory ~6 GB at x=1e8.
`raw/` is a cache; delete it to recompute from scratch.

## Files
- `sqf.py` – core algorithm and formulas (docstring has the derivation). `validate.py` – checks. `compute.py` – entry point/driver.
  `analyze.py` – fits and extrapolation. `results.json` – required output. `details.json` – extra diagnostics
  (per-x exponent fits, per-ratio slopes, joint free-exponent fit, stability table, all extrapolation models, dense fits).
  `raw/<f>_<x>.json` – exact cumulative V (50-digit strings) at every k (k^2+1, k^3+2) or at the checkpoints (2k+1; the 8 grid ratios plus ~90 extra diagnostics ratios).

## Algorithm
sum_l Q(x;q,l)^2 = #{(m,n) squarefree <= x: m = n mod q} = C(0) + 2 sum_{j>=1} C(jq), with C(h) the autocorrelation of the
squarefree indicator. One FFT gives C(h) for all h <= x (rounded to exact integers; max rounding residual 3e-8 at x=1e8;
spot-checked against exact integer dot products), after which each modulus costs O(x/q).
The g-dependent parts sum_l g Q and sum_l g^2 have closed forms (see `sqf.py`); g(q,l) = (6/pi^2)/q * prod_{p|q} u_p(l),
u_p = p^2/(p^2-1) generically, p/(p+1) if p||q and p|l, 0 if p^2|q and p^2|l. They are evaluated as exact rationals
with 50-digit Decimal arithmetic. So V is exact up to ~1e-40 relative error (the printed float is the rounding of the 50-digit value).

## Validation (see `validation.json`, also embedded in results.json)
g vs Moebius series and brute-force densities (q<=50); sum_l g = 6/pi^2 and sum_l g^2 closed form exactly (rational);
sum_l Q = Q(x;1,1); fast sum_l E^2 vs brute-force bincount for x=3000, 2<=q<600 (rel dev 2e-44);
FFT autocorrelation vs dot products; whole V_f(5000,y_max) for all three f vs brute force (rel dev <1e-47).
`numerics/results.json` mentioned in problem.md was not present in this working directory, so no comparison with it was made.

## Caveats (also in `notes` in results.json)
- The normalised value N=V/(x^(1/2) f^(3/2)) depends on r=f(y)/x (0.14 -> 0.17-0.18), so there is no pure power law; fitted beta at fixed x is 1.53-1.55.
- Extrapolation r->0 is model dependent at the ~0.005 level (polynomial in r vs sqrt(r) models); the reported uncertainties include that.
  k^2+1 and 2k+1 are stable in x at fixed r; k^3+2 still drifts down by ~0.3% per factor 3.16 in x.
- For k^2+1 and k^3+2 the nominal-ratio values are log-f interpolations of the exact curve (f(y) jumps are not small for small y);
  `ratio_actual`/`V_over_x12_fy32_actual` give the raw values at the grid y. Rows (`y`, `fy`, `V`) are always exact.
- Stability cutoff used: |N(x=1e8,r)/N(x=3162278... [31622777],r) - 1| < 1% for all grid ratios >= cutoff.

## Sources
No external literature was used or consulted (everything derived directly; no papers/ folder existed in the working directory).
Nothing by the excluded author or the excluded paper was searched, opened or used.
