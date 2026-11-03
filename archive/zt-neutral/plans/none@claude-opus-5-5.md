# Plan: none@claude-opus-5-5

Model: claude-opus-5-5

PLAN: elementary dispersion and correlation method, one modulus at a time, then an average over the values f(k).

Step 1 (P3). Take one modulus q ≤ x and expand V(x;q) = Σ_l E(x;q,l)². The diagonal, the x²Σg² terms and the 'x·6/π²' terms cancel exactly against the main terms of the shifted correlations C(x,hq). What is left is an exact closed form M(x;q) = -2A_0 q Σ_e β(e) e_q B2*(x/(q e_q)), which is ≥0. Three error terms remain:
- the pointwise correlation error (P1), which totals x^{5/3}/q;
- Vaughan's (3.7)-type error for Σ_l Q·g against xΣg² (P2), which totals x^{3/2+ε}/q;
- Q(x) − 6x/π² = O(x^{1/2}).

Step 2 (P4, P5). Evaluate M(x;q) = 4A_0|ζ(-1/2)| κ(q) (xq)^{1/2}(1 + O((q/x)^{1/6})). Here κ is an explicit multiplicative factor that depends only on min(v_p(q),2). The constant comes from ∫_0^∞ B2*(u)u^{-3/2}du = 4ζ(-1/2), which I checked numerically to 12 digits. This is the analytic crux: a mean-value estimate plus van der Corput (Kusmin–Landau) for Σ_v w(v)B2(c/v²).

Step 3 (P6). Average κ(f(k)) with weight f'(k)f(k)^{1/2}. The local densities come from ρ(p) and ρ(p²).

Step 4 (P7). Assemble.

PREDICTED CONSTANT. C_f = (8/3)|ζ(-1/2)| Π_p λ_p(f), where λ_p = 1 − p^{-2} − (1−p^{-1})p^{-2}[2 + (1−p^{-1/2})(ρ(p) + ρ(p²)p^{-3/2})].

SANITY CHECKS.
1. For f(t)=t (weight 1, so V_f is the full variance) my formula gives 0.1284788, which matches Vaughan's c_2 = 8C_1|ζ(-1/2)|/(3ζ(2)²) = 0.1284788. The two Euler products agree to 8e-7 once truncated at p<2·10^5. This is independent confirmation of κ, A_0 and the B2* constant.
2. A direct check at x=10^6 for single moduli. Exact V(q) against my closed form M(q):
   - q=20000: 19791 vs 19872;
   - q=99991: 83097 vs 83220.
   - q=5003: within 1.3%.
   - q=101 and 1000: off by 15–20%. For small q the per-modulus error terms are relatively large.
   M(q) against the asymptotic 4A_0|ζ(-1/2)|κ(q)√(xq): the relative gap grows like about (q/x)^{1/4}, as expected.

COMPARISON WITH results.json. Predicted C_f:
- k²+1: 0.13808
- k³+2: 0.13561
- 2k+1: 0.14261

Operator extrapolations to r=Y/x→0:
- k²+1: 0.1345 ± 0.0073
- k³+2: 0.1363 ± 0.0024
- 2k+1: 0.1417 ± 0.0082

All three agree within the stated uncertainties. The raw normalised values at r≈0.01, x=2.56·10^8, are 0.14086, 0.13999, 0.14460, i.e. 2.0%, 3.2%, 1.4% above my constants. That fits the per-modulus correction of relative size (Y/x)^{1/4} to (Y/x)^{1/2} that I saw in the single-modulus check. The data's exponents (α+β = 2.000 at fixed ratio) match x^{1/2}Y^{3/2}.

There is no real discrepancy, with two caveats:
- (i) V_f/(x^{1/2}Y^{3/2}) tends to a non-constant function of r = Y/x (0.14 rising to 0.17–0.18 as r goes from 0.01 to 1). So the asymptotic with constant C_f can only hold for Y = o(x). The theorem states this, and its first error term has relative size (Y/x)^{1/6}.
- (ii) The operator's fitted correction model a√r + b·r is heuristic. The 2k+1 data are visibly bumpy in r because of B2*-type oscillation. So the extrapolation error bars, not my constant, are the soft part.

LIMITS OF THE PLAN.
- The range x^{7/9+δ} ≤ Y is set entirely by P1, which uses no averaging over h. Averaging the correlations over h and k with a circle-method argument (Vaughan 2005 §4, Brüdern–Wooley §3, the BGPVW 1998 minor-arc mean square) could plausibly push this to about x^{2/3}. I left that out because it needs power-saving minor-arc bounds for T_f(α) = Σ_k f'(k)Σ_h e(αhf(k)), which depend on d.
- P4 is stated with relative saving c^{-1/6} so that a plain van der Corput argument is enough. A Mellin argument using the zero-free region would give about (q/x)^{1/4}, but plain Mellin inversion of B2*(z)/z does not converge absolutely past Re s = 1/2, so I did not make it the contract.

COMPLIANCE.
- I did not search for, open, or use anything by the excluded author or the excluded 2015 paper.
- I did no web searches.
- Sources used:
  - the provided papers: R. C. Vaughan, 'A variance for k-free numbers in arithmetic progressions', PLMS 91 (2005); J. Brüdern–T. D. Wooley, 'Sparse variance for primes in arithmetic progression' (2011, provided); R. C. Vaughan, 'The Hardy–Littlewood Method', 2nd ed. (1997), Lemma 4.2;
  - standard facts: the Feller–Tornier correlation constant, and |ζ(-1/2)| = 0.2078862250.
- No result from 2011 or later was used apart from the provided Brüdern–Wooley paper.

## Main theorem

Let f ∈ Z[t] have degree d ≥ 1 with f(t) ≥ 2 and f'(t) ≥ 1 for t ≥ 1. Let ρ(m) = #{a mod m : f(a) ≡ 0 mod m}.

For each prime p put
λ_p(f) = 1 − p^{-2} − (1 − p^{-1}) p^{-2} [ 2 + (1 − p^{-1/2}) (ρ(p) + ρ(p²) p^{-3/2}) ].
Each λ_p(f) lies in (0,1], and λ_p(f) = 1 − (3+ρ(p))p^{-2} + O_f(p^{-5/2}), so the product Π_p λ_p(f) converges absolutely.

Define
C_f = (8/3) |ζ(−1/2)| Π_p λ_p(f), where |ζ(−1/2)| = 0.2078862250…

THEOREM. For every ε > 0 there is a constant B(f,ε) such that, for all real x ≥ 2 and y ≥ 1 with Y := f(y) ≤ x,
|V_f(x,y) − C_f x^{1/2} Y^{3/2}| ≤ B(f,ε) [ x^{1/3} Y^{5/3+ε} + x^{5/3} (log x)² + x^{1/2} Y^{3/2} y^{−1+ε} ].

Consequences:
- For each fixed δ ∈ (0, 1/10), V_f(x,y) = C_f x^{1/2} Y^{3/2} (1 + O_{f,δ}(x^{−δ/10})) uniformly for x^{7/9+δ} ≤ Y ≤ x^{1−δ}.
- The weight f'(k) and the class of f are unchanged from problem.md.
- For f(t) = t, C_f equals Vaughan's constant c_2 = 8 C_1 |ζ(−1/2)| / (3 ζ(2)²) ≈ 0.128479, where C_1 is Vaughan's constant (1.15) at k = 2.
- The restriction Y ≤ x^{1−δ} is genuine: V_f / (x^{1/2} Y^{3/2}) tends to a non-constant function of Y/x when Y ≍ x.

## Numerics check

Yes, within the numerical uncertainty.

Exponents: the operator's fixed-ratio slope is α+β = 2.0008 (k²+1), 1.998 (k³+2) and 2.0001 (2k+1), consistent with x^{1/2}Y^{3/2}.

Constants:

| f | predicted C_f | extrapolated r→0 | raw at r≈0.01, x=2.56e8 |
|---|---|---|---|
| k²+1 | 0.13808 | 0.1345 ± 0.0073 | 0.14086 |
| k³+2 | 0.13561 | 0.1363 ± 0.0024 | 0.13999 |
| 2k+1 | 0.14261 | 0.1417 ± 0.0082 | 0.14460 |

The raw values sit above the constants by 1.4–3.2%. This is consistent with a positive correction of order (Y/x)^{1/4} to (Y/x)^{1/2}; my own single-modulus check at x=10^6 shows the relative per-modulus correction behaving like about (q/x)^{1/4}.

The strong rise of the normalised value with r = Y/x (up to 0.171–0.184 at r = 1) is not a contradiction. The theorem is an asymptotic only for Y/x → 0.

Independent check of the constant: with f(t)=t my formula reproduces Vaughan's c_2 = 0.1284788 (PLMS 2005, (1.14)–(1.15)); the two Euler products agree to about 8e-7.

## P1: Uniform asymptotic for shifted squarefree correlations

Depends on: none  
Cites: none

Notation:
- μ is the Möbius function.
- A_0 := Π_p (1 − 2p^{-2}).
- For m ∈ N, A(m) := Π_p (1 − 2p^{-2}) · Π_{p: p² | m} (p² − 1)/(p² − 2).
- For squarefree e, β(e) := Π_{p|e} (p² − 2)^{-1}; β(e) := 0 if e is not squarefree.
- For real x ≥ 2 and integer m with 1 ≤ m ≤ x, C(x,m) := Σ_{1 ≤ n ≤ x−m} μ²(n) μ²(n+m). The sum is 0 if x − m < 1.

Claims:
(i) A(m) = A_0 Σ_{e ≥ 1, e² | m} β(e), and 0 < A(m) ≤ 1.
(ii) There is an absolute constant c_1 such that, for all real x ≥ 2 and all integers 1 ≤ m ≤ x,
|C(x,m) − A(m)(x − m)| ≤ c_1 x^{2/3} log x.

Suggested route: write μ²(n) = Σ_{d² | n} μ(d). Treat d, e ≤ z = x^{1/3} by counting in residue classes modulo [d², e²], which needs (d,e)² | m and gives an O(1) error each. Bound the terms with d > z or e > z trivially by Σ_{z < d ≤ √(2x)} (x/d² + 1). Complete the main-term series with tail O(z^{-1} log z).

*Risk:* Low; this is classical (Mirsky-type) and elementary. Care is needed for uniformity in m up to x, including n + m ≤ x, so that d, e range up to √x. This proposition alone fixes the lower end x^{7/9} of the theorem's range, because its error is summed over about x/q shifts per modulus with no cancellation.

## P2: Local densities and the linear term

Depends on: none  
Cites: Vaughan 2005, Lemma 2.2, Vaughan 2005, Lemma 2.3, Vaughan 2005, Lemma 2.4, Vaughan 2005, Lemma 2.17

Notation:
- μ² is the indicator of squarefree numbers.
- Q(x;q,l) := #{n ≤ x : n ≡ l (mod q), n squarefree}.
- g(q,l) := lim_{x→∞} Q(x;q,l)/x.
- τ is the divisor function.
- A_0 := Π_p (1 − 2p^{-2}).
- β(e) := μ²(e) Π_{p|e} (p² − 2)^{-1}.

Claims:
(a) For every q ∈ N and l ∈ Z the limit g(q,l) exists and depends on l only through gcd(l,q). Moreover 0 ≤ g(q,l) ≤ 1/q and Σ_{l=1}^q g(q,l) = 6/π². Explicitly, with m_p := min(2, v_p(q)),
g(q,l) = q^{-1} Π_{p ∤ q} (1 − p^{-2}) · Π_{p | q} (1 − 1[p^{m_p} | l] · p^{m_p − 2}).
(b) For every q ∈ N: q Σ_{l=1}^q g(q,l)² = A_0 Σ_{e ≥ 1} β(e) gcd(e², q)/e².
(c) A_0 Σ_{e ≥ 1} β(e) = 6/π².
(d) There is an absolute constant c_2 such that, for real x ≥ 2 and integers 1 ≤ q ≤ x,
|Σ_{l=1}^q Q(x;q,l) g(q,l) − x Σ_{l=1}^q g(q,l)²| ≤ c_2 τ(q)³ x^{1/2}/q.
(e) |Q(x;1,1) − 6x/π²| ≤ c_2 x^{1/2} for x ≥ 1.

*Risk:* Low. Vaughan's f(q,a) with k = 2 is our g(q,a), by his (1.2) and (1.4).

For (d), group l by r = gcd(l,q) and use Möbius over t | q/r. Then apply Lemma 2.2(ii), which needs rt ≤ q ≤ x; this holds. Lemma 2.3 turns the main term into x Σ_{r|q} g(q,r)² φ(q/r), and Lemma 2.4 identifies that with x Σ_l g(q,l)².

For (b), compare Euler factors at v_p(q) = 0, 1, ≥ 2. Alternatively, use Lemma 2.17 with G(p) = G(p²) = 1/(p² − 1). I checked the local factors by hand:
- v = 0 gives (p² − 1)²/p⁴;
- v = 1 gives ratio (p⁴ − 2p² + p)/(p² − 1)²;
- v ≥ 2 gives ratio (p⁴ − p²)/(p² − 1)².

## P3: Exact per-modulus decomposition of the variance (CRUX)

Depends on: P1, P2  
Cites: Vaughan 2005, Lemma 2.16

Notation:
- Q(x;q,l), g(q,l) and E(x;q,l) := Q(x;q,l) − g(q,l)x are as in problem.md.
- V(x;q) := Σ_{l=1}^q E(x;q,l)².
- B2*(u) := ({u}² − {u})/2, where {u} is the fractional part. So −1/8 ≤ B2*(u) ≤ 0, and B2*(u) = (u² − u)/2 for 0 ≤ u < 1.
- A_0 := Π_p (1 − 2p^{-2}), β(e) := μ²(e) Π_{p|e} (p² − 2)^{-1}, and A(m) := A_0 Σ_{e² | m} β(e).
- C(x,m) := Σ_{1 ≤ n ≤ x−m} μ²(n) μ²(n+m).
- For e, q ∈ N, e_q := e²/gcd(e², q).
- M(x;q) := −2 A_0 q Σ_{e ≥ 1} β(e) e_q B2*(x/(q e_q)).

Claims. For real x ≥ 2 and integers 1 ≤ q ≤ x:
(i) The series defining M(x;q) converges absolutely and M(x;q) ≥ 0.
(ii) The exact identity
V(x;q) = M(x;q) + [Q(x;1,1) − 6x/π²] + 2 Σ_{1 ≤ h ≤ x/q} [C(x,hq) − A(hq)(x − hq)] − 2x [Σ_l Q(x;q,l) g(q,l) − x Σ_l g(q,l)²]
holds.
(iii) Consequently, with an absolute constant c_3,
|V(x;q) − M(x;q)| ≤ c_3 ( x^{5/3} (log x)/q + x^{1/2} + τ(q)³ x^{3/2}/q ).

Key steps:
- Σ_l Q(x;q,l)² = Q(x;1,1) + 2 Σ_{h ≥ 1} C(x, hq).
- For H = x/q, Σ_{1 ≤ h ≤ H, e_q | h} (H − h) = e_q [ Z²/2 − Z/2 − B2*(Z) ] with Z = H/e_q.
- e² | hq if and only if e_q | h.
- The H² term equals x² Σ_l g(q,l)² by P2(b).
- The −H/2 term equals −(6/π²)x by P2(c).

*Risk:* The proof is algebraic, but this is where an error in sign or normalisation would destroy the main term. I verified the identity numerically: at x = 10^6, M(x;q) matches the exact V(x;q) to within 0.4% for q = 20000 and 99991, and to 1.3% for q = 5003.

Points to watch:
- absolute convergence when e_q > H (there each bracket is ≈ −H/2 · β(e), which is summable);
- the endpoint h = x/q when x is an integer (C(x,x) = 0 and A·0 = 0);
- error (iii) uses P1 for each of the ≤ x/q shifts.

## P4: Oscillatory sum over large squares (analytic crux) (CRUX)

Depends on: none  
Cites: Vaughan 1997 (The Hardy–Littlewood Method), Lemma 4.2

Notation:
- B2*(u) := ({u}² − {u})/2 and ψ(z) := B2*(z)/z for z > 0. Then |ψ(z)| ≤ min(1/2, 1/(8z)), and ψ(z) = (z − 1)/2 for 0 < z < 1.
- β(v) := μ²(v) Π_{p|v} (p² − 2)^{-1}.
- For q ∈ N, m_q := Π_{p | q} (1 − p^{-1}) · Π_{p ∤ q} (1 − p^{-1})(1 + p/(p² − 2)). This is the mean value lim_{T→∞} T^{-1} Σ_{v ≤ T, (v,q) = 1} v² β(v).
- For real c > 0, S_q(c) := Σ_{v ≥ 1, gcd(v,q) = 1} β(v) ψ(c/v²).
- ω(q) is the number of distinct prime factors of q.

Claims:
(i) ∫_0^∞ B2*(u) u^{-3/2} du = 4ζ(−1/2), where ζ(−1/2) = −0.2078862250…
(ii) There are absolute constants B_1, C_1 ≥ 1 such that, for all q ∈ N and all real c > 0,
|S_q(c) − 2ζ(−1/2) m_q c^{-1/2}| ≤ B_1 C_1^{ω(q)} c^{-1/2} min(1, c^{-1/6}).

Suggested route:
- The main term is m_q ∫_0^∞ t^{-2} ψ(c/t²) dt = m_q c^{-1/2} · (1/2) ∫_0^∞ B2*(u) u^{-3/2} du.
- Range v > √c: ψ is the polynomial (c/v² − 1)/2. Use partial summation with Σ_{v ≤ T, (v,q)=1} v² β(v) = m_q T + O(C^{ω(q)} T^{1/2}).
- Range v ≤ √c: write B2* = −1/12 + Σ_{n ≥ 1} cos(2πnu)/(2π² n²), which converges absolutely. Decompose v² β(v) 1_{(v,q)=1} as a convolution of 1 with a sparse, absolutely summable weight. On each smooth block, use the Kusmin–Landau / van der Corput first-derivative step: Σ e(F) = ∫ e(F) + O(1) where |F'| ≤ 1/2. Bound the remaining range trivially. This loses O((nc)^{1/3} L^{-2/3}) per block, giving a total error O(C^{ω(q)} c^{1/3}) inside the bracket, which becomes c^{-2/3} after dividing by c.

*Risk:* This is the real analytic difficulty.
- The obvious Mellin approach fails: the Mellin transform of ψ, Φ(1 − s) = ζ(−s)/(s(1 − s)) up to sign, decays only like |t|^{σ − 3/2}. So the inversion is not absolutely convergent once Re s ≥ 1/2, and one cannot shift past the main pole without smoothing or truncation. That is why the contract asks only for c^{-1/6} relative saving and allows the elementary exponential-sum route.
- Weaker exponents (anything c^{-1/2 − η} with η > 0) would still give an asymptotic, with a smaller range near Y ≍ x.
- I verified identity (i) numerically to 12 digits.
- Uniformity in q enters only through Π_{p|q} factors, which is why the bound has C_1^{ω(q)}.

## P5: Per-modulus main term

Depends on: P4  
Cites: none

Notation:
- A_0 := Π_p (1 − 2p^{-2}) = 0.32263…
- β(e) := μ²(e) Π_{p|e} (p² − 2)^{-1}.
- e_q := e²/gcd(e², q).
- B2*(u) := ({u}² − {u})/2.
- M(x;q) := −2 A_0 q Σ_{e ≥ 1} β(e) e_q B2*(x/(q e_q)).
- κ(q) := Π_p κ_p(min(2, v_p(q))), where κ_p(j) := (1 − p^{-1})(1 + p^{1 − j/2}/(p² − 2)) for j = 0, 1, 2. The product converges absolutely because κ_p(0) = 1 + O(p^{-2}). One has 0 < κ(q) ≤ Π_p κ_p(0) · Π_{p|q} (κ_p(1)/κ_p(0)).
- ω(q) is the number of distinct prime factors of q.

Claim. There are absolute constants B_2, C_2 ≥ 1 such that, for real x ≥ 2 and integers 1 ≤ q ≤ x,
|M(x;q) − 4 A_0 |ζ(−1/2)| κ(q) x^{1/2} q^{1/2}| ≤ B_2 C_2^{ω(q)} x^{1/3} q^{2/3}.

Route:
- M(x;q) = −2 A_0 x Σ_e β(e) ψ(x gcd(e², q)/(q e²)), with ψ(z) = B2*(z)/z.
- Write e = uv with u squarefree, every prime factor of u dividing q, and gcd(v,q) = 1.
- Then M(x;q) = −2 A_0 x Σ_u β(u) S_q(c_u), with c_u := x gcd(u², q)/(q u²) and S_q as in P4.
- Apply P4 to each u and sum over u, using β(u) u ≤ 2/u.
- Check the identity m_q Σ_{u | rad q} u² β(u) u^{-1} gcd(u², q)^{-1/2} = κ(q) prime by prime.

*Risk:* Mainly bookkeeping:
- c_u can be < 1 for large u, and P4 must cover all c > 0 (it does, via the min(1, c^{-1/6}) factor);
- Σ_{u | rad q} of the error terms must give only C^{ω(q)} losses.

Numerically, M(q)/(4A_0|ζ(−1/2)|κ(q)√(xq)) at x = 10^6 is 0.987, 0.977, 0.93, 0.917, 1.10 for q = 101, 1000, 5003, 20000, 99991. That is consistent with a relative error of order (q/x)^{1/4} to (q/x)^{1/6}.

## P6: Averaging κ over polynomial values

Depends on: none  
Cites: Brüdern–Wooley 2011, Lemma 2

Notation:
- f ∈ Z[t] has degree d ≥ 1, with f(t) ≥ 2 and f'(t) ≥ 1 for t ≥ 1.
- ρ(m) := #{a mod m : f(a) ≡ 0 (mod m)}.
- κ(q) := Π_p κ_p(min(2, v_p(q))), with κ_p(j) := (1 − p^{-1})(1 + p^{1 − j/2}/(p² − 2)).
- A_0 := Π_p (1 − 2p^{-2}).
- λ_p(f) := 1 − p^{-2} − (1 − p^{-1}) p^{-2} [2 + (1 − p^{-1/2})(ρ(p) + ρ(p²) p^{-3/2})].

Claims:
(i) 0 < λ_p(f) ≤ 1 for every p, and Π_p λ_p(f) converges absolutely.
(ii) For each p, λ_p(f) = (1 − 2p^{-2}) · [ (1 − ρ(p)/p) κ_p(0) + (ρ(p)/p − ρ(p²)/p²) κ_p(1) + (ρ(p²)/p²) κ_p(2) ].
(iii) For every ε > 0 there is B(f,ε) such that, for all real y ≥ 1, with Y := f(y),
|Σ_{1 ≤ k ≤ y} f'(k) f(k)^{1/2} κ(f(k)) − (2/3) A_0^{-1} (Π_p λ_p(f)) Y^{3/2}| ≤ B(f,ε) Y^{3/2} y^{-1+ε}.

Route:
- Write κ = κ_∞ · (1 ∗ η), where κ_∞ = Π_p κ_p(0), and η is multiplicative, supported on cube-free m, with |η(p)|, |η(p²)| ≪ 1/p.
- Interchange the sums.
- For each m ≤ Y, count k ≤ y with m | f(k) in ρ(m) residue classes. Euler summation in progressions gives an error O(f'(y) Y^{1/2}) per class (compare Brüdern–Wooley 2011, Lemma 2).
- Complete the sum over m. The tail is O(Y^{-1/2+ε}), and Σ_{m ≤ Y} |η(m)| ρ(m) ≪ Y^ε.

*Risk:* Moderate bookkeeping:
- ρ(p^j) can be as large as p^j when p^j divides the content of f. This affects only finitely many p, but the bounds ρ(m) ≪_f m^ε (for cube-free m) and the absolute convergence must handle it.
- Identity (ii) was checked numerically for random (p, ρ(p), ρ(p²)).
- Euler summation needs g(t) = f'(t) f(t)^{1/2} with ∫ |g'| ≪ f'(y) Y^{1/2}. This holds because f' and f are eventually monotone; the finite initial segment goes into B(f,ε).

## P7: Main theorem: assembly

Depends on: P3, P5, P6  
Cites: none

Let f ∈ Z[t] have degree d ≥ 1, with f(t) ≥ 2 and f'(t) ≥ 1 for t ≥ 1. Let ρ(m) := #{a mod m : f(a) ≡ 0 mod m}, and put
λ_p(f) := 1 − p^{-2} − (1 − p^{-1}) p^{-2} [2 + (1 − p^{-1/2})(ρ(p) + ρ(p²) p^{-3/2})],
C_f := (8/3) |ζ(−1/2)| Π_p λ_p(f).
Let V_f(x,y) be as in problem.md.

Claim. For every ε > 0 there is B(f,ε) such that, for all real x ≥ 2 and y ≥ 1 with Y := f(y) ≤ x,
|V_f(x,y) − C_f x^{1/2} Y^{3/2}| ≤ B(f,ε) [ x^{1/3} Y^{5/3+ε} + x^{5/3} (log x)² + x^{1/2} Y^{3/2} y^{-1+ε} ].
In particular, V_f(x,y) ~ C_f x^{1/2} Y^{3/2} uniformly for x^{7/9+δ} ≤ Y ≤ x^{1−δ}, for any fixed δ > 0.

Route:
- V_f(x,y) = Σ_{k ≤ y} f'(k) V(x; f(k)), since f is increasing on [1,∞) and f(k) ≤ Y ≤ x.
- Apply P3 and P5 to each q = f(k).
- Sum the errors with τ(n), C^{ω(n)} ≪_ε n^ε and with Σ_{k ≤ y} f'(k)/f(k) ≤ log Y + O_f(1).
- Apply P6 to the main terms 4 A_0 |ζ(−1/2)| κ(f(k)) x^{1/2} f(k)^{1/2}.
- Note that 4 A_0 |ζ(−1/2)| · (2/3) · A_0^{-1} Π_p λ_p(f) = C_f.

*Risk:* Low, provided the dependencies hold. Things to check:
- the diagonal error Σ_k f'(k) x^{1/2} ≤ Y x^{1/2} ≤ x^{3/2};
- the linear-term error, which totals x^{3/2+ε};
- that Σ_k f'(k) C^{ω(f(k))} f(k)^{2/3} ≪_ε Y^{5/3+ε}.
The exponent 7/9 comes from x^{5/3} (log x)² ≤ x^{1/2} Y^{3/2} x^{-δ'}.
