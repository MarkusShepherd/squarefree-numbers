# Proof of P3

We prove the stronger bound
\[
\bigl|C_x(m)-(x-m)\mathfrak S(m)\bigr|\le Kx^{4/5}
\tag{1}
\]
with an absolute constant \(K\), for all the parameters in the statement.
The argument is elementary and does not require a circle-method cutoff.
No external sources or results from the supplied papers are used, and the
dependency P1 is not needed. No numerical checks are used.

## An explicit divisor bound

Write \(\tau(n)\) for the number of positive divisors of a positive integer
\(n\). Define the absolute constant
\[
D=\prod_{p<2^{10}}(1-p^{-1/10})^{-2},
\]
where the product is over primes. We will use
\[
\tau(n)\le Dn^{1/10}\qquad(n\ge1).
\tag{2}
\]
Here is an elementary verification. For every integer \(a\ge0\),
\(a+1\le2^a\), as follows by induction. Consequently, if \(p\ge2^{10}\),
then \(a+1\le p^{a/10}\). If \(p<2^{10}\), the geometric-series identity gives
\[
(a+1)p^{-a/10}
\le\sum_{j=0}^{\infty}(j+1)p^{-j/10}
=(1-p^{-1/10})^{-2}.
\]
Multiplication over the prime powers in the factorization of \(n\) proves
(2); the factors included in \(D\) but absent from this factorization are
all at least one.

We also record the following bounds for positive real \(t\ge1\) and positive
integers \(H\):
\[
\sum_{j=1}^{\infty}\frac1{j^2}\le2,\qquad
\sum_{j>H}\frac1{j^2}\le\frac1H,\qquad
\sum_{j>t}\frac1{j^2}\le\frac2t,\qquad
\sum_{j=1}^{H}\frac1j\le1+\log H.
\tag{3}
\]
The first, second and fourth inequalities follow by comparison with the
integrals of \(u^{-2}\) and \(u^{-1}\). For the third, put \(k=\lfloor t\rfloor\).
Then \(k\ge t/2\), so the second inequality gives a bound \(1/k\le2/t\).

## Truncating the square-divisor identities

Fix real \(x\ge2\) and an integer \(1\le m\le x\), and put
\[
L=x-m\ge0,\qquad H=\lfloor x^{2/5}\rfloor.
\]
In particular,
\[
\tfrac12x^{2/5}\le H\le x^{2/5}.
\tag{4}
\]
For positive integers \(k\), define
\[
T_H(k)=\sum_{\substack{d\le H\\d^2\mid k}}\mu(d),\qquad
R_H(k)=\sum_{\substack{d>H\\d^2\mid k}}\mu(d).
\]
All divisor variables in this proof are positive integers. The identity
\[
\mu^2(k)=\sum_{d^2\mid k}\mu(d)=T_H(k)+R_H(k)
\tag{5}
\]
follows by multiplying the local factors: a prime occurring to exponent at
least two contributes \(1+\mu(p)=0\); if no such prime occurs, the sum is one.
Also
\[
|T_H(k)|\le\tau(k),\qquad
|R_H(k)|\le\sum_{\substack{d>H\\d^2\mid k}}1.
\tag{6}
\]

For either of the two sets
\[
I_0=\{n:1\le n\le L\},\qquad
I_m=\{n+m:1\le n\le L\},
\]
there are \(\lfloor L\rfloor\) elements, all positive integers at most \(x\).
For each fixed \(d\), the number of elements divisible by \(d^2\) is at most
\(\lfloor x/d^2\rfloor\le x/d^2\). The outer sum below has
\(\max(0,\lfloor\sqrt x\rfloor-H)\le\sqrt x\) terms. Thus (3) and (6) give,
for each \(I\in\{I_0,I_m\}\),
\[
\sum_{k\in I}|R_H(k)|
\le\sum_{H<d\le\sqrt x}\frac{x}{d^2}
\le\frac{x}{H}.
\tag{7}
\]
This estimate also holds when either set is empty.

The exact product identity
\[
\mu^2(n)\mu^2(n+m)-T_H(n)T_H(n+m)
=R_H(n)\mu^2(n+m)+T_H(n)R_H(n+m)
\]
and \(0\le\mu^2(k)\le1\) show that the absolute value of each summand is at
most
\[
|R_H(n)|+Dx^{1/10}|R_H(n+m)|,
\]
where we used (2), (6), and \(n\le x\). Summing over the
\(\lfloor L\rfloor\le x\) admissible integers \(n\), and using (7) for
each of its two terms, yields
\[
\left|C_x(m)-\sum_{1\le n\le L}T_H(n)T_H(n+m)\right|
\le (1+Dx^{1/10})\frac{x}{H}
\le2x^{3/5}+2Dx^{7/10}.
\tag{8}
\]
In particular this estimate has no inverse power of \(L\).

## Counting the truncated congruences

For \(d,e\le H\), set \(g=(d,e)\). The congruences
\[
n\equiv0\pmod{d^2},\qquad n\equiv-m\pmod{e^2}
\]
are soluble precisely when \(g^2\mid m\). Necessity follows by reducing
both congruences modulo \(g^2\). To verify sufficiency and the modulus of
the solutions, write \(d=ga\), \(e=gb\), where \((a,b)=1\), and write
\(n=d^2u\). If \(g^2\mid m\), the second congruence becomes
\[
a^2u\equiv -m/g^2\pmod{b^2}.
\]
Since \((a^2,b^2)=1\), this specifies one residue class of \(u\) modulo
\(b^2\), and hence one residue class of \(n\) modulo
\[
h=d^2b^2=\frac{d^2e^2}{g^2}.
\]
For any integer representative \(r\) of a residue class modulo \(h\), its
number of representatives in \(1\le n\le L\) is
\[
\left\lfloor\frac{L-r}{h}\right\rfloor
-\left\lfloor\frac{-r}{h}\right\rfloor
=\frac Lh+\theta,\qquad |\theta|\le1.
\tag{9}
\]
This formula is valid for every real \(L\ge0\).

Define
\[
A_H(m)=\sum_{\substack{d,e\le H\\(d,e)^2\mid m}}
\frac{\mu(d)\mu(e)(d,e)^2}{d^2e^2}.
\]
Expanding the two finite divisor sums and applying (9) gives
\[
\sum_{1\le n\le L}T_H(n)T_H(n+m)=LA_H(m)+E_H,
\qquad |E_H|\le H^2\le x^{4/5}.
\tag{10}
\]
Indeed, the error for each compatible pair \((d,e)\) has absolute value
at most one after multiplication by \(\mu(d)\mu(e)\), and there are at
most \(H^2\) pairs. Incompatible pairs contribute zero.

## The infinite main term and its uniform tail

Consider
\[
A(m)=\sum_{\substack{d,e\ge1\\(d,e)^2\mid m}}
\frac{\mu(d)\mu(e)(d,e)^2}{d^2e^2}.
\]
This series is absolutely convergent. In fact, writing \(d=ga\), \(e=gb\)
with \((a,b)=1\), and then dropping this coprimality condition, bounds its
absolute sum by
\[
\sum_{d,e\ge1}\frac{(d,e)^2}{d^2e^2}
\le\sum_{g\ge1}\frac1{g^2}
   \left(\sum_{a\ge1}\frac1{a^2}\right)
   \left(\sum_{b\ge1}\frac1{b^2}\right)
\le8.
\tag{11}
\]

We now bound the tail without using any restriction on the divisors of
\(m\). For the part with \(d>H\), the same change of variables gives
\[
\sum_{\substack{d>H\\e\ge1}}\frac{(d,e)^2}{d^2e^2}
\le\sum_{g\ge1}\frac1{g^2}
  \left(\sum_{a>H/g}\frac1{a^2}\right)
  \left(\sum_{b\ge1}\frac1{b^2}\right).
\tag{12}
\]
For a fixed \(g\le H\), the summand on the right of (12) is at most
\(g^{-2}(2g/H)\,2=4/(Hg)\), by (3). There are \(H\) such values of \(g\),
and their total is at most
\[
\frac4H\sum_{g=1}^{H}\frac1g
\le\frac{4(1+\log H)}H.
\]
For a fixed \(g>H\), both inner sums in (12) are at most two, giving
\(4/g^2\) before summing. The infinite sum over these \(g\) is at most
\(4/H\), by (3). Consequently the left side of (12) is at most
\((8+4\log H)/H\). The change of variables \((d,e)\mapsto(e,d)\) is a
bijection preserving the summand and carries the condition \(e>H\) to
\(d>H\), so the tail with \(e>H\) has exactly the same bound. The union
bound, together with \(|\mu(d)\mu(e)|\le1\), now gives
\[
|A(m)-A_H(m)|\le\frac{16+8\log H}{H}
=\frac{8(2+\log H)}H.
\tag{13}
\]
All sums used to obtain (13) were bounded after dropping
\((d,e)^2\mid m\), so its constant is independent of \(m\).

Absolute convergence in (11) permits factorization into prime factors:
one may first restrict both divisor variables to integers supported on a
finite set of primes and then let these sets exhaust the primes. Only
exponents zero and one occur in \(d,e\) because of the Möbius factors.
For a fixed prime \(p\), the choices of these two exponents contribute as
follows:

| Exponent in \(d\) | Exponent in \(e\) | Contribution |
| --- | --- | --- |
| 0 | 0 | \(1\) |
| 1 | 0 | \(-p^{-2}\) |
| 0 | 1 | \(-p^{-2}\) |
| 1 | 1 | \(p^{-2}\) if \(p^2\mid m\), and \(0\) otherwise |

It follows that
\[
\begin{aligned}
A(m)
&=\prod_p\left(1-\frac2{p^2}
                   +\frac{\mathbf1_{p^2\mid m}}{p^2}\right)\\
&=\prod_p\left(1-\frac2{p^2}\right)
  \prod_{p^2\mid m}
  \frac{1-p^{-2}}{1-2p^{-2}}\\
&=\prod_p\left(1-\frac2{p^2}\right)
  \prod_{p^2\mid m}\frac{p^2-1}{p^2-2}
=\mathfrak S(m).
\end{aligned}
\tag{14}
\]
The second product is finite since \(m\ge1\). The first product converges
because \(\sum_p2p^{-2}<\infty\), and each of its factors is positive.

## Combining the bounds

Since \(0\le L\le x\), (4), (13), and (14) imply
\[
\begin{aligned}
L|A_H(m)-\mathfrak S(m)|
&\le\frac{8x(2+\log H)}H\\
&\le16x^{3/5}\left(2+\frac25\log x\right)\\
&=32x^{3/5}+\frac{32}{5}x^{3/5}\log x.
\end{aligned}
\tag{15}
\]
For \(x\ge1\),
\[
\log x=\int_1^x\frac{dt}{t}
\le\int_1^x t^{-4/5}\,dt
=5(x^{1/5}-1)\le5x^{1/5}.
\]
Thus (15) is at most
\[
32x^{3/5}+32x^{4/5}\le64x^{4/5}.
\tag{16}
\]
Finally, (8), (10), and (16) give the fully explicit error bound
\[
\begin{aligned}
\bigl|C_x(m)-L\mathfrak S(m)\bigr|
&\le2x^{3/5}+2Dx^{7/10}+x^{4/5}+64x^{4/5}\\
&\le(67+2D)x^{4/5}.
\end{aligned}
\]
This proves (1). For every \(\varepsilon>0\), take
\(C(\varepsilon)=67+2D\) and use
\(x^{4/5}\le x^{4/5+\varepsilon}\). All bounds above hold for every
\(L\ge0\), including bounded \(L\) and \(L=0\), establishing the required
uniformity. \(\square\)
