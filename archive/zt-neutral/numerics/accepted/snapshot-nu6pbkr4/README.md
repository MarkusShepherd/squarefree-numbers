# Reproducible squarefree-variance computation

Run from this directory:

```sh
python3 compute.py
```

Requires Python 3 with numpy, scipy and mpmath, plus clang++ with C++17 support.
No installation, network access, papers, or external data are used. The script
compiles `counts.cpp`, validates the implementation, runs the calculations,
writes per-size caches `run_<x>.json`, then writes `results.json` and `report.md`.
The C++ executable `counts` is generated and can be deleted.

The default x grid is 250000, 500000, 1000000, 2000000, 4000000, 8000000,
16000000, 32000000, 64000000, 128000000, 256000000. Each polynomial uses all
eight requested target ratios. Integer y is the largest value satisfying
f(y) <= target_ratio*x. One extra ratio 0.005 is computed at the two largest
sizes to check cutoff sensitivity below the smallest requested ratio.

For a smaller run or to reanalyse existing caches:

```sh
python3 compute.py --xs 250000,500000,1000000
python3 compute.py --reuse
```

`--reuse` trusts the per-size JSON caches. Omit it after changing counting code,
precision, or the ratio grid. At least two sizes are required for the fits.
Recorded primary computations total 753.00 seconds; the extra diagnostics
total 176.84 seconds (15.50 minutes combined). The entire task, including
implementation and validation, finished in about 20 minutes. The largest
run uses approximately 4.6 GB of memory. Per-size timings are in
`results.json` and `report.md`.

## Algorithm and stored quantities

Write a(n)=1 if n is squarefree and 0 otherwise, with a(0)=0, and
C(h)=sum_{n=1}^{x-h} a(n)a(n+h). A single integer number-theoretic transform
autocorrelation gives every C(h). The padded length is the smallest power of
two at least 2*x+1. The transform prime is 3221225473 with primitive root 5;
every correlation is at most x, so reduction modulo this prime loses no
information. The worker checks C(0) and seven lag sums directly.

The integer sum of squared progression counts is evaluated as
sum_l Q(x;q,l)^2 = Q(x;1,1) + 2*sum_{m>=1} C(m*q).
All desired moduli reuse the same correlations; the linear control therefore
costs O(x log x) in total rather than O(x) for every modulus. A multiples sieve
also computes S_d = number of squarefree n<=x divisible by d, for squarefree d.

Density evaluation uses g(q,l)=c*h(q,l), where c=6/pi^2 and h is rational:

- h(q,l)=0 if p^2 divides both q and l for any prime p.
- Otherwise h(q,l)=(1/q) product_{p|q} p^2/(p^2-1), multiplied by
  (1-1/p) whenever p divides q exactly once and p divides l.

For each modulus the worker computes exact rational coefficients
B_q=sum_l Q(x;q,l)*h(q,l) and D_q=sum_l h(q,l)^2. For implementation details,
if R is the product of primes dividing q exactly once, use

```
B_q = (1/q) product_{p|q} p^2/(p^2-1)
      * sum_{d|R} mu(d)*S_d/d

D_q = (1/q)
      * product_{p||q} p*(p^2+p-1)/((p-1)*(p+1)^2)
      * product_{p^2|q} p^2/(p^2-1).
```

The worker streams exact unsigned integer numerators and denominators to
Python. Integer intermediates use 64 or 128 bits; the supplied x range fits
these types. The B coefficient cancels product p^2 before multiplication, to
avoid unnecessarily large intermediates. The code is intended for the supplied
range, not arbitrary x; do not extrapolate its integer bounds blindly.

Python accumulates weighted B and D with 70 decimal digits, using an 85-digit
evaluation of c, then evaluates

```
V = sum_Q_squared_weighted - 2*c*x*B + c^2*x^2*D.
```

The counts are exact integers. V itself involves pi and is not a rational or
an exactly represented real number. `V_decimal`, `B_decimal` and `D_decimal`
retain 70-digit numerical evaluations; `V` is also supplied as a conventional
JSON floating-point number. The normalized value uses actual f(y)/x.

## Empirical fits and caveats

Fixed-x log-log fits estimate beta and C*x^alpha. Separate fixed-target-ratio
fits estimate alpha+beta and C*r^beta; integer rounding of y means the ratios
are approximate. The output includes largest-four-x fits and an additional
quantisation adjustment assuming beta=3/2. An unrestricted joint fit supplies
alpha, beta, C, and formal OLS standard errors. These are finite-range fits.

The primary stability cutoff is the smallest ratio in the **requested** grid
such that every row at that ratio or above changes by less than 1% between the
two largest x. An isolated passing low-ratio row cannot bypass an unstable
higher row. The extra 0.005 row is a diagnostic for the lower neighboring
cutoff; it does not redefine the requested primary grid.

Only stable-cutoff rows at the largest x enter the primary extrapolation
N(r)=C+a*sqrt(r)+b*r, using actual ratios. The reported uncertainty is the
maximum of twice the formal intercept SE, the full neighboring-cutoff spread,
the previous-x shift, shifts from sqrt-only and cubic-in-sqrt(r) models, and
shifts when the maximum fitted ratio is reduced to 0.1, 0.2, or 0.4 (provided
there are enough rows to fit with residual degrees of freedom).
It is a heuristic sensitivity envelope, not a confidence interval or an
asymptotic error bound. A lowered-cutoff sensitivity fit can deliberately
include a row failing stability; it is not the primary fit. Too few stable
points, or no stable suffix, produce a null extrapolated constant.

No excluded work, remembered numerical constants, or external sources were
consulted. This is numerical evidence only, with no claimed proofs.
