# Plan: none

Model: codex:gpt-6.1-sol

Plan for the subclass f ∈ Z[t], retaining the original weight f′(k) and including all three numerical examples. Reconstruct a fixed-modulus variance estimate, then average its multiplicative main factor over polynomial values. The resulting asymptotic range is x^(7/9+δ) ≤ f(y) ≤ x^(1−δ), for fixed 0 < δ < 1/9. The main analytic proposition uses a weaker contour estimate than the supplied fixed-modulus paper. That paper cannot be applied verbatim: its residue computation omits the factor 1/2 from ζ(2s+2), doubling its squarefree constant, and its displayed Euler product for ζ(−1/2) requires analytic continuation. The corrected prediction agrees with the numerical extrapolations. Restricting to integer coefficients ensures that polynomial congruences have period equal to their modulus and satisfy the Chinese remainder theorem without denominator corrections. Reviewed sources: J. Brüdern and T. D. Wooley, Sparse variance for primes in arithmetic progression (2011), https://doi.org/10.1093/qmath/hap029, used for motivation only; J. Brüdern, A. Granville, A. Perelli, R. C. Vaughan and T. D. Wooley, On the exponential sum over k-free numbers (1998), https://doi.org/10.1098/rsta.1998.0183; Tomos Parry, A variance for k-free numbers in arithmetic progressions of given modulus (2019, revised 2023), arXiv:1912.04683v2. Neither excluded source was searched, opened, or used.

## Main theorem

Let f ∈ Z[t] have degree d ≥ 1 and satisfy the assumptions in problem.md. All prime products below run over positive primes. Let ζ denote the analytically continued Riemann zeta function. Define A_p = (p²−2+√p)/(p²+p−2), B_p = (p²−1)/(p²+p−2), κ = −4ζ(−1/2)ζ(2)^(−1) ∏_p(1−2/(p(p+1))), and C(f) = (2κ/3)∏_p[1+(A_p−1)ρ(p)/p+(B_p−A_p)ρ(p²)/p²]. These products converge absolutely and C(f) > 0. For every 0 < ε < 1/(4d), there exists K(f,ε) such that, uniformly for real x ≥ 2 and y ≥ 1 with Y = f(y) ≤ x, |V_f(x,y)−C(f)x^(1/2)Y^(3/2)| ≤ K(f,ε)[x^(4/9+ε)Y^(14/9)+x^(5/3+ε)log(2Y)+x^(1/2)Y^(3/2−1/(2d)+ε)]. Consequently, for every fixed 0 < δ < 1/9 there exists K(f,δ) such that, uniformly when x^(7/9+δ) ≤ Y ≤ x^(1−δ), |V_f(x,y)/(C(f)x^(1/2)Y^(3/2))−1| ≤ K(f,δ)x^(−δ/(100d)).

## Numerics check

The powers x^(1/2)f(y)^(3/2) agree with results.json, including total exponent 2 at fixed f(y)/x. The predicted constants lie within the reported extrapolation uncertainties: 0.13506±0.01082 for t²+1, 0.14192±0.01079 for t³+2, and 0.14084±0.00846 for 2t+1. At the largest available x, the normalized values at ratio 0.01 are respectively 0.14151, 0.14501, and 0.14456. Their larger values at ratio 1 are outside the asserted asymptotic regime; the stated error bound permits a contribution of main-term size there. The finite data are consistent with, but do not establish, the required limit f(y)/x → 0.

## P1: Density, second moment, and elementary reduction to a triangular sum

Depends on: none  
Cites: J. Brüdern, A. Granville, A. Perelli, R. C. Vaughan and T. D. Wooley, On the exponential sum over k-free numbers (1998), Lemma 2.1, specialized to k=2; https://doi.org/10.1098/rsta.1998.0183, Tomos Parry, A variance for k-free numbers in arithmetic progressions of given modulus (2019, revised 2023), Lemma 2.3(B), specialized to k=2; arXiv:1912.04683v2, Tomos Parry, A variance for k-free numbers in arithmetic progressions of given modulus (2019, revised 2023), Lemma 2.7, specialized to k=2 and shifts 1 ≤ N ≤ x; arXiv:1912.04683v2

Let μ be the Möbius function, ζ(2)=π²/6, (a,b)=gcd(a,b), and [a,b]=lcm(a,b). All prime products run over positive primes. For integers q ≥ 1 and 1 ≤ l ≤ q, the density in problem.md is g(q,l) = (qζ(2))^(−1)∏_{p|q}(1−p^(−2))^(−1)∏_{p||q, p|l}(1−p^(−1)), unless some prime p satisfies p²|q and p²|l, in which case g(q,l)=0; here p||q means p|q and p²∤q. Define α(q)=∏_p[1−2/p²+(q,p²)/p⁴]. Then Σ_{l=1}^q g(q,l)²=α(q)/q. For real x ≥ 2 and integer 1 ≤ q ≤ x define L(q,a,b)=[q,(a²,b²)] and J_q(x)=Σ_{a,b≥1} μ(a)μ(b)L(q,a,b)/[a²,b²] · Σ_{1≤j≤x/L(q,a,b)}(x/L(q,a,b)−j). This double series converges absolutely. For every ε>0 there exists K_ε, independent of x and q, such that |Σ_{l=1}^q E(x;q,l)²−2J_q(x)−x/ζ(2)+α(q)x²/q| ≤ K_ε x^(5/3+ε)/q, uniformly throughout these ranges. No truncation parameter remains in this assertion.

*Risk:* The weighted first moment must retain its factor 1/q before multiplication by x. Losing that factor would prevent the final asymptotic range. Terms with square factors in q must be included.

## P2: Independent analytic evaluation with the corrected residue (CRUX)

Depends on: none  
Cites: Tomos Parry, A variance for k-free numbers in arithmetic progressions of given modulus (2019, revised 2023), Lemma 2.1, initially on Re(s)>1 and specialized to k=2; arXiv:1912.04683v2

Let μ denote the Möbius function, (a,b)=gcd(a,b), [a,b]=lcm(a,b), and ζ the analytically continued Riemann zeta function. For integers q ≥ 1 define α(q)=∏_p[1−2/p²+(q,p²)/p⁴], H(q)=∏_{p|q}[1−2/p²+(q,p²)^(−1/2)/p]/[1−2/p²+1/p], and κ=−4ζ(−1/2)ζ(2)^(−1)∏_p(1−2/(p(p+1))); an empty product is 1. For real x ≥ 2 and 1 ≤ q ≤ x, define L(q,a,b)=[q,(a²,b²)] and J_q(x)=Σ_{a,b≥1} μ(a)μ(b)L(q,a,b)/[a²,b²] · Σ_{1≤j≤x/L(q,a,b)}(x/L(q,a,b)−j). For every ε>0 there exists K_ε such that |J_q(x)−α(q)x²/(2q)+x/(2ζ(2))−(κ/2)H(q)√(xq)| ≤ K_ε x^ε q(x/q)^(4/9), uniformly for all such real x and integer q. All products displayed here converge absolutely. This assertion has no free contour or truncation parameters.

*Risk:* This must be proved independently of Parry's Lemma 2.6 and stated main constant. The residue of ζ(2s+2) at s=−1/2 is 1/2. A plausible route shifts the triangular Perron integral to Re(s)=−3/4+η, with fixed η>0 chosen in terms of ε, and uses the zeta mean-square estimate on Re(2s+2)>1/2. For X=x/q≥1, height T=max(2,X^(7/9)) balances X²/T² against X^(1/4)T^(1/4), yielding exponent 4/9 after explicit ε losses. Uniform control of the q-dependent Euler product and Perron errors, including X near 1 and integer endpoints, is essential.

## P3: Divisor expansion and summable polynomial root weights

Depends on: none  
Cites: none

Fix f ∈ Z[t] of degree d ≥ 1 satisfying problem.md, and retain its root-count function ρ. For each prime p define A_p=(p²−2+√p)/(p²+p−2) and B_p=(p²−1)/(p²+p−2). Define the multiplicative function a on positive integers by a(1)=1, a(p)=A_p−1, a(p²)=B_p−A_p, and a(p^j)=0 for j≥3; multiplicative means a(mn)=a(m)a(n) when gcd(m,n)=1. Define H(n)=∏_{p|n}[1−2/p²+gcd(n,p²)^(−1/2)/p]/[1−2/p²+1/p], with H(1)=1. Then H(n)=Σ_{r|n}a(r) for every integer n≥1. For every ε>0 there is K_ε such that Σ_{r|n}|a(r)|r^(1/2) ≤ K_ε n^ε for all n≥1. There is K_f such that Σ_{r≥1}|a(r)|ρ(r)/r^(1/2) ≤ K_f. Consequently, uniformly for real R≥1, Σ_{r>R}|a(r)|ρ(r)/r ≤ K_f R^(−1/2) and Σ_{r≤R}|a(r)|ρ(r) ≤ K_f R^(1/2). Moreover M_f=Σ_{r≥1}a(r)ρ(r)/r converges absolutely, equals ∏_p[1+(A_p−1)ρ(p)/p+(B_p−A_p)ρ(p²)/p²], and satisfies 0<M_f≤1. Constants K_f depend only on f, and K_ε only on ε.

*Risk:* Repeated factors of f are allowed, so a bound ρ(p²)≤d cannot be assumed. Outside finitely many primes depending on f, the sufficient bound is ρ(p²)≤dp. Primes dividing every coefficient require separate finite local factors.

## P4: Effective arithmetic averaging with the original derivative weight

Depends on: P3  
Cites: none

Fix f ∈ Z[t] of degree d≥1 satisfying problem.md. For each prime p let A_p=(p²−2+√p)/(p²+p−2), B_p=(p²−1)/(p²+p−2), and define M_f=∏_p[1+(A_p−1)ρ(p)/p+(B_p−A_p)ρ(p²)/p²]. For integers n≥1 let H(n)=∏_{p|n}[1−2/p²+gcd(n,p²)^(−1/2)/p]/[1−2/p²+1/p], with H(1)=1. For every ε>0 there is K(f,ε) such that, uniformly for real z≥1 and real truncation parameter R≥1, |Σ_{1≤k≤z}H(f(k))−M_f z| ≤ K(f,ε)[R^(1/2)+z^(1+ε)R^(−1/2)]. In particular the choice R=z is permitted. Furthermore, for every 0<ε<1/(4d), there is K′(f,ε) such that, uniformly for real y≥1 and Y=f(y), |Σ_{1≤k≤y}f′(k)√f(k)H(f(k))−(2M_f/3)Y^(3/2)| ≤ K′(f,ε)Y^(3/2−1/(2d)+ε). All sums over k are over positive integers, and all constants are independent of z, R, and y.

*Risk:* The truncation must control omitted divisors pointwise before averaging. Partial summation must handle real endpoints and any initial interval on which the auxiliary weight f′(t)√f(t) is not monotone. Integer coefficients are used for residue-class counting modulo r.

## P5: Summation of the uniform estimates and extraction of an asymptotic range

Depends on: P1, P2, P4  
Cites: none

Fix f ∈ Z[t] of degree d≥1 satisfying problem.md. Let ζ be the analytically continued Riemann zeta function. For each prime p define A_p=(p²−2+√p)/(p²+p−2) and B_p=(p²−1)/(p²+p−2), and set κ=−4ζ(−1/2)ζ(2)^(−1)∏_p(1−2/(p(p+1))), M_f=∏_p[1+(A_p−1)ρ(p)/p+(B_p−A_p)ρ(p²)/p²], and C(f)=2κM_f/3. For every 0<ε<1/(4d), there is K(f,ε) such that, uniformly for real x≥2 and y≥1 with Y=f(y)≤x, |V_f(x,y)−C(f)x^(1/2)Y^(3/2)| ≤ K(f,ε)[x^(4/9+ε)Y^(14/9)+x^(5/3+ε)log(2Y)+x^(1/2)Y^(3/2−1/(2d)+ε)]. In particular, for every fixed 0<δ<1/9, there is K(f,δ) such that |V_f(x,y)/(C(f)x^(1/2)Y^(3/2))−1| ≤ K(f,δ)x^(−δ/(100d)) uniformly for x^(7/9+δ)≤Y≤x^(1−δ). Constants depend only on their displayed arguments. No lower cutoff on the individual moduli f(k) is imposed.

*Risk:* The fixed-modulus error must be summed over every k, including small moduli. Its reciprocal-modulus component contributes x^(5/3+ε)log(2Y), which explains the lower threshold 7/9. The first error has relative size x^ε(Y/x)^(1/18), so this plan does not establish a constant-only asymptotic at fixed positive Y/x.
