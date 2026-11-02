# Variance of squarefree numbers in APs (sparse moduli $f(k)$): what I recall, with confidence levels

This is from memory only. I could not check anything, so treat all bibliographic details as approximate.

## 1. Results for $V_f(x,y)$ itself

**I know of no published result for $V_f(x,y)$**, meaning the squarefree variance restricted to moduli $f(k)$ with weight $f'(k)$.

- I have a vague sense that "Barban–Davenport–Halberstam (BDH) or Montgomery–Hooley over polynomial or sparse moduli" has been studied for squarefree or $k$-free numbers. I cannot name an author, title or statement, so I won't.
- If such a result exists, it is probably a recent preprint or thesis that I don't reliably know.
- My guess at its shape: the $f'(k)$ weight makes $\sum_{k\le y} f'(k)\,g(f(k)) \approx \int g(u)\,du$, so you would expect something like $V_f \sim C\,x^{1/2}\sum_{k\le y} f'(k)\,f(k)\cdot(\text{local factor}) \approx C' x^{1/2} f(y)^2$ in a suitable range. **This is my heuristic, not a known theorem.**

## 2a. Squarefree numbers, all moduli $q \le Q$

Write $V(x,Q)=\sum_{q\le Q}\sum_{a=1}^{q} E(x;q,a)^2$.

**Upper bounds of BDH type.**
- Warlimont (around 1969–1980; I think one paper is in J. London Math. Soc. 1980) gave bounds roughly of the form $V \ll x^2/Q + Qx^{1/2+\varepsilon}$, or close to it.
- Blomer, "The average value of divisor sums in arithmetic progressions," Quart. J. Math. (around 2008), has related bounds.
- *Confidence: medium on the authors, low on the exact exponents.*

**Asymptotic: Croft, "Square-free numbers in arithmetic progressions," Proc. LMS (around 1975).**
- States $V(x,Q) \sim C\,Q\,x^{1/2}$ for $Q$ in a range below $x$.
- $C$ is an explicit constant involving $\zeta(3/2)$, a factor like $1/\pi$, and an Euler product resembling $\prod_p(1-3p^{-2}+2p^{-3})$.
- *Confidence: high that Croft proved an asymptotic with main term $\asymp Qx^{1/2}$. Low on the exact constant and on the admissible range (something like $x^{\theta+\varepsilon}\le Q\le x$ with $\theta$ around $2/3$ or less; I don't trust that number).*

**$k$-free generalisations.**
- Brüdern, Granville, Perelli, Vaughan and Wooley, "On the exponential sum over $k$-free numbers," Phil. Trans. R. Soc. A (1998), used a circle-method approach.
- Vaughan, "A variance for $k$-free numbers in arithmetic progressions," Proc. LMS (around 2005), gives $V_k(x,Q) = C_k\,Q\,x^{1/k} + (\text{error})$ over a wider range.
- *Confidence: medium-high on existence and main-term shape, low on error terms and ranges.*

**Individual modulus**, i.e. $\sum_a E(x;q,a)^2$ for a single $q$:
- Hooley (1970s) did work on this.
- Le Boudec, "On the distribution of squarefree integers in arithmetic progressions," Math. Z. (around 2018), gives an asymptotic of size $\asymp x^{1/2}q^{\cdots}$ for $q$ in a range near $x$.
- Nunes had related work around 2015–2017.
- *Confidence: medium on authors, low on ranges.*

**Gorodetsky, Matomäki, Radziwiłł and Rodgers**, "On the variance of squarefree integers in short intervals and arithmetic progressions," GAFA (around 2021).
- Unconditional asymptotic for the variance in short intervals of length $H<x^{6/11-\varepsilon}$.
- Unconditional asymptotic for the variance in APs modulo a single $q>x^{5/11+\varepsilon}$.
- Wider ranges hold under RH or Lindelöf-type hypotheses.
- *Confidence: fairly high on the $6/11$ and $5/11$ exponents.*

**Function field analogue.** Keating and Rudnick, "Squarefree polynomials and Möbius values in short intervals and arithmetic progressions," Algebra & Number Theory (around 2016). They give variance asymptotics in $\mathbb F_q[t]$ and matching conjectures over $\mathbb Z$. *Confidence: high.*

**Related, short intervals.** R. R. Hall, Mathematika (around 1982), proved a variance asymptotic $\sim A\,h^{1/2}x$ for $h \le x^{2/9-\varepsilon}$. *Confidence: medium-high.*

## 2b. Primes, all moduli

**BDH upper bound.** Proved by Barban (1964), Davenport–Halberstam (1966, with a corrigendum) and Gallagher (1967):
$$\sum_{q\le Q}\sum_{(a,q)=1}\Big(\psi(x;q,a)-\frac{x}{\varphi(q)}\Big)^2 \ll xQ\log x$$
for $x(\log x)^{-A}\le Q\le x$. *Confidence: high.*

**Montgomery–Hooley asymptotic.**
- Montgomery, Michigan Math. J. (1970), and Hooley, J. reine angew. Math. (1975), plus Hooley's long series "On the Barban–Davenport–Halberstam theorem I, II, …".
- States the sum equals $Qx\log Q + cQx + O\big(Q^{5/4}x^{3/4} + x^2(\log x)^{-A}\big)$.
- *Confidence: high on the main terms, medium on the exact error term.*

**Extended ranges.** Friedlander and Goldston, "Variance of distribution of primes in residue classes," Quart. J. Math. (around 1996), extend the range, partly under hypotheses. *Confidence: medium.*

## 2c. Primes, sparse moduli

- Baier, and Baier–Zhao, around 2006–2008 (Acta Arith., J. Ramanujan Math. Soc.), proved large-sieve inequalities for square and polynomial moduli. They derived Bombieri–Vinogradov and BDH-type upper bounds for sparse moduli sets such as $q=k^2$.
- *Confidence: medium that these exist. Low on titles and exact statements.*
- I do not reliably recall a Montgomery–Hooley-type **asymptotic** for primes over polynomial moduli with the $f'(k)$ weighting. I suspect something like it exists (possibly in Hooley's series, or recent work), but I can't cite it.

## 3. Confidence summary

| Item | Confidence |
|---|---|
| No known result for $V_f$ itself (squarefree) | I know of none; one may exist that I'm unaware of |
| Croft 1975, asymptotic $\asymp Qx^{1/2}$ | High on existence; low on constant and range |
| Vaughan 2005; BGPVW 1998 ($k$-free) | Medium-high on existence; low on details |
| Warlimont, Blomer upper bounds | Medium on authors; low on exponents |
| Le Boudec, Nunes, Hooley (individual $q$) | Medium on authors; low on ranges |
| GMRR (GAFA), $6/11$ and $5/11$ | Fairly high |
| Keating–Rudnick | High |
| Hall, $h^{1/2}x$ for $h\le x^{2/9-\varepsilon}$ | Medium-high |
| BDH; Montgomery–Hooley for primes | High (medium on error term) |
| Friedlander–Goldston | Medium |
| Baier / Baier–Zhao sparse-moduli large sieve and BV/BDH bounds | Medium on existence; low on details |
| Sparse-moduli Montgomery–Hooley asymptotic for primes | Don't know; possibly exists |