# Proof of P4

We use P1 exactly as supplied. No external paper is used. All logarithms are natural. Constants introduced below depend only on $f$, except for the absolute constant supplied by P1.

## Polynomial bounds and a periodic averaging lemma

The leading coefficient of $f$ is positive: otherwise $f(t)\geq 2$ for all $t\geq 1$ would fail. Since $f(t)>0$ on this interval, continuity and the positive limit of $f(t)/t^d$ give constants $a>0$ and $B\geq 1$ such that, for every $t\geq 1$,
\[
 a t^d\leq f(t)\leq B t^d,
 \qquad |f'(t)|\leq B t^{d-1}.
 \tag{1}
\]
When $d\geq 2$, enlarge $B$ so that
\[
 |f''(t)|\leq B t^{d-2}\quad(t\geq 1).
 \tag{2}
\]
When $d=1$, $f''=0$. Define
\[
 U=\frac{B}{a},\qquad
 V=\frac{B}{a}+\frac{B^2}{a^2},\qquad D=U+V.
 \tag{3}
\]
For $w(t)=f'(t)/f(t)$, equations (1)--(2), including $f''=0$ when $d=1$, imply
\[
 0<w(t)\leq\frac{U}{t},\qquad
 |w'(t)|
 \leq\frac{|f''(t)|}{f(t)}+\frac{|f'(t)|^2}{f(t)^2}
 \leq\frac{V}{t^2}.
 \tag{4}
\]
Also $f'(t)\geq 1$ and $f(1)\geq 2$ give $f(t)\geq t+1$. Thus $y<x$, and
\[
 \sum_{z<k\leq y}\frac{f'(k)}{f(k)}
 \leq U\sum_{1\leq k\leq y}\frac1k
 \leq U(1+\log y)
 \leq 2U\log(2x).
 \tag{5}
\]
Here the sum has at most $\lfloor y\rfloor\leq\lfloor x\rfloor$ terms; the harmonic-sum bound follows by comparison with the integral of $1/t$ on $[1,y]$.

We will use the following elementary lemma. If $b(k)$ is periodic of integer period $r\geq 1$, satisfies $|b(k)|\leq 1$, and has mean
\[
 m=\frac1r\sum_{a=1}^r b(a),
\]
then, for real $1\leq u\leq v$ and a continuously differentiable function $F$ on $[u,v]$,
\[
 \left|\sum_{u<k\leq v}b(k)F(k)-m\int_u^v F(t)\,dt\right|
 \leq 4r\left(|F(v)|+\int_u^v|F'(t)|\,dt\right).
 \tag{6}
\]
To prove this, put
\[
 P(t)=\sum_{1\leq k\leq t}b(k)-mt.
\]
Writing $t=qr+s$, where $q=\lfloor t/r\rfloor$ and $0\leq s<r$, the $q$ complete periods cancel. The remaining sum has at most $r$ terms of modulus at most $1$, and $|ms|\leq r$. Hence $|P(t)|\leq 2r$. Consequently
\[
 D_u(t)=\sum_{u<k\leq t}b(k)-m(t-u)=P(t)-P(u)
 \quad\hbox{satisfies}\quad |D_u(t)|\leq 4r.
\]
Integration by parts gives the exact identity
\[
 \sum_{u<k\leq v}b(k)F(k)-m\int_u^vF(t)\,dt
 =F(v)D_u(v)-\int_u^vF'(t)D_u(t)\,dt,
\]
which proves (6), with the indicated convention at both endpoints.

For later use, (4) and (6) yield
\[
 \left|\sum_{z<k\leq y}b(k)\frac{f'(k)}{f(k)}
       -m\log(Y/Z)\right|
 \leq \frac{4Dr}{z}.
 \tag{7}
\]
Indeed, $|w(y)|\leq U/z$, while
\(
\int_z^y |w'(t)|\,dt\leq V/z.
\)
These bounds also cover $z=y$; in that case the two conclusions of P4 are immediate. We may henceforth take $z<y$.

## Spectral notation and the common density

Let $c_r(n)$, $\gamma(r)$, and $\lambda(r)$ have the meanings in P1. Since
\(
\lambda(r)=\varphi(r)\gamma(r)^2
\)
and $c_r(n)$ is a sum of $\varphi(r)$ complex numbers of modulus $1$,
\[
 |c_r(n)|\leq\varphi(r),\qquad
 \mathfrak S(n)=\sum_{r\geq 1}\lambda(r)\frac{c_r(n)}{\varphi(r)}.
 \tag{8}
\]
In particular, P1 gives absolute convergence, uniformly in $n\geq 1$, because $\sum_r\lambda(r)=c$.

For $h\geq 1$, define
\[
 \beta_r(h)=\frac1r\sum_{a=1}^r
           \frac{c_r(hf(a))}{\varphi(r)}.
 \tag{9}
\]
Thus $|\beta_r(h)|\leq 1$, and
\[
 \mathcal W(h):=\sum_{r\geq 1}\lambda(r)\beta_r(h)
 \tag{10}
\]
converges absolutely and uniformly in $h\geq 1$. We now prove that
\[
 \mathcal W(h)=W_f(h).
 \tag{11}
\]

For completeness, the elementary Ramanujan-sum identities needed here follow directly from finite sums. Inserting
\(
\mathbf 1_{(a,r)=1}=\sum_{b\mid(a,r)}\mu(b)
\)
into the definition of $c_r(n)$, and summing the resulting geometric progression, gives
\[
 c_r(n)
 =\sum_{b\mid r}\mu(b)
       \sum_{a'=1}^{r/b}\exp\!\left(\frac{2\pi i a'n}{r/b}\right)
 =\sum_{s\mid(r,n)}s\mu(r/s).
 \tag{12}
\]
Factoring this divisor sum over two coprime moduli shows that $c_{rs}(n)=c_r(n)c_s(n)$ when $(r,s)=1$. The Chinese remainder theorem, applied to the complete average in (9), therefore gives
\[
 \beta_{rs}(h)=\beta_r(h)\beta_s(h)\quad((r,s)=1).
 \tag{13}
\]
Here we also use $\varphi(rs)=\varphi(r)\varphi(s)$, which follows by counting invertible residue classes under the same bijection.

The function $\lambda(r)/c^2$ is multiplicative, is supported on integers with no prime cube divisor, and has prime-power values
\[
 \frac{\lambda(p)}{c^2}=\frac{p-1}{(p^2-1)^2},\qquad
 \frac{\lambda(p^2)}{c^2}=\frac{p^2-p}{(p^2-1)^2}.
 \tag{14}
\]
The absolute convergence in (10) and (13)--(14) permit its Euler product. Equations (12) give, for each integer $n$,
\[
 c_p(n)=p\mathbf 1_{p\mid n}-1,
 \qquad
 c_{p^2}(n)=p^2\mathbf 1_{p^2\mid n}-p\mathbf 1_{p\mid n},
\]
and hence
\[
 c_p(n)+c_{p^2}(n)=p^2\mathbf 1_{p^2\mid n}-1.
 \tag{15}
\]
Put
\[
 \delta_p(h)=\frac1{p^2}\#\{a\bmod p^2:p^2\mid hf(a)\}.
\]
The average defining $\beta_p(h)$ can also be taken modulo $p^2$, since its summand has period $p$. It follows from (14)--(15) that the local factor, before including the local factor of $c^2$, is
\[
 1+\frac{(p-1)\beta_p(h)+(p^2-p)\beta_{p^2}(h)}{(p^2-1)^2}
 =1+\frac{p^2\delta_p(h)-1}{(p^2-1)^2}.
 \tag{16}
\]

Write $j=\max\{2-v_p(h),0\}$. If $j=2$, the condition is $p^2\mid f(a)$, so there are $\rho(p^2)$ classes modulo $p^2$. If $j=1$, the condition is $p\mid f(a)$, and each of its $\rho(p)$ classes modulo $p$ has $p$ lifts modulo $p^2$. If $j=0$, every class is allowed. Using $\rho(1)=1$, the three cases give
\[
 \delta_p(h)=\frac{\rho(p^j)}{p^j},\qquad 0\leq\delta_p(h)\leq 1.
 \tag{17}
\]
No restriction on the coefficients of $f$ modulo $p$ has been used.

Unique factorization and the absolutely convergent geometric series for each prime give
\(
c^2=\prod_p(1-p^{-2})^2.
\)
Multiplying (16) by its local factor gives the exact identity
\[
 \begin{aligned}
 (1-p^{-2})^2
 \left(1+\frac{p^2\delta_p(h)-1}{(p^2-1)^2}\right)
 &=1-\frac2{p^2}+\frac{\delta_p(h)}{p^2}\\
 &=(1-2p^{-2})
       \left(1+\frac{\rho(p^{j_p(h)})}
       {p^{j_p(h)}(p^2-2)}\right).
 \end{aligned}
 \tag{18}
\]
This proves (11). All product rearrangements are absolute: the deviation from $1$ of the first expression on the right of (18) is at most $2/p^2$, and the added term in the second factor is at most
\(
1/(p^2-2)\leq 2/p^2.
\)
The sum of these bounds over primes is finite. This proves the asserted absolute convergence of $W_f(h)$. For the product defining $\mathfrak S(n)$, its local factor is
$1-2/p^2+\mathbf 1_{p^2\mid n}/p^2$, whose deviation from $1$ is at most $2/p^2$; its product therefore converges absolutely as well. Finally,
\[
 0\leq\frac{\rho(r)}r\leq 1,
 \qquad
 \sum_{r\geq 1}\lambda(r)\frac{\rho(r)}r
 \leq\sum_{r\geq 1}\lambda(r)=c,
 \tag{19}
\]
which proves absolute convergence of $R_f$.

For real $R\geq 2$, set
\[
 L_R=(\log(2R))^2,\qquad
 T_R=\sum_{r>R}\lambda(r),\qquad
 M_R=\sum_{r\leq R}r\lambda(r).
\]
By P1 there is an absolute $C_0>0$ such that
\[
 T_R\leq C_0R^{-1/2}L_R,
 \qquad M_R\leq C_0R^{1/2}L_R.
 \tag{20}
\]

## The first averaging assertion

For each positive integer $r$, the sequence
\(
b(k)=\mathbf 1_{r\mid f(k)}
\)
has period $r$, modulus at most $1$, and mean $\rho(r)/r$. Thus (7) gives
\[
 \sum_{z<k\leq y}\frac{f'(k)}{f(k)}\mathbf 1_{r\mid f(k)}
 =\frac{\rho(r)}r\log(Y/Z)+e_r,
 \qquad |e_r|\leq\frac{4Dr}{z}.
 \tag{21}
\]
The first identity for the squared densities in P1 applies to $q=f(k)$, which is a positive integer. Therefore, writing the expression to be estimated as $S_1$,
\[
 \begin{aligned}
 S_1
 &=\sum_{z<k\leq y}f'(k)\sum_{l=1}^{f(k)}g(f(k),l)^2\\
 &=\sum_{z<k\leq y}\frac{f'(k)}{f(k)}
                     \sum_{r\mid f(k)}\lambda(r).
 \end{aligned}
 \tag{22}
\]
The part in (22) with $r>R$ is nonnegative and at most
\[
 T_R\sum_{z<k\leq y}\frac{f'(k)}{f(k)}
 \leq 2U T_R\log(2x)
 \tag{23}
\]
by (5). This uses at most $\lfloor y\rfloor$ values of $k$; before summing, the bound for each such value is $T_R f'(k)/f(k)\leq U T_R/k$.

For $r\leq R$, there are $\lfloor R\rfloor$ indices. Before summing, the error after multiplication by $\lambda(r)$ in (21) is at most $4Dr\lambda(r)/z$. After summing it is at most $4DM_R/z$. Equations (21)--(23) consequently give
\[
 \left|S_1-\log(Y/Z)\sum_{r\leq R}\lambda(r)\frac{\rho(r)}r\right|
 \leq\frac{4DM_R}{z}+2U T_R\log(2x).
 \tag{24}
\]
For the infinite omitted part of the density coefficient, (19) gives the bound $\lambda(r)\log(Y/Z)$ at each index $r>R$, and summing gives
\[
 \log(Y/Z)\sum_{r>R}\lambda(r)\frac{\rho(r)}r
 \leq T_R\log(2x),
 \tag{25}
\]
since $2\leq Z\leq Y\leq x$. As $Z\leq Bz^d$, we have
\(
z^{-1}\leq B^{1/d}Z^{-1/d}.
\)
Combining (20), (24), and (25) proves the explicit bound
\[
 \boxed{
 |S_1-R_f\log(Y/Z)|
 \leq C_0\left(
 4DB^{1/d} Z^{-1/d}R^{1/2}L_R
 +(2U+1)R^{-1/2}L_R\log(2x)
 \right).}
 \tag{26}
\]

## A weight bound for the second assertion

Let
\[
 H=\left\lfloor\frac{x}{Z}\right\rfloor.
\]
Since $f'(t)\geq 1$, $f$ has a continuous increasing inverse on $[f(1),\infty)$. For $1\leq h\leq H$, define
\[
 v_h=\min\{y,f^{-1}(x/h)\},\qquad
 F_h(t)=f'(t)(x-hf(t))\quad(z\leq t\leq v_h).
 \tag{27}
\]
These definitions are valid because $x/h\geq Z=f(z)$. They give
\[
 z\leq v_h\leq (x/(ah))^{1/d},\qquad
 0\leq x-hf(t)\leq x\quad(z\leq t\leq v_h).
 \tag{28}
\]
Define a constant $K$ by
\[
 K=
 \begin{cases}
 B+B^2/a,&d=1,\\[2mm]
 B+B/(d-1)+B^2/((2d-1)a),&d\geq 2.
 \end{cases}
 \tag{29}
\]
We claim
\[
 |F_h(v_h)|+\int_z^{v_h}|F_h'(t)|\,dt
 \leq Kxv_h^{d-1}.
 \tag{30}
\]
For $d\geq 2$, (1)--(2) and (28) give
\[
 |F_h(v_h)|\leq Bxv_h^{d-1},
\]
and
\[
 \begin{aligned}
 \int_z^{v_h}|F_h'(t)|\,dt
 &\leq\int_z^{v_h}
       \left(|f''(t)|(x-hf(t))+h|f'(t)|^2\right)\,dt\\
 &\leq Bx\int_z^{v_h}t^{d-2}\,dt
       +hB^2\int_z^{v_h}t^{2d-2}\,dt\\
 &\leq\frac{B}{d-1}xv_h^{d-1}
       +\frac{hB^2}{2d-1}v_h^{2d-1}\\
 &\leq\left(\frac{B}{d-1}+\frac{B^2}{(2d-1)a}\right)
          xv_h^{d-1}.
 \end{aligned}
 \tag{31}
\]
The last inequality uses $hv_h^d\leq x/a$, from (28). For $d=1$, $f''=0$ gives
\[
 |F_h(v_h)|\leq Bx,\qquad
 \int_z^{v_h}|F_h'(t)|\,dt
 \leq hB^2(v_h-z)\leq hB^2v_h\leq B^2x/a.
 \tag{32}
\]
Thus (30) holds for every $d\geq 1$.

Apply (6) to
\(
b(k)=c_r(hf(k))/\varphi(r)
\)
with mean $\beta_r(h)$. This sequence has period $r$ because $f$ has integer coefficients. Equations (28)--(30) give
\[
 \begin{aligned}
 &\left|\sum_{z<k\leq v_h}
     f'(k)(x-hf(k))\frac{c_r(hf(k))}{\varphi(r)}
   -\beta_r(h)\int_z^{v_h}f'(u)(x-hf(u))\,du\right|\\
 &\hspace{15mm}\leq
 4Kr x v_h^{d-1}
 \leq 4K a^{-(d-1)/d} r x^{2-1/d}h^{-1+1/d}.
 \end{aligned}
 \tag{33}
\]
If $v_h=z$, the left side is zero and this bound still applies.

The $h$-sum has exactly $H\leq x/Z$ indices. The bound in (33) is the bound before summing. To sum it, the function $t^{-1+1/d}$ is nonincreasing and integrable on $(0,H]$, and therefore
\[
 \sum_{h=1}^{H}h^{-1+1/d}
 \leq\int_0^H t^{-1+1/d}\,dt
 =dH^{1/d}\leq d(x/Z)^{1/d}.
 \tag{34}
\]
This includes $d=1$, when the first inequality is equality. Combining (33)--(34), the error after summing over $h$ is at most
\[
 K_2 r x^2 Z^{-1/d},\qquad
 K_2=4Kd\,a^{-(d-1)/d}.
 \tag{35}
\]
In particular no logarithm is introduced by this sum.

## The second averaging assertion

Define the finite approximations
\[
 \mathfrak S_R(n)=\sum_{r\leq R}\lambda(r)
                         \frac{c_r(n)}{\varphi(r)},\qquad
 W_R(h)=\sum_{r\leq R}\lambda(r)\beta_r(h).
\]
Equations (8)--(11) give, uniformly for positive integers $n,h$,
\[
 |\mathfrak S(n)-\mathfrak S_R(n)|\leq T_R,
 \qquad |W_f(h)-W_R(h)|\leq T_R.
 \tag{36}
\]

Let $S_2$ denote the discrete expression in the second assertion and $I_2$ its integral expression. Define $S_{2,R}$ and $I_{2,R}$ by replacing $\mathfrak S$ and $W_f$ with $\mathfrak S_R$ and $W_R$, respectively.

For a fixed integer $k$ with $z<k\leq y$, there are
\(
H_k=\lfloor x/f(k)\rfloor\leq x/f(k)
\)
indices $h$. Before summing over $h$, the error from (36) is at most $T_R f'(k)(x-hf(k))\leq T_R x f'(k)$. After summing over these $H_k$ indices, it is at most
\(
T_R x^2 f'(k)/f(k).
\)
Summing this last bound over at most $\lfloor y\rfloor$ values of $k$ and using (5) gives
\[
 |S_2-S_{2,R}|\leq 2U T_R x^2\log(2x).
 \tag{37}
\]
For each $t\in[Z,Y]$, the $h$-sum has $\lfloor x/t\rfloor\leq x/t$ indices. Before summing, the error in an integrand term is at most $T_R(x-ht)\leq T_R x$. After summing it is at most $T_R x^2/t$. Integration gives
\[
 |I_2-I_{2,R}|
 \leq T_R x^2\int_Z^Y\frac{dt}{t}
 =T_R x^2\log(Y/Z)
 \leq T_R x^2\log(2x).
 \tag{38}
\]

It remains to compare the finite approximations. All relevant sums are finite, so their orders can be interchanged. The change of variables $t=f(u)$ gives, for each $h\leq H$,
\[
 \int_z^{v_h}f'(u)(x-hf(u))\,du
 =\int_Z^{\min\{Y,x/h\}}(x-ht)\,dt.
 \tag{39}
\]
Moreover, for integer $k$ in $(z,y]$, the condition $h\leq x/f(k)$ is equivalent to $k\leq v_h$. Thus (35) compares the entire $h$-sum at a fixed $r$ in $S_{2,R}$ with its counterpart in $I_{2,R}$. Before summing over $r$, its error after multiplication by $\lambda(r)$ is at most
\(
K_2r\lambda(r)x^2 Z^{-1/d}.
\)
There are $\lfloor R\rfloor$ indices $r\leq R$; after summing, (20) gives
\[
 |S_{2,R}-I_{2,R}|
 \leq K_2x^2Z^{-1/d}M_R
 \leq C_0K_2 x^2 Z^{-1/d}R^{1/2}L_R.
 \tag{40}
\]
Combining (20) and (37)--(40) proves
\[
 \boxed{
 |S_2-I_2|
 \leq C_0 x^2\left(
 K_2 Z^{-1/d}R^{1/2}L_R
 +(2U+1)R^{-1/2}L_R\log(2x)
 \right).}
 \tag{41}
\]

Finally, set
\[
 C(f)=C_0\max\{4DB^{1/d},\ K_2,\ 2U+1\}.
\]
With $A$ as in the statement, (26) is the first asserted inequality with right side $C(f)A$, and (41) is the second with right side $C(f)x^2A$. All constants are independent of $x,z,y,R$. Every estimate above is valid on the full stated ranges, including $d=1$ and polynomials with arbitrary content, discriminant, or factorization.

## Numerical sanity checks and source record

A Python check using exact rational arithmetic verified (18) for $p=2,3,5,7,11$ and each of the test densities $0,p^{-2},p^{-1},1$. A separate floating-point check verified the bound (34) for $d=1,\ldots,8$ and $H=1,2,10,1000$. These checks were only sanity checks; (18) and (34) were proved algebraically and by integration above.

The only assumed proposition is the supplied P1. No published source or other run's artifacts were consulted; no excluded source was encountered. There were no supplied objections or previous-proof artifacts for this attempt.
