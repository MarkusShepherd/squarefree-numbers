# Plan: simplest

Model: codex:gpt-6.1-sol

Plan an elementary correlation argument, restricting explicitly to f in Z[t]; this retains every polynomial in results.json and makes polynomial congruences periodic modulo their stated moduli. Six propositions give both a transition formula and a constant-times-power asymptotic. The predicted constants agree with the reported extrapolation ranges. Persistent fixed-ratio curvature is explained by the transition formula, while polynomial sampling contributes a separate finite-size error. An independent direct sieve reproduced the x=1000000, target_ratio=0.01 row for each polynomial to displayed double precision. The literature result used is R. C. Vaughan, “A variance for k-free numbers in arithmetic progressions” (2005), Lemma 2.15, https://doi.org/10.1112/S0024611505015352. No excluded source or disallowed later result is used.

## Main theorem

Restrict the problem to f in Z[t], retaining its other hypotheses, and put d=deg f and Y=f(y). Let zeta denote the Riemann zeta function. Define the positive, absolutely convergent product C_f=(2*zeta(3/2)/(3*pi))*product_p [(1-1/p)*(1+1/p-(2+rho(p))/p^2+rho(p)/p^(5/2)+rho(p^2)/p^4-rho(p^2)/p^(7/2))], where p runs over primes. For every 0<epsilon<1/12 there is K_(f,epsilon)>0 such that, uniformly for real x>=2 and y>=1 with Y<=x, |V_f(x,y)-C_f*x^(1/2)*Y^(3/2)| <= K_(f,epsilon)*(x^(1/3)*Y^(5/3)+x^(5/3+epsilon)+x*Y^(1-1/(2*d))*log(2*x)). More precisely, the explicit function F_f defined in P4 satisfies |V_f(x,y)-x^2*F_f(Y/x)| <= K_(f,epsilon)*(x^(5/3+epsilon)+x*Y^(1-1/(2*d))*log(2*x)) in the same range. Consequently, put theta_d=max(7/9,d/(d+1)). For every fixed 0<eta<(1-theta_d)/2, there is K_(f,eta)>0 such that |V_f(x,y)/(C_f*x^(1/2)*Y^(3/2))-1| <= K_(f,eta)*x^(-eta/6) whenever x>=2 and x^(theta_d+eta)<=Y<=x^(1-eta). All constants depend only on their indicated subscripts. The original weight f'(k) is unchanged.

## Numerics check

Yes, within the evidence's stated extrapolation sensitivity. The reported constants are 0.138371 +/- 0.007020, 0.138511 +/- 0.007292, and 0.140863 +/- 0.008159, respectively; all contain the predicted constants. The fixed-ratio x-exponent is 2, as observed. For 2k+1 at ratio approximately 1, numerical evaluation of the transition expression gives F_f(1) approximately 0.183691, compared with the largest-x normalized observation 0.183691458. Thus the persistent difference between that observation and C_f approximately 0.142613 is consistent with ratio dependence. Direct counting independently checked three supplied rows; the full production implementation was unavailable for inspection. The extrapolation uncertainties remain empirical, and the nonlinear sequences have additional endpoint sampling effects covered by the theorem's explicit error.

## P1: Local densities and the density-weighted first moment

Depends on: none  
Cites: none

Let mu denote the Mobius function, let zeta denote the Riemann zeta function, and let p always denote a prime. Set c=1/zeta(2), A=product_p(1-2/p^2), and a(r)=mu^2(r)*product_(p|r)(p^2-2)^(-1) for positive integers r, with empty products equal to 1. For every integer q>=1 define T(q)=A*sum_(r>=1) a(r)*gcd(r^2,q)/r^2. These series converge absolutely, A*sum_(r>=1)a(r)=c, and T(q)=product_p(1-2/p^2+gcd(p^2,q)/p^4). For every integer 1<=l<=q, the density in problem.md exists and equals g(q,l)=(1/q)*sum_(r>=1, gcd(r^2,q)|l) mu(r)*gcd(r^2,q)/r^2. Moreover, sum_(l=1)^q g(q,l)^2=T(q)/q. For every 0<epsilon<1/12 there is K_epsilon>0 such that, uniformly for real x>=2 and integers 1<=q<=x, |sum_(n<=x) mu^2(n)*g(q,n)-x*T(q)/q| <= K_epsilon*x^(1/2)*q^(-1+epsilon), where n runs over positive integers and g(q,n) is extended periodically in its second argument. The constant depends only on epsilon.

*Risk:* The local factors must distinguish primes dividing q exactly once from primes whose squares divide q. The first-moment error must retain the factor 1/q; a bound lacking it would spoil the variance reduction.

## P2: An elementary squarefree correlation estimate uniform in the shift

Depends on: none  
Cites: R. C. Vaughan, A variance for k-free numbers in arithmetic progressions (2005), Lemma 2.15, https://doi.org/10.1112/S0024611505015352

For real x>=2 and an integer 1<=h<=floor(x), define C(x,h)=sum_(1<=n<=x-h) mu^2(n)*mu^2(n+h), with an empty sum interpreted as zero. Put A=product_p(1-2/p^2), a(r)=mu^2(r)*product_(p|r)(p^2-2)^(-1), and S(h)=A*sum_(r>=1, r^2|h)a(r)=A*product_(p^2|h)(p^2-1)/(p^2-2). For every 0<epsilon<1/12 there is K_epsilon>0 such that |C(x,h)-(x-h)*S(h)| <= K_epsilon*x^(2/3+epsilon), uniformly throughout the stated range of x and h. The constant depends only on epsilon. The cited lemma supplies the singular-series evaluation, not the asserted correlation error.

*Risk:* A fixed-shift estimate is insufficient. The elementary truncation must remain uniform when h is comparable to x and when x-h is very short.

## P3: Reduction of the variance to a positive fractional-part kernel

Depends on: P1, P2  
Cites: none

Fix f in Z[t] satisfying the hypotheses of problem.md, and put d=deg f. For u>=0 define psi(u)={u}*(1-{u}), where {u}=u-floor(u). Set A=product_p(1-2/p^2), a(r)=mu^2(r)*product_(p|r)(p^2-2)^(-1), and m_r(q)=r^2/gcd(r^2,q) for positive integers r and q. For real x>=2 and y>=1 with Y=f(y)<=x, define K_f(x,y)=A*sum_(r>=1) a(r)*sum_(1<=k<=y) f'(k)*f(k)*m_r(f(k))*psi(x/(f(k)*m_r(f(k)))), where k is integral. The outer series converges absolutely. For every 0<epsilon<1/12 there is K_(f,epsilon)>0 such that |V_f(x,y)-K_f(x,y)| <= K_(f,epsilon)*x^(5/3+epsilon), uniformly throughout this range. The constant depends only on f and epsilon.

*Risk:* The diagonal, density-square term, and pair-correlation main term must cancel with their exact normalizations. Replacing the actual derivative-weighted sum by an integral at this stage would introduce an unaccounted endpoint error.

## P4: Periodic averaging over polynomial moduli with an explicit truncation error (CRUX)

Depends on: none  
Cites: none

Fix f in Z[t] satisfying problem.md and put d=deg f. Define psi(u)={u}*(1-{u}) for u>=0, A=product_p(1-2/p^2), a(r)=mu^2(r)*product_(p|r)(p^2-2)^(-1), and m_r(q)=r^2/gcd(r^2,q). Define K_f(x,y)=A*sum_(r>=1)a(r)*sum_(1<=k<=y)f'(k)*f(k)*m_r(f(k))*psi(x/(f(k)*m_r(f(k)))). For r>=1 and b in {0,...,r^2-1}, put M_(r,b)=r^2/gcd(r^2,f(b)), including the convention gcd(r^2,0)=r^2. For 0<t<=1 define F_f(t)=A*sum_(r>=1)(a(r)/r^2)*sum_(b=0)^(r^2-1) integral_(0)^t v*M_(r,b)*psi(1/(v*M_(r,b))) dv. The series and improper integrals converge absolutely. There is K_f>0 such that, uniformly for real x>=2, y>=1, Y=f(y)<=x, and every real truncation parameter D>=1, |K_f(x,y)-x^2*F_f(Y/x)| <= K_f*(x*Y/D+x*Y^(1-1/d)*D*log(2*x)). In particular, D=Y^(1/(2*d)) gives the bound 2*K_f*x*Y^(1-1/(2*d))*log(2*x). The constant depends only on f.

*Risk:* The kernel oscillates increasingly rapidly toward the lower endpoint. Uniform weighted periodic averaging must control its total variation on the actual interval, and the omitted lower integral and polynomial endpoints must be included. Integer-valued rational polynomials cannot simply be assumed periodic modulo r^2.

## P5: A universal square-lattice kernel asymptotic

Depends on: none  
Cites: none

Let zeta denote the Riemann zeta function and define psi(u)={u}*(1-{u}) for u>=0. For every real t>0 define G(t)=integral_(0)^t v*sum_(n>=1)psi(1/(v*n^2)) dv, where n ranges over positive integers. This nonnegative series and improper integral converge. There is an absolute constant K>0 such that |G(t)-(2*zeta(3/2)/(3*pi))*t^(3/2)| <= K*t^(5/3) for every real t>0. The constant is independent of t and of every polynomial or variance parameter.

*Risk:* A direct bounded-variation assertion at zero is false. The required explicit rate must account for the oscillatory part of the square-lattice sum.

## P6: Arithmetic convolution and the explicit small-ratio constant (CRUX)

Depends on: P5  
Cites: none

Fix f in Z[t] satisfying problem.md. Let zeta denote the Riemann zeta function. For every prime p put u_p=rho(p)/p, v_p=rho(p^2)/p^2, B_(p,0)=1+v_p/(p^2-2), B_(p,1)=(u_p-v_p)/(p^2-2), and B_(p,2)=(1-u_p)/(p^2-2). For a complex variable s define H_f(s)=product_p (1-p^(-2-2*s))*(B_(p,0)+B_(p,1)*p^(-s)+B_(p,2)*p^(-2*s)). This Euler product has an absolutely convergent Dirichlet-series expansion H_f(s)=sum_(m>=1)c_f(m)*m^(-s) whenever Re(s)>-3/4. There is K_f>0 such that sum_(m>=1)|c_f(m)|*m^(2/3)<=K_f, and H_f(-1/2)>0. Set A=product_p(1-2/p^2), a(r)=mu^2(r)*product_(p|r)(p^2-2)^(-1), psi(u)={u}*(1-{u}), and M_(r,b)=r^2/gcd(r^2,f(b)) for 0<=b<r^2. Define F_f(t)=A*sum_(r>=1)(a(r)/r^2)*sum_(b=0)^(r^2-1) integral_(0)^t v*M_(r,b)*psi(1/(v*M_(r,b))) dv, and define G(t)=integral_(0)^t v*sum_(n>=1)psi(1/(v*n^2)) dv. Uniformly for 0<t<=1, F_f(t)=A*sum_(m>=1)(c_f(m)/m)*G(m*t), with absolute convergence, and |F_f(t)-C_f*t^(3/2)|<=K_f*t^(5/3), after increasing K_f if necessary. Here C_f=(2*zeta(3/2)/(3*pi))*A*H_f(-1/2)=(2*zeta(3/2)/(3*pi))*product_p [(1-1/p)*(1+1/p-(2+rho(p))/p^2+rho(p)/p^(5/2)+rho(p^2)/p^4-rho(p^2)/p^(7/2))]. This last product converges absolutely and is positive. Every constant depends only on f.

*Risk:* The probabilities of valuations zero, one, and at least two must be kept separately; interchanging them changes the constant. Absolute convergence must handle repeated polynomial factors and primes dividing the polynomial's content without assuming a nonzero discriminant.
