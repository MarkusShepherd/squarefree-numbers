This directory contains an independent numerical experiment for `problem.md`. No papers, web pages, excluded sources, or external mathematical sources were consulted. There are no proofs here.

Run from this directory:

```sh
python3 compute.py
```

Requirements: a C++17 compiler called `c++`, Python 3, NumPy, SciPy, and mpmath. No installation or network access is used. The entry point compiles `compute_core.cpp`, computes the data, runs independent validation, fits the data, and writes `results.json`. All supporting mathematical source is in these two files. The executable files can be deleted and rebuilt.

The default x grid is 1,000,000; 4,000,000; 16,000,000; 64,000,000; and 256,000,000. Each polynomial has eight rows at each x, for 120 production rows overall. The target ratios are 0.01, 0.02, 0.05, 0.1, 0.2, 0.4, 0.7, 1.0. For each target r, y is the largest integer satisfying f(y) <= floor(r*x). The JSON records both the target and actual ratios. The sum starts at k=1, and the original derivative weights 2k, 3k^2, and 2 are used.

The observed production counting times were approximately 0.37, 1.53, 6.79, 31.11, and 131.35 seconds at the five sizes. Counting took 171 seconds in total; compilation, validation, and fitting take a few additional seconds. The largest run needs approximately 4.2 GiB of array storage. This is the chosen practical memory budget; the default is already 256 times the requested million-point target. The complete interactive investigation finished well within 45 minutes. The transform supports x <= 536,870,911, but such a run would require substantially more memory. Do not use fast-math compiler flags: the double-double arithmetic relies on ordinary IEEE binary64 rounding and explicit `fma`.

To regenerate the fits and repeat independent checks from existing raw CSVs:

```sh
python3 compute.py --reuse
```

To run a smaller experiment:

```sh
python3 compute.py --xs 1000000 4000000
```

The full run also leaves `raw_1000.csv` for direct small-case validation and `validation_other_modulus.csv` for an independent transform-prime check. The largest run's raw CSV has only 24 rows: it stores per-modulus and cumulative aggregates at the requested grid endpoints. All intermediate counts are recomputed on rerunning. Reusing CSVs preserves the original counting runtimes in the JSON; `runtime_seconds_this_invocation` measures the latest invocation only.

The algorithm uses an exact modular autocorrelation of the squarefree indicator a(n), supported on 1 <= n <= x, with a(0)=0. A zero-padded NTT with length N >= 2x+1 computes C(h)=sum_n a(n)a(n+h). The prime is 3*2^30+1 = 3221225473, with primitive root 5. Every coefficient is a nonnegative integer <= x < the prime, so the modular result lifts uniquely. No floating-point convolution or rounding of counts occurs. Only one forward and one inverse transform are needed, multiplying transform entry j by entry -j.

For each needed modulus q, the integer square-count sum is

```
S2(q) = Q(x;1,1) + 2 * sum_{h>=1, h*q<x} C(h*q).
```

These harmonic divisor sums handle all the linear-control moduli without an O(x) scan for each modulus. S_d = #{n<=x: n squarefree and d divides n} is also computed with integer sums over multiples. The counting and divisor stages take O(x log x) work and O(x) space, with constant factors determined mainly by the transform.

The density implementation uses c=6/pi^2 and H(q)=product_{p|q} p^2/(p^2-1). Its coefficient g(q,l)/c is zero if p^2 divides both q and l for some p. Otherwise it is

```
H(q)/q * product_{p||q, p|l} (1-1/p).
```

Write a(q)=product_{p||q} p and T(q)=sum_{d|a(q)} mu(d)*S_d/d. The coefficients aggregated by the code are

```
B(q) = sum_l Q(x;q,l)*g(q,l)/c = H(q)*T(q)/q,
D(q) = sum_l (g(q,l)/c)^2
     = H(q)^2/q * product_{p||q}(1-2/p^2+1/p^3)
                    * product_{p^2|q}(1-1/p^2).
V = A_cum - 2*x*c*B_cum + x^2*c^2*D_cum.
```

The weighted A_cum is an exact uint64 integer. Rational B and D coefficients are evaluated with approximately 31-digit double-double arithmetic implemented in the C++ source. All prime powers in these coefficients are formed in double-double arithmetic, including p^2 and p^3. Final combination with c uses mpmath at 70 digits. CSV high/low components are printed with round-trip binary64 precision and converted back to exact binary floats before mpmath reconstruction. `V_decimal` is conservatively rounded to 20 significant figures. V itself is generally neither an integer nor a rational, and the reported decimal is a high-precision evaluation rather than an exact real-number encoding.

Validation includes:

- Exact finite-period sieves for all 1 <= q <= 50 and every residue, using primes 2, 3 and all primes dividing q. Fraction arithmetic checks every rational local-density coefficient; finite-period Euler products are removed exactly.
- Direct actual squarefree densities at x=1,000,000 for the same moduli. Their maximum absolute discrepancy from the limiting density is about 3.17e-5; this finite discrepancy is not asserted to vanish exactly.
- At x=1000, direct residue counts check every q <= 1000 in C++, and exact Fraction arithmetic independently checks every modulus used by any polynomial, including all odd q <= 999. Per-modulus rational-coefficient discrepancies are below 5e-32 on the stated scale, and cumulative variances agree within 1e-23 relative.
- At every production x, direct counts check sum_l Q=Q(x;1,1) and sum_l Q^2 for every q <= 50. Every transform correlation also passes its integer upper bound, and its zero lag equals the squarefree count.
- At x=256,000,000, the 24 grid-endpoint B(q), D(q) values are checked against independent exact Fraction evaluations, with S_d recomputed by an integer Mobius floor sum. The maximum scaled discrepancy is below 6e-32.
- At x=1,000,000, all 24 endpoint count aggregates are reproduced with prime 469762049 and root 3, agreeing exactly with the production transform.

The fits are unweighted regressions of logarithms. `fit_fixed_x` gives beta at the largest x and individually at every x. `fit_fixed_ratio` gives alpha+beta at every target ratio; its top-level slope is the mean of the eight slopes, and its SE is their sample dispersion divided by sqrt(8). Individual OLS slope SEs are also present. Actual ratios change slightly because y is integral, especially for the cubic. `fit_combined_two_ways` combines these estimates into alpha and C; `fit_joint` separately estimates C, alpha, beta simultaneously from all rows. Fixed-x fits show curvature in the ratio: their beta should not be treated as an unbiased asymptotic exponent.

Extrapolation first compares the two largest x values. The cutoff is the smallest requested grid ratio such that EVERY row at or above it changes by less than 1%. A passing row below a failing row does not permit lowering the cutoff. The central extrapolation fits z(r)=C+a*sqrt(r), where z=V/(sqrt(x)*f(y)^(3/2)), using actual r at the largest x and only rows at or above the cutoff. It also fits C+a*sqrt(r)+b*r and C+a*r to gauge model dependence. The uncertainty is the largest of twice the central intercept SE, the largest adjacent-cutoff shift, either alternative-model shift, and the intercept shift at the second-largest x. This is an empirical sensitivity envelope, not a confidence interval or a rigorous bound. No finite grid identifies an unrestricted r->0 limit.

The lower adjacent cutoff is outside the prescribed grid when the cutoff is 0.01; the JSON explicitly records this boundary. For an interior cutoff, the lower diagnostic deliberately includes an unstable row to quantify sensitivity. The central estimate always excludes those rows.

For the delivered default run, the largest-x fixed-x fits and the mean fixed-ratio fits are:

| f | beta (SE) | alpha+beta (dispersion SE) | joint fitted C |
|---|---:|---:|---:|
| k^2+1 | 1.545447 (0.003875) | 2.000587 (0.000461) | 0.171792 |
| k^3+2 | 1.538298 (0.003730) | 2.000517 (0.001623) | 0.186050 |
| 2k+1 | 1.551171 (0.007484) | 2.000054 (0.000033) | 0.178538 |

The empirical small-ratio constants use the separate normalised extrapolation, not the joint power-law coefficient:

| f | empirical constant | uncertainty envelope | cutoff | cutoff sensitivity |
|---|---:|---:|---:|---|
| k^2+1 | 0.138371 | 0.007020 | 0.01 | 0.01: 0.138371; 0.02: 0.138904 |
| k^3+2 | 0.138511 | 0.007292 | 0.05 | 0.02: 0.137883; 0.05: 0.138511; 0.1: 0.139634 |
| 2k+1 | 0.140863 | 0.008159 | 0.01 | 0.01: 0.140863; 0.02: 0.141182 |

At the cubic cutoff the lower 0.02 diagnostic is unstable and the upper diagnostic uses 0.1. At the other two cutoffs, the lower grid step is unavailable. The cubic has a nonmonotone stability pattern: its 0.01 row changes by only 0.31%, but its 0.02 row changes by 1.23%; hence 0.05 is the valid cutoff. In fact, the cubic cutoff was 0.02 using 16 and 64 million, before the 256-million run moved it upward. Polynomial sampling can therefore affect this test even as x grows.

The normalised tables below use target ratios as column labels; the JSON records the actual ratios and unrounded values. These are deterministic finite computations. Standard errors elsewhere describe regression residuals, not uncertainty in the integer counts.

For f(k) = k^2+1:

| x | .01 | .02 | .05 | .1 | .2 | .4 | .7 | 1 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1000000 | 0.141855 | 0.143162 | 0.144886 | 0.151912 | 0.156975 | 0.163179 | 0.170250 | 0.171362 |
| 4000000 | 0.141686 | 0.143302 | 0.144687 | 0.151276 | 0.156752 | 0.162938 | 0.170032 | 0.171220 |
| 16000000 | 0.141175 | 0.143090 | 0.144622 | 0.151153 | 0.156632 | 0.162835 | 0.169986 | 0.171153 |
| 64000000 | 0.140949 | 0.142966 | 0.144505 | 0.151012 | 0.156578 | 0.162792 | 0.169935 | 0.171120 |
| 256000000 | 0.140858 | 0.142919 | 0.144457 | 0.150976 | 0.156550 | 0.162775 | 0.169925 | 0.171101 |

For f(k) = k^3+2:

| x | .01 | .02 | .05 | .1 | .2 | .4 | .7 | 1 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1000000 | 0.153562 | 0.149407 | 0.154182 | 0.155026 | 0.155087 | 0.158578 | 0.166278 | 0.170713 |
| 4000000 | 0.144716 | 0.147763 | 0.146250 | 0.151598 | 0.154780 | 0.157141 | 0.165214 | 0.168422 |
| 16000000 | 0.142399 | 0.144360 | 0.144416 | 0.149753 | 0.153584 | 0.156699 | 0.164844 | 0.167875 |
| 64000000 | 0.140427 | 0.142955 | 0.143925 | 0.149586 | 0.152600 | 0.155833 | 0.164525 | 0.167244 |
| 256000000 | 0.139990 | 0.141202 | 0.143912 | 0.148477 | 0.152339 | 0.155499 | 0.163990 | 0.166706 |

For f(k) = 2k+1:

| x | .01 | .02 | .05 | .1 | .2 | .4 | .7 | 1 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1000000 | 0.144392 | 0.148302 | 0.149320 | 0.156700 | 0.161696 | 0.162452 | 0.182388 | 0.183690 |
| 4000000 | 0.144507 | 0.148327 | 0.149321 | 0.156694 | 0.161706 | 0.162449 | 0.182390 | 0.183693 |
| 16000000 | 0.144609 | 0.148375 | 0.149350 | 0.156706 | 0.161712 | 0.162452 | 0.182390 | 0.183691 |
| 64000000 | 0.144593 | 0.148366 | 0.149341 | 0.156702 | 0.161709 | 0.162451 | 0.182390 | 0.183692 |
| 256000000 | 0.144598 | 0.148368 | 0.149343 | 0.156703 | 0.161710 | 0.162451 | 0.182390 | 0.183691 |

The normalised values are stable in x over most of this grid but retain sizeable ratio dependence. For example, the linear control ranges from about 0.1446 to 0.1837 at the largest x. That variation does not shrink in the displayed x range. Treat the fixed-ratio slopes near 2 and the fixed-x slopes near 1.54 as different empirical diagnostics; the latter absorb the persistent ratio curvature.
