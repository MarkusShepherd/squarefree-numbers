# Variance of squarefree numbers in arithmetic progressions to polynomial moduli: what I recall

This is from memory only, with no lookup. Confidence tags are **[high]**, **[medium]** and **[low]**.

## 1. The sparse variance $V_f(x,y)$ for squarefree numbers

**I know of no result for $V_f(x,y)$ itself**, nor for any variance of squarefree numbers in progressions where the moduli run over polynomial values $f(k)$. That includes the special case of square moduli $q=k^2$.

The weight $f'(k)$ is the natural one. It makes $\sum_{k\le y} f'(k) \approx f(y)$, which mimics summing over all $q \le Y = f(y)$ with density 1. So the natural conjecture is a main term of the form $C_f\, f(y)\, x^{1/2}$ in a suitable range. That is a heuristic, not a known theorem. If such a result exists, it is likely a recent preprint or thesis I cannot reliably recall, and I won't invent a reference.

## 2. Related results

### (a) Squarefree numbers, all moduli $q \le Y$

Write $V(x,Y)=\sum_{q\le Y}\sum_{l=1}^q E(x;q,l)^2$.

- **Croft (1975)**, *"Square-free numbers in arithmetic progressions"*, Proc. London Math. Soc. (3) 30 (1975). **[medium]**
  - Proved an asymptotic of the shape $V(x,Y) \sim C\, Y x^{1/2}$ in a range of $Y$ near $x$, with an explicit constant built from an Euler product and a zeta-value factor. **[medium]**
  - I do not reliably remember the exact range, error term or constant. **[low]**
- **Hooley (1975)**, a note on squarefree numbers in arithmetic progressions, Bull. London Math. Soc. **[low]**
  - I believe it concerns a related variance or average.
- **Warlimont**, papers on squarefree numbers in progressions from around 1969–1980 (Monatsh. Math.; J. London Math. Soc.). **[medium]** that they exist.
  - They give bounds or asymptotics for such variances. I can't state the exact claims. **[low]**
- **R. C. Vaughan (2005)**, *"A variance for k-free numbers in arithmetic progressions"*, Proc. London Math. Soc. **[medium-high]**
  - Asymptotic for the all-moduli variance of $k$-free numbers, main term of order $Y x^{1/k}$, in a wider range than Croft's. **[medium]**
  - Exact range and error term **[low]**.
- **Single-modulus variance** ($\sum_{l} E(x;q,l)^2$ for one $q$). This is not exactly the question, but it is closely related.
  - **Le Boudec**, Math. Z. (~2018) **[medium]**: asymptotic for $q$ in a range below $x$ but above $x^{1/2}$. The exponents are **[low]**.
  - **Gorodetsky–Matomäki–Radziwiłł–Rodgers**, *"On the variance of squarefree integers in short intervals and arithmetic progressions"*, GAFA (~2021) **[medium-high]** that the paper exists. Exact AP statements **[low]**.
  - **Keating–Rudnick** (Algebra & Number Theory, ~2016): the function-field analogue **[medium-high]**.

### (b) Primes, all moduli

- **Barban (1964); Davenport–Halberstam (1966–68)**: the upper bound $\sum_{q\le Q}\sum_{a}^{*} E(x;q,a)^2 \ll xQ\log x$ for $x(\log x)^{-A}\le Q\le x$. **[high]**
- **Montgomery (1970)**: the asymptotic $\sim Qx\log Q$. **[high]**
- **Hooley**: refinements in the series *"On the Barban–Davenport–Halberstam theorem I–…"*, J. reine angew. Math. and elsewhere, 1975 onward. **[high]** that the series exists; individual statements **[medium]**.

### (c) Primes, sparse or polynomial moduli

- **Baier–Zhao**, *"Bombieri–Vinogradov type theorems for sparse sets of moduli"*, Acta Arith. (~2006). **[medium]**
  - Treats square (and I think more general power or polynomial) moduli via large-sieve inequalities for square moduli.
  - I believe it includes a BDH-type upper bound for moduli $k^2$. That part is **[low–medium]**.
  - Related: Baier–Zhao, large sieve for square moduli, J. Number Theory (~2008). **[medium]**
- **R. C. Baker**, *"Primes in arithmetic progressions to spaced moduli"* (I, II, III; Acta Arith. / related journals, ~2017+). **[medium]**
  - BV/BDH-type results for sparse moduli sets.
  - I'm unsure whether polynomial-value moduli with an asymptotic variance are covered. **[low]**
- I don't recall a proven **asymptotic** (Montgomery–Hooley type) for primes with polynomial moduli and the $f'(k)$ weighting. **[low]**: it may exist, but I can't name it.

## 3. Confidence summary

- **High:** the classical prime BDH and Montgomery results, and the existence of Hooley's BDH series.
- **Medium:** that Croft, Vaughan, Warlimont, Le Boudec, GMRR, Baier–Zhao and Baker have the papers described, and their broad content.
- **Low:** every precise range, exponent, constant and error term above, and Hooley's 1975 squarefree note.
- **None known:** any theorem for $V_f(x,y)$ itself.