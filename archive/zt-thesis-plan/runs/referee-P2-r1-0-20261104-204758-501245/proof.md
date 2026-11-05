# Proof of P2

All counting variables are positive integers, unless stated otherwise. We use
the definitions of \(Q,g,E,V_f\) in `problem.md` and assume P1 exactly as
supplied. In particular, \(g(q,l)\) is periodic in \(l\), is real, and is the
density of squarefree integers in the indicated residue class. Constants
introduced below depend only on \(f\), or on the displayed positive error
parameter, as indicated.

**1. Polynomial weights and endpoints.** Put

\[
\alpha=1-\frac1d.
\]

There are constants \(0<A\le1\) and \(B\ge1\), depending only on \(f\), such
that, for every real \(t\ge1\),

\[
 At^d\le f(t)\le Bt^d,\qquad
 1\le f'(t)\le Bt^{d-1}.                                      \tag{1}
\]

For \(d\ge2\), enlarge \(B\) to ensure

\[
 |f''(t)|\le Bt^{d-2}\quad(t\ge1).                            \tag{2}
\]

These constants exist because the leading coefficient of \(f\) is positive,
\(f(t)/t^d\) is positive and continuous on \([1,\infty)\), and its limit at
infinity is positive. The upper bounds follow by bounding each coefficient
of the relevant polynomial. For \(d=1\), \(f''=0\).

For the interval in the proposition, write

\[
 W=\sum_{z<k\le y}f'(k),\qquad
 N=\lfloor y\rfloor-\lfloor z\rfloor.
\]

Thus this sum has exactly \(N\le y\) terms. Let \(n=\lfloor z\rfloor\) and
\(m=\lfloor y\rfloor\). For each of its \(N\) terms, the error on replacing
\(f'(k)\) by its integral over \([k-1,k]\) has absolute value at most
\(\int_{k-1}^k|f''(t)|\,dt\). After summing these \(N\) errors, their total
absolute value is at most \(\int_n^m|f''(t)|\,dt\). The two endpoint
integrals needed to replace \([n,m]\) by \([z,y]\) have lengths less than
one each. Consequently,

\[
 \left|W-\int_z^y f'(t)\,dt\right|
 \le 2\sup_{1\le t\le y}f'(t)+\int_1^y|f''(t)|\,dt
 \le 3B y^{d-1}.                                             \tag{3}
\]

For \(d\ge2\), the integral in this inequality is at most
\(B(y^{d-1}-1)/(d-1)\le By^{d-1}\). For \(d=1\), it is zero, so (3) holds
in that case as well. Since \(Y=f(y)\ge Ay^d\), the constant

\[
 K=3BA^{-\alpha}
\]

satisfies

\[
 |W-(Y-Z)|\le K Y^\alpha,\qquad
 0\le W\le(1+K)Y.                                           \tag{4}
\]

Here we used \(Y\ge2\) and \(Y^\alpha\le Y\).

We shall also use the following elementary divisor bound. If \(\tau(q)\)
denotes the number of divisors of \(q\), then for every \(\eta>0\) there is
a finite \(D_\eta\) such that

\[
 \tau(q)\le D_\eta q^\eta\quad(q\ge1).                       \tag{5}
\]

Indeed, for primes \(p\ge2^{1/\eta}\) and integers \(e\ge0\),
\(e+1\le2^e\le p^{\eta e}\). For each of the finitely many smaller primes,
\(\sup_{e\ge0}(e+1)p^{-\eta e}\) is finite. Their product gives \(D_\eta\).

**2. An elementary mixed-moment estimate.** For a positive integer \(a\),
define

\[
 N_a(x)=\sum_{\substack{n\le x\\a\mid n}}\mu^2(n),\qquad
 D_a=\sum_{r\ge1}\frac{\mu(r)}{[a,r^2]},
\]

where brackets denote the least common multiple. The series for \(D_a\)
converges absolutely because \([a,r^2]\ge r^2\). The elementary identity
\(\mu^2(n)=\sum_{r^2\mid n}\mu(r)\) gives

\[
 N_a(x)=\sum_{r\le\sqrt x}\mu(r)
              \left\lfloor\frac{x}{[a,r^2]}\right\rfloor.
\]

This \(r\)-sum has \(\lfloor\sqrt x\rfloor\) terms. Each floor replacement
has error of absolute value at most one; their total error is at most
\(\sqrt x\). The omitted part of the absolutely convergent main-term series
has absolute value at most

\[
 x\sum_{r>\sqrt x}\frac1{[a,r^2]}
 \le x\sum_{r>\sqrt x}\frac1{r^2}
 \le\frac{x}{\lfloor\sqrt x\rfloor}
 \le2\sqrt x.
\]

Thus, uniformly in \(a\ge1\) and real \(x\ge2\),

\[
 |N_a(x)-xD_a|\le3\sqrt x.                                  \tag{6}
\]

Fix a positive integer \(q\), and put

\[
 q_1=\prod_{p\parallel q}p,\qquad
 A_q=\prod_{p\mid q}(1-p^{-2})^{-1},\qquad
 H(q)=\sum_{l=1}^q g(q,l)^2.
\]

By the absolutely convergent Euler product for \(\zeta(2)\),
\(cA_q\le1\). For squarefree \(n\), the zero-density exception in P1 never
occurs, since no prime square divides \(n\). Expanding the remaining factors
in P1 therefore gives the exact identity

\[
 \mu^2(n)g(q,n)
 =\frac{cA_q}{q}\mu^2(n)
       \sum_{\substack{a\mid q_1\\a\mid n}}\frac{\mu(a)}a.
                                                                    \tag{7}
\]

Set

\[
 B(q)=\frac{cA_q}{q}\sum_{a\mid q_1}\frac{\mu(a)}aD_a.
\]

The divisor sum here has \(\tau(q_1)\le\tau(q)\) terms. Before summing, the
error contributed by a divisor \(a\), on using (6) in (7), has absolute
value at most \(3cA_q\sqrt x/(qa)\). After summing over these divisors,

\[
 \left|\sum_{n\le x}\mu^2(n)g(q,n)-xB(q)\right|
 \le\frac{3\sqrt x}{q}\sum_{a\mid q_1}\frac1a
 \le\frac{3\sqrt x}{q}\tau(q).                               \tag{8}
\]

There is no uniform-limit issue in identifying \(B(q)\). For this fixed
\(q\), periodicity gives a sum of exactly \(q\) residue classes,

\[
 \sum_{n\le t}\mu^2(n)g(q,n)
 =\sum_{l=1}^q g(q,l)Q(t;q,l).
\]

Divide by \(t\) and let \(t\to\infty\). By the definition of the densities,
the right side tends to \(H(q)\); by (8), the left side tends to \(B(q)\).
Hence \(B(q)=H(q)\). In particular, if

\[
 M(x;q)=\sum_{l=1}^q g(q,l)E(x;q,l),
\]

then (8) proves the uniform estimate

\[
 |M(x;q)|
 =\left|\sum_{n\le x}\mu^2(n)g(q,n)-xH(q)\right|
 \le\frac{3\sqrt x}{q}\tau(q).                               \tag{9}
\]

Taking \(a=1\) in (6), the Euler product
\(D_1=\sum_{r\ge1}\mu(r)/r^2=c\) also gives

\[
 \left|\sum_{n\le x}\mu^2(n)-cx\right|\le3\sqrt x.           \tag{10}
\]

**3. Exact expansion and its accumulated errors.** For every integer
\(1\le q\le x\), counting ordered pairs of squarefree integers in the same
residue class gives

\[
 \sum_{l=1}^q Q(x;q,l)^2
 =\sum_{n\le x}\mu^2(n)
     +2\sum_{1\le h\le x/q}C_x(hq).                         \tag{11}
\]

Indeed, pairs with equal coordinates contribute the first term. For a pair
with unequal coordinates, its positive difference is exactly \(hq\) for
one of the \(\lfloor x/q\rfloor\) possible positive integers \(h\). The
number of such pairs in increasing order is \(C_x(hq)\), and reversing
their order gives the factor two. These are exact finite identities,
including for nonintegral \(x\).

Since \(Q=E+xg\), expansion of the square, followed by the definition of
\(M(x;q)\), gives

\[
 \sum_{l=1}^q E(x;q,l)^2
 =\sum_{n\le x}\mu^2(n)
     +2\sum_{1\le h\le x/q}C_x(hq)
     -x^2H(q)-2xM(x;q).                                     \tag{12}
\]

Sum this identity over the \(N\) integers \(z<k\le y\), with \(q=f(k)\)
and weight \(f'(k)\). The hypotheses imply \(q\le Y\le x\). There is no
approximation in the correlation sum or in the term containing \(H(q)\).
Thus the difference asserted in the first part of P2 is exactly

\[
 R=\left(\sum_{n\le x}\mu^2(n)-cx\right)W
      +cx\bigl(W-(Y-Z)\bigr)
      -2x\sum_{z<k\le y}f'(k)M(x;f(k)).                     \tag{13}
\]

We bound each of these three errors. Before summing the diagonal error
over \(k\), its absolute value is at most \(3\sqrt x f'(k)\), by (10).
After summing its \(N\) terms, (4) gives

\[
 \left|\left(\sum_{n\le x}\mu^2(n)-cx\right)W\right|
 \le3\sqrt x W
 \le3(1+K)\sqrt x Y
 \le3(1+K)x^{3/2}.                                          \tag{14}
\]

The endpoint error in (13) satisfies

\[
 |cx(W-(Y-Z))|\le cKxY^\alpha.                              \tag{15}
\]

For the mixed error, fix the prescribed \(\varepsilon>0\) and set
\(\eta=\varepsilon/2\). Before summing over \(k\), (1), (5), (9), and
\(f(k)\le x\) give

\[
 |f'(k)M(x;f(k))|
 \le3D_\eta x^{1/2+\eta}\frac{f'(k)}{f(k)}
 \le\frac{3D_\eta B}{A}\frac{x^{1/2+\eta}}{k}.              \tag{16}
\]

There are \(N\le\lfloor y\rfloor\le A^{-1/d}x^{1/d}\) terms. Summing
the displayed reciprocal bound, rather than its maximum, yields

\[
 \sum_{z<k\le y}|f'(k)M(x;f(k))|
 \le\frac{3D_\eta B}{A}x^{1/2+\eta}(1+\log y).              \tag{17}
\]

For completeness, \(\sum_{k=1}^{\lfloor y\rfloor}1/k\le1+\log y\)
follows by bounding the terms with \(k\ge2\) by
\(\int_{k-1}^{k}dt/t\). From \(Ay^d\le x\),

\[
 1+\log y\le L\log(2x),\qquad
 L=1+\frac1d+\frac{\log(A^{-1})}{d}.
\]

The elementary maximum of \(u e^{-\eta u}\), for \(u\ge0\), gives

\[
 \log(2x)\le J_\eta x^\eta,\qquad
 J_\eta=\log2+\frac1{e\eta}\quad(x\ge2).
\]

Consequently, with \(M_{f,\varepsilon}=3D_\eta BLJ_\eta/A\), the error
before multiplication by \(2x\) in (13) is at most
\(M_{f,\varepsilon}x^{1/2+2\eta}\). After that multiplication it is at
most

\[
 2x\left|\sum_{z<k\le y}f'(k)M(x;f(k))\right|
 \le2M_{f,\varepsilon}x^{3/2+\varepsilon}.                   \tag{18}
\]

Combining (13)--(18), and using \(x^{3/2}\le x^{3/2+\varepsilon}\), proves

\[
 \left|V_f(x;z,y)
  -\{cx(Y-Z)+2S_f(x;z,y)-x^2T_f(z,y)\}\right|
 \le\bigl(3(1+K)+2M_{f,\varepsilon}\bigr)x^{3/2+\varepsilon}
       +cKxY^{1-1/d}.                                      \tag{19}
\]

This also covers \(z=y\), and intervals containing no integer \(k\).

**4. The published full-variance bound, with its normalization checked.**
We use J. Brüdern, A. Granville, A. Perelli, R. C. Vaughan and T. D.
Wooley, *On the exponential sum over k-free numbers* (1998),
*Philosophical Transactions of the Royal Society of London A* **356**,
739--761, [DOI:10.1098/rsta.1998.0183](https://doi.org/10.1098/rsta.1998.0183).
The reference is the supplied `papers/bgpvw-1998.pdf`, Lemma 2.2, on page
6 of that PDF. Its statement, quoted verbatim with its mathematical
notation typeset in LaTeX, is:

> **Lemma 2.2.** Suppose that \(Q\) and \(x\) are positive real numbers,
> and that \(k\) is an integer with \(k\ge2\). Then for each positive
> number \(\varepsilon\),
> \[
> \Upsilon_k(x,Q)\ll
> \begin{cases}
> x^{2/k+\varepsilon}Q^{2-2/k},&\text{when }1\le Q\le x,\\
> Q^2\log(2Q),&\text{when }Q>x.
> \end{cases}
> \]

The source's defining equations (2.6) and (2.7), also quoted, are

> \[
> \sum_{\substack{1\le n\le x\\n\equiv a\pmod q}}\mu_k(n)
> =\frac{x}{\zeta(k)}g_k(q,(q,a))+E_k(x;q,a),                 \tag{2.6}
> \]
> \[
> \Upsilon_k(x,Q)=\sum_{1\le q\le Q}\sum_{a=1}^q
>                          |E_k(x;q,a)|^2.                  \tag{2.7}
> \]

Here \(\mu_k\) is the source's characteristic function of the \(k\)-free
integers; its \(k\) is the power parameter, independent of our polynomial
index. In particular, \(\mu_2=\mu^2\).

We check the density normalization without assuming any formula for the
source's \(g_k\). Fix positive integers \(q,a\), with \(1\le a\le q\), and
apply the quoted lemma with power parameter \(k=2\), \(Q=q\), error
parameter \(1/2\), and real \(t\ge\max\{2,q\}\) in place of \(x\).
These are positive real \(Q,t\), an integer power parameter at least two,
a positive error parameter, and \(1\le Q\le t\), as required. Since each
term of (2.7) is nonnegative, the lemma implies, for a constant \(B_{1/2}\),

\[
 |E_2(t;q,a)|^2\le B_{1/2}t^{3/2}q,\qquad
 \frac{|E_2(t;q,a)|}{t}
       \le B_{1/2}^{1/2}q^{1/2}t^{-1/4}\longrightarrow0.
\]

Dividing (2.6) by \(t\) therefore shows that

\[
 c\,g_2(q,(q,a))
 =\lim_{t\to\infty}\frac{Q(t;q,a)}t=g(q,a).
\]

Thus \(E_2(x;q,a)=E(x;q,a)\) exactly, and the source's sum (2.7) is

\[
 U(x,Q):=\sum_{1\le q\le Q}\sum_{a=1}^q E(x;q,a)^2.
\]

The inner sum includes every residue class, including the classes not
coprime to \(q\); there is no missing coprimality restriction. With power
parameter \(2\), the exponents in the lemma's first branch are

\[
 \frac22+\varepsilon=1+\varepsilon,\qquad
 2-\frac22=1.
\]

It follows that for each \(\varepsilon>0\) there is \(B_\varepsilon\)
such that

\[
 U(x,Q)\le B_\varepsilon x^{1+\varepsilon}Q
       \qquad(1\le Q\le x).                                \tag{20}
\]

The statement was checked both in the text extraction and in a rendered
image of the relevant supplied PDF page.

**5. Disposal of the initial moduli.** Let \(z\ge1\) be real, set
\(Z=f(z)\le x\), and use the definition \(V_f(x,z)\) in `problem.md`.
For each of the \(\lfloor z\rfloor\) indices in this sum, (1) gives the
weight bound

\[
 0<f'(k)\le Bz^{d-1}\le BA^{-\alpha}Z^\alpha.                \tag{21}
\]

Moreover, \(f'(t)\ge1\) implies
\(f(k+1)-f(k)=\int_k^{k+1}f'(t)\,dt\ge1\). Hence the integers \(f(k)\)
are distinct positive moduli, and all those with \(k\le z\) are at most
\(Z\). Each residue-class variance is nonnegative. Before summing in \(k\),
(21) bounds its weighted value by \(BA^{-\alpha}Z^\alpha\) times the
corresponding unweighted variance. After summing its \(\lfloor z\rfloor\)
terms and enlarging to the \(\lfloor Z\rfloor\) possible positive moduli,
we obtain

\[
 0\le V_f(x,z)
 \le BA^{-\alpha}Z^\alpha
       \sum_{1\le q\le Z}\sum_{l=1}^q E(x;q,l)^2
 =BA^{-\alpha}Z^\alpha U(x,Z).                              \tag{22}
\]

To apply (20) here, \(x\ge2\) is positive, \(Q=Z=f(z)\ge2\) is a
positive real number, \(1\le Q\le x\) is part of the present hypotheses,
the power parameter is the integer \(2\ge2\), and the error parameter is
the prescribed \(\varepsilon>0\). These check every hypothesis of the
quoted lemma for this application. Equations (20) and (22) yield

\[
 0\le V_f(x,z)
 \le BA^{-\alpha}B_\varepsilon
       x^{1+\varepsilon}Z^{1+\alpha}
 =BA^{-\alpha}B_\varepsilon
       x^{1+\varepsilon}f(z)^{2-1/d}.                        \tag{23}
\]

Taking a common constant larger than the constants in (19) and (23)
proves both assertions of P2, uniformly in all the stated ranges.

**Source and verification notes.** R. C. Vaughan, *A variance for k-free
numbers in arithmetic progressions* (2005), *Proceedings of the London
Mathematical Society* (3) **91**, 573--597,
[DOI:10.1112/S0024611505015352](https://doi.org/10.1112/S0024611505015352),
was consulted as a bibliographical pointer to the 1998 lemma. The estimate
used in the proof is the verbatim lemma quoted above from the supplied
1998 paper. A bibliographical web search returned post-2010 sources;
reading stopped when their dates were identified, and their content was
excluded from the argument.

A Python sanity check tested (9) and the exact identity (12) for all
integers \(1\le q\le\lfloor x\rfloor\), with
\(x\in\{2,3.25,10,31.75,100,200.5\}\), comprising 346 pairs \((x,q)\).
It used direct squarefree counts and the density formula of P1. Identity
(12) agreed within floating-point tolerance, and every test satisfied
(9). These computations serve only as checks; the proofs of (9) and
(12) are the finite identities and inequalities above.
