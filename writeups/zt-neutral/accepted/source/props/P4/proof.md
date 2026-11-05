# P4: Trivial-size error pieces — proof

Notation as in the statement. $\omega(r)$ is the number of distinct prime factors of $r$. Throughout, $\mu^2(n)=\sum_{d^2\mid n}\mu(d)$. The proof is elementary. It uses only the dependency P1 (i) and (iii), and the fact $\sum_{d\ge1}\mu(d)d^{-2}=1/\zeta(2)=6/\pi^2$. I ran no numerical checks.

**Tail bound.** For real $z\ge1$, put $N=\lfloor z\rfloor\ge z/2$. Then
$$\sum_{d>z}d^{-2}\le\sum_{d\ge N+1}d^{-2}\le \frac1N\le \frac 2z. \tag{0}$$

## (i)

Every squarefree-indicator identity gives $Q(x)=\sum_{n\le x}\sum_{d^2\mid n}\mu(d)=\sum_{d\le\sqrt x}\mu(d)\lfloor x/d^2\rfloor$. Write $\lfloor x/d^2\rfloor=x/d^2+\theta_d$ with $|\theta_d|\le1$. The sum has at most $\sqrt x$ terms. Hence
$$Q(x)=x\sum_{d\le\sqrt x}\frac{\mu(d)}{d^2}+O_1(\sqrt x)
= x\sum_{d\ge1}\frac{\mu(d)}{d^2}-x\sum_{d>\sqrt x}\frac{\mu(d)}{d^2}+O_1(\sqrt x),$$
where $O_1(Y)$ denotes a quantity of modulus at most $Y$. By (0) with $z=\sqrt x\ge1$, the middle term has modulus at most $x\cdot 2/\sqrt x=2\sqrt x$. Therefore $|Q(x)-6x/\pi^2|\le 3\sqrt x$ for all $x\ge1$.

## (ii)

Fix $q\ge1$ (the hypothesis $q\le x$ will not be needed). Let $q_1=\prod_{p\,\|\,q}p$, the product of the primes dividing $q$ exactly once.

**Step 1: reduction to a sum over squarefree $n$.** By P1 (i), $g(q,\cdot)$ depends only on the residue class mod $q$. Hence
$$S(x):=\sum_{l=1}^q g(q,l)Q(x;q,l)=\sum_{n\le x}\mu^2(n)\,g(q,n),$$
and
$$\sum_{l=1}^q g(q,l)E(x;q,l)=S(x)-x\sum_{l=1}^q g(q,l)^2. \tag{1}$$

**Step 2: insert P1 (iii).** For squarefree $n$, P1 (iii) states
$$g(q,n)=\frac{6}{\pi^2}\,q^{-1}\prod_{p\mid q}(1-p^{-2})^{-1}\prod_{p\mid\gcd(n,q),\ p\|q}(1-1/p).$$
The second product is over primes $p\mid n$ with $p\,\|\,q$, that is, over $p\mid\gcd(n,q_1)$. Put
$$c_q=\frac6{\pi^2}\prod_{p\mid q}(1-p^{-2})^{-1}.$$
Then $0<c_q\le\frac6{\pi^2}\zeta(2)=1$. Also, since $q_1$ is squarefree,
$$\prod_{p\mid\gcd(n,q_1)}(1-1/p)=\sum_{r\mid\gcd(n,q_1)}\frac{\mu(r)}r.$$
So for squarefree $n$, $g(q,n)=\dfrac{c_q}{q}\sum_{r\mid q_1,\ r\mid n}\mu(r)/r$. Interchanging the (finite) sum over $r$ with the sum over $n$ gives
$$S(x)=\frac{c_q}{q}\sum_{r\mid q_1}\frac{\mu(r)}{r}\,N_r(x),\qquad N_r(x)=\#\{n\le x:\ r\mid n,\ n\text{ squarefree}\}. \tag{2}$$

**Step 3: asymptotics for $N_r$.** Let $r$ be squarefree. Write $n=rm$. Then $n$ is squarefree iff $m$ is squarefree and $(m,r)=1$. So $N_r(x)=T_r(x/r)$, where
$$T_r(y)=\#\{m\le y:\ \mu^2(m)=1,\ (m,r)=1\}.$$
Use $\mu^2(m)=\sum_{d^2\mid m}\mu(d)$ and $\mathbf 1_{(m,r)=1}=\sum_{e\mid\gcd(m,r)}\mu(e)$. This gives
$$T_r(y)=\sum_{d\ge1}\sum_{e\mid r}\mu(d)\mu(e)\Big\lfloor \frac{y}{[d^2,e]}\Big\rfloor .$$
Here $[d^2,e]$ is the lcm, and the floor vanishes unless $[d^2,e]\le y$. That forces $d\le\sqrt y$. Define
$$\kappa_r=\sum_{d\ge1}\sum_{e\mid r}\frac{\mu(d)\mu(e)}{[d^2,e]}.$$
The sum converges absolutely, since $[d^2,e]\ge d^2$ gives $|\kappa_r|\le 2^{\omega(r)}\zeta(2)\le 2\cdot2^{\omega(r)}$.

*Case $y\ge1$.* The pairs $(d,e)$ with $d\le\sqrt y$, $e\mid r$ number at most $2^{\omega(r)}\sqrt y$. Replacing each floor by $y/[d^2,e]$ costs at most $1$ per pair. Completing $d\le\sqrt y$ to all $d$ costs, by (0) with $z=\sqrt y$,
$$y\sum_{d>\sqrt y}\sum_{e\mid r}\frac1{[d^2,e]}\le y\,2^{\omega(r)}\sum_{d>\sqrt y}d^{-2}\le 2\cdot 2^{\omega(r)}\sqrt y .$$
Hence $|T_r(y)-\kappa_ry|\le 3\cdot2^{\omega(r)}\sqrt y$.

*Case $0<y<1$.* Here $T_r(y)=0$, so $|T_r(y)-\kappa_r y|\le 2\cdot 2^{\omega(r)}y\le 2\cdot2^{\omega(r)}\sqrt y$.

So for all $y>0$,
$$|T_r(y)-\kappa_r y|\le 3\cdot 2^{\omega(r)}\sqrt y. \tag{3}$$

**Step 4: summing over $r$.** The sum in (2) is over the divisors $r$ of $q_1$. There are $2^{\omega(q_1)}\le 2^{\omega(q)}$ of them, and we bound the sum by the sum over all squarefree $r$. From (2) and (3) with $y=x/r$,
$$S(x)=M_q\,x+R_q(x),\qquad M_q=\frac{c_q}q\sum_{r\mid q_1}\frac{\mu(r)\kappa_r}{r^2},$$
$$|R_q(x)|\le\frac{c_q}{q}\sum_{r\mid q_1}\frac1r\cdot3\cdot2^{\omega(r)}\sqrt{x/r}
\le \frac{3\sqrt x}{q}\sum_{r\ \text{squarefree}}2^{\omega(r)}r^{-3/2}
=\frac{3\sqrt x}{q}\prod_p\bigl(1+2p^{-3/2}\bigr).$$
We used $c_q\le1$. The Euler product converges, and
$$\prod_p(1+2p^{-3/2})\le\exp\Bigl(2\sum_p p^{-3/2}\Bigr)\le e^{2\zeta(3/2)}=:B<\infty,$$
an absolute constant. So $|R_q(x)|\le 3B\sqrt x/q$ for all $x>0$.

**Step 5: identification of $M_q$.** By P1 (i), $Q(x;q,l)/x\to g(q,l)$ as $x\to\infty$ for each of the finitely many $l\in\{1,\dots,q\}$. Hence $S(x)/x\to\sum_{l=1}^q g(q,l)^2$. On the other hand, $S(x)/x=M_q+R_q(x)/x$, and $|R_q(x)/x|\le 3B/(q\sqrt x)\to0$. Therefore
$$M_q=\sum_{l=1}^q g(q,l)^2 .$$

**Step 6: conclusion.** By (1) and Step 5,
$$\sum_{l=1}^q g(q,l)E(x;q,l)=S(x)-M_q x=R_q(x),\qquad
\Bigl|\sum_{l=1}^q g(q,l)E(x;q,l)\Bigr|\le\frac{3B\sqrt x}{q}.$$

## Conclusion

Take $c_0=\max(3,3B)=3e^{2\zeta(3/2)}$. Then (i) holds for all real $x\ge1$ by the first part. Part (ii) holds for all real $x\ge1$ and all integers $q\ge1$, in particular for $1\le q\le x$. $\qquad\blacksquare$
