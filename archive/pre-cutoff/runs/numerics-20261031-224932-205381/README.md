# Numerics for V_f(x,y), squarefree numbers in AP to polynomial moduli

Files: `sqf.c` (exact counting + double-double combination), `compute.py` (driver, fits, writes `results.json`),
`validate.py` (independent pure-Python checks, writes `validation.json`), `raw_data.json` (cached C output),
`notes.txt` (copied into `results.json["notes"]`), `results.json`.

## Rerun
```
clang -O2 -o sqf sqf.c -lm
python3 validate.py          # ~8 s
python3 compute.py --fresh   # ~2 min wall-clock on one core (k^2+1 at x=1e7 takes ~75 s); omit --fresh to reuse raw_data.json
```
Only the C compiler and the Python 3 standard library are needed (numpy/scipy were not available).
Memory: < 1 GB (FFT for x=5e6, N=2^24).  `./sqf <poly 0|1|2> <x> <direct|fft> <dump 0|1> y1 y2 ...` prints cumulative V at the given y.

## Algorithm
With T(q)=sum_l Q(x;q,l)^2 (integer), u = x*(6/pi^2)*R_q/q, R_q = prod_{p|q} p^2/(p^2-1):

    sum_l E(x;q,l)^2 = T(q) - 2 u M_q/q' + u^2 S_q.

* g(q,l) = (6/pi^2) (R_q/q) prod_{p||q, p|l}(1-1/p) * [no p with p^2 | gcd(q,l)]  (derived by hand; checked, see validation).
* sum_l g Q = (6/pi^2)(R_q/q) * M_q/q' with M_q/q' = sum_{e | q'} mu(e)/e * N(x/e, e), q' = prod_{p||q} p,
  N(X,e) = #{m<=X squarefree, (m,e)=1} computed from the prefix count of squarefree numbers via N(X,e)=sum_j (-1)^j N(X/p^j, e/p).
* sum_l g^2 = (6/pi^2)^2 (R_q/q)^2 S_q, S_q = prod_{p^a||q} s_p, s_p = p^a-p^(a-2) (a>=2), (p-1)(p^2+p-1)/p^2 (a=1).
* T(q): either "direct" (bincount over n<=x, O(x) per modulus; used for k^2+1, k^3+2 where there are <=3162 moduli),
  or "fft": T(q) = Q(x) + 2 sum_{j>=1} C(jq), C(h)=#{n<=x-h: n,n+h squarefree} from one FFT autocorrelation (exact after rounding, deviation <= 2.3e-9), cost O(x log x) for ALL moduli (used for 2k+1 with up to 2.5e6 moduli).
* The cancellation T - 2uM/q' + u^2 S (terms ~x^2/q, result ~x) is done in double-double (~32 digits); constant 6/pi^2 to 32 digits.
* Weights: f'(k)=2k, 3k^2, 2.

## Grid
x in {1,2,5}*10^j, 1e4..1e7 (k^2+1, k^3+2) and 1e4..5e6 (2k+1; FFT memory limit); for each x the 8 ratios 0.01..1.0 with y = nearest integer to f^{-1}(ratio*x), f(y)<=x.
Largest cases: k^2+1 up to y=3162 (x=1e7), k^3+2 up to y=215, 2k+1 up to y=2.5e6 (x=5e6 ratio 1: y=2499999).

## Caveats (important; see also results.json["notes"])
* V/(x^(1/2) f(y)^(3/2)) is stable in x at fixed ratio but depends on the ratio and is NOT smooth in it (features at r=1/2,1/3,1/4,...). The fixed-x exponent beta is therefore 1.53-1.55, not 1.5. alpha+beta=2 at fixed ratio.
* The extrapolated r->0 constant is ~0.14 (all three f) with uncertainty ~0.01, dominated by the choice of fit form. Dense-grid cross-check included in `constant_extrapolated.dense_grid_check`.
* k^3+2 has few moduli (y<=215): N(r) carries 1-2% arithmetic noise and has not stabilised at r<=0.1.
* The `numerics/results.json` mentioned in problem.md was not available; no comparison against it was made.
* No literature was consulted; none of the excluded sources was searched, opened or used.
