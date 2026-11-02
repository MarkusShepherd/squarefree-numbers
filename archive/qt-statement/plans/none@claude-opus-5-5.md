# Plan: none@claude-opus-5-5

Model: claude-opus-5-5

PREDICTION. V_f(x,y) ~ C_f x^{1/2} f(y)^{3/2}. The constant C_f is Vaughan's full-variance constant c_2 = 0.1284787 times an f-dependent Euler product. The plan proves the asymptotic for x^{13/15+eps} <= f(y) <= x^{1-eps}.

HOW THE CONSTANT WAS FOUND (exploration, not part of the proof).
- Per modulus, V(q) = sum_l E(x;q,l)^2 is approximately eta(q) (xq)^{1/2}. Here eta(q) is eta_0 times a product, over primes p dividing q, of local factors that depend only on min(v_p(q),2).
- eta comes from the 'correlation model' V*(q) = (6/pi^2)x + 2 sum_{v<=x/q} A(vq)(x-vq) - x^2 sum_l g(q,l)^2. Here A(n) is the density of n' with n' and n'+n both squarefree.
- V*(q) equals -2q times a series in Btilde_2(t) = {t}^2/2-{t}/2. A Mellin/lattice-sum analysis of that series gives the constant 2 zeta(-1/2) and the local factors.
- Averaging eta(q) over all q reproduces Vaughan's c_2 to 8 digits (0.12847867 vs 0.12847868). That is a strong check of the local factors.
- Exact per-modulus numerics at x=10^6, q<=10^4 confirm the q-dependence:
  - mean h over even q / mean over odd q: observed 0.801, predicted 0.802;
  - q ≡ 0 mod 4: observed 0.747, predicted 0.750;
  - q ≡ 2 mod 4: observed 0.856, predicted 0.854.
- V*(q) matches the true V(q) for individual q (e.g. q=10^4: 13744.5 vs 13744.8).
- Sparse moduli are arithmetically 'poorer' than average (e.g. odd), so C_f > c_2. This explains why the data sit about 7–11% above c_2.

PROOF ARCHITECTURE (adapting Vaughan 2005 and Brüdern–Wooley).
1. Open the square: V_f = sum_k f'(k) V*(f(k)) + 2 D_f + O(x^{3/2+eps}).
2. The circle method with K_f(alpha) = sum_k f'(k) sum_{v<=x/f(k)} e(alpha v f(k)) gives D_f << x^{9/5+eps}. It uses the BGPVW minor-arc L^2 bound and BGPVW Lemmas 3.2/4.2 with major arcs of level P = x^{2/5}/2, plus only the trivial bound sup|K_f| << x log x. That bound works for every degree d, including linear f.
3. An exact identity expresses V*(q) as a Btilde_2 series.
4. A lattice-sum lemma: sum_u Btilde_2(Z/u^2) = 2 zeta(-1/2) Z^{1/2} + O(Z^{1/3} log).
5. Per-modulus asymptotic: V*(q) = eta(q)(xq)^{1/2} + O(q^{2/3+eps} x^{1/3} log x).
6. Averaging eta(f(k)) over k uses only rho(p) and rho(p^2).

RANGE. The barrier x^{9/5} comes from trivial bounds on K_f on the minor arcs. With the minor arcs used here, the BGPVW L^2 bound cannot go below x^{4/5}. A larger range would need nontrivial Weyl-type bounds for K_f together with Vaughan's K_q + H_q major-arc refinement; that is not attempted. For linear f it would presumably recover Vaughan's range f(y) >= x^{2/3} exp(-...).

DISCREPANCIES CHECKED.
- The raw normalised data V/(x^{1/2} f(y)^{3/2}) at the smallest ratio r = f(y)/x = 0.01 are 1.4–3% above C_f.
- This is a finite-ratio effect, not a constant mismatch:
  - at fixed r the normalised values are x-independent to 3–4 digits across x = 10^6 … 2.56·10^8 (V ≈ x^2 Psi(f(y)/x));
  - V / [sum_k f'(k) eta(f(k)) (x f(k))^{1/2}] is 1.014–1.019 at r ≈ 0.01 for all three polynomials, growing roughly like a·sqrt(r). This matches a per-modulus secondary term of size O(q), i.e. an f(y)^2 term.
  - the full variance computed by me at x=10^6, Q=10^4 gives V/(x^{1/2}Q^{3/2}) = 0.1303 vs c_2 = 0.1285, the same +1.4% offset.
- The operator's linear-in-sqrt(r) extrapolations agree with my constants within their stated uncertainty:
  - k^2+1: 0.1384 ± 0.0070 vs 0.13808;
  - k^3+2: 0.1385 ± 0.0073 vs 0.13561;
  - 2k+1: 0.1409 ± 0.0082 vs 0.14261.
- The fitted exponents (alpha ≈ 0.45–0.46, beta ≈ 1.54–1.55, alpha+beta = 2.000) are biased by this curvature in r; they are consistent with (1/2, 3/2).

SOURCES AND COMPLIANCE.
- No web search was performed. No excluded author or excluded paper was consulted, and nothing from memory of them was used.
- Sources used: papers/vaughan-2005.pdf (R. C. Vaughan, Proc. LMS 91 (2005) 573–597); papers/bgpvw-1998.pdf (Brüdern–Granville–Perelli–Vaughan–Wooley, Phil. Trans. R. Soc. A 356 (1998) 739–761); papers/bruedern-wooley-2011.pdf (structure only).
- External, pre-2010: E. C. Titchmarsh, The Theory of the Riemann Zeta-Function, 2nd ed., rev. D. R. Heath-Brown, Oxford 1986 (van der Corput second-derivative test, Theorem 5.9).
- All numerics were my own Python checks against results.json; they reproduce its V values exactly.
- One background numerical job (a slow duplicate of the row check) was stopped at its time limit; a faster sieve-based version completed and its results are the ones reported. That version covers all rows for k^2+1 and k^3+2, and the 2k+1 rows except the three at x = 2.56·10^8 with ratios 0.1–0.4, which fall outside its sieve range.

## Main theorem

Let f be as in problem.md: integer-valued, degree d >= 1, f(t) >= 2 and f'(t) >= 1 for t >= 1. Let rho(m) = #{a mod m : f(a) ≡ 0 mod m}.

Definitions.
- L_0(p) := 1 + (p^3-1)/(p^2-1)^2 = p^2(p+2)/((p-1)(p+1)^2).
- lambda_p(1) := (p^4 + p^{5/2} - 2p^2)/(p^4 + p^3 - 2p^2).
- lambda_p(2) := (p+1)/(p+2).
- eta_0 := -4 zeta(-1/2) zeta(2)^{-2} prod_p (1 - (p+1)^{-2}) = 0.238443366...
- E_p(f) := 1 - rho(p)/p + (rho(p)/p - rho(p^2)/p^2) lambda_p(1) + (rho(p^2)/p^2) lambda_p(2).
- C_f := (2/3) eta_0 prod_p E_p(f). The product converges absolutely.

THEOREM. For every eps > 0, uniformly for real x >= 2 and y >= 1 with f(y) <= x,

  V_f(x,y) = C_f x^{1/2} f(y)^{3/2} + O_{f,eps}( x^{9/5+eps} + x^{1/3+eps} f(y)^{5/3} + x^{1/2} f(y)^{3/2} y^{-1/5+eps} ).

In particular V_f(x,y) ~ C_f x^{1/2} f(y)^{3/2} for x^{13/15+eps} <= f(y) <= x^{1-eps}.

Consistency check: for f(k) = k+1, C_f equals Vaughan's c_2 = 0.1284787.

## Numerics check

Yes, within the extrapolation uncertainty. The finite-size offset is explained.

- Exponents: the fixed-ratio slopes give alpha+beta = 2.000, matching x^{1/2} f(y)^{3/2}.
- Constants, operator's extrapolation vs prediction:
  - k^2+1: 0.1384 ± 0.0070 vs 0.13808;
  - k^3+2: 0.1385 ± 0.0073 vs 0.13561;
  - 2k+1: 0.1409 ± 0.0082 vs 0.14261.
- Direct check: V / [sqrt(x) sum_k f'(k) eta(f(k)) f(k)^{1/2}] is 1.008–1.019 at r ≈ 0.01, x-independent, and increasing with r roughly like sqrt(r).
- The full variance shows the same +1.4% offset against Vaughan's proven c_2. So the offset is a lower-order term, not a wrong constant.

## P1: Arithmetic identities for densities, singular series and tau

Depends on: none  
Cites: Vaughan 2005, Lemma 2.4, Vaughan 2005, Lemma 2.5, Vaughan 2005, Lemma 2.14, Vaughan 2005, Lemma 2.15, Vaughan 2005, Lemma 2.17, BGPVW 1998, Lemma 3.1

Notation: mu is the Möbius function, phi is Euler's function, sigma is the sum of divisors, c_s(n) is Ramanujan's sum, and e(t) = exp(2 pi i t). For s in N let tau(s) := sum_{d>=1, s | d^2} mu(d) d^{-2}. Then:
(a) tau(s) = (6/pi^2) prod_{p|s} (-1/(p^2-1)) if s is cube-free, and tau(s) = 0 otherwise.
(b) For q in N and l in Z, g(q,l) = (6/pi^2) q^{-1} prod_{p|q} (1-p^{-2})^{-1} eps_p(q,l). Here, with b = v_p(q), s = v_p(l) (s = infinity if l = 0) and m = min(2,b): eps_p = 1 - p^{m-2} if s >= m, and eps_p = 1 otherwise. Hence g(q,l) depends only on gcd(q,l), and 0 <= g(q,l) <= 1/q.
(c) For gcd(a,q) = 1: sum_{l=1}^q g(q,l) e(al/q) = tau(q).
(d) sum_{l=1}^q g(q,l)^2 = q^{-1} sum_{s|q} phi(s) tau(s)^2.
(e) sum_s phi(s) tau(s)^2 = 6/pi^2. For S >= 1: sum_{s>S} sigma(s) tau(s)^2 << S^{-1/2}(log 2S)^3 and sum_{s<=S} s^2 tau(s)^2 << S^{1/2}(log 2S)^2, with absolute implied constants.
(f) A(n) := sum_s tau(s)^2 c_s(n) converges absolutely and equals prod_p(1-2/p^2) prod_{p^2|n}(p^2-1)/(p^2-2).
(g) Q(x) := #{n <= x : n squarefree} = (6/pi^2) x + O(x^{1/2}) for real x >= 1, with an absolute implied constant.

*Risk:* Low; these are standard facts. The prover must reconcile normalisations: Vaughan's rho(q) is our tau(q), and Vaughan's and BGPVW's G(q) differ by sign and normalisation.

## P2: Opening the square

Depends on: P1  
Cites: Vaughan 2005, Lemma 2.2, Vaughan 2005, Lemma 2.3

Notation as in problem.md (Q(x;q,l), g(q,l), E(x;q,l), f, V_f). For n in N let A(n) := prod_p (1-2/p^2) prod_{p^2|n}(p^2-1)/(p^2-2). For real x >= 1 and h in N let C(x;h) := #{n in N : n+h <= x, n and n+h squarefree}. For q in N define
  V*(x;q) := (6/pi^2) x + 2 sum_{1<=v<=x/q} A(vq)(x-vq) - x^2 sum_{l=1}^q g(q,l)^2.
Claim: for every eps > 0, uniformly for real x >= 2 and y >= 1 with f(y) <= x,
  V_f(x,y) = sum_{k<=y} f'(k) V*(x;f(k)) + 2 sum_{k<=y} f'(k) sum_{1<=v<=x/f(k)} [C(x;v f(k)) - A(v f(k))(x - v f(k))] + O_{f,eps}(x^{3/2+eps}).

*Risk:* Low. The cross term follows Vaughan's (3.5)–(3.7), using Lemma 2.2(ii). This gives sum_l g(q,l) Q(x;q,l) = x sum_l g(q,l)^2 + O(x^{1/2} d(q)^3 / q), where d is the divisor function.

## P3: Circle method bound for the correlation errors (CRUX)

Depends on: P1  
Cites: BGPVW 1998, Theorem 2, BGPVW 1998, Lemma 3.1, BGPVW 1998, Lemma 3.2, BGPVW 1998, Lemma 4.2

Let f be as in problem.md. For n in N let A(n) := prod_p(1-2/p^2) prod_{p^2|n}(p^2-1)/(p^2-2). For real x >= 1 and h in N let C(x;h) := #{n in N : n+h <= x, n and n+h squarefree}. Define
  D_f(x,y) := sum_{k<=y} f'(k) sum_{1<=v<=x/f(k)} [C(x;v f(k)) - A(v f(k))(x - v f(k))].
Claim: for every eps > 0, D_f(x,y) = O_{f,eps}(x^{9/5+eps}) uniformly for x >= 2 and y >= 1 with f(y) <= x.
Route:
- Orthogonality with F(alpha) = sum_{n<=x} mu^2(n) e(n alpha) and K_f(alpha) = sum_k f'(k) sum_v e(-alpha v f(k)), using the trivial bound |K_f| << x log x.
- Major arcs of level P = x^{2/5}/2, as in BGPVW.
- Minor arcs via BGPVW Theorem 2: int_m |F|^2 << x^{1+eps} P^{-1/2} + x^eps P^2.
- Major-arc errors via BGPVW Lemmas 3.2 and 4.2.
- Complete the beta-integral and the q-sum using BGPVW Lemma 3.1.

*Risk:* The arcs must match BGPVW's M and m exactly; their lemmas require Q <= x^{1/2}/2. Only the trivial bound on K_f may be used, otherwise the claimed x^{9/5} needs more justification. Every constant in the completion steps must stay uniform in y.

## P4: Exact Bernoulli-series identity

Depends on: P1  
Cites: Vaughan 2005, Lemma 2.16, Vaughan 2005, Lemma 2.17

Definitions:
- For real t >= 0: Btilde_2(t) := {t}^2/2 - {t}/2.
- tau(s) := sum_{d: s|d^2} mu(d) d^{-2}.
- A(n) := prod_p(1-2/p^2) prod_{p^2|n}(p^2-1)/(p^2-2).
- For q in N and real x >= 1: V*(x;q) := (6/pi^2) x + 2 sum_{1<=v<=x/q} A(vq)(x-vq) - x^2 sum_{l=1}^q g(q,l)^2, with g as in problem.md.
- For e | s let e_q := e/gcd(e,q). For real X > 0: Phi_q(X) := sum_s tau(s)^2 sum_{e|s} mu(s/e) e e_q Btilde_2(X/e_q).
Claim: each summand of Phi_q is bounded by tau(s)^2 e X/2, so the series converges absolutely, and V*(x;q) = -2q Phi_q(x/q) exactly for all q in N and real x >= 1.

*Risk:* Low. Check the sign convention of Btilde_2 in Vaughan's Lemma 2.16 against the definition here.

## P5: Lattice sum of Btilde_2 over squares

Depends on: none  
Cites: Titchmarsh 1986, Theorem 5.9, Vaughan 2005, Lemma 2.18

For real t >= 0 let Btilde_2(t) := {t}^2/2 - {t}/2. Claim:
(i) int_0^infinity Btilde_2(v^{-2}) dv = 2 zeta(-1/2).
(ii) There is an absolute constant c such that for all real Z > 0, |sum_{u>=1} Btilde_2(Z/u^2) - 2 zeta(-1/2) Z^{1/2}| <= c Z^{1/3} log(2+Z).
Suggested route: Fourier expansion of B_2, the van der Corput second-derivative test, and comparison with the integral where the phase varies slowly.

*Risk:* Medium-low. The range u ~ Z^{1/2} must be compared with the integral rather than bounded by cancellation; that comparison is what produces the constant. Numerics confirm both parts.

## P6: Per-modulus asymptotic (CRUX)

Depends on: P4, P5, P1  
Cites: none

Definitions:
- Btilde_2, tau, Phi_q and e_q as in P4.
- lambda_p(1) := (p^4+p^{5/2}-2p^2)/(p^4+p^3-2p^2), lambda_p(2) := (p+1)/(p+2).
- eta_0 := -4 zeta(-1/2) zeta(2)^{-2} prod_p(1-(p+1)^{-2}).
- eta(q) := eta_0 prod_{p||q} lambda_p(1) prod_{p^2|q} lambda_p(2).
Claim: for every eps > 0, uniformly for q in N and real X >= 1, -2q Phi_q(X) = eta(q) q X^{1/2} + O_eps(q^{1+eps} X^{1/3} log 2X). Equivalently, V*(x;q) = eta(q)(xq)^{1/2} + O_eps(q^{2/3+eps} x^{1/3} log 2x) for 1 <= q <= x.
Hint: Phi_q(X) = sum_m b_q(m) m Btilde_2(X/m), where b_q factorises with local factors:
- p not dividing q: b(1) = 1-(p^2-1)^{-2}, b(p^2) = p^2(p^2-1)^{-2};
- p || q: b(1) = 1-(p^2-1)^{-2}, b(p) = p^2(p^2-1)^{-2};
- p^2 | q: b(1) = p^2/(p^2-1);
all times (6/pi^2)^2. Then apply P5.

*Risk:* Identifying the constant exactly as eta(q), with uniformity in q. Sanity check: averaging eta over all q must reproduce Vaughan's c_2 (verified numerically to 8 digits). Do not shift contours past Re = -3/4.

## P7: Averaging over polynomial values

Depends on: none  
Cites: none

Let f be as in problem.md, rho(m) = #{a mod m : f(a) ≡ 0 mod m}, and lambda_p(1), lambda_p(2), eta_0, eta(q) as in P6. Let E_p(f) := 1 - rho(p)/p + (rho(p)/p - rho(p^2)/p^2) lambda_p(1) + (rho(p^2)/p^2) lambda_p(2), and frakE(f) := prod_p E_p(f).
Claim:
(i) prod_p E_p(f) converges absolutely.
(ii) For every eps > 0, uniformly for y >= 2: sum_{k<=y} f'(k) f(k)^{1/2} eta(f(k)) = (2/3) eta_0 frakE(f) f(y)^{3/2} + O_{f,eps}(f(y)^{3/2} y^{-1/5+eps}).

*Risk:* Low-medium. f may have repeated factors, so the proof should use only rho(r) <= r and rho(p) <= d for all but finitely many p.

## P8: Assembly

Depends on: P2, P3, P6, P7  
Cites: none

Let f be as in problem.md, with rho, lambda_p(1), lambda_p(2), eta_0 and E_p(f) as defined in P6 and P7, and C_f := (2/3) eta_0 prod_p E_p(f). Claim: for every eps > 0, uniformly for x >= 2 and y >= 1 with f(y) <= x,
  V_f(x,y) = C_f x^{1/2} f(y)^{3/2} + O_{f,eps}(x^{9/5+eps} + x^{1/3+eps} f(y)^{5/3} + x^{1/2} f(y)^{3/2} y^{-1/5+eps}).

*Risk:* Low; this is bookkeeping. Check that the definitions of V* in P2 and P6 coincide, and that P6 is applied only with q = f(k) <= x.
