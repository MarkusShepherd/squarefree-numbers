I do **not** know a result for \(V_f(x,y)\) itself that I can reliably attribute and state. In particular, I cannot supply a reference for a general polynomial \(f\), or a main-term constant and admissible range for that sum.

Here is what I can recall, with the limits of that recollection made explicit. Everything below is from memory.

1. **Squarefree integers: variance for a fixed prime modulus.**

   Gorodetsky, Matomäki, Radziwiłł and Rodgers, *“On the variance of squarefree integers in short intervals and arithmetic progressions,”* published in *Geometric and Functional Analysis*, prove an asymptotic for the variance in arithmetic progressions.

   A consequence I recall is that, for fixed \(\varepsilon>0\) and prime \(q\) in
   \[
   x^{5/11+\varepsilon}\le q\le x^{1-\varepsilon},
   \]
   one has
   \[
   \sum_{a=1}^{q-1}
   \left(
   \sum_{\substack{n\le x\\n\equiv a\pmod q}}\mu^2(n)
   -\frac{6}{\pi^2}\frac{x}{q}(1-q^{-2})^{-1}
   \right)^2
   =
   C\sqrt{xq}+o_\varepsilon(\sqrt{xq}),
   \]
   uniformly in that range, where
   \[
   C=\frac{\zeta(3/2)}{\pi}
   \prod_p\left(1-\frac{3}{p^2}+\frac{2}{p^3}\right).
   \]

   **Confidence:** high in the authors, paper, constant and basic asymptotic; reasonably high in the \(5/11+\varepsilon\) range. I do not remember their more precise quantitative error term. This is a fixed-modulus result over reduced residue classes, so it does not directly state your polynomial-modulus theorem.

2. **Squarefree integers: averaging over all moduli.**

   M. J. Croft’s paper *“Square-free numbers in arithmetic progressions,” Proceedings of the London Mathematical Society* (1975), is a classical reference for mean-square results of this kind. I associate it with an asymptotic whose leading scale, after summing over \(q\le Y\), is
   \[
   x^{1/2}Y^{3/2}.
   \]

   **Confidence:** high in the reference and its relevance. I do **not** reliably remember the precise residue-class convention, constant, error term or range. Consequently, I cannot give the exact theorem requested here without consulting it. I also cannot confidently reconstruct subsequent improvements from memory.

3. **Primes: averaging over all moduli.**

   The classical Barban–Davenport–Halberstam theorem, together with Montgomery’s asymptotic refinement, gives the following standard formulation. With
   \[
   \psi(x;q,a)=
   \sum_{\substack{n\le x\\n\equiv a\pmod q}}\Lambda(n),
   \]
   for each fixed \(A>0\),
   \[
   \sum_{q\le Y}\ \sum_{\substack{a\bmod q\\(a,q)=1}}
   \left|\psi(x;q,a)-\frac{x}{\varphi(q)}\right|^2
   \sim xY\log x
   \]
   uniformly for
   \[
   \frac{x}{(\log x)^A}\le Y\le x.
   \]

   Montgomery’s paper *“Primes in arithmetic progressions”* is a reference for the asymptotic refinement.

   **Confidence:** high in this formulation and attribution. I am stating the error as \(o(xY\log x)\); I do not recall the precise explicit remainder or the original bibliographic details of all the component results.

4. **Primes: sparse square moduli—a related theorem, not a variance asymptotic.**

   Baier and Zhao proved a Bombieri–Vinogradov theorem for square moduli. The formulation I recall is
   \[
   \sum_{r\le x^{2/9-\varepsilon}}
   r\max_{\substack{a\bmod r^2\\(a,r)=1}}
   \left|\psi(x;r^2,a)-\frac{x}{\varphi(r^2)}\right|
   \ll_{\varepsilon,A}\frac{x}{(\log x)^A}
   \qquad(A>0).
   \]
   The relevant paper is *“Bombieri–Vinogradov type theorem for sparse sets of moduli.”*

   This has moduli \(f(r)=r^2\) and a weight proportional to \(f'(r)\), but controls a maximum absolute error rather than your sum of squared errors.

   **Confidence:** high in the authors and square-modulus result; medium in the exact displayed formulation and its placement in that particular paper. I do not remember a general polynomial sparse-prime **variance asymptotic** well enough to quote one.

One convention matters when comparing these results: your sum includes **all** residue classes, whereas several familiar squarefree variance theorems use only \((l,q)=1\). For all residue classes, the appropriate squarefree density depends on \(l\) and \(q\); the reduced-class centering displayed in item 1 cannot simply be used for every \(l\).