# Proof of P3

No external literature is used beyond the divisor bound $\tau(n)\ll_\varepsilon n^{\varepsilon}$ (standard) and $\mu^2(n)=\sum_{d^2\mid n}\mu(d)$. No numerical checks were needed. No excluded source was consulted.

Fix $x\ge 2$ real, an integer $1\le m\le x$, and put
$$N=x-m\ge 0,\qquad z=x^{1/3}\ge 1 .$$
Then $C_x(m)=\sum_{1\le n\le N}\mu^2(n)\mu^2(n+m)$. All implied constants below depend only on $\varepsilon$. Put $\tau^*=\max_{k\le x}\tau(k)\ll_\varepsilon x^{\varepsilon}$; this also bounds $\tau(m)$.

## Step 0: an elementary tail bound

For real $w>0$,
$$\sum_{a>w}a^{-2}\le \frac{2}{w}\qquad(\ast)$$
If $w\ge1$, let $k=\lfloor w\rfloor+1>w$. Then $\sum_{a\ge k}a^{-2}\le k^{-2}+\int_k^\infty u^{-2}du\le 2/k<2/w$. If $w<1$, the sum is at most $\pi^2/6<2<2/w$.

## Step 1: truncating the Möbius expansions

For an integer $k\ge1$ let
$$S(k)=\sum_{d\le z,\ d^2\mid k}\mu(d),\qquad R(k)=\mu^2(k)-S(k)=\sum_{d>z,\ d^2\mid k}\mu(d).$$
Then $|S(k)|\le\#\{d:d^2\mid k\}\le\tau(k)$ and $|R(k)|\le\#\{d>z:d^2\mid k\}$.

With $a=\mu^2(n)=S(n)+R(n)$ and $b=\mu^2(n+m)=S(n+m)+R(n+m)$ we have the identity
$$ab-S(n)S(n+m)=R(n)\,b+S(n)\,R(n+m).$$
Hence
$$C_x(m)=\sum_{n\le N}S(n)S(n+m)+\mathcal E_1,\qquad |\mathcal E_1|\le\sum_{n\le N}|R(n)|+\tau^*\sum_{n\le N}|R(n+m)|.$$

For $d>z$ the number of $n\le N$ with $d^2\mid n$ is at most $N/d^2$. The number of $n\le N$ with $d^2\mid n+m$ is at most the number of integers $k\le x$ divisible by $d^2$, which is at most $x/d^2$. By $(\ast)$ with $w=z$,
$$\sum_{n\le N}|R(n)|\le N\sum_{d>z}d^{-2}\le \frac{2x}{z}=2x^{2/3},\qquad \sum_{n\le N}|R(n+m)|\le \frac{2x}{z}=2x^{2/3}.$$
Therefore $|\mathcal E_1|\le 2(1+\tau^*)x^{2/3}\ll x^{2/3+\varepsilon}$.

## Step 2: counting solutions of the congruences

$$\sum_{n\le N}S(n)S(n+m)=\sum_{d_1,d_2\le z}\mu(d_1)\mu(d_2)\,\#\{1\le n\le N:\ d_1^2\mid n,\ d_2^2\mid n+m\}.$$
The system $n\equiv0\ (d_1^2)$, $n\equiv -m\ (d_2^2)$ is solvable iff $\gcd(d_1^2,d_2^2)=(d_1,d_2)^2$ divides $m$. In that case the solutions form one residue class modulo $L=\operatorname{lcm}(d_1^2,d_2^2)=d_1^2d_2^2/(d_1,d_2)^2$. The number of $n\in[1,N]$ in one class mod $L$ is $N/L+\theta$ with $|\theta|\le1$, also when $N<1$. There are at most $\lfloor z\rfloor^2\le x^{2/3}$ pairs $(d_1,d_2)$, so
$$\sum_{n\le N}S(n)S(n+m)=N\sum_{\substack{d_1,d_2\le z\\ (d_1,d_2)^2\mid m}}\frac{\mu(d_1)\mu(d_2)}{L(d_1,d_2)}+\mathcal E_2,\qquad|\mathcal E_2|\le x^{2/3}.$$

## Step 3: completing the sum

Write $d_1=ea$, $d_2=eb$ with $e=(d_1,d_2)$ and $(a,b)=1$. Then $L=e^2a^2b^2$ and the condition is $e^2\mid m$. Define
$$\Sigma=\sum_{\substack{d_1,d_2\ge1\\ (d_1,d_2)^2\mid m}}\frac{\mu(d_1)\mu(d_2)}{L(d_1,d_2)} .$$
The pairs with $\max(d_1,d_2)>z$ contribute in absolute value at most twice the contribution of those with $d_1>z$ (by symmetry), i.e. at most
$$2\sum_{e^2\mid m}\frac1{e^2}\sum_{a>z/e}\frac1{a^2}\sum_{b\ge1}\frac1{b^2}
\le 2\cdot\frac{\pi^2}{6}\sum_{e^2\mid m}\frac1{e^2}\cdot\frac{2e}{z}\le\frac{4\pi^2}{3z}\sum_{e^2\mid m}\frac1e\le\frac{14\,\tau(m)}{z}.$$
Here $(\ast)$ is used with $w=z/e$. This bound also shows that $\Sigma$ converges absolutely. Hence
$$N\sum_{\substack{d_1,d_2\le z\\ (d_1,d_2)^2\mid m}}\frac{\mu(d_1)\mu(d_2)}{L}=N\Sigma+\mathcal E_3,\qquad|\mathcal E_3|\le \frac{14\,x\,\tau^*}{z}\ll x^{2/3+\varepsilon}.$$

## Step 4: evaluation of $\Sigma$

A nonzero term of $\Sigma$ needs $d_1=ea$ and $d_2=eb$ squarefree. Then $e$, $a$, $b$ are squarefree and pairwise coprime, and $\mu(ea)\mu(eb)=\mu(a)\mu(b)$. So, by absolute convergence,
$$\Sigma=\sum_{\substack{e\ \text{sqfree}\\ e^2\mid m}}\frac1{e^2}\sum_{\substack{a,b\ \text{sqfree},\ (a,b)=1\\ (ab,e)=1}}\frac{\mu(a)\mu(b)}{a^2b^2}.$$
For fixed $e$, the inner sum is an absolutely convergent sum over pairs $(a,b)$ whose summand factors over primes. At each prime $p\nmid e$ there are three local choices: $p\nmid ab$ (weight $1$), $p\mid a$ (weight $-p^{-2}$), $p\mid b$ (weight $-p^{-2}$). At $p\mid e$ the only choice is $p\nmid ab$. So the inner sum equals
$$\prod_{p\nmid e}\Bigl(1-\frac2{p^2}\Bigr)=A_0\prod_{p\mid e}\Bigl(1-\frac2{p^2}\Bigr)^{-1}=A_0\prod_{p\mid e}\frac{p^2}{p^2-2},$$
which is legitimate because every factor $1-2/p^2$ is nonzero ($p\ge2$). Therefore
$$\Sigma=A_0\sum_{\substack{e\ \text{sqfree}\\ e^2\mid m}}\prod_{p\mid e}\frac{1}{p^2-2}=A_0\sum_{t^2\mid m}\eta(t)=A(m),$$
since $e^{-2}\prod_{p\mid e}p^2=1$ for squarefree $e$.

## Conclusion

Combining Steps 1–4 and using $N=x-m$,
$$C_x(m)=A(m)(x-m)+\mathcal E_1+\mathcal E_2+\mathcal E_3,$$
so
$$|D_x(m)|\le 2(1+\tau^*)x^{2/3}+x^{2/3}+14\,\tau^*x^{2/3}\ll_\varepsilon x^{2/3+\varepsilon},$$
uniformly for real $x\ge2$ and integers $1\le m\le x$, since $\tau^*\ll_\varepsilon x^{\varepsilon}$. $\qquad\blacksquare$
