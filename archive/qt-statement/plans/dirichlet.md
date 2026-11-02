# Plan: dirichlet

Model: claude-opus-5-5

PLAN. (1) Reduce each modulus to an exact "model" V*(x;q). (2) Evaluate V*(x;q) asymptotically with a van der Corput argument. (3) Average over q = f(k) using multiplicativity. Every step is elementary. The circle method is not used: a trivial bound for T_f combined with BGPVW Theorem 2 would only give an x^{9/5} error, which is worse.

STEP 1: PER-MODULUS REDUCTION (P1–P5). Open the square. The off-diagonal part is 2 Σ_h C(x,hq), where C(x,r) counts n ≤ x−r with n and n+r both squarefree. A Mirsky-type uniform bound C(x,r) = (x−r)B(r) + O(x^{2/3+ε}) (P2) replaces this by Σ_h (x−hq)B(hq). That sum is evaluated exactly (P3) by writing B(r) = Σ_{d²|r} β(d) and summing over h in closed form. The result is x²Σ_l g(q,l)² − 6x/π² + V*(x;q), where V*(x;q) = Σ_d β(d) N_d ψ2(x/N_d), with ψ2(t) = {t}(1−{t}) and N_d = q d²/(d²,q).

This matches the hint's Dirichlet series: Σ_h B(hq) h^{-s} = ζ(s) Σ_d β(d) (d²/(d²,q))^{-s} has poles at s = 1, 0 and −1/2. These give, in order, the x²Σg² term, the −6x/π² term (which cancels the diagonal) and the main term x^{1/2}q^{1/2}. However, a literal contour shift cannot control the error: ζ(s) grows on Re s < −1/2 and the kernel 1/(s(s+1)) does not compensate. I therefore keep the exact floor-sum identity and estimate V* directly. The cross term and the diagonal are handled elementarily (P4). Summing over k gives an error x^{5/3+ε} (P5, P9).

STEP 2: THE CRUX (P6, P7). The core sum is S(Z) = Σ_t ψ2(Z/t²) = (ζ(3/2)/π)Z^{1/2} + O(Z^{1/4}). It is handled in three ranges:
- t ≤ Z^{1/4}: trivial bound.
- Z^{1/4} < t ≤ Z^{3/8}: Fourier-expand ψ2 and apply the van der Corput second-derivative test.
- t > Z^{3/8}: total-variation comparison with the integral.

The constant uses ∫_0^∞ψ2(v)v^{-3/2}dv = 2ζ(3/2)/π, which I checked numerically to 9 digits. P7 reduces V*(x;q) to such core sums by multiplicative bookkeeping. This gives 𝒜(q) x^{1/2}q^{1/2} + O(x^{1/4+ε}q^{3/4}), with 𝒜 explicit and multiplicative in its q-dependence.

STEP 3: POLYNOMIAL AVERAGE (P8). Average 𝒜(f(k)) along polynomial values, using local densities ρ(p) and ρ(p²).

CHECKS.
- The constant reproduces Vaughan's c_2. For f(k) = k, my C_f = 0.1284787, and Vaughan 2005 (1.14)–(1.15) with k = 2 gives 0.1284787.
- The model term in (A), Σ_k f'(k) V*(x;f(k)), was compared with the exact V in results.json at x = 10^6. It agrees to within 0.15% for all 24 rows (3 polynomials × 8 ratios), and to better than 10^{-3.5} for ratios ≥ 0.1. So the decomposition is right and the true error is far below the proven x^{5/3+ε}.
- An earlier, slower version of this check was stopped by its time limit. An efficient rewrite of the same check completed and produced all the figures quoted here.

LIMITATIONS AND DISCREPANCIES.
- The proven range Y ≥ x^{7/9+δ} comes only from the per-shift error in P2. Extending it needs cancellation over h and k in the pair-count errors (for example BGPVW Theorem 2 plus Weyl bounds for Σ f'(k)e(αhf(k)) as in Brüdern–Wooley Lemma 1). That is not in this plan.
- The normalised data V/(x^{1/2}Y^{3/2}) depend on r = Y/x. The excess over C_f is +1–3% at r = 0.01 and +24–29% at r = 1, consistent with the secondary term O(x^{1/4}Y^{7/4}), i.e. relative size (Y/x)^{1/4}. So C_f is only the r → 0 limit.
- The operator's √r-extrapolated constants are 0.1384±0.007 (k²+1), 0.1385±0.007 (k³+2) and 0.1409±0.008 (2k+1). They agree with mine within the stated uncertainty, but that functional form is empirical; (Y/x)^{1/4} is the theoretically expected correction.
- k³+2 converges slowest in x because there are few moduli (about 21–137 at r = 0.01), so the k-average defining C_f is not yet reached.

SOURCES AND RULE COMPLIANCE. I ran no web searches. I used only papers/ (Vaughan 2005, BGPVW 1998, Brüdern–Wooley 2011) and classical pre-2010 results from memory: E. C. Titchmarsh, The Theory of the Riemann Zeta-Function, 2nd ed. (rev. Heath-Brown), Oxford 1986, Lemma 4.2 and Theorem 5.9 (van der Corput tests); L. Mirsky 1947 (shifted squarefree pairs), cited only as the classical origin of P2. I did not consult anything by the excluded author or the excluded paper, and no 2011+ source apart from the permitted Brüdern–Wooley paper in papers/.

## Main theorem

Notation:
- f is as in problem.md, d = deg f, ρ(m) = #{a mod m : f(a) ≡ 0 mod m}.
- For x ≥ 2 and real y ≥ 1 with f(y) ≤ x, put Y = f(y).
- c0 = Π_p(1−2/p²).
- β(d) = c0 μ²(d) Π_{p|d}(p²−2)^{-1}.
- N_d(q) = q d²/gcd(d²,q).
- ψ2(t) = {t}(1−{t}).
- V*(x;q) = Σ_{d≥1} β(d) N_d(q) ψ2(x/N_d(q)).
- C_f = (2ζ(3/2)/(3π)) Π_p ℓ_f(p), where ℓ_f(p) = (1−ρ(p)/p)(1−1/p)²(1+2/p) + (ρ(p)/p − ρ(p²)/p²)(1−1/p)(p²−2+√p)/p² + (ρ(p²)/p²)(1−1/p)²(1+1/p). The product converges absolutely and C_f > 0.

THEOREM. For every ε > 0, uniformly in x ≥ 2 and y ≥ 1 with f(y) ≤ x:

(A) V_f(x,y) = Σ_{1≤k≤y} f'(k) V*(x; f(k)) + O_{f,ε}(x^{5/3+ε}).

(B) V_f(x,y) = C_f x^{1/2} Y^{3/2} + O_{f,ε}( x^{1/4+ε} Y^{7/4} + x^{1/2} Y^{3/2} y^{-1+ε} + x^{5/3+ε} ).

Consequently, for each fixed δ > 0, V_f(x,y) = C_f x^{1/2}f(y)^{3/2}(1 + O(x^{-η})) uniformly for x^{7/9+δ} ≤ f(y) ≤ x^{1−δ}, with some η = η(δ,d) > 0.

The implied constants depend only on f and ε. The weight f'(k) and the class of f are exactly as in problem.md.

Examples: for f(k) = k, C_f equals Vaughan's c_2 = 0.1284787… For k²+1, k³+2 and 2k+1, C_f = 0.138083, 0.135608 and 0.142613.

## Numerics check

Yes.

Exponents: the operator's fits give α+β = 2.0006 (k²+1), 2.0005 (k³+2) and 2.00005 (2k+1). Fixed-x values of β are 1.538–1.551, drifting towards 3/2 as the ratio shrinks, consistent with a correction of order (Y/x)^{1/4}.

Constants: the operator's extrapolated constants are 0.1384±0.0070 (k²+1), 0.1385±0.0073 (k³+2) and 0.1409±0.0082 (2k+1). The predicted values 0.13808, 0.13561 and 0.14261 all lie inside these envelopes. At the largest x = 2.56·10^8, V/(C_f x^{1/2}Y^{3/2}) decreases towards 1 as the ratio shrinks:
- 1.020 for k²+1 and 1.014 for 2k+1 at r = 0.01;
- 1.03 for k³+2, with slower convergence in x because there are few moduli.

Main term in (A): I computed it independently and compared it with the exact V at x = 10^6. The ratio V/model lies in [0.9985, 1.0010] for all 24 rows, and in [0.9997, 1.0002] for ratios ≥ 0.1.

The r-dependence of the normalised data (excess up to about 29% at r = 1) is real. It is the (Y/x)^{1/4}-order secondary structure, not a discrepancy. The √r extrapolation form used by the operator is empirical; the theory suggests r^{1/4}.

## P1: Local densities and elementary identities

Depends on: none  
Cites: Vaughan 2005, eq. (1.2) and (1.4) (definition and limit formula for f(q,a) = g(q,a), case k=2), Vaughan 2005, Lemma 2.4

Notation: μ is the Möbius function; τ is the divisor function; ζ(2) = π²/6; c0 := Π_p(1−2/p²); β(d) := c0 μ²(d) Π_{p|d}(p²−2)^{-1} for integers d ≥ 1; for r ≥ 1, B(r) := Π_p(1−2/p²) · Π_{p: p²|r} (p²−1)/(p²−2); g(q,l) and Q(x) = Q(x;1,1) are as in problem.md.
(i) For integers q ≥ 1 and l, g(q,l) = (1/q) Σ_{m≥1, gcd(m²,q) | l} μ(m) gcd(m²,q)/m² (an absolutely convergent series). Hence g(q,l) depends only on gcd(l,q), and 0 ≤ g(q,l) ≤ 1/q.
(ii) For every integer r ≥ 1: B(r) = Σ_{d≥1, d²|r} β(d) = Σ_{a,b≥1} μ(a)μ(b) 1[gcd(a,b)² | r] / lcm(a²,b²). The double series converges absolutely, and for every real z ≥ 1, Σ_{a,b≥1, max(a,b)>z} gcd(a,b)²/(a²b²) ≤ 2ζ(2) Σ_{a>z} τ(a)/a² ≤ C_0 (1+log z)/z, with C_0 absolute.
(iii) 0 ≤ β(d) ≤ d^{-2} for all d ≥ 1, and Σ_{d≥1} β(d) = 6/π².
(iv) For real x ≥ 1, |Q(x) − (6/π²)x| ≤ C_1 x^{1/2}, with C_1 absolute.

*Risk:* Low. Part (ii): the density of n with a²|n and b²|n+r is 1[gcd(a,b)²|r]/lcm(a²,b²); expanding the Euler product gives B(r). The bound Σ_b gcd(a,b)²/b² ≤ ζ(2)τ(a) is elementary. Part (iii): β(d) ≤ d^{-2} follows from c0 Π_{p|d} p²/(p²−2) ≤ c0 Π_p (1−2/p²)^{-1} = 1.

## P2: Uniform asymptotic for shifted squarefree pairs

Depends on: P1  
Cites: none

For real x ≥ 2 and an integer r with 1 ≤ r < x, put C(x,r) := #{integers n : 1 ≤ n ≤ x−r, μ²(n) = μ²(n+r) = 1}, and let B(r) := Π_p(1−2/p²) · Π_{p: p²|r} (p²−1)/(p²−2). Then for every ε > 0, |C(x,r) − (x−r)B(r)| ≤ C_ε x^{2/3+ε}, where C_ε depends only on ε (not on r or x).

*Risk:* Classical (Mirsky-type). Suggested proof: expand μ²(n)μ²(n+r) = Σ_{a²|n, b²|n+r} μ(a)μ(b) and take z = x^{1/3}.
- Pairs with a, b ≤ z: count n in one residue class mod lcm(a²,b²), with error ≤ 1 per pair, so the total error is ≤ z².
- Completing the main term to B(r): by P1(ii), the cost is ≪ x(log z)/z.
- Pairs with a > z: bounded by Σ_{n≤x} #{a > z : a²|n} ≤ x/z.
- Pairs with a ≤ z, b > z: bounded by (1 + τ_z(n)) τ_z(n+r), where τ_z(m) := #{b > z : b²|m}. This needs τ(n) ≪ x^ε, which is the only source of the ε.
Pitfall: |Σ_{a≤z, a²|n} μ(a)| is not bounded by 1. Use μ²(n) − t_z(n), where t_z(n) := Σ_{a>z, a²|n} μ(a).

## P3: Exact evaluation of the h-sum (Dirichlet-series main terms)

Depends on: P1, P2  
Cites: none

Notation: c0, β(d) and B(r) as in P1. For integers q, d ≥ 1 let N_d(q) := q d²/gcd(d²,q). Let ψ2(t) := {t}(1−{t}) for real t. Define
V*(x;q) := Σ_{d≥1} β(d) N_d(q) ψ2(x/N_d(q)) (a convergent series of nonnegative terms), and
G(q) := Σ_{d≥1} β(d)/N_d(q) = (c0/q) Π_p (1 + p^{min(2, v_p(q))}/(p²(p²−2))).
Then for every real x > 0 and integer q ≥ 1:
2 Σ_{integers h, 1 ≤ h < x/q} (x − hq) B(hq) = x² G(q) − (6/π²) x + V*(x;q).
Moreover G(q) = Σ_{l=1}^{q} g(q,l)², with g as in problem.md.
(Equivalently, the three terms on the right are the residues at s = 1, s = 0 and the contribution of the pole at s = −1/2 of ζ(s) Σ_d β(d)(d²/gcd(d²,q))^{-s} = Σ_{h≥1} B(hq)h^{-s}. The identity is exact; no contour integral is needed.)

*Risk:* Low; this is bookkeeping.
- Insert B(hq) = Σ_{d²|hq} β(d). The condition d²|hq is equivalent to m_d | h, where m_d := d²/gcd(d²,q).
- With N = q m_d and T = x/N, the floor-sum identity Σ_{1≤j<T}(x − jN) = x²/(2N) − x/2 + (N/2)ψ2(T) holds for every T > 0, including T < 1, where both sides vanish.
- Σ_d β(d) = 6/π² by P1(iii); absolute convergence follows from β(d) ≤ d^{-2}.
- For G(q) = Σ_l g(q,l)²: divide Σ_l Q(x;q,l)² = Q(x) + 2Σ_h C(x,hq) by x² and let x → ∞. Use P2, P1(iv), and V*(x;q) ≤ Σ_d β(d) min(N_d/4, x) = o(x²) for fixed q.
- The Euler product for G is just the multiplicativity of d ↦ β(d)gcd(d²,q)/d².
The main pitfall is an off-by-one in the h-range: pairs with hq = x contribute 0.

## P4: Cross term and diagonal

Depends on: P1, P3  
Cites: Vaughan 2005, Lemma 2.2(ii) (optional: uniform asymptotic for Σ_{m≤y} μ_k(mq); use it only if its stated range covers the moduli needed, otherwise prove the needed estimate directly)

Let g(q,l), E(x;q,l) and Q(x) be as in problem.md, and let G(q) := Σ_{l=1}^q g(q,l)². For every ε > 0 there is C_ε such that, for all real x ≥ 2 and integers 1 ≤ q ≤ x:
(i) |Σ_{l=1}^{q} g(q,l) E(x;q,l)| = |Σ_{n≤x} μ²(n) g(q,n) − x G(q)| ≤ C_ε x^{1/2} q^{-1+ε};
(ii) |Q(x) − (6/π²)x| ≤ C_1 x^{1/2}, with C_1 absolute.

*Risk:* Low. Write t_m := gcd(m²,q). By P1(i), Σ_n μ²(n)g(q,n) = (1/q) Σ_m μ(m)(t_m/m²) Σ_{n≤x, t_m|n} μ²(n). The inner sum vanishes unless t_m is squarefree, and then equals Σ_{n'≤x/t_m, (n',t_m)=1} μ²(n') = (6/π²)(x/t_m) Π_{p|t_m} p/(p+1) + O(2^{ω(t_m)}(x/t_m)^{1/2}). The main terms add up to xG(q) because xG(q) is the x-linear term by definition. The errors give (x^{1/2}/q) Σ_m μ²(m) t_m^{1/2} 2^{ω(t_m)}/m² ≪ x^{1/2}q^{-1} Π_{p|q}(1+2/p)².

## P5: Per-modulus reduction to the model V*

Depends on: P1, P2, P3, P4  
Cites: none

Let V*(x;q) = Σ_{d≥1} β(d) N_d(q) ψ2(x/N_d(q)), where β(d) = c0 μ²(d) Π_{p|d}(p²−2)^{-1}, c0 = Π_p(1−2/p²), N_d(q) = q d²/gcd(d²,q) and ψ2(t) = {t}(1−{t}). Let E(x;q,l) be as in problem.md. For every ε > 0 there is C_ε such that, for all real x ≥ 2 and integers 1 ≤ q ≤ x:
| Σ_{l=1}^{q} E(x;q,l)² − V*(x;q) | ≤ C_ε ( x^{5/3+ε}/q + x^{1/2} ).

*Risk:* Low. Use G(q) = Σ_l g(q,l)² (P3).
- Expand: Σ_l E² = Σ_l Q(x;q,l)² − 2x Σ_{n≤x} μ²(n)g(q,n) + x²G(q).
- Diagonal plus off-diagonal: Σ_l Q(x;q,l)² = Q(x) + 2 Σ_{1≤h<x/q} C(x,hq).
- P2 gives an error ≤ 2(x/q)C_ε x^{2/3+ε}.
- Then P3 gives Σ_l E² = V*(x;q) + [Q(x) − 6x/π²] − 2x Σ_l g(q,l)E(x;q,l) + error.
- P4 bounds the last two terms by x^{1/2} + x^{3/2+ε}/q.
Check: Σ_n μ²(n)g(q,n) = Σ_l g(q,l)Q(x;q,l) because g(q,·) has period q.

## P6: Core lattice-type sum Σ_t ψ2(Z/t²) (van der Corput) (CRUX)

Depends on: none  
Cites: Titchmarsh 1986 (The Theory of the Riemann Zeta-Function, 2nd ed., Oxford), Theorem 5.9 (van der Corput second-derivative test), Titchmarsh 1986, Lemma 4.2 (first-derivative test for integrals)

Let ψ2(t) := {t}(1−{t}) for real t, and for real Z > 0 let S(Z) := Σ_{t=1}^{∞} ψ2(Z/t²). The series converges, since ψ2(v) = v − v² for 0 ≤ v ≤ 1. Then there is an absolute constant C_2 such that, for all Z > 0,
| S(Z) − (ζ(3/2)/π) Z^{1/2} | ≤ C_2 min(Z^{1/4}, Z^{1/2}).
Here ζ(3/2)/π = (1/2)∫_0^∞ ψ2(v) v^{-3/2} dv = Z^{-1/2}∫_0^∞ ψ2(Z/t²) dt.

*Risk:* This is the analytic heart. Suggested proof for Z ≥ 1, with L = Z^{1/8}, T0 = Z^{1/4} and T1 = Z^{1/2}/L. Compare Σ_{t≥1} with ∫_0^∞ψ2(Z/t²)dt.
(a) t ≤ T0: trivial, giving O(Z^{1/4}).
(b) T0 < t ≤ T1: use ψ2(v) = 1/6 − π^{-2} Σ_{n≥1} cos(2πnv)/n², valid for all real v. On dyadic blocks t ~ D, the phase nZ/t² has second derivative ≍ nZ/D⁴, so the van der Corput bound is ≪ (nZ)^{1/2}/D + D²/(nZ)^{1/2}. Summed this gives O(Z^{1/4} + Z^{1/2}/L²). The integrals ∫cos(2πnZ/t²)dt are ≪ T1³/(nZ) by the first-derivative test. The 1/6-parts differ by O(1).
(c) t > T1: ψ2(Z/t²) is continuous with total variation ≤ (L²+1)/2 on [T1,∞), so the sum minus the integral is O(L²).
Total: O(Z^{1/4}). For Z < 1, use S(Z) ≤ ζ(2)Z.
Risks: the transition region t ≍ √Z, where van der Corput fails, must be routed to (c). Make sure Theorem 5.9's hypotheses (F'' of one sign, λ ≤ |F''| ≤ hλ) are checked blockwise. ∫_0^∞ψ2(v)v^{-3/2}dv = 2ζ(3/2)/π was verified numerically (1.6630898).

## P7: Per-modulus main term of the model V* (CRUX)

Depends on: P1, P6  
Cites: none

Notation: c0 = Π_p(1−2/p²); β(d) = c0 μ²(d) Π_{p|d}(p²−2)^{-1}; N_d(q) = q d²/gcd(d²,q); ψ2(t) = {t}(1−{t}); V*(x;q) := Σ_{d≥1} β(d) N_d(q) ψ2(x/N_d(q)).
Define, for integers q ≥ 1,
𝒜(q) := (ζ(3/2)/π) · Π_{p∤q} (1−1/p)²(1+2/p) · Π_{p∥q} (1−1/p)(p²−2+√p)/p² · Π_{p²|q} (1−1/p)²(1+1/p).
Then for every ε > 0 there is C_ε (depending only on ε) such that, for all real x ≥ 1 and integers 1 ≤ q ≤ x:
| V*(x;q) − 𝒜(q) x^{1/2} q^{1/2} | ≤ C_ε x^{1/4+ε} q^{3/4}.

*Risk:* Multiplicative bookkeeping; the main risk is a wrong constant or a hidden non-uniformity in q. Suggested route:
- Write d = e·t with e squarefree, all primes of e dividing q, and gcd(t,q) = 1. Then N_d = q m_e t² with m_e = e²/gcd(e²,q), and β(d) = β(e)β(t)/c0.
- Write β(t)t² = c0 μ²(t)κ(t), with κ(t) = Π_{p|t} p²/(p²−2). Expand μ²κ = λ*1, where λ(p) = 2/(p²−2), λ(p²) = −p²/(p²−2) and λ(p^j) = 0 for j ≥ 3.
- Remove gcd(t,q) = 1 with Σ_{r|q} μ(r). This reduces V* to Σ_e (β(e)/c0) q m_e c0 Σ_m λ(m) Σ_{r|q} μ(r) S(x/(q m_e m² r²)), with S from P6.
- |λ(l²)| ≈ 1 makes Σ|λ(m)|m^{-1/2} diverge logarithmically. Use P6's Z^{1/2} branch when m² r² > Z; this costs log(2x).
- The q-dependence of the error, Σ_{e|rad q} m_e^{3/4} Π_{p|e}(p²−2)^{-1} · τ(q), is ≪ q^ε ≤ x^ε.
- Main-term check: the Euler factors are (p−1)²(p+2)/p³ for p∤q, (p−1)(p²−2+√p)/p³ for p∥q, and (p−1)²(p+1)/p³ for p²|q.
As checks: 𝒜(1) = 0.23845, and the mean of 𝒜 over all q equals (3/2)·0.128479 (Vaughan's c_2).

## P8: Average of 𝒜 over polynomial values

Depends on: none  
Cites: none

Let f be as in problem.md (integer-valued, degree d ≥ 1, f(t) ≥ 2 and f'(t) ≥ 1 for t ≥ 1), let ρ(m) = #{a mod m : f(a) ≡ 0 mod m}, and let
𝒜(q) = (ζ(3/2)/π) Π_{p∤q}(1−1/p)²(1+2/p) Π_{p∥q}(1−1/p)(p²−2+√p)/p² Π_{p²|q}(1−1/p)²(1+1/p).
Define C_f := (2ζ(3/2)/(3π)) Π_p ℓ_f(p), where
ℓ_f(p) := (1−ρ(p)/p)(1−1/p)²(1+2/p) + (ρ(p)/p − ρ(p²)/p²)(1−1/p)(p²−2+√p)/p² + (ρ(p²)/p²)(1−1/p)²(1+1/p).
The product converges absolutely, since ℓ_f(p) = 1 + O_f(p^{-2}), and C_f > 0. For every ε > 0 and all real y ≥ 1, with Y = f(y):
Σ_{1≤k≤y} f'(k) f(k)^{1/2} 𝒜(f(k)) = C_f Y^{3/2} + O_{f,ε}( Y^{3/2} y^{-1+ε} ).

*Risk:* Moderate.
- Write 𝒜(q) = 𝒜(1)h(q) with h multiplicative, h(p^v) depending on min(v,2), and h = 1*γ. Here γ(p) = a_p − 1 = −√p(√p−1)/((p+2)(p−1)), γ(p²) = (1−√p)/((p+2)(p−1)), γ(p^j) = 0 for j ≥ 3, and a_p := (p²−2+√p)/(p²+p−2).
- Swap the sums: Σ_e γ(e) Σ_{k≤y, e|f(k)} w(k), with w(k) = f'(k)f(k)^{1/2} eventually monotone.
- Each of the ρ(e) residue classes mod e gives (1/e)Σ_k w(k) + O(w(y)).
- Truncate at e ≤ y. For the tail, use #{k≤y : e|f(k)} ≤ ρ(e)(y/e+1).
- Check that the mean Σ_e γ(e)ρ(e)/e equals the product of ℓ_f(p)/((1−1/p)²(1+2/p)).
- Bound ρ(e) for cube-free e with care at primes dividing the denominator of f or disc(f) (finitely many, so the constants depend on f).
- Euler–Maclaurin: Σ_{k≤y} f'(k)f(k)^{1/2} = (2/3)Y^{3/2} + O_f(Y^{3/2}/y).
Numerical values: C_f = 0.128479 (f = k), 0.138083 (k²+1), 0.135608 (k³+2), 0.142613 (2k+1).

## P9: Assembly: main theorem

Depends on: P5, P7, P8  
Cites: none

Let f, d, ρ and V_f(x,y) be as in problem.md. Let V*(x;q) = Σ_{d≥1} β(d) N_d(q) ψ2(x/N_d(q)), with β(d) = c0 μ²(d) Π_{p|d}(p²−2)^{-1}, c0 = Π_p(1−2/p²), N_d(q) = q d²/gcd(d²,q) and ψ2(t) = {t}(1−{t}). Let C_f be as in P8. Then for every ε > 0, uniformly for real x ≥ 2 and y ≥ 1 with f(y) ≤ x, writing Y = f(y):
(A) V_f(x,y) = Σ_{1≤k≤y} f'(k) V*(x; f(k)) + O_{f,ε}(x^{5/3+ε});
(B) V_f(x,y) = C_f x^{1/2} Y^{3/2} + O_{f,ε}( x^{1/4+ε} Y^{7/4} + x^{1/2} Y^{3/2} y^{-1+ε} + x^{5/3+ε} ).
In particular, for fixed δ > 0 and x^{7/9+δ} ≤ Y ≤ x^{1−δ}, the error in (B) is ≪ x^{1/2}Y^{3/2}·x^{-η} for some η = η(δ,d) > 0.

*Risk:* Low.
- Since f' ≥ 1 on [1,∞), f is increasing, so 2 ≤ f(k) ≤ Y ≤ x for 1 ≤ k ≤ y. P5 and P7 therefore apply with q = f(k).
- P5 errors: Σ_k f'(k)(x^{5/3+ε}/f(k) + x^{1/2}) ≪_f x^{5/3+ε} log(2Y) + x^{1/2}Y, using Σ_{k≤y} f'(k)/f(k) ≪_f log(2Y) (monotone comparison with ∫ f'/f).
- P7 errors: Σ_k f'(k) x^{1/4+ε} f(k)^{3/4} ≪_f x^{1/4+ε} Y^{7/4}.
- Main term: x^{1/2} Σ_k f'(k) f(k)^{1/2} 𝒜(f(k)) = C_f x^{1/2}Y^{3/2} + O(x^{1/2}Y^{3/2}y^{-1+ε}) by P8.
- For the 'in particular' clause: x^{1/4}Y^{7/4} ≤ x^{1/2}Y^{3/2}x^{-δ/4}; x^{5/3} ≤ x^{1/2}Y^{3/2}x^{-3δ/2}; and y ≫_f Y^{1/d}.
The main term C_f x^{1/2}Y^{3/2} is not asymptotic at Y ≍ x; there (A) is the meaningful statement.
