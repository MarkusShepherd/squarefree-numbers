**1. Results for V_f(x,y) itself**

I know of no published result, thesis or preprint on V_f(x,y), meaning the variance of squarefree numbers over moduli restricted to values f(k) of a polynomial and weighted by f'(k). I'm not going to cite one.

The nearest literature, all from memory:

- **Individual modulus q (variance over residues l mod q).**
  - Prachar (1950s) gave pointwise bounds for E(x;q,l).
  - Hooley ("A note on square-free numbers in arithmetic progressions", Bull. LMS, mid-1970s) gave an upper bound for Σ_l E². I don't remember the exact exponents.
  - Warlimont (Monatsh. Math., around 1980) gave an asymptotic with main term of size roughly c·x^{1/2}q^{1/2}, for q in a range below x.
  - Nunes (J. Number Theory, c. 2016–17) improved the range and error term for the individual-modulus variance and related questions.
  - Confidence: moderate on who and roughly what. Low on exact constants, exponents and ranges.
- **Sparse moduli for related problems.** Baier and Zhao (Acta Arith. 2006, Math. Ann. 2008, and a square-moduli large-sieve paper in J. Number Theory 2008) proved Bombieri–Vinogradov-type and large-sieve results for sparse moduli such as squares, with applications to primes in quadratic progressions. These are not about squarefree variance or polynomial moduli with the f'(k) weight. Confidence: moderate on existence, low on details.

**2. Analogous variances**

- **All moduli q ≤ Y (squarefree Barban–Davenport–Halberstam analogue).** Σ_{q≤Y} Σ_l E² is known with an asymptotic main term, plausibly of shape c·x^{1/2}Y^{3/2}. This comes from summing the individual-q variance.
  - I associate Blomer (Quart. J. Math. 2008, divisor sums in progressions, with squarefree as a related case) and Le Boudec with asymptotics and error terms here.
  - Confidence: low to moderate on attribution, low on the exact statement.
- **Primes, all moduli.** The Barban–Davenport–Halberstam theorem and its refinements are classical: Montgomery–Hooley (asymptotic with the Hooley/Montgomery main term), Goldston–Vaughan (sharper error), and Languasco–Zaccagnini (explicit constants). Confidence: high on existence, moderate on details.
- **Primes, sparse moduli.** I'm not aware of a theorem for the polynomial-value sparse BDH sum with weight f'(k). The nearest results are the Baier–Zhao square-moduli results above. I'd treat any claim of a polynomial-moduli BDH asymptotic as unverified.

**3. Heuristic, not a literature result**

Squarefree n ≡ l (mod q) with n = d²m and d > √(x/q) contribute a pseudo-random term. That suggests Σ_l E(x;q,l)² ≍ √(xq) for q up to about x. Summing over q = f(k) with weight f'(k) would then give V_f ≍ x^{1/2}y^{3·deg(f)/2}, up to constants, in a suitable range. This is my own derivation, unchecked, and not a cited theorem. A rigorous version would need care with the arithmetic of f modulo d² and with the range of validity.