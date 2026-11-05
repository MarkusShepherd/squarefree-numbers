# Proof of P4

We use P1 as a black box. No external literature or numerical computation is used.
All logarithms are natural. Constants introduced below depend only on the fixed
polynomial (f), except for the absolute constant in P1.

## 1. A weighted periodic counting estimate

The assumptions in `problem.md` are

\[
f\in\mathbb Z[t],\qquad d=\deg f\geq1,\qquad
f(t)\geq2,\quad f'(t)\geq1\quad(t\geq1).
\]

In particular, (f) is strictly increasing on ([1,\infty)) and its leading
coefficient is positive. Put

\[
m=\inf_{t\geq1}\frac{f(t)}{t^d}>0,\qquad
M=\sup_{t\geq1}\frac{f(t)}{t^d}<\infty,\qquad
L=\sup_{t\geq1}\frac{f'(t)}{t^{d-1}}<\infty.
\]

These assertions follow from continuity, positivity, and the positive finite
limit of (f(t)/t^d) at infinity; the assertion about (L) follows by dividing
the polynomial (f') by (t^{d-1}). Define

\[
\alpha=1-\frac1d,\qquad
K=Lm^{-\alpha},\qquad
B=2d\frac{LM^{1/d}}m,\qquad D=2d^2K.
\tag{1}
\]

We will use two elementary weighted estimates, proved here. If (b(k)) is a
complex periodic sequence of integer period (r\geq1), write

\[
\overline b=\frac1r\sum_{a=1}^r b(a),\qquad
\Delta_b=\sum_{a=1}^r|b(a)|.
\]

For real (z\leq t), the number of integers in ((z,t]) in a fixed residue
class modulo (r) differs from ((t-z)/r) by at most (1): this follows by
writing the count as a difference of two floor functions. Consequently

\[
\left|\sum_{z<k\leq t}b(k)-\overline b(t-z)\right|\leq\Delta_b.
\]

Integration by parts for this counting function gives, for every continuously
differentiable real weight (w) on ([z,v]),

\[
\left|\sum_{z<k\leq v}b(k)w(k)
 -\overline b\int_z^v w(u)\,du\right|
\leq\Delta_b\left(|w(v)|+\int_z^v|w'(u)|\,du\right).
\tag{2}
\]

This also holds when (v=z), when the expression on the left vanishes.

First take (w(u)=f'(u)/f(u)). For (u\geq z\geq1), with (Z=f(z)),

\[
0<w(u)\leq\frac{L}{mu}\leq\frac{L}{mz}
\leq\frac{LM^{1/d}}m Z^{-1/d}.
\tag{3}
\]

The numerator of (w') is (f''f-(f')^2), a nonzero polynomial of degree
(2d-2): its leading coefficient is (-d a_d^2), where (a_d) is the
leading coefficient of (f). It has at most (2d-2) real zeros. Thus any
interval ([z,v]) has at most (2d-1) subintervals on which (w) is
monotone. Since (w) is positive, its variation on each such subinterval is
at most the supremum in (3). Including the endpoint term in (2) yields

\[
|w(v)|+\int_z^v|w'(u)|\,du\leq BZ^{-1/d}.
\tag{4}
\]

Apply (2) to (b(k)=1_{r\mid f(k)}). Its mean is \(\rho(r)/r\) and
\(\Delta_b=\rho(r)\), because (f\) has integer coefficients. Therefore

\[
\left|\sum_{\substack{z<k\leq y\\r\mid f(k)}}\frac{f'(k)}{f(k)}
 -\frac{\rho(r)}r\log\frac YZ\right|
\leq B\rho(r)Z^{-1/d}.
\tag{5}
\]

In particular, (\rho(1)=1), so if

\[
S_0=\sum_{z<k\leq y}\frac{f'(k)}{f(k)},\qquad
\ell=\log(Y/Z),
\]

then

\[
0\leq S_0\leq\ell+BZ^{-1/d}.
\tag{6}
\]

For the second weight, let (h\geq1) be an integer with (h\leq x/Z), and
let (v_h\in[z,y]) be specified by

\[
f(v_h)=\min(Y,x/h).
\]

The inverse exists by strict monotonicity. Set

\[
w_h(u)=f'(u)(x-hf(u))\qquad(z\leq u\leq v_h).
\]

The inequality (f'(u)\leq Kf(u)^\alpha), which follows from
(f'(u)\leq Lu^{d-1}) and (f(u)\geq mu^d), gives

\[
0\leq w_h(u)\leq Kx(x/h)^\alpha
=Kx^{1+\alpha}h^{-\alpha}.
\tag{7}
\]

The polynomial (w_h) has degree (2d-1) and leading coefficient
(-hd a_d^2). Its derivative has at most (2d-2) real zeros. The variation
argument used for (4), now with the nonnegative weight in (7), gives

\[
|w_h(v_h)|+\int_z^{v_h}|w_h'(u)|\,du
\leq2dKx^{1+\alpha}h^{-\alpha}.
\tag{8}
\]

## 2. Convergence and the local mean of the singular series

Use the notation (\gamma(r)) and (c_r(n)) of P1. The definition as a sum
of (\varphi(r)) complex numbers of modulus (1) gives

\[
|c_r(n)|\leq\varphi(r),\qquad
\gamma(r)^2|c_r(n)|\leq\lambda(r).
\tag{9}
\]

For each positive integer (h), define

\[
\beta_r(h)=\frac1r\sum_{a=1}^r c_r(hf(a)).
\]

Then (|\beta_r(h)|\leq\varphi(r)). Since P1 states
(\sum_r\lambda(r)=c), both

\[
\sum_{r\geq1}\lambda(r)\frac{\rho(r)}r,
\qquad
\sum_{r\geq1}\gamma(r)^2\beta_r(h)
\tag{10}
\]

converge absolutely, uniformly in the integer (h) for the second series.
Here we used only (0\leq\rho(r)\leq r); no estimate for polynomial roots
at exceptional primes is needed.

We now identify the second series in (10). If (u,v) are coprime, writing
each unit modulo (uv) uniquely as (bv+cu\pmod{uv}), with (b,c) units
modulo (u,v), respectively, proves

\[
c_{uv}(n)=c_u(n)c_v(n).
\]

The Chinese remainder correspondence for the variable (a), together with
the fact that (f(a)\bmod u) depends only on (a\bmod u), now gives

\[
\beta_{uv}(h)=\beta_u(h)\beta_v(h).
\tag{11}
\]

Finite geometric sums, subtracting the multiples of (p) in the second
formula, give

\[
c_p(n)=p1_{p\mid n}-1,\qquad
c_{p^2}(n)=p^2 1_{p^2\mid n}-p1_{p\mid n}.
\]

Thus (c_p(n)+c_{p^2}(n)=p^2 1_{p^2\mid n}-1). Let

\[
j=j_p(h)=\max(2-v_p(h),0),\qquad
u_p(h)=\frac{\rho(p^j)}{p^j}.
\]

The condition (p^2\mid hf(a)) is exactly (p^j\mid f(a)). Among the
(p^2) residue classes for (a), there are
(p^{2-j}\rho(p^j)) satisfying this condition, including when (j=0).
Averaging the preceding Ramanujan-sum identity modulo (p^2) therefore gives

\[
\beta_p(h)+\beta_{p^2}(h)=p^2u_p(h)-1.
\tag{12}
\]

The square of the function (G) in P1 is multiplicative and supported on
integers with no prime cube divisor. Equations (11), (12), and absolute
convergence in (10) give

\[
\begin{aligned}
\sum_{r\geq1}\gamma(r)^2\beta_r(h)
&=c^2\prod_p\left(1+
 \frac{\beta_p(h)+\beta_{p^2}(h)}{(p^2-1)^2}\right)\\
&=\prod_p\left(1-\frac1{p^2}\right)^2
 \left(1+\frac{p^2u_p(h)-1}{(p^2-1)^2}\right)\\
&=\prod_p\left(1-\frac2{p^2}\right)
 \left(1+\frac{u_p(h)}{p^2-2}\right)
=W_f(h).
\end{aligned}
\tag{13}
\]

The identity (c=\prod_p(1-p^{-2})) used here follows by expanding the
absolutely convergent geometric Euler product for \(\sum_{n\geq1}n^{-2}\).
To justify the product rearrangements directly, (9) and P1 give
(\sum_r G(r)^2|\beta_r(h)|\leq c^{-1}); finite prime products expand
into subseries of this absolutely convergent series and tend to the full
series. Also (0\leq u_p(h)\leq1), and the final local factor in (13) is
(1-(2-u_p(h))/p^2), whose difference from (1) is at most (2/p^2).
The two individual products displayed in the definition of (W_f(h))
converge absolutely as well, since

\[
\frac{u_p(h)}{p^2-2}\leq\frac2{p^2},\qquad
\sum_p\frac1{p^2}\leq\sum_{n\geq2}\frac1{n^2}<\infty.
\]

For each fixed positive integer (n), the product defining
\(\mathfrak S(n)\) consists of the absolutely convergent product
\(\prod_p(1-2/p^2)\) and a finite product over (p^2\mid n).
This verifies all the asserted convergence statements.

For real (R\geq2), put

\[
T_R=\sum_{r>R}\lambda(r),\qquad
U_R=\sum_{r\leq R}r\lambda(r),\qquad L_R=\log(2R).
\]

Fix an absolute constant (C_0) large enough that both bounds in P1 read

\[
T_R\leq C_0R^{-1/2}L_R^2,\qquad
U_R\leq C_0R^{1/2}L_R^2.
\tag{14}
\]

Define finite truncations

\[
\mathfrak S_R(n)=\sum_{r\leq R}\gamma(r)^2c_r(n),\qquad
W_R(h)=\sum_{r\leq R}\gamma(r)^2\beta_r(h).
\]

P1, (9), and (13) imply the uniform bounds

\[
|\mathfrak S(n)-\mathfrak S_R(n)|\leq T_R,\qquad
|W_f(h)-W_R(h)|\leq T_R.
\tag{15}
\]

## 3. The density-square average

By P1, for every integer (q\geq1),

\[
\sum_{l=1}^qg(q,l)^2=\frac1q\sum_{r\mid q}\lambda(r).
\]

Consequently the first discrete expression in P4 equals

\[
S_1=\sum_{r\geq1}\lambda(r)
 \sum_{\substack{z<k\leq y\\r\mid f(k)}}\frac{f'(k)}{f(k)}.
\tag{16}
\]

All summands here are nonnegative, and only finitely many divisors occur for
each of the finitely many (k). For each (r\leq R), the error in replacing
the inner sum by \((\rho(r)/r)\ell\) is at most
(B\rho(r)Z^{-1/d}), by (5). There are \(\lfloor R\rfloor\) such
values of (r); after multiplication by \(\lambda(r)\) and summation, the
total error is at most

\[
BZ^{-1/d}\sum_{r\leq R}\lambda(r)\rho(r)
\leq BZ^{-1/d}U_R.
\tag{17}
\]

For the remaining (r), their contribution to (16) is at most (T_RS_0),
by first fixing (k) and bounding the sum over its divisors (r>R) by
(T_R). The omitted part of \(R_f\ell\) is at most (T_R\ell), because
\(\rho(r)/r\leq1\). Equation (6) thus proves

\[
|S_1-R_f\ell|
\leq BZ^{-1/d}U_R+T_R(2\ell+BZ^{-1/d}).
\tag{18}
\]

Here the infinite sums have been bounded by the explicitly summable majorant
\(\lambda(r)\), rather than by multiplying a pointwise error by an infinite
length. Since (Z\geq2), \(0\leq\ell\leq\log(2x)\), and
\(\log(2x)\geq\log4>1\), (14) yields

\[
|S_1-R_f\log(Y/Z)|
\leq C_0B Z^{-1/d}R^{1/2}L_R^2
 +C_0(2+B)R^{-1/2}L_R^2\log(2x).
\tag{19}
\]

This is the first required estimate.

## 4. The singular-series average

Put (H=\lfloor x/Z\rfloor\), so that (1\leq H\leq x/Z). For a fixed
(r\geq1) and (1\leq h\leq H), the sequence
(b(k)=c_r(hf(k))) has period (r), mean \(\beta_r(h)\), and

\[
\Delta_b\leq r\varphi(r).
\]

Using (2) and (8), and then substituting (t=f(u)), gives

\[
\begin{aligned}
\Bigg|\sum_{\substack{z<k\leq y\\f(k)\leq x/h}}
 f'(k)(x-hf(k))c_r(hf(k))
&-\beta_r(h)\int_Z^{\min(Y,x/h)}(x-ht)\,dt\Bigg|\\
&\leq2dK r\varphi(r)x^{1+\alpha}h^{-\alpha}.
\end{aligned}
\tag{20}
\]

This remains valid if (x/h=Z): both expressions on the left vanish.
The sum over (h) has exactly (H) terms. Before summation the bound is
the right side of (20). Since (t^{-\alpha}) is decreasing and
\(1-\alpha=1/d\),

\[
\sum_{h=1}^Hh^{-\alpha}
\leq1+\int_1^Ht^{-\alpha}\,dt
=dH^{1/d}-(d-1)
\leq d(x/Z)^{1/d}.
\tag{21}
\]

The bound after summation in (h) is therefore

\[
2d^2K r\varphi(r)x^{1+\alpha+1/d}Z^{-1/d}
=D r\varphi(r)x^2Z^{-1/d}.
\tag{22}
\]

In particular, the exponent of (x) is exactly (2). Multiply (22) by
\(\gamma(r)^2\) and sum over the \(\lfloor R\rfloor\) integers (r\leq R).
Before this summation the bound is
\(D r\lambda(r)x^2Z^{-1/d}\); afterwards it is
\(Dx^2Z^{-1/d}U_R\). Interchanging only finite sums and integrals gives

\[
\begin{aligned}
\Bigg|\sum_{z<k\leq y}f'(k)
 \sum_{1\leq h\leq x/f(k)}(x-hf(k))\mathfrak S_R(hf(k))
&-\int_Z^Y\sum_{1\leq h\leq x/t}(x-ht)W_R(h)\,dt\Bigg|\\
&\leq Dx^2Z^{-1/d}U_R.
\end{aligned}
\tag{23}
\]

It remains to bound both truncation errors, including their summation
lengths. For real (q>0) there are \(\lfloor x/q\rfloor\) terms in the
following sum. The function \(u\mapsto(x-qu)_+\) is nonnegative and
decreasing, so its value at each positive integer is at most its integral
over the preceding unit interval. Hence

\[
\sum_{1\leq h\leq x/q}(x-hq)
\leq\int_0^{x/q}(x-qu)\,du=\frac{x^2}{2q}.
\tag{24}
\]

For each (k), the first bound in (15) gives a truncation error at most
(T_R f'(k)(x-hf(k))) before summation in (h). Summing its
\(\lfloor x/f(k)\rfloor\) terms using (24) gives at most
(T_Rx^2 f'(k)/(2f(k))). The (k)-sum has
\(\lfloor y\rfloor-\lfloor z\rfloor\) terms. After this summation, (6)
gives the bound

\[
\frac{T_Rx^2}{2}S_0
\leq\frac{T_Rx^2}{2}(\ell+BZ^{-1/d}).
\tag{25}
\]

For each (t\in[Z,Y]), the second bound in (15) gives error at most
(T_R(x-ht)) before summation in (h). There are
\(\lfloor x/t\rfloor\) terms, and (24) bounds their sum by
(T_Rx^2/(2t)). Integrating this explicit bound gives

\[
\int_Z^Y\frac{T_Rx^2}{2t}\,dt=\frac{T_Rx^2}{2}\ell.
\tag{26}
\]

Combining (23), (25), and (26), the absolute difference in the second
assertion of P4 is at most

\[
x^2\left[DZ^{-1/d}U_R
 +T_R\left(\ell+\frac B2Z^{-1/d}\right)\right].
\tag{27}
\]

Applying (14), (Z^{-1/d}\leq1), and
\(\ell\leq\log(2x)\), this is at most

\[
C_0D x^2Z^{-1/d}R^{1/2}L_R^2
 +C_0(1+B/2)x^2R^{-1/2}L_R^2\log(2x).
\tag{28}
\]

Finally, take

\[
C(f)=C_0\max\{B,\ 2+B,\ D,\ 1+B/2\}.
\]

Equations (19) and (28) give precisely the two asserted bounds with

\[
A=Z^{-1/d}R^{1/2}(\log(2R))^2
 +R^{-1/2}(\log(2R))^2\log(2x).
\]

Every constant is independent of (x,z,y,R,h,r). The only properties of
polynomial congruences used were periodicity, the bound \(\rho(r)\leq r\),
and exact lifting of residue classes from (p^j) to (p^2). Thus the proof
imposes no condition on the discriminant, content, or factorization of (f).
