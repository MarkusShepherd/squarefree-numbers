# Proof of P5: sawtooth sums $B(Z/t^2)$ with multiplicative weights

No external result is used except the classical analytic continuation of $\zeta$ (derived below from Euler–Maclaurin, cf. Montgomery–Vaughan, *Multiplicative Number Theory I* (2007), Thm. B.5 and §1.3) and the bound $2^{\omega(q)}\ll_\varepsilon q^\varepsilon$. Nothing from the excluded sources was used.

Notation: $B(u)=\{u\}(1-\{u\})\in[0,\tfrac14]$ (1-periodic, continuous); $\psi(u)=\{u\}-\tfrac12$; $\psi_2(u)=\tfrac12(\{u\}^2-\{u\})+\tfrac1{12}=\tfrac1{12}-\tfrac12B(u)$. Then $\psi_2$ is continuous, 1-periodic, $\psi_2'=\psi$ off the integers, $|\psi_2|\le\frac1{12}$, $\psi_2(n)=\frac1{12}$ for $n\in\mathbb Z$, and $|\psi|\le\frac12$, $\psi(n)=-\frac12$.

## 0. Euler–Maclaurin in the form used

**Lemma EM.** Let $a<b$ be reals, $F\in C^2[a,b]$. Then
$$\sum_{a<n\le b}F(n)=\int_a^bF\,du+\psi(a)F(a)-\psi(b)F(b)-\psi_2(a)F'(a)+\psi_2(b)F'(b)-\int_a^b\psi_2(u)F''(u)\,du .$$
*Proof.* $\lfloor u\rfloor=u-\frac12-\psi(u)$, so $\sum_{a<n\le b}F(n)=\int_{(a,b]}F\,d\lfloor u\rfloor=\int_a^bF\,du-\int_{(a,b]}F\,d\psi$. As $\psi$ is right-continuous of bounded variation and $F$ is continuous, $\int_{(a,b]}F\,d\psi=F(b)\psi(b)-F(a)\psi(a)-\int_a^b\psi F'\,du$. Finally $\int_a^b\psi F'=[\psi_2F']_a^b-\int_a^b\psi_2F''$. $\square$ (Check: $F\equiv1$ gives $\lfloor b\rfloor-\lfloor a\rfloor$.) If $b=\infty$ and $F,F'\to0$, $F''\in L^1$, the same holds with the terms at $b$ dropped.

## (a) The value of $I$

Substituting $v=u^{-2}$, $du=-\frac12v^{-3/2}dv$ gives $I=\frac12\int_0^\infty B(v)v^{-3/2}dv$. This converges: $B(v)\le v$ near $0$ and $B\le\frac14$, $\int^\infty v^{-3/2}<\infty$ at infinity. So $I$ is finite and the first equality holds.

*Value.* $B$ is continuous and piecewise $C^1$ with $B'(v)=1-2\{v\}$. Integrating by parts on $[0,X]$,
$\int_0^XB\,v^{-3/2}dv=[-2Bv^{-1/2}]_0^X+2\int_0^XB'v^{-1/2}dv$. The boundary term tends to $0$ ($B(v)v^{-1/2}\le v^{1/2}$ at $0$; $\le\frac12X^{-1/2}$ at $X$). Hence $\int_0^\infty Bv^{-3/2}=2\lim_N\int_0^NB'v^{-1/2}dv$ ($N\in\mathbb N$), the limit existing since the integral on the left converges.
On $(n,n+1)$ we have $B'(n^+)=1$, $B'((n+1)^-)=-1$, $B''=-2$, so integrating by parts with the antiderivative $2v^{1/2}$,
$$\int_n^{n+1}B'v^{-1/2}dv=-2(n+1)^{1/2}-2n^{1/2}+4\int_n^{n+1}v^{1/2}dv .$$
Summing over $0\le n\le N-1$:
$$\int_0^NB'v^{-1/2}dv=-4\sum_{m=1}^{N}m^{1/2}+2N^{1/2}+\tfrac83N^{3/2}.$$
Now apply Lemma EM on $(N,\infty)$ with $F(u)=u^{-s}$, $\sigma>1$ (with $\psi(N)=-\frac12,\ \psi_2(N)=\frac1{12}$):
$$\sum_{n>N}n^{-s}=\frac{N^{1-s}}{s-1}-\frac{N^{-s}}2+\frac{s}{12}N^{-s-1}-s(s+1)\int_N^\infty\psi_2(u)u^{-s-2}du.$$
The right side is analytic in $\sigma>-1$, $s\neq1$; by analytic continuation, $\zeta(s)=\sum_{n\le N}n^{-s}+\text{RHS}$ there. At $s=-\frac12$ (where $s(s+1)=-\frac14$, and $|\int_N^\infty\psi_2u^{-3/2}du|\le\frac1{12}\cdot2N^{-1/2}$):
$$\sum_{m\le N}m^{1/2}=\zeta(-\tfrac12)+\tfrac23N^{3/2}+\tfrac12N^{1/2}+O(N^{-1/2}).$$
Inserting: $\int_0^NB'v^{-1/2}dv=-4\zeta(-\frac12)-\frac83N^{3/2}-2N^{1/2}+2N^{1/2}+\frac83N^{3/2}+O(N^{-1/2})\to-4\zeta(-\tfrac12)$.
Therefore $\int_0^\infty Bv^{-3/2}dv=-8\zeta(-\frac12)$ and $I=-4\zeta(-\frac12)$.

*Numerical check (Python/mpmath):* $-4\zeta(-1/2)=0.8315448999\ldots$ (matches the stated value), and $\frac12\int_0^{400}B(v)v^{-3/2}dv=0.82321$, with tail $\approx\frac12\cdot\frac16\cdot2\cdot400^{-1/2}=0.00833$, total $0.83154$. $\square$

Also, for $Z>0$, $u=\sqrt Z\,w$ gives
$$\int_0^\infty B(Z/u^2)\,du=I\sqrt Z.\tag{0.1}$$

## (b) $\bigl|\sum_{s\ge1}B(Z/s^2)-I\sqrt Z\bigr|\le c_1Z^{1/3}$

I show this with $c_1=60$.

**Case $Z<1$.** $0\le B(Z/s^2)\le Z/s^2$, so $0\le\sum_sB(Z/s^2)\le\zeta(2)Z<2Z\le2Z^{1/3}$, and $0<I\sqrt Z\le IZ^{1/3}<Z^{1/3}$ ($I<1$). The difference of two numbers in $[0,2Z^{1/3}]$ is at most $2Z^{1/3}$.

**Case $Z\ge1$.** Put $\Lambda=Z^{1/3}\ge1$, $T=\lfloor\Lambda\rfloor\ge1$. Since $T+1>\Lambda$ and $T+1\le2T$, we have $\Lambda/2<T\le\Lambda$, hence
$$\frac Z{T^3}<8,\qquad K_0:=\frac Z{T^2}<4\Lambda,\qquad\frac{Z^2}{T^5}<32\Lambda.\tag{b.1}$$
(Indeed $Z/T^3<\Lambda^3/(\Lambda/2)^3=8$; $Z/T^2<\Lambda^3/(\Lambda^2/4)=4\Lambda$; $Z^2/T^5<\Lambda^6\cdot32/\Lambda^5$.)

*Small $s$.* $\sum_{s\le T}B(Z/s^2)\le T/4\le\Lambda/4$ and by (0.1) $0\le\int_0^TB(Z/u^2)du\le T/4\le\Lambda/4$. So it suffices to show
$$\Bigl|\sum_{s>T}B(Z/s^2)-\int_T^\infty B(Z/u^2)du\Bigr|\le 57\Lambda,\tag{b.2}$$
which gives $|\sum_sB(Z/s^2)-I\sqrt Z|\le57\Lambda+\Lambda/2\le60\Lambda$.

*Decomposition.* For real $x\ge0$ with $m=\lfloor x\rfloor$: $B(x)=(x-m)(1-x+m)=x-x^2+2mx-m-m^2$, and $\sum_{k=1}^{m}2(x-k)=2mx-m^2-m$. Hence
$$B(x)=x-x^2+2\sum_{k\ge1}(x-k)_+,\qquad(y)_+=\max(y,0).$$
Put $A(u)=Z/u^2-Z^2/u^4$ and $G_k(u)=(Z/u^2-k)_+$. Then $B(Z/u^2)=A(u)+2\sum_{k\ge1}G_k(u)$. For $u\ge T$ only $k<K_0$ contribute ($G_k(u)\le(Z/T^2-k)_+$), so at most $K_0<4\Lambda$ values of $k$ occur. For such $k$, $G_k(u)=Z/u^2-k$ for $T\le u\le R_k:=\sqrt{Z/k}$ (note $R_k>T$) and $0$ beyond.

*Apply Lemma EM.* With $F=A$ on $(T,\infty)$ and with $F=Z/u^2-k$ on $(T,R_k]$, using $\psi(T)=-\frac12$, $\psi_2(T)=\frac1{12}$, $G_k(R_k)=0$, and adding (the $k$-sum is finite):
$$\sum_{s>T}B(Z/s^2)=\int_T^\infty B(Z/u^2)du+E_1+E_2+E_3+E_4+E_5,$$
where (writing $G_k'$, $G_k''$ for the derivatives of $Z/u^2-k$)

* $E_1=\psi(T)\bigl[A(T)+2\sum_{k<K_0}G_k(T)\bigr]=\psi(T)B(Z/T^2)$, by the decomposition at $u=T$. **This is the one place where cancellation is essential:** the individual terms are of size $Z^2/T^4\asymp Z^{2/3}$, but their sum is $\le\frac12\cdot\frac14$. So $|E_1|\le\frac18$.
* $E_2=-\frac1{12}\bigl[A'(T)+2\sum_{k<K_0}G_k'(T)\bigr]$. Here $A'(T)=-2Z/T^3+4Z^2/T^5$, $G_k'(T)=-2Z/T^3$. By (b.1), $|A'(T)|<16+128\Lambda$, $|2\sum_kG_k'(T)|\le4K_0Z/T^3<4\cdot4\Lambda\cdot8=128\Lambda$. So $|E_2|\le\frac1{12}(16+256\Lambda)\le\frac{272}{12}\Lambda$.
* $E_3=-\int_T^\infty\psi_2A''du$, $A''=6Z/u^4-20Z^2/u^6$, so $|E_3|\le\frac1{12}\bigl(2Z/T^3+4Z^2/T^5\bigr)<\frac1{12}(16+128\Lambda)\le12\Lambda$.
* $E_4=-2\sum_{k<K_0}\int_T^{R_k}\psi_2G_k''du$, with $G_k''=6Z/u^4$ and $\int_T^\infty6Z/u^4\,du=2Z/T^3<16$. So $|E_4|\le2\cdot\frac1{12}\cdot K_0\cdot16<\frac2{12}\cdot4\Lambda\cdot16=\frac{32}3\Lambda$.
* $E_5=2\sum_{k<K_0}\psi_2(R_k)G_k'(R_k)$, $G_k'(R_k)=-2Z/R_k^3=-2k^{3/2}/\sqrt Z$. Since $k<K_0<4\Lambda$: $k^{3/2}<8\Lambda^{3/2}$, so $\sum_{k<K_0}k^{3/2}<4\Lambda\cdot8\Lambda^{3/2}=32\Lambda^{5/2}$, and with $\sqrt Z=\Lambda^{3/2}$: $|E_5|\le2\cdot\frac1{12}\cdot2\cdot\frac{32\Lambda^{5/2}}{\Lambda^{3/2}}=\frac{32}3\Lambda$. (This is the kink of $G_k$ at $R_k$; summing over $K_0\ll Z^{1/3}$ values of $k$ is exactly what produces the exponent $\frac13$.)

Also $\int_T^\infty G_k=\int_T^{R_k}G_k$ and $\sum_k$ over $k\ge K_0$ gives $0$, so $\int_T^\infty[A+2\sum_kG_k]=\int_T^\infty B(Z/u^2)du$ (all integrals converge absolutely).

Total: $|E_1|+\dots+|E_5|\le\Lambda\bigl(\tfrac18+\tfrac{272}{12}+12+\tfrac{32}3+\tfrac{32}3\bigr)<57\Lambda$ (using $\Lambda\ge1$ for $E_1$): $0.125+22.67+12+10.67+10.67=56.1$. This is (b.2). $\square$

*Numerical check:* $(\sum_sB(Z/s^2)-I\sqrt Z)/Z^{1/3}$ for $Z=1.5,\,10,\dots,10^7$ lies in $[-0.16,0.02]$.

## (c) Weighted version

Fix $q\in\mathbb N$ and put $f(t)=\kappa(t)\mathbf 1_{(t,q)=1}$. It is multiplicative with $f(p)=\frac{p^2}{p^2-2}$ for $p\nmid q$, $f(p)=0$ for $p\mid q$, and $f(p^j)=0$ for $j\ge2$. In particular $0\le f\le C_0:=\prod_p(1+\frac2{p^2-2})<\infty$.

**Convolution.** Let $b=\mu*f$, i.e. $f=1*b$. $b$ is multiplicative, with $b(p^j)=f(p^j)-f(p^{j-1})$:
* $p\mid q$: $b(p)=-1$, $b(p^j)=0$ ($j\ge2$);
* $p\nmid q$: $b(p)=\frac{2}{p^2-2}$, $b(p^2)=-\frac{p^2}{p^2-2}$, $b(p^j)=0$ ($j\ge3$).

*Absolute convergence.* $\sum_d|b(d)|d^{-\alpha}=\prod_p\bigl(1+\sum_{j}|b(p^j)|p^{-j\alpha}\bigr)$. For $\alpha=\frac23$:
$$\Sigma_{2/3}:=\sum_d\frac{|b(d)|}{d^{2/3}}=\prod_{p\mid q}(1+p^{-2/3})\prod_{p\nmid q}\Bigl(1+\frac{2p^{-2/3}}{p^2-2}+\frac{p^2}{p^2-2}p^{-4/3}\Bigr).$$
For $p\nmid q$ the factor is $\le1+\frac{2}{p^2-2}p^{-2/3}+2p^{-4/3}$ (as $\frac{p^2}{p^2-2}\le2$), and $\sum_pp^{-4/3}<\infty$, $\sum_p\frac1{p^2-2}<\infty$. Hence the product over $p\nmid q$ is bounded by an absolute constant $C_1$ (independent of $q$), and
$$\Sigma_{2/3}\le C_1\prod_{p\mid q}(1+p^{-2/3})\le C_1\,2^{\omega(q)}\le C(\varepsilon)\,q^{\varepsilon}$$
by the standard bound $2^{\omega(q)}\le d(q)\ll_\varepsilon q^\varepsilon$. Likewise ($\alpha=1$) $\sum_d|b(d)|/d<\infty$ (the $p\mid q$ factors are finite in number for fixed $q$; the $p\nmid q$ factors are $1+O(p^{-2})$).

**Rearrangement.** For $Z>0$ let $S(W)=\sum_{m\ge1}B(W/m^2)$. Then
$$\sum_{t\ge1}f(t)B(Z/t^2)=\sum_{d,m\ge1}b(d)\,B\!\Bigl(\frac{Z/d^2}{m^2}\Bigr)=\sum_db(d)\,S(Z/d^2).$$
The interchange is justified by absolute convergence. For $W>0$, $\sum_m B(W/m^2)\le\sum_m\min(\frac14,W/m^2)\le3\sqrt W$: for $W<1$ the sum is $\le\zeta(2)W\le2\sqrt W$; for $W\ge1$, $\sum_{m\le\sqrt W}\frac14\le\frac14\sqrt W$ and $\sum_{m>\sqrt W}W/m^2\le W\cdot\frac{2}{\sqrt W}=2\sqrt W$ (as $\sum_{m>x}m^{-2}\le1/\lfloor x\rfloor\le2/x$ for $x\ge1$). With $W=Z/d^2$, $\sum_{d,m}|b(d)|B(Z/(dm)^2)\le3\sqrt Z\sum_d|b(d)|/d<\infty$. Also the left side converges since $0\le f\le C_0$ and $B(Z/t^2)\le Z/t^2$.

**Main term.** By (b) applied with $Z/d^2$ in place of $Z$ (it holds for every real positive argument), and $I\sqrt{Z/d^2}=I\sqrt Z/d$,
$$\Bigl|\sum_tf(t)B(Z/t^2)-I\sqrt Z\sum_d\frac{b(d)}d\Bigr|\le\sum_d|b(d)|\,c_1\Bigl(\frac Z{d^2}\Bigr)^{1/3}=c_1\Sigma_{2/3}Z^{1/3}\le c_1C(\varepsilon)q^\varepsilon Z^{1/3}.$$

**Identification of the constant.** $\sum_d b(d)/d$ converges absolutely, so equals the Euler product $\prod_p(1+\sum_jb(p^j)p^{-j})$:
* $p\mid q$: $1-\frac1p=(1-\frac1p)\cdot1$.
* $p\nmid q$: $1+\frac{2}{p(p^2-2)}-\frac1{p^2-2}=\frac{p^3-3p+2}{p(p^2-2)}=\frac{(p-1)^2(p+2)}{p(p^2-2)}$, while $(1-\frac1p)\bigl(1+\frac p{p^2-2}\bigr)=\frac{p-1}p\cdot\frac{p^2+p-2}{p^2-2}=\frac{(p-1)^2(p+2)}{p(p^2-2)}$. ✓.

So $\sum_db(d)/d=\prod_p(1-\frac1p)\bigl(1+\mathbf 1[p\nmid q]\frac p{p^2-2}\bigr)=\delta_q$. (The factors for $p\nmid q$ equal $1+O(p^{-2})$, from the formula $\frac{(p-1)^2(p+2)}{p(p^2-2)}=1+O(p^{-2})$, so the product converges absolutely, as claimed in the statement.) Hence
$$\Bigl|\sum_{(t,q)=1}\kappa(t)B(Z/t^2)-\delta_qI\sqrt Z\Bigr|\le c_1C(\varepsilon)\,q^\varepsilon Z^{1/3}.$$
Note $\kappa$ already contains $\mu^2(t)$, which is built into $f$ (vanishing on non-squarefree $t$). $\square$

*Numerical check:* for $q=1,6,30$ and $Z=10^4,10^6,10^8$ the quantity $(\sum_{(t,q)=1}\kappa(t)B(Z/t^2)-\delta_qI\sqrt Z)/Z^{1/3}$ (truncated at $t\le3\cdot10^6$, $\delta_q$ computed from primes $<10^6$) lies in $[-0.06,0.002]$.
