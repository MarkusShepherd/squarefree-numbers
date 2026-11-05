# Integration of the passed propositions

The propositions compose, with all errors as stated. They prove the chosen
plan's main theorem for the original polynomial class and weight, with no
additional loss. This conclusion uses the passed propositions as premises;
it does not replace their independent refereeing.

Only `problem.md`, `plan.json`, `results.json`, and the supplied proposition
artifacts were used. No external source was consulted, and no excluded source,
previous proof attempt, or previous manuscript was encountered or used.

## Common notation and coefficient interfaces

Write
\[
c=\zeta(2)^{-1},\quad d=\deg f,\quad Y=f(y),\quad
a=4d-1,\quad \eta=\min\{1/5,1/a\}.
\]
Use \(\mathfrak S,\lambda,W_f,D_f,P_f,H_f,\Theta_f,F_f\) exactly as
defined in P1 and P4–P6. The following identifications are essential:

* P1's \(\lambda(r)=\varphi(r)c^2G(r)^2\) is precisely the
  cube-free-supported function in P4 and P5, including \(\lambda(1)=c^2\).
* The singular series and the local factors of \(W_f\) agree in P3–P6.
  In particular, \(\rho(1)=1\) handles primes with \(p^2\mid h\).
* P5 supplies
  \[
  R_f=P_f(1)=\operatorname{Res}_{s=1}D_f(s)
      =\sum_{r\ge1}\lambda(r)\rho(r)/r.
  \]
  Thus P4's density coefficient is exactly P6's residue, rather than
  another coefficient requiring an approximation.
* Writing \(L_f\) for the constant Laurent coefficient of \(D_f\) at one,
  P5 gives \(L_f=\gamma_E R_f+P_f'(1)\); hence both definitions give
  \(B_f=L_f-3R_f/2\).
* At \(s=-1/2\),
  \[
  \operatorname{Res}D_f(s)=\tfrac12\zeta(-1/2)H_f(-1/2),\qquad
  K_f=-\tfrac{16}{3}\operatorname{Res}D_f(s)
      =-\tfrac83\zeta(-1/2)H_f(-1/2)>0.
  \]
  The factor \(1/2\) comes from \(\zeta(2s+2)\). P5 also gives
  \(D_f(0)=-c/2\), consistent with the positive \(cH\) term in P6.

## Composition before choosing the cutoffs

Fix \(0<\varepsilon<\eta/2\), and apply P2 and P3 with the smaller
exponent \(e=\varepsilon/2\). All constants below depend at most on
\(f,\varepsilon\). Initially suppose
\[
1\le z\le y,\qquad 2\le Z=f(z)\le Y\le x,\qquad 2\le R\le x.
\]
Define
\[
\begin{split}
M&=\sum_{z<k\le y}f'(k)\sum_{1\le h\le x/f(k)}
             (x-hf(k))\mathfrak S(hf(k)),\\
I&=\int_Z^Y\sum_{1\le h\le x/t}(x-ht)W_f(h)\,dt,\\
A&=Z^{-1/d}R^{1/2}(\log(2R))^2
      +R^{-1/2}(\log(2R))^2\log(2x).
\end{split}
\]
The polynomial assumptions give \(f(t)\asymp_f t^d\),
\(f'(t)\ll_f t^{d-1}\), and therefore
\[
\sum_{z<k\le y}\frac{f'(k)}{f(k)}\ll_f\log(2x).
\]
For every pair \((k,h)\) in these sums, \(m=hf(k)\) is an integer
in \([1,x]\), as required by P3. Its error is uniform in this entire
range, including \(m\) close to \(x\). Summing that error gives
\[
\begin{split}
|S_f-M|
&\le C_e x^{4/5+e}\sum_{z<k\le y}f'(k)\lfloor x/f(k)\rfloor\\
&\ll_{f,e}x^{9/5+e}\log(2x).
\end{split}
\]
P4 separately gives
\[
M=I+O_f(x^2A),\qquad T_f=R_f\log(Y/Z)+O_f(A).
\]
Consequently P2 implies
\[
\begin{split}
V_f(x;z,y)
={}&cx(Y-Z)+2I-x^2R_f\log(Y/Z)\\
&+O_{f,e}\left(x^{3/2+e}+xY^{1-1/d}
                     +x^{9/5+e}\log(2x)+x^2A\right).
\tag{1}
\end{split}
\]
In detail, the correlation substitution contributes twice its bound;
the off-diagonal averaging contributes \(2O_f(x^2A)\), and density
averaging contributes \(-x^2O_f(A)\). These constants are absorbed in
(1); no error has been omitted.

P6's integral identity is exact:
\[
2I=Z^2\Theta_f(x/Z)-Y^2\Theta_f(x/Y).
\]
The definition
\[
F_f(H)=R_f\log H+B_f+c/H-\Theta_f(H)/H^2
\]
then gives the exact cancellation
\[
\begin{split}
cx(Y-Z)+2I-x^2R_f\log(Y/Z)
=x^2\{F_f(x/Y)-F_f(x/Z)\}.
\end{split}
\tag{2}
\]
The \(B_f\) terms cancel, and the signs of both the logarithm and
diagonal terms agree. By P6, uniformly for \(H\ge1\),
\[
F_f(H)=K_fH^{-3/2}+O_f(H^{-13/8}),\qquad
|F_f(H)|\ll_f H^{-3/2}.
\tag{3}
\]
Splitting the original sum at the real point \(z\), and using P2 on
the initial part, (1)–(3) now yield the full unoptimized error budget
\[
\boxed{\begin{split}
V_f(x,y)=x^2F_f(x/Y)+O_{f,e}\big(&x^{3/2+e}
 +xY^{1-1/d}+x^{9/5+e}\log(2x)\\
 &+x^2Z^{-1/d}R^{1/2}(\log(2R))^2\\
 &+x^2R^{-1/2}(\log(2R))^2\log(2x)\\
 &+x^{1+e}Z^{2-1/d}+x^{1/2}Z^{3/2}\big).
\end{split}}
\tag{4}
\]
The last two errors respectively dispose of \(V_f(x,z)\) and
\(x^2F_f(x/Z)\). Alternatively, expanding that boundary profile by
(3) gives a boundary main term \(K_fx^{1/2}Z^{3/2}\) and error
\(O_f(x^{3/8}Z^{13/8})\). The latter is bounded by the last term
of (4), since \((Z/x)^{1/8}\le1\).

## Cutoff choices and every exponent

Take
\[
\theta=\frac{2d}{4d-1}=\frac{2d}{a},\qquad
Z=x^\theta,\qquad R=Z^{1/d}=x^{2/a}.
\]
For all sufficiently large \(x\), depending only on \(f\),
\(Z\ge f(1)\), \(Z\ge2\), and \(R\ge2\).
Both cutoff powers are strictly less than one. Since \(f'\ge1\),
there is a unique real \(z\ge1\) with \(f(z)=Z\); if \(Y\ge Z\),
then \(z\le y\). Thus all hypotheses of P2, P4, and P6 hold.

The errors of (4) specialize as follows, retaining logarithmic losses:

| Origin | Bound after choosing the cutoffs |
|---|---|
| P2 variance reduction | \(x^{3/2+e}\) |
| P2 polynomial endpoint | \(xY^{1-1/d}\le x^{2-1/d}\) |
| P3 summed correlation error | \(x^{9/5+e}\log(2x)\) |
| P4 finite spectral sum | \(x^{2-1/a}(\log(2R))^2\) |
| P4 spectral tail | \(x^{2-1/a}(\log(2R))^2\log(2x)\) |
| P2 initial moduli | \(x^{1+e}Z^{2-1/d}=x^{2-1/a+e}\) |
| Lower profile boundary | \(x^{1/2}Z^{3/2}=x^{1/2+3d/a}\) |

For the last row,
\[
2-1/a-(1/2+3d/a)=\frac{6d-5}{2a}>0.
\]
Also \(\eta\le1/5\), \(\eta\le1/a\), and \(\eta\le1/d\).
Use \(\log(2x)\ll_\varepsilon x^{\varepsilon/2}\) in the P3 row,
and \((\log(2x))^3\ll_\varepsilon x^{\varepsilon/2}\) in the P4 rows.
Since \(e=\varepsilon/2\), every row is
\(O_{f,\varepsilon}(x^{2-\eta+\varepsilon})\). This proves
\[
V_f(x,y)=x^2F_f(x/Y)+O_{f,\varepsilon}(x^{2-\eta+\varepsilon})
\tag{5}
\]
when \(Y\ge Z\).

If \(Y<Z\), apply P2 directly at \(y\):
\[
V_f(x,y)\ll_{f,e}x^{1+e}Y^{2-1/d}
 \le x^{2-1/a+e}O_{f,e}(1).
\]
At the same time (3) gives
\[
x^2|F_f(x/Y)|\ll_f x^{1/2}Y^{3/2}
 \le x^{1/2+3d/a}O_f(1).
\]
The same exponent comparisons prove (5) in this case too. Real \(y\)
and \(z\) cause no further error: the discrete sums split exactly with
the conventions \(k\le z\) and \(z<k\le y\), and the propositions
already include real endpoints and the error \(xY^{1-1/d}\).

Finally, (3) at \(H=x/Y\), multiplied by \(x^2\), gives exactly
\[
x^2F_f(x/Y)=K_fx^{1/2}Y^{3/2}
                 +O_f(x^{3/8}Y^{13/8}).
\tag{6}
\]
Combining (5) and (6) is the second estimate of P7 and of the plan.

## Numerical constant and independent checks

For convenient numerical evaluation, set
\[
\alpha_p=1-2/p^2+\rho(p^2)/p^4,\quad
\beta_p=\rho(p)/p^3-\rho(p^2)/p^4,\quad
\delta_p=1/p^2-\rho(p)/p^3.
\]
The grouped local factor at the relevant point is
\[
L_p=(1-1/p)(\alpha_p+\beta_p\sqrt p+\delta_pp),\qquad
K_f=-\tfrac83\zeta(-1/2)\prod_p L_p.
\tag{7}
\]
This is algebraically the Euler product in P5, with its normalization
and residue factor retained.

For \(f(t)=t^2+1\), \(\rho(2)=1\), \(\rho(4)=0\); for odd primes,
\(\rho(p)=\rho(p^2)=2\) if \(p\equiv1\pmod4\), and both are zero
otherwise. For \(f(t)=t^3+2\), the exceptional pairs
\((\rho(p),\rho(p^2))\) at \(p=2,3\) are both \((1,0)\).
For \(p>3\), the two root counts agree; they are one if
\(p\equiv2\pmod3\), and otherwise three or zero according as
\((-2)^{(p-1)/3}\equiv1\pmod p\) or not. Simple roots have unique
lifts modulo \(p^2\), as follows directly by expanding
\(f(u+pv)\) modulo \(p^2\).

A sieve and these modular tests give the following partial products:

| Prime cutoff | \(K_{t^2+1}\) | \(K_{t^3+2}\) |
|---:|---:|---:|
| \(10^4\) | 0.138088026876 | 0.135612819679 |
| \(10^5\) | 0.138083068192 | 0.135607953971 |
| \(10^6\) | 0.138082663035 | 0.135607555131 |
| \(10^7\) | 0.138082628837 | 0.135607521554 |

For a conservative truncation bound, beyond this cutoff both root
counts are at most three. Expanding (7) shows
\(|L_p-1|\le15/p^2\). Thus the omitted product differs from one by at
most \(\exp(15/N)-1\), using
\(\sum_{p>N}p^{-2}\le\sum_{n>N}n^{-2}\le1/N\).
At \(N=10^7\), this bounds the absolute truncation error in these
constants by \(2.08\times10^{-7}\) and \(2.04\times10^{-7}\),
respectively. These bounds concern truncation; numerical evaluation
used extended precision for the product and 40-digit zeta evaluation,
without a formal interval-arithmetic rounding certificate.

Accordingly the predicted small-ratio main terms are
\[
\begin{array}{ll}
f(k)=k^2+1:& V_f(x,y)\sim0.138083\,x^{1/2}(y^2+1)^{3/2},\\
f(k)=k^3+2:& V_f(x,y)\sim0.135608\,x^{1/2}(y^3+2)^{3/2},
\end{array}
\]
in the asymptotic range specified below. Comparing with
`constant_extrapolated`, rather than a fixed-ratio row, gives:

| Polynomial | Analytic constant, cutoff \(10^7\) | Extrapolated constant | Heuristic uncertainty | Relative discrepancy \((K-C)/C\) |
|---|---:|---:|---:|---:|
| \(k^2+1\) | 0.138082628837 | 0.134474705492 | 0.007284958561 | +2.68298% |
| \(k^3+2\) | 0.135607521554 | 0.136321256839 | 0.002403606058 | −0.52357% |

Both differences are inside the recorded heuristic bands (0.4953
and 0.2969 times their respective half-widths). There is no clean-factor
discrepancy. The bands are not rigorous confidence intervals or bounds
on the theorem's remainder.

I independently reconstructed the primary extrapolation by taking the
largest-\(x\) rows with target ratio at least 0.01 and fitting
\(N(r)=C+a\sqrt r+br\) by unweighted least squares, using the actual
ratios as arguments. The coefficient vectors reproduce the snapshot:
\[
\begin{split}
t^2+1:&\quad(0.13447470549221466,\ 0.05829819823814369,
                                  -0.020881393324478102),\\
t^3+2:&\quad(0.13632125683949853,\ 0.037554586806314995,
                                  -0.006861994814706394).
\end{split}
\]
No numerical implementation source was supplied in the working directory.
As an independent check of the snapshot's counting and density conventions,
I sieved squarefree integers through \(x=250000\), counted every residue
class directly for all \(k\le49\) in the quadratic case and \(k\le13\)
in the cubic case, and evaluated P1's local density factors as exact
rationals times \(c\). If \(b(q,l)=g(q,l)/c\), the checked decomposition is
\[
V=A-2xcB+x^2c^2D,\quad
A=\sum_k f'(k)\sum_l Q^2,\quad
B=\sum_k f'(k)\sum_l Qb,\quad
D=\sum_k f'(k)\sum_l b^2.
\]
Here the snapshot's `B_decimal` and `D_decimal` represent these rational
coefficients before multiplication by \(c\) and \(c^2\). Both integer
\(A\)'s agree exactly, the rational coefficients agree to the stored
precision, and 70-digit evaluation gives
\[
\begin{split}
V_{t^2+1}(250000,49)&=8396479.996849530485497723\ldots,\\
V_{t^3+2}(250000,13)&=8245012.516153072373414919\ldots,
\end{split}
\]
matching the supplied rows. This spot check and the reproduced fits do
not constitute an audit of every production count or of the full
heuristic uncertainty calculation.

For a fixed positive \(r=Y/x\), the theorem predicts \(x^2F_f(1/r)\).
In particular, its power-main-term error, divided by
\(x^{1/2}Y^{3/2}\), is \(O_f(r^{1/8})\), which need not vanish as
\(x\) increases at fixed \(r\). This is why individual fixed-ratio
rows cannot be used as measurements of \(K_f\).

## Final theorem and comparison with the plan

Let \(f\in\mathbb Z[t]\) have degree \(d\ge1\), with
\(f(t)\ge2\) and \(f'(t)\ge1\) for real \(t\ge1\), and retain the
original variance and original weight \(f'(k)\). Set \(Y=f(y)\),
\(\eta_d=\min\{1/5,1/(4d-1)\}\), and define \(F_f\) as above and
\(K_f>0\) by (7). For every \(0<\varepsilon<\eta_d/2\), uniformly
for real \(x\ge x_0(f,\varepsilon)\), \(y\ge1\), and \(Y\le x\),
\[
\boxed{V_f(x,y)=x^2F_f(x/Y)
                 +O_{f,\varepsilon}(x^{2-\eta_d+\varepsilon})}
\]
and
\[
\boxed{V_f(x,y)=K_fx^{1/2}Y^{3/2}
 +O_{f,\varepsilon}\left(x^{3/8}Y^{13/8}
                           +x^{2-\eta_d+\varepsilon}\right).}
\]
For any fixed \(0<\delta<\eta_d/3\), choose
\(\varepsilon=\delta/2\). Dividing the second estimate by its
positive main term yields
\[
\left|\frac{V_f(x,y)}{K_fx^{1/2}Y^{3/2}}-1\right|
\ll_{f,\delta}(Y/x)^{1/8}
             +x^{3/2-\eta_d+\delta/2}Y^{-3/2}.
\]
On the range
\[
x^{1-2\eta_d/3+\delta}\le Y\le x^{1-\delta},
\]
the two terms are at most \(x^{-\delta/8}\) and \(x^{-\delta}\).
Thus the plan's claimed relative error \(O_{f,\delta}(x^{-\delta/8})\)
follows as well. In particular the lower exponents are
\(19/21+\delta\) for the quadratic and \(31/33+\delta\) for the cubic.
The range is nonempty because \(\delta<\eta_d/3\).

There are no interface mismatches and no loss relative to the chosen
plan. The two limitations already present in the plan are visible in
the budget: summing P3 caps the saving at \(1/5\), and balancing P2's
initial-modulus bound with P4's averaging error gives \(1/(4d-1)\).
No irreducibility, discriminant, content, or squarefreeness restriction
on the polynomial is added.
