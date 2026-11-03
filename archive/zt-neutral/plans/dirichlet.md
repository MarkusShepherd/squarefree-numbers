# Plan: dirichlet

Model: claude-opus-5-5

APPROACH (follows the hint, no circle method). (1) Exact reduction, one modulus at a time: V(x;q) := Σ_l E(x;q,l)^2 = Q(x) + 2N(x;q) − x^2 G(q) − 2x R(x;q). Here N is the off-diagonal count #{m<n≤x squarefree, q | n−m}, G(q) = Σ_l g(q,l)^2, and R is a small gcd-error term (P2). (2) Write n − m = hq, so N(x;q) = Σ_{h<x/q} T(x,hq) with T(x,r) = Σ_m μ²(m)μ²(m+r). Replace T by A(r)(x−r) + O(x^{2/3+ε}) uniformly in r (P3, Mirsky-type, elementary). (3) The resulting singular-series sum q·Σ_q(H), Σ_q(H) = Σ_{h≤H} A(hq)(H−h) with H = x/q, has Dirichlet series Σ_h A(hq)h^{-s} = c2 ζ(s) ζ(2s+2) P_q(s), where P_q is holomorphic for Re s > −3/4. Poles: s = 1 gives x^2 G(q)/2, which cancels exactly (identity qG(q) = c2 F_q(1)). s = 0 gives −3x/π², which cancels the diagonal Q(x). The pole of ζ(2s+2) at s = −1/2 gives the main term (κ(q)/2) x^{1/2} q^{1/2}. A technical obstruction: for the Cesàro-1 weight (H−h), the Perron integral diverges to the left of Re s = −1/2, because |ζ(s)| grows like |t|^{1/2−σ}. So the contour shift is done for the Cesàro-2 sum, where it converges (P4); this identifies the constant. The Cesàro-1 asymptotic, with error H^{1/4+ε}, is then obtained from an exact formula, Σ_q(H) = smooth part + (c2/2) Σ_d a(d) L_d β(H/L_d) with β(Y) = {Y}(1−{Y}), using truncated Poisson summation / van der Corput (P5, the crux). Integrating the result and comparing with P4 pins down the H^{1/2} coefficient. (4) The per-modulus result is V(x;q) = κ(q) x^{1/2} q^{1/2} + O(x^{5/3+ε}/q + x^{1/4+ε} q^{3/4+ε} + x^{1/2}) (P6). Averaging κ(f(k)) over k uses the densities ρ(p)/p and ρ(p²)/p² (P7), giving C_f.

CONSTANT CHECKS. (i) With ρ ≡ 1 (all moduli), the formula for C_f reproduces Vaughan's (2005) constant c_2 = 8C_1(−ζ(−1/2))/(3ζ(2)^2) = 0.1284787 to 7 digits. (ii) An independent computation at x = 4·10^7 for 8 single moduli gives V(x;q)/(xq)^{1/2} within about 10% of κ(q), and it tracks the arithmetic dependence: prime q gives 0.238; q = 10^5 gives 0.153 vs observed 0.155; q = 360360 gives 0.106 vs observed 0.094. (iii) A direct computation of Σ_q(H) for q = 1, 6, 7, 12 and H ≤ 10^5 matches the predicted three-term expansion, with residual about 0.01–0.02·H^{1/4}.

NUMERICS. The predicted constants are C_{k²+1} = 0.13808, C_{k³+2} = 0.13561 and C_{2k+1} = 0.14261. The results.json extrapolations (r = f(y)/x → 0) are 0.1345±0.0073, 0.1363±0.0024 and 0.1417±0.0082. All three agree, and no discrepancy was found. The fixed-ratio slopes α+β ≈ 2.000 confirm the exponent pair (1/2, 3/2). The fixed-x exponent β ≈ 1.54 and the joint-fit C ≈ 0.17–0.20 are artifacts of a secondary term: (normalised − C_f)/√r ≈ 0.03–0.04 is nearly constant in r, i.e. V_f contains roughly +0.035·f(y)^2. That term sits inside the theorem's error x^{1/4} f(y)^{7/4}; Vaughan's full-moduli theorem also only bounds such a term. Caveat: all data have f(y)/x ≥ 0.005, which is outside the proven asymptotic range for fixed x, so the comparison rests on the r → 0 extrapolation, and the extrapolations agree.

RANGE. The proven range is x^{7/9+δ} ≤ f(y) ≤ x^{1−δ}. The only bottleneck is the trivial summation of the uniform x^{2/3+ε} error of P3 over ≈ x log x shifts, which costs x^{5/3+ε}. Any averaged bound Σ_k f'(k) Σ_h |T(x,hf(k)) − A(hf(k))(x−hf(k))| ≪ x^{3/2+ε} would extend the range to x^{2/3+δ}. That is the natural barrier, because the R-term in P2 is genuinely of size x^{3/2}/q, as in Vaughan 2005's x^{1+1/k} error. The upper limit x^{1−δ} only reflects ε-losses; the main term already dominates once x/f(y) → ∞ by a power.

COMPLIANCE. No web searches were made and nothing by the excluded author or the excluded paper was opened or used. Sources used: Vaughan 2005, Brüdern–Wooley 2011 (structure of the Dirichlet-series/Perron step, §5), Montgomery–Vaughan 2007 (Ch. 1, 10), Vaughan 1997 (Lemma 4.2). P3 is classical (L. Mirsky, Quart. J. Math. 18 (1947) / Proc. London Math. Soc. (2) 50 (1949)); it should be proved from scratch, and the citation details are from memory and unverified.

## Main theorem

Let f ∈ Z[t] have degree d ≥ 1, with f(t) ≥ 2 and f'(t) ≥ 1 for all t ≥ 1, and let ρ(m) = #{a mod m : f(a) ≡ 0 mod m}. For each prime p put λ̄_p := 1 − ρ(p)/p + p^{-1/2}(ρ(p)/p − ρ(p²)/p²) + p^{-1}·ρ(p²)/p², and define
C_f := (2ζ(3/2)/(3π)) · ∏_p (1 − 1/p)(1 − 2/p² + λ̄_p/p).
The product converges absolutely and C_f > 0. Then for every ε > 0 there is a constant C(f,ε) such that, for all real x ≥ 2 and y ≥ 1 with f(y) ≤ x,
| V_f(x,y) − C_f x^{1/2} f(y)^{3/2} | ≤ C(f,ε) · ( x^{5/3+ε} + x^{1/4+ε} f(y)^{7/4} + x^{1/2} f(y)^{3/2} y^{-1/3} ).
In particular, for each fixed δ ∈ (0, 1/9), V_f(x,y) = C_f x^{1/2} f(y)^{3/2} (1 + O_{f,δ}(x^{-δ/8})) uniformly for x^{7/9+δ} ≤ f(y) ≤ x^{1−δ}.
Equivalently, C_f = (2/3)·lim_{Y→∞} Y^{-1} Σ_{k≤Y} κ(f(k)), where κ(q) := (ζ(3/2)/π) ∏_p (1−1/p)(1 − 2/p² + λ_p(q)/p) and λ_p(q) = 1, p^{-1/2} or p^{-1} according as p ∤ q, p ‖ q or p² | q. Here ζ(3/2)/π = −4ζ(−1/2). With ρ ≡ 1, the formula for C_f gives Vaughan's constant c_2 = 0.128479 for the full variance.

## Numerics check

Yes. Exponents: the fixed-ratio log-log slopes in results.json give α+β = 2.0008±0.0006 (k²+1), and similarly ≈ 2.00 for the other two polynomials, matching x^{1/2} f(y)^{3/2}. Constants, comparing results.json's r = f(y)/x → 0 extrapolation with the prediction: k²+1: 0.1345±0.0073 vs 0.1381; k³+2: 0.1363±0.0024 vs 0.1356; 2k+1: 0.1417±0.0082 vs 0.1426. All are within the stated uncertainty. At the largest x (2.56·10^8), (normalised − C_f)/√r ≈ 0.028–0.041 (k²+1), 0.031–0.044 (k³+2) and 0.020–0.048 (2k+1), roughly constant in r. This points to a secondary term ≈ 0.035·f(y)^2, which is O(x^{1/4} f(y)^{7/4}) and explains both the fixed-x exponent β ≈ 1.54 and the inflated joint-fit C ≈ 0.17–0.20. The prediction is not adjusted to the data. Caveat: every data row has f(y)/x ≥ 0.005, outside the proven asymptotic range at these x, so the agreement rests on the extrapolation r → 0. Independent cross-checks: the ρ ≡ 1 formula equals Vaughan's c_2 to 7 digits, and a direct computation of single-modulus variances at x = 4·10^7 tracks κ(q) to within about 10%.

## P1: Local densities, pair singular series, and basic identities

Depends on: none  
Cites: Vaughan 2005, (1.2) and (1.4), Vaughan 2005, Lemma 2.4

Notation: p always denotes a prime; (a,b) is the gcd and [a,b] the lcm; 1[·] is an indicator. Put c2 := ∏_p (1 − 2p^{-2}). For q ∈ N put G(q) := Σ_{l=1}^{q} g(q,l)^2 and F_q(1) := ∏_p (1 + (p²,q)·p^{-2}(p²−2)^{-1}). For d ∈ N put a(d) := μ²(d) ∏_{p|d} (p²−2)^{-1}. For r ∈ N put A(r) := ∏_p (1 − (2 − 1[p² | r])·p^{-2}). Let Q(x) := #{1 ≤ n ≤ x : n squarefree}. g(q,l) is as in problem.md. Claims:
(a) For all q ∈ N and l ∈ Z, g(q,l) = q^{-1} ∏_p (1 − (p²,q) p^{-2} · 1[(p²,q) | l]). Consequently g(q,l) depends only on (l,q), and 0 ≤ g(q,l) ≤ 1/q.
(b) For all q ∈ N, q·G(q) = c2·F_q(1). Moreover c2·Σ_{d≥1} a(d) = 6/π², and 0 < c2 F_q(1) ≤ 6/π².
(c) For all r ∈ N, A(r) = c2 Σ_{d≥1, d²|r} a(d) = Σ_{a,b≥1, (a²,b²)|r} μ(a)μ(b)/[a²,b²], where the last double series converges absolutely.
(d) For all real x ≥ 1, |Q(x) − 6x/π²| ≤ 3√x.
All statements are exact or carry absolute constants.

*Risk:* Low. These are Euler-product bookkeeping. (b) was checked numerically for q ∈ {1,2,4,6,12,18,25,30}. In (a), note that the factor is 0 when p² | q and p² | l (no squarefree n ≡ l mod q).

## P2: Exact reduction to the off-diagonal count; gcd-error term

Depends on: P1  
Cites: Vaughan 2005, Lemma 2.2, Vaughan 2005, Lemma 2.3, Vaughan 2005, Lemma 2.4

Notation: for q ∈ N and real x ≥ 1 let V(x;q) := Σ_{l=1}^{q} E(x;q,l)^2; let N(x;q) := #{(m,n) ∈ N² : m < n ≤ x, μ²(m) = μ²(n) = 1, q | n−m}; let G(q) := Σ_{l=1}^q g(q,l)^2; let R(x;q) := Σ_{n≤x} μ²(n) g(q,n) − x·G(q); let Q(x) := #{n ≤ x : n squarefree}; τ is the divisor function. E and g are as in problem.md. Claims:
(a) For all q ∈ N and x ≥ 1: V(x;q) = Q(x) + 2N(x;q) − x²G(q) − 2x·R(x;q).
(b) There is an absolute constant C such that for all real x ≥ 1 and integers 1 ≤ q ≤ x: |R(x;q)| ≤ C·τ(q)^3·x^{1/2}·q^{-1}.

*Risk:* Low. (a) comes from expanding the square, using Σ_l Q(x;q,l)² = Q(x) + 2N(x;q) and Σ_l g(q,l)Q(x;q,l) = Σ_{n≤x} μ²(n)g(q,n). For (b), write R = Σ_{r|q} g(q,r)(S_r(x) − x φ(q/r) g(q,r)) with S_r(x) = #{n ≤ x squarefree : (n,q) = r}. Expand S_r by Möbius over t | q/r. Vaughan 2005 Lemma 2.2(ii) (k=2) gives Σ_{n≤x, D|n} μ²(n) = g(D,D)x + O(τ(D)(x/D)^{1/2}) for D ≤ x; for D > x the sum is 0 and g(D,D)x < 1. Lemma 2.3 identifies the main terms. Vaughan states his lemmas for x large; small x is trivial.

## P3: Uniform asymptotic for shifted squarefree correlations

Depends on: P1  
Cites: none

Let T(x,r) := Σ_{1 ≤ m ≤ x−r} μ²(m) μ²(m+r) and A(r) := ∏_p (1 − (2 − 1[p²|r]) p^{-2}). For every ε > 0 there is a constant C(ε), depending only on ε, such that for all real x ≥ 2 and all integers r with 1 ≤ r < x: |T(x,r) − A(r)(x − r)| ≤ C(ε)·x^{2/3+ε}.

*Risk:* Low. Classical (Mirsky 1947/49); prove directly. Write μ²(n) = Σ_{a²|n} μ(a) on both factors and use z = x^{1/3}. Pairs a,b ≤ z: the count of m ≤ X with a²|m and b²|m+r is X·1[(a²,b²)|r]/[a²,b²] + O(1), which gives O(z²) error. Completing the main term costs X·Σ_{max(a,b)>z} 1/[a²,b²] ≪ X z^{-1} log z. Terms with a > z: at most Σ_{a>z} X/a² ≪ X/z. Terms with a ≤ z, b > z: bounded by x^ε·X/z, using |Σ_{a²|m, a≤z} μ(a)| ≤ τ(m). The only real requirement is that the constant be independent of r.

## P4: Dirichlet series in h and the Cesàro-2 singular-series sum (contour shift) (CRUX)

Depends on: P1  
Cites: Montgomery–Vaughan 2007, Corollary 10.4, Montgomery–Vaughan 2007, Corollary 10.5, Montgomery–Vaughan 2007, Corollary 1.17, Brüdern–Wooley 2011, §5 (37)–(38)

Notation: c2, a(d), A(r), G(q) as in P1 (c2 = ∏_p(1−2p^{-2}), a(d) = μ²(d)∏_{p|d}(p²−2)^{-1}, A(r) = ∏_p(1 − (2 − 1[p²|r])p^{-2}), G(q) = Σ_{l≤q} g(q,l)²). For q ∈ N let L_d(q) := d²/(d²,q), F_q(s) := Σ_{d≥1} a(d) L_d(q)^{-s}, P_q(s) := ∏_p (1 − p^{-2s−2})(1 + (p²,q)^s p^{-2s}(p²−2)^{-1}), λ_p(q) := 1 if p∤q, p^{-1/2} if p‖q, p^{-1} if p²|q, and κ(q) := (ζ(3/2)/π)·∏_p (1 − p^{-1})(1 − 2p^{-2} + λ_p(q) p^{-1}). For real H ≥ 1 let Θ_q(H) := Σ_{1≤h≤H} A(hq)(H − h)². Claims:
(a) For Re s > 1, Σ_{h≥1} A(hq) h^{-s} = c2 ζ(s) F_q(s). F_q(s) converges absolutely for Re s > −1/2, and F_q(s) = ζ(2s+2) P_q(s) there. P_q extends holomorphically to Re s > −3/4, and for every ε ∈ (0,1/8) there is C(ε) with |P_q(s)| ≤ C(ε) q^ε for all q ∈ N and −3/4+ε ≤ Re s ≤ 3.
(b) c2 F_q(1) = q G(q), c2 F_q(0) = 6/π², and κ(q) = −4 ζ(−1/2) c2 P_q(−1/2), using ζ(−1/2) = −ζ(3/2)/(4π). Also 0 < κ(q) ≤ ζ(3/2)/π.
(c) For every ε ∈ (0,1/8) there is C(ε) such that for all q ∈ N and real H ≥ 1: |Θ_q(H) − (qG(q)/3)H³ + (3/π²)H² − (2/3)κ(q)H^{3/2}| ≤ C(ε) q^ε H^{5/4+ε}.

*Risk:* Medium. Use Θ_q(H) = (1/πi)∫_{(2)} c2 ζ(s)F_q(s) H^{s+2} ds/(s(s+1)(s+2)) and shift to Re s = −3/4+ε. On that line |ζ(s)| ≪ τ^{5/4} (MV Cor. 10.5) and |ζ(2s+2)| ≪ τ^{1/2} (MV Cor. 1.17), so the integrand is ≪ q^ε τ^{-5/4}: integrable. The only poles crossed are s = 1, 0, −1/2. Residues: s=1 gives qG H³/3; s=0 gives ζ(0)c2F_q(0)H² = −(3/π²)H²; s=−1/2 gives (2/3)κ(q)H^{3/2}, since F_q ~ P_q(−1/2)/(2(s+1/2)). Pitfalls: the Euler factors at p | q must be bounded uniformly (∏_{p|q}(1+p^{-1/2}) ≪ q^ε). P_q may have singularities (zeros of ζ(4s+4)) for Re s ≤ −3/4, so do not go further left. Do NOT try the same shift for the Cesàro-1 weight: that integral diverges left of Re s = −1/2, which is why P5 exists.

## P5: Cesàro-1 singular-series sum with the H^{1/2} term (CRUX)

Depends on: P1, P4  
Cites: Vaughan 1997 (The Hardy–Littlewood Method), Lemma 4.2

Notation: A(r), c2, a(d), G(q) as in P1; L_d(q) := d²/(d²,q); κ(q) := (ζ(3/2)/π)·∏_p (1 − p^{-1})(1 − 2p^{-2} + λ_p(q)p^{-1}), with λ_p(q) = 1, p^{-1/2}, p^{-1} according as p∤q, p‖q, p²|q. For q ∈ N and real H ≥ 1 let Σ_q(H) := Σ_{1≤h≤H} A(hq)(H − h). Claim: for every ε ∈ (0,1/8) there is a constant C(ε), depending only on ε, such that for all q ∈ N and all real H ≥ 1:
| Σ_q(H) − (q G(q)/2) H² + (3/π²) H − (κ(q)/2) H^{1/2} | ≤ C(ε) q^ε H^{1/4+ε}.

*Risk:* This is the main difficulty. Suggested route: (i) exact formula Σ_q(H) = c2 Σ_d a(d) L_d Φ(H/L_d) with Φ(Y) = Σ_{1≤j≤Y}(Y−j) = (Y² − Y + β(Y))/2 and β(Y) = {Y}(1−{Y}); this holds for all Y ≥ 0, since Φ = 0 = (Y² − Y + Y(1−Y))/2 when Y < 1. Hence Σ_q(H) = (qG/2)H² − (3/π²)H + (c2/2)·B_q(H), with B_q(H) := Σ_d a(d) L_d β(H/L_d). (ii) Show B_q(H) = K(q)H^{1/2} + O(q^ε H^{1/4+ε}). Write d = e·d' with e | rad(q) and (d',q) = 1, and remove squarefreeness and coprimality by Möbius inversion. Expand β = 1/6 − π^{-2}Σ_{j≥1} j^{-2} cos(2πjY); the Fourier series converges absolutely. Estimate Σ_{d'} e(jY/d'^2) using Lemma 4.2 (truncated Poisson) plus first/second-derivative bounds for the integrals. The range L_d > H, where β(Y) = Y(1−Y), must be treated too. (iii) Identify K(q) = κ(q)/c2 by integrating: Θ_q(H) = 2∫_0^H Σ_q(u) du, then compare the H^{3/2} coefficient with P4(c); the P4 error H^{5/4+ε} is o(H^{3/2}). Risks: uniformity in q of the Möbius/coprimality decomposition, and possibly an extra log. If only an exponent θ ∈ (1/4, 1/2) is obtained in place of 1/4, the main theorem still holds with x^{1/4+ε}f(y)^{7/4} replaced by x^{θ+ε}f(y)^{2−θ}. Numerically, for q ∈ {1,6,7,12} and H ≤ 10^5, the remainder is ≈ 0.01–0.02·H^{1/4}.

## P6: Asymptotic for the variance to a single modulus

Depends on: P1, P2, P3, P5  
Cites: none

Notation: V(x;q) := Σ_{l=1}^{q} E(x;q,l)², with E as in problem.md. κ(q) := (ζ(3/2)/π)·∏_p (1 − p^{-1})(1 − 2p^{-2} + λ_p(q)p^{-1}), with λ_p(q) = 1, p^{-1/2}, p^{-1} according as p∤q, p‖q, p²|q. Claim: for every ε ∈ (0,1/8) there is a constant C(ε), depending only on ε, such that for all real x ≥ 2 and all integers 1 ≤ q ≤ x:
| V(x;q) − κ(q) x^{1/2} q^{1/2} | ≤ C(ε)·( x^{5/3+ε} q^{-1} + x^{1/4+ε} q^{3/4+ε} + x^{1/2} ).

*Risk:* Low (assembly). By P2(a), V = Q(x) + 2N − x²G − 2xR. Then N(x;q) = Σ_{1≤h<x/q} T(x,hq) = qΣ_q(x/q) + Σ_{h<x/q}(T(x,hq) − A(hq)(x−hq)); the term h = x/q contributes 0 to Σ_q. P5 gives 2qΣ_q(x/q) = x²G − (6/π²)x + κ x^{1/2}q^{1/2} + O(q^{3/4+ε}x^{1/4+ε}). P3 gives the error 2(x/q)·C x^{2/3+ε}. P1(d) handles Q(x) − 6x/π². P2(b) gives 2x|R| ≪ τ(q)³x^{3/2}/q ≪ x^{5/3}/q. Watch the h-range conventions.

## P7: Mean of κ over polynomial values

Depends on: none  
Cites: Brüdern–Wooley 2011, Lemma 2

Let f, ρ be as in problem.md (f ∈ Z[t], degree d ≥ 1, f(t) ≥ 2 and f'(t) ≥ 1 for t ≥ 1). For q ∈ N let κ(q) := (ζ(3/2)/π)·∏_p (1 − p^{-1})(1 − 2p^{-2} + λ_p(q)p^{-1}), with λ_p(q) = 1, p^{-1/2}, p^{-1} according as p∤q, p‖q, p²|q. For primes p let λ̄_p := 1 − ρ(p)/p + p^{-1/2}(ρ(p)/p − ρ(p²)/p²) + p^{-1}ρ(p²)/p², and C_f := (2ζ(3/2)/(3π))·∏_p (1 − p^{-1})(1 − 2p^{-2} + λ̄_p p^{-1}). Claims: (a) the product defining C_f converges absolutely and C_f > 0; (b) there is a constant C(f), depending only on f, such that for all real y ≥ 1:
| Σ_{1≤k≤y} f'(k) f(k)^{1/2} κ(f(k)) − C_f f(y)^{3/2} | ≤ C(f) f(y)^{3/2} y^{-1/3}.

*Risk:* Low to medium. Write κ(q) = K0 Σ_{d|q} θ(d), where K0 = κ(1) and θ is multiplicative, supported on d whose prime exponents are ≤ 2, with θ(p) = r1(p) − 1, θ(p²) = r2(p) − r1(p), r1 = (1−2/p²+p^{-3/2})/(1−2/p²+1/p), r2 = (1−2/p²+p^{-2})/(1−2/p²+1/p). Then |θ(p)| ≤ 1/p and |θ(p²)| ≤ 2p^{-3/2}. Count k ≤ y with d | f(k) in residue classes (error O(ρ(d)·f(y)^{3/2}/y) by Euler summation), truncate at D = y^{4/3}, and bound the k-tail by τ(f(k))2^{ω(f(k))}D^{-3/4}. Pitfall: if f has repeated irreducible factors, ρ(p²) can be as large as p·ρ(p) for infinitely many p. Only ρ(p²) ≤ pρ(p), and ρ(p) ≤ d for p not dividing the content, may be assumed. This is why the error is stated as y^{-1/3} rather than y^{-1}. Lower limit: ∫_1^y f'(t)f(t)^{1/2}dt = (2/3)(f(y)^{3/2} − f(1)^{3/2}), and f(y) ≥ y+1.

## P8: Main theorem: assembly over k

Depends on: P6, P7  
Cites: none

Let f, ρ, V_f be as in problem.md and C_f as defined in P7. For every ε > 0 there is a constant C(f,ε) such that for all real x ≥ 2 and y ≥ 1 with f(y) ≤ x:
| V_f(x,y) − C_f x^{1/2} f(y)^{3/2} | ≤ C(f,ε)·( x^{5/3+ε} + x^{1/4+ε} f(y)^{7/4} + x^{1/2} f(y)^{3/2} y^{-1/3} ).
Hence, for each fixed δ ∈ (0,1/9), V_f(x,y) = C_f x^{1/2} f(y)^{3/2}(1 + O_{f,δ}(x^{-δ/8})) uniformly for x^{7/9+δ} ≤ f(y) ≤ x^{1−δ}.

*Risk:* Low. V_f = Σ_{k≤y} f'(k) V(x; f(k)), and P6 applies because 2 ≤ f(k) ≤ f(y) ≤ x (f is increasing on [1,∞)). Sum the P6 errors: Σ_k f'(k)/f(k) ≪_f log(2y) ≤ log x, absorbed into x^ε; Σ_k f'(k) f(k)^{3/4+ε} ≤ C(f) f(y)^{7/4+ε} ≤ C(f) x^ε f(y)^{7/4}; Σ_k f'(k) x^{1/2} ≤ x^{1/2} f(y) ≤ x^{1/2} f(y)^{3/2} y^{-1/3}, using f(y) ≥ y+1. The main term comes from P7 multiplied by x^{1/2}. For the 'hence' part, take ε = δ/8 and use y ≥ (f(y)/C(f))^{1/d}.
