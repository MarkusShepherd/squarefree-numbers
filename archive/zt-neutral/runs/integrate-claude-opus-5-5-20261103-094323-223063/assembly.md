# Assembly of P1–P9 (integrator report)

Sources: only the files in this folder: `props/*`, `plan.json`, `results.json`, and
`papers/vaughan-2005.pdf`, which I used solely for the constant check in §4: R. C. Vaughan, *A variance for k-free numbers in
arithmetic progressions*, Proc. London Math. Soc. (3) 91 (2005) 573–597,
doi:10.1112/S0024611505015352, eqs. (1.13)–(1.15). I did no web search. I did not
search for, open or use any work by the excluded author or the excluded paper,
and I used no post-2010 source.

Notation is as in the propositions: $Y=f(y)$, $F=f'f^{1/2}$, and
$V(x;q)=\sum_{l\le q}E(x;q,l)^2$, so $V_f(x,y)=\sum_{k\le y}f'(k)V(x;f(k))$.

## 1. Dependency graph and hypotheses actually used

| used | where | hypothesis required by the statement | hypothesis available at the call site | ok |
|---|---|---|---|---|
| P1(iv),(v) | P2 step 3 | $q\in\mathbb N$ | any $q$ | ✓ |
| P1(i),(iii) | P4(ii) | $q\in\mathbb N$, $n$ squarefree | same | ✓ |
| P2 | P7 | real $x\ge1$, $q\in\mathbb N$ | $x\ge2$, $1\le q\le x$ | ✓ |
| P3 | P7 | real $x\ge2$, integer $1\le m\le x$ | $m=hq$, $1\le h\le x/q$, so $q\le m\le x$ | ✓ |
| P4(i) | P7 | $x\ge1$ | $x\ge2$ | ✓ |
| P4(ii) | P7 | $x\ge1$, $1\le q\le x$ | same | ✓ |
| P5(a),(c) | P6 | all $q\in\mathbb N$, all real $Z>0$ | $Z=x/(qt_2)>0$ | ✓ |
| P6 | P7(ii) | $x\ge1$, $1\le q\le x$ | $x\ge2$, $1\le q\le x$ | ✓ |
| P7(i),(ii) | P9 | $x\ge2$, $1\le q\le x$ | $q=f(k)$, $k\le y$: $2\le f(k)\le f(y)=Y\le x$, since $f'\ge1$ on $[1,\infty)$ | ✓ |
| P8(0),(a),(b),(c) | P9 | $f$ as in problem.md, $y\ge1$ | same | ✓ |

Every symbol has the same definition wherever it appears: $A_0$, $\eta$,
$m_t(q)$, $B$, $\mathrm{MT}$, $h$, $\tau_p$, $C_f$, $C_x(m)$, $A(m)$ and $D_x(m)$.
In particular, P6, P7 and P8 use the same formula for $h$, and P8 and the plan use
the same formula for $\tau_p$. Every implied constant depends only on the
parameters the statements allow: $\varepsilon$ in P3, P5, P6 and P7, absolute in
P4, and $f,\varepsilon$ in P8 and P9. No proposition is used outside its stated
range, uniformity or error term.

## 2. Explicit composition

Fix $\varepsilon>0$, real $x\ge2$, $y\ge1$ with $Y\le x$.

**Single modulus (P2 + P3 + P4 → P7(i)).** For $2\le q\le x$, P2 gives the exact identity
$$V(x;q)-\mathrm{MT}(x;q)=2\!\!\sum_{h\le x/q}\!\!D_x(hq)+(Q(x)-6x/\pi^2)-2x\sum_l g(q,l)E(x;q,l).$$
The three terms are bounded as follows:
- by P3, $|2\sum_{h\le x/q} D_x(hq)|\le 2(x/q)\,c_3(\varepsilon)x^{2/3+\varepsilon}$;
- by P4(i), $|Q(x)-6x/\pi^2|\le c_0\sqrt x$;
- by P4(ii), $|2x\sum_l gE|\le 2c_0x^{3/2}/q\le 2c_0x^{5/3+\varepsilon}/q$.

Hence
$$|V(x;q)-\mathrm{MT}(x;q)|\le (2c_3(\varepsilon)+2c_0)\,x^{5/3+\varepsilon}q^{-1}+c_0x^{1/2}.\tag{A}$$

**Main term per modulus (P5 → P6; P6 + (A) → P7(ii)).**
$$|\mathrm{MT}(x;q)-h(q)\sqrt{xq}|\le c_6(\varepsilon)x^{1/3}q^{2/3+\varepsilon}.\tag{B}$$

**Summation over $q=f(k)$ (P8(b),(c)).** Multiply (A) and (B) by $f'(k)>0$ and sum over $k\le y$:
- $\sum_{k\le y} f'(k)\,x^{5/3+\varepsilon}/f(k)\le c(f)(1+\log Y)x^{5/3+\varepsilon}\le c(f,\varepsilon)x^{5/3+2\varepsilon}$;
- $\sum_{k\le y} f'(k)\,x^{1/2}\le c(f)x^{1/2}Y$;
- $\sum_{k\le y} f'(k)\,x^{1/3}f(k)^{2/3+\varepsilon}\le x^{1/3}Y^{2/3+\varepsilon}\cdot c(f)Y\le c(f)x^{1/3+\varepsilon}Y^{5/3}$.

Renaming $\varepsilon$ gives
$$\Big|V_f(x,y)-\sum_{k\le y}f'(k)\mathrm{MT}(x;f(k))\Big|\le c(f,\varepsilon)\big(x^{5/3+\varepsilon}+x^{1/2}Y\big),\tag{ii}$$
$$\Big|V_f(x,y)-x^{1/2}\sum_{k\le y}F(k)h(f(k))\Big|\le c(f,\varepsilon)\big(x^{1/3+\varepsilon}Y^{5/3}+x^{5/3+\varepsilon}+x^{1/2}Y\big).\tag{C}$$

**Average of $h$ over polynomial values (P8(a)).**
$|\sum_{k\le y}F(k)h(f(k))-C_fY^{3/2}|\le c(f,\varepsilon)Y^{3/2+\varepsilon}y^{-1/2}$.
Since $Y=f(y)\le(\sum|a_i|)y^d$, we have $y^{-1/2}\ll_f Y^{-1/(2d)}$. Using $Y^\varepsilon\le x^\varepsilon$ and multiplying by $x^{1/2}$, this error becomes $\ll x^{1/2+\varepsilon}Y^{3/2-1/(2d)}$.
Also $x^{1/2}Y\le x^{1/2}Y^{3/2-1/(2d)}$, because $Y\ge2$ and $d\ge1$. Combining with (C):
$$\big|V_f(x,y)-C_fx^{1/2}Y^{3/2}\big|\le c(f,\varepsilon)\big(x^{1/3+\varepsilon}Y^{5/3}+x^{5/3+\varepsilon}+x^{1/2+\varepsilon}Y^{3/2-1/(2d)}\big).\tag{i}$$

**Corollary.** Divide each error in (i) by $x^{1/2}Y^{3/2}$ and use $x^{7/9+\delta}\le Y\le x^{1-\delta}$ with $\varepsilon=\min(\delta/12,1/(9d))$:
- $x^{-1/6+\varepsilon}Y^{1/6}\le x^{-\delta/6+\varepsilon}\le x^{-\delta/12}$;
- $x^{7/6+\varepsilon}Y^{-3/2}\le x^{-3\delta/2+\varepsilon}\le x^{-\delta/12}$;
- $x^{\varepsilon}Y^{-1/(2d)}\le x^{1/(9d)-7/(18d)}=x^{-5/(18d)}\le x^{-1/(6d)}$.

P8(0) gives $0<C_f<\infty$. Hence $V_f=C_fx^{1/2}Y^{3/2}(1+O_{f,\delta}(x^{-\eta}))$ with $\eta=\min(\delta/12,1/(6d))$.

So (i), (ii) and the corollary match the statement of P9 and the plan's main theorem exactly, with every error term accounted for. **The propositions compose.**

Benign observations, none of them a mismatch:
- P4(ii) is proved for all $q\ge1$, which is more than stated.
- P6 is proved for all $x>0$.
- P9's step $Y^{\varepsilon}\le x^{\varepsilon}$ uses $Y\le x$, which is a hypothesis.
- In the corollary the bound for the third error is $x^{-5/(18d)}$, stronger than the stated $x^{-1/(6d)}$.
- The term $x^{1/3+\varepsilon}Y^{5/3}$ is $o(x^{1/2}Y^{3/2})$ only for $Y\le x^{1-\delta}$. This is why the range stops at $x^{1-\delta}$ and not at $Y\asymp x$.

## 3. Constant $C_f$, numerically

$C_f=\tfrac23\,(-4\zeta(-\tfrac12))\prod_p\tau_p$, with $-4\zeta(-1/2)=0.8315448999$. I evaluated the product over primes $p<2\cdot10^7$; the tail changes the result by about $10^{-8}$ in relative terms.

- $f=k^2+1$:
  - local data: $\rho(2)=1$, $\rho(4)=0$, and $\rho(p)=\rho(p^2)=1+\left(\frac{-1}{p}\right)$ for odd $p$;
  - **$C_{k^2+1}=0.1380826$**.
- $f=k^3+2$:
  - local data: $\rho(2)=\rho(3)=1$ and $\rho(4)=\rho(9)=0$; for $p\equiv2\ (3)$, $\rho(p)=1$; for $p\equiv1\ (3)$, $\rho(p)=3$ or $0$ according as $-2$ is a cube mod $p$ or not; for $p\ge5$, $\rho(p^2)=\rho(p)$;
  - **$C_{k^3+2}=0.1356075$**.
- I checked both sets of $\rho$-values by brute force for all $p<300$, both mod $p$ and mod $p^2$; there were no mismatches.

Check against the full variance: for $f(t)=t$ the formula gives $C_t=0.12847867$. Vaughan (2005), (1.14)–(1.15) with $k=2$, gives
$c_2=8C_1(-\zeta(-1/2))/(3\zeta(2)^2)$ with $C_1=0.62709534$, so $c_2=0.12847867$. The two agree to all printed digits.

## 4. Comparison with `results.json`

| $f$ | $C_f$ (predicted) | `constant_extrapolated` | relative discrepancy (extrap − pred)/pred | in units of stated uncertainty |
|---|---|---|---|---|
| $k^2+1$ | 0.138083 | 0.134475 ± 0.007285 | **−2.61 %** | −0.50 |
| $k^3+2$ | 0.135608 | 0.136321 ± 0.002404 | **+0.53 %** | +0.30 |

Neither discrepancy is a clean factor; the ratios are 1.027 and 0.995. Both lie inside the stated heuristic envelopes.

**Cross-check of the data against the proved shape (ii).** I computed $\sum_{k\le y}f'(k)\mathrm{MT}(x;f(k))$ independently in my own code (`$TMPDIR/w/mt.py`). It uses the full $t$-sum up to $20\sqrt{x/q}$, and the exact tail identity $\eta(t)m_tB(u)=\eta(t)(x/q)(1-u)$ for $u<1$. For every row at $x=10^6$ and $x=1.6\cdot10^7$, all eight ratios and both polynomials, $V/\sum f'\mathrm{MT}$ lies in $[0.9985,1.0008]$. This confirms that the exact-shape statement (ii) describes the data.

**Why the $k^2+1$ extrapolation sits 2.6 % low.** The finite-ratio drift is a genuine secondary term in $\mathrm{MT}$ of relative size about $a\sqrt{r}$, where $r=f(y)/x$. Near $r=0$ the slope $a$ is about $0.027$. The data's 3-parameter fit $C+a\sqrt r+br$ over $r\in[0.01,1]$ returns $a=0.058$, so its intercept is pulled down. The alternative fits recorded in `results.json` give:
- $0.1384$ for the pure $C+a\sqrt r$ model;
- $0.1371$ for the model with an added $r^{3/2}$ term;
- $0.1418$ for the fit with $r\le0.1$.

These bracket $C_f$, so the spread comes from the extrapolation model, not from the constant.

I confirmed this by evaluating the proved main-term shape at $x=10^{12}$ and much smaller ratios than the data reach. Here $N_{\rm MT}=\sum f'\mathrm{MT}/(x^{1/2}Y^{3/2})$ and $N_h=\sum_{k\le y}F(k)h(f(k))/Y^{3/2}$:

| $f$ | $r$ | $y$ | $N_{\rm MT}$ | $N_h$ |
|---|---|---|---|---|
| $k^2+1$ | $10^{-2}$ | 99999 | 0.14077 | 0.13808 |
| $k^2+1$ | $10^{-3}$ | 31622 | 0.13880 | 0.13809 |
| $k^2+1$ | $10^{-4}$ | 9999 | 0.13820 | 0.13810 |
| $k^3+2$ | $10^{-2}$ | 2154 | 0.13873 | 0.13575 |
| $k^3+2$ | $10^{-3}$ | 999 | 0.13656 | 0.13594 |
| $k^3+2$ | $10^{-4}$ | 464 | 0.13626 | 0.13624 |

How to read this table:
- At $r=0.01$, $N_{\rm MT}=0.14077$ agrees with the data's value $0.14086$ at $x=2.56\cdot10^8$. So the normalised variance at fixed $r$ is stable in $x$.
- As $r\to0$, $N_{\rm MT}$ approaches $N_h$, and the gap behaves like $0.027\sqrt r$.
- $N_h\to C_f$ as $y\to\infty$, which is the P8(a) convergence. For $k^3+2$ at small $r$, $y$ is only a few hundred, so $N_h$ still carries the finite-$y$ fluctuation $O(y^{-1/2})$.

Everything is consistent with $C_{k^2+1}=0.13808$ and $C_{k^3+2}=0.13561$.

## 5. Final theorem proved

The theorem proved is exactly the plan's main theorem, with no loss: (i), (ii) and the corollary (b) on $x^{7/9+\delta}\le f(y)\le x^{1-\delta}$, with $\eta=\min(\delta/12,1/(6d))$, the weight $f'(k)$, and the class of $f$ as in problem.md.

The plan itself is deliberately weaker than what the circle method should give, and the reason is known. P3's pointwise bound $D_x(m)\ll x^{2/3+\varepsilon}$, summed trivially over $h\le x/q$, costs $x^{5/3+\varepsilon}$. This forces $Y\ge x^{7/9+\delta}$. P5(b)'s $Z^{1/3}$ bound gives the $(Y/x)^{1/6}$ loss, which forces $Y\le x^{1-\delta}$.
