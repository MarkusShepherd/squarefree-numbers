# Plan: thesis@gpt-6.1-sol

Model: codex:gpt-6.1-sol

Plan for the original class of polynomials and original weight. First obtain a uniform squarefree correlation estimate from the supplied exponential-sum paper; then average its singular series over polynomial moduli. This avoids requiring a new sparse-moduli variance theorem. The result retains an explicit profile when f(y)/x is fixed and yields a constant main term when f(y)/x tends to zero. The predicted constants agree with the numerical extrapolation bands. Methodological starting points: R. C. Vaughan, A variance for k-free numbers in arithmetic progressions (2005), https://doi.org/10.1112/S0024611505015352; J. Brüdern and T. D. Wooley, Sparse variance for primes in arithmetic progression (2011, supplied exception), https://doi.org/10.1093/qmath/hap029. Exposure report: a literature search returned metadata for an unrelated 2015 Journal of Number Theory article; it was not opened or used. No excluded-author source, GitLab content, or previous proof attempt was consulted. These are proposed proof contracts, not proved results.

## Main theorem

Let f and V_f be as in problem.md, let d=deg f, put Y=f(y), and define η_d=min{1/5,1/(4d−1)}. Let the explicit function F_f and positive constant K_f be defined in P5–P6. For every ε with 0<ε<η_d/2, there are constants C(f,ε)>0 and x_0(f,ε) such that, uniformly for real x≥x_0 and y≥1 with Y≤x, |V_f(x,y)−x²F_f(x/Y)|≤C(f,ε)x^(2−η_d+ε), and |V_f(x,y)−K_f x^(1/2)Y^(3/2)|≤C(f,ε)[x^(3/8)Y^(13/8)+x^(2−η_d+ε)]. In particular, for every fixed δ with 0<δ<η_d/3, uniformly in x^(1−2η_d/3+δ)≤Y≤x^(1−δ), |V_f(x,y)/(K_f x^(1/2)Y^(3/2))−1|≤C(f,δ)x^(−δ/8). No irreducibility or squarefreeness assumption on f is imposed.

## Numerics check

Yes, with the distinction between the profile and its small-ratio limit. The snapshot extrapolates constants 0.134475±0.007285, 0.136321±0.002404, and 0.141686±0.008218, respectively; all three proposed constants lie within these heuristic bands. At the largest x, evaluating the explicit profile at each actual recorded ratio gives maximum relative differences across the eight requested ratios of approximately 0.071%, 0.90%, and 0.00075%, respectively. The larger cubic discrepancy is compatible with slower convergence of the polynomial sampling, but is not established as such. Persistent ratio dependence explains why unrestricted power-law regression does not recover exponents 1/2 and 3/2 exactly. The snapshot reports exact-integer count validation and high-precision density evaluation; its implementation was not independently inspected, and its extrapolation uncertainty is not treated as a rigorous error bound.

## P1: Local densities and summable spectral coefficients

Depends on: none  
Cites: R. C. Vaughan, A variance for k-free numbers in arithmetic progressions (2005), Lemmas 2.5, 2.14, 2.15 and 2.17, specialized to k=2; https://doi.org/10.1112/S0024611505015352., J. Brüdern, A. Granville, A. Perelli, R. C. Vaughan and T. D. Wooley, On the exponential sum over k-free numbers (1998), Lemma 3.1, specialized to k=2; https://research-information.bris.ac.uk/en/publications/on-the-exponential-sum-over-k-free-numbers/.

Let μ be the Möbius function, φ Euler's totient, ζ the Riemann zeta function, and c=ζ(2)^(−1). All products below are over primes. For every integer q≥1 and integer l, the density g(q,l) from problem.md equals q^(−1)Σ_{m≥1, gcd(m²,q)|l} μ(m)gcd(m²,q)/m². Equivalently, it is zero if some p² divides both q and l; otherwise it equals (c/q)∏_{p|q}(1−p^(−2))^(−1)∏_{p||q, p|l}(1−p^(−1)). In particular 0≤g(q,l)≤1/q. Define the multiplicative function G by G(1)=1, G(p)=G(p²)=−1/(p²−1), and G(p^a)=0 for a≥3. Put γ(r)=cG(r), λ(r)=φ(r)γ(r)², and c_r(n)=Σ_{1≤a≤r, gcd(a,r)=1} exp(2πian/r). Then qΣ_{l=1}^q g(q,l)²=Σ_{r|q}λ(r), Σ_{r≥1}λ(r)=c, and, for every integer n≥1, the absolutely convergent series Σ_{r≥1}γ(r)²c_r(n) equals 𝔖(n)=∏_p(1−2/p²)∏_{p²|n}(p²−1)/(p²−2). There is an absolute constant C such that, uniformly for real R≥2, Σ_{r>R}λ(r)≤CR^(−1/2)(log(2R))² and Σ_{r≤R}rλ(r)≤CR^(1/2)(log(2R))².

*Risk:* The Fourier coefficient includes ζ(2)^(−1); omitting it changes both the density cancellation and the final constant. Residue classes not coprime to q must remain included.

## P2: Variance reduction and disposal of initial moduli

Depends on: P1  
Cites: R. C. Vaughan, A variance for k-free numbers in arithmetic progressions (2005), Lemmas 2.2(ii), 2.3 and 2.4, specialized to k=2; https://doi.org/10.1112/S0024611505015352., J. Brüdern, A. Granville, A. Perelli, R. C. Vaughan and T. D. Wooley, On the exponential sum over k-free numbers (1998), Lemma 2.2, specialized to k=2 and 1≤Q≤x; https://research-information.bris.ac.uk/en/publications/on-the-exponential-sum-over-k-free-numbers/.

Let f be as in problem.md, d=deg f, and c=ζ(2)^(−1), where ζ is the Riemann zeta function. For real x≥2 and integers 1≤m≤x define C_x(m)=Σ_{1≤n≤x−m}μ²(n)μ²(n+m). For real 1≤z≤y with Z=f(z)≤Y=f(y)≤x, define V_f(x;z,y)=Σ_{z<k≤y}f'(k)Σ_{l=1}^{f(k)}E(x;f(k),l)², T_f(z,y)=Σ_{z<k≤y}f'(k)Σ_{l=1}^{f(k)}g(f(k),l)², and S_f(x;z,y)=Σ_{z<k≤y}f'(k)Σ_{1≤h≤x/f(k)}C_x(hf(k)); all sums over k and h are over positive integers. For every ε>0 there is C(f,ε)>0 such that, uniformly throughout these ranges, |V_f(x;z,y)−[cx(Y−Z)+2S_f(x;z,y)−x²T_f(z,y)]|≤C(f,ε)[x^(3/2+ε)+xY^(1−1/d)]. In addition, uniformly for x≥2 and real z≥1 with f(z)≤x, 0≤V_f(x,z)≤C(f,ε)x^(1+ε)f(z)^(2−1/d).

*Risk:* The initial-modulus bound must use positivity before multiplying the full-modulus variance bound by the maximum polynomial weight. The mixed term requires divisibility counts, rather than a pointwise progression error multiplied by every residue class.

## P3: Uniform correlation estimate for squarefree numbers

Depends on: P1  
Cites: J. Brüdern, A. Granville, A. Perelli, R. C. Vaughan and T. D. Wooley, On the exponential sum over k-free numbers (1998), Theorem 2 and Lemmas 3.1, 3.2 and 4.2, specialized to k=2; https://research-information.bris.ac.uk/en/publications/on-the-exponential-sum-over-k-free-numbers/.

For real x≥2 and every integer 1≤m≤x, define C_x(m)=Σ_{1≤n≤x−m}μ²(n)μ²(n+m) and 𝔖(m)=∏_p(1−2/p²)∏_{p²|m}(p²−1)/(p²−2), with products over primes. For every ε>0 there is C(ε)>0 such that |C_x(m)−(x−m)𝔖(m)|≤C(ε)x^(4/5+ε), uniformly for all such x and m. A permitted circle-method cutoff is Q=x^(2/5), for x sufficiently large that Q≤x^(1/2)/2; the major arcs are the subsets of R/Z with |α−a/q|≤Q/(qx), 1≤q≤Q and gcd(a,q)=1. The bound is uniform even when x−m is bounded.

*Risk:* This is a difference-correlation adaptation of the supplied mean-square estimates, not a direct quotation of the paper's additive-representation corollary. Uniformity must come from an L¹ bound for the Fourier approximation, with x retained as the ambient length.

## P4: Polynomial averaging with a common density coefficient (CRUX)

Depends on: P1  
Cites: none

Let f and ρ be as in problem.md, d=deg f, and put ρ(1)=1. Write ζ for the Riemann zeta function, c=ζ(2)^(−1), and φ for Euler's totient. Define λ(r)=c²φ(r)∏_{p|r}(p²−1)^(−2) when no prime cube divides r, and λ(r)=0 otherwise; the product for r=1 is empty. Define R_f=Σ_{r≥1}λ(r)ρ(r)/r and 𝔖(n)=∏_p(1−2/p²)∏_{p²|n}(p²−1)/(p²−2). For h≥1 let v_p(h) be the exponent of p in h, j_p(h)=max{2−v_p(h),0}, and W_f(h)=∏_p(1−2/p²)[1+ρ(p^{j_p(h)})/(p^{j_p(h)}(p²−2))]. These series and products converge absolutely. For real x≥2, 1≤z≤y, Z=f(z)≤Y=f(y)≤x, and 2≤R≤x, put A=Z^(−1/d)R^(1/2)(log(2R))²+R^(−1/2)(log(2R))²log(2x). There is C(f)>0, uniform throughout these ranges, such that |Σ_{z<k≤y}f'(k)Σ_{l=1}^{f(k)}g(f(k),l)²−R_f log(Y/Z)|≤C(f)A, and |Σ_{z<k≤y}f'(k)Σ_{1≤h≤x/f(k)}(x−hf(k))𝔖(hf(k))−∫_Z^Y Σ_{1≤h≤x/t}(x−ht)W_f(h)dt|≤C(f)x²A. All discrete summation variables are positive integers. No condition on the discriminant, content, or factorization of f is imposed.

*Risk:* The same R_f must occur in the density average and the off-diagonal expansion. The Euler-summation error must be summed using the h-dependent endpoint f(k)≤x/h; using y for every h would lose the claimed range. Fixed prime divisors and repeated polynomial factors must be retained.

## P5: Dirichlet series, residues, and the explicit constant (CRUX)

Depends on: P4  
Cites: none

Let f and ρ be as in problem.md, set ρ(1)=1, and write ζ for the Riemann zeta function. For each prime p define a_p=1+ρ(p²)/(p²(p²−2)), b_p=1+ρ(p)/(p(p²−2)), c_p=1+1/(p²−2), and B_p(s)=a_p+(b_p−a_p)p^(−s)+(c_p−b_p)p^(−2s). Define W_f(h)=∏_p(1−2/p²)[1+ρ(p^{max{2−v_p(h),0}})/(p^{max{2−v_p(h),0}}(p²−2))] for positive integers h, where v_p(h) is the exponent of p in h. Put D_f(s)=Σ_{h≥1}W_f(h)h^(−s), P_f(s)=∏_p(1−2/p²)B_p(s), and H_f(s)=∏_p(1−2/p²)(1−p^(−2s−2))B_p(s). The series for D_f converges absolutely for Re(s)>1; the products for P_f and H_f converge absolutely and locally uniformly for Re(s)>−1/2 and Re(s)>−3/4, respectively. For Re(s)>1, D_f(s)=ζ(s)P_f(s)=ζ(s)ζ(2s+2)H_f(s), and the latter identity continues D_f meromorphically to Re(s)>−3/4. For every fixed σ>−3/4 there is C(f,σ)>0 with |H_f(σ+it)|≤C(f,σ) for all real t. Define R_f=P_f(1), B_f=(γ_E−3/2)R_f+P_f'(1), where γ_E is Euler's constant, and K_f=−(8/3)ζ(−1/2)H_f(−1/2). Then D_f(0)=−1/(2ζ(2)), K_f>0, and R_f=ζ(2)^(−2)∏_p[1+(1−1/p)(ρ(p)+ρ(p²))/(p²−1)²]. This R_f equals Σ_{r≥1}λ(r)ρ(r)/r, where λ(r)=ζ(2)^(−2)φ(r)∏_{p|r}(p²−1)^(−2) for integers r with no prime-cube divisor and is zero otherwise; φ is Euler's totient. Every displayed Euler product specifying R_f or K_f is absolutely convergent.

*Risk:* The pole at s=−1/2 determines the constant. Missing either ρ(p²) or the factor 1/2 in the residue of ζ(2s+2) changes the answer. The identity D_f(0)=−1/(2ζ(2)) is essential for cancellation of the diagonal term.

## P6: Smoothed singular-series sum and the ratio profile

Depends on: P5  
Cites: R. C. Vaughan, A variance for k-free numbers in arithmetic progressions (2005), Lemma 2.18, for the Mellin-transform framework; https://doi.org/10.1112/S0024611505015352., H. L. Montgomery and R. C. Vaughan, Multiplicative Number Theory I: Classical Theory (2007), Corollary 10.4, the zeta functional equation; https://doi.org/10.1017/CBO9780511618314.

Let f and ρ be as in problem.md and put ρ(1)=1. For each integer h≥1 define W_f(h)=∏_p(1−2/p²)[1+ρ(p^{max{2−v_p(h),0}})/(p^{max{2−v_p(h),0}}(p²−2))], where products are over primes and v_p(h) is the exponent of p in h. Let D_f(s)=Σ_{h≥1}W_f(h)h^(−s), initially for Re(s)>1 and then by meromorphic continuation. Define R_f=Res_{s=1}D_f(s), B_f=lim_{s→1}[D_f(s)−R_f/(s−1)]−3R_f/2, K_f=−(16/3)Res_{s=−1/2}D_f(s), and c=ζ(2)^(−1), with ζ the Riemann zeta function. For real H≥1 put Θ_f(H)=Σ_{1≤h≤H}W_f(h)(H−h)²/h and F_f(H)=R_f log H+B_f+c/H−Θ_f(H)/H². There is C(f)>0 such that, uniformly for all real H≥1, |Θ_f(H)−[R_fH²log H+B_fH²+cH−K_fH^(1/2)]|≤C(f)H^(3/8), and consequently |F_f(H)−K_fH^(−3/2)|≤C(f)H^(−13/8). Moreover, uniformly for real x≥2 and 2≤Z≤Y≤x, 2∫_Z^Y Σ_{1≤h≤x/t}(x−ht)W_f(h)dt=Z²Θ_f(x/Z)−Y²Θ_f(x/Y).

*Risk:* The Mellin kernel is 2/[s(s+1)(s+2)] applied to D_f(s+1). The residue at s=−1 has a negative kernel residue, producing +cH. A sign error there prevents diagonal cancellation. The contour shift to Re(s)=−13/8 must include an explicit integrable vertical bound.

## P7: Assembly and uniform error budget

Depends on: P2, P3, P4, P5, P6  
Cites: none

Let f and V_f be as in problem.md, d=deg f, Y=f(y), and η_d=min{1/5,1/(4d−1)}. Define W_f(h)=∏_p(1−2/p²)[1+ρ(p^{max{2−v_p(h),0}})/(p^{max{2−v_p(h),0}}(p²−2))], with ρ(1)=1 and v_p(h) the exponent of p in h. Let D_f(s)=Σ_{h≥1}W_f(h)h^(−s), continued meromorphically; put R_f=Res_{s=1}D_f(s), B_f=lim_{s→1}[D_f(s)−R_f/(s−1)]−3R_f/2, K_f=−(16/3)Res_{s=−1/2}D_f(s), Θ_f(H)=Σ_{1≤h≤H}W_f(h)(H−h)²/h, and F_f(H)=R_f log H+B_f+1/(ζ(2)H)−Θ_f(H)/H². For every 0<ε<η_d/2 there are C(f,ε)>0 and x_0(f,ε) such that, uniformly for real x≥x_0 and y≥1 with Y≤x, |V_f(x,y)−x²F_f(x/Y)|≤C(f,ε)x^(2−η_d+ε) and |V_f(x,y)−K_f x^(1/2)Y^(3/2)|≤C(f,ε)[x^(3/8)Y^(13/8)+x^(2−η_d+ε)]. Permitted auxiliary choices for Y≥x^θ are θ=2d/(4d−1), Z=x^θ, the real z≥1 satisfying f(z)=Z, and R=Z^(1/d) in P4; for Y<Z the initial-modulus bound applies directly. All constants may depend only on the indicated f and ε.

*Risk:* All logarithmic losses must be absorbed using portions of ε fixed in advance. The correlation error summed over h contributes x^(9/5+ε), explaining the cap η_d≤1/5. The theorem must cover real y, including the gap between y and its integer part.
