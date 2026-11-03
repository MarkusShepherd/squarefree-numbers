# Proof of P2: exact decomposition of the single-modulus variance

Throughout, $x\ge 1$ is real and $q\in\mathbb N$. All sums over $n,n'$ run over positive integers. We use from `deps/P1.md` only:

* (iv) $\displaystyle\sum_{l=1}^q g(q,l)^2=\frac{A_0}{q}\sum_{t\ge1}\eta(t)\frac{\gcd(t^2,q)}{t^2}$, and
* (v) $\displaystyle\sum_{t\ge1}\eta(t)=\frac{6}{\pi^2A_0}$.

Since $\eta\ge 0$, (v) shows $\sum_t \eta(t)<\infty$. Also $\gcd(t^2,q)/t^2=1/m_t(q)$ with $1\le m_t(q)$, so every series below that has the form $\sum_t\eta(t)\cdot(\text{quantity bounded by }c(x,q))$ converges absolutely.

## Step 1: reduction to $\sum_l Q(x;q,l)^2$

Write $Q_l=Q(x;q,l)$, $g_l=g(q,l)$, $E_l=Q_l-g_lx$, $S_2=\sum_{l=1}^q g_l^2$. Expanding,
$$V=\sum_l (Q_l-g_lx)^2=\sum_l Q_l^2-2x\sum_l g_lQ_l+x^2S_2 .$$
Since $Q_l=E_l+g_lx$, we get $\sum_l g_lQ_l=\sum_l g_lE_l+xS_2$. Hence
$$V(x;q)=\sum_{l=1}^q Q_l^2-x^2S_2-2x\sum_{l=1}^q g_lE_l. \tag{1}$$

## Step 2: counting pairs

$\sum_{l=1}^q Q_l^2$ is the number of ordered pairs $(n,n')$ of squarefree integers in $[1,x]$ with $n\equiv n'\pmod q$. The diagonal $n=n'$ contributes $Q(x)$. Pairs with $n<n'$ are $n'=n+hq$ with $h\ge1$ and $n+hq\le x$; the pairs with $n>n'$ are their mirror images. So
$$\sum_l Q_l^2=Q(x)+2\sum_{h\ge1}C_x(hq).$$
If $hq>x$ there is no $n\ge1$ with $n+hq\le x$, so $C_x(hq)=0$. Also $C_x(hq)=0$ if $hq=x$. Hence the sum may be restricted to $1\le h\le x/q$, a finite sum (empty if $q>x$). Writing $C_x(hq)=D_x(hq)+A(hq)(x-hq)$,
$$\sum_l Q_l^2=Q(x)+2\sum_{1\le h\le x/q}D_x(hq)+2\sum_{1\le h\le x/q}A(hq)(x-hq). \tag{2}$$

## Step 3: evaluating $\Sigma_A:=\sum_{1\le h\le x/q}A(hq)(x-hq)$

By definition $A(hq)=A_0\sum_{t\ge1,\ t^2\mid hq}\eta(t)$. This is a finite sum, and only squarefree $t$ contribute because $\eta(t)=0$ otherwise.

**Divisibility lemma.** For squarefree $t$ and $h\in\mathbb N$: $t^2\mid hq\iff m_t(q)\mid h$.
*Proof.* Let $\gamma=\gcd(t^2,q)$. Then $t^2\mid hq\iff (t^2/\gamma)\mid h(q/\gamma)$. Since $\gcd(t^2/\gamma,q/\gamma)=1$, this holds iff $(t^2/\gamma)\mid h$, i.e. $m_t(q)\mid h$. $\square$

Hence, interchanging two finite sums (for $h\le x/q$ only $t$ with $t^2\mid hq\le x$ occur, so $t\le\sqrt x$),
$$\Sigma_A=A_0\sum_{t\ge1}\eta(t)\sum_{\substack{1\le h\le x/q\\ m_t(q)\mid h}}(x-hq).$$
Fix $t$, write $m=m_t(q)$, $M=qm$, $X=x/M$, $N=\lfloor X\rfloor$, $\theta=\{X\}$. Putting $h=jm$ ($1\le j\le N$), we have $x-hq=x-jM=M(X-j)$ and
$$\sum_{\substack{h\le x/q\\ m\mid h}}(x-hq)=M\sum_{j=1}^{N}(X-j)=M\Big(NX-\tfrac{N(N+1)}2\Big).$$
Substituting $N=X-\theta$:
$$NX-\tfrac{N(N+1)}{2}=\tfrac12(X-\theta)(X+\theta-1)=\tfrac12\big(X^2-X+\theta(1-\theta)\big)=\tfrac12\big(X^2-X+B(X)\big).$$
This is valid also when $N=0$ (then $X=\theta<1$, both sides vanish, as $B(X)=X-X^2$). Therefore
$$2\sum_{\substack{h\le x/q\\ m\mid h}}(x-hq)=M\big(X^2-X+B(X)\big)=\frac{x^2}{qm}-x+qm\,B\!\Big(\frac{x}{qm}\Big),$$
and
$$2\Sigma_A=A_0\sum_{t\ge1}\eta(t)\Big[\frac{x^2}{q\,m_t(q)}-x+q\,m_t(q)B\Big(\frac{x}{q\,m_t(q)}\Big)\Big]. \tag{3}$$
(The $t$-sum is a sum of finitely many nonzero terms *after* the bracket is rewritten as above; but each of the three pieces separately is an absolutely convergent series, since $\eta\ge0$, $\sum\eta<\infty$, $m_t(q)\ge1$, and $0\le q\,m\,B(x/(qm))\le x$ by $B(u)\le u$.) Splitting (3) into three series is therefore legitimate:

* $A_0\,x^2\sum_t \eta(t)/(q\,m_t(q))=x^2\cdot\frac{A_0}{q}\sum_t\eta(t)\frac{\gcd(t^2,q)}{t^2}=x^2S_2$ by P1(iv), because $1/m_t(q)=\gcd(t^2,q)/t^2$;
* $-A_0\,x\sum_t\eta(t)=-\dfrac{6x}{\pi^2}$ by P1(v);
* $A_0\,q\sum_t\eta(t)m_t(q)B(x/(qm_t(q)))=\mathrm{MT}(x;q)$ by definition.

So
$$2\Sigma_A=x^2S_2-\frac{6x}{\pi^2}+\mathrm{MT}(x;q). \tag{4}$$

## Step 4: conclusion

Insert (4) into (2), and then (2) into (1):
$$V(x;q)=Q(x)+2\!\!\sum_{1\le h\le x/q}\!\!D_x(hq)+x^2S_2-\frac{6x}{\pi^2}+\mathrm{MT}(x;q)-x^2S_2-2x\sum_lg_lE_l .$$
The $x^2S_2$ terms cancel, giving
$$V(x;q)=\mathrm{MT}(x;q)+2\sum_{1\le h\le x/q}D_x(hq)+\Big(Q(x)-\frac{6x}{\pi^2}\Big)-2x\sum_{l=1}^q g(q,l)E(x;q,l),$$
exactly as claimed. No inequalities or error terms were used; the identity is exact. $\blacksquare$

## Numerical sanity check

I checked the identity numerically in Python for $(x,q)=(200,7),(300,12),(150,1),(100,30),(97,5)$. $g$ was computed from P1(i) with the series truncated at $d<3\cdot10^5$, $A_0$ from primes below $2\cdot10^5$, and $\eta$ for $t<400$, with the tail $\sum_{t\ge400}\eta(t)$ taken from P1(v). Both sides agreed to about $10^{-3}$ or better, which is the truncation error. For example, at $(200,7)$ the left side is $3.8691$ and the right side is $3.8676$.
