# Plan: simplest@claude-opus-5-5

Model: claude-opus-5-5

I took the simplest route I could make fully rigorous. It is elementary and avoids the circle method; the price is a weaker range. The steps:

1. Open the square for each single modulus q. Then Σ_l Q(x;q,l)² equals Q(x) plus twice a sum over j < x/q of the pair-correlation counts C(x, jq).
2. Estimate each C(x,h) with a simple Mirsky-type argument: C(x,h) = A(h)(x−h) + O(x^{3/4}), uniformly in h. This uses only the trivial bound |E(t;q,l)| ≪ t^{1/2}.
3. Sum the main terms A(jq)(x−|j|q) over j exactly. The terms of order x² cancel; I proved this by a limit argument with q fixed and x → ∞. What remains is an explicit sawtooth sum:
   M(x,q) = q·Σ_c μ²(c)P(c)(m_c/c²)·B(x/(q·m_c)), with B(t) = {t}(1−{t}).
4. A one-variable lemma, Σ_n B(Z/n²) = −4ζ(−1/2)·Z^{1/2} + O(Z^{1/3}), gives M(x,q) = Φ_∞·h(q)·x^{1/2}q^{1/2} + O(x^{1/3}q^{2/3+ε}). Here h(q) is an explicit product over p | q whose factor depends on whether p ∥ q or p² | q.
5. Average h(f(k)) over k by a divisor-sum expansion. This produces the factor 𝔖_f, which involves ρ(p) and ρ(p²).

The x^{3/4} pair-correlation error costs x^{7/4}/q per modulus. That limits the theorem to x^{5/6+δ} ≤ f(y) ≤ x^{1−δ}. A uniform Mirsky bound of x^{2/3+ε} would widen this to x^{7/9+δ}; I left that out to keep things simple.

**Checks:**
- For f(k) = k, the constant (2/3)Φ_∞·𝔖 = 0.1284788 equals Vaughan's c₂ from (1.14)–(1.15) of Vaughan 2005 (0.1284787) to truncation accuracy.
- Exact single-modulus variances at x = 10⁶ match M(x,q) within 0.3% for q ≥ 10⁴.
- The intermediate formula Σ_k f'(k)·M(x, f(k)) matches the exact V in results.json to 1e−3 or better. This holds at ratios 0.01, 0.1 and 1 for k²+1, and at 0.01 and 0.1 for 2k+1. So the reduction is numerically confirmed even where f(y) is close to x.
- **No discrepancy with the data:** all three predicted constants fall inside the data's extrapolation envelopes (see `agrees_with_numerics`).

**Sources and rule compliance:**
- No source by the excluded author (Schepke/Shepherd) and not Dehnert's paper was searched for, encountered or used.
- Two web searches (for Hooley 1975 and Blomer 2008) returned only post-2010 papers: arXiv:1402.0684, arXiv:1411.2360 and arXiv:2006.04060. I did not open them and used nothing from them or their snippets.
- External literature cited:
  - L. Mirsky, "Arithmetical pattern problems relating to divisibility by rth powers", Proc. London Math. Soc. (2) 50 (1949) 497–508 — for orientation only. P2 is to be proved self-contained.
  - Montgomery–Vaughan 2007, Theorem 1.12.
  - Vaughan 2005, main Theorem — used only as a consistency check.

## Main theorem

Setting: f is as in problem.md (integer-valued, degree d ≥ 1, f(t) ≥ 2 and f'(t) ≥ 1 for t ≥ 1).

Definitions:
- D_f is the least positive integer with D_f·f ∈ Z[t].
- ρ*(m) := D_f^{−1}·#{a mod m·D_f : f(a) ≡ 0 (mod m)}. This equals ρ(m) when f ∈ Z[t].
- C_f := −(8/3)·ζ(−1/2)·∏_p (1 − 1/p)·(1 + 1/p − 2/p² − ρ*(p)·(p^{−2} − p^{−5/2}) − ρ*(p²)·(p^{−7/2} − p^{−4})). The product converges absolutely and C_f > 0.

THEOREM. For every ε > 0, all real x ≥ 2 and y ≥ 1 with f(y) ≤ x:

V_f(x,y) = C_f·x^{1/2}·f(y)^{3/2} + O_{f,ε}( x^{1/2}f(y)^{3/2}·y^{−1/5} + x^{1/3+ε}·f(y)^{5/3} + x^{7/4+ε} ).

In particular, if y → ∞ with x^{5/6+δ} ≤ f(y) ≤ x^{1−δ} for some fixed δ > 0, then V_f(x,y) ~ C_f·x^{1/2}·f(y)^{3/2}.

Supplement, valid for all f(y) ≤ x including f(y) ≍ x:

V_f(x,y) = Σ_{k≤y} f'(k)·M(x, f(k)) + O_f(x^{7/4}·log 2x),

with M as defined in P3. The weight f'(k) and the class of f are unchanged from problem.md.

## Numerics check

Yes.

**Exponents.** The fitted exponent sum α+β is 2.0006, 2.0005 and 2.00005; theory gives 2. The fixed-x slope β ≈ 1.54–1.55 instead of 1.5 is explained by the secondary term. The normalised values rise from about 0.141 at ratio 0.01 to about 0.17 at ratio 1. This matches the supplement: Σ f'(k)·M(x, f(k)) is not a pure power when f(y) ≍ x.

**Constants (small-ratio extrapolation vs prediction):**

| f | data | prediction | difference |
|---|---|---|---|
| k²+1 | 0.13837 ± 0.0070 | 0.13808 | 0.0003 |
| k³+2 | 0.13851 ± 0.0073 | 0.13561 | 0.0029 |
| 2k+1 | 0.14086 ± 0.0082 | 0.14261 | 0.0018 |

All differences are inside the reported sensitivity envelopes.

**Direct check of the reduction.** I computed Σ_{k≤y} f'(k)·M(x, f(k)) independently at x = 10⁶. Values (V_data in parentheses):
- k²+1:
  - y = 99: 1.37480e8 (1.37662e8)
  - y = 316: 4.79318e9 (4.79358e9)
  - y = 999: 1.708387e11 (1.708490e11)
- 2k+1:
  - y = 4999: 1.44546e8 (1.44371e8)
  - y = 49999: 4.95490e9 (4.95521e9)

The relative differences are at most 1.3e−3. So the remaining gaps between the extrapolated and predicted constants come from extrapolating in the ratio, not from the theory. For k³+2 the extra effect of the small y (y ≈ 136–634) is also relevant; this is the y^{−1/5} term. Single-modulus checks of S(x,q) against M(x,q) at x = 10⁶ agree within 0.3% for q ≥ 10⁴.

## P1: Uniform elementary facts on squarefree numbers in progressions

Depends on: none  
Cites: Vaughan 2005, (1.2) and (1.4)

Notation: μ²(n) is the squarefree indicator; Q(x;q,l), g(q,l), E(x;q,l) are as in problem.md; Q(x) := Q(x;1,0); τ is the divisor function; v_p is the p-adic valuation. For q ≥ 1 put t_p := p^{min(2, v_p(q))} for p | q, and q* := ∏_{p|q} t_p.

(a) For all integers q ≥ 1 and l:
  g(q,l) = Σ_{m≥1} μ(m)·gcd(m²,q)·1[gcd(m²,q) | l] / (m²·q)
         = (6/π²)·q^{−1}·∏_{p|q} (1 − 1[t_p | l]·t_p·p^{−2})·(1 − p^{−2})^{−1}.
  Consequently 0 ≤ g(q,l) ≤ 1/q, and g(q,l) depends on l only through gcd(l, q*).

(b) There is an absolute constant C_0 such that |E(t;q,l)| ≤ C_0·t^{1/2} for all real t ≥ 1 and all integers q ≥ 1 and l. In particular Q(x) = 6x/π² + O(x^{1/2}).

(c) There is an absolute constant C_1 such that for all real x ≥ 1 and integers q ≥ 1:
  |Σ_{l=1}^{q} g(q,l)·E(x;q,l)| ≤ C_1·τ(q)²·x^{1/2}/q.

*Risk:* Low. For (b), expand μ²(n) = Σ_{d²|n} μ(d). For d ≤ t^{1/2}, the count of m ≤ t/d² with d²m ≡ l (mod q) equals 1[h_d | l]·t·h_d/(d²q) + O(1), where h_d = gcd(d²,q). The tail of the main term over d > t^{1/2} is ≤ Σ_{d>√t} t/d². For (c), sort l by r = gcd(l,q*) and apply Möbius inversion over divisors s of q*/r. Each sum Σ_{l≡0 (mod t)} E(x;q,l) equals #{n ≤ x squarefree, t | n} − x·(its density), which is O(x^{1/2}) uniformly in t by the argument of (b). Watch that g(q,l) is defined for all l, not only for gcd(l,q) = 1.

## P2: Uniform pair correlation of squarefree numbers (Mirsky type)

Depends on: P1  
Cites: none

For an integer h ≥ 0 and real x put C(x,h) := #{n ∈ N : n + h ≤ x, μ²(n) = μ²(n+h) = 1}. In particular C(x,0) = Q(x).

Define A(h) := Σ_{a,b≥1} μ(a)μ(b)·1[gcd(a,b)² | h] / lcm(a,b)². The series converges absolutely, and A(h) = Σ_{a≥1} μ(a)·g(a², h), with g as in problem.md. Also A(0) = 6/π².

There is an absolute constant C_2 such that for every real x ≥ 2 and every integer h with 0 ≤ h < x:
  |C(x,h) − A(h)·(x − h)| ≤ C_2·x^{3/4}.

*Risk:* Low to moderate; the main danger is losing uniformity in h. Suggested proof: write μ²(n) = Σ_{a²|n, a≤z} μ(a) + Σ_{a²|n, a>z} μ(a) with z = x^{1/4}.
- The a > z part contributes at most Σ_{a>z} x/a² ≪ x/z, counting with multiplicity and bounding μ²(n+h) ≤ 1.
- For a ≤ z, the inner count is #{squarefree n' ∈ (h, x] : n' ≡ h (mod a²)} = Q(x;a²,h) − Q(h;a²,h). By P1(b) this is g(a²,h)·(x − h) + O(x^{1/2}).
- Completing Σ_{a≤z} μ(a)·g(a²,h) to A(h) costs x·Σ_{a>z} a^{−2}, by P1(a).
Note Q(h;·) = 0 when h < 1. Mirsky (Proc. LMS 1949) gives x^{2/3+ε} for fixed h. That is not needed, and its uniformity in h must not be assumed.

## P3: Single-modulus reduction of the variance to an explicit sawtooth sum (CRUX)

Depends on: P1, P2  
Cites: none

Notation:
- B(t) := {t}·(1 − {t}) for real t.
- For squarefree c, P(c) := ∏_{p∤c} (1 − 2p^{−2}).
- For integers c, q ≥ 1, m_c(q) := c²/gcd(c², q).
- For real x > 0 and integer q ≥ 1:
    M(x,q) := q·Σ_{c≥1} μ²(c)·P(c)·(m_c(q)/c²)·B(x/(q·m_c(q))).
  The series converges absolutely since B(t) ≤ min(1/4, t).
- S(x,q) := Σ_{l=1}^{q} E(x;q,l)², with E as in problem.md.

Claim. There is an absolute constant C_3 such that for every integer q ≥ 1 and real x ≥ max(2, q):
  |S(x,q) − M(x,q)| ≤ C_3·(x^{7/4}/q + x^{1/2}).

Moreover, Σ_{l=1}^{q} g(q,l)² = q^{−1}·Σ_{c≥1} μ²(c)·P(c)/(c²·m_c(q)).

*Risk:* Bookkeeping. Steps:
1. Σ_l Q(x;q,l)² = Q(x) + 2·Σ_{1≤j<x/q} C(x, jq).
2. Σ_l g(q,l)·Q(x;q,l) = x·Σ_l g(q,l)² + Σ_l g(q,l)·E(x;q,l), which is O(x^{1/2}τ(q)²/q) by P1(c). Note x·τ(q)²·x^{1/2}/q ≤ C·x^{7/4}/q because q ≤ x.
3. Apply P2 to each C(x, jq); there are fewer than x/q values of j.
4. Exact lattice sum. Group a, b by c = gcd(a,b); the coprime parts give P(c). Since c² | jq ⇔ m_c | j, use Σ_{|i|<T} (T − |i|) = T² + B(T) with T = x/(q·m_c). This gives
     Σ_{j∈Z, |j|q<x} A(|j|q)·(x − |j|q) = x²·K(q) + M(x,q),  with K(q) = q^{−1}·Σ_c μ²(c)P(c)/(c²·m_c).
5. Hence S = x²·(K(q) − Σ_l g²) + M + O(…). The coefficient of x² must vanish: for fixed q, S(x,q)/x² → 0 because g is the limit density, and M(x,q) ≤ q·Σ_c min(1/4, x/(q c²)) ≪_q x^{1/2}.
The off-by-one cases j·q = x contribute 0. Possible failure modes: a factor-2 error between the j > 0 and j < 0 halves, or forgetting the j = 0 term. For j = 0, C(x,0) = Q(x) replaces A(0)·x = 6x/π², at a cost of O(x^{1/2}). Numerically, S(10⁶, q)/M(10⁶, q) ∈ [0.998, 1.000] for q ∈ [2·10⁴, 2·10⁵].

## P4: Sawtooth sum over squares

Depends on: none  
Cites: Montgomery–Vaughan 2007, Theorem 1.12

Let B(t) := {t}·(1 − {t}) and I := ∫_0^∞ B(t^{−2}) dt = (1/2)·∫_0^∞ B(v)·v^{−3/2} dv.

Then I = −4ζ(−1/2) = 0.8315448999…, and there is an absolute constant C_4 such that for every real Z > 0:
  |Σ_{n≥1} B(Z/n²) − I·Z^{1/2}| ≤ C_4·Z^{1/3}.

*Risk:* Low. For the error term, split at N = Z^{1/3}:
- n ≤ N contributes at most N/4, and so does ∫_0^N.
- For n > N, the function t ↦ B(Z/t²) is continuous, with total variation on [N, ∞) ≪ Z/N² + 1. The usual sum-versus-integral comparison then gives Z/N² + 1.
- For Z < 1 the bound is trivial, since B(Z/n²) ≤ Z/n².
The constant needs the continuation of ζ to σ > −1. Theorem 1.12 of Montgomery–Vaughan is stated only for σ > 0; integrate by parts once more using the periodic Bernoulli function B̄₂(v) = {v}² − {v} + 1/6 = 1/6 − B(v). Numerically confirmed: I = 0.83154489990941…

## P5: Asymptotic evaluation of M(x,q) with explicit arithmetic factor (CRUX)

Depends on: P4  
Cites: none

Use M(x,q), B, P(c), m_c(q) as in P3. For an integer q ≥ 1 define
  h(q) := ∏_{p|q} λ_p(q),  h(1) = 1,
where
  λ_p(q) := (p² + p^{1/2} − 2)/(p² + p − 2) if p ∥ q,
  λ_p(q) := (p + 1)/(p + 2) if p² | q.
Let Φ_∞ := −4ζ(−1/2)·∏_p (1 − 3p^{−2} + 2p^{−3}) ≈ 0.238443.

Claim. For every ε > 0 there is C_5(ε) such that for all integers q ≥ 1 and real x ≥ q:
  |M(x,q) − Φ_∞·h(q)·x^{1/2}·q^{1/2}| ≤ C_5(ε)·x^{1/3}·q^{2/3+ε}.

*Risk:* The q-dependence must be tracked exactly. Steps:
1. Write c = c₁c₂ with c₁ | rad(q) and gcd(c₂, q) = 1. Then m_c = u(c₁)·c₂², where u(c₁) = ∏_{p|c₁} p^{2−min(2, v_p(q))}; that is, p if p ∥ q and 1 if p² | q.
2. P(c) = P₀·κ(c₁)·κ(c₂), with P₀ = ∏_p (1 − 2/p²) and κ(c) = ∏_{p|c} (1 − 2/p²)^{−1}.
3. Write μ²(c₂)·κ(c₂)·1[gcd(c₂,q) = 1] = Σ_{e|c₂} v_q(e). Here v_q is multiplicative:
   - p ∤ q: v_q(p) = 2/(p² − 2), v_q(p²) = −κ(p), v_q(p^j) = 0 for j ≥ 3.
   - p | q: v_q(p) = −1, v_q(p^j) = 0 for j ≥ 2.
4. Apply P4 with Z = X/(u·e²), where X = x/q ≥ 1. The total error is ≪ X^{1/3}·Σ_e |v_q(e)|·e^{−2/3}·Σ_{c₁|rad q} κ(c₁)·u(c₁)^{2/3}/c₁² ≪_ε q^ε·X^{1/3}.
5. The main term is I·P₀·δ_q·∏_{p|q} (1 + u_p^{1/2}/(p² − 2)), with δ_q = Σ_e v_q(e)/e. This simplifies to Φ_∞·h(q).
Cross-checks: averaging h(q)·q^{1/2} over all q reproduces Vaughan 2005's c₂ = 0.1284787 to 7 digits, and M matches exact single-modulus variances. Risk: algebra slips in the Euler factor for p | q.

## P6: Weighted mean of h over polynomial values

Depends on: none  
Cites: none

Let f be as in problem.md (integer-valued, degree d ≥ 1, f(t) ≥ 2 and f'(t) ≥ 1 for t ≥ 1). Let D_f be the least positive integer with D_f·f ∈ Z[t], and
  ρ*(m) := D_f^{−1}·#{a mod m·D_f : f(a) ≡ 0 (mod m)}.
Then ρ* = ρ when f ∈ Z[t], and ρ* is multiplicative.

Let h be the multiplicative-type function of P5:
  h(q) = ∏_{p|q} λ_p(q), with λ_p(q) = (p² + p^{1/2} − 2)/(p² + p − 2) if p ∥ q and (p + 1)/(p + 2) if p² | q.

Define
  𝔖_f := ∏_p [1 + β_p·ρ*(p)/p + β'_p·ρ*(p²)/p²],
  β_p := (p^{1/2} − p)/(p² + p − 2),  β'_p := (1 − p^{1/2})/(p² + p − 2).
The product converges absolutely.

Claim. There is C_6(f) such that for all real y ≥ 1:
  |Σ_{1≤k≤y} f'(k)·f(k)^{1/2}·h(f(k)) − (2/3)·𝔖_f·f(y)^{3/2}| ≤ C_6(f)·f(y)^{3/2}·y^{−1/5}.

*Risk:* Low to moderate. Write h(q) = Σ_{t|q} β(t), where β is multiplicative with β(p) = β_p, β(p²) = β'_p, β(p^j) = 0 for j ≥ 3. Then |β(t)| ≤ t^{−3/4}.

Needed bounds on ρ*: for all p outside a finite set E_f, ρ*(p) ≤ d and ρ*(p²) ≤ d·p. (Roots mod p of a nonzero polynomial of degree ≤ d; each root lifts to at most p roots mod p².) Hence |β(t)|·ρ*(t) ≪_f C^{ω(t)}·t^{−1/4} for cube-free t.

Steps:
- Periodicity: m | f(k) depends only on k mod m·D_f.
- F(k) = f'(k)·f(k)^{1/2} is piecewise monotone on [1, ∞) with at most 2d − 1 pieces, and max_{[1,y]} F ≪_f f(y)^{3/2}/y.
- For t ≤ T, sum over arithmetic progressions.
- For t > T, bound by Σ_k F(k)·Σ_{t|f(k), t>T} |β(t)| ≪ T^{−1/4}·f(y)^{3/2+ε}, using the divisor bound.
- Take T = y.

Do not use the problem's ρ(m) literally when f ∉ Z[t]; it may be ill-defined, which is why ρ* is used.

## P7: Assembly: main theorem

Depends on: P3, P5, P6  
Cites: none

Let f be as in problem.md, and V_f(x,y) as in problem.md. Let M(x,q) be as in P3, Φ_∞ and h as in P5, and 𝔖_f and ρ* as in P6. Put C_f := (2/3)·Φ_∞·𝔖_f. Equivalently,
  C_f = −(8/3)·ζ(−1/2)·∏_p (1 − 1/p)·(1 + 1/p − 2/p² − ρ*(p)·(p^{−2} − p^{−5/2}) − ρ*(p²)·(p^{−7/2} − p^{−4})).

(a) For all real x ≥ 2 and y ≥ 1 with f(y) ≤ x:
  V_f(x,y) = Σ_{1≤k≤y} f'(k)·M(x, f(k)) + O_f(x^{7/4}·log 2x).

(b) For every ε > 0 and the same x, y:
  V_f(x,y) = C_f·x^{1/2}·f(y)^{3/2} + O_{f,ε}( x^{1/2}·f(y)^{3/2}·y^{−1/5} + x^{1/3+ε}·f(y)^{5/3} + x^{7/4}·log 2x ).

In particular V_f(x,y) ~ C_f·x^{1/2}·f(y)^{3/2} whenever y → ∞ and x^{5/6+δ} ≤ f(y) ≤ x^{1−δ} for some fixed δ > 0.

*Risk:* Low; this is summation. Since f(k) ≤ f(y) ≤ x and f(k) ≥ 2, P3 and P5 apply with q = f(k).
- Σ_{k≤y} f'(k)/f(k) ≪_f log(2y) ≪ log 2x.
- Σ_{k≤y} f'(k) ≪_f f(y) ≤ x, so the x^{1/2} terms total O(x^{3/2}).
- Σ_{k≤y} f'(k)·x^{1/3}·f(k)^{2/3+ε} ≪ x^{1/3+ε}·f(y)^{5/3}.
- The main term is x^{1/2}·Φ_∞·Σ_k f'(k)·f(k)^{1/2}·h(f(k)), evaluated by P6.
Verify the equality of the two expressions for C_f (Euler-factor algebra). Numerically, C_k = 0.128479, matching Vaughan's c₂.
