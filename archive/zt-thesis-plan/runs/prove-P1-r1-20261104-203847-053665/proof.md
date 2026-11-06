# Proof of P1

Write \(e(t)=\exp(2\pi i t)\), and take logarithms to base \(e\). All sums over integers below are over positive integers unless another range is specified. We prove the assertions directly; no external literature or dependency proposition is used.

## Existence and evaluation of the density

For every positive integer \(n\), prime factorization gives
\[
\sum_{m^2\mid n}\mu(m)
=\prod_{p^2\mid n}(1-1)=\mu^2(n),
\tag{1}
\]
where an empty product equals one. Fix \(q\geq1\) and \(l\in\mathbb Z\). For \(x\geq1\), put \(M=\lfloor\sqrt{x}\rfloor\) and \(d_m=(m^2,q)\). The simultaneous congruences
\[
n\equiv l\pmod q,\qquad n\equiv0\pmod{m^2}
\]
are soluble precisely when \(d_m\mid l\). Indeed, writing \(n=m^2k\) reduces them to a linear congruence in \(k\); division by \(d_m\) leaves a coefficient coprime to \(q/d_m\). When soluble, the solutions form one residue class modulo \(qm^2/d_m\). The number of its members in \([1,x]\) differs from \(xd_m/(qm^2)\) by at most one. Consequently (1) gives
\[
Q(x;q,l)=\frac{x}{q}
\sum_{\substack{m\leq M\\d_m\mid l}}
\frac{\mu(m)d_m}{m^2}+E_1,
\qquad |E_1|\leq M.
\tag{2}
\]
Here each counting error has absolute value at most one, and there are at most \(M\) terms, so their sum has absolute value at most \(M\).

The series
\[
D(q,l)=\frac1q\sum_{\substack{m\geq1\\d_m\mid l}}
\frac{\mu(m)d_m}{m^2}
\tag{3}
\]
converges absolutely: each summand has absolute value at most \(m^{-2}\), since \(d_m\leq q\). The infinite omitted tail in (2), after multiplication by \(x\), has absolute value at most
\[
x\sum_{m>M}\frac1{m^2}
\leq x\int_M^\infty t^{-2}\,dt=\frac{x}{M}.
\tag{4}
\]
Since \(\sqrt{x}/2\leq M\leq\sqrt{x}\), equations (2)--(4) prove the explicit estimate
\[
|Q(x;q,l)-xD(q,l)|
\leq M+\frac{x}{M}\leq3\sqrt{x},
\qquad x\geq1.
\tag{5}
\]
Dividing by \(x\) and letting \(x\) tend to infinity proves that the density from `problem.md` exists and equals (3).

We will use the elementary Euler identity
\[
c=\zeta(2)^{-1}=\prod_p(1-p^{-2}).
\tag{6}
\]
To justify it here, expanding \(\prod_{p\leq z}(1-p^{-2})^{-1}\) gives the sum of \(m^{-2}\) over integers all of whose prime factors are at most \(z\). These sums increase to \(\sum_{m\geq1}m^{-2}=\zeta(2)\), because every integer has finitely many prime factors. Taking reciprocals gives (6).

For a prime \(p\), let \(t=v_p(q)\). The summand in (3) vanishes unless \(m\) is squarefree. The choice to include \(p\) in such an \(m\) contributes
\(-p^{\min(2,t)-2}\), and is allowed precisely when
\(p^{\min(2,t)}\mid l\). Thus the local factor in \(qg(q,l)\) is
\[
\begin{cases}
1-p^{-2},&t=0,\\
1,&t=1,\ p\nmid l,\\
1-p^{-1},&t=1,\ p\mid l,\\
1,&t\geq2,\ p^2\nmid l,\\
0,&t\geq2,\ p^2\mid l.
\end{cases}
\tag{7}
\]
This Euler expansion is justified by the absolute convergence of (3); equivalently, expand over finitely many primes and pass to the absolutely convergent series. The divisibility conditions in (7) also apply to \(l=0\).

If some \(p^2\) divides both \(q\) and \(l\), (7) gives \(g(q,l)=0\). In every other case, combining (6) and (7) gives exactly
\[
g(q,l)=\frac cq
\prod_{p\mid q}(1-p^{-2})^{-1}
\prod_{\substack{p\parallel q\\p\mid l}}(1-p^{-1}).
\tag{8}
\]
Every local factor in (7) lies in \([0,1]\). Their product therefore lies in \([0,1]\), proving
\[
0\leq g(q,l)\leq\frac1q.
\tag{9}
\]

## The finite second-moment identity

Let
\[
L(r)=\varphi(r)G(r)^2,
\qquad \lambda(r)=c^2L(r).
\]
The function \(L\) is multiplicative. Its prime-power values are
\[
L(p)=\frac{p-1}{(p^2-1)^2},\qquad
L(p^2)=\frac{p(p-1)}{(p^2-1)^2},\qquad
L(p^j)=0\quad(j\geq3).
\tag{10}
\]
These formulas follow from counting the \(p^j-p^{j-1}\) residues coprime to \(p^j\); multiplicativity of \(\varphi\) follows from the Chinese remainder theorem.

For \(t\geq1\), define a function on residues modulo \(p^t\) by
\[
b_{p,t}(l)=
\begin{cases}
1-p^{-1},&t=1,\ p\mid l,\\
0,&t\geq2,\ p^2\mid l,\\
1,&\text{otherwise}.
\end{cases}
\]
Equations (7)--(8), including their zero cases, give
\[
qg(q,l)=c\prod_{p^t\parallel q}
(1-p^{-2})^{-1}b_{p,t}(l).
\tag{11}
\]
For \(t=1\), there are \(p-1\) residues with \(b_{p,1}=1\) and one with \(b_{p,1}=1-p^{-1}\). Hence
\[
\begin{aligned}
(1-p^{-2})^{-2}\frac1p\sum_{l\bmod p}b_{p,1}(l)^2
&=(1-p^{-2})^{-2}
\left(1-\frac2{p^2}+\frac1{p^3}\right)\\
&=\frac{p^4-2p^2+p}{(p^2-1)^2}\\
&=1+\frac{p-1}{(p^2-1)^2}=1+L(p).
\end{aligned}
\tag{12}
\]
For \(t\geq2\), precisely \(p^{t-2}\) of the \(p^t\) residues have \(b_{p,t}=0\), and the other \(p^t-p^{t-2}\) have value one. Therefore
\[
\begin{aligned}
(1-p^{-2})^{-2}\frac1{p^t}
\sum_{l\bmod p^t}b_{p,t}(l)^2
&=(1-p^{-2})^{-1}\\
&=1+\frac1{p^2-1}\\
&=1+L(p)+L(p^2).
\end{aligned}
\tag{13}
\]
The last equality uses
\((p-1)+p(p-1)=p^2-1\).

The Chinese remainder theorem identifies the \(q\) residues modulo \(q\) with the Cartesian product of the residue sets modulo its prime-power factors. Averaging the square of (11) consequently factors into the local averages (12)--(13). With empty products understood when \(q=1\), this yields
\[
\begin{aligned}
q\sum_{l=1}^qg(q,l)^2
&=\frac1q\sum_{l=1}^q(qg(q,l))^2\\
&=c^2\prod_{p^t\parallel q}
\left(1+\sum_{j=1}^tL(p^j)\right)\\
&=c^2\sum_{r\mid q}L(r)
=\sum_{r\mid q}\lambda(r).
\end{aligned}
\tag{14}
\]

## Absolute summability and explicit tail estimates

The support of \(L\) consists of integers with no prime exponent exceeding two. Every such integer has a unique representation
\[
r=ab^2,
\qquad a,b\text{ squarefree},\quad(a,b)=1.
\tag{15}
\]
For every prime \(p\geq2\), set
\[
A_p=\frac{p^3}{(p-1)(p+1)^2}.
\]
The denominator minus the numerator equals \(p^2-p-1\), which is at least one for \(p\geq2\). Thus \(0<A_p\leq1\), and (10) becomes
\[
L(p)=\frac{A_p}{p^3},\qquad
L(p^2)=\frac{A_p}{p^2}.
\]
Multiplying these inequalities over the prime factors in (15) proves
\[
0\leq\lambda(ab^2)\leq\frac{c^2}{a^3b^2}.
\tag{16}
\]
Dropping the restrictions on \(a,b\) only increases these nonnegative sums. In particular
\[
\sum_{r\geq1}\lambda(r)
\leq c^2\left(\sum_{a\geq1}a^{-3}\right)
\left(\sum_{b\geq1}b^{-2}\right)
\leq3c^2<\infty,
\tag{17}
\]
where the two series are bounded by
\(1+\int_1^\infty t^{-3}dt=3/2\) and
\(1+\int_1^\infty t^{-2}dt=2\), respectively.

We can now evaluate the sum by its absolutely convergent Euler product. Equation (10) gives
\[
1+L(p)+L(p^2)
=1+\frac1{p^2-1}=(1-p^{-2})^{-1}.
\]
Consequently (6) implies
\[
\sum_{r\geq1}\lambda(r)
=c^2\prod_p(1+L(p)+L(p^2))
=c^2\zeta(2)=c.
\tag{18}
\]

For every real \(T>0\), we have the explicit bound
\[
\sum_{b>T}\frac1{b^2}\leq\frac2T.
\tag{19}
\]
For \(T\geq1\), putting \(N=\lfloor T\rfloor\geq T/2\) bounds this infinite tail by
\(\int_N^\infty t^{-2}dt=1/N\leq2/T\).
For \(0<T<1\), the sum is at most \(2\), which is at most \(2/T\).
For any \(R>0\), (16) and then (19), with \(T=\sqrt{R/a}\), give
\[
\begin{aligned}
\sum_{r>R}\lambda(r)
&\leq c^2\sum_{a\geq1}\frac1{a^3}
\sum_{b>\sqrt{R/a}}\frac1{b^2}\\
&\leq2c^2R^{-1/2}\sum_{a\geq1}a^{-5/2}\\
&\leq\frac{10}{3}R^{-1/2}.
\end{aligned}
\tag{20}
\]
For each \(a\), the inner infinite sum before summation over \(a\) is at most \(2\sqrt{a/R}\). Its contribution after multiplication by \(c^2a^{-3}\) is at most \(2c^2R^{-1/2}a^{-5/2}\). The final bound uses \(c\leq1\) and
\[
\sum_{a\geq1}a^{-5/2}
\leq1+\int_1^\infty t^{-5/2}dt=\frac53.
\tag{21}
\]

Multiplication of (16) by \(ab^2\) gives
\(ab^2\lambda(ab^2)\leq c^2a^{-2}\). Thus
\[
\begin{aligned}
\sum_{r\leq R}r\lambda(r)
&\leq c^2\sum_{1\leq a\leq R}\frac1{a^2}
\sum_{1\leq b\leq\sqrt{R/a}}1\\
&\leq c^2R^{1/2}\sum_{1\leq a\leq R}a^{-5/2}
\leq\frac53R^{1/2}.
\end{aligned}
\tag{22}
\]
For each \(a\leq R\), the inner sum has
\(\lfloor\sqrt{R/a}\rfloor\leq\sqrt{R/a}\) terms, each contributing at most \(c^2a^{-2}\). Its total is at most \(c^2R^{1/2}a^{-5/2}\). Summing over the \(\lfloor R\rfloor\) possible values of \(a\), and applying (21), gives the last inequality in (22).

For \(R\geq2\), \(\log(2R)\geq\log4>1\). Therefore (20) and (22) imply both bounds requested in the statement, with the same absolute constant \(C=10/3\). They also prove the stronger versions without logarithmic factors.

## The Ramanujan series

There are \(\varphi(r)\) terms in the defining sum for \(c_r(n)\), each of absolute value one. Hence, for every integer \(n\),
\[
|c_r(n)|\leq\varphi(r),\qquad
\sum_{r\geq1}|\gamma(r)^2c_r(n)|
\leq\sum_{r\geq1}\lambda(r)=c.
\tag{23}
\]
This proves absolute convergence, with a bound uniform in \(n\).

For completeness, the multiplicativity needed to evaluate the series follows directly from the Chinese remainder theorem. If \((s,t)=1\), choose integers \(u,v\) with \(tu\equiv1\pmod s\) and \(sv\equiv1\pmod t\). A unit residue \(a\pmod{st}\) corresponding to unit residues \(b\pmod s\), \(d\pmod t\) satisfies
\[
\frac{a}{st}\equiv\frac{bu}{s}+\frac{dv}{t}\pmod1.
\]
Summing the resulting exponential identity over \(b,d\), and using the permutations of unit residues induced by multiplication by \(u,v\), gives
\[
c_{st}(n)=c_s(n)c_t(n).
\tag{24}
\]

The finite geometric sum satisfies
\[
\sum_{a=1}^k e(an/k)=k\,\boldsymbol1_{k\mid n}.
\]
Subtracting the term for the zero residue modulo \(p\) gives
\(c_p(n)=p\boldsymbol1_{p\mid n}-1\).
Subtracting the sum over residues divisible by \(p\) from the full sum modulo \(p^2\) gives
\[
c_{p^2}(n)=p^2\boldsymbol1_{p^2\mid n}
-p\boldsymbol1_{p\mid n}.
\]
Adding these two exact identities yields
\[
c_p(n)+c_{p^2}(n)=p^2\boldsymbol1_{p^2\mid n}-1.
\tag{25}
\]
By (23)--(24), the absolutely convergent series has the Euler expansion
\[
\sum_{r\geq1}\gamma(r)^2c_r(n)
=c^2\prod_p
\left(1+\frac{c_p(n)+c_{p^2}(n)}{(p^2-1)^2}\right).
\tag{26}
\]
Using (6), absorb the factor \((1-p^{-2})^2\) of \(c^2\) into each local factor. If \(p^2\nmid n\), (25) gives
\[
(1-p^{-2})^2\left(1-\frac1{(p^2-1)^2}\right)
=\frac{(p^2-1)^2-1}{p^4}
=1-\frac2{p^2}.
\tag{27}
\]
If \(p^2\mid n\), it gives
\[
(1-p^{-2})^2\left(1+\frac{p^2-1}{(p^2-1)^2}\right)
=\frac{p^2-1}{p^2}
=1-\frac1{p^2}.
\tag{28}
\]
All these product operations are legitimate: (26) is justified by absolute convergence, and (6) converges. The product \(\prod_p(1-2/p^2)\) converges to a positive number as well. Indeed, for \(0\leq u\leq1/2\),
\(-\log(1-u)=\int_0^u(1-t)^{-1}dt\leq2u\), so
\(\sum_p|\log(1-2/p^2)|\leq4\sum_p p^{-2}<\infty\).

Finally, when \(n\geq1\), only finitely many primes satisfy \(p^2\mid n\). Replacing the factors (27) by (28) for those primes multiplies the baseline product by
\[
\frac{1-p^{-2}}{1-2p^{-2}}=\frac{p^2-1}{p^2-2}.
\]
Thus (26) equals precisely
\[
\boxed{\displaystyle
\mathfrak S(n)=\prod_p\left(1-\frac2{p^2}\right)
\prod_{p^2\mid n}\frac{p^2-1}{p^2-2}.}
\]
This proves every assertion of P1.

No numerical checks or external sources were used.
