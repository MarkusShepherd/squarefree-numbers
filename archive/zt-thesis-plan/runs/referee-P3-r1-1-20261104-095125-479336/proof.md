# Proof of P3

We prove the stronger estimate
\[
\left|C_x(m)-(x-m)\mathfrak S(m)\right|
\le B_\varepsilon x^{2/3+\varepsilon}
\qquad (x\ge2,\ 1\le m\le x),
\tag{1}
\]
where \(m\) is an integer and \(B_\varepsilon\) depends only on
\(\varepsilon>0\). No published result is needed; in particular, no
circle-method estimate is assumed.

Put \(X=x-m\) and \(H=\lfloor x^{1/3}\rfloor\). All sums over \(n\) below
are over integers, even when their upper limits are real. Thus \(X\ge0\),
\(H\ge1\), and
\[
\frac12x^{1/3}\le H\le x^{1/3}.
\tag{2}
\]
Indeed, \(\lfloor t\rfloor\ge t/2\) for every real \(t\ge1\).

## 1. An elementary divisor bound

For \(\delta>0\), define the finite constant
\[
K_\delta=\prod_{p<2^{1/\delta}}(1-p^{-\delta})^{-2},
\tag{3}
\]
where an empty product is \(1\). We will use
\[
\tau(k)\le K_\delta k^\delta\qquad(k\ge1).
\tag{4}
\]
To prove it, write \(k=\prod_p p^{a_p}\). If
\(p\ge2^{1/\delta}\), the inequality \(a+1\le2^a\), valid for every
integer \(a\ge0\), gives
\((a+1)p^{-\delta a}\le1\). If \(p<2^{1/\delta}\), then
\[
(a+1)p^{-\delta a}
\le\sum_{j=0}^\infty(j+1)p^{-\delta j}
=(1-p^{-\delta})^{-2}.
\]
Multiplication over the prime factors of \(k\) proves (4).

## 2. Truncating the two square-divisor sums

For a positive integer \(k\), let
\[
A_H(k)=\sum_{\substack{d\le H\\d^2\mid k}}\mu(d),
\qquad
R_H(k)=\sum_{\substack{d>H\\d^2\mid k}}1.
\]
The exact identity
\[
\mu^2(k)=\sum_{d^2\mid k}\mu(d)
\tag{5}
\]
follows by factoring the sum into \(\prod_{p^2\mid k}(1-1)\): it is
\(1\) when no prime square divides \(k\), and \(0\) otherwise. Consequently,
\[
|\mu^2(k)-A_H(k)|\le R_H(k),\qquad
|A_H(k)|\le\tau(k).
\tag{6}
\]

We first bound the total discarded count. The outer sum in
\(\sum_{k\le x}R_H(k)\) has \(\lfloor x\rfloor\) terms. Reversing the
finite sums gives
\[
\sum_{k\le x}R_H(k)
=\sum_{H<d\le\sqrt{x}}\left\lfloor\frac{x}{d^2}\right\rfloor
\le x\sum_{d>H}\frac1{d^2}
\le\frac{x}{H}.
\tag{7}
\]
Here there are \(\max(0,\lfloor\sqrt{x}\rfloor-H)\) terms before
extending the \(d\)-sum; each is at most \(x/d^2\). The last inequality
uses \(\sum_{d>H}d^{-2}\le\int_H^\infty t^{-2}\,dt=H^{-1}\).

For \(1\le n\le X\), both \(n\) and \(n+m\) belong to
\([1,x]\). The exact decomposition
\[
\begin{split}
\mu^2(n)\mu^2(n+m)-A_H(n)A_H(n+m)
={}&(\mu^2(n)-A_H(n))\mu^2(n+m)\\
&+A_H(n)(\mu^2(n+m)-A_H(n+m))
\end{split}
\]
and (4), (6) imply the pointwise bound
\[
\left|\mu^2(n)\mu^2(n+m)-A_H(n)A_H(n+m)\right|
\le R_H(n)+K_\delta x^\delta R_H(n+m).
\]
There are \(\lfloor X\rfloor\) terms in the \(n\)-sum. Each of the maps
\(n\mapsto n\) and \(n\mapsto n+m\) is injective into the positive
integers at most \(x\). Therefore (7) bounds each of the two sums of
\(R_H\) by \(x/H\), and
\[
C_x(m)=\sum_{n\le X}A_H(n)A_H(n+m)+E_1,
\qquad
|E_1|\le(1+K_\delta x^\delta)\frac{x}{H}.
\tag{8}
\]
This remains valid for \(0\le X<1\), when both \(n\)-sums are empty.

## 3. Counting the truncated congruences

For \(1\le d,e\le H\), put \(g=\gcd(d,e)\). The congruences
\[
n\equiv0\pmod{d^2},\qquad n\equiv-m\pmod{e^2}
\tag{9}
\]
are compatible if and only if \(g^2\mid m\). For completeness, necessity
follows by subtracting the congruences. For sufficiency, write
\(d=ga\), \(e=gb\), with \(\gcd(a,b)=1\). Substitution of \(n=d^2t\)
reduces (9) to
\[
a^2t\equiv-m/g^2\pmod{b^2},
\]
which has exactly one residue class of solutions for \(t\) modulo
\(b^2\), because \(a^2\) is invertible modulo \(b^2\). Hence (9)
defines one residue class modulo
\[
L=d^2b^2=\frac{d^2e^2}{g^2}.
\]
The count of positive integers in one residue class modulo \(L\) up to
any real \(X\ge0\) differs from \(X/L\) by at most \(1\). Explicitly,
choose its representative \(r\) with \(1\le r\le L\). The count is
\(\lfloor(X+L-r)/L\rfloor\), and subtracting \(X/L\) gives a number
between \(-1\) and \(1\).

Define
\[
S_H(m)=\sum_{\substack{d,e\le H\\\gcd(d,e)^2\mid m}}
\frac{\mu(d)\mu(e)\gcd(d,e)^2}{d^2e^2}.
\]
Expanding the finite product of divisor sums and applying the preceding
count gives
\[
\sum_{n\le X}A_H(n)A_H(n+m)=X S_H(m)+E_2,
\qquad |E_2|\le H^2.
\tag{10}
\]
Indeed, there are \(H^2\) ordered pairs \((d,e)\). An incompatible pair
contributes no error; a compatible pair has counting error at most \(1\),
and its coefficient \(\mu(d)\mu(e)\) has absolute value at most \(1\).
Thus summing these errors gives precisely the stated bound \(H^2\).

## 4. The infinite coefficient and its uniform tail

Set
\[
S_\infty(m)=\sum_{\substack{d,e\ge1\\\gcd(d,e)^2\mid m}}
\frac{\mu(d)\mu(e)\gcd(d,e)^2}{d^2e^2}.
\]
This series is absolutely convergent. To verify that assertion, write
\(d=ga\), \(e=gb\), where \(g=\gcd(d,e)\), and remove both the
restriction \(g^2\mid m\) and the restriction \(\gcd(a,b)=1\) in an
upper bound. Then
\[
\sum_{\substack{d,e\ge1\\\gcd(d,e)^2\mid m}}
\frac{|\mu(d)\mu(e)|\gcd(d,e)^2}{d^2e^2}
\le\sum_{g,a,b\ge1}\frac1{g^2a^2b^2}
\le 8,
\tag{11}
\]
since \(\sum_{j\ge1}j^{-2}\le1+\int_1^\infty t^{-2}\,dt=2\).

For a finite set of primes, expand the sum restricted to squarefree
\(d,e\) supported on that set. At a prime \(p\), the choices
\((v_p(d),v_p(e))=(0,0),(1,0),(0,1)\) contribute respectively
\(1,-p^{-2},-p^{-2}\). The choice \((1,1)\) is allowed exactly when
\(p^2\mid m\), and then contributes \(+p^{-2}\). Thus its local factor
is
\[
1-\frac2{p^2}+\frac{\mathbf 1_{p^2\mid m}}{p^2}.
\]
By the absolute convergence in (11), passing through increasing finite
sets of primes yields
\[
\begin{split}
S_\infty(m)
&=\prod_p\left(1-\frac2{p^2}
                 +\frac{\mathbf 1_{p^2\mid m}}{p^2}\right)\\
&=\prod_p\left(1-\frac2{p^2}\right)
  \prod_{p^2\mid m}\frac{p^2-1}{p^2-2}
=\mathfrak S(m).
\end{split}
\tag{12}
\]
The second product is finite because \(m\ge1\). The first product
converges to a positive number: its factors are positive, and
\(|\log(1-2/p^2)|\le4/p^2\), as follows by integrating
\((1-u)^{-1}\le2\) for \(0\le u\le1/2\).

Here is a tail estimate independent of \(m\). Define
\[
T_H=\sum_{\substack{d>H\\e\ge1}}
\frac{\gcd(d,e)^2}{d^2e^2}.
\]
For every real \(t\ge1\),
\[
\sum_{a>t}a^{-2}\le\frac1{\lfloor t\rfloor}\le\frac2t;
\]
for \(0\le t<1\), the sum is at most \(2\). The decomposition
\(d=ga\), \(e=gb\), with the coprimality condition removed in an
upper bound, therefore gives
\[
\begin{split}
T_H
&\le\sum_{g\ge1}\frac1{g^2}
       \left(\sum_{a>H/g}\frac1{a^2}\right)
       \left(\sum_{b\ge1}\frac1{b^2}\right)\\
&\le\frac4H\sum_{g=1}^H\frac1g
       +4\sum_{g>H}\frac1{g^2}\\
&\le\frac{4(1+\log H)}H+\frac4H
 =\frac{4(2+\log H)}H.
\end{split}
\tag{13}
\]
In the first \(g\)-range there are exactly \(H\) terms, each bounded
by \(4/(Hg)\); their sum is bounded by
\(4(1+\log H)/H\). In the infinite second range, each term is at most
\(4/g^2\); the integral tail bounds their sum by \(4/H\).

The omitted pairs in \(S_H(m)\) have either \(d>H\) or \(e>H\).
Removing the Möbius factors and compatibility restrictions bounds the
first set by \(T_H\). Exchanging the names \(d,e\) in the second set
bounds it by the same \(T_H\). The triangle inequality, (12), and (13)
give
\[
|S_H(m)-\mathfrak S(m)|
\le2T_H\le\frac{8(2+\log H)}H.
\tag{14}
\]
In particular, define \(E_3=X(S_H(m)-\mathfrak S(m))\). Its bound after
multiplication by \(X\) is
\[
|E_3|=|X(S_H(m)-\mathfrak S(m))|
\le\frac{8x(2+\log H)}H,
\tag{15}
\]
because \(0\le X\le x\).

## 5. Combining the errors and checking the ranges

Equations (8), (10), and (15) give the exact decomposition
\[
C_x(m)-X\mathfrak S(m)=E_1+E_2+E_3
\]
with the explicit bound
\[
\left|C_x(m)-X\mathfrak S(m)\right|
\le H^2+\frac{x}{H}
       \left(1+K_\delta x^\delta+8(2+\log H)\right).
\tag{16}
\]
Using (2) and \(\log H\le\tfrac13\log x\), we obtain
\[
\begin{split}
\left|C_x(m)-X\mathfrak S(m)\right|
&\le x^{2/3}
       \left(35+2K_\delta x^\delta+\frac{16}{3}\log x\right)\\
&\le\left(35+2K_\delta+\frac{16}{3\delta}\right)
       x^{2/3+\delta}.
\end{split}
\tag{17}
\]
For the last step, \(x^\delta\ge1\) and
\[
\log x=\int_1^x\frac{dt}{t}
\le\int_1^x t^{\delta-1}\,dt
=\frac{x^\delta-1}{\delta}\le\frac{x^\delta}{\delta}.
\]
Take \(\delta=\varepsilon\). Since
\(2/3+\varepsilon\le4/5+\varepsilon\) and \(x\ge2\), the proposition
holds with, for example,
\[
C(\varepsilon)=35+2K_\varepsilon+\frac{16}{3\varepsilon}.
\]
This proves (1) and the requested estimate. All preceding bounds are
independent of \(m\) in its specified range and require no lower bound
on \(X=x-m\). They therefore include bounded \(X\), including \(X=0\).

The stated optional circle-method cutoff is also consistent with its
specified range: for \(Q=x^{2/5}\),
\[
Q\le\frac{x^{1/2}}2
\quad\Longleftrightarrow\quad x^{1/10}\ge2
\quad\Longleftrightarrow\quad x\ge1024.
\]
For these \(x\), its arcs are well-defined subsets of \(\mathbb R/\mathbb Z\).
They are disjoint: distinct reduced centers of denominators \(q,r\le Q\)
have circular distance at least \(1/(qr)\), whereas the sum of their
radii is
\[
\frac{Q}{qx}+\frac{Q}{rx}
=\frac{Q(q+r)}{qr x}
\le\frac{2Q^2}{qr x}
\le\frac1{2qr}<\frac1{qr}.
\]
The proof above does not require this cutoff or any restriction to large
\(x\).

## Numerical sanity checks and sources

As a check only, a Python calculation tested the truncated congruence
count and its total error bound \(H^2\) for all permitted integer shifts
at \(x=2,3,10,31,100,10.75,31.2\), comprising \(187\) pairs \((x,m)\).
Using exact rational arithmetic, it also checked the finite Euler-product
expansion in (12), restricted to the primes \(2,3,5,7\), for
\(1\le m\le100\). The proof does not rely on these computations.

No external source was used, and no excluded source was consulted.
