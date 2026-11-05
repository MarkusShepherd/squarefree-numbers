# Plan: thesis

Model: claude-opus-5-5

STRATEGY. Combine Vaughan (2005) with Brüdern–Wooley (2011).
(i) Open the square in each modulus q=f(k). The cross term and the square term are evaluated exactly with Vaughan's identities (Lemmas 2.2(ii), 2.3, 2.4, 2.17). This leaves the correlation sum S_f = Σ_k f'(k) Σ_h Σ_n μ²(n)μ²(n+hf(k)) = ∫|F|²T_f, where T_f(α) = Σ_k f'(k) Σ_{h≤x/f(k)} e(αhf(k)) is the Brüdern–Wooley generating function.
(ii) Apply Vaughan's circle-method dissection with R=x^{3/5} and major arcs q≤P=x^{2/5}. Use Vaughan's Lemmas 2.6–2.8 (squarefree exponential-sum bounds from BGPVW) and only the trivial bound |T_f|≤x log x. The three error terms (minor arcs, |Δ|², f*Δ) balance exactly at x^{9/5+ε}.
(iii) On the major arcs, the singular series turns the main term into Σ_k f'(k)Σ_h 𝔖(hf(k))(x−hf(k)). Vaughan's B̃_2 computation, done one modulus at a time, gives an exact identity. Its x² part cancels the square term and its x part cancels the diagonal Q(x). Hence V_f = A_f + O(x^{9/5+ε}), where A_f = Σ_k f'(k)Ψ(x;f(k)) and Ψ(x;u) = C_0 Σ_m γ(m) lcm(u,m²) ψ(x/lcm(u,m²)) with ψ(θ) = {θ}(1−{θ}).
(iv) Arithmetic part, the new ingredient compared with Vaughan:
- Average Ψ over the sparse moduli. For m ≤ M=√y, use residue classes mod m² and Euler–Maclaurin as in Brüdern–Wooley (22).
- For m > M, use the exact form x − x²/L of Λ when L ≥ x, plus a gcd/ρ bound. Small k are cut off with an a priori bound.
- Evaluate the averaged main term by Mellin inversion, using Vaughan's Lemma 2.18 with a generalised Euler product. The constant enters through the local distribution of (f(k),p²), i.e. through ρ(p) and ρ(p²).

RANGE. The circle-method error x^{9/5+ε} forces f(y) ≥ x^{13/15+ε}. The arithmetic error forces yf(y) ≥ x^{1+ε}, i.e. f(y) ≥ x^{d/(d+1)+ε}, which only binds for d ≥ 7. The secondary term x^{1/4+η}f(y)^{7/4−η} requires f(y)=o(x), as in Vaughan's theorem. The 13/15 comes entirely from the trivial sup bound for T_f. A Weyl-type minor-arc bound for T_f, or a q-dependent bound on the major arcs, would enlarge the range; I did not plan this because it is messy and risky. Restriction (H), that f has no repeated factor, is used only in P7 to get ρ(e) ≪ e^ε for e | m² with m squarefree. All three test polynomials satisfy it.

CONSISTENCY CHECKS.
- For f(t)=t the Euler product reduces symbolically to Vaughan's c_2, using −8ζ(−1/2) = ∫_0^∞ψ(θ)θ^{−5/2}dθ, which I checked numerically to 1e-6.
- I computed A_f(x,y) directly (scripts/check_A.py) at x=10^6 and compared it with the exact V in results.json, for y ≤ 20000 only. That covers every listed f(y)/x from 0.01 to 1 for k²+1 and k³+2, but only 0.01 and 0.02 for 2k+1. In every checked row the relative difference is at most 1.4e-3. This supports the reduction V_f ≈ A_f (P1–P5) numerically.
- In the checked rows, the rise of V/(x^{1/2}f(y)^{3/2}) with f(y)/x is already present in A_f. So it is the arithmetic secondary term of P8/P9, not a defect.
- A first run that also included the large-y rows for 2k+1 was too slow and was stopped at its time limit; it produced no results and nothing relies on it.

SOURCES. Only files in papers/ were used: Vaughan, PLMS 91 (2005) 573–597; Brüdern–Wooley, QJM 62 (2011) 289–305; BGPVW 1998 through Vaughan's Lemmas 2.6–2.8. No web searches were made. No excluded author, excluded paper, GitLab, prior write-up or prior run was encountered or used.

## Main theorem

Let f ∈ Z[t] be as in problem.md: degree d ≥ 1, f(t) ≥ 2 and f'(t) ≥ 1 for real t ≥ 1. Assume in addition:

(H) f has no repeated irreducible factor in Q[t].

Notation:
- ρ(m) = #{a mod m : f(a) ≡ 0 (mod m)}.
- For each prime p, e_p = 1 − ρ(p)/p + (ρ(p)/p − ρ(p²)/p²)p^{−1/2} + ρ(p²)p^{−3}.
- C_f = −(8/3)ζ(−1/2) Π_p (1 − 1/p)(1 − 2/p² + e_p/p).

The product converges absolutely and C_f > 0.

Then for every ε > 0 and every η ∈ (0,1/8], uniformly for real x ≥ 2 and real y ≥ 1 with f(y) ≤ x (the sum runs over integers 1 ≤ k ≤ y):

V_f(x,y) = C_f x^{1/2} f(y)^{3/2} + O_{f,ε,η}( x^{9/5+ε} + x^{1+ε} f(y) y^{−1/2} + x^{1/4+η} f(y)^{7/4−η} ).

Hence V_f(x,y) ~ C_f x^{1/2} f(y)^{3/2} as x → ∞ whenever f(y)/x → 0 and f(y) ≥ x^{max(13/15, d/(d+1))+δ} for some fixed δ > 0.

## Numerics check

Yes.

Exponents: the fixed-ratio fits give α+β ≈ 2.000 for all three polynomials, as predicted.

Constant: the operator's extrapolations to f(y)/x → 0 compare with the predicted C_f as follows.

| f | extrapolated | predicted C_f |
|---|---|---|
| k²+1 | 0.1345 ± 0.0073 | 0.1381 |
| k³+2 | 0.1363 ± 0.0024 | 0.1356 |
| 2k+1 | 0.1417 ± 0.0082 | 0.1426 |

All three agree within the stated uncertainty.

Independent check: I computed A_f directly at x = 10^6 for y ≤ 20000. This covers every listed f(y)/x from 0.01 to 1 for k²+1 and k³+2, but only 0.01 and 0.02 for 2k+1. In every checked row A_f matches the exact V in results.json to relative error at most 1.4e-3. In the checked rows the roughly 20% rise of V/(x^{1/2}f(y)^{3/2}) with f(y)/x is reproduced by A_f, so it is the arithmetic secondary term, not a failure. The fixed-x estimate β ≈ 1.545 is biased by that same term. No discrepancy was found.

## P1: Opening the square

Depends on: none  
Cites: Vaughan 2005, Lemma 2.2, Vaughan 2005, Lemma 2.3, Vaughan 2005, Lemma 2.4

Notation:
- f is as in problem.md.
- Q(x) := #{n≤x squarefree}.
- σ2(q) := Σ_{l=1}^q g(q,l)².
- S_f(x,y) := Σ_{1≤k≤y} f'(k) Σ_{h≥1} Σ_{1≤n≤x−hf(k)} μ²(n)μ²(n+hf(k)).

Claim. For every ε>0, uniformly for x≥2 and y≥1 with f(y)≤x:
V_f(x,y) = 2S_f(x,y) + Σ_{k≤y} f'(k)[Q(x) − x²σ2(f(k))] + O_{f,ε}(x^{3/2+ε}).

Key step: for every integer 1≤q≤x, Σ_l Q(x;q,l)g(q,l) = xσ2(q) + O_ε(x^{1/2+ε}/q).

Useful facts: g(q,l) = Σ_{m≥1, (m²,q)|l} μ(m)(m²,q)/(m²q), and 0 ≤ g(q,l) ≤ 1/q.

*Risk:* Low. Follow Vaughan's (3.5)–(3.7) for a single q, using Lemma 2.2(ii) (needs q ≤ x).

## P2: Circle method: minor arcs and Δ-terms

Depends on: none  
Cites: Vaughan 2005, Lemma 2.5, Vaughan 2005, Lemma 2.6, Vaughan 2005, Lemma 2.7, Vaughan 2005, Lemma 2.8

Notation:
- F(α) = Σ_{n≤x} μ²(n)e(αn) and I(β) = Σ_{1≤n≤x} e(βn).
- T_f(α) = Σ_{k≤y} f'(k) Σ_{1≤h≤x/f(k)} e(αhf(k)).
- G is multiplicative with G(p) = G(p²) = −1/(p²−1) and G(p^t) = 0 for t≥3; ν(q) = G(q)/ζ(2).
- R = x^{3/5} and P = x^{2/5}.

Claim. S_f = ∫_0^1 |F|²T_f, and uniformly for x≥2 and y≥1 with f(y)≤x:
S_f = Σ_{q≤P} ν(q)² Σ_{(a,q)=1} ∫_{|β|≤1/(qR)} |I(β)|² T_f(a/q+β) dβ + O_{f,ε}(x^{9/5+ε}).

Use only |T_f| ≤ T_f(0) ≪ x log x, together with Vaughan's Lemmas 2.6 (k=2), 2.7 and 2.8 (T=P).

*Risk:* Low to moderate. Check the lemma hypotheses (2√x ≤ R ≤ x and T ≤ √x/2) and that the minor arcs are contained in Lemma 2.6's set. The three error terms balance exactly at x^{9/5}.

## P3: Major arcs: completion to the singular series

Depends on: none  
Cites: Vaughan 2005, Lemma 2.14, Vaughan 2005, Lemma 2.15, Vaughan 2005, (6.1)

Notation:
- γ(m) = μ²(m)Π_{p|m}(p²−2)^{−1} and C_0 = Π_p(1−2/p²).
- 𝔖(n) = Σ_q ν(q)²c_q(n) = C_0 Σ_{m²|n} γ(m).
- M_f = Σ_{k≤y} f'(k) Σ_{h≤x/f(k)} 𝔖(hf(k))(x−hf(k)).

Claim. The major-arc sum of P2 equals M_f + O_f(x^{9/5}(log 2x)³), uniformly for f(y) ≤ x.

Steps: extend β to [−1/2,1/2]; extend q to all q≥1 using Σ_{y<q≤2y} qν(q)² ≪ y^{−1/2}log²(2y); then apply orthogonality.

*Risk:* Low.

## P4: Per-modulus identity

Depends on: none  
Cites: Vaughan 2005, Lemma 2.16, Vaughan 2005, Lemma 2.17, Vaughan 2005, (6.8)

Notation:
- ψ(θ) = {θ}(1−{θ}) and Λ_x(L) = Lψ(x/L).
- Ψ(x;u) = C_0 Σ_m γ(m) Λ_x(lcm(u,m²)).
- 𝔖, γ and C_0 are as in P3; σ2 is as in P1.

Claim. For every integer u≥1 and real x>0, exactly:
Σ_{1≤h≤x/u} 𝔖(hu)(x−hu) = x²σ2(u)/2 − x/(2ζ(2)) + Ψ(x;u)/2.

Uses: C_0Σγ = 1/ζ(2); C_0 Σ_m γ(m)/lcm(u,m²) = σ2(u); and Vaughan's Lemma 2.16.

*Risk:* Low. Sign convention: B̃2 = −ψ/2. Checked numerically.

## P5: Reduction V_f = A_f + O(x^{9/5+ε})

Depends on: P1, P2, P3, P4  
Cites: Montgomery–Vaughan 2007, Ch. 2

With A_f(x,y) = Σ_{k≤y} f'(k)Ψ(x;f(k)) (Ψ as in P4): uniformly for x≥2 and y≥1 with f(y)≤x,
V_f(x,y) = A_f(x,y) + O_{f,ε}(x^{9/5+ε}).

*Risk:* Low: bookkeeping only.

## P6: A priori bound

Depends on: none  
Cites: none

For x≥1 and integers u≥1: 0 ≤ Ψ(x;u) ≤ c_0(xu)^{1/2}, with c_0 absolute.

Hence Σ_{k≤y'} f'(k)Ψ(x;f(k)) ≤ c_f x^{1/2}f(y')^{3/2}.

*Risk:* Very low.

## P7: Transfer from sparse moduli to the averaged local distribution (CRUX)

Depends on: none  
Cites: Brüdern–Wooley 2011, Lemma 2, Brüdern–Wooley 2011, (22)

Assume (H): f has no repeated irreducible factor.

Definition. 𝓜_f(x,T) = C_0 Σ_m γ(m) m^{−2} Σ_{r mod m²} ∫_0^T Λ_x(τm²/(f(r),m²)) dτ.

Claim. Uniformly for f(y) ≤ x, 1 ≤ y_1 ≤ y and 1 ≤ M ≤ x:
Σ_{y_1<k≤y} f'(k)Ψ(x;f(k)) = 𝓜_f(x,f(y)) − 𝓜_f(x,f(y_1)) + O_{f,ε}(M x y^{d−1} log 2x + x²M^ε[(y/y_1)M^{−3} + (y_1M)^{−1}]).

Method: for m ≤ M, residue classes mod m² plus Euler summation; for m > M, Λ_x(L) = x − x²/L when L ≥ x, plus a gcd/ρ bound.

*Risk:* Bookkeeping for m > M where (f(k),m²) is large. Needs ρ(e) ≪ e^ε, which uses (H). Euler summation must handle a piecewise-C¹ function.

## P8: Mellin evaluation (CRUX)

Depends on: none  
Cites: Vaughan 2005, Lemma 2.18, Vaughan 2005, Lemma 2.19

Assume (H); C_f is as in the main theorem.

Claim. For η ∈ (0,1/8], uniformly for x≥1 and 0 < T ≤ x:
𝓜_f(x,T) = C_f x^{1/2}T^{3/2} + O_{f,η}(x^{1/4+η}T^{7/4−η}).

Method: Vaughan's Lemma 2.18 for Ξ(z) = ∫_z^∞ ψθ^{−3}; factor the Dirichlet series as ζ(4+2s)·𝒢̃_f(s); shift the contour to σ = −7/4+η.

*Risk:* Signs and normalisation; analytic continuation of the Euler product; vertical growth of ζ.

## P9: Asymptotic for A_f

Depends on: P6, P7, P8  
Cites: none

Claim. Uniformly for x≥2 and y≥1 with f(y)≤x:
A_f = C_f x^{1/2}f(y)^{3/2} + O_{f,ε,η}(x^{1+ε}f(y)y^{−1/2} + x^{1/4+η}f(y)^{7/4−η}).

Parameter choice: w = yf(y)/x, M = √y, and f(y_1) = f(y)w^{−1/3}. The case w < 1 is trivial.

*Risk:* Low: parameter bookkeeping.
