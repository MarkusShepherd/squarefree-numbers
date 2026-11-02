# Numerics for V_f(x,y) (squarefree numbers in progressions to sparse moduli)

## Rerun
```
python3 compute.py                  # validation + rows + fits -> results.json
python3 compute.py --skip-validate  # reuse validation.json
```
Needs numpy, scipy, mpmath only.  Intermediate exact rows are cached in `cache/*.json`
(delete the directory to recompute from scratch).  Runtime on a 12-core Mac: cold start about
2 min for the rows (k^2+1 and k^3+2 up to x=1e8: seconds each; 2k+1 up to x=1e7: 22 s for the largest x),
about 25 s validation, about 25 s for the diagnostic ratio scans; rerun with cache: a few seconds.
Peak memory is about 4 GB at x=1e8 (FFT of length 2e8).

## Files
- `sqfcore.py` – algorithm (sieve, FFT autocorrelation, closed forms for g, exact rational terms).
- `validate.py` – brute-force validation (output in `validation.json` and `results.json`).
- `rows.py` – exact V_f rows per (f,x) with cache; `scan.py` – fine ratio scan (diagnostic);
  `analyze.py` – fits, stability cutoff, extrapolation; `compute.py` – entry point.

## Algorithm (why it is fast)
With s(n) the squarefree indicator, sum_l Q(x;q,l)^2 = #{(n,m): n≡m mod q} = Q(x) + 2 sum_{j>=1} C(jq),
C(h) = #{n<=x-h : n, n+h squarefree}.  One FFT autocorrelation per x gives all C(h) exactly (integers;
rounding error < 1e-7, checked), then each modulus costs x/q.  Closed form (derived, validated exactly):
g(q,l) = (6/pi^2)/q * prod_{p|q}(1-p^-2)^-1 * prod_{p|q} c_p(l),
c_p = 1 if p∤l; 1-1/p if p|l, p||q; 1 if p||l, p^2|q; 0 if p^2|l, p^2|q.
For squarefree n only the primes with p||q matter, so sum_l g Q = (6/pi^2)(W_q/q) sum_{e|q1} mu(e)/e * #{n<=x sf: e|n};
sum_l g^2 is multiplicative (formula in `sqfcore.py`).  y for ratio rho is the largest k with f(k) <= rho x.

## Results (see `results.json`; all V are exact to >= 9 digits, everything below the line is a fit)
Normalised N = V/(x^{1/2} f(y)^{3/2}) at the two largest x (full tables for all 10 x in results.json):

| f | x | 0.01 | 0.02 | 0.05 | 0.1 | 0.2 | 0.4 | 0.7 | 1.0 |
|---|---|---|---|---|---|---|---|---|---|
| k^2+1 | 5e7 | 0.14105 | 0.14300 | 0.14454 | 0.15107 | 0.15659 | 0.16282 | 0.16996 | 0.17111 |
| k^2+1 | 1e8 | 0.14097 | 0.14299 | 0.14452 | 0.15103 | 0.15657 | 0.16280 | 0.16994 | 0.17111 |
| k^3+2 | 5e7 | 0.14190 | 0.14583 | 0.14613 | 0.14948 | 0.15311 | 0.15627 | 0.16477 | 0.16707 |
| k^3+2 | 1e8 | 0.14221 | 0.14457 | 0.14460 | 0.14954 | 0.15273 | 0.15584 | 0.16412 | 0.16679 |
| 2k+1 | 5e6 | 0.14456 | 0.14835 | 0.14934 | 0.15670 | 0.16171 | 0.16245 | 0.18239 | 0.18369 |
| 2k+1 | 1e7 | 0.14457 | 0.14835 | 0.14933 | 0.15670 | 0.16171 | 0.16245 | 0.18239 | 0.18369 |

| f | cutoff (1% test) | beta (fixed x, largest x) | alpha+beta (fixed ratio) | joint alpha, beta | N(rho->0) |
|---|---|---|---|---|---|
| k^2+1 | 0.01 | 1.545 ± 0.004 | 1.9992 ± 0.0003 | 0.455 ± 0.002, 1.545 ± 0.001 | 0.142 ± 0.007 |
| k^3+2 | 0.1  | 1.549 ± 0.007 | 1.9956 ± 0.0013 | 0.448 ± 0.003, 1.548 ± 0.002 | 0.147 ± 0.004 |
| 2k+1  | 0.01 | 1.551 ± 0.007 | 2.0001 ± 0.0001 | 0.449 ± 0.007, 1.551 ± 0.003 | 0.147 ± 0.006 |

Observations:
- alpha+beta = 2 (fixed ratio) confirmed to 1e-3 or better; the fixed-x slope beta is 1.545-1.551, not 3/2,
  because N depends on the ratio (slope = 3/2 + dlnN/dln rho); the joint fit therefore gives alpha ≈ 0.45,
  and fitting a pure power law is biased by this ratio dependence.  N is the thing to look at.
- N is stable in x at fixed ratio (rel. change between the two largest x: <0.07% for k^2+1, <1.1% k^3+2, <1e-4 for 2k+1)
  but varies with the ratio from ~0.141 (rho=0.01) to ~0.171-0.187 (rho=1) and is **not smooth** in rho
  (oscillations at scale ~0.05; broad hump with maximum at rho≈0.86 for all three f; see `diagnostic_scan`).
  The 8-point grid is therefore too coarse for a precise extrapolation; the quoted uncertainty includes
  cutoff shifts, a sqrt(rho) model variant and the x-drift, and is dominated by the model variant.
  Direct values at the smallest computed ratios (rho = 5e-4..0.01): mean N = 0.1403 (k^2+1), 0.1421 (k^3+2), 0.1439 (2k+1).
- Only k^3+2 fails the 1% test at rho=0.05 (1.06%), hence cutoff 0.1; it still drifts down slowly in x (0.2-0.4%
  per doubling for rho >= 0.7), so its extrapolation is the least reliable.  For k^3+2 there are only 46..464 moduli.
- Extrapolation: N(r)=N0+a r+b r^2, r=f(y)/x, rows with ratio >= cutoff, largest x.

## Caveats
- No `papers/` folder or `numerics/results.json` existed in my working directory, so nothing was read from them;
  no external literature was used at all (g derived by hand and verified exactly).  No excluded author's work consulted.
- float64 is used for the final combination for q > 3000 (max rel. error 3.5e-10 per modulus measured).
- Linear case goes to x=1e7 only (5e6 moduli); polynomial cases to x=1e8.
