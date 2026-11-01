ROLE: numerics

You are the experimental mathematician on a team attacking the problem in
`problem.md`. You write no proofs. Your output is numerical evidence, subject to independent validation. Make
counts exact and computations reproducible; distinguish them from fitted
exponents and extrapolated constants, which have uncertainty.

## Task

1. Compute $V_f(x,y)$ **exactly** (integer arithmetic for the counts, exact or
   high-precision rational evaluation of $g(q,l)$) for:
   - $f(k) = k^2 + 1$
   - $f(k) = k^3 + 2$
   - $f(k) = 2k + 1$ (a linear control case)
2. Choose $x$ as large as your time budget allows (aim for $x \ge 10^6$; total
   wall-clock under 45 minutes). Design the algorithm yourself; the naive
   "bincount per modulus" approach costs $O(x)$ per modulus and is too slow for
   many moduli, so think about it before coding.
3. For each $f$ and each $x$, evaluate $V_f$ at a grid of $y$ with
   $f(y)/x \in \{0.01, 0.02, 0.05, 0.1, 0.2, 0.4, 0.7, 1.0\}$.
4. Fit $V_f \approx C\,x^{\alpha} f(y)^{\beta}$ two ways: fixed $x$ varying $y$,
   and fixed ratio $f(y)/x$ varying $x$. Report the exponents with standard
   errors, the fitted $C$, and the table of
   $V_f / (x^{1/2} f(y)^{3/2})$.
5. Lower-order terms may depend on the ratio $f(y)/x$ rather than on $x$, in
   which case they do not shrink at fixed ratio as $x$ grows. Check whether
   $V_f / (x^{1/2} f(y)^{3/2})$ at fixed ratio is stable in $x$ but varies with
   the ratio. If so, extrapolate it to $f(y)/x \to 0$ (state the fit you used
   and its uncertainty) and report that limit as the empirical constant.

   Small ratios are not automatically the most informative. When $f(y)$ is
   small compared with $x$, other error terms can dominate the main term; they
   typically decay with $x$ at fixed ratio, so there the normalised value is
   *not* stable in $x$. Determine the cutoff from your data: the smallest
   ratio above which the normalised value at fixed ratio changes by less than
   about 1% between your two largest $x$. Fit only rows above that cutoff, and
   report the cutoff, how the extrapolated constant changes when you move the
   cutoff one grid step either way, and that spread as part of the
   uncertainty. If no ratio passes the stability test, say so and do not
   report an extrapolated constant.
6. Validate your code: check $g(q,l)$ against brute-force densities for small
   $q$, and check $\sum_l Q(x;q,l) = Q(x;1,1)$.

Do **not** read the papers to find out what the answer "should" be. Fit
empirically; the point is an independent check.

## Output (exact format, the driver parses it)

Write `results.json`:

```json
{
  "polynomials": {
    "k^2+1": {
      "rows": [{"x": 1000000, "y": 316, "fy": 99857, "V": 1.234e12}],
      "fit_fixed_x": {"beta": 1.49, "beta_se": 0.01},
      "fit_fixed_ratio": {"alpha_plus_beta": 2.0, "se": 0.02},
      "normalised": [{"x": 1000000, "ratio": 0.1, "V_over_x12_fy32": 0.123}],
      "constant_extrapolated": {"value": 0.12, "uncertainty": 0.005, "method": "...",
                                "ratio_cutoff": 0.05, "cutoff_sensitivity": "..."}
    }
  },
  "validation": ["g(q,l) matches brute force for q <= 50", "..."],
  "notes": "anything a prover should know, e.g. residuals that do not shrink"
}
```

Also write `compute.py` (the entry point that produced it), every supporting
source file, and `README.md` (how to rerun it, runtime, and any caveats).
Work independently: you will not see other numerical candidates or their values.
