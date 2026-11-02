**Short answer:** I know of no published result for the sparse variance V_f(x,y) itself. I can't point to a paper, thesis or preprint that treats moduli restricted to values f(k) with the weight f'(k). Everything below is for neighbouring problems, recalled from memory, and several details are shaky.

## 1. V_f or closely related sums

- **Nothing I can cite for V_f.** I don't recall a source for squarefree numbers in progressions with polynomially sparse moduli. If one exists, it is probably after or outside what I remember.
- **Heuristic only, not a theorem.** E(x;q,l) is typically of size (x/q)^{1/4}, so Σ_l E² should be about (xq)^{1/2} times an arithmetic factor depending on q. The f'(k) weight turns the sum over k into a sum over q ≈ f(k) with density dq. This suggests V_f ≍ x^{1/2} Σ f'(k) f(k)^{1/2} ≍ x^{1/2} y^{3d/2}, where d = deg f. The leading constant would involve an average of the arithmetic factor over q = f(k), which would need a polynomial-value analogue of a multiplicative mean. This is my own extrapolation, and I have no result backing it.

## 2. Analogous results

**All moduli q ≤ Y** (squarefree numbers in progressions):
- **Prachar (1958)** and **Hooley (1975, Bull. LMS, "A note on square-free numbers in arithmetic progressions")** gave early bounds on Σ_l E² for a single q and on averages over q. I'm fairly confident of the authors and general content, but not of the exact exponents.
- **Croft (1975, Proc. LMS)** and **Warlimont (around 1980, J. London Math. Soc.)** proved asymptotic formulas for the mean square, with order x^{1/2}Y^{3/2} after summing over q ≤ Y. I'm moderately confident about this, and not confident about the constants or ranges.
- **Blomer (2008, Quart. J. Math., on divisor sums in progressions)** improved ranges and error terms, and has a squarefree application. Moderate confidence.
- **Nunes (around 2015, JNT)** and **Le Boudec** have variance and large-sieve-type results extending the admissible range of Y relative to x. I'm unsure of the exact statements, ranges and exponents.
- **Related analogue: Hall (1982, Mathematika)**, squarefree numbers in short intervals, with variance ≍ x·h^{1/2}. I recall a constant involving ζ(3/2)/ζ(3), but I'm not sure of its exact form.

**Sparse variance for primes** (moduli restricted to primes, or similar thin sets):
- I don't recall a squarefree result with prime moduli. I'm aware of the general theme of prime-moduli averages for primes in progressions (Bombieri–Vinogradov-type), but that is a different problem, and I won't attribute a specific statement to it.

## 3. Confidence summary

| Item | Confidence |
|---|---|
| No known result for V_f | Moderate: it's absent from my memory, which doesn't prove absence |
| Heuristic order x^{1/2}Y^{3/2} for all-moduli variance | High that this is the true order, moderate on attribution |
| Croft / Warlimont asymptotics | Moderate on authors, low on details |
| Prachar / Hooley | Moderate on authors, low on exponents |
| Blomer / Nunes / Le Boudec | Low to moderate on exact statements |
| Hall's constant | Low |
| Prime sparse variance | I know of none |

Before relying on any of this, check the citations against MathSciNet or zbMATH, or ask me to look them up once tools are available.