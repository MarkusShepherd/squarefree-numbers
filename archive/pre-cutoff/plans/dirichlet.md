# Plan: dirichlet

Model: claude-opus-5-5

PLAN IN ONE PARAGRAPH. Fix one modulus q and split mu^2 = alpha + beta at d <= z. For alpha, the sum over differences hq is evaluated EXACTLY: the Fejer identity sum_{i in Z}(x-|i|q')_+ = x^2/q' + q'B({x/q'}), with B(t)=t(1-t), cancels the g^2 term and the diagonal in closed form, and leaves V(x;q) ~ q A_q(x/q), an explicit sum over squarefree c. For beta, an elementary pair count (Cauchy-Schwarz over ratios t = a^2/b^2 mod m, plus a lattice bound) gives ||E_beta||^2 << x^eps(x/z + x/q^{1/2} + x^2/(z^2 q)). This yields, for every individual q in x^{2/3} <= q <= x, V(x;q) = q A_q(x/q) + O(x^eps(x^{7/6}q^{-1/2} + x^{4/5})). Averaging over k with the Dirichlet series D_f(w) = zeta(2w)G_f(w) gives the main term x^{1/2}Y^{3/2} N_f(Y/x), which tends to C_f x^{1/2}Y^{3/2} as Y/x -> 0. Sparsity and the degree d enter only through the local densities and the error term y^{-1/2}.

HOW THIS RELATES TO THE HINT. I followed its reduction to the off-diagonal count and the generating Dirichlet series, but no contour shift is needed. The h-sum is exact, the only pole that matters (s=-1/2, i.e. w=1/2) is read off from zeta(2w), and the remainder is handled by an elementary sum-versus-integral argument (P5). The circle method is not used at all. The papers Brüdern-Wooley and BGPVW are not used, so no proposition cites them.

NUMERICS CHECK (all by hand: I had no code execution in this session). Numerics are sharp only near r=1, and there the plan's closed form gives N_f(1) = 6/pi^2 - (3/2 - gamma_E) D_f(2) + D_f'(2): k^2+1 predicted 0.17108, numerics 0.1712; 2k+1 predicted 0.18369, numerics 0.1837; k^3+2 predicted 0.16614, numerics 0.1680 and still falling (0.1696, 0.1685, 0.1680 at x=2e6, 5e6, 1e7, with y <= 215). The k^3+2 value is NOT yet confirmed: the gap is about 1%, the direction is right, and P7's error y^{-1/2} is plausibly the cause. An independent hand check on x-> q-> x with prime-like q also gives 6/pi^2(1-6/pi^2) = 0.2384 vs the formula's about 0.239. Predicted C_f: 0.1381 (k^2+1), 0.1356 (k^3+2), 0.1426 (2k+1); the extrapolated values are about 0.14 +- 0.01, so these agree but only weakly. C_f genuinely depends on f, which those extrapolations cannot resolve. The fitted beta of about 1.54 is explained by N_f(r) rising with r, not by a different exponent; alpha+beta=2 holds.

KNOWN LIMITS AND FLAGS. (1) Range: the main theorem stops at x^{2/3}, the same threshold GMRR report for Warlimont and Vaughan with all moduli. Gorodetsky-Matomäki-Radziwiłł-Rodgers reach q > x^{5/11+eps} but only for PRIME q and coprime residues, so it does not apply to f(k). Going below x^{2/3} would need a dual off-diagonal treatment of E_alpha and is not attempted. (2) The per-modulus range x^{2/3} is stronger than Nunes's x^{31/41} as reported by GMRR, using only elementary means. I rechecked P3 by hand, including limiting cases and the identity w1(2) = 1/4 + 2^{-5/2} from splitting odd and even residues, but a prover should treat it as the place to look for a mistake. (3) The problem's rho(m) is not well defined mod m when f has non-integer coefficients, so the plan uses densities delta_f, which equal rho(p^j)/p^j for f in Z[t]. f with repeated roots, e.g. (t+1)^2, are allowed, and P6/P7 are worded to cover them. (4) I could not list papers/ (no directory listing tool; guessed filenames failed), so I did not read the local PDFs. Vaughan's range comes from the GMRR description; the theorem of Vaughan was not read. The plan does not depend on either. (5) Nothing by the excluded authors was searched for, opened or used. A PDF of arXiv:1912.04683 was auto-saved outside the working directory; I did not read it, and only the arXiv abstract page was used.

Sources: O. Gorodetsky, K. Matomäki, M. Radziwiłł, B. Rodgers, On the variance of squarefree integers in short intervals and arithmetic progressions, Geom. Funct. Anal. 31 (2021) 111-149, https://arxiv.org/abs/2006.04060 ; R. M. Nunes, Square-free numbers in arithmetic progressions, 2014, https://arxiv.org/abs/1402.0684 ; R. M. Nunes, Moments of the distribution of k-free numbers in short intervals and arithmetic progressions, 2020, https://arxiv.org/abs/2010.03696 ; T. Parry, A variance for k-free numbers in arithmetic progressions of given modulus, https://arxiv.org/abs/1912.04683 (abstract only). All used for context only, not as proof inputs.

## Main theorem

Notation. B(t)=t(1-t). {·} is the fractional part. gamma(c)=prod_{p∤c}(1-2/p^2). For j>=1, delta_f(p^j) is the natural density of {k in N: p^j | f(k)} (equal to rho(p^j)/p^j when f in Z[t]). delta_1=delta_f(p), delta_2=delta_f(p^2). alpha_p=1-2/p^2+delta_2/p^2, beta_p=(delta_1-delta_2)/p, eta_p=1-delta_1. D_f(w)=prod_p(alpha_p+beta_p p^{-w}+eta_p p^{-2w})=sum_{e>=1} theta_f(e) e^{-w} for Re w>1/2. A_f(J)=sum_{e>=1} theta_f(e) B({J/e}). N_f(r)=r^{-3/2} int_0^r u A_f(1/u) du for 0<r<=1.

Theorem. Let f be as in problem.md, of degree d. For every eps>0 and all x>=2, y>=2 with x^{2/3} <= Y:=f(y) <= x,
V_f(x,y) = x^{1/2} Y^{3/2} N_f(Y/x) + O_{f,eps}( x^eps ( x^{7/6} Y^{1/2} + x^{4/5} Y + x^{1/2} Y^{3/2} y^{-1/2} ) ),
and N_f(r) = C_f + O_f(r^{1/6}) uniformly for 0<r<=1, where
C_f = (2/3)(zeta(3/2)/pi) prod_p [ (1-delta_1) w_0(p) + (delta_1-delta_2) w_1(p) + delta_2 w_2(p) ] > 0,
w_0(p)=1-3/p^2+2/p^3, w_1(p)=(1-1/p)(1-2/p^2+p^{-3/2}), w_2(p)=(1-1/p)(1-1/p^2).
Consequently
V_f(x,y) = C_f x^{1/2} Y^{3/2} + O_{f,eps}( x^{1/3} Y^{5/3} + x^eps( x^{7/6} Y^{1/2} + x^{4/5} Y + x^{1/2} Y^{3/2} y^{-1/2} ) ).
This is an asymptotic formula as soon as x^{2/3+c} <= Y = o(x) (for N_f form: x^{2/3+c} <= Y <= x), the error being a power saving in x and, in the C_f form, in x/Y. Moreover N_f(1) = 6/pi^2 - (3/2 - gamma_E) D_f(2) + D_f'(2). For Y comparable to x the correct main term is N_f(Y/x), not C_f; N_f has kinks at r=1/n. The weight f'(k) and the class of f are unchanged.

## Numerics check

Yes for k^2+1 and 2k+1; not yet confirmed for k^3+2. N_f(1): k^2+1 0.17108 vs 0.1712; 2k+1 0.18369 vs 0.1837; k^3+2 0.16614 vs 0.1680, which is still drifting down at x=1e7 with y<=215 (about 1% gap, right direction, unconfirmed). Constants as r->0: 0.1381, 0.1356, 0.1426 vs extrapolations of about 0.135-0.146 with uncertainty about 0.01, so consistent but a weak test. alpha+beta=2 matches the fixed-ratio fits. The fitted beta of about 1.54 is explained by N_f rising in r and the kinks at r=1/n are predicted. All predictions were computed by hand, not by machine.

## P1: Exact evaluation of the truncated variance

Depends on: none  
Cites: none

Notation: Q, g, E are as in problem.md. B(t)=t(1-t); {t} is the fractional part; gamma(c)=prod_{p∤c}(1-2/p^2); [m,n] is the lcm. For integers q>=1 and real J>0 put A_q(J)=sum_{c>=1} mu^2(c) gamma(c) (c^2,q)^{-1} B({J (c^2,q)/c^2}).

Let 1<=q<=x, J=x/q, 1<=z<=x^{1/2}. Put alpha(n)=sum_{a<=z, a^2|n} mu(a); g_alpha(q,l)=sum_{a<=z} mu(a) 1[(a^2,q)|l]/[a^2,q]; E_alpha(l)=sum_{n<=x, n≡l (q)} alpha(n) - x g_alpha(q,l).

Claims:
(a) g(q,l)=sum_{a>=1} mu(a) 1[(a^2,q)|l]/[a^2,q], absolutely convergent.
(b) For every eps>0, sum_{l mod q} E_alpha(l)^2 = q A_q(J) + O_eps( x^eps ( z^2 J + x/z ) ), the implied constant depending only on eps.
(c) For every eps>0, 0 <= A_q(J) <<_eps J^{1/2+eps} uniformly in q>=1 and J>=1.

Route. Write F_a(l)=#{n<=x: a^2|n, n≡l (q)} - x 1[(a^2,q)|l]/[a^2,q]. Let D=(a^2,b^2), D'=D/(D,q), q'=qD'. Counting n, n+hq gives N(a,b)=[a^2,b^2]^{-1} sum_{i in Z}(x-|i|q')_+ + O(1+J/D'). Use the identity sum_{i in Z}(x-|i|q')_+ = x^2/q' + q' B({x/q'}) and check x^2/(q'[a^2,b^2]) = x^2 sum_l d_a(l) d_b(l). The cross terms are x sum_{n<=x, a^2|n} d_b(n) = x^2 sum_l d_a d_b + O(x/[b^2,q]). Then set c=(a,b), a=c a_1, b=c b_1, sum over a_1,b_1 to obtain gamma(c) with tail <<c/z, and use (c^2,q)^{-1}B({J(c^2,q)/c^2}) <= J/c^2 for the tails. For (c) use B({t})<=min(1/4,t)<=t^{1/2+eps} and an Euler product bounded by zeta(1+2eps).

*Risk:* Bookkeeping only: c, a_1, b_1 must be pairwise coprime and squarefree so the sign is mu(a_1)mu(b_1); moduli with p^2|q must be followed through (c^2,q).

## P2: Two elementary counting lemmas modulo m

Depends on: none  
Cites: none

Let m>=1 be an integer and U,A>=1 real. All implied constants are absolute or depend only on eps.

For a unit t mod m let lambda(t)=min{max(|u|,|v|): (u,v) in Z^2 nonzero, v≡tu (mod m)}, and let h(t)=U/lambda(t) if lambda(t)<=U, h(t)=0 otherwise.

(a) For every unit t, #{(u,v) in Z^2 cap [1,U]^2: v≡tu (mod m)} << U^2/m + h(t).
(b) sum_{t in (Z/m)^*} h(t)^2 <<_eps (mU)^eps U^2.
(c) #{(a_1,b_1,a_2,b_2) in ([1,A] cap Z)^4, all coprime to m: (a_1 b_2)^2 ≡ (a_2 b_1)^2 (mod m)} <<_eps (mA)^eps (A^2 + A^4/m).

Route. (a) is the standard count of points of a planar lattice of determinant m in a box, <<1+U/lambda+U^2/m, where no nonzero point in the box means lambda>U. (b) A vector (u,v) with |u|,|v|<=2L, u≠0 and g=(u,m)=(v,m) fixes t modulo m/g, so at most g units t; hence #{t: lambda(t)<=2L} << sum_{g|m} g (L/g)^2 << m^eps L^2 for 2L<m, and for 2L>=m use the trivial bound #t<=m. Sum dyadically in L. (c) Put P=a_1b_2-a_2b_1, R=a_1b_2+a_2b_1>0, so m|PR. The case P=0 gives <<A^{2+eps}. If P≠0 take d_1=(P,m), d_2=m/d_1, so d_2|R; the number of pairs (P,R) is << tau(m) A^4/m, and the divisor bound recovers a_1,b_2,a_2,b_1.

*Risk:* Low. The case u=0 in (b), which forces |v|>=m, and small m need a line each.

## P3: Pairs of integers with large square divisors, for an individual modulus (CRUX)

Depends on: P2  
Cites: none

Let 1<=q<=x and A>=1. Let I_A=(A,2A]. Define beta_A(n)=sum_{a in I_A, a^2|n} mu(a), g_A(q,l)=sum_{a in I_A} mu(a) 1[(a^2,q)|l]/[a^2,q], and G_A(l)=sum_{n<=x, n≡l (q)} beta_A(n) - x g_A(q,l).

Claims, for every eps>0 with constants depending only on eps:
(a) If A<=x^{1/2}: N_A(q):=#{(a,b,u,v): a,b in I_A squarefree, u,v>=1, a^2u<=x, b^2v<=x, a^2u≡b^2v (mod q)} << x^eps ( x/A + x q^{-1/2} + x^2/(A^2 q) ).
(b) x^2 sum_{l mod q} g_A(q,l)^2 << x^{2+eps}/(A^2 q) for all A>=1 (with q^eps in place of x^eps).
(c) Hence sum_{l mod q} G_A(l)^2 << x^eps ( x/A + x q^{-1/2} + x^2/(A^2 q) ) for A<=x^{1/2}, and << x^{2+eps}/(A^2 q) for A>x^{1/2}, where the n-sum is empty.

Route for (a). Let r(l)=#{(a,u): a^2u≡l (q)} so N_A=sum_l r(l)^2. Group l by d=(l,q) and (a,u) by t=(a^2,d). Since a is squarefree, t=t_1 t_2^2 with t_1 t_2 | a and (t_1,t_2)=1. Put d'=d/t, so d'|u; write u=d'u', a=t_1 t_2 a', m=q/d. Then l/d ≡ t_1 a'^2 u' (mod m) with t_1, a', u' units mod m. Cauchy-Schwarz over the at most tau(d) values of t reduces to counting a'^2u_1≡b'^2u_2 (mod m), with a',b'<=A':=2A/(t_1t_2), u_i<=U':=x/(A^2 d'), all units. With T=a'^2 b'^{-2} mod m this is at most sum_T w(T) w'(T), where w(T)=#{(a',b')} and w'(T)=#{(u_1,u_2) in [1,U']^2: u_2≡T u_1}. Apply P2(a), then Cauchy-Schwarz with P2(b),(c), to get <<x^eps( A'^2U'^2/m + U'(A' + A'^2 m^{-1/2}) ). Substituting A', U', m gives the claim, using t^{1/2}<=(t_1t_2)^2 and t<=(t_1t_2)^2. Empty ranges (A'<1 or U'<1) contribute zero. (b) expands g_A^2, uses sum_l d_a d_b=(c^2,q)/(a^2 b^2 q) with c=(a,b), and sum_c (c^2,q)/c^2 << q^eps over squarefree c.

*Risk:* This is the heart of the range. It gives a per-modulus result beating Nunes's x^{31/41} (as reported by GMRR) by elementary means, so it deserves real scrutiny. The danger points are moduli with large square factors and non-coprime a,q, and the reduction by (d,t); the Cauchy-Schwarz must keep all pairs, not only those with equal t. Limiting checks passed: q=1 gives x^2/A^2; U'=1 gives count about A'; a=b=1 gives U^2/m+U.

## P4: Variance for an individual modulus

Depends on: P1, P3  
Cites: none

Let V(x;q)=sum_{l=1}^q E(x;q,l)^2 and let A_q(J) be as in P1. Put J=x/q. All constants depend only on eps>0.

(a) For 1<=q<=x and 1<=z<=x^{1/2}, with T=x^{1/2}q^{1/2} and R=x/z+x q^{-1/2}+x^2/(z^2 q):
V(x;q) = q A_q(J) + O( x^eps ( z^2 J + x/z + R + (RT)^{1/2} ) ).
(b) For x^{2/3}<=q<=x: V(x;q) = q A_q(x/q) + O( x^eps ( x^{7/6} q^{-1/2} + x^{4/5} ) ).
(c) For 1<=q<=x^{2/3}: V(x;q) << x^{3/2+eps}/q and q A_q(x/q) << x^{3/2+eps}/q.

Route. Write mu^2=alpha+beta with beta(n)=sum_{a>z, a^2|n} mu(a), and E=E_alpha+E_beta, where E_beta=sum_{i>=0} G_{2^i z}. The triangle inequality over dyadic A with P3 gives ||E_beta||^2 << x^eps R. Then V=||E_alpha||^2+O(||E_alpha|| ||E_beta||+||E_beta||^2) with ||E_alpha||^2 from P1(b) and q A_q(J) << x^eps T from P1(c).
For (b) take z=max(x^{1/12}q^{1/4}, q^{1/2}x^{-1/10}); note z>=x^{1/4} and z<=x^{1/2}.
For (c) take z=x^{1/4} and use T<=x^{3/2}/q in this range.

*Risk:* Low given P1 and P3; check that each term in (b) is covered at both ends of the range, and that the dyadic tail A>x^{1/2} sums geometrically.

## P5: The model sum Phi

Depends on: none  
Cites: none

Let B(t)=t(1-t) and for t>0 let Phi(t)=sum_{n>=1} B({t/n^2}). Let C_0=int_0^infty B({v^{-2}}) dv.

(a) C_0 = zeta(3/2)/pi = -4 zeta(-1/2).
(b) |Phi(t) - C_0 t^{1/2}| <= C t^{1/3} for all t>0, with an absolute constant C.

Route. For (a), set t=v^{-2} and use the Mellin identity int_0^infty B({t}) t^{-s-2} dt = 2 zeta(s)/(s(s+1)) for -1<Re s<0, which follows from sum_{j>=1}(t-j)_+ = (1/2 pi i) int zeta(s) t^{s+1}/(s(s+1)) ds with the residues at s=1 and s=0 removed. Evaluate at s=-1/2 and apply the functional equation. For (b) with t>=1: the terms n<=t^{1/3} are trivial; for n>t^{1/3}, G(u)=B({t/u^2}) is Lipschitz with |G'(u)|<=2t/u^3, so sum minus integral is at most the total variation, << t^{1/3}; the integral from t^{1/3} to infinity is C_0 t^{1/2}+O(t^{1/3}). For t<1, Phi(t)<<t and t^{1/2}<=t^{1/3}.

*Risk:* Low. Exponent 1/3 is not optimal but suffices; it is what produces the r^{1/6} in P8.

## P6: Local densities, the Dirichlet series and the averaged sum A_f

Depends on: P5  
Cites: none

Let f be as in problem.md. D>=1 is an integer with Df in Z[t]. For integers b>=1, delta_f(b) is the natural density of {k in N: b|f(k)}; it exists, is multiplicative in b (CRT on residues mod bD), and equals rho(b)/b when f in Z[t]. For squarefree c and g|c^2 let delta_f(c;g) be the density of {k: (c^2,f(k))=g}, and let gamma(c)=prod_{p∤c}(1-2/p^2), B(t)=t(1-t). Define theta_f(e)=sum_{c squarefree, g|c^2, c^2/g=e} gamma(c) g^{-1} delta_f(c;g), and A_f(J)=sum_{e>=1} theta_f(e) B({J/e}).

Claims, with constants depending only on f:
(a) (Progressions) For cubefree b the set {k>=1: b|f(k)} is a union of at most C_f^{omega(b)} arithmetic progressions, of moduli dividing bD. This must hold also if f has repeated roots, e.g. f=(t+1)^2: then p^2|f(k) is one class mod p, and for all but finitely many p, {t in Z_p: v_p(f(t))>=j} (j<=2) is a union of at most d balls. Also delta_f(p)<=d/p and delta_f(p^2)<=delta_f(p) for all p>p_0(f).
(b) D_f(w):=sum_e theta_f(e) e^{-w} = prod_p(alpha_p+beta_p p^{-w}+eta_p p^{-2w}) for Re w>1/2, with alpha_p=1-2/p^2+delta_f(p^2)/p^2, beta_p=(delta_f(p)-delta_f(p^2))/p, eta_p=1-delta_f(p), and theta_f(e)>=0.
(c) D_f(w)=zeta(2w) G_f(w), with G_f(w)=sum_m g_f(m) m^{-w} and sum_m |g_f(m)| m^{-1/3} < infinity.
(d) A_f(J)=sum_m g_f(m) Phi(J/m), with Phi as in P5, hence A_f(J)=c_f J^{1/2}+O_f(J^{1/3}) for all J>0, where c_f=(zeta(3/2)/pi) G_f(1/2).
(e) G_f(1/2)=prod_p[(1-delta_1)w_0(p)+(delta_1-delta_2)w_1(p)+delta_2 w_2(p)] > 0, with delta_j=delta_f(p^j), w_0(p)=1-3/p^2+2/p^3, w_1(p)=(1-1/p)(1-2/p^2+p^{-3/2}), w_2(p)=(1-1/p)(1-1/p^2).

Route. For (c), the local factor is (1-u)(alpha_p+beta_p p^{-w}+eta_p u), u=p^{-2w}; at Re w=1/3 the sum of absolute coefficients is 1+O(p^{-4/3}) for large p, using delta_f(p)<=d/p. For (e), expand and use w_i=(1-1/p)×(...), and note all three w_i>0.

*Risk:* Fixed divisors of f (delta_f(p)=1 for finitely many p) and non-integer coefficients; rho(m) in problem.md is not well defined for those, hence delta_f. Repeated roots break the naive bound rho(p^2)<<1, so (a) must be stated in terms of progressions rather than rho.

## P7: Averaging the explicit main term over k (CRUX)

Depends on: P6  
Cites: none

Let f be as in problem.md, A_q(J) as in P1 and A_f(J) as in P6. Let x>=2, y>=2 with x^{2/3}<=Y:=f(y)<=x. Then for every eps>0,
sum_{k<=y} f'(k) f(k) A_{f(k)}(x/f(k)) = x^2 int_0^{Y/x} u A_f(1/u) du + O_{f,eps}( x^{1/2+eps} Y^{3/2} y^{-1/2} ).

Route. Expand A_q by c and g=(c^2,f(k)). Truncate c<=C:=(xy/Y)^{1/2}; the tail on both sides is << xY/C using (c^2,q)^{-1}B({J(c^2,q)/c^2})<=J/c^2. For c<=C_0:=max(1,(x/(yY))^{1/2}), if C_0>1, bound both sides trivially by <<C_0 Y^2 (here y is too sparse for equidistribution of x/f(k) to be used, and none is needed). For C_0<c<=C, use Moebius over b with g|b|c^2 and P6(a) to split {k: (c^2,f(k))=g} into << x^eps arithmetic progressions. On each, compare sum and integral by total variation: G(s)=f'(s)f(s)B({E/f(s)}) with E=xg/c^2 has TV << f'(y)(Y+E) log y, since the integral of f'(s)^2/f(s) is << f'(y) log y. With the weight 1/g this gives << x^eps f'(y)(Y+x/c^2) per c, and f'(y)<<Y/y. Change variables t=f(s), u=t/x; replacing the lower limit f(1) by 0 costs <<x, which is within the error since Y>=x^{2/3}. Each of the three error sources equals x^{1/2}Y^{3/2}y^{-1/2} up to x^eps.

*Risk:* For high degree d near Y=x^{2/3} one has yY<x, so B({x/(f(k)e)}) is not smooth at the spacing of k for small e; a naive Riemann sum fails. The cut at C_0 handles this and must not be dropped. Check f'(s) monotonic only for large s; small s contribute to constants. The numerics for k^3+2 (y<=215) suggest this error term is visible in practice.

## P8: Properties of the profile N_f

Depends on: P5, P6  
Cites: none

Let A_f, D_f, c_f be as in P6 and N_f(r)=r^{-3/2} int_0^r u A_f(1/u) du for 0<r<=1.

(a) The integral converges and N_f(r)=sum_{e>=1} theta_f(e) r^{-3/2} e^{-2} I(re), where I(T)=int_0^T v B({1/v}) dv.
(b) N_f(r)=C_f+O_f(r^{1/6}) uniformly on 0<r<=1, with C_f=(2/3)c_f>0, which is the constant in the main theorem.
(c) int_1^infty B({t}) t^{-3} dt = gamma_E-1/2, I(T)=gamma_E-3/2+T-log T for T>=1, D_f(1)=6/pi^2 for every f (because alpha_p+beta_p/p+eta_p/p^2=1-1/p^2), and N_f(1)=6/pi^2-(3/2-gamma_E) D_f(2)+D_f'(2).

Route. (b) is immediate from P6(d) applied in the integral: int_0^r u(c_f u^{-1/2}+O(u^{-1/3}))du. (c) uses the Mellin formula from P5, continued to s=1 after removing the contribution of t in (0,1).

*Risk:* Low. Part (c) is only used for the numerical comparison.

## P9: Assembly: the main theorem

Depends on: P4, P7, P8  
Cites: none

Let f be as in problem.md, x>=2, y>=2, x^{2/3}<=Y:=f(y)<=x. Note V_f(x,y)=sum_{k<=y} f'(k) V(x;f(k)), with V as in P4. Then for every eps>0,
(a) V_f(x,y)=sum_{k<=y} f'(k) f(k) A_{f(k)}(x/f(k)) + O_{f,eps}( x^eps ( x^{7/6} Y^{1/2} + x^{4/5} Y ) );
(b) V_f(x,y)=x^{1/2} Y^{3/2} N_f(Y/x) + O_{f,eps}( x^eps ( x^{7/6} Y^{1/2} + x^{4/5} Y + x^{1/2} Y^{3/2} y^{-1/2} ) );
(c) V_f(x,y)=C_f x^{1/2} Y^{3/2} + O_{f,eps}( x^{1/3} Y^{5/3} + x^eps ( x^{7/6} Y^{1/2} + x^{4/5} Y + x^{1/2} Y^{3/2} y^{-1/2} ) ).

Route. Split k by f(k)>=x^{2/3} (use P4(b)) or f(k)<x^{2/3} (use P4(c)). sum_k f'(k) f(k)^{-1/2} << Y^{1/2}, sum_k f'(k) << Y, and sum_k f'(k)/f(k) << log x, the last giving << x^{3/2+eps} <= x^{7/6+eps} Y^{1/2}. Then (b) follows from P7 with the definition of N_f, and (c) from P8(b), since x^{1/2}Y^{3/2}(Y/x)^{1/6}=x^{1/3}Y^{5/3}.

*Risk:* Low. f(k)>=2 and f'>=1 ensure every modulus is admissible and f(k)<=Y<=x for k<=y.
