# Plan: dirichlet@gpt-6.1-sol

Model: codex:gpt-6.1-sol

Proposed six-proposition plan using squarefree pair correlations, polynomial averaging of local factors, and a generating Dirichlet series. Restrict f to Z[t] with no repeated complex root, retaining the original weight f'(k). This restriction supplies bounded root counts modulo p and p² outside finitely many primes and includes all three numerical examples. The plan gives a ratio-dependent main term up to f(y)=x, and a constant times x^(1/2)f(y)^(3/2) in a narrower range. The predicted constants agree with the numerical extrapolation ranges. The fitted exponents differ from (1/2,3/2), but the derived ratio-dependent term explains that discrepancy without changing the theorem to fit data. The Dirichlet-series organization follows the permitted supplied paper by J. Brüdern and T. D. Wooley, Sparse variance for primes in arithmetic progression (2011), §5, https://doi.org/10.1093/qmath/hap029; no prime-variance theorem is transferred. No excluded work was consulted. A search incidentally returned a 2026 CV and a current publication list; neither was opened or used. These are proposed contracts, not completed proofs.

## Main theorem

Restrict f to an integer-coefficient polynomial satisfying the assumptions in problem.md and gcd(f,f')=1 in Q[t]. Put Y=f(y), a_d=max{5/3,2-1/(2d)}, and λ_d=(2a_d-1)/3=max{7/9,1-1/(3d)}. Let Φ_f and the positive constant C_f be the explicit quantities defined in P5. For every 0<ε<min{1/8,1/(4d)}, there exist K_{f,ε}>0 and x_0(f,ε) such that, uniformly for real x≥x_0(f,ε) and real y≥1 with sqrt(x)≤Y≤x, |V_f(x,y)-x²Φ_f(Y/x)|≤K_{f,ε}x^(a_d+ε). In the same range, |V_f(x,y)-C_f x^(1/2)Y^(3/2)|≤K_{f,ε}[x^(1/4+ε)Y^(7/4-ε)+x^(a_d+ε)]. Consequently, for every 0<η<(1-λ_d)/2, there exist K_{f,η}>0 and x_1(f,η) such that, uniformly for x≥x_1(f,η) and x^(λ_d+η)≤Y≤x^(1-η), |V_f(x,y)/(C_f x^(1/2)Y^(3/2))-1|≤K_{f,η}x^(-η/5). Thus λ_1=7/9 and λ_d=1-1/(3d) for d≥2.

## Numerics check

Yes, with the distinction between fixed-ratio and vanishing-ratio limits. The reported extrapolated constants are 0.13837±0.00702, 0.13851±0.00729, and 0.14086±0.00816, respectively; all contain the predicted constants. At x=256,000,000, finite-product evaluations of the ratio-dependent formula have maximum relative discrepancies across the eight supplied ratios of approximately 0.071% for t²+1, 0.89% for t³+2, and 0.0011% for 2t+1. These evaluations are numerical checks, not certified error bounds. The larger cubic discrepancies are compatible with sparse endpoint effects, since the sampled y values are only 136–634. Independently, direct squarefree sieving and residue counting reproduced the complete x=1,000,000, y=99 quadratic row and y=21 cubic row: both displayed variances agreed, and both integer weighted count-square sums agreed exactly. The production implementation was unavailable, so its other validation claims were not independently audited. The persistent ratio curvature explains why joint power fits produce exponents near (0.45,1.55); their regression errors do not measure the uncertainty in the vanishing-ratio exponents or constant.

## P1: Local densities and uniform control of the centering term

Depends on: none  
Cites: R. C. Vaughan, A variance for k-free numbers in arithmetic progressions (2005), Lemma 2.2(ii), specialized to squarefree numbers and squarefree divisors r≤x, https://doi.org/10.1112/S0024611505015352.

Let δ=1/ζ(2), where ζ is the Riemann zeta function. For every integer q≥1 and integer l, define q_1=∏_{p||q}p, where p||q means p divides q but p² does not. The density in problem.md is g(q,l)=(δ/q)∏_{p|q}(1-p^(-2))^(-1)∏_{p||q, p|l}(1-p^(-1))∏_{p²|q}1_{p²∤l}. Empty products equal 1. Put G(q)=Σ_{l=1}^q g(q,l)². Then G(q)=(δ²/q)∏_{p||q}[(1-2p^(-2)+p^(-3))/(1-p^(-2))²]∏_{p²|q}(1-p^(-2))^(-1). There exists an absolute constant K>0 such that, uniformly for real x≥2 and integers 1≤q≤x, |Σ_{l=1}^q g(q,l)Q(x;q,l)-xG(q)|≤K sqrt(x)/q. Also |Q(x;1,1)-δx|≤K sqrt(x). No coprimality restriction on l is imposed.

*Risk:* Residues divisible by p when p||q have a different local factor from residues modulo p². Confusing these cases changes both the centering term and the final constant. Only Lemma 2.2(ii), which has no q≤x^(1-η) restriction, is required.

## P2: Squarefree pair correlations uniformly in the difference

Depends on: none  
Cites: none

For every positive integer r define S(r)=∏_p(1-2p^(-2))∏_{p²|r}(p²-1)/(p²-2), with products over primes. For real x≥2 and integers 1≤r≤x, define R(x;r)=Σ_{1≤n≤x-r}μ²(n)μ²(n+r), where the sum is empty when x-r<1. For every 0<ε<1/6 there exists K_ε>0 such that |R(x;r)-(x-r)S(r)|≤K_ε x^(2/3+ε), uniformly throughout these ranges. The constant is independent of r and x.

*Risk:* The assigned proof must establish uniformity for differences as large as x, rather than import a theorem for a fixed difference. Square-divisor truncation must retain the compatibility condition gcd(a,b)²|r when completing the singular series.

## P3: Discarding small polynomial moduli

Depends on: P1  
Cites: J. Brüdern, A. Granville, A. Perelli, R. C. Vaughan and T. D. Wooley, On the exponential sum over k-free numbers (1998), Lemma 2.2, with its k=2 and 1≤Q=Z≤x, https://www.math.purdue.edu/~twooley/publ/1998%20kfree.pdf.

Let f satisfy the assumptions of problem.md, allowing the original integer-valued rational coefficients. For every ε>0 there exists K_{f,ε}>0 such that, uniformly for real x≥2 and 2≤Z≤x, 0≤Σ_{k≥1, f(k)≤Z}f'(k)Σ_{l=1}^{f(k)}E(x;f(k),l)²≤K_{f,ε}x^(1+ε)Z^(2-1/d). The sum is over positive integers k. In particular, at Z=sqrt(x) this is at most K_{f,ε}x^(2-1/(2d)+ε).

*Risk:* The cited lemma uses a differently normalized density; P1 identifies it with the density in problem.md. Positivity and injectivity of k↦f(k) permit comparison with all moduli, and the derivative contributes the factor Z^(1-1/d).

## P4: Averaging singular series and density factors along the polynomial (CRUX)

Depends on: P1  
Cites: none

Let f∈Z[t] satisfy problem.md and have no repeated complex root. Put δ=1/ζ(2), C_0=∏_p(1-2p^(-2)), and S(r)=C_0∏_{p²|r}(p²-1)/(p²-2) for positive integers r. For every prime p put a_p=1/(p²-2), u_p=ρ(p)/p, v_p=ρ(p²)/p², b_{0,p}=1+a_pv_p, b_{1,p}=1+a_pu_p, and b_{j,p}=1+a_p for integers j≥2. For positive integers h, let v_p(h) be the exponent of p in h and define W_f(h)=∏_p(1-2p^(-2))b_{v_p(h),p}. Define c_f=∏_p(1-2p^(-2))[b_{0,p}+(b_{1,p}-b_{0,p})/p+(b_{2,p}-b_{1,p})/p²], G(q)=Σ_{l=1}^q g(q,l)², and P_f(H)=Σ_{1≤h≤H}W_f(h)(H-h)²/h for real H≥1. These products converge absolutely. There exist K_f>0 and x_0(f) such that the following estimates hold. First, uniformly for all integers h≥1 and real 1≤t_0≤t_1, |Σ_{t_0<k≤t_1}S(hf(k))-(t_1-t_0)W_f(h)|≤K_f. Second, uniformly for x≥x_0(f), f(1)≤Z≤Y=f(y)≤x, and the unique real z≥1 satisfying f(z)=Z, |Σ_{z<k≤y}f'(k)G(f(k))-c_f log(Y/Z)|≤K_f Z^(-1/d) and |Σ_{z<k≤y}f'(k)-(Y-Z)|≤K_f Y^(1-1/d). Finally, define M_f(x;z,y)=Σ_{z<k≤y}f'(k)Σ_{h≥1, hf(k)≤x}(x-hf(k))S(hf(k)). Uniformly in the same ranges, |2M_f(x;z,y)-Z²P_f(x/Z)+Y²P_f(x/Y)|≤K_f x²Z^(-1/d). All sums over k and h are over integers, and log denotes the natural logarithm.

*Risk:* The essential issue is summable discrepancy after expanding the singular series into square-divisibility conditions. The relevant modulus is r²/gcd(r²,h), so primes dividing h once and twice must be distinguished. All bad primes of f must remain in the local factors. The no-repeated-root restriction is essential to the proposed uniform summability argument.

## P5: Dirichlet series, contour shift, and explicit main terms (CRUX)

Depends on: none  
Cites: H. L. Montgomery and R. C. Vaughan, Multiplicative Number Theory I. Classical Theory (2007), Theorem 5.1 and equation (5.19) with smoothing order 2, https://doi.org/10.1017/CBO9780511618314., H. L. Montgomery and R. C. Vaughan, Multiplicative Number Theory I. Classical Theory (2007), Corollaries 1.16, 1.17, 10.4 and 10.5, https://doi.org/10.1017/CBO9780511618314.

Let f∈Z[t] satisfy problem.md and have no repeated complex root. For each prime p define a_p=1/(p²-2), u_p=ρ(p)/p, v_p=ρ(p²)/p², b_{0,p}=1+a_pv_p, b_{1,p}=1+a_pu_p, and b_{j,p}=1+a_p for j≥2. Let W_f(h)=∏_p(1-2p^(-2))b_{v_p(h),p}, where v_p(h) is the exponent of p in the positive integer h. Put T_p(s)=b_{0,p}+(b_{1,p}-b_{0,p})p^(-s)+(b_{2,p}-b_{1,p})p^(-2s), A_f(s)=∏_p(1-2p^(-2))T_p(s), and J_f(s)=∏_p(1-p^(-2s-2))(1-2p^(-2))T_p(s). The product for A_f converges absolutely and locally uniformly for Re(s)>-1/2, and the product for J_f does so for Re(s)>-3/4. For each 0<ε<1/8, |J_f(s)|≤K_{f,ε} uniformly for Re(s)≥-3/4+ε. For Re(s)>1, F_f(s)=Σ_{h≥1}W_f(h)h^(-s)=ζ(s)A_f(s)=ζ(s)ζ(2s+2)J_f(s); the last identity continues F_f meromorphically to Re(s)>-3/4. Put δ=1/ζ(2), c_f=A_f(1), B_f=c_f(γ-3/2)+A_f'(1), and C_f=-(8/3)ζ(-1/2)J_f(-1/2), where γ is Euler's constant. Then c_f>0, C_f>0, and F_f(0)=-δ/2. For P_f(H)=Σ_{1≤h≤H}W_f(h)(H-h)²/h, every 0<ε<1/8 admits K_{f,ε}>0 such that, uniformly for H≥1, P_f(H)=c_fH²log H+B_fH²+δH-C_fH^(1/2)+R_f(H), with |R_f(H)|≤K_{f,ε}H^(1/4+ε). The Mellin integral uses 2F_f(w+1)H^(w+2)/[w(w+1)(w+2)], initially on Re(w)=2 and shifted to Re(w)=-7/4+ε; there is no finite height or major-arc cutoff. Define, for 0<r≤1, Φ_f(r)=δr-r²P_f(1/r)+c_f log(1/r)+B_f. Then |Φ_f(r)-C_fr^(3/2)|≤K_{f,ε}r^(7/4-ε), uniformly for 0<r≤1. The constant C_f equals the Euler product stated in predicted_main_term. If that product is truncated to p≤R, its error in absolute value is at most K_f/R for every real R≥2, with K_f depending only on f.

*Risk:* The residue at w=-1 must cancel the squarefree diagonal exactly; an incorrect local factor changes F_f(0). The pole at w=-3/2 supplies the main constant. Absolute convergence of J_f and integrability on the shifted line must be checked explicitly, including finitely many bad primes; no zero-free region or hypothesis on zeta zeros is available or needed.

## P6: Reduction of the variance to the averaged pair model

Depends on: P1, P2, P3  
Cites: none

Let f∈Z[t] satisfy problem.md and have no repeated complex root. Put δ=1/ζ(2), a_d=max{5/3,2-1/(2d)}, G(q)=Σ_{l=1}^qg(q,l)², and S(r)=∏_p(1-2p^(-2))∏_{p²|r}(p²-1)/(p²-2) for positive integers r. For every 0<ε<1/8 there exist K_{f,ε}>0 and x_0(f,ε)≥f(1)² such that the following holds uniformly for real x≥x_0(f,ε) and y≥1 with sqrt(x)≤Y=f(y)≤x. Set Z=sqrt(x) and let z≥1 be the unique real solution of f(z)=Z. Define M_f(x;z,y)=Σ_{z<k≤y}f'(k)Σ_{h≥1, hf(k)≤x}(x-hf(k))S(hf(k)), with integer k,h. Then V_f(x,y)=δx(Y-Z)+2M_f(x;z,y)-x²Σ_{z<k≤y}f'(k)G(f(k))+R, where |R|≤K_{f,ε}x^(a_d+ε). The constant and threshold depend only on f and ε. Combining this identity with P4 and P5 gives the main theorem, including the ratio-dependent term and the stated relative rate in the power-law range.

*Risk:* The pair-correlation error is summed with total weight at most a constant depending on f times x log(2x); its contribution must be absorbed using a smaller ε in P2. Endpoint errors from replacing Σf'(k) by Y-Z must also be retained. Treating the small-modulus block by pair correlations would lose the required saving.
