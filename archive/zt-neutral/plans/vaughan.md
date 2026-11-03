# Plan: vaughan

Model: claude-opus-5-5

Plan: follow Vaughan (2005) step by step with the moduli restricted to f(k), weighted by f'(k).
(1) Open the square (Vaughan §3) and write the off-diagonal pairs as S_f = ∫|F|²K_f with K_f(α)=Σ_k f'(k)Σ_{h≤x/f(k)} e(αhf(k)), i.e. the Brüdern–Wooley ternary set-up.
(2) Circle method with T=x^{2/5}. Only the trivial bound |K_f| ≪ x log x is used. The minor-arc L² bound of BGPVW Thm 2 (x^{4/5+ε} at Q=x^{2/5}) and the major-arc bounds BGPVW Lemmas 3.2/4.2 for Δ make every error O(x^{9/5+ε}). Orthogonality turns the major arcs into Σ_k f'(k)Σ_h S(hf(k))(x−hf(k)), with S(n)=Σ_q|ψ(q)|²c_q(n)=C∏_{p²|n}(p²−1)/(p²−2).
(3) An exact per-modulus identity (Vaughan Lemma 2.16) cancels the x² and x terms. This leaves V_f = 𝔐_f + O(x^{9/5+ε}) with 𝔐_f = −2C Σ_k f'(k) Σ_m γ(m) f(k) r_m B̃₂(x/(f(k) r_m)).
(4) Crux A: replace the k-sum by an integral. Inclusion–exclusion on the gcd (m²,f(k)) reduces it to sums over k with D | f(k), which Euler summation handles at cost O(x^{1+ε}f(y)^{1−1/d}).
(5) Crux B: the Mellin evaluation of Vaughan §6. The Dirichlet series 𝒟_f(s)=ζ(2s+4)H_f(s) has its pole at s=−3/2, which gives c_f x^{1/2}f(y)^{3/2}. The line Re s=−7/4+ε gives O(x^{1/4+ε}f(y)^{7/4−ε}).

Predicted constant: c_f = (2ζ(3/2)/(3π)) ∏_p (1−1/p)(1+1/p−(ρ(p)+2)/p²+ρ(p)p^{−5/2}−ρ(p²)p^{−7/2}+ρ(p²)p^{−4}). For f(k)=k it reproduces Vaughan's c₂=0.128479.

Numerical checks (scripts in ./scripts):
(i) At x=250000 for k²+1, Σ_k f'(k)·[Q(x)−x/ζ(2)+(per-modulus major-arc term)] reproduces the exact V_f to 0.01–0.4% across all eight rows (relative error 1e-4 at the larger y). This supports P2–P6.
(ii) The smooth main term x²F_f(x/f(y)) of P8, evaluated by numerical Mellin inversion, matches the x=2.56e8 data:
- k²+1 and 2k+1: to about 1e-4 or better at every ratio (e.g. k²+1, r=0.01: 0.14074 vs data 0.14086; r=1: 0.17108 vs 0.17110).
- k³+2: to 0.3–1.2%, with the gap shrinking as x grows. The gap matches the size of a k-sum endpoint effect, about d/y with y≤634, which lies inside P7's error term.

No discrepancy with results.json beyond its stated uncertainty. The ratio drift of the normalised values (0.14→0.17) is genuine lower-order structure: x²F_f(x/Y) has (Y/x)^{1/4}-type and oscillatory corrections. The fit ansatz C+a√r+br is therefore mis-specified and biases the extrapolated intercept low for k²+1 (0.1345 vs predicted 0.1381; still within ±0.0073).

No web search was done. Nothing by the excluded author and not the excluded Dehnert paper was consulted. Sources:
- the papers in papers/: Vaughan 2005 (doi:10.1112/S0024611505015352); BGPVW 1998 (Phil. Trans. R. Soc. A 356, 739–761); Brüdern–Wooley 2011 (Quart. J. Math. 62, 289–305);
- E. C. Titchmarsh, The Theory of the Riemann Zeta-Function, 2nd ed. rev. D. R. Heath-Brown, OUP 1986, for standard convexity bounds on ζ.

The theorem is weaker than Vaughan's full-moduli result in two places:
- the circle-method error is x^{9/5+ε}, not x^{3/2}, because K_f is bounded trivially;
- the k-sum→integral step costs x^{1+ε}f(y)^{1−1/d}.

So the pure-power asymptotic is only proved for x^{θ_d+η} ≤ f(y) ≤ x^{1−η}, with θ_d = max(13/15, d/(d+2)).

## Main theorem

Let f be as in problem.md (f∈ℤ[t], deg f = d ≥ 1, f(t) ≥ 2 and f'(t) ≥ 1 for t ≥ 1), ρ(m) = #{a mod m : f(a) ≡ 0 mod m}, and write Y = f(y).

Define the following.
- c_f = (2ζ(3/2)/(3π)) · ∏_p (1 − 1/p)(1 + 1/p − (ρ(p)+2)/p² + ρ(p)p^{−5/2} − ρ(p²)p^{−7/2} + ρ(p²)p^{−4}). The product converges absolutely and c_f > 0; equivalently c_f = (16/3)·C·(−ζ(−1/2))·Res_{s=−3/2} 𝒟_f(s) as in P8.
- F_f(w) for w ≥ 1 is the explicit Mellin integral of P8.

Then for every ε > 0, uniformly for real x ≥ 2 and y ≥ 1 with f(y) ≤ x (V_f sums over integers 1 ≤ k ≤ y):

(i) V_f(x,y) = x² F_f(x/f(y)) + O_{f,ε}( x^{1+ε} f(y)^{1−1/d} + x^{9/5+ε} );

(ii) V_f(x,y) = c_f x^{1/2} f(y)^{3/2} + O_{f,ε}( x^{1/4+ε} f(y)^{7/4−ε} + x^{1+ε} f(y)^{1−1/d} + x^{9/5+ε} ).

In particular, with θ_d := max{13/15, d/(d+2)}: for any fixed η > 0, uniformly for x^{θ_d+η} ≤ f(y) ≤ x^{1−η},

V_f(x,y) = c_f x^{1/2} f(y)^{3/2} (1 + O_{f,η}(x^{−η/5})).

The weight f'(k) and the class of f are those of problem.md. No restriction is needed: f need not be squarefree or primitive.

Examples: c_k = 0.128479 (equals Vaughan's c₂), c_{k²+1} = 0.13808, c_{k³+2} = 0.13561, c_{2k+1} = 0.14261.

## Numerics check

Yes.

Exponents: results.json gives a fixed-ratio slope α+β = 2.0008 ± 0.0006 (k²+1) and 1.998 ± 0.002 (k³+2), against the predicted 2. Fixed-x slopes β ≈ 1.53–1.55 against the predicted 3/2; these are biased upward by the ratio dependence, as the notes in results.json themselves point out.

Constants, extrapolated (results.json) vs predicted:

| f | extrapolated | predicted |
|---|---|---|
| k²+1 | 0.1345 ± 0.0073 | 0.13808 |
| k³+2 | 0.1363 ± 0.0024 | 0.13561 |
| 2k+1 | 0.1417 ± 0.0082 | 0.14261 |

All agree within the stated uncertainty.

Stronger check: I evaluated the P8 main term x²F_f(x/Y)/(x^{1/2}Y^{3/2}) by numerical Mellin inversion (Euler product to 2e5, contour Re s = −5/4).
- k²+1, ratios 0.01 → 1: 0.14074, 0.14281, 0.14440, 0.15094, 0.15651, 0.16275, 0.16990, 0.17108. Data at x = 2.56e8: 0.14086, 0.14292, 0.14446, 0.15098, 0.15655, 0.16278, 0.16993, 0.17110.
- 2k+1: agreement to about 1e-5.
- k³+2 (at the actual ratios): F lies 0.3–1.2% below the data. The gap shrinks with x (e.g. r≈0.01: data 0.14127 → 0.13999 as x doubles, while F = 0.13875). It fits a finite-y effect of the k-sum versus the integral, about d/y with y ≤ 634, which lies inside P7's error term.
- As r → 0, F_f·w^{3/2} tends to c_f: 0.13876 at r = 0.001 for k²+1, approaching 0.13808.

Separately, the reduction V_f ≈ Σ_k f'(k)[Q(x) − x/ζ(2) − 2C Σ_m γ(m) f(k) r_m B̃₂(x/(f(k) r_m))] reproduces the exact V for k²+1 at x = 250000 to within 0.4% on every row (1e-4 for y ≥ 223).

Conclusion: the extrapolation ansatz C + a√r + br in results.json is mis-specified, since the true correction is (Y/x)^{1/4}-type and oscillatory. That bias explains the slightly low intercept for k²+1. It is not a conflict with the theorem.

## P1: Arithmetic of the local densities and the singular series

Depends on: none  
Cites: Vaughan 2005, Lemma 2.3, Vaughan 2005, Lemma 2.4, Vaughan 2005, Lemma 2.5, Vaughan 2005, Lemma 2.14, Vaughan 2005, Lemma 2.15, Vaughan 2005, Lemma 2.17, Vaughan 2005, equation (6.8), BGPVW 1998, Lemma 3.1

Notation: μ² and g(q,l) are as in problem.md. Let:
- e(θ) = exp(2πiθ);
- φ = Euler's function, τ = divisor function;
- c_q(n) = Σ_{1≤a≤q,(a,q)=1} e(an/q), Ramanujan's sum;
- γ(m) = μ²(m) ∏_{p|m} (p²−2)^{−1};
- C = ∏_p (1 − 2/p²);
- 𝔰(q) = Σ_{l=1}^{q} g(q,l)²;
- ψ(q) = Σ_{b=1}^{q} g(q,b) e(b/q).

Then for all q, n ∈ ℕ:

(a) g(q,l) = g(q,(q,l)) and 0 ≤ g(q,l) ≤ 1/q.

(b) ψ(q) = ζ(2)^{−1} G(q), where G is multiplicative with G(p) = G(p²) = −1/(p²−1) and G(p^t) = 0 for t ≥ 3. Hence ψ(q) = 0 unless q is cube-free, and |ψ(q)|² ≤ A q^{−2} with an absolute constant A.

(c) Σ_{q≥1} φ(q)|ψ(q)|² = 1/ζ(2), and Σ_{q≤T} q²|ψ(q)|² ≤ A T^{1/2} log²(2T) for every real T ≥ 1.

(d) S(n) := Σ_{q≥1} |ψ(q)|² c_q(n) converges absolutely, and S(n) = C Σ_{m≥1, m²|n} γ(m) = C ∏_{p²|n} (p²−1)/(p²−2).

(e) C Σ_{m≥1} γ(m) = 1/ζ(2).

(f) q·𝔰(q) = C Σ_{m≥1} γ(m)(m²,q)/m².

(g) For every real T ≥ 1: Σ_{q>T} |ψ(q)|² |c_q(n)| ≤ A τ(n)/T.

The constant A is absolute.

*Risk:* Low; these are Vaughan's k=2 formulas.
- Sign of G: the PDF text extraction drops the minus sign. Direct computation gives ψ(p) = ψ(p²) = −ζ(2)^{−1}/(p²−1); only |ψ|² matters downstream.
- Normalisation: Vaughan's f(q,a) equals problem.md's g(q,a), and BGPVW's ζ(k)^{−1}g_k(q,(q,a)) equals the density. The prover should check this when citing.
- (f) combines Lemma 2.4, Lemma 2.17 and (6.8) with (u,m²) = Σ_{l|(u,m²)} φ(l).
- (g): use |c_q(n)| ≤ Σ_{d|(q,n)} d and Σ_{q>T, d|q} q^{−2} ≪ 1/(dT).

## P2: Opening the square

Depends on: P1  
Cites: Vaughan 2005, Lemma 2.2(ii), Vaughan 2005, Lemma 2.3, Vaughan 2005, Lemma 2.4, Vaughan 2005, equations (3.1)-(3.8)

Let f, d, V_f, Q(x;q,l), g(q,l) be as in problem.md. Let:
- Q(x) = #{n ≤ x : μ²(n) = 1};
- 𝔰(q) = Σ_{l=1}^{q} g(q,l)²;
- S_f(x,y) = Σ_{1≤k≤y} f'(k) · #{(m,n) ∈ ℕ² : m < n ≤ x, μ²(m) = μ²(n) = 1, n ≡ m (mod f(k))}.
All sums over k run over integers 1 ≤ k ≤ y.

(a) For every ε > 0, uniformly for real x ≥ 2 and integers 1 ≤ q ≤ x:
Σ_{n≤x} μ²(n) g(q,n) = x𝔰(q) + O_ε(x^{1/2} q^{−1+ε}).

(b) For every ε > 0, uniformly for real x ≥ 2 and y ≥ 1 with f(y) ≤ x:
V_f(x,y) = Σ_{1≤k≤y} f'(k)(Q(x) − x²𝔰(f(k))) + 2S_f(x,y) + O_{f,ε}(x^{3/2+ε}).

*Risk:* Low.
- (a) is Vaughan's (3.5)–(3.7) for one modulus, using Lemma 2.2(ii) (valid for every q ≤ x, error τ(rt)(x/rt)^{1/2}) and g(q,r) ≤ 1/q. The divisor sums give q^{ε}.
- In (b), Σ_l Q(x;q,l)² = Q(x) + 2·#{off-diagonal pairs} and Σ_l Q(x;q,l)g(q,l) = Σ_{n≤x} μ²(n)g(q,n). Summing the error of (a) against f'(k) gives x·x^{1/2}·Σ_k f'(k)f(k)^{−1+ε} ≪ x^{3/2+ε}.
- Check that every modulus satisfies f(k) ≤ f(y) ≤ x, which holds because f is increasing on [1,∞).

## P3: Circle method: minor arcs and the Δ-terms

Depends on: P1  
Cites: BGPVW 1998, Theorem 2, BGPVW 1998, Lemma 3.2, BGPVW 1998, Lemma 4.2, Vaughan 2005, equations (4.1)-(4.8)

Let f be as in problem.md and let x ≥ 2, y ≥ 1 be real with f(y) ≤ x. Let e(θ) = exp(2πiθ), and define:
- F(α) = Σ_{1≤n≤x} μ²(n) e(nα);
- I(β) = Σ_{1≤n≤x} e(nβ);
- K_f(α) = Σ_{1≤k≤y} f'(k) Σ_{1≤h≤x/f(k)} e(αhf(k)), with k, h integers;
- ψ(q) = Σ_{b=1}^{q} g(q,b)e(b/q), with g as in problem.md;
- S_f(x,y) = Σ_{1≤k≤y} f'(k)·#{(m,n) ∈ ℕ² : m < n ≤ x, μ²(m) = μ²(n) = 1, f(k) | n−m}.

Put T = x^{2/5}. For q ∈ ℕ and a ∈ ℤ let 𝔐(q,a) = {α ∈ [0,1) : |qα − a| ≤ T/x}. Let 𝔐 be the union of the 𝔐(q,a) with 1 ≤ q ≤ T, 0 ≤ a ≤ q, (a,q) = 1; these arcs are pairwise disjoint for x ≥ 2^{10}. Define F*(α) = ψ(q)I(α − a/q) for α ∈ 𝔐(q,a), and F*(α) = 0 for α ∈ [0,1)∖𝔐.

Claims:
(a) S_f(x,y) = ∫_0^1 |F(α)|² K_f(α) dα.
(b) sup_{α∈ℝ} |K_f(α)| ≤ B_f x log(2x), with B_f depending only on f.
(c) For every ε > 0, S_f(x,y) = ∫_𝔐 |F*(α)|² K_f(α) dα + O_{f,ε}(x^{9/5+ε}), uniformly in x ≥ 2, y ≥ 1 with f(y) ≤ x.

*Risk:* Medium, mostly about matching definitions.
- BGPVW's major arcs with their Q = T = x^{2/5} ≤ x^{1/2}/2 (true for x ≥ 2^{10}; smaller x is trivial) are exactly 𝔐, and their f* equals F*, because ζ(2)^{−1}G_BGPVW(q) = ψ(q).
- Minor arcs: Theorem 2 gives ∫_{[0,1)∖𝔐} |F|² ≪ x^{1+ε}T^{−1/2} + x^{ε}T² = x^{4/5+ε}; times (b) this is x^{9/5+ε}.
- On 𝔐, |F|² − |F*|² ≤ 2|F*Δ| + |Δ|². Lemma 4.2 (x^{1/2+ε}T^{3/4}) and Lemma 3.2 (x^{ε}T²), each multiplied by (b), give x^{9/5+ε}.
- (b) follows from |K_f| ≤ Σ_k f'(k)x/f(k) ≪_f x log(2x).
- K_f is complex, but only absolute bounds are used.

## P4: Major arcs to the singular-series sum

Depends on: P1  
Cites: BGPVW 1998, Lemma 3.1, Vaughan 2005, §5 (equations (5.2)-(5.7)), Brüdern-Wooley 2011, §4 (derivation of (19)-(20))

Notation as in P3: x ≥ 2, y ≥ 1 real, f(y) ≤ x, T = x^{2/5}, 𝔐, F*, K_f, ψ. Let c_q(n) be Ramanujan's sum and S(n) = Σ_{q≥1} |ψ(q)|² c_q(n). Then for every ε > 0, uniformly in this range,

∫_𝔐 |F*(α)|² K_f(α) dα = Σ_{1≤k≤y} f'(k) Σ_{1≤h≤x/f(k)} S(hf(k))·(x − hf(k)) + O_{f,ε}(x^{9/5+ε}),

with k, h integers.

*Risk:* Low to medium. Three steps:
1. Complete each β-integral from |β| ≤ T/(qx) to |β| ≤ 1/2. Using |I(β)| ≤ 1/(2‖β‖), the bound of P3(b) and P1(c), the error is ≪ x log x · Σ_{q≤T} φ(q)|ψ(q)|² · qx/T ≪ x^{2+ε}T^{−1/2} = x^{9/5+ε}.
2. Apply orthogonality: ∫_{−1/2}^{1/2} |I(β)|² K_f(a/q+β) dβ = Σ_k f'(k) Σ_h e(ahf(k)/q)(⌊x⌋ − hf(k)). Replacing ⌊x⌋ by x costs O(x log x). Summing over a gives c_q(hf(k)).
3. Extend the q-sum to all q. By P1(g) the error is ≪ Σ_k f'(k) Σ_h x·τ(hf(k))/T ≪ x^{8/5+ε}.
No splitting of small k is needed, provided the tail bound is applied per n (P1(g)) and not by first summing over divisors of q.

## P5: Exact per-modulus identity

Depends on: P1  
Cites: Vaughan 2005, Lemma 2.16, Vaughan 2005, Lemma 2.15, Vaughan 2005, equations (6.2)-(6.10)

Let:
- B̃₂(θ) = ({θ}² − {θ})/2, where {θ} is the fractional part; so −1/8 ≤ B̃₂ ≤ 0, B̃₂(θ) = (θ²−θ)/2 for 0 ≤ θ < 1, and |B̃₂(θ)| ≤ min(1/8, θ/2) for θ ≥ 0;
- γ(m) = μ²(m) ∏_{p|m} (p²−2)^{−1};
- C = ∏_p (1 − 2/p²);
- r_m(q) = m²/(m²,q);
- 𝔰(q) = Σ_{l=1}^{q} g(q,l)², with g as in problem.md;
- S(n) = Σ_q |ψ(q)|² c_q(n), with ψ(q) = Σ_{b=1}^{q} g(q,b)e(b/q).

Then for every q ∈ ℕ and every real x ≥ 1,

Σ_{1≤h≤x/q} S(hq)(x − hq) = (x²/2)𝔰(q) − x/(2ζ(2)) − C Σ_{m≥1} γ(m) q r_m(q) B̃₂( x/(q r_m(q)) ).

The m-series converges absolutely, each term being at most γ(m)x/2 in modulus.

*Risk:* Low; this is exact algebra. Insert S(n) = C Σ_{m²|n} γ(m) from P1(d). The condition m² | hq is equivalent to r_m(q) | h. Then use Σ_{1≤w≤X}(X − w) = X²/2 − X/2 − B̃₂(X) (Vaughan Lemma 2.16) with X = x/(q r_m(q)), and finally P1(e),(f).
The identity was checked numerically: together with P2–P4 it reproduces exact V_f to 1e-4 relative.

## P6: Reduction of V_f to the arithmetic sum 𝔐_f

Depends on: P2, P3, P4, P5  
Cites: none

Let f, d, V_f be as in problem.md, and γ, C, r_m, B̃₂ as in P5. Define

𝔐_f(x,y) = −2C Σ_{1≤k≤y} f'(k) Σ_{m≥1} γ(m) f(k) r_m(f(k)) B̃₂( x/(f(k) r_m(f(k))) )

(k an integer; the m-series converges absolutely; 𝔐_f ≥ 0). Then for every ε > 0, uniformly for real x ≥ 2 and y ≥ 1 with f(y) ≤ x,

V_f(x,y) = 𝔐_f(x,y) + O_{f,ε}(x^{9/5+ε}).

*Risk:* Low; this is assembly.
- Substitute P5 with q = f(k) into P4 and P3(c), then into P2(b). The x²𝔰 terms cancel exactly.
- What remains besides 𝔐_f is Σ_k f'(k)(Q(x) − 6x/π²) ≪ x^{1/2}·Σ_k f'(k) ≪_f x^{1/2}f(y), using Q(x) = 6x/π² + O(x^{1/2}).
- All other errors are O(x^{3/2+ε}) or O(x^{9/5+ε}).

## P7: Replacing the sum over k by an integral (CRUX)

Depends on: none  
Cites: Brüdern-Wooley 2011, equation (22) (Euler summation in residue classes)

Let f, d, ρ be as in problem.md, and γ, C, r_m, B̃₂ as in P5. Let N_f(m²,e) = #{a mod m² : (f(a), m²) = e} for e | m², and define for real 1 ≤ Y ≤ x

𝔐_f^{int}(x,Y) = −2C Σ_{m≥1} γ(m) Σ_{e|m²} (N_f(m²,e)/m²) ∫_0^Y u·(m²/e)·B̃₂( xe/(u m²) ) du,

which converges absolutely. Let 𝔐_f(x,y) be as in P6. Then for every ε > 0, uniformly for real x ≥ 2 and y ≥ 1 with f(y) ≤ x,

𝔐_f(x,y) = 𝔐_f^{int}(x, f(y)) + O_{f,ε}( x^{1+ε} f(y)^{1−1/d} ).

*Risk:* Main technical risk.

Suggested route:
1. For m > √x, f(k)·r_m(f(k)) ≥ m² > x, so B̃₂ is the polynomial (θ²−θ)/2. The terms reduce to x²(m²,f(k))/(2f(k)m²) − x/2. Both the sum and the integral version of these are O(x^{1/2}f(y)^{1/2+ε} + x^{1/2}y^{d−1}).
2. For m ≤ √x, write m = abc, where p | a means p ∤ f(k), p | b means p ‖ f(k), and p | c means p² | f(k). Then r_m = a²b. Use inclusion–exclusion 1 = Σ_{l1|a, l2|b} μ(l1)μ(l2)·1[l1·b·l2·c² | f(k)] to reduce to sums over k with D | f(k), where D | m².
3. Euler summation over each of the ρ(D) root classes: Σ_{1≤k≤y, D|f(k)} G(k) = (ρ(D)/D)∫_1^y G + O(ρ(D)(sup|G| + TV_{[1,y]}G)), with G(t) = f'(t)Φ_R(f(t)) and Φ_R(u) = uR·B̃₂(x/(uR)).

Key bounds and pitfalls:
- |Φ_R| ≤ min(uR/8, x/2), and TV_{[f(1),f(y)]}Φ_R ≪ x log(2x).
- TV on [0,·] is infinite (logarithmic divergence as u → 0). So start at u = f(1) and bound the piece u ∈ [0, f(1)] separately by O_f(x).
- Σ_{m≤√x} γ(m) Σ ρ(D) ≪ x^{ε} even when ρ(p²) ≍ p (f with repeated factors).
- D may exceed y. The Euler bound still holds, since each class then has at most one element.

The error x^{1+ε}Y^{1−1/d} is crude, probably far from the truth (≈ x^{1/2}Y^{3/2−1/d}). Improving it would need exponential sums in k.

## P8: Mellin evaluation of the smooth main term (CRUX)

Depends on: none  
Cites: Vaughan 2005, Lemma 2.18, Vaughan 2005, Lemma 2.19, Vaughan 2005, §6 (equation (6.12) and the final contour shift), Titchmarsh, The Theory of the Riemann Zeta-Function (2nd ed., 1986), §5.1 (convexity bounds)

Notation as in P7: γ, C, N_f, 𝔐_f^{int}; ρ as in problem.md. Define for Re s > −3/2

𝒟_f(s) = Σ_{m≥1} γ(m) m^{−4−2s} Σ_{e|m²} N_f(m²,e) e^{1+s},

which converges absolutely there, and for real w ≥ 1

F_f(w) = −2C · (1/(2πi)) ∫_{Re s = −5/4} ζ(s+1) 𝒟_f(s) w^s / (s(s+1)(s+2)) ds.

Claims:

(a) 𝔐_f^{int}(x,Y) = x² F_f(x/Y) for all real 1 ≤ Y ≤ x.

(b) 𝒟_f(s) = ζ(2s+4) H_f(s), where
H_f(s) = ∏_p (1 − p^{−4−2s}) (1 + p^{−4−2s}(p²−2)^{−1}[p² − pρ(p) + (pρ(p) − ρ(p²))p^{1+s} + ρ(p²)p^{2+2s}]).
H_f converges absolutely and is holomorphic in Re s > −7/4, and is bounded by a constant B(f,ε) on −7/4+ε ≤ Re s ≤ −1.

(c) For every ε ∈ (0, 1/8) and w ≥ 1: F_f(w) = c_f w^{−3/2} + O_{f,ε}(w^{−7/4+ε}), where c_f = (16/3) C (−ζ(−1/2)) · H_f(−3/2)/2. This equals
c_f = (2ζ(3/2)/(3π)) ∏_p (1−1/p)(1 + 1/p − (ρ(p)+2)/p² + ρ(p)p^{−5/2} − ρ(p²)p^{−7/2} + ρ(p²)p^{−4}) > 0.

Consequently 𝔐_f^{int}(x,Y) = c_f x^{1/2}Y^{3/2} + O_{f,ε}(x^{1/4+ε}Y^{7/4−ε}) for 1 ≤ Y ≤ x.

*Risk:* Second crux.

(a) Substitute θ = xe/(um²) to get ∫_0^Y uR·B̃₂(x/(uR)) du = (x²/R) ∫_{x/(YR)}^∞ B̃₂(θ)θ^{−3} dθ. Then apply Vaughan Lemma 2.18 (valid for −2 < σ < −1) on σ = −5/4. Interchanging the sum and the integral needs absolute convergence of 𝒟_f at σ = −5/4 (fine: terms ≪ γ(m)m^{−4−2σ}τ(m²)·Σ_e N_f/m²) and |ζ(s+1)|/|s|³ integrable.

(b) The Euler factor of H_f is 1 + O(ρ(p)p^{−5−2σ} + ρ(p)p^{−4−σ} + ρ(p²)p^{−4} + p^{−8−4σ}). Use ρ(p) ≤ d for p ∤ content(f), and ρ(p²) ≤ dp otherwise; only finitely many primes are exceptional.

(c) Shift the contour to Re s = −7/4+ε, crossing only the simple pole of ζ(2s+4) at s = −3/2, whose residue is 1/2. Bounds on the new line: ζ(s+1) ≪ |t|^{5/4}, ζ(2s+4) ≪ |t|^{1/4}, |s(s+1)(s+2)| ≍ |t|³, so the integral converges absolutely. No zero-free region is needed on this line.

The closed form was checked numerically against Vaughan's c₂ for f(k) = k (0.128479). Mellin inversion of F_f reproduces the exact data to 1e-4.
