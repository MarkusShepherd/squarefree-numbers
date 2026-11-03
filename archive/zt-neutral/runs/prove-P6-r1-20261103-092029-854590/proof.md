# Proof of P6

Only P5 (as stated in `deps/P5.md`) is used. Throughout, $\eta(t)=0$ for non-squarefree $t$, and $I=-4\zeta(-1/2)$ by P5(a).

## Step 0: elementary facts

* For every prime $p\ge2$, $p^2-2\ge p^2/2>0$. Hence for squarefree $t$, $0<\eta(t)\le 2^{\omega(t)}t^{-2}$.
* $\eta$ is multiplicative on squarefree integers: $\eta(ab)=\eta(a)\eta(b)$ if $\gcd(a,b)=1$.
* $\kappa(t)=t^2\eta(t)$ for all $t$, where $\kappa$ is as in P5.
* $0\le B(u)\le \min(1/4,u)$ for $u\ge0$.

**Absolute convergence.** Write $m=m_t(q)$. Then $\eta(t)\,m\,B\!\big(x/(qm)\big)\le \eta(t)\,m\cdot x/(qm)=\eta(t)x/q$. Also $\sum_t\eta(t)\le\sum_t 2^{\omega(t)}t^{-2}<\infty$. So the series defining $MT(x;q)$ converges absolutely, and its terms may be regrouped freely.

## Step 1: decomposition of $t$

Fix $q$. Every squarefree $t$ factors uniquely as $t=t_1t_2t_3$, where

* $t_1$ is composed of primes $p\nmid q$,
* $t_2$ is composed of primes $p\,\|\,q$,
* $t_3$ is composed of primes $p^2\mid q$.

Conversely, any triple $(t_1,t_2,t_3)$ of squarefree integers of these three types gives a squarefree $t$. The three factors are pairwise coprime. Let $\mathcal S_2$ and $\mathcal S_3$ be the sets of admissible $t_2$ and $t_3$. Both are finite, since $t_2,t_3\mid q$.

For squarefree $t$, $\gcd(t^2,q)=\prod_{p\mid t}p^{\min(2,v_p(q))}$. This equals $1$ on primes of $t_1$, $p$ on primes of $t_2$, and $p^2$ on primes of $t_3$. So $\gcd(t^2,q)=t_2t_3^2$ and
$$m_t(q)=\frac{t_1^2t_2^2t_3^2}{t_2t_3^2}=t_1^2t_2 .$$
Therefore
$$\frac{x}{q\,m_t(q)}=\frac{Z}{t_1^2},\qquad Z=Z(t_2):=\frac{x}{q\,t_2},$$
and $\eta(t)m_t(q)=\eta(t_2)\eta(t_3)\,t_2\cdot \eta(t_1)t_1^2=\eta(t_2)\eta(t_3)\,t_2\,\kappa(t_1)$.

By Step 0, regrouping gives
$$MT(x;q)=A_0\,q\sum_{t_2\in\mathcal S_2}\sum_{t_3\in\mathcal S_3}\eta(t_2)\eta(t_3)\,t_2\;\Sigma(t_2),\qquad
\Sigma(t_2)=\sum_{\substack{t_1\ge1\\(t_1,q)=1}}\kappa(t_1)B\!\Big(\frac{Z(t_2)}{t_1^2}\Big).$$

## Step 2: apply P5(c)

P5(c) holds for every $q\in\mathbb N$ and every real $Z>0$. Here $Z(t_2)=x/(qt_2)>0$, so
$$\Big|\Sigma(t_2)-\delta_qI\sqrt{Z(t_2)}\Big|\le c(\epsilon)\,q^{\epsilon}\,Z(t_2)^{1/3}.$$

**Main term.** Since $t_2\sqrt{Z(t_2)}=\sqrt{x/q}\;t_2^{1/2}$,
$$MT(x;q)=A_0\delta_qI\sqrt{xq}\sum_{t_2\in\mathcal S_2}\eta(t_2)t_2^{1/2}\sum_{t_3\in\mathcal S_3}\eta(t_3)\;+\;R,$$
where, using $0<A_0\le1$ and $t_2\,Z(t_2)^{1/3}=(x/q)^{1/3}t_2^{2/3}$,
$$|R|\le c(\epsilon)\,q^{1+\epsilon}\Big(\frac xq\Big)^{1/3}\Big(\sum_{t_2\in\mathcal S_2}\eta(t_2)t_2^{2/3}\Big)\Big(\sum_{t_3\in\mathcal S_3}\eta(t_3)\Big).$$

**The two finite sums.** By Step 0, $\eta(t_2)t_2^{2/3}\le 2^{\omega(t_2)}t_2^{-4/3}$. Hence
$$\sum_{t_2\in\mathcal S_2}\eta(t_2)t_2^{2/3}\le\prod_{p\mid q}\big(1+2p^{-4/3}\big)\le\prod_{p}\big(1+2p^{-4/3}\big)=:C_1<\infty .$$
Similarly
$$\sum_{t_3\in\mathcal S_3}\eta(t_3)\le\prod_p(1+2p^{-2})=:C_2<\infty .$$
Both bounds are absolute constants, independent of $q$ and $x$. So
$$|R|\le c(\epsilon)C_1C_2\,x^{1/3}q^{2/3+\epsilon}.$$
No use was made of $q\le x$ or $x\ge1$ in this step; the error bound holds for all $x>0$, $q\ge1$.

## Step 3: the constant equals $h(q)$

The sums over $\mathcal S_2,\mathcal S_3$ factor as Euler products over the finitely many primes dividing $q$:
$$\sum_{t_2\in\mathcal S_2}\eta(t_2)t_2^{1/2}=\prod_{p\|q}\Big(1+\frac{\sqrt p}{p^2-2}\Big),\qquad
\sum_{t_3\in\mathcal S_3}\eta(t_3)=\prod_{p^2\mid q}\Big(1+\frac1{p^2-2}\Big).$$
Also $A_0\delta_q=\prod_p(1-2/p^2)(1-1/p)\big(1+\mathbf 1[p\nmid q]\,p/(p^2-2)\big)$. This is a product of two absolutely convergent products (P5 for $\delta_q$), so it can be multiplied factor by factor. Collecting the local factor at each prime $p$:

* $p\nmid q$:
$$\Big(1-\tfrac2{p^2}\Big)\Big(1-\tfrac1p\Big)\Big(1+\tfrac{p}{p^2-2}\Big)=\frac{(p-1)(p^2+p-2)}{p^3}=\frac{(p-1)^2(p+2)}{p^3}=1-\frac3{p^2}+\frac2{p^3}.$$
* $p\,\|\,q$:
$$\Big(1-\tfrac2{p^2}\Big)\Big(1-\tfrac1p\Big)\Big(1+\tfrac{\sqrt p}{p^2-2}\Big)=\frac{(p-1)(p^2-2+\sqrt p)}{p^3}.$$
* $p^2\mid q$:
$$\Big(1-\tfrac2{p^2}\Big)\Big(1-\tfrac1p\Big)\Big(1+\tfrac1{p^2-2}\Big)=\frac{(p-1)(p^2-1)}{p^3}=\frac{(p-1)^2(p+1)}{p^3}.$$

The product of these local factors, times $I=-4\zeta(-1/2)$, is exactly $h(q)$. The product over $p\nmid q$ converges absolutely, since its factors are $1+O(p^{-2})$. Hence
$$A_0\,\delta_q\,I\sum_{t_2}\eta(t_2)t_2^{1/2}\sum_{t_3}\eta(t_3)=h(q).$$

## Conclusion

For all real $x>0$ (in particular $x\ge1$) and all integers $q\ge1$ (in particular $1\le q\le x$),
$$\big|MT(x;q)-h(q)\sqrt{xq}\big|\le C_1C_2\,c(\epsilon)\;x^{1/3}q^{2/3+\epsilon},$$
where $c(\epsilon)$ is the constant of P5(c) and $C_1,C_2$ are absolute. This is the claim, with constant $C_1C_2c(\epsilon)$ depending only on $\epsilon$. $\qquad\blacksquare$

## Numerical sanity check

I computed $MT(x;q)$ with $t\le3000$ and compared it with $h(q)\sqrt{xq}$ for $(x,q)=(10^6,12)$, $(10^6,72)$, $(123457,30)$ and $(10^6,360)$. The differences ($92$, $78$, $17$ and $53$) were below $x^{1/3}q^{2/3}$ in each case. The case $(10^6,1)$ gave a difference of $92$ against $x^{1/3}q^{2/3}=100$. These runs are only a rough check of the constant $h(q)$, because truncating at $t\le 3000$ discards a tail of size about $A_0 x/(q\cdot 3000)$. The local-factor identities of Step 3 were verified by hand above.
