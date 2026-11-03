# Plan: simplest

Model: codex:gpt-6.1-sol

Plan: use elementary squarefree correlations, retain the resulting fractional-part kernel, and average that kernel over polynomial moduli using periodicity. Seven propositions give a theorem for every polynomial allowed in problem.md. The constant-term asymptotic holds in the weaker range x^(θ_d+δ) ≤ f(y) ≤ x^(1−δ), where θ_d=max(7/9,d/(d+1)). A ratio-dependent main term also covers f(y) comparable to x. The predicted constants agree with the numerical extrapolation uncertainties; the ratio profile explains the persistent ratio dependence. Sources used: J. Brüdern, A. Granville, A. Perelli, R. C. Vaughan and T. D. Wooley, [On the exponential sum over k-free numbers](https://doi.org/10.1098/rsta.1998.0183), 1998, particularly Lemma 2.1; background comparisons were R. C. Vaughan, [A variance for k-free numbers in arithmetic progressions](https://doi.org/10.1112/S0024611505015352), 2005, and J. Brüdern and T. D. Wooley, [Sparse variance for primes in arithmetic progression](https://doi.org/10.1093/qmath/hap029), the explicitly permitted supplied 2011 paper. No excluded source or other post-2010 result was used. This is a proof plan, not a proof.

## Main theorem

Let f satisfy every hypothesis in problem.md, let d=deg(f), and put Y=f(y). For each prime p define w₀(p)=1−ρ(p)/p, w₁(p)=ρ(p)/p−ρ(p²)/p², and w₂(p)=ρ(p²)/p². Define the absolutely convergent positive Euler product C_f=−(8/3)ζ(−1/2) ∏_p (1−1/p)[1−2/p²+(p w₀(p)+√p w₁(p)+w₂(p))/p²], where ζ is the analytically continued Riemann zeta function. For every ε>0 there is a constant A(f,ε)>0 such that, uniformly for real x≥2 and y≥2 with Y≤x, |V_f(x,y)−C_f x^(1/2)Y^(3/2)| ≤ A(f,ε)[x^(1/3)Y^(5/3)+x^(5/3+ε)+xY√(log(2x)/y)]. In particular, put θ_d=max(7/9,d/(d+1)). For every 0<δ<(1−θ_d)/2 there are constants A(f,δ)>0 and x₀(f,δ) such that, uniformly for x≥x₀(f,δ) and x^(θ_d+δ)≤Y≤x^(1−δ), |V_f(x,y)/(C_f x^(1/2)Y^(3/2))−1| ≤ A(f,δ)x^(−δ/6). No irreducibility, separability, or restriction on fixed prime divisors of f is imposed.

## Numerics check

Yes, within the distinction between a fixed-ratio profile and its small-ratio limit. The reported extrapolations are 0.134475±0.007285 for t²+1, 0.136321±0.002404 for t³+2, and 0.141686±0.008218 for 2t+1; all contain the predicted constants. These uncertainty envelopes are heuristic. Independent evaluation of the P4 profile with its square-divisor index truncated at 40000 reproduces the observed ratio dependence. For example, at ratio 1 it gives normalized values approximately 0.171077, 0.166100, and 0.183684, respectively. The largest-x observations are 0.171101, 0.166706, and 0.183691, at their recorded actual ratios. The cubic has only 634 sampled moduli. Keeping those actual moduli instead of averaging them, the P3 kernel truncated at 40000 gives 0.166698419, compared with 0.166705566 observed; the difference 0.000007147 is below the explicit kernel truncation bound. Thus finite sampling explains the larger cubic discrepancy. The validation records in results.json support the numerical implementation, although its production code was not available for an independent audit. No theorem was adjusted to fit the regression.

## P1: Local densities and the mixed moment

Depends on: none  
Cites: J. Brüdern, A. Granville, A. Perelli, R. C. Vaughan and T. D. Wooley, On the exponential sum over k-free numbers (1998), Lemma 2.1, specialized to k=2, for the density Euler product; https://doi.org/10.1098/rsta.1998.0183. The mixed-moment estimate is an additional elementary contract.

Let c=1/ζ(2), where ζ denotes the Riemann zeta function. For integers q≥1 and 1≤l≤q, the density g(q,l) from problem.md is zero if some prime p satisfies p²|q and p²|l. Otherwise g(q,l)=(c/q)∏_{p|q}(1−p^(−2))^(−1)∏_{p∥q, p|l}(1−p^(−1)). Here p∥q means that p divides q exactly once, all products are over primes, and an empty product is 1. Define D(q)=∑_{l=1}^q g(q,l)². Then D(q)=(c²/q)∏_{p∥q}[(1−2p^(−2)+p^(−3))/(1−p^(−2))²]∏_{p²|q}(1−p^(−2))^(−1). There is an absolute constant A>0 such that, uniformly for every real x≥2 and integer q≥1, |∑_{1≤n≤x} μ²(n)g(q,n mod q)−xD(q)|≤A√x/q and |∑_{1≤n≤x}μ²(n)−cx|≤A√x. In g(q,n mod q), the residue zero is represented by l=q.

*Risk:* The cases p∥q and p²|q must remain distinct. The mixed-moment bound requires uniform treatment of divisibility parameters exceeding x; a fixed-q asymptotic is insufficient.

## P2: A correlation estimate uniform in the shift

Depends on: none  
Cites: none

Define C₀=∏_p(1−2/p²), with the product over all primes. For each positive integer h define S(h)=C₀∏_{p²|h}(p²−1)/(p²−2). For every ε>0 there is a constant A(ε)>0 such that, uniformly for real x≥2 and integers 1≤h≤x, |∑_{1≤n≤x−h} μ²(n)μ²(n+h)−(x−h)S(h)|≤A(ε)x^(2/3+ε). The sum is zero when its upper limit is below 1. The constant is independent of h and x.

*Risk:* Uniformity for shifts as large as x is essential. An estimate stated only for each fixed shift cannot be substituted. Elementary Möbius truncation must bound the shift-dependent divisor factors uniformly.

## P3: Reduction of each variance to a positive kernel

Depends on: P1, P2  
Cites: none

For positive integers m define a(m)=μ²(m)∏_{p|m}(p²−2)^(−1), where the empty product is 1. Put C₀=∏_p(1−2/p²), c=1/ζ(2), B(t)={t}(1−{t}) for t≥0, and R_q(m)=m²/gcd(m²,q), where {t}=t−floor(t). For real x≥2 and integers 1≤q≤x define the absolutely convergent series W(x;q)=C₀q∑_{m≥1}a(m)R_q(m)B(x/(qR_q(m))). Define D(q)=∑_{l=1}^q g(q,l)² and S(h)=C₀∏_{p²|h}(p²−1)/(p²−2). Then W(x;q)=cx+2∑_{1≤h≤x/q}(x−hq)S(hq)−x²D(q), and 0≤W(x;q)≤cx. For every ε>0 there is a constant A(ε)>0 such that, uniformly in this entire range, |∑_{l=1}^q E(x;q,l)²−W(x;q)|≤A(ε)x^(5/3+ε)/q. The constants are independent of q and x.

*Risk:* The diagonal and both centering terms must cancel exactly before averaging small moduli. Losing an x²/q contribution would invalidate the plan.

## P4: Periodic averaging of the kernel over polynomial moduli (CRUX)

Depends on: none  
Cites: none

Let f satisfy problem.md and put Y=f(y). Define C₀=∏_p(1−2/p²), a(m)=μ²(m)∏_{p|m}(p²−2)^(−1), B(t)={t}(1−{t}), and R_m(b)=m²/gcd(m²,f(b)) for integers m≥1 and b, using gcd(m²,0)=m². For r>0 define F_f(r)=C₀∑_{m≥1}a(m)m^(−2)∑_{b=0}^{m²−1}∫₀ʳ tR_m(b)B(1/(tR_m(b)))dt; the integrand at t=0 is defined as zero. Define W(x;q)=C₀q∑_{m≥1}a(m)[m²/gcd(m²,q)]B(x/(q[m²/gcd(m²,q)])). All these series converge absolutely. There is a constant A(f)>0 such that, uniformly for real x≥2, y≥2, Y≤x, and integers 1≤M≤floor(y), |∑_{1≤k≤y}f′(k)W(x;f(k))−x²F_f(Y/x)|≤A(f)xY[M^(−1)+M log(2x)/y]. Consequently, throughout the same x,y range, the left side is at most A(f)xY√(log(2x)/y), after increasing A(f). If F_{f,M} denotes the displayed definition of F_f with m≤M, then 0≤F_f(r)−F_{f,M}(r)≤r/M for every r>0 and integer M≥1.

*Risk:* The fractional-part kernel oscillates infinitely often near t=0. A quadrature argument must isolate the initial interval and bound variation on the remaining interval uniformly in m and its residue class. The claimed dependence on M must survive summation over all m² residue classes.

## P5: The universal square kernel

Depends on: none  
Cites: none

Let B(t)={t}(1−{t}) for real t≥0, where {t}=t−floor(t), and let ζ denote the analytically continued Riemann zeta function. Define κ=∫₀^∞B(1/u²)du. This integral converges and κ=−4ζ(−1/2)>0. There is an absolute constant A>0 such that, uniformly for every real Z>0, |∑_{v≥1}B(Z/v²)−κ√Z|≤AZ^(1/3). The series converges absolutely for every Z>0.

*Risk:* The integral and the square-root scaling must be evaluated with the correct normalization. The error bound must include 0<Z<1 because arithmetic convolution produces such arguments.

## P6: Small-ratio expansion and the polynomial Euler product (CRUX)

Depends on: P5  
Cites: none

Let f and ρ be as in problem.md. Define C₀=∏_p(1−2/p²), a(m)=μ²(m)∏_{p|m}(p²−2)^(−1), B(t)={t}(1−{t}), and R_m(b)=m²/gcd(m²,f(b)), with gcd(m²,0)=m². For r>0 define F_f(r)=C₀∑_{m≥1}a(m)m^(−2)∑_{b=0}^{m²−1}∫₀ʳ tR_m(b)B(1/(tR_m(b)))dt, defining the integrand as zero at t=0. For each prime p put w₀(p)=1−ρ(p)/p, w₁(p)=ρ(p)/p−ρ(p²)/p², and w₂(p)=ρ(p²)/p². The product C_f=−(8/3)ζ(−1/2)∏_p(1−1/p)[1−2/p²+(p w₀(p)+√p w₁(p)+w₂(p))/p²] converges absolutely and is strictly positive. There is a constant A(f)>0 such that, uniformly for 0<r≤1, |F_f(r)−C_f r^(3/2)|≤A(f)r^(5/3). This assertion includes polynomials with repeated factors and fixed prime-square divisors.

*Risk:* The arithmetic factorization must distinguish valuations zero, one, and at least two, which produce factors p, √p, and 1 in the constant. A sufficient intermediate contract is to factor the relevant coefficient Dirichlet series as ζ(2s)G_f(s), with the coefficients γ_f(n) of G_f satisfying ∑_{n≥1}|γ_f(n)|n^(−1/3)≤A(f). Exceptional primes dividing the polynomial content must be retained.

## P7: Assembly and the uniform asymptotic range

Depends on: P3, P4, P6  
Cites: none

Let f satisfy problem.md, write d=deg(f) and Y=f(y), and define w₀(p)=1−ρ(p)/p, w₁(p)=ρ(p)/p−ρ(p²)/p², w₂(p)=ρ(p²)/p² for every prime p. Let C_f=−(8/3)ζ(−1/2)∏_p(1−1/p)[1−2/p²+(p w₀(p)+√p w₁(p)+w₂(p))/p²]. For every ε>0 there is a constant A(f,ε)>0 such that, uniformly for real x≥2 and y≥2 with Y≤x, |V_f(x,y)−C_f x^(1/2)Y^(3/2)|≤A(f,ε)[x^(1/3)Y^(5/3)+x^(5/3+ε)+xY√(log(2x)/y)]. Put θ_d=max(7/9,d/(d+1)). For every 0<δ<(1−θ_d)/2 there are constants A(f,δ)>0 and x₀(f,δ) such that, uniformly for x≥x₀(f,δ) and x^(θ_d+δ)≤Y≤x^(1−δ), |V_f(x,y)/(C_f x^(1/2)Y^(3/2))−1|≤A(f,δ)x^(−δ/6). Every constant is independent of x and y. In summing the individual-modulus errors, the required auxiliary bound is ∑_{1≤k≤y}f′(k)/f(k)≤A(f)log(2y), uniformly for y≥2.

*Risk:* The correlation error must be summed with f′(k)/f(k), preserving its logarithmic growth. The relative averaging error imposes the degree-dependent threshold d/(d+1), while the correlation error imposes 7/9.
