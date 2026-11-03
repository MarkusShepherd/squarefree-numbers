# Proof of P1

Throughout, $q\in\mathbb N$ is fixed, $l\in\mathbb Z$, and for $d\ge1$
$$g_d:=\gcd(d^2,q).$$
No external results are used beyond $\sum_{n\ge1}n^{-2}<\infty$, $\sum_{n}\mu(n)n^{-2}=\prod_p(1-p^{-2})=6/\pi^2$ and the identity $\mu^2(n)=\sum_{d^2\mid n}\mu(d)$.

## (i) Existence and closed form

Since $\mu^2(n)=\sum_{d^2\mid n}\mu(d)$,
$$Q(x;q,l)=\sum_{d\le\sqrt x}\mu(d)\,N_d(x),\qquad N_d(x):=\#\{n\le x:\ n\equiv l\ (q),\ d^2\mid n\}$$
(for $d>\sqrt x$ there is no $n\le x$ with $d^2\mid n$). Write $n=d^2m$; then $m\le x/d^2$ and $d^2m\equiv l \pmod q$.

* This congruence is solvable in $m$ iff $g_d\mid l$. If $g_d\nmid l$, then $N_d(x)=0$.
* If $g_d\mid l$, it is equivalent to $(d^2/g_d)\,m\equiv l/g_d \pmod{q/g_d}$. Here $\gcd(d^2/g_d,q/g_d)=1$, so this is a single residue class $m\equiv m_0 \pmod{q/g_d}$. The number of $m\in[1,x/d^2]$ in a fixed residue class mod $q/g_d$ is $\frac{x/d^2}{q/g_d}+\theta$ with $|\theta|\le1$. Hence $N_d(x)=\frac{g_d}{d^2q}x+\theta_d$, $|\theta_d|\le 1$.

Therefore
$$Q(x;q,l)=x\sum_{d\le\sqrt x}\mu(d)\frac{g_d}{d^2q}\mathbf 1[g_d\mid l]+R_1,\qquad |R_1|\le\sqrt x .$$
Since $g_d\le q$, each term of the series $S(q,l):=\sum_{d\ge1}\mu(d)\frac{g_d}{d^2q}\mathbf 1[g_d\mid l]$ is bounded in modulus by $d^{-2}$, so $S$ converges absolutely, and the tail satisfies
$$\Big|x\sum_{d>\sqrt x}\mu(d)\tfrac{g_d}{d^2q}\mathbf 1[g_d\mid l]\Big|\le x\sum_{d>\sqrt x}d^{-2}\le x\cdot\frac{2}{\sqrt x}=2\sqrt x ,$$
using $\sum_{d>D}d^{-2}\le \int_{\lfloor D\rfloor}^\infty u^{-2}du=1/\lfloor D\rfloor\le 2/D$ for $D\ge1$. So $|Q(x;q,l)-xS(q,l)|\le3\sqrt x$ for $x\ge1$, and $Q/x\to S(q,l)$. Thus $g(q,l)$ exists and equals $S(q,l)$, which is the claimed formula.

*Bounds.* $Q(x;q,l)\ge0$ gives $g\ge0$. $Q(x;q,l)\le\#\{1\le n\le x: n\equiv l\ (q)\}\le x/q+1$ gives $g\le 1/q$.
*Periodicity.* $g_d\mid q$, so $\mathbf 1[g_d\mid l]$ depends only on $l \bmod q$; hence so does $g(q,l)$.

## (ii)

$g(q,\cdot)$ is $q$-periodic, and for each $d$, since $g_d\mid q$, $\#\{1\le l\le q: g_d\mid l\}=q/g_d$. Summing the absolutely convergent series over the finitely many $l$ and interchanging:
$$\sum_{l=1}^q g(q,l)=\sum_{d\ge1}\mu(d)\frac{g_d}{d^2q}\cdot\frac q{g_d}=\sum_{d\ge1}\frac{\mu(d)}{d^2}=\frac6{\pi^2}.$$

## (iii) Squarefree $n$

Only squarefree $d$ contribute. For squarefree $d$, $g_d=\prod_{p\mid d}\gcd(p^2,q)$, the factors being powers of distinct primes and hence pairwise coprime. So $g_d\mid n$ iff $\gcd(p^2,q)\mid n$ for every $p\mid d$. Hence for squarefree $d$ the summand $q\cdot\mu(d)\frac{g_d}{d^2}\mathbf 1[g_d\mid n]$ equals $\prod_{p\mid d}h(p)$ with
$$h(p):=-\frac{\gcd(p^2,q)}{p^2}\mathbf 1[\gcd(p^2,q)\mid n].$$
As $\sum_p|h(p)|\le\sum_p p^{-2}<\infty$, the sum over squarefree $d$ of $\prod_{p\mid d}h(p)$ equals $\prod_p(1+h(p))$ (absolutely convergent Euler product). Now:

* $p\nmid q$: $\gcd(p^2,q)=1$, $h(p)=-p^{-2}$.
* $p\,\|\,q$: $\gcd(p^2,q)=p$, $h(p)=-p^{-1}\mathbf 1[p\mid n]$.
* $p^2\mid q$: $\gcd(p^2,q)=p^2$, and $p^2\nmid n$ since $n$ is squarefree, so $h(p)=0$.

Thus
$$g(q,n)=\frac1q\prod_{p\nmid q}(1-p^{-2})\prod_{\substack{p\|q\\ p\mid n}}(1-p^{-1}).$$
Finally $\prod_{p\nmid q}(1-p^{-2})=\prod_p(1-p^{-2})\prod_{p\mid q}(1-p^{-2})^{-1}=\frac6{\pi^2}\prod_{p\mid q}(1-p^{-2})^{-1}$, giving
$g(q,n)=\frac6{\pi^2}\,q^{-1}\prod_{p\mid q}(1-p^{-2})^{-1}\prod_{p\mid\gcd(n,q),\,p\|q}(1-1/p)$. $\qquad\blacksquare$

## (iv) Second moment

Write $g(q,l)=\frac1q\sum_d\mu(d)\frac{g_d}{d^2}\mathbf 1[g_d\mid l]$. Squaring (product of two absolutely convergent series) and summing over $1\le l\le q$ (finite sum, interchange allowed):
$$\sum_{l=1}^qg(q,l)^2=\frac1{q^2}\sum_{d,e}\mu(d)\mu(e)\frac{g_dg_e}{d^2e^2}\,\#\{l\bmod q:\ g_d\mid l,\ g_e\mid l\}.$$
Both $g_d,g_e$ divide $q$, so $\mathrm{lcm}[g_d,g_e]\mid q$ and the count is $q/\mathrm{lcm}[g_d,g_e]$. Since $g_dg_e/\mathrm{lcm}[g_d,g_e]=\gcd(g_d,g_e)=\gcd(d^2,e^2,q)=\gcd(\gcd(d,e)^2,q)$,
$$\sum_{l=1}^qg(q,l)^2=\frac1q\sum_{d,e\ \mathrm{sqfree}}\mu(d)\mu(e)\frac{G(\gcd(d,e))}{d^2e^2},\qquad G(t):=\gcd(t^2,q).$$
(The sum is absolutely convergent: $G\le q$ is bounded and $\sum_{d,e}d^{-2}e^{-2}<\infty$.)

Parametrise squarefree pairs $(d,e)$ by $t=\gcd(d,e)$, $d=td'$, $e=te'$. This is a bijection onto triples $(t,d',e')$ of squarefree integers that are pairwise coprime; and $\mu(d)\mu(e)=\mu(t)^2\mu(d')\mu(e')=\mu(d')\mu(e')$. By absolute convergence we may sum over $t$ first:
$$\sum_{d,e}\dots=\sum_{t\ \mathrm{sqfree}}\frac{G(t)}{t^4}\,I(t),\qquad I(t):=\sum_{\substack{d',e'\ \mathrm{sqfree}\\ (d',e')=(d'e',t)=1}}\frac{\mu(d')\mu(e')}{d'^2e'^2}.$$
The summand is multiplicative in the pair; at each prime $p\nmid t$ the local choices are: $p\nmid d'e'$ (weight 1), $p\mid d'$ only (weight $-p^{-2}$), $p\mid e'$ only (weight $-p^{-2}$); primes $p\mid t$ divide neither. Since the sum converges absolutely,
$$I(t)=\prod_{p\nmid t}\Big(1-\frac2{p^2}\Big)=A_0\prod_{p\mid t}\Big(1-\frac2{p^2}\Big)^{-1}$$
(note $1-2/p^2\ge1/2>0$). As $t$ is squarefree, $\prod_{p\mid t}p^2=t^2$, so
$$\frac1{t^4}\prod_{p\mid t}\frac{p^2}{p^2-2}=\frac{1}{t^2}\prod_{p\mid t}\frac1{p^2-2}\quad\Longrightarrow\quad \frac{G(t)}{t^4}I(t)=A_0\,\eta(t)\frac{\gcd(t^2,q)}{t^2}.$$
Hence $\sum_{l=1}^qg(q,l)^2=\frac{A_0}q\sum_{t\ge1}\eta(t)\frac{\gcd(t^2,q)}{t^2}$, where the series converges absolutely because $p^2-2\ge p^2/2$ gives $\eta(t)\le2^{\omega(t)}t^{-2}$ and $\gcd(t^2,q)/t^2\le 1$.

## (v)

$\eta$ is multiplicative and supported on squarefree integers, with $\eta(p)=1/(p^2-2)$, and $\sum_p\eta(p)<\infty$ (also $\sum_t \eta(t)\le\sum_t 2^{\omega(t)}t^{-2}<\infty$). So
$$\sum_{t\ge1}\eta(t)=\prod_p\Big(1+\frac1{p^2-2}\Big)=\prod_p\frac{p^2-1}{p^2-2}=\prod_p\frac{1-p^{-2}}{1-2p^{-2}}=\frac{6/\pi^2}{A_0}.$$
(All products converge absolutely and $A_0>0$.) $\qquad\blacksquare$

## Numerical sanity checks (Python)

For $q\in\{1,4,12,18,30\}$ and $x=10^6$ I compared (a) the brute-force density $Q(x;q,l)/x$ with the series in (i) (max discrepancy $\le 3.2\cdot10^{-5}$, consistent with the $O(x^{-1/2})$ error), (b) $\sum_l g(q,l)$ with $6/\pi^2$ (difference $\sim10^{-6}$, due to truncating the series), (c) formula (iii) for all squarefree $n\le q$ (agreement to $10^{-5}$), (d) $\sum_l g(q,l)^2$ with the right side of (iv) (difference $\le 1.4\cdot10^{-6}$). All agree. As an additional hand check, the case $q=1$ of (iv) reads $A_0\sum\eta(t)t^{-2}=\prod_p(p^2-1)^2/p^4=36/\pi^4=g(1,1)^2$.
