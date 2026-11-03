I do **not** know a theorem for the polynomially restricted quantity \(V_f(x,y)\) itself. I cannot supply a reliable reference for it from memory.

There is also a convention to check: for squarefree numbers, the main term for a general residue \(l\) depends on its divisibility by primes dividing \(q\). A theorem summing only over \((l,q)=1\) does not immediately give your sum over all \(l\).

1. **A closely related squarefree variance that I do remember.**

   Ofir Gorodetsky, Kaisa Matomäki, Maksym Radziwiłł and Brad Rodgers, *On the variance of squarefree integers in short intervals and arithmetic progressions*, published in *Geometric and Functional Analysis* (2021).

   A consequence of their arithmetic-progression theorem is the following. For fixed \(\varepsilon>0\), uniformly for **prime** \(q\) in
   \[
   x^{5/11+\varepsilon}\le q\le x^{1-\varepsilon},
   \]
   one has
   \[
   \frac1{q-1}\sum_{a=1}^{q-1}
   \left(
   \sum_{\substack{n\le x\\n\equiv a\pmod q}}\mu^2(n)
   -\frac{6}{\pi^2}\frac{x}{q}(1-q^{-2})^{-1}
   \right)^2
   =
   C\sqrt{\frac{x}{q}}
   +o_\varepsilon\!\left(\sqrt{\frac{x}{q}}\right),
   \]
   where
   \[
   C=\frac{\zeta(3/2)}{\pi}
   \prod_p\left(1-\frac3{p^2}+\frac2{p^3}\right).
   \]
   The paper gives a quantitative error; I do **not** reliably remember its exponent, so the displayed statement is a weaker asymptotic consequence, not a quotation of its full error term.

   **Confidence:** high in the authors, title, main term and prime-modulus range; reasonably high in the displayed constant. This is a result about squarefree integers with prime moduli, not about counting primes.

2. **Squarefree variance averaged over all moduli.**

   I remember Croft’s *Square-free numbers in arithmetic progressions* (1975) as a source for this problem, and recall the characteristic main-term scale
   \[
   x^{1/2}Y^{3/2}
   \]
   for the unnormalised sum over \(q\le Y\) and residue classes.

   However, I cannot reliably reconstruct from memory the precise centering convention, constant, error term or admissible range in Croft’s theorem. **This is an incomplete bibliographic recollection, not a theorem statement you should cite.** I do not know enough from memory to satisfy your request for an exact all-moduli squarefree theorem.

3. **Primes: all moduli and polynomially restricted moduli.**

   For all moduli, the classical **Barban–Davenport–Halberstam theorem** gives, with
   \[
   \psi(x;q,a)=\sum_{\substack{n\le x\\n\equiv a\pmod q}}\Lambda(n),
   \]
   the bound
   \[
   \sum_{q\le Y}\ \sum_{\substack{a\bmod q\\(a,q)=1}}
   \left|\psi(x;q,a)-\frac{x}{\varphi(q)}\right|^2
   \ll_A xY\log x,
   \qquad
   \frac{x}{(\log x)^A}\le Y\le x,
   \]
   for each fixed \(A>0\). This is an upper bound, so it has no asserted leading constant. The theorem originates in papers of Barban and of Davenport–Halberstam; I do not reliably remember their exact bibliographic details. I am highly confident in this formulation of the bound. It concerns von Mangoldt weighted counts.

   For the **sparse prime variance with moduli \(f(k)\) and weight \(f'(k)\)**, I cannot confidently identify a paper or state an exact theorem from memory. I would not infer one merely from sparse large-sieve results: those need not supply a variance asymptotic or its constant.

Thus my reliable positive recollection is the individual prime-modulus squarefree asymptotic above and the classical all-moduli prime variance bound. I have no reliable theorem-level answer for \(V_f\) itself or its polynomial-modulus prime analogue.