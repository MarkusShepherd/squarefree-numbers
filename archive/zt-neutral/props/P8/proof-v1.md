# Proof of P8 (averages over polynomial moduli)

No dependencies and no papers are needed beyond standard facts: the functional equation of $\zeta$ (Riemann; e.g. Montgomery–Vaughan, *Multiplicative Number Theory I*, 2007, Ch. 10), the divisor bound $\tau(n)\ll_\varepsilon n^{\varepsilon}$, and the Chinese remainder theorem. Nothing by the excluded authors was used.

Throughout, $p$ denotes a prime, $c_0:=-4\zeta(-1/2)$, and
$$A_p=1-\tfrac3{p^2}+\tfrac2{p^3},\quad B_p=\tfrac{(p-1)(p^2-2+\sqrt p)}{p^3},\quad D_p=\tfrac{(p-1)^2(p+1)}{p^3}.$$
Then $h(q)=c_0\prod_p a_p(v_p(q))$ with $a_p(0)=A_p$, $a_p(1)=B_p$, $a_p(v)=D_p$ for $v\ge2$. Write $f(t)=a\,t^d+\dots$ with $a\ge1$.

## 0. Preliminaries

**Sign of $c_0$.** By the functional equation $\zeta(s)=2^s\pi^{s-1}\sin(\pi s/2)\Gamma(1-s)\zeta(1-s)$ at $s=-1/2$:
$\zeta(-1/2)=2^{-1/2}\pi^{-3/2}\sin(-\pi/4)\Gamma(3/2)\zeta(3/2)=-\zeta(3/2)/(4\pi)<0$, since $\zeta(3/2)>0$. So $c_0=\zeta(3/2)/\pi>0$. (Numerically $\zeta(-1/2)=-0.2078862\ldots$, matching $-\zeta(3/2)/(4\pi)$; checked with mpmath.)

**Elementary identities** (verified symbolically with sympy, and by hand):
$$A_p=\frac{(p-1)^2(p+2)}{p^3},\qquad B_p-A_p=-\frac1p+p^{-3/2}+p^{-2}-p^{-5/2},\qquad D_p-B_p=-p^{-3/2}(1-p^{-1/2})(1-p^{-1}).$$
Consequently, for all primes $p$:

* $A_p,B_p,D_p>0$ (for $B_p$: $p^2-2+\sqrt p>0$). Also $A_2=\frac12$ and $A_p\ge 1-3/p^2\ge\frac23$ for $p\ge3$, so $A_p\ge\frac12$, and $0<1-A_p\le 3/p^2$.
* $|B_p-A_p|\le 1/p$, because $-1/p+p^{-3/2}\in(-1/p,0)$ and $p^{-2}-p^{-5/2}\in[0,p^{-2})$.
* $-p^{-3/2}<D_p-B_p<0$.

**The function $\rho$.** By the Chinese remainder theorem $\rho$ is multiplicative. Let $P_0$ be the finite set of primes dividing the content of $f$.

* For $p\notin P_0$, $f\bmod p$ is a nonzero polynomial of degree $\le d$, so $\rho(p)\le d$.
* Every root mod $p$ has exactly $p$ lifts mod $p^2$, so $\rho(p^2)\le p\rho(p)$ for all $p$.
* Trivially $\rho(p^j)\le p^j$.

**Shape of $F$.** For $t\ge1$ we have $f(t)>0$, $f'(t)>0$, and $f(t)\sim at^d$, $f'(t)\sim adt^{d-1}$. Hence there are constants $0<c_1\le c_2$, depending only on $f$, with
$$c_1t^d\le f(t)\le c_2t^d,\qquad c_1t^{d-1}\le f'(t)\le c_2t^{d-1},\qquad c_1t^{3d/2-1}\le F(t)\le c_2t^{3d/2-1}\quad(t\ge1).\tag{0.1}$$
Consequences for $y\ge1$, $Y=f(y)$:

* $\sup_{[1,y]}F\le (c_2/c_1)F(y)=:c_3F(y)$.
* $F(y)\asymp Y^{3/2}/y$.
* $y\le Y/c_1$ (as $y^d \ge y$).

Moreover $F'=P/(2\sqrt f)$ with $P=2ff''+f'^2$ a polynomial of degree $2d-2$ and leading coefficient $a^2d(3d-2)>0$. (For $d=1$, $P=a^2$.) So $P$ is a nonzero polynomial with at most $2d-2$ real zeros, and $[1,\infty)$ splits into $\le 2d-1$ intervals on each of which $F$ is monotone. Finally $\int_1^yF=\frac23\bigl(Y^{3/2}-f(1)^{3/2}\bigr)$ because $(f^{3/2})'=\frac32 f'f^{1/2}$.

## 1. Claim (0)

Let $x_p=\rho(p)/p$ and $z_p=\rho(p^2)/p^2$. Then $0\le z_p\le x_p\le1$, since $\rho(p^2)\le p\rho(p)$. These are the densities of the events $p\nmid f(k)$, $p\| f(k)$ and $p^2\mid f(k)$ for $k$ in a residue class mod $p^2$:

* $p\nmid f(k)$ has density $1-x_p$.
* $p\mid f(k)$ has density $x_p$.
* $p^2\mid f(k)$ has density $z_p$.

Then
$$\tau_p=A_p(1-x_p)+B_p(x_p-z_p)+D_pz_p$$
is a convex combination of $A_p,B_p,D_p>0$, so $\tau_p\ge\min(A_p,B_p,D_p)>0$.

Also $\tau_p=A_p+(B_p-A_p)x_p+(D_p-B_p)z_p$, so for $p\notin P_0$ (using $x_p\le d/p$, $z_p\le d/p$)
$$|\tau_p-1|\le (1-A_p)+\frac1p\cdot\frac dp+p^{-3/2}\cdot\frac dp\le \frac{3+2d}{p^{2}}.$$
Thus $\sum_p|\tau_p-1|<\infty$. Hence $\sum_p|\log\tau_p|<\infty$ (all $\tau_p>0$, and $|\log(1+x)|\le2|x|$ for $|x|\le\frac12$, which excludes only finitely many $p$). So $\prod_p\tau_p$ converges absolutely to a positive finite number. Similarly $A:=\prod_pA_p\in(0,1)$. With $c_0>0$ this gives $0<C_f=\frac23c_0\prod_p\tau_p<\infty$. $\square$

## 2. Claims (b), (c)

By (0.1), for $1\le k\le y$: $f'(k)/f(k)\le (c_2/c_1)/k$ and $f'(k)\le c_2k^{d-1}$. Hence
$$\sum_{k\le y}\frac{f'(k)}{f(k)}\le \frac{c_2}{c_1}(1+\log y)\le \frac{c_2}{c_1}\bigl(1+\log Y+\log(1/c_1)\bigr)\le c(f)(1+\log Y),$$
using $y\le Y/c_1$ and $1+\log Y\ge1$ (as $Y\ge2$). Also
$$\sum_{k\le y}f'(k)\le c_2\,y\cdot y^{d-1}=c_2y^d\le (c_2/c_1)Y.\qquad\square$$

## 3. Claim (a)

### 3.1 Reduction to a divisor sum

Put $b(q)=\prod_{p\mid q}a_p(v_p(q))/A_p$. Then $\prod_pa_p(v_p(q))=A\,b(q)$, so $h(q)=c_0A\,b(q)$ and
$$\sum_{k\le y}F(k)h(f(k))=c_0A\,S,\qquad S:=\sum_{k\le y}F(k)b(f(k)).$$

$b$ is multiplicative, with $b(p)=B_p/A_p$ and $b(p^j)=D_p/A_p$ for $j\ge2$. Let $u=b*\mu$, which is multiplicative, so $b(q)=\sum_{e\mid q}u(e)$. Then
$$u(p)=\frac{B_p-A_p}{A_p},\quad u(p^2)=\frac{D_p-B_p}{A_p},\quad u(p^j)=0\ (j\ge3).$$
From §0 and $A_p\ge\frac12$:
$$|u(p)|\le \frac2p,\qquad|u(p^2)|\le 2p^{-3/2}.\tag{3.1}$$

So $u(e)=0$ unless $e$ is cube-free. Each cube-free $e$ is uniquely $e=ab^2$ with $a,b$ squarefree and coprime. By (3.1), and since $2/p\le 4p^{-3/4}$ and $2p^{-3/2}=2(p^2)^{-3/4}$,
$$|u(e)|\le 4^{\omega(e)}e^{-3/4}\qquad(\text{all }e),\tag{3.2}$$
$$|u(e)|\le 2^{\omega(e)}a^{-1}b^{-3/2}\qquad(e=ab^2).\tag{3.3}$$
For cube-free $e=ab^2$, the bounds on $\rho$ give $\rho(e)=\prod\rho(p^{v_p(e)})\le C_1d^{\omega(e)}b$, where $C_1=\prod_{p\in P_0}p^2$. Here $\rho(p)\le d$ for $p\|e$, $\rho(p^2)\le pd$ for $p^2\|e$, and a factor $\le p^2$ for $p\in P_0$ (for those $p$ we may also drop the factor $p\ge1$ from $b$). With (3.3),
$$|u(e)|\rho(e)\le C_1(2d)^{\omega(e)}a^{-1}b^{-1/2},\qquad \frac{|u(e)|\rho(e)}{e}\le C_1(2d)^{\omega(e)}a^{-2}b^{-5/2}.\tag{3.4}$$

### 3.2 Three estimates on $u$ and $\rho$

**(i) Tail.** For $E\ge1$, by Rankin's trick with $e^{1/2}/E^{1/2}\ge1$ for $e>E$, and (3.4) (note $(2d)^{\omega(e)}\le(2d)^{\omega(a)}(2d)^{\omega(b)}$ and $e^{1/2}=a^{1/2}b$):
$$\sum_{e>E}\frac{|u(e)|\rho(e)}{e}\le E^{-1/2}C_1\sum_{a,b\text{ sqfree}}(2d)^{\omega(a)+\omega(b)}a^{-3/2}b^{-3/2}=E^{-1/2}C_1\Bigl(\prod_p\bigl(1+2dp^{-3/2}\bigr)\Bigr)^2=:c_4E^{-1/2}.\tag{3.5}$$
In particular $\sum_e|u(e)|\rho(e)/e<\infty$.

**(ii) Short sum.** Using $(2d)^{\omega(n)}\le C_\varepsilon n^\varepsilon$ and (3.4),
$$\sum_{e\le E}|u(e)|\rho(e)\le C_1C_\varepsilon E^{\varepsilon}\sum_{a\le E}\frac1a\sum_{b\le E^{1/2}}b^{-1/2}\le C_1C_\varepsilon E^\varepsilon(1+\log E)\cdot2E^{1/4}\ll_{f,\varepsilon}E^{1/4+2\varepsilon}.\tag{3.6}$$

**(iii) Euler product.** The multiplicative function $e\mapsto u(e)\rho(e)/e$ has absolutely convergent sum by (3.5). So
$$\sum_e\frac{u(e)\rho(e)}{e}=\prod_p\Bigl(1+u(p)x_p+u(p^2)z_p\Bigr).$$
Now $1+u(p)x_p+u(p^2)z_p=1+\frac{B_p-A_p}{A_p}x_p+\frac{D_p-B_p}{A_p}z_p=\tau_p/A_p$ by the second formula for $\tau_p$ in §1. Hence
$$\sum_e\frac{u(e)\rho(e)}e=\prod_p\frac{\tau_p}{A_p}=\frac1A\prod_p\tau_p.\tag{3.7}$$
(The product converges as $\prod\tau_p$ and $\prod A_p$ both converge absolutely and are nonzero.)

### 3.3 Truncation of the divisor sum

Take $E=y$ and write $b(f(k))=\sum_{e\mid f(k),\,e\le y}u(e)+T_k$ with $T_k=\sum_{e\mid f(k),\,e>y}u(e)$. By (3.2), for $e>y$, $|u(e)|\le 4^{\omega(e)}y^{-3/4}$. Since $4^{\omega(e)}\le\tau(e)^2$, we have $\sum_{e\mid n}4^{\omega(e)}\le\tau(n)^3\le C_\varepsilon n^{\varepsilon}$. Thus
$$|T_k|\le y^{-3/4}C_\varepsilon f(k)^\varepsilon\le C_\varepsilon y^{-3/4}Y^\varepsilon\quad(k\le y;\ f\text{ increasing}).$$
By (0.1), $\sum_{k\le y}F(k)\le yc_3F(y)\le c_5Y^{3/2}$ (using $F(y)\ll Y^{3/2}/y$). So
$$\Bigl|\sum_{k\le y}F(k)T_k\Bigr|\le C_\varepsilon c_5\,Y^{3/2+\varepsilon}y^{-3/4}.\tag{3.8}$$
(This is stronger than needed since $y^{-3/4}\le y^{-1/2}$.)

### 3.4 Counting in residue classes

For $e\le y$ let $N(e)=\sum_{k\le y,\ e\mid f(k)}F(k)=\sum_{r\bmod e,\ f(r)\equiv0}\ \sum_{1\le k\le y,\ k\equiv r(e)}F(k)$, a sum over $\rho(e)$ classes.

**Lemma.** Let $G\ge 0$ be monotone on an interval $I=(\alpha,\beta]$ and let $k_1<\dots<k_n$ be the points of $I$ in a fixed residue class mod $e$. Then $|\sum_jG(k_j)-\frac1e\int_IG|\le3\sup_IG$.

*Proof.* If $G$ is nonincreasing, then $G(k_{j+1})\le\frac1e\int_{k_j}^{k_{j+1}}G\le G(k_j)$. Summing over $j<n$ gives $\sum_{j}G(k_j)-G(k_1)\le\frac1e\int_{k_1}^{k_n}G\le\sum_jG(k_j)-G(k_n)$. So $|\sum_jG(k_j)-\frac1e\int_{k_1}^{k_n}G|\le\sup G$. The remaining pieces $(\alpha,k_1]$, $(k_n,\beta]$ have length $\le e$, so contribute $\le\sup G$ each to $\frac1e\int$. If $n=0$, then $|I|\le e$ and $\frac1e\int_IG\le\sup G$. The nondecreasing case is symmetric. $\square$

Split $[1,y]$ into at most $2d-1$ intervals of monotonicity of $F$ (§0), made half-open so that each integer lies in exactly one. The first interval is closed, which only adds the point $1$, handled identically by treating $[1,\beta]$ as $(1-\delta,\beta]$ with $\delta<1$. By the Lemma, for each residue class,
$$\Bigl|\sum_{k\le y,\ k\equiv r(e)}F(k)-\frac1e\int_1^yF\Bigr|\le3(2d-1)\sup_{[1,y]}F\le3(2d-1)c_3F(y).$$
Summing over the $\rho(e)$ classes,
$$N(e)=\frac{\rho(e)}e\cdot\frac23\bigl(Y^{3/2}-f(1)^{3/2}\bigr)+\theta_e\,6d\,c_3\rho(e)F(y),\qquad|\theta_e|\le1.\tag{3.9}$$

### 3.5 Assembly

Since $S=\sum_{e\le y}u(e)N(e)+\sum_{k\le y}F(k)T_k$, (3.9) gives
$$S=\tfrac23\bigl(Y^{3/2}-f(1)^{3/2}\bigr)\sum_{e\le y}\frac{u(e)\rho(e)}e+O\Bigl(F(y)\sum_{e\le y}|u(e)|\rho(e)\Bigr)+O\bigl(Y^{3/2+\varepsilon}y^{-3/4}\bigr).$$
By (3.7) and (3.5) with $E=y$: $\sum_{e\le y}u(e)\rho(e)/e=A^{-1}\prod_p\tau_p+O(y^{-1/2})$. The sum $\sum_{e\le y}u(e)\rho(e)/e$ is bounded by a constant. By (3.6) with $E=y$ and $F(y)\ll Y^{3/2}/y$, the middle error is $\ll Y^{3/2}y^{-1}y^{1/4+2\varepsilon}=Y^{3/2}y^{-3/4+2\varepsilon}$. Hence
$$S=\frac{2}{3A}\Bigl(\prod_p\tau_p\Bigr)Y^{3/2}+O\bigl(Y^{3/2}y^{-1/2}\bigr)+O(1)+O\bigl(Y^{3/2}y^{-3/4+2\varepsilon}\bigr)+O\bigl(Y^{3/2+\varepsilon}y^{-3/4}\bigr).$$
The $O(1)$ term arises from $f(1)^{3/2}$ times a bounded sum. It is $\ll Y^{3/2}y^{-1/2}$ because $Y^{3/2}\ge c_1^{3/2}y^{3d/2}$ and $3d/2-1/2\ge1$. Taking $\varepsilon$ small (replace $2\varepsilon$ by $\varepsilon'$) and using $y^{-3/4+\varepsilon'}\le y^{-1/2}$ for $\varepsilon'\le1/4$ (all remaining errors are then $\ll Y^{3/2+\varepsilon}y^{-1/2}$; for larger $\varepsilon$ the claim follows from the claim for smaller $\varepsilon$ since $Y\ge 2$):
$$S=\frac{2}{3A}\Bigl(\prod_p\tau_p\Bigr)Y^{3/2}+O_{f,\varepsilon}\bigl(Y^{3/2+\varepsilon}y^{-1/2}\bigr).$$
Multiplying by $c_0A$:
$$\sum_{k\le y}F(k)h(f(k))=\tfrac23c_0\Bigl(\prod_p\tau_p\Bigr)Y^{3/2}+O\bigl(Y^{3/2+\varepsilon}y^{-1/2}\bigr)=C_fY^{3/2}+O_{f,\varepsilon}\bigl(Y^{3/2+\varepsilon}y^{-1/2}\bigr).\qquad\blacksquare$$

All implied constants depend only on $f$ and $\varepsilon$ (through $d$, $c_1,c_2$, $C_1$, $f(1)$, $C_\varepsilon$).

## 4. Numerical sanity checks (Python)

* sympy confirmed the identities for $A_p$, $B_p-A_p$ and $D_p-B_p$ in §0.
* mpmath confirmed $\zeta(-1/2)=-\zeta(3/2)/(4\pi)=-0.2078862\ldots$.
* A direct computation of $\sum_{k\le2000}F(k)h(f(k))$ against $C_fY^{3/2}$ for $f=t^2+1$ gave $1.10576\times10^9$ vs $1.10482\times10^9$. For $f=t+1$ it gave $11505.97$ vs $11501.80$. Both agree to $\approx10^{-3}$. The check truncates the Euler products at $p\le3000$ and approximates $\rho(p^2)\approx\rho(p)/p$, which is exact for these squarefree $f$ at large $p$.
