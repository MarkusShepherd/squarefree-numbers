# Assembly verdict

**The passed propositions compose and prove the chosen plan's full theorem.**
There is no loss of range, uniformity, polynomial class, weight, or error term
relative to `plan.json`. In particular, the constant-main-term formula below
is an error bound throughout $2\le Y=f(y)\le x$; it is an asymptotic only
when its errors are smaller than its main term. No asymptotic with constant
$C_f$ is claimed at a fixed positive ratio $Y/x$.

This audit uses the supplied local statements and proofs and `results.json`.
No external literature was searched, opened, or used, and no excluded source
or additional post-2010 source was consulted. There are consequently no
external sources to cite. Reproducible numerical calculations are in
`audit_numerics.py`, with output in `numerics_audit.json`.

## 1. Common notation and the constant

Fix $f\in\mathbb Z[t]$ of degree $d\ge1$, satisfying $f(t)\ge2$ and
$f'(t)\ge1$ for every real $t\ge1$. Put

\[
Y=f(y),\qquad F(t)=f'(t)f(t)^{1/2},\qquad
\rho(m)=\#\{a\bmod m:f(a)\equiv0\pmod m\}.
\]

Use the following three local factors, named $a_p,b_p,c_p$ here to avoid
confusing a local factor with the periodic function $B$:

\[
\begin{split}
a_p&=1-3p^{-2}+2p^{-3},\\
b_p&=\frac{(p-1)(p^2-2+\sqrt p)}{p^3},\\
c_p&=\frac{(p-1)^2(p+1)}{p^3}.
\end{split}
\]

Then P6 and P8 use exactly the same functions and constants:

\[
\begin{split}
I&=-4\zeta(-1/2)=0.831544899909418264\ldots,\\
h(q)&=I\prod_{p\nmid q}a_p\prod_{p\parallel q}b_p
                 \prod_{p^2\mid q}c_p,\\
\tau_p&=a_p\left(1-\frac{\rho(p)}p\right)
       +b_p\left(\frac{\rho(p)}p-\frac{\rho(p^2)}{p^2}\right)
       +c_p\frac{\rho(p^2)}{p^2},\\
C_f&=\frac23 I\prod_p\tau_p.
\end{split} \tag{1}
\]

By P8(0), this product converges absolutely and $0<C_f<\infty$.
The factor $2/3$ occurs once, from integration of the weight:

\[
\int_1^y f'(t)f(t)^{1/2}\,dt
=\frac23\bigl(Y^{3/2}-f(1)^{3/2}\bigr).
\tag{2}
\]

The factors in $\tau_p$ are the probabilities of $p\nmid f(k)$,
$p\parallel f(k)$, and $p^2\mid f(k)$, respectively. In particular,
$\rho(p^2)$ is a **root count**, and is divided by $p^2$, not by $p$.
Content primes are allowed; P8 handles their finite exceptional set.

## 2. Exact cancellation and every per-modulus error

For clarity define all terms in P2:

\[
\begin{gathered}
A_0=\prod_p(1-2/p^2),\qquad
\eta(t)=\mu^2(t)\prod_{p\mid t}(p^2-2)^{-1},\\
m_t(q)=\frac{t^2}{(t^2,q)},\qquad B(u)=\{u\}(1-\{u\}),\\
\operatorname{MT}(x;q)=A_0q\sum_{t\ge1}\eta(t)m_t(q)
                         B\left(\frac{x}{qm_t(q)}\right),\\
Q(x)=\sum_{n\le x}\mu^2(n),\qquad
C_x(m)=\sum_{1\le n\le x-m}\mu^2(n)\mu^2(n+m),\\
A(m)=A_0\sum_{t^2\mid m}\eta(t),\qquad
D_x(m)=C_x(m)-A(m)(x-m),\\
S_2(q)=\sum_{l=1}^q g(q,l)^2.
\end{gathered}
\]

The MT series converges absolutely by $B(u)\le u$ and P1(v).
Opening the square and counting ordered pairs gives

\[
V(x;q)=Q(x)+2\sum_{1\le h\le x/q}C_x(hq)
              -x^2S_2(q)-2x\sum_{l=1}^qg(q,l)E(x;q,l).
\tag{3}
\]

The pair factor 2 is necessary: each positive shift represents both orders.
The identity

\[
2\sum_{j\le T}(T-j)=T^2-T+B(T)
\]

and P1(iv),(v) imply

\[
\begin{split}
2\sum_{h\le x/q}A(hq)(x-hq)
&=\frac{A_0x^2}{q}\sum_t\frac{\eta(t)}{m_t(q)}
  -A_0x\sum_t\eta(t)+\operatorname{MT}(x;q)\\
&=x^2S_2(q)-\frac{6x}{\pi^2}+\operatorname{MT}(x;q).
\end{split} \tag{4}
\]

Thus the $x^2S_2(q)$ terms cancel exactly; the remaining diagonal is
$Q(x)-6x/\pi^2$, with no uncancelled term of order $x$. This is P2:

\[
V(x;q)=\operatorname{MT}(x;q)
 +2\sum_{h\le x/q}D_x(hq)
 +\left(Q(x)-\frac{6x}{\pi^2}\right)
 -2x\sum_lg(q,l)E(x;q,l).
\tag{5}
\]

Fix a small exponent $\theta>0$, and suppose $x\ge2$, $1\le q\le x$.
The three errors in (5), kept separate, are:

| Origin | Bound | Validity check |
|---|---|---|
| P3, pair errors | $O_\theta(x^{5/3+\theta}/q)$ | Every shift $m=hq$ is an integer in $[1,x]$; at most $x/q$ shifts |
| P4(i), diagonal | $O(x^{1/2})$ | $x\ge2\ge1$ |
| P4(ii), density cross term | $O(x^{3/2}/q)$ | Multiply the stated $O(x^{1/2}/q)$ by $2x$ |

Consequently,

\[
V(x;q)=\operatorname{MT}(x;q)
 +O_\theta\left(\frac{x^{5/3+\theta}}q+x^{1/2}
                         +\frac{x^{3/2}}q\right).
\tag{6}
\]

The last error can be absorbed in the first, which recovers P7(i).
It has not been mistaken for an error of size $x^{1/2}/q$.

For the other branch, P5 gives P6 with the same $I$ and local factors
in (1). To check the uniformity explicitly, write squarefree $t=uv$,
where $u\mid\operatorname{rad}(q)$, $(v,q)=1$, and put
$M_u=u^2/(u^2,q)$. Then

\[
\operatorname{MT}(x;q)=A_0q\sum_{u\mid\operatorname{rad}(q)}\eta(u)M_u
 \sum_{(v,q)=1}\kappa(v)B\left(\frac{x/(qM_u)}{v^2}\right).
\]

Here $Z=x/(qM_u)>0$ may be smaller than 1. P5(c) explicitly covers
**all** positive $Z$, so its use is legitimate. Its total error is

\[
\begin{split}
O_\theta\left(q^{1+\theta}
 \sum_{u\mid\operatorname{rad}(q)}\eta(u)M_u
          \left(\frac{x}{qM_u}\right)^{1/3}\right)
&=O_\theta\left(x^{1/3}q^{2/3+\theta}
 \sum_{u\mid\operatorname{rad}(q)}\eta(u)M_u^{2/3}\right)\\
&=O_\theta(x^{1/3}q^{2/3+\theta}).
\end{split} \tag{7}
\]

Indeed $M_p=p$ at $p\parallel q$, and $M_p=1$ at $p^2\mid q$.
The finite sum in (7) is bounded by the convergent product
$\prod_p(1+p^{2/3}/(p^2-2))$, independently of $q$.
The main coefficient before simplifying is

\[
A_0\delta_q I\prod_{p\mid q}\left(1+\frac{\sqrt{M_p}}{p^2-2}\right),
\]

whose local factors are exactly $a_p,b_p,c_p$. Hence P6 reads

\[
\operatorname{MT}(x;q)=h(q)\sqrt{xq}
                   +O_\theta(x^{1/3}q^{2/3+\theta}).
\tag{8}
\]

Combining (6) and (8) gives, before absorbing any error,

\[
V(x;q)=h(q)\sqrt{xq}
 +O_\theta\left(x^{1/3}q^{2/3+\theta}
 +\frac{x^{5/3+\theta}}q+x^{1/2}+\frac{x^{3/2}}q\right).
\tag{9}
\]

This recovers P7(ii) after the same absorption.

## 3. Weighted assembly, with exponent bookkeeping

For $x\ge2$, real $y\ge1$, and $Y=f(y)\le x$, monotonicity gives

\[
2\le f(k)\le Y\le x\quad(1\le k\le y),\qquad f'(k)>0.
\tag{10}
\]

Thus all applications of P3, P4, P6, and P7 made above have their stated
ranges and uniform constants. Put $L=1+\log Y$. P8(b),(c) state

\[
\sum_{k\le y}\frac{f'(k)}{f(k)}\ll_f L,
\qquad \sum_{k\le y}f'(k)\ll_f Y.
\tag{11}
\]

Multiplying (6) by $f'(k)$, at $q=f(k)$, and summing gives the
unabsorbed exact-shape error

\[
V_f(x,y)=\sum_{k\le y}f'(k)\operatorname{MT}(x;f(k))
 +O_{f,\theta}\left(x^{5/3+\theta}L+x^{1/2}Y+x^{3/2}L\right).
\tag{12}
\]

For any target $\varepsilon>0$, choose $\theta=\varepsilon/3$ and use
$L\ll_\varepsilon x^{\varepsilon/3}$, since $Y\le x$. The first term is
$O(x^{5/3+2\varepsilon/3})$, and the last is smaller than
$O(x^{5/3+\varepsilon})$. Thus

\[
\boxed{\displaystyle
V_f(x,y)=\sum_{k\le y}f'(k)\operatorname{MT}(x;f(k))
 +O_{f,\varepsilon}(x^{5/3+\varepsilon}+x^{1/2}Y).}
\tag{13}
\]

Alternatively sum (9). The errors, including the averaging step P8(a), are
all displayed here:

| Origin | Error after weighting and summing |
|---|---|
| P6 sawtooth approximation | $O_{f,\theta}(x^{1/3}Y^{5/3+\theta})$ |
| P3 pair correlations | $O_{f,\theta}(x^{5/3+\theta}L)$ |
| P4(i) diagonal | $O_f(x^{1/2}Y)$ |
| P4(ii) cross term | $O_f(x^{3/2}L)$ |
| P8(a) average of $h(f(k))$ | $O_{f,\theta}(x^{1/2}Y^{3/2+\theta}y^{-1/2})$ |

The first line uses $f(k)\le Y$ and (11), rather than an unstated
estimate for a weighted polynomial sum. The main sum is exactly

\[
\sqrt x\sum_{k\le y}F(k)h(f(k))
=C_fx^{1/2}Y^{3/2}
 +O_{f,\theta}(x^{1/2}Y^{3/2+\theta}y^{-1/2}).
\]

Write $f(t)=\sum_{j=0}^d a_jt^j$ and $A_f=\sum_j|a_j|$. Since
$Y\le A_fy^d$,

\[
y^{-1/2}\le A_f^{1/(2d)}Y^{-1/(2d)}. \tag{14}
\]

With $\theta=\varepsilon/3$, use $Y^\theta\le x^\theta$,
$L\ll_\varepsilon x^{\varepsilon/3}$, and (14). The five errors become

\[
\begin{array}{ll}
x^{1/3}Y^{5/3+\theta}
 &\le x^{1/3+\varepsilon/3}Y^{5/3},\\
x^{5/3+\theta}L
 &\ll_\varepsilon x^{5/3+2\varepsilon/3},\\
x^{1/2}Y
 &\le x^{1/2}Y^{3/2-1/(2d)},\\
x^{3/2}L
 &\ll_\varepsilon x^{3/2+\varepsilon/3}
 \le O_\varepsilon(x^{5/3+\varepsilon}),\\
x^{1/2}Y^{3/2+\theta}y^{-1/2}
 &\ll_f x^{1/2+\varepsilon/3}Y^{3/2-1/(2d)}.
\end{array}
\tag{15}
\]

The inequality on the third line holds also for $d=1$, when the power of
$Y$ on the right is exactly 1. Enlarging the epsilon powers to the
prescribed ones proves

\[
\boxed{\displaystyle
V_f(x,y)=C_fx^{1/2}Y^{3/2}
 +O_{f,\varepsilon}\left(
 x^{1/3+\varepsilon}Y^{5/3}
 +x^{5/3+\varepsilon}
 +x^{1/2+\varepsilon}Y^{3/2-1/(2d)}\right).}
\tag{16}
\]

This proves P9 directly from its dependencies, rather than relying on
P9 as an additional assumption. Real endpoints and $y=1$ are covered by
P8 as stated; no replacement of $f(y)$ by $f(\lfloor y\rfloor)$ is needed.

## 4. Asymptotic range and final theorem

Take $0<\delta<1/9$,
$x^{7/9+\delta}\le Y\le x^{1-\delta}$, and choose

\[
\varepsilon_* = \min(\delta/12,1/(9d)),\qquad
\eta_* = \min(\delta/12,1/(6d)).
\]

After division by $x^{1/2}Y^{3/2}$, the three errors of (16) are

\[
\begin{split}
x^{-1/6+\varepsilon_*}Y^{1/6}
 &\le x^{-\delta/6+\varepsilon_*}
 \le x^{-\delta/12},\\
x^{7/6+\varepsilon_*}Y^{-3/2}
 &\le x^{-3\delta/2+\varepsilon_*}
 \le x^{-17\delta/12},\\
x^{\varepsilon_*}Y^{-1/(2d)}
 &\le x^{\varepsilon_*-7/(18d)-\delta/(2d)}
 \le x^{-5/(18d)}
 \le x^{-1/(6d)}.
\end{split} \tag{17}
\]

Each is $O(x^{-\eta_*})$. Positivity of $C_f$ allows the relative form

\[
\boxed{\displaystyle
V_f(x,y)=C_fx^{1/2}f(y)^{3/2}
 \left(1+O_{f,\delta}(x^{-\eta_*})\right),\qquad
\eta_*=\min(\delta/12,1/(6d)).}
\tag{18}
\]

**Final theorem:** Under exactly the polynomial and weight hypotheses in
`problem.md`, formulas (13) and (16) hold uniformly for every real
$x\ge2,y\ge1$ with $f(y)\le x$, with $C_f$ given by (1) and MT as
defined above. Formula (18) holds uniformly in the indicated range for
every fixed $0<\delta<1/9$. These are exactly all parts of the plan's
main theorem.

The principal lower-range limitation is the accumulated P3 bound
$x^{5/3+\varepsilon}(1+\log Y)$, which requires $Y$ above
$x^{7/9}$ by a power. The upper-range limitation comes from P6, whose
relative error is $x^\varepsilon(Y/x)^{1/6}$. P8 contributes the degree
dependent error $x^{1/2+\varepsilon}Y^{3/2-1/(2d)}$.
These limitations are already present in the plan; assembly adds no loss.

## 5. Interface audit

There are **no operative interface mismatches**.

| Interface | Check |
|---|---|
| P1 to P2 | The second moment and total $\eta$-mass are identical, including factors $q^{-1}$ and $A_0$; both cancellations are exact |
| P2 to P3 | Only integer shifts $1\le hq\le x$ occur; the P3 constant is independent of the shift |
| P2 to P4 | $q\le x$ holds; the cross term retains its factor $2x$ |
| P5 to P6 | Both $q^\theta$ uniformity and all $Z>0$ are supplied, including $Z<1$ |
| P6 to P7 | Same MT, same $h(q)$, and same $x,q$ ranges |
| P7 to polynomial sum | Integer $q=f(k)\in[2,x]$, positive weights, and a constant uniform in $q$ |
| P8 to P9 | Exactly the specified $F=f'\sqrt f$, real $y\ge1$, root counts, and polynomial hypotheses; (14) gives the stated degree dependence |
| Epsilon bookkeeping | Apply dependencies with smaller positive exponents before absorbing $1+\log Y$ and $Y^\theta$ |

One nonoperative typo occurs in the final numerical sanity-check paragraph
of `props/P8/proof.md`: it writes $\rho(p^2)\approx\rho(p)/p$ and calls
this exact at good primes. With the root-count notation this should be
$\rho(p^2)=\rho(p)$; equivalently, the **density**
$\rho(p^2)/p^2$ is $1/p$ times $\rho(p)/p$. This paragraph is not
used in the proof or composition. The numerical calculation here uses the
correct counts and explicitly checks exceptional primes.

## 6. Independent constants and comparison with results.json

For $f(t)=t^2+1$, the pairs $\bigl(\rho(p),\rho(p^2)\bigr)$ are

\[
\begin{cases}
(1,0),&p=2,\\
(2,2),&p\equiv1\pmod4,\\
(0,0),&p\equiv3\pmod4.
\end{cases} \tag{19}
\]

For $f(t)=t^3+2$, they are

\[
\begin{cases}
(1,0),&p=2\text{ or }3,\\
(1,1),&p>3,\ p\equiv2\pmod3,\\
(3,3),&p>3,\ p\equiv1\pmod3,\ (-2)^{(p-1)/3}\equiv1\pmod p,\\
(0,0),&\text{otherwise}.
\end{cases} \tag{20}
\]

The cube map is a bijection for $p\equiv2\pmod3$; when
$p\equiv1\pmod3$, a nonzero cubic residue has three cube roots.
For all nonexceptional primes in (19),(20), each root is simple. Indeed,
expansion $f(a+pt)\equiv f(a)+ptf'(a)\pmod{p^2}$ gives precisely one
root lift when $f'(a)\not\equiv0\pmod p$. Direct enumeration checks
the exceptional pairs, and the script enumerates residues modulo $p$
and $p^2$ for every prime $p\le100$ to check both formulas.

The product (1) was evaluated through every prime $p\le10^7$. Some
successive partial products, including the factor $2I/3$, are:

| Prime cutoff | $t^2+1$ | $t^3+2$ |
|---|---:|---:|
| $10^3$ | 0.1381524607 | 0.1356755959 |
| $10^4$ | 0.1380880269 | 0.1356128197 |
| $10^5$ | 0.1380830682 | 0.1356079540 |
| $10^6$ | 0.1380826630 | 0.1356075551 |
| $10^7$ | 0.1380826288 | 0.1356075216 |

The tail can be bounded without assuming a distribution of primes. From
the displayed local factors, $b_p<a_p<1$ and $c_p<b_p$; thus
$0<\tau_p<1$ for these polynomials. P8's elementary bound gives
$1-\tau_p\le K/p^2$, where $K=3+2d$. For $N=10^7$,

\[
0\le-\log\prod_{p>N}\tau_p
 \le\frac{K}{1-K/N^2}\sum_{p>N}p^{-2}
 \le\frac{8K}{1-K/N^2}
       \left(\frac1{30N}+\frac1{N^2}\right).
\tag{21}
\]

For the last inequality, every tail prime is coprime to 30. There are eight
reduced residue classes modulo 30. In each, if the first integer above
$N$ is $n_0$, its reciprocal-square tail is at most
$n_0^{-2}+(30n_0)^{-1}\le N^{-2}+(30N)^{-1}$ by the decreasing-integral
bound.

This gives the following deliberately outward-rounded intervals
(the rounding allowance is much larger than floating point summation
error):

\[
\begin{split}
0.1380826030&<C_{t^2+1}<0.1380826290,\\
0.1356074889&<C_{t^3+2}<0.1356075217.
\end{split} \tag{22}
\]

In particular, the predicted main terms, to the precision needed by the
data, are

\[
\begin{split}
C_{t^2+1}x^{1/2}(y^2+1)^{3/2}
 &\approx0.1380826\,x^{1/2}(y^2+1)^{3/2},\\
C_{t^3+2}x^{1/2}(y^3+2)^{3/2}
 &\approx0.1356075\,x^{1/2}(y^3+2)^{3/2}.
\end{split} \tag{23}
\]

in the proved asymptotic range. The powers are $x^{1/2}Y^{3/2}$, so the
fixed-ratio total exponent is 2.

The requested comparison is with `constant_extrapolated`, not any single
fixed-ratio row. Define signed relative discrepancy as

\[
\Delta=\frac{C_{\rm predicted}-C_{\rm extrapolated}}
                   {C_{\rm extrapolated}}.
\]

| Polynomial | Predicted $C_f$ | Extrapolated constant | Reported heuristic uncertainty | Relative discrepancy |
|---|---:|---:|---:|---:|
| $t^2+1$ | 0.1380826 | 0.1344747055 | 0.0072849586 | $+2.683\%$ |
| $t^3+2$ | 0.1356075 | 0.1363212568 | 0.0024036061 | $-0.524\%$ |

The rigorous truncation allowance in (21) changes either percentage by
less than $0.0001$ percentage points. Using the $10^7$ partial products,
the differences are $+0.0036079233$ and $-0.0007137353$, or 0.4953 and
0.2969 times the respective reported uncertainty. These uncertainties are
heuristic envelopes, not confidence intervals or rigorous bounds.
There is no clean-factor discrepancy.

Both the analytic normalization and numerical construction were checked:

* The pair-counting factor 2, $I=-4\zeta(-1/2)$, and integration factor
  $2/3$ are accounted for separately above; the exceptional local root
  counts are checked independently.
* All normalizations $V/(x^{1/2}f(y)^{3/2})$ in the two polynomials'
  production rows were recomputed; their largest relative difference from
  the saved normalization is $2.23\times10^{-16}$.
* The reported unweighted fits $N(r)=C+a\sqrt r+br$ were repeated using
  the eight largest $x$ rows, the selected cutoff $r\ge0.01$, and the
  **actual** ratios. They reproduce the saved coefficients and intercept
  standard errors to within $10^{-12}$. The coefficients are
  $(0.13447470549221466,0.05829819823814369,-0.020881393324478102)$
  and
  $(0.13632125683949853,0.037554586806314995,-0.006861994814706394)$.
* The original numerical source code is not present. An independent
  direct squarefree sieve and residue-class enumeration reproduced all
  eight production rows for each polynomial at $x=250000$. For each
  modulus, the density was constructed from its local factors:
  $g=(6/\pi^2)q^{-1}\prod_{p\mid q}(1-p^{-2})^{-1}$, multiplied by
  $1-1/p$ on classes divisible by $p\parallel q$, and set to zero on
  classes divisible by $p^2\mid q$. Summing the squared errors with
  weights $2k$ or $3k^2$ matched the saved variances with maximum
  relative differences $6.67\times10^{-16}$ and $2.23\times10^{-16}$.
  All 16 weighted integer sums of $Q^2$ matched exactly. This is an
  independent check of representative raw counts and density terms;
  it is not a rerun of the largest production size.

At fixed positive $Y/x$, the P6 error need not decrease relative to the
main term, which explains why a fixed-ratio row is not an estimator of
$C_f$ by itself. The square-root extrapolation model is an empirical
choice in `results.json`; the passed propositions establish the weaker
power bound displayed in (17), not an exact expansion in $\sqrt{Y/x}$.
The extrapolated evidence is consistent with the constants above, within
its stated limitations, and does not constitute an additional proof.
