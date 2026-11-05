# Assembly of P1–P7

Integrator's report. Inputs: `problem.md`, `plan.json`, `props/P1..P7/{statement,proof}.md`,
`results.json`. The only external text I opened was the supplied
`papers/bgpvw-1998.pdf` (J. Brüdern, A. Granville, A. Perelli, R. C. Vaughan,
T. D. Wooley, *On the exponential sum over k-free numbers*, Phil. Trans. R. Soc.
Lond. A 356 (1998) 739–761, doi:10.1098/rsta.1998.0183). I used it only to confirm
that P2 quotes Lemma 2.2 correctly; the quotation is accurate. I did not access
any excluded author, the excluded paper, GitLab, other runs or post-2010 sources.
My scripts are in `scripts/` (`constants.py`, `profile.py`).

Notation: $c=\zeta(2)^{-1}$, $d=\deg f$, $a=4d-1$, $\theta=2d/a$,
$\eta=\eta_d=\min\{1/5,1/a\}$, $Y=f(y)$. $W_f$, $D_f$, $R_f$, $B_f$, $K_f$, $\Theta_f$ and $F_f$
are as in P7. Their definitions in P4, P5, P6 and P7 agree verbatim; the
identifications between them are listed in §2.

## 1. Explicit composition

Fix $0<\varepsilon<\eta/2$ and put $\delta=\varepsilon/2$. Take $x\ge x_0(f)$, so that
$Z:=x^\theta\ge\max\{2,f(1)\}$ and $R:=x^{2/a}\ge 2$. Let $z\ge1$ be the
unique real number with $f(z)=Z$; it exists because $f'\ge1$.

**Case $Y\ge Z$.** Then $z\le y$, and exactly
$V_f(x,y)=V_f(x,z)+V_f(x;z,y)$.

*Step 1 (P2, first part, exponent $\delta$).* This step needs
$x\ge2$, $1\le z\le y$ and $Z\le Y\le x$:
$$V_f(x;z,y)=cx(Y-Z)+2S_f(x;z,y)-x^2T_f(z,y)+O_{f,\varepsilon}\big(x^{3/2+\delta}+xY^{1-1/d}\big).$$

*Step 2 (P3, exponent $\delta$).* For $z<k\le y$ and $1\le h\le x/f(k)$, the
number $m=hf(k)$ is an integer in $[1,x]$, so P3 applies to it. There are
$\le x/f(k)$ values of $h$, and $f'(k)/f(k)\ll_f 1/k$, $y\ll_f x^{1/d}$. Hence
$$S_f=M+O_{f,\varepsilon}\big(x^{9/5+\delta}\log 2x\big),\qquad
M:=\sum_{z<k\le y}f'(k)\sum_{h\le x/f(k)}(x-hf(k))\,\mathfrak S(hf(k)).$$

*Step 3 (P4).* This step needs $x\ge2$, $1\le z\le y$, $Z\le Y\le x$ and $2\le R\le x$. With
$A=Z^{-1/d}R^{1/2}\log^2(2R)+R^{-1/2}\log^2(2R)\log(2x)$:
$$T_f=R_f\log(Y/Z)+O_f(A),\qquad M=I+O_f(x^2A),\quad I:=\int_Z^Y\sum_{h\le x/t}(x-ht)W_f(h)\,dt .$$
P4's coefficient is $\sum_r\lambda(r)\rho(r)/r$. P5 shows that it equals $P_f(1)=\operatorname{Res}_{s=1}D_f$, which is the
$R_f$ of P6 and P7.

*Step 4 (P6 integral identity; needs $2\le Z\le Y\le x$).* Exactly,
$2I=Z^2\Theta_f(x/Z)-Y^2\Theta_f(x/Y)$. From the definition of $F_f$, the
following identity also holds exactly:
$$x^2\big(F_f(x/Y)-F_f(x/Z)\big)=-x^2R_f\log(Y/Z)+cx(Y-Z)+Z^2\Theta_f(x/Z)-Y^2\Theta_f(x/Y).$$
I re-derived both identities. The $B_f$ terms cancel, and the $cx(Y-Z)$
from P2 is matched by the $c/H$ term of $F_f$.

*Steps 1–4 combined.* The errors from Step 3 are multiplied by $2$ (on $S_f$)
and by $x^2$ (on $T_f$). This gives
$$\Big|V_f(x;z,y)-x^2\big(F_f(x/Y)-F_f(x/Z)\big)\Big|\ll_{f,\varepsilon}
x^{3/2+\delta}+xY^{1-1/d}+x^{9/5+\delta}\log 2x+x^2A. \tag{$*$}$$

*Step 5 (boundary terms).*
- P2, second part, at $z$: $0\le V_f(x,z)\ll_{f,\varepsilon} x^{1+\delta}Z^{2-1/d}=x^{2-1/a+\delta}$, since $1+\theta(2-1/d)=2-1/a$.
- P6, using $|F_f(H)|\ll_f H^{-3/2}$ for $H\ge1$: $x^2|F_f(x/Z)|\ll_f x^{1/2}Z^{3/2}=x^{1/2+3d/a}\le x^{2-1/a}$, because $(2-1/a)-(1/2+3d/a)=(6d-5)/(2a)>0$.

*Step 6 (bounding each error term).* With $Z^{-1/d}R^{1/2}=R^{-1/2}=x^{-1/a}$:

| term | bound | uses |
|---|---|---|
| $x^{3/2+\delta}$ | $\le x^{2-\eta+\varepsilon}$ | $\eta\le 1/5<1/2$ |
| $xY^{1-1/d}$ | $\le x^{2-1/d}\le x^{2-\eta}$ | $Y\le x$, $\eta\le 1/a\le 1/d$ |
| $x^{9/5+\delta}\log 2x$ | $\ll_\varepsilon x^{9/5+\varepsilon}\le x^{2-\eta+\varepsilon}$ | $\eta\le1/5$ (**this is the source of the cap $1/5$**) |
| $x^2A$ | $\ll x^{2-1/a}\log^3 2x\ll_\varepsilon x^{2-\eta+\varepsilon}$ | $\eta\le 1/a$ |
| $V_f(x,z)$ | $\ll x^{2-1/a+\delta}$ | $\eta\le 1/a$ |
| $x^2\lvert F_f(x/Z)\rvert$ | $\ll x^{2-1/a}$ | Step 5 |

Therefore $|V_f(x,y)-x^2F_f(x/Y)|\ll_{f,\varepsilon}x^{2-\eta+\varepsilon}$.

**Case $Y<Z$.**
- P2, second part, at $y$: $V_f(x,y)\ll x^{1+\delta}Y^{2-1/d}\le x^{2-1/a+\delta}$.
- P6: $x^2|F_f(x/Y)|\ll x^{1/2}Y^{3/2}\le x^{2-1/a}$.

The triangle inequality gives the same bound $x^{2-\eta+\varepsilon}$.

**Power main term.** By P6, $|F_f(H)-K_fH^{-3/2}|\le C_fH^{-13/8}$ for $H=x/Y\ge1$. Multiplying by $x^2$:
$$|x^2F_f(x/Y)-K_fx^{1/2}Y^{3/2}|\le C_f\,x^{3/8}Y^{13/8}.$$
Combined with the profile estimate:
$$|V_f(x,y)-K_fx^{1/2}Y^{3/2}|\ll_{f,\varepsilon}x^{3/8}Y^{13/8}+x^{2-\eta+\varepsilon}.$$

**Corollary in the plan.** Take $0<\delta'<\eta/3$, $x^{1-2\eta/3+\delta'}\le Y\le x^{1-\delta'}$ and $\varepsilon=\delta'$
(admissible, since $\delta'<\eta/2$). The two relative errors are:
- $x^{3/8}Y^{13/8}/(x^{1/2}Y^{3/2})=(Y/x)^{1/8}\le x^{-\delta'/8}$;
- $x^{2-\eta+\delta'}/(x^{1/2}Y^{3/2})\le x^{-\delta'/2}\le x^{-\delta'/8}$.

Since $K_f>0$ (P5), this gives $|V_f/(K_fx^{1/2}Y^{3/2})-1|\ll_{f,\delta'}x^{-\delta'/8}$ for $x\ge x_0$.

All constants depend only on $f$ and $\varepsilon$. **The propositions compose to the plan's main theorem exactly, with no loss.**

Explicit exponents:

| $d$ | $\eta_d$ | where $V_f\sim K_f x^{1/2}Y^{3/2}$ is guaranteed |
|---|---|---|
| 1 | $1/5$ | $x^{13/15+\delta}\le Y\le x^{1-\delta}$ |
| 2 | $1/7$ | $x^{19/21+\delta}\le Y\le x^{1-\delta}$ |
| 3 | $1/11$ | $x^{31/33+\delta}\le Y\le x^{1-\delta}$ |

## 2. Interface check

Each item below is a hypothesis of one proposition, checked at the point where P7 uses it:

- **P2 ranges.** P2 needs $x\ge2$, $1\le z\le y$ and $Z\le Y\le x$, with real $z,y$. P7's $z$ is real with $f(z)=x^\theta$, and $z\le y$ by monotonicity. The initial-modulus bound needs $z\ge1$ and $f(z)\le x$; P7 also applies it at $z=y$ when $Y<Z$. ✓
- **P3 range.** P3 needs an integer $1\le m\le x$ and is uniform in $m$, including when $x-m$ is bounded. P7 uses $m=hf(k)$ with $h\le x/f(k)$. ✓ P3 proves the stronger bound $x^{4/5}$, which has no $\varepsilon$. It lists P1 as a dependency but does not use it; this is harmless.
- **P3 and P4 definitions.** The definitions of $C_x$ and $\mathfrak S$ are identical in P2, P3 and P4. ✓
- **P4 ranges.** P4 needs $2\le R\le x$ and $2\le Z$; the latter follows from $f(1)\ge2$. P7's choice $R=x^{2/a}$ satisfies both once $x\ge x_0$. The $Z^{-1/d}$ in $A$ comes from a factor $1/z$, valid for real $z$. ✓
- **P4/P5 constant.** P4 defines $R_f=\sum\lambda\rho/r$, with $\lambda=c^2\varphi\prod_{p\mid r}(p^2-1)^{-2}$, which equals P1's $\varphi\gamma^2$. P6 and P7 define $R_f$ as $\operatorname{Res}_{s=1}D_f$. P5 proves that both equal $P_f(1)$. ✓
- **$B_f$.** P5 gives $B_f=(\gamma_E-3/2)R_f+P_f'(1)$, and P6 and P7 use the Laurent definition; P5 (26) proves they agree. In any case $B_f$ cancels in the assembly.
- **$K_f$.** P5 gives $K_f=-\tfrac83\zeta(-\tfrac12)H_f(-\tfrac12)$, and P6 and P7 use $-\tfrac{16}3\operatorname{Res}_{-1/2}D_f$. They agree, because the residue of $\zeta(2s+2)$ at $s=-\tfrac12$ is $\tfrac12$. ✓
- **$D_f(0)=-1/(2\zeta(2))$.** P5 states this and P6 uses it to produce the $+cH$ term. ✓
- **P5→P6 uniformity (minor, not a defect).** P5 bounds $H_f$ only on each fixed vertical line ($C(f,\sigma)$). P6 needs a bound that is uniform on the strip $-5/8\le\sigma\le2$. P6 proves this itself from the Euler product (its eq. (9)) and does not rely on P5 for it. The contour line $\Re s=-5/8$ lies inside P5's region of continuation, $\Re s>-3/4$. ✓
- **P6 ranges.** The bound $|F_f-K_fH^{-3/2}|\le CH^{-13/8}$ holds for all real $H\ge1$; P7 uses it at $H=x/Y$ and $H=x/Z$, both $\ge1$. The integral identity needs $2\le Z\le Y\le x$. ✓
- **External input.** P2 uses BGPVW Lemma 2.2 with $k=2$ and $1\le Q\le x$, which states $\Upsilon_2(x,Q)\ll x^{1+\varepsilon}Q$. I checked the PDF: the quotation is exact. P2 also correctly checks that the source's normalisation of $E$ matches ours and that all residue classes are included.

No proposition is used with a range, uniformity or error term other than the one it states. Two points are cosmetic only: the P3 dependency that is listed but unused, and the strip uniformity that P6 supplies itself rather than taking from P5.

## 3. Numerics

I recomputed the constants independently (`scripts/constants.py`), with Euler products over $p\le10^7$ plus a tail correction. The values agree with those from $p\le10^6$ to 7 digits.

| $f$ | $R_f$ | $B_f$ | $H_f(-1/2)$ | $K_f$ | `constant_extrapolated` | rel. discrepancy $(K_f-C)/C$ |
|---|---|---|---|---|---|---|
| $k^2+1$ | 0.3923477 | −0.4368427 | 0.2490833 | **0.1380826** | 0.134475 ± 0.007285 | **+2.68 %** (0.50 of the band) |
| $k^3+2$ | 0.3953324 | −0.4418196 | 0.2446185 | **0.1356075** | 0.136321 ± 0.002404 | **−0.52 %** (0.30 of the band) |
| $2k+1$ (extra) | 0.3786969 | −0.4242357 | 0.2572561 | 0.1426133 | 0.141686 ± 0.008218 | +0.65 % |

These match the plan's values (0.138083, 0.135608, 0.142613). None of the discrepancies is close to a clean factor.

**Diagnosing the extrapolation.** I fitted the snapshot's own model, $N(r)=C+a\sqrt r+br$, to the eight largest-$x$ ratios. I did this once on the data and once on the **exact predicted profile** $N_{\rm pred}(r)=F_f(H)H^{3/2}$ at $H=x/Y$ (`scripts/profile.py`). Intercepts:

| $f$ | fit to data | fit to predicted profile | true limit $K_f$ |
|---|---|---|---|
| $k^2+1$ | 0.134475 | 0.134364 | 0.138083 |
| $k^3+2$ | 0.136321 | 0.135793 | 0.135608 |
| $2k+1$ | 0.141686 | 0.141685 | 0.142613 |

Applied to the predicted profile, the fit model reproduces the snapshot's intercepts to within 0.08 %, 0.4 % and 0.001 %. So the 2.7 % gap for $k^2+1$ is bias in the three-term model, not an error in $K_f$. The profile approaches $K_f$ slowly: at $H=200,400,700,1000$, $N_{\rm pred}$ for $k^2+1$ is 0.14024, 0.13963, 0.13891, 0.13877.

**Direct profile comparison** at $x=2.56\cdot10^8$, $(N_{\rm data}/N_{\rm pred}-1)$ over the eight ratios plus the diagnostic ratio 0.005:

| $f$ | range of $N_{\rm data}/N_{\rm pred}-1$ | trend from $x=1.28\cdot10^8$ to $2.56\cdot10^8$ |
|---|---|---|
| $k^2+1$ | +0.007 % to +0.10 % | decreasing at most ratios |
| $k^3+2$ | −0.02 % to +2.2 % | decreasing at 7 of 9 ratios |
| $2k+1$ | ≤ 0.0005 % | — |

For $k^3+2$, $y$ is small (86–635), so the $k$-sampling terms (the $Z^{-1/d}$ terms in P4) are large at this $x$. The theorem's error bound $x^{2-1/11}$ is not small at $x\approx 2.6\cdot10^8$; relative to the main term it is $\approx x^{-1/11}r^{-3/2}$. The numerics are therefore consistent with the theorem but cannot test its error exponent.

## 4. Final theorem (what P1–P7 prove)

Let $f\in\mathbb Z[t]$ with $\deg f=d\ge1$, $f(t)\ge2$ and $f'(t)\ge1$ for $t\ge1$; no irreducibility or squarefreeness condition is needed. Put $Y=f(y)$ and $\eta_d=\min\{1/5,1/(4d-1)\}$. Define
$$W_f(h)=\prod_p(1-2p^{-2})\Big[1+\rho(p^{j})/(p^{j}(p^2-2))\Big],\qquad j=\max\{2-v_p(h),0\},$$
and
$$\Theta_f(H)=\sum_{h\le H}W_f(h)(H-h)^2/h,\qquad F_f(H)=R_f\log H+B_f+1/(\zeta(2)H)-\Theta_f(H)/H^2,$$
where $R_f$ and $B_f$ are the residue and the shifted constant term of $D_f(s)=\sum W_f(h)h^{-s}$ at $s=1$. Let $K_f=-\tfrac83\zeta(-\tfrac12)H_f(-\tfrac12)>0$, with $H_f$ the Euler product of P5.

Then for $0<\varepsilon<\eta_d/2$, uniformly for $x\ge x_0(f,\varepsilon)$ and real $y\ge1$ with $Y\le x$:
$$V_f(x,y)=x^2F_f(x/Y)+O_{f,\varepsilon}(x^{2-\eta_d+\varepsilon}),$$
$$V_f(x,y)=K_fx^{1/2}Y^{3/2}+O_{f,\varepsilon}(x^{3/8}Y^{13/8}+x^{2-\eta_d+\varepsilon}).$$
Consequently, $V_f\sim K_fx^{1/2}Y^{3/2}$ with relative error $\ll x^{-\delta/8}$ for $x^{1-2\eta_d/3+\delta}\le Y\le x^{1-\delta}$.

This is exactly the plan's main theorem; there is no loss.
