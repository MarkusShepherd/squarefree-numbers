**I know of no result for $V_f(x,y)$ that I can state.** I can't give a theorem, constant, or range for it, and everything below is from memory and unchecked.

## 1. $V_f$ and closely related sums

- **Possible paper on $V_f$ (low confidence):** I vaguely recall a title like "Sparse variance for $k$-free numbers in arithmetic progression", possibly by Brüdern and/or Wooley. This could be a false memory based on the primes paper in section 3, so treat the title, authors, and existence as unverified. I don't recall a statement or know of a relevant thesis or preprint.
- **Likely tools (high confidence that these exist, but they are not results on $V_f$):**
    - Brüdern, Perelli, Wooley, "Twins of $k$-free numbers and their exponential sum", *Michigan Math. J.* (1999).
    - Brüdern, Granville, Perelli, Vaughan, Wooley, "On the exponential sum over $k$-free numbers", *Phil. Trans. R. Soc. A* 356 (1998).

**Heuristic only, not a known theorem:** If $\sum_l E(x;q,l)^2 \approx C(q)\,x^{1/2}q^{1/2}$ holds on average over $q=f(k)$, then partial summation suggests

$$V_f(x,y)\approx \tfrac23\,\bar C_f\,x^{1/2}f(y)^{3/2}.$$

Here $\bar C_f$ would be a suitable average of the arithmetic factor $C(q)$ over the values of $f$, and $f(y)\le x$ with $f(y)$ not too small. I can't say what range is provable.

## 2. All moduli $q\le Y$, squarefree numbers

| Result | Statement as I recall it | Confidence |
|---|---|---|
| Croft, "Square-free numbers in arithmetic progressions", *Proc. LMS* 30 (1975) | $\sum_{q\le Y}\sum_{l=1}^q E(x;q,l)^2\sim C\,x^{1/2}Y^{3/2}$ | Citation and shape: fairly high. Constant, error term, range: not recalled |
| Vaughan, "A variance for $k$-free numbers in arithmetic progressions", *Proc. LMS* 91 (2005) | $k$-free analogue, main term $\asymp x^{1/k}Y^{2-1/k}$ | Citation: high. Shape: fairly high. Details: not recalled |
| Orr, *J. Number Theory* 3 (1971); Warlimont, *Monatsh. Math.* 73 (1969) and *JLMS* 22 (1980) | Earlier work on this variance, probably mostly upper bounds | Medium; I can't state these exactly |

**Fixed-modulus and short-interval results:**

- **Hall**, *Mathematika* 29 (1982): the short-interval variance is $\sim A\,h^{1/2}$ for $h\le x^{2/9-\varepsilon}$, with $A=\frac{\zeta(3/2)}{\pi}\prod_p\left(1-\frac{3p-2}{p^3}\right)$. Confidence: high.
- **Gorodetsky, Matomäki, Radziwiłł, Rodgers**, "On the variance of squarefree integers in short intervals and arithmetic progressions", *GAFA* (2021):
    - Short intervals: asymptotic for $H<x^{6/11-\varepsilon}$, or $H<x^{2/3-\varepsilon}$ under Lindelöf. Confidence: high.
    - Progressions: analogous result for $q>x^{5/11+\varepsilon}$, or $q>x^{1/3+\varepsilon}$ under GLH. Confidence: high for these ranges, but I'm unsure of the exact conditions on $q$ (possibly prime).
- **Other related work:** Blomer, *Q. J. Math.* (2008), and Le Boudec, *Math. Z.* (2018), give fixed-modulus variance bounds. I'm confident these exist, but can't state them exactly.

## 3. Sparse variance and all-moduli variance, primes

- **Sparse variance:** Brüdern and Wooley, "Sparse variance for primes in arithmetic progression", *Q. J. Math.* 62 (2011).
    - The paper treats essentially the sum above with $\psi$ in place of the squarefree count, and uses a circle-method approach.
    - Confidence: high for existence and fairly high for the citation details. I can't reliably recall the theorem, the degree hypotheses, or the range of $y$.
    - The expected main term is $x f(y)\log f(y)$, inferred from Hooley's heuristic rather than recalled from the paper.
- **All moduli:**
    - Barban (1960s), and Davenport and Halberstam, *Michigan Math. J.* 13 (1966), proved the upper bound $\ll xQ\log x$ for $x(\log x)^{-A}\le Q\le x$. Gallagher (1967) gave a simplified proof. Confidence: high.
    - Montgomery, *Michigan Math. J.* 17 (1970), proved that the variance equals $Qx\log x+O(Qx\log(2x/Q))+O(x^2(\log x)^{-A})$ for $Q\le x$. Using $\log Q$ instead of $\log x$ is equivalent within this error. Confidence: high.
    - Hooley, in the series "On the Barban–Davenport–Halberstam theorem" (from 1975), refined this. Goldston and Vaughan (1996) and Friedlander and Goldston (1996) gave further work on lower-order terms. Vaughan, *Phil. Trans. R. Soc. A* 356 (1998), treated general sequences. Confidence: high that these exist, medium on details.