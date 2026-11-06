Put \(A_d=[t^d]f(t)\ne0\), and fix
\[
C_0=\max\{d,|A_d|,1\}.
\]
For every prime \(p\nmid A_d\), reduction modulo \(p\) is a nonzero
polynomial of degree \(d\), so the factor theorem gives at most \(d\)
roots. If \(p\mid A_d\), the bound
\(\rho(p)\le p\le |A_d|\) applies. Each residue class modulo \(p\) has
exactly \(p\) lifts modulo \(p^2\). Consequently,
\[
0\le\rho(p)\le\min\{C_0,p\},\qquad
0\le\rho(p^2)\le p\rho(p)\le C_0p.                 \tag{1}
\]
These bounds require no assumption on the content, discriminant, or
factorization of \(f\).

We will use the following explicit summation estimate. If \(u>1\) and
\(N\ge1\) is an integer, comparison with an integral gives
\[
\sum_{p>N}p^{-u}\le\sum_{n>N}n^{-u}
\le\int_N^\infty t^{-u}\,dt
=\frac{N^{1-u}}{u-1}.                              \tag{2}
\]
Both sums in (2) have infinitely many possible indices. A bound
\(k p^{-u}\) for each prime therefore has total at most
\(kN^{1-u}/(u-1)\) after summing over \(p>N\). In particular, the sum over
all primes is at most \(k/(u-1)\).
If local factors are \(1+e_p(s)\), the estimate
\[
\left|\prod_{p>N}(1+e_p(s))-1\right|
\le \exp\!\left(\sum_{p>N}|e_p(s)|\right)-1          \tag{3}
\]
follows first for finite products by expansion and then for their limits.
Thus all the prime-sum tail estimates below also give explicit product
tail estimates. Uniform summability of \(|e_p|\) on compact sets gives
local uniform convergence to a holomorphic function, since the finite
products are holomorphic.

For brevity put \(q_p=1-2/p^2\), and introduce the three coefficients
\[
\begin{aligned}
\alpha_p&=q_pa_p=1-\frac2{p^2}+\frac{\rho(p^2)}{p^4},\\
\beta_p&=q_p(b_p-a_p)=\frac{\rho(p)}{p^3}
                              -\frac{\rho(p^2)}{p^4},\\
\delta_p&=q_p(c_p-b_p)=\frac1{p^2}-\frac{\rho(p)}{p^3}.
\end{aligned}                                                    \tag{4}
\]
By (1),
\[
\begin{gathered}
0<q_p\le\alpha_p\le1,\qquad
0\le\beta_p\le C_0p^{-3},\qquad
0\le\delta_p\le p^{-2},\\
|\alpha_p-1|\le2p^{-2}+C_0p^{-3},\qquad
\alpha_p+\beta_p+\delta_p=1-p^{-2}.                 \tag{5}
\end{gathered}
\]
In particular, \(b_p-a_p\ge0\) and \(c_p-b_p\ge0\).

The local factor \(w_p(h)\) in \(W_f(h)\) is, according as
\(v_p(h)=0,1\) or at least \(2\),
\[
w_p(h)=\alpha_p,\quad
\alpha_p+\beta_p,\quad
\alpha_p+\beta_p+\delta_p,
\]
respectively. Alternatively, the elementary bound
\(0\le\rho(p^j)\le p^j\), including \(j=0\), gives directly
\[
1-\frac2{p^2}\le w_p(h)\le1-\frac1{p^2},\qquad
|w_p(h)-1|\le\frac2{p^2}.                          \tag{6}
\]
The prime tail of the last bound is at most \(2/N\) by (2), uniformly
in \(h\). Every factor is at least \(1/2\). For \(1/2\le t\le1\),
\(-\log t\le2(1-t)\); hence
\[
\sum_p|\log w_p(h)|\le4\sum_pp^{-2}\le4.
\]
It follows that the product defining \(W_f(h)\) is absolutely convergent
and \(0<W_f(h)\le1\). For \(s=\sigma+it\) with \(\sigma>1\), this gives
\[
\sum_{h\ge1}|W_f(h)h^{-s}|\le\sum_{h\ge1}h^{-\sigma}<\infty.
\]
More explicitly, the sum of the errors over the infinitely many indices
\(h>N\) is bounded by
\[
\sum_{h>N}|W_f(h)h^{-s}|
\le\sum_{h>N}h^{-\sigma}
\le\frac{N^{1-\sigma}}{\sigma-1}.                  \tag{7}
\]
This proves the asserted absolute convergence of \(D_f\).

Write
\[
L_p(s)=q_pB_p(s)=\alpha_p+\beta_pp^{-s}+\delta_pp^{-2s}.
\]
On the closed half-plane \(\Re s\ge\sigma\), (5) gives the bound for
each individual prime
\[
|L_p(s)-1|
\le2p^{-2}+C_0p^{-3}+C_0p^{-3-\sigma}+p^{-2-2\sigma}.       \tag{8}
\]
If \(\sigma>-1/2\), all four exponents exceed \(1\). Summing (8) over
the infinitely many primes \(p>N\), using (2) separately for its four
terms, yields
\[
\begin{aligned}
\sum_{p>N}|L_p(s)-1|\le E_P(N;\sigma)
={}&\frac2N+\frac{C_0}{2N^2}
 +\frac{C_0N^{-2-\sigma}}{2+\sigma}
 +\frac{N^{-1-2\sigma}}{1+2\sigma}.                 \tag{9}
\end{aligned}
\]
Every power of \(N\) on the right has negative exponent. Equations
(3) and (9) prove absolute and locally uniform convergence of \(P_f\)
on \(\Re s>-1/2\). They also prove its holomorphy there.

The local factor in \(H_f\) is
\[
\begin{aligned}
M_p(s)&=(1-p^{-2s-2})L_p(s)\\
 &=\alpha_p+\beta_pp^{-s}
 +(\delta_p-\alpha_pp^{-2})p^{-2s}
 -\beta_pp^{-2}p^{-3s}-\delta_pp^{-2}p^{-4s}.         \tag{10}
\end{aligned}
\]
The coefficient where cancellation is needed is exactly
\[
\delta_p-\alpha_pp^{-2}
 =-\frac{\rho(p)}{p^3}+\frac2{p^4}
                         -\frac{\rho(p^2)}{p^6},
\]
so its absolute value is at most
\(C_0p^{-3}+2p^{-4}+C_0p^{-5}\). Thus, for \(\Re s\ge\sigma\),
\[
\begin{aligned}
|M_p(s)-1|\le{}&2p^{-2}+C_0p^{-3}+C_0p^{-3-\sigma}
 +C_0p^{-3-2\sigma}+2p^{-4-2\sigma}\\
 &+C_0p^{-5-2\sigma}+C_0p^{-5-3\sigma}
 +p^{-4-4\sigma}.                                  \tag{11}
\end{aligned}
\]
For \(\sigma>-3/4\), the eight exponents on the right are, respectively,
\[
2,\ 3,\ 3+\sigma,\ 3+2\sigma,\ 4+2\sigma,
\ 5+2\sigma,\ 5+3\sigma,\ 4+4\sigma,
\]
and each is greater than \(1\). The sum over the infinitely many primes
\(p>N\), before summation bounded prime by prime by (11), is after
summation bounded by
\[
\begin{aligned}
\sum_{p>N}|M_p(s)-1|\le E_H(N;\sigma)
={}&\frac2N+\frac{C_0}{2N^2}
 +\frac{C_0N^{-2-\sigma}}{2+\sigma}
 +\frac{C_0N^{-2-2\sigma}}{2+2\sigma}\\
 &+\frac{2N^{-3-2\sigma}}{3+2\sigma}
 +\frac{C_0N^{-4-2\sigma}}{4+2\sigma}
 +\frac{C_0N^{-4-3\sigma}}{4+3\sigma}
 +\frac{N^{-3-4\sigma}}{3+4\sigma}.                 \tag{12}
\end{aligned}
\]
All denominators in (12) are positive, and all powers of \(N\) have
negative exponents in this range. Equations (3) and (12) prove absolute
and locally uniform convergence, and holomorphy, of \(H_f\) on
\(\Re s>-3/4\). For every real \(t\), the bound
\(|M_p(\sigma+it)|\le\exp(|M_p(\sigma+it)-1|)\) also proves
\[
|H_f(\sigma+it)|\le \exp(E_H(1;\sigma)).             \tag{13}
\]
Thus one may take \(C(f,\sigma)=\exp(E_H(1;\sigma))\), with every
term in its exponent specified in (12).

We next identify the Dirichlet series. The positive number
\[
A=\prod_p\alpha_p
\]
exists by (5), or by (6) with \(h=1\). Define
\(u(h)=W_f(h)/A\). Only the primes dividing \(h\) change a factor of
this quotient, so \(u\) is multiplicative and
\[
u(1)=1,\qquad u(p)=\frac{b_p}{a_p},\qquad
u(p^e)=\frac{c_p}{a_p}\quad(e\ge2).
\]
In particular \(0<u(h)\le A^{-1}\). For \(\Re s>1\), its local series is
\[
\sum_{e\ge0}u(p^e)p^{-es}
 =1+\frac{b_p}{a_p}p^{-s}
       +\frac{c_p}{a_p}\frac{p^{-2s}}{1-p^{-s}}
 =\frac{B_p(s)}{a_p(1-p^{-s})}.                    \tag{14}
\]
To justify multiplication of these series, first include only primes
\(p\le N\). Their finite product expands into the sum over integers
whose prime factors are all at most \(N\). Every omitted integer is
greater than \(N\). The omitted sum has infinitely many possible
indices, each term has modulus at most \(A^{-1}h^{-\sigma}\), and its
total modulus is at most
\[
\frac{A^{-1}N^{1-\sigma}}{\sigma-1}.                \tag{15}
\]
This tends to zero. Multiplying (14) over all primes therefore gives
\[
\begin{aligned}
D_f(s)
 &=\lim_{N\to\infty}
 \left(\prod_{p\le N}\frac{L_p(s)}{1-p^{-s}}\right)
 \left(\prod_{p>N}\alpha_p\right)\\
 &=\zeta(s)P_f(s),\qquad \Re s>1.                 \tag{16}
\end{aligned}
\]
Here the Euler product for \(\zeta(s)=\sum_{n\ge1}n^{-s}\) follows
by unique prime factorization: its finite-prime expansion omits only
integers \(n>N\), whose total absolute contribution is at most
\(N^{1-\sigma}/(\sigma-1)\). The extra tail product in (16) tends to
\(1\), with explicit bound
\[
\left|\prod_{p>N}\alpha_p-1\right|
 \le \exp\!\left(\frac2N+\frac{C_0}{2N^2}\right)-1. \tag{17}
\]

For \(\Re s>-1/2\), the Euler product for \(\zeta(2s+2)\) is
absolutely convergent. Its reciprocal product is nonzero, since
\(|p^{-2s-2}|<1\) and
\(\sum_p|p^{-2s-2}|<\infty\). Multiplying the absolutely convergent
products defining \(P_f\) and \(H_f\) gives
\[
P_f(s)=\zeta(2s+2)H_f(s)\quad(\Re s>-1/2).          \tag{18}
\]
In particular, (16) proves both required identities on \(\Re s>1\).

For completeness, the zeta-function facts needed for continuation and
signs can all be derived directly. For \(\Re w>1\), integrating the
counting function of the positive integers gives
\[
\zeta(w)=w\int_1^\infty\lfloor x\rfloor x^{-w-1}\,dx
 =\frac1{w-1}+\frac12
       -w\int_1^\infty(\{x\}-1/2)x^{-w-1}\,dx.     \tag{19}
\]
Let
\(\mathcal B_2(x)=\{x\}^2-\{x\}+1/6\).
This function is continuous at integers, is bounded in absolute value
by \(1/6\), and has derivative \(2(\{x\}-1/2)\) between consecutive
integers. More explicitly, for an integer \(T\ge2\), integration by
parts over the \(T-1\) intervals between \(1\) and \(T\) gives the
exact identity
\[
\int_1^T(\{x\}-1/2)x^{-w-1}\,dx
 =\frac{T^{-w-1}-1}{12}
  +\frac{w+1}{2}\int_1^T\mathcal B_2(x)x^{-w-2}\,dx.
\]
The internal endpoint terms cancel exactly. The upper endpoint
term, after multiplication by \(-w\), has modulus
\(|w|T^{-\Re w-1}/12\), which tends to zero for \(\Re w>1\).
Substitution in (19) therefore yields
\[
\zeta(w)=\frac1{w-1}+\frac12+\frac w{12}
 -\frac{w(w+1)}2
       \int_1^\infty\mathcal B_2(x)x^{-w-2}\,dx.    \tag{20}
\]
The integral is holomorphic for \(\Re w>-1\). Explicitly, its tail
past \(T\ge1\), including the coefficient in (20), has absolute value
at most
\[
\frac{|w(w+1)|}{12(\Re w+1)}T^{-\Re w-1}.           \tag{21}
\]
For each nonnegative integer \(m\), the \(m\)-th derivative of the
integrand with respect to \(w\) is dominated on \(\Re w\ge\eta>-1\)
by \((\log x)^m x^{-\eta-2}/6\), whose integral is
\(m!/[6(\eta+1)^{m+1}]\). These bounds justify holomorphy and the
continuation in (20), with its sole pole at \(w=1\) and residue \(1\).

We also record the constant term at that pole. For an integer \(N\ge1\),
the same counting-function integration gives, initially for
\(\Re w>1\) and then by continuation for \(\Re w>0\),
\[
\zeta(w)=\sum_{n=1}^N n^{-w}+\frac{N^{1-w}}{w-1}
       -w\int_N^\infty\{x\}x^{-w-1}\,dx.           \tag{22}
\]
The finite sum has exactly \(N\) terms. The final integral, including
its coefficient, is bounded by
\(|w|N^{-\Re w}/\Re w\). Subtracting \(1/(w-1)\) and taking
\(w\to1\) gives
\[
\lim_{w\to1}\left(\zeta(w)-\frac1{w-1}\right)
 =\sum_{n=1}^N\frac1n-\log N
       -\int_N^\infty\{x\}x^{-2}\,dx.
\]
The integral is between \(0\) and \(1/N\). Taking \(N\to\infty\),
the right side is Euler's constant \(\gamma_E\), by its defining
harmonic-sum limit.

Equation (20) gives \(\zeta(0)=-1/2\). At \(w=-1/2\) it gives
\[
\zeta(-1/2)=-\frac5{24}
       +\frac18\int_1^\infty\mathcal B_2(x)x^{-3/2}\,dx.
\]
The integral has absolute value at most
\((1/6)\int_1^\infty x^{-3/2}\,dx=1/3\). Hence
\[
-\frac14\le\zeta(-1/2)\le-\frac16<0.              \tag{23}
\]

For \(\Re s>-3/4\), the two arguments \(s\) and \(2s+2\) in
\[
\widetilde D_f(s)=\zeta(s)\zeta(2s+2)H_f(s)         \tag{24}
\]
satisfy \(\Re s>-1\) and \(\Re(2s+2)>1/2>-1\).
Thus (20) and the holomorphy of \(H_f\) prove that (24) is
meromorphic throughout this region. It agrees with \(D_f\) on
\(\Re s>1\) by (16) and (18), so it is the claimed continuation.
We henceforth use the notation \(D_f\) for this continuation.

At \(s=0\),
\[
L_p(0)=\alpha_p+\beta_p+\delta_p=1-p^{-2},\qquad
P_f(0)=\prod_p(1-p^{-2})=\frac1{\zeta(2)}.
\]
The equality \(D_f(s)=\zeta(s)P_f(s)\) extends meromorphically to
\(\Re s>-1/2\) by (18) and (24). Both factors are regular at zero,
so
\[
D_f(0)=\zeta(0)P_f(0)=-\frac1{2\zeta(2)}.          \tag{25}
\]

At \(s=1\), \(P_f\) is holomorphic. With \(R_f=P_f(1)\), equations
(16) and (22) show
\[
\operatorname*{Res}_{s=1}D_f(s)=R_f,\qquad
\lim_{s\to1}\left(D_f(s)-\frac{R_f}{s-1}\right)
 =\gamma_ER_f+P_f'(1)=B_f+\frac32R_f.               \tag{26}
\]
This proves that the definitions of \(R_f\) and \(B_f\) have the
specified values without any unspecified remainder in a Laurent
expansion.

At \(s=-1/2\), every local factor of \(H_f\) is strictly positive:
\[
M_p(-1/2)
 =(1-p^{-1})\bigl(\alpha_p+\beta_p\sqrt p+\delta_pp\bigr)>0. \tag{27}
\]
The nonnegativity and strict positivity needed here are exactly (5).
The series of absolute deviations of these factors from \(1\)
converges by (11)--(12) with \(\sigma=-1/2\). A convergent product
of positive factors with summable absolute deviations has positive
limit: after finitely many factors, \(|M_p(-1/2)-1|\le1/2\), and
then \(|\log M_p(-1/2)|\le2|M_p(-1/2)-1|\).
Consequently \(H_f(-1/2)>0\). Combining this with (23) proves
\[
K_f=-\frac83\zeta(-1/2)H_f(-1/2)>0.                \tag{28}
\]
For clarity, the explicit Euler product in this constant is
\[
K_f=-\frac83\zeta(-1/2)
 \prod_p\left\{
 (1-2/p^2)(1-1/p)
 \bigl[a_p+(b_p-a_p)\sqrt p+(c_p-b_p)p\bigr]
 \right\}.                                       \tag{29}
\]
The factors inside braces are kept grouped at each prime; their
absolute convergence is precisely the convergence just proved for
\(H_f(-1/2)\). The pole of \(\zeta(2s+2)\) contributes a factor
\(1/2\) to its residue. Equations (23)--(24) therefore also give
\[
\operatorname*{Res}_{s=-1/2}D_f(s)
 =\frac12\zeta(-1/2)H_f(-1/2)=-\frac3{16}K_f.       \tag{30}
\]
The only possible poles in the stated region are \(1\) and \(-1/2\).
Both are genuine: the local factors of \(P_f(1)\) are positive with
summable absolute deviations, and (28) makes (30) nonzero.

It remains to identify the common density coefficient. Substitution
of (4) into \(L_p(1)\) gives the exact identity
\[
\begin{aligned}
L_p(1)
 &=\alpha_p+\frac{\beta_p}{p}+\frac{\delta_p}{p^2}\\
 &=1-\frac2{p^2}+\frac1{p^4}
       +\frac{(1-1/p)(\rho(p)+\rho(p^2))}{p^4}\\
 &=(1-p^{-2})^2
 \left[1+\frac{(1-1/p)(\rho(p)+\rho(p^2))}{(p^2-1)^2}\right].
                                                               \tag{31}
\end{aligned}
\]
Let
\[
T_p=\frac{(1-1/p)(\rho(p)+\rho(p^2))}{(p^2-1)^2}.
\]
Since \(p^2-1\ge3p^2/4\), (1) bounds the term for each prime by
\[
0\le T_p\le\frac{16C_0}{9}(p^{-4}+p^{-3}).          \tag{32}
\]
The sum over the infinitely many primes \(p>N\) is therefore bounded
explicitly by
\[
\sum_{p>N}T_p
 \le\frac{16C_0}{9}\left(\frac1{3N^3}+\frac1{2N^2}\right). \tag{33}
\]
This proves absolute convergence of the product of \(1+T_p\).
The product of \((1-p^{-2})^2\) is absolutely convergent as well,
since the absolute deviation of its factor from \(1\) is
\(2p^{-2}-p^{-4}\le2p^{-2}\), with prime tail at most \(2/N\).
Multiplying (31) over the primes and using the Euler product for
\(\zeta(2)\) proves
\[
R_f=\zeta(2)^{-2}\prod_p
 \left[1+\frac{(1-1/p)(\rho(p)+\rho(p^2))}{(p^2-1)^2}\right]. \tag{34}
\]

Finally, the Chinese remainder theorem gives
\(\rho(mn)=\rho(m)\rho(n)\) for \((m,n)=1\): the bijection between
residues modulo \(mn\) and pairs of residues modulo \(m,n\) restricts
to a bijection between the respective polynomial roots. Put
\[
v(r)=
\begin{cases}
\displaystyle\frac{\varphi(r)\rho(r)}r
             \prod_{p\mid r}(p^2-1)^{-2},
 &\text{if no prime cube divides }r,\\
0,&\text{otherwise}.
\end{cases}
\]
This is a nonnegative multiplicative function with \(v(1)=1\).
Its first two prime-power values are
\[
v(p)=\frac{(1-1/p)\rho(p)}{(p^2-1)^2},\qquad
v(p^2)=\frac{(1-1/p)\rho(p^2)}{(p^2-1)^2}.          \tag{35}
\]
For \(e\ge3\), its value \(v(p^e)\) is zero.
For the primes at most \(N\), the finite product of
\(1+v(p)+v(p^2)=1+T_p\) expands into a finite nonnegative sum over
the \(3^{\pi(N)}\) integers obtained by choosing each such prime's
exponent from \(\{0,1,2\}\). These sets increase to all integers
with no prime-cube divisor. By (32) and (2), their sums are bounded
by
\[
\prod_p(1+T_p)\le
 \exp\!\left(\frac{16C_0}{9}\left(\frac13+\frac12\right)\right)
 =\exp(40C_0/27).                                  \tag{36}
\]
Monotone convergence thus proves absolute convergence and the
Euler-product identity
\[
\sum_{r\ge1}v(r)=\prod_p(1+T_p).
\]
Explicitly, the omitted sum over the infinitely many integers having
a prime divisor greater than \(N\) is at most
\[
\exp(40C_0/27)
 \left[
 \exp\!\left(\frac{16C_0}{9}
                \left(\frac1{3N^3}+\frac1{2N^2}\right)\right)-1
 \right].                                         \tag{37}
\]
Indeed the omitted sum is exactly
\[
\left(\prod_{p\le N}(1+T_p)\right)
\left(\prod_{p>N}(1+T_p)-1\right),
\]
so (3), (33), and (36) give (37).
The definition of \(\lambda(r)\) in the statement satisfies
\(\lambda(r)\rho(r)/r=\zeta(2)^{-2}v(r)\). Equations (34)--(35)
therefore give the required identity
\[
R_f=\sum_{r\ge1}\frac{\lambda(r)\rho(r)}r.
\]
All the Euler products specifying \(R_f\) or \(K_f\) have had their
absolute convergence established above.

No external literature or numerical checks were used in this proof.
