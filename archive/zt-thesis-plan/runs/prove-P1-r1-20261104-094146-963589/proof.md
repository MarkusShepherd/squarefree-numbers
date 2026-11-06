# Proof of P1

All sums over integers below are over positive integers unless another range is specified. Write \(e(t)=\exp(2\pi i t)\), and take logarithms to base \(e\). The proof is elementary and uses no external sources or numerical checks. There are no supplied dependencies or referee objections.

We use the Euler product
\[
c=\zeta(2)^{-1}=\prod_p(1-p^{-2}).
\tag{1}
\]
Indeed, expansion of a finite product of the geometric series \((1-p^{-2})^{-1}\) gives the sum of \(m^{-2}\) over integers whose prime divisors belong to that finite set. As the finite sets exhaust the primes, these nonnegative sums increase to \(\sum_{m\ge1}m^{-2}=\zeta(2)\). This proves (1). Also \(0<c\le1\).

## The density

For every real \(t>0\), put \(N=\lfloor t\rfloor+1\). Since \(u^{-2}\) decreases on the positive real axis,
\[
\sum_{m>t}\frac1{m^2}
\le \frac1{N^2}+\int_N^\infty u^{-2}\,du
=\frac1{N^2}+\frac1N
\le\frac2N\le\frac2t.
\tag{2}
\]

The divisor identity
\[
\mu^2(n)=\sum_{m^2\mid n}\mu(m)
\tag{3}
\]
follows by factoring the right side into \(\prod_{p^2\mid n}(1-1)\): it is 1 if no prime square divides \(n\), and 0 otherwise. Fix \(q\ge1\), \(l\in\mathbb Z\), and \(x\ge1\). For \(d_m=(m^2,q)\), the congruences
\[
n\equiv0\pmod{m^2},\qquad n\equiv l\pmod q
\]
are soluble exactly when \(d_m\mid l\). In that case they specify one class modulo \([m^2,q]=qm^2/d_m\). To verify this, write \(n=m^2u\), divide the resulting congruence by \(d_m\), and use that \(m^2/d_m\) is invertible modulo \(q/d_m\).

The number of positive integers at most \(x\) in a single class modulo an integer \(M\ge1\) differs from \(x/M\) by at most 1. Applying (3) therefore gives
\[
Q(x;q,l)=\frac{x}{q}
\sum_{\substack{m\le\sqrt x\\d_m\mid l}}
\frac{\mu(m)d_m}{m^2}+E_0(x;q,l),
\qquad |E_0(x;q,l)|\le\lfloor\sqrt x\rfloor.
\tag{4}
\]
Here there are at most \(\lfloor\sqrt x\rfloor\) terms, each contributing an error of absolute value at most 1.

The infinite series obtained by extending the sum in (4) converges absolutely: \(d_m\le q\), so each absolute summand after multiplication by \(1/q\) is at most \(m^{-2}\). The error from the extension, including the factor \(x/q\), is bounded by
\[
\frac{x}{q}\sum_{m>\sqrt x}\frac{d_m}{m^2}
\le x\sum_{m>\sqrt x}\frac1{m^2}
\le2\sqrt x
\tag{5}
\]
by (2). Consequently
\[
\left|Q(x;q,l)-\frac{x}{q}
\sum_{\substack{m\ge1\\(m^2,q)\mid l}}
\frac{\mu(m)(m^2,q)}{m^2}\right|\le3\sqrt x.
\tag{6}
\]
Dividing by \(x\) and letting \(x\to\infty\) proves existence of the density and the asserted formula
\[
g(q,l)=\frac1q\sum_{\substack{m\ge1\\(m^2,q)\mid l}}
\frac{\mu(m)(m^2,q)}{m^2}.
\tag{7}
\]

For a prime \(p\), write \(d_p=(p^2,q)\). In a nonzero summand of (7), \(m\) is squarefree, and then
\[
(m^2,q)=\prod_{p\mid m}d_p,
\qquad (m^2,q)\mid l\ \Longleftrightarrow\ d_p\mid l\text{ for every }p\mid m.
\]
Absolute convergence of (7) permits the product expansion
\[
g(q,l)=\frac1q\prod_p
\left(1-\frac{d_p}{p^2}\mathbf1_{d_p\mid l}\right).
\tag{8}
\]
If \(p\nmid q\), the factor is \(1-p^{-2}\). If \(p\parallel q\), the factor is \(1-p^{-1}\) when \(p\mid l\), and 1 when \(p\nmid l\). If \(p^2\mid q\), the factor is 0 when \(p^2\mid l\), and 1 when \(p^2\nmid l\). These cases give exactly the claimed zero condition and, when there is no such zero factor,
\[
g(q,l)=\frac cq\prod_{p\mid q}(1-p^{-2})^{-1}
\prod_{\substack{p\parallel q\\p\mid l}}(1-p^{-1}).
\tag{9}
\]
Finally, \(0\le Q(x;q,l)\le x/q+1\). Taking limits after division by \(x\) gives
\[
0\le g(q,l)\le\frac1q.
\tag{10}
\]

## Finite Fourier coefficients and the quadratic identity

For \(j\in\{0,\ldots,q-1\}\), define
\[
\widehat g_q(j)=\sum_{l=1}^q g(q,l)e(-jl/q),
\qquad r=\frac q{(j,q)},
\]
where \((0,q)=q\). Interchanging (7) with this finite sum is legitimate by the absolute convergence already proved. For any \(d\mid q\),
\[
\sum_{\substack{1\le l\le q\\d\mid l}}e(-jl/q)
=\sum_{v=1}^{q/d}e\left(-\frac{jv}{q/d}\right)
=\begin{cases}q/d,&q/d\mid j,\\0,&q/d\nmid j.\end{cases}
\tag{11}
\]
The last equality follows by summing a finite geometric progression. Writing \(j=(j,q)b\), with \((b,r)=1\), shows
\[
q/d\mid j\ \Longleftrightarrow\ q\mid jd
\ \Longleftrightarrow\ r\mid d.
\]
For \(d=d_m\), the condition \(r\mid d_m\) is equivalent to \(r\mid m^2\), because \(r\mid q\). Thus (11) gives
\[
\widehat g_q(j)=\sum_{\substack{m\ge1\\r\mid m^2}}\frac{\mu(m)}{m^2}.
\tag{12}
\]
If a prime cube divides \(r\), every integer \(m\) contributing to (12) has a square prime divisor, so (12) is zero. Otherwise, each prime divisor of \(r\) must divide the squarefree integer \(m\), and every other prime is unrestricted. Expanding this absolutely convergent series into its prime factors gives
\[
\widehat g_q(j)
=\prod_{p\mid r}(-p^{-2})\prod_{p\nmid r}(1-p^{-2})
=c\prod_{p\mid r}\frac{-1}{p^2-1}
=cG(r)=\gamma(r).
\tag{13}
\]
The cube-divisor case also equals \(cG(r)\) by the definition of \(G\).

Finite Fourier inversion follows from
\(\sum_{j=0}^{q-1}e(jv/q)=q\mathbf1_{q\mid v}\). Grouping its terms by the reduced denominator \(r\mid q\) gives the additional exact identity
\[
g(q,l)=\frac1q\sum_{r\mid q}\gamma(r)c_r(l).
\tag{14}
\]
The same orthogonality identity, applied to the squared absolute value of the inverse Fourier sum, yields
\[
q\sum_{l=1}^q|g(q,l)|^2
=\sum_{j=0}^{q-1}|\widehat g_q(j)|^2.
\tag{15}
\]
There are exactly \(\varphi(r)\) indices \(j\) with reduced denominator \(r\): they are \(j=(q/r)b\) with \(b\) running through the invertible classes modulo \(r\). For \(r=1\), the sole index is \(j=0\). Since \(g\) and \(\gamma\) are real, (13)--(15) prove
\[
q\sum_{l=1}^q g(q,l)^2
=\sum_{r\mid q}\varphi(r)\gamma(r)^2
=\sum_{r\mid q}\lambda(r).
\tag{16}
\]

## Total mass and quantitative bounds

Put \(h(r)=\varphi(r)G(r)^2\), so \(\lambda(r)=c^2h(r)\). The function \(h\) is nonnegative and multiplicative, with
\[
h(p)=\frac{p-1}{(p^2-1)^2},\qquad
h(p^2)=\frac{p(p-1)}{(p^2-1)^2},\qquad
h(p^a)=0\quad(a\ge3).
\tag{17}
\]
In particular,
\[
1+h(p)+h(p^2)
=1+\frac{(p-1)(p+1)}{(p^2-1)^2}
=\frac1{1-p^{-2}}.
\tag{18}
\]
For each finite set of primes, expansion of the corresponding product of (18) equals the sum of \(h(r)\) over integers supported on that set. Nonnegativity allows passage to the increasing limit, giving, by (1),
\[
\sum_{r\ge1}\lambda(r)
=c^2\prod_p(1+h(p)+h(p^2))
=c^2\zeta(2)=c.
\tag{19}
\]

We now give explicit bounds stronger than the requested ones. For every prime \(p\ge2\),
\[
(p-1)(p+1)^2-p^3=p^2-p-1\ge1,
\]
and therefore (17) implies
\[
h(p)=\frac1{(p-1)(p+1)^2}\le p^{-3},
\qquad h(p^2)=p\,h(p)\le p^{-2}.
\tag{20}
\]
Every \(r\) with \(h(r)\ne0\) has a unique expression \(r=ab^2\), where \(a,b\) are squarefree and \((a,b)=1\). Multiplying (20) over its prime divisors gives
\[
h(ab^2)\le a^{-3}b^{-2}.
\tag{21}
\]
We may drop the squarefreeness and coprimality restrictions when taking upper bounds, since all terms are nonnegative. We will also use
\[
\sum_{a\ge1}a^{-5/2}
\le1+\int_1^\infty u^{-5/2}\,du=\frac53.
\tag{22}
\]

Fix real \(R\ge2\). For each fixed \(a\ge1\), the \(b\)-sum in the tail is infinite, starts at \(\lfloor\sqrt{R/a}\rfloor+1\), and, before summing over \(a\), satisfies by (2)
\[
a^{-3}\sum_{b>\sqrt{R/a}}b^{-2}
\le a^{-3}\frac2{\sqrt{R/a}}
=2R^{-1/2}a^{-5/2}.
\tag{23}
\]
Summing this bound over all \(a\ge1\), an infinite sum bounded by (22), gives
\[
\sum_{r>R}\lambda(r)
\le c^2\sum_{a\ge1}a^{-3}\sum_{b>\sqrt{R/a}}b^{-2}
\le\frac{10c^2}{3}R^{-1/2}.
\tag{24}
\]

For the weighted sum, multiplying (21) by \(r=ab^2\) bounds each summand \(rh(r)\) by \(a^{-2}\). For fixed \(1\le a\le\lfloor R\rfloor\), the number of \(b\)-terms is \(\lfloor\sqrt{R/a}\rfloor\), hence their sum is at most
\[
a^{-2}\lfloor\sqrt{R/a}\rfloor
\le R^{1/2}a^{-5/2}.
\tag{25}
\]
The remaining \(a\)-sum has \(\lfloor R\rfloor\) terms; applying (22) after summing (25) gives
\[
\sum_{r\le R}r\lambda(r)
\le c^2\sum_{a\le R}a^{-2}\sum_{b\le\sqrt{R/a}}1
\le\frac{5c^2}{3}R^{1/2}.
\tag{26}
\]
Since \(c^2\le1\) and \(\log(2R)\ge\log4>1\), (24) and (26) imply both requested inequalities with the same absolute constant \(C=4\).

## The Ramanujan series

By its definition as a sum of \(\varphi(r)\) complex numbers of absolute value 1,
\[
|c_r(n)|\le\varphi(r).
\]
Thus (19) proves absolute convergence, with the explicit bound
\[
\sum_{r\ge1}|\gamma(r)^2c_r(n)|
\le\sum_{r\ge1}\lambda(r)=c.
\tag{27}
\]
In fact (24) bounds the absolute tail after \(r=R\) by \((10c^2/3)R^{-1/2}\).

For coprime \(u,v\), the invertible classes modulo \(uv\) are represented uniquely by \(bv+du\), where \(b\) and \(d\) range over the invertible classes modulo \(u\) and \(v\). Factoring the exponential shows
\[
c_{uv}(n)=c_u(n)c_v(n).
\tag{28}
\]
For every prime \(p\) and integer \(a\ge1\), subtracting the sum over multiples of \(p\) from the sum over all classes modulo \(p^a\) gives
\[
c_{p^a}(n)
=p^a\mathbf1_{p^a\mid n}-p^{a-1}\mathbf1_{p^{a-1}\mid n}.
\tag{29}
\]
Both sums here are finite geometric sums. In particular,
\[
c_p(n)+c_{p^2}(n)=p^2\mathbf1_{p^2\mid n}-1.
\tag{30}
\]

The function \(r\mapsto G(r)^2c_r(n)\) is multiplicative by (28). Its series is absolutely convergent by (27), because \(c>0\). Expanding over finite prime sets and passing to the absolutely convergent limit therefore gives
\[
\sum_{r\ge1}\gamma(r)^2c_r(n)
=c^2\prod_p\left(1+
\frac{c_p(n)+c_{p^2}(n)}{(p^2-1)^2}\right).
\tag{31}
\]
To compute each factor, combine (1) and (30). When \(p^2\nmid n\),
\[
(1-p^{-2})^2\left(1-\frac1{(p^2-1)^2}\right)
=\frac{(p^2-1)^2-1}{p^4}
=1-\frac2{p^2}.
\tag{32}
\]
When \(p^2\mid n\),
\[
(1-p^{-2})^2\left(1+\frac{p^2-1}{(p^2-1)^2}\right)
=\frac{(p^2-1)^2}{p^4}\frac{p^2}{p^2-1}
=1-\frac1{p^2}.
\tag{33}
\]
These computations apply to every prime, including \(p=2\), for which all denominators are nonzero. For fixed \(n\ge1\), only finitely many primes satisfy \(p^2\mid n\). Also \(\sum_p2/p^2<\infty\), so the product of the factors in (32) converges. Taking limits of the finite products in (31)--(33) proves
\[
\begin{aligned}
\sum_{r\ge1}\gamma(r)^2c_r(n)
&=\prod_{p^2\nmid n}(1-2/p^2)
  \prod_{p^2\mid n}(1-1/p^2)\\
&=\prod_p(1-2/p^2)
  \prod_{p^2\mid n}\frac{p^2-1}{p^2-2}
=\mathfrak S(n).
\end{aligned}
\tag{34}
\]
Together, (7), (9), (10), (16), (19), (24), (26), and (34) prove all assertions. \(\square\)
