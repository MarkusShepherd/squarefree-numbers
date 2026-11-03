**1. Results for V_f(x,y) itself**

I know of no result for V_f(x,y), meaning the variance restricted to moduli q = f(k) with the weight f'(k). I can't point to any paper, thesis or preprint that states a main term, constant, error term or range for it. If such a result exists, I don't recall it, and I won't invent a citation.

Heuristic only, not a recalled result: the weight f'(k) is the Jacobian of k ↦ q = f(k). So V_f looks like a smoothed version of the full-modulus sum, with the sparse set of moduli weighted by its local density. I'd expect the same x^{1/2}·(modulus)² scale as in the dense case below. I can't state the constant or the error term from memory.

**2. Related results**

All of these are from memory, and the exact statements are fuzzy.

*Squarefree numbers, single modulus or all moduli q ≤ Q:*
- **Prachar, Croft, Hooley (1950s–70s).** Early mean-square bounds for the squarefree error term in progressions. Hooley's is "A note on square-free numbers in arithmetic progressions", Bull. LMS 7 (1975). I'm fairly sure of the paper. I'm unsure of its exact exponents.
- **Warlimont**, J. London Math. Soc. (1980). I believe this gives an asymptotic for Σ_a E(x;q,a)² for a single q in a range of q, of size about x^{1/2}·q times a constant. I'm unsure of the range and the constant.
- **Blomer**, "The average value of divisor sums in arithmetic progressions", Quart. J. Math. (2008). I believe this gives an asymptotic for Σ_{q≤Q} Σ_a E² of the form c·x^{1/2}Q² with a power-saving error in a wide range of Q. I'm unsure of the constant and the exact range.
- **Nunes** and **Le Boudec**. Both worked on squarefree numbers in progressions with large moduli, including mean-square or large-sieve-type bounds. I'm not confident of the statements. Treat these as pointers to look up, not facts.

*Primes, all moduli:*
- **Barban–Davenport–Halberstam** (1960s). Σ_{q≤Q} Σ_{(a,q)=1} (ψ(x;q,a) − x/φ(q))² ≪ xQ log x for Q ≤ x/(log x)^A.
- **Montgomery** (1970) and **Hooley** (1975, "On the Barban–Davenport–Halberstam theorem", I onward) gave the asymptotic ~ Qx log(x/Q) + O(Qx) in a range up to Q ≈ x. I'm confident of the shape and moderately confident of the attributions.
- **Friedlander–Goldston** refined the error terms. This is moderate confidence.

*Primes, sparse moduli:*
- I know of no sparse-polynomial-moduli variance result for primes. This covers both a "sum over k of f'(k)·(variance at modulus f(k))" form and the case where the moduli are themselves prime. Bombieri–Vinogradov-type averages over restricted or sparse moduli exist, but I can't cite a specific mean-square statement.

**3. Confidence**

| Item | Confidence |
|---|---|
| No known result for V_f | Moderate. It may exist after my knowledge or outside my recall. |
| Barban–Davenport–Halberstam / Montgomery–Hooley | Fairly high on the shape, moderate on the details |
| Warlimont, Blomer shape (x^{1/2}·modulus²) | Moderate |
| Constants, ranges, error terms for any squarefree result | Low |
| Nunes, Le Boudec relevance | Low |
| Sparse prime-moduli variance | Low. I know of none. |

I'd verify the squarefree items against the originals before relying on them.