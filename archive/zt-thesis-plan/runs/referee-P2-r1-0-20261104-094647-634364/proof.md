# Proof of P2

We use P1 as a black box and prove both assertions as stated. All integers counted below are positive. Put
\[
D_q(x)=\sum_{a=1}^{q}E(x;q,a)^2,\qquad
M(x)=\sum_{n\le x}\mu^2(n),\qquad
H_q=\sum_{a=1}^{q}g(q,a)^2.
\]
Constants with a subscript \(f\) depend only on the fixed polynomial, and constants with a subscript \(\varepsilon\) may also depend on the specified positive \(\varepsilon\).

## Polynomial estimates and real endpoints

There are constants \(a_f,b_f>0\) such that, for every real \(t\ge1\),
\[
f(t)\ge a_f t^d,\qquad 1\le f'(t)\le b_f t^{d-1},\qquad
\frac{f'(t)}{f(t)}\le\frac{b_f}{a_f t}.                     \tag{1}
\]
Indeed, the positive function \(f(t)/t^d\) has a positive limit, namely the leading coefficient of \(f\), and is bounded below on every compact subinterval of \([1,\infty)\). The derivative bound follows by bounding each coefficient of \(f'\) in absolute value. Also,
\[
f(t)\ge f(1)+t-1\ge t+1.                                  \tag{2}
\]
Consequently \(y\le x\) whenever \(f(y)\le x\).

Write
\[
W(z,y)=\sum_{z<k\le y}f'(k).
\]
This sum has \(N=\lfloor y\rfloor-\lfloor z\rfloor\le y\) terms. Each term is at most \(b_f y^{d-1}\); hence, before and after summing,
\[
f'(k)\le b_f y^{d-1},\qquad
0\le W(z,y)\le b_f y^d\le (b_f/a_f)Y.                    \tag{3}
\]
We also require a more accurate endpoint estimate. Set \(n=\lfloor z\rfloor\) and \(m=\lfloor y\rfloor\), so \(1\le n\le m\). For every integer \(n<k\le m\), the fundamental theorem of calculus gives
\[
\left|f'(k)-\int_{k-1}^{k}f'(t)\,dt\right|
\le\int_{k-1}^{k}|f''(t)|\,dt.
\]
There are \(m-n\) such intervals, and their interiors are disjoint. Summing their displayed errors gives
\[
\left|W(z,y)-\int_n^m f'(t)\,dt\right|
\le\int_n^m|f''(t)|\,dt.
\]
The two endpoint intervals \([n,z]\) and \([m,y]\) each have length less than one, and each contributes at most \(b_f y^{d-1}\). If \(d\ge2\), the coefficient bound \(|f''(t)|\le b'_f t^{d-2}\) gives
\[
\int_n^m|f''(t)|\,dt
\le \frac{b'_f}{d-1}y^{d-1}.
\]
If \(d=1\), this integral is zero. Combining these bounds with (1), including the case \(m=n\), proves
\[
|W(z,y)-(Y-Z)|\le K_fY^{1-1/d}                            \tag{4}
\]
for a fixed constant \(K_f\). The exponent is zero when \(d=1\).

## An elementary estimate for squarefree multiples

For an integer \(1\le u\le x\), define
\[
B_u(x)=\sum_{\substack{n\le x\\u\mid n}}\mu^2(n).
\]
We claim that
\[
|B_u(x)-xg(u,u)|\le3\tau(u)\sqrt{x/u},                     \tag{5}
\]
where \(\tau\) is the number of positive divisors. If \(u\) is not squarefree, both \(B_u(x)\) and \(g(u,u)\) vanish: the first assertion follows from a square prime divisor of \(u\), and the second follows from P1.

Suppose that \(u\) is squarefree and put \(X=x/u\ge1\). Prime factorization gives
\[
\mu^2(ub)=\mu^2(b)\boldsymbol{1}_{(b,u)=1}.
\]
Using \(\mu^2(b)=\sum_{a^2\mid b}\mu(a)\), we obtain the exact identity
\[
B_u(x)=\sum_{\substack{a\le\sqrt X\\(a,u)=1}}\mu(a)
        \sum_{\substack{b\le X/a^2\\(b,u)=1}}1.
\]
For every real \(T\ge0\), inclusion-exclusion gives
\[
\sum_{\substack{b\le T\\(b,u)=1}}1
=\sum_{v\mid u}\mu(v)\lfloor T/v\rfloor
=\frac{\phi(u)}uT+R_u(T),\qquad |R_u(T)|\le\tau(u).
\]
The sum over \(a\) has at most \(\lfloor\sqrt X\rfloor\) terms, each with error at most \(\tau(u)\). Their total error is therefore at most \(\tau(u)\sqrt X\). Completing the main sum over \(a\) to infinity incurs error at most
\[
X\frac{\phi(u)}u\sum_{a>\sqrt X}\frac1{a^2}
\le 2\sqrt X.
\]
Here \(\sum_{a>T}a^{-2}\le2/T\) for \(T\ge1\), by comparison with the integral starting at \(\lfloor T\rfloor\ge T/2\). The completed main term is
\[
X\frac{\phi(u)}u
 \prod_{p\nmid u}(1-p^{-2})
=\frac{cx}{u}\prod_{p\mid u}(1+p^{-1})^{-1}
=xg(u,u),
\]
where the last equality is exactly the squarefree-\(u\) specialization of P1. The combined error is at most \((\tau(u)+2)\sqrt X\le3\tau(u)\sqrt X\), proving (5). In particular, its specialization \(u=1\) gives
\[
|M(x)-cx|\le3\sqrt x.                                    \tag{6}
\]

## The mixed density term

For each integer \(1\le q\le x\), put
\[
A_q(x)=\sum_{a=1}^{q}g(q,a)Q(x;q,a).
\]
P1 shows that \(g(q,a)\) depends only on \((q,a)\). Partitioning the integers \(n\le x\) according to \(r=(n,q)\), followed by inclusion-exclusion, gives
\[
A_q(x)=\sum_{r\mid q}g(q,r)
       \sum_{t\mid q/r}\mu(t)B_{rt}(x).                  \tag{7}
\]
Every integer \(rt\) in this expression divides \(q\), so \(rt\le x\), as required for (5). For each pair \((r,t)\), substituting (5) into (7) gives an error of absolute value at most
\[
3g(q,r)\tau(rt)\sqrt{x/(rt)}
\le\frac{3\sqrt x}{q}\frac{\tau(rt)}{\sqrt{rt}},
\]
using \(0\le g(q,r)\le1/q\) from P1. There are
\(\sum_{r\mid q}\tau(q/r)\le\tau(q)^2\) pairs, and each satisfies
\(\tau(rt)/\sqrt{rt}\le\tau(q)\). Thus, after summing these errors,
\[
\left|A_q(x)-x\sum_{r\mid q}g(q,r)
                    \sum_{t\mid q/r}\mu(t)g(rt,rt)\right|
\le\frac{3\sqrt x}{q}\tau(q)^3.                         \tag{8}
\]

To identify this finite main coefficient without assuming an extra density identity, fix \(q\) and \(r\mid q\). Counting the integers of gcd \(r\) with \(q\) in two ways gives, for every real \(X>0\),
\[
\sum_{\substack{1\le a\le q\\(a,q)=r}}Q(X;q,a)
=\sum_{t\mid q/r}\mu(t)B_{rt}(X).
\]
Divide by \(X\) and let \(X\) tend to infinity. These are finite sums. The definition of \(g\), or (5) on the right, yields
\[
\sum_{\substack{1\le a\le q\\(a,q)=r}}g(q,a)
=\sum_{t\mid q/r}\mu(t)g(rt,rt).
\]
Multiplication by \(g(q,r)\), and then summation over the \(\tau(q)\) possible values of \(r\), is an exact finite operation. Since \(g(q,a)=g(q,r)\) in the corresponding group, (8) becomes
\[
|A_q(x)-xH_q|\le\frac{3\sqrt x}{q}\tau(q)^3.              \tag{9}
\]

We now sum (9) over the polynomial moduli. For every \(\delta>0\) there is a constant \(D_\delta\) such that
\[
\tau(q)^3\le D_\delta q^\delta.                          \tag{10}
\]
For completeness, write \(q=\prod p^{a_p}\). For every prime with \(p^\delta\ge8\),
\((a+1)^3\le8^a\le p^{\delta a}\) for \(a\ge1\). For each of the finitely many remaining primes,
\(\sup_{a\ge0}(a+1)^3p^{-\delta a}<\infty\). The product of these finitely many suprema is an admissible \(D_\delta\).

Take \(\delta=\varepsilon/2\). For a single integer \(z<k\le y\), (1), (9), (10), and \(f(k)\le x\) give
\[
f'(k)|A_{f(k)}(x)-xH_{f(k)}|
\le3D_\delta\sqrt x\,x^\delta\frac{b_f}{a_fk}.
\]
There are \(N=\lfloor y\rfloor-\lfloor z\rfloor\le y\le x\) such integers. Summing the preceding bound with its displayed \(1/k\) factor gives
\[
\begin{aligned}
\sum_{z<k\le y}f'(k)|A_{f(k)}(x)-xH_{f(k)}|
&\le3D_\delta(b_f/a_f)x^{1/2+\delta}(1+\log y)\\
&\le L_{f,\varepsilon}x^{1/2+\varepsilon}.               \tag{11}
\end{aligned}
\]
The last inequality uses \(y\le x\) and
\(1+\log x\le C_\varepsilon x^{\varepsilon/2}\) for \(x\ge2\).

## Expansion of the variance

Expanding a square gives the exact formula
\[
D_q(x)=\sum_{a=1}^{q}Q(x;q,a)^2-2xA_q(x)+x^2H_q.
\]
The first sum counts ordered pairs of squarefree integers at most \(x\) which are congruent modulo \(q\). Its diagonal has \(M(x)\) elements. Each unordered off-diagonal pair has a unique positive difference \(hq\), and its count is \(C_x(hq)\). Consequently
\[
D_q(x)=M(x)+2\sum_{1\le h\le x/q}C_x(hq)-x^2H_q
                  -2x(A_q(x)-xH_q).                    \tag{12}
\]
The sum over \(h\) has \(\lfloor x/q\rfloor\) terms and has not been approximated. In particular, an endpoint with \(hq=x\) contributes zero.

Multiply (12) by \(f'(k)\) and sum over the \(N\) integers \(z<k\le y\). The \(h\)-sum and the \(H_q\)-sum become exactly \(S_f(x;z,y)\) and \(T_f(z,y)\), respectively. The individual mixed errors and their sum were bounded in (9) and (11). Multiplication of (11) by \(2x\) therefore gives
\[
\left|V_f(x;z,y)-\left[M(x)W(z,y)+2S_f(x;z,y)-x^2T_f(z,y)\right]\right|
\le2L_{f,\varepsilon}x^{3/2+\varepsilon}.                \tag{13}
\]
Finally (3), (4), and (6) show explicitly that
\[
\begin{aligned}
|M(x)W(z,y)-cx(Y-Z)|
&\le |M(x)-cx|W(z,y)+cx|W(z,y)-(Y-Z)|\\
&\le3(b_f/a_f)\sqrt x\,Y+cK_fxY^{1-1/d}\\
&\le3(b_f/a_f)x^{3/2}+cK_fxY^{1-1/d}.                   \tag{14}
\end{aligned}
\]
Combining (13) and (14), and enlarging the constant, proves the first assertion uniformly in every stipulated range.

## Disposal of the initial moduli

The external estimate used here is Lemma 2.2 of J. Brüdern, A. Granville, A. Perelli, R. C. Vaughan and T. D. Wooley, *On the exponential sum over k-free numbers* (1998), *Philosophical Transactions of the Royal Society A* **356**, 739–761, [doi:10.1098/rsta.1998.0183](https://doi.org/10.1098/rsta.1998.0183). We use the supplied file `papers/bgpvw-1998.pdf`, manuscript page 6. Its statement is, verbatim (with mathematical typography transcribed):

> **Lemma 2.2.** Suppose that \(Q\) and \(x\) are positive real numbers, and that \(k\) is an integer with \(k\ge2\). Then for each positive number \(\varepsilon\),
> \[
> \Upsilon_k(x,Q)\ll
> \begin{cases}
> x^{2/k+\varepsilon}Q^{2-2/k},&\text{when }1\le Q\le x,\\
> Q^2\log(2Q),&\text{when }Q>x.
> \end{cases}
> \]

For clarity about normalization, the paper's definitions (2.6) and (2.7) are
\[
\sum_{\substack{1\le n\le x\\n\equiv a\pmod q}}\mu_k(n)
=\frac{x}{\zeta(k)}g_k(q,(q,a))+E_k(x;q,a),\qquad
\Upsilon_k(x,Q)=\sum_{1\le q\le Q}\sum_{a=1}^{q}|E_k(x;q,a)|^2.
                                                               \tag{15}
\]
Here \(\mu_k\) is the characteristic function of the \(k\)-free numbers. We check the density normalization from the paper's local definitions (2.1) and (2.2), rather than identifying functions by their names. For a prime \(p\mid q\), put \(L=v_p(q)\ge1\) and \(M=v_p((q,a))\), so \(0\le M\le L\). At \(k=2\), the three local cases in (2.1) are exactly
\[
p^L(1-p^{-2})g_2(p^L,p^M)=
\begin{cases}
0,&L\ge M\ge2,\\
1,&M<\min\{L,2\},\\
1-p^{L-2},&L=M<2.
\end{cases}                                                   \tag{16}
\]
These cases exhaust all \(L\ge1\), \(0\le M\le L\). The last case is precisely \(L=M=1\), with factor \(1-p^{-1}\). Thus the product rule (2.2) gives
\[
\frac{1}{\zeta(2)}g_2(q,(q,a))=
\begin{cases}
0,&\text{some }p^2\mid q\text{ also divides }a,\\
\displaystyle\frac cq\prod_{p\mid q}(1-p^{-2})^{-1}
\prod_{\substack{p\parallel q\\p\mid a}}(1-p^{-1}),&\text{otherwise}.
\end{cases}
\]
For \(q=1\) the products are empty and the value is \(c\). These values agree exactly with P1 for every \(q\) and \(a\). Accordingly \(E_2(x;q,a)=E(x;q,a)\), and the lemma implies
\[
\sum_{q\le Q}D_q(x)\le B_\varepsilon x^{1+\varepsilon}Q
\qquad(1\le Q\le x).                                      \tag{17}
\]

Here are all the hypothesis checks for its application. The lemma's integer \(k\) is set to \(2\); it is unrelated to the index of the polynomial moduli. The parameter \(x\ge2\) is a positive real number. We take \(Q=f(z)\), which is a positive real number with \(Q\ge2\) since \(z\ge1\), and satisfies \(Q\le x\) by the assumed range. Thus the first branch applies, including \(Q=x\), and its exponents specialize to \(2/k+\varepsilon=1+\varepsilon\) and \(2-2/k=1\). Its residue sum runs over all \(1\le a\le q\), exactly as in \(D_q\), without a coprimality restriction. Its arbitrary positive \(\varepsilon\) is the \(\varepsilon\) fixed in the proposition. The paper states that its implicit constants depend at most on \(k\) and \(\varepsilon\), so \(B_\varepsilon\) is independent of \(x,Q,z\).

There are \(\lfloor z\rfloor\) polynomial-modulus terms in \(V_f(x,z)\). Before summing, (1) gives, for each integer \(1\le k\le z\),
\[
0<f'(k)\le b_f z^{d-1}
\le b_f a_f^{-(d-1)/d}Q^{1-1/d}.
\]
The integers \(f(k)\) are distinct because \(f'\ge1\), and they all lie in \([1,Q]\). Every \(D_q(x)\) is nonnegative. Therefore summing these individually bounded terms, and then using (17), gives
\[
\begin{aligned}
0\le V_f(x,z)
&\le b_f a_f^{-(d-1)/d}Q^{1-1/d}
       \sum_{k\le z}D_{f(k)}(x)\\
&\le b_f a_f^{-(d-1)/d}Q^{1-1/d}\sum_{q\le Q}D_q(x)\\
&\le b_f a_f^{-(d-1)/d}B_\varepsilon
       x^{1+\varepsilon}Q^{2-1/d}.
\end{aligned}
\]
Since \(Q=f(z)\), this is the second assertion. Taking the larger of the constants obtained for the two assertions supplies a single \(C(f,\varepsilon)\) as requested.

## Source and verification notes

No numerical check was used. The quoted lemma and its normalization were checked against the supplied PDF, including a rendered image of manuscript page 6. P1 was used only as stated; no other proposition was assumed. R. C. Vaughan, *A variance for k-free numbers in arithmetic progressions* (2005), *Proceedings of the London Mathematical Society* **91**, 573–597, [doi:10.1112/S0024611505015352](https://doi.org/10.1112/S0024611505015352), was inspected in the supplied corpus to locate the mean-square lemma, but no result from it is needed in the proof.

A bibliographic search for the 1998 paper's URL also returned a search result headed as a 2013 Saratov journal issue. Reading stopped at that identification; that source was not opened and none of its results was used. No excluded author, excluded paper, GitLab material, or write-up from another run was used.
