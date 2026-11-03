# Plan: simplest@claude-opus-5-5

Model: claude-opus-5-5

Strategy (elementary, no circle method). For one modulus q, write V(x;q)=sum_{l=1}^q E(x;q,l)^2. Opening the square and counting pairs n'=n+hq gives an EXACT identity (P2). It splits V(x;q) into four pieces: (i) an explicit arithmetic 'main term' MT(x;q) = A_0 q sum_t eta(t) m_t(q) B(x/(q m_t(q))) with B(u)={u}(1-{u}); (ii) 2*sum_{h<=x/q} D_x(hq), where D_x(m) is the error in the asymptotic for #{n: n, n+m squarefree}; (iii) Q(x)-6x/pi^2; (iv) -2x*sum_l g(q,l)E(x;q,l). In (i), the x^2 and x terms of sum_h A(hq)(x-hq) cancel exactly against x^2*sum g^2 and the diagonal 6x/pi^2. The leftover sawtooth-type terms B(.) are exactly the source of the x^{1/2}q^{1/2} size of the variance.

Each piece is then handled by elementary means:
- (ii) by the classical uniform bound D_x(m) << x^{2/3+eps}, Mirsky-type (P3). Mirsky is cited only as background; the prover must prove it.
- (iii) and (iv) by O(sqrt x) counting (P4).
- (i) by Euler–Maclaurin on sum_s B(Z/s^2) = I sqrt(Z) + O(Z^{1/3}), with I = int_0^infty B(u^{-2}) du = -4 zeta(-1/2) (P5, P6).

This yields a per-modulus asymptotic V(x;q) = h(q) sqrt(xq) + error with an explicit multiplicative-type h (P7). Averaging h over polynomial values with weight f'(k) f(k)^{1/2} is a routine divisor-sum argument using rho(p) <= d and rho(p^2) <= dp for p not dividing the content of f (P8). P9 assembles the result.

Range: the pointwise bound in P3 is the bottleneck, so the asymptotic holds for x^{7/9+delta} <= f(y) <= x^{1-delta}. This is deliberately weaker than what the circle method (Vaughan 2005 / Brüdern–Wooley) should give, in exchange for a fully elementary proof. Statement (a) of the theorem, V_f = sum_k f'(k) MT(x;f(k)) + O(x^{5/3+eps} + x^{1/2} f(y)), remains meaningful up to f(y) ~ x. It captures the x^2 F(x/Q)-type shape seen in the data.

Consistency checks I ran (scripts in work/):
1. Averaging my h(q) over ALL moduli gives (2/3)·mean(h) = 0.1284787. Vaughan's constant c_2 = 8 C_1 (-zeta(-1/2)) / (3 zeta(2)^2) (Vaughan 2005, (1.14)–(1.15)) evaluates to 0.1284787. They agree to 7 digits, which independently confirms the per-modulus main term.
2. The identity sum_l g(q,l)^2 = (A_0/q) sum_t eta(t) gcd(t^2,q)/t^2 checked exactly for q <= 50, up to the Euler-product truncation.
3. For f = k^2+1 at x = 10^6 and 4·10^6, sum_k f'(k) MT(x;f(k)) reproduces the tabulated V to within 0.1% at every ratio f(y)/x from 0.01 to 1.

No discrepancy with results.json. Two remarks:
- The data's finite-ratio drift (normalised value rising from about 0.140 at r=0.005 to 0.17–0.18 at r=1) is a genuine secondary term of relative size about sqrt(f(y)/x). It comes from sum_s B(Z/s^2) - I sqrt(Z) = O(1)-type corrections and is captured exactly by MT. My proven error (f(y)/x)^{1/6} is weaker than this but correct.
- The numerics' extrapolated constants (C + a sqrt(r) + b r fits) agree with the predicted C_f within their stated uncertainties.

Sources used: only the supplied papers (Vaughan 2005, for the definition of g and the constant check). L. Mirsky, 'Arithmetical pattern problems relating to divisibility by rth powers', Proc. London Math. Soc. (2) 50 (1949) 497–508, is named only as the classical origin of P3; I did not read it, and the prover must prove P3 directly. No web search was done. No work by the excluded author and no excluded paper was searched for, opened or used. No post-2010 source was used.

## Main theorem

Notation. Let f in Z[t] have degree d >= 1 with f(t) >= 2 and f'(t) >= 1 for t >= 1. Let rho(m) = #{a mod m : f(a) ≡ 0 mod m}. Write Y = f(y).

Define
  tau_p = (1 - 3/p^2 + 2/p^3)(1 - rho(p)/p) + ((p-1)(p^2 - 2 + sqrt p)/p^3)(rho(p)/p - rho(p^2)/p^2) + ((p-1)^2 (p+1)/p^3)(rho(p^2)/p^2),
and
  C_f = (2/3) · (-4 zeta(-1/2)) · prod_p tau_p.
The product converges absolutely and C_f > 0. Here -4 zeta(-1/2) = 0.8315448999...

Theorem. Fix eps > 0. Uniformly for real x >= 2 and real y >= 1 with f(y) <= x,

  V_f(x,y) = C_f x^{1/2} Y^{3/2} + O_{f,eps}( x^{1/3+eps} Y^{5/3} + x^{5/3+eps} + x^{1/2+eps} Y^{3/2 - 1/(2d)} ).

Moreover:

(a) Exact-shape version. Uniformly in the same range,
  V_f(x,y) = sum_{1<=k<=y} f'(k) MT(x; f(k)) + O_{f,eps}( x^{5/3+eps} + x^{1/2} Y ).
Here MT(x;q) = A_0 q sum_{t>=1} eta(t) m_t(q) B(x/(q m_t(q))), with
- A_0 = prod_p (1 - 2/p^2),
- eta(t) = mu^2(t) prod_{p|t} (p^2 - 2)^{-1},
- m_t(q) = t^2 / gcd(t^2, q),
- B(u) = {u}(1 - {u}).

(b) Asymptotic range. For each fixed delta in (0, 1/9), uniformly for x^{7/9+delta} <= f(y) <= x^{1-delta},
  V_f(x,y) = C_f x^{1/2} f(y)^{3/2} (1 + O_{f,delta}(x^{-eta})),   with eta = min(delta/12, 1/(6d)).

The weight f'(k) and the class of f are exactly as in problem.md; no change.

## Numerics check

Yes.

Exponents: the fixed-ratio fits give alpha + beta = 2.0008 (k^2+1), 1.998 (k^3+2) and 2.0001 (2k+1), against the predicted 2. The fixed-x beta of about 1.54–1.55 is inflated by the secondary term described below.

Constants: results.json extrapolates (to ratio -> 0) 0.1345 ± 0.0073 for k^2+1, 0.1363 ± 0.0024 for k^3+2 and 0.1417 ± 0.0082 for 2k+1. The predictions are 0.13808, 0.13561 and 0.14261, all inside the stated envelopes. At ratio 0.005 the normalised values are 0.1404, 0.1402 and 0.1446, about 1.5–2% above C_f.

That excess is explained, not a discrepancy. Replacing h(q) sqrt(xq) by the exact per-modulus term MT(x;q) (theorem part (a)), I computed sum_k f'(k) MT(x;f(k)) for k^2+1 at x = 10^6 and 4·10^6. V/that sum lies between 0.9992 and 1.0010 for every ratio from 0.01 to 1. The cruder h-approximation overshoots by 1.6% at ratio 0.01 and 9% at ratio 0.1, which is consistent with a secondary term of relative size about sqrt(f(y)/x).

The data can't distinguish the exponent of that correction from my proven, weaker error (f(y)/x)^{1/6}, but nothing in the data contradicts the theorem.

## P1: Closed form and moments of g(q,l)

Depends on: none  
Cites: Vaughan 2005, eq. (1.2) and (1.4) (formula and limit property of f(q,a), case k=2)

Notation: mu is the Mobius function, A_0 = prod_p (1 - 2/p^2), eta(t) = mu^2(t) prod_{p|t} (p^2-2)^{-1}. For q in N and l in Z, g(q,l) = lim_{x->oo} Q(x;q,l)/x (problem.md).

Claims. For every q in N and l in Z:

(i) The limit g(q,l) exists, and g(q,l) = sum_{d>=1} mu(d) · gcd(d^2,q)/(d^2 q) · 1[gcd(d^2,q) | l]. The series converges absolutely. Also 0 <= g(q,l) <= 1/q, and g(q,l) depends only on l mod q.

(ii) sum_{l=1}^q g(q,l) = 6/pi^2.

(iii) For squarefree n,
  g(q,n) = (6/pi^2) · q^{-1} · prod_{p|q} (1 - p^{-2})^{-1} · prod_{p | gcd(n,q), p||q} (1 - 1/p).

(iv) sum_{l=1}^q g(q,l)^2 = (A_0/q) · sum_{t>=1} eta(t) gcd(t^2,q)/t^2.

(v) sum_{t>=1} eta(t) = 6/(pi^2 A_0).

No implied constants occur.

*Risk:* Low. (i) follows from mu^2(n) = sum_{d^2|n} mu(d). (ii)–(iv) follow by multiplicativity over p^a || q: compute local densities of squarefree n in a class mod p^a, and compare Euler factors. For (iv), compare prod_{p^a||q} sum_{l mod p^a} (local factor)^2 with A_0/q · prod_p (1 + eta(p) gcd(p^2,q)/p^2). I checked (iv) numerically and exactly for q <= 50. Care is needed at p^2 | q, where classes with p^2 | l have g = 0, and at p || q, p | l.

## P2: Exact decomposition of the single-modulus variance (CRUX)

Depends on: P1  
Cites: none

Notation:
- B(u) = {u}(1 - {u}) for real u >= 0.
- A_0 = prod_p (1 - 2/p^2); eta(t) = mu^2(t) prod_{p|t} (p^2-2)^{-1}.
- For q in N and squarefree t, m_t(q) = t^2 / gcd(t^2, q).
- Q(x) = #{n <= x : n squarefree}.
- For real x >= 1 and integer m >= 1: C_x(m) = #{n in N : n + m <= x, mu^2(n) = mu^2(n+m) = 1}.
- A(m) = A_0 sum_{t>=1, t^2 | m} eta(t).
- D_x(m) = C_x(m) - A(m)(x - m).
- MT(x;q) = A_0 q sum_{t>=1} eta(t) m_t(q) B(x/(q m_t(q))). This converges absolutely, since B(u) <= u.
- V(x;q) = sum_{l=1}^q E(x;q,l)^2, with E and g as in problem.md.

Claim. For every real x >= 1 and every q in N,

  V(x;q) = MT(x;q) + 2 sum_{1 <= h <= x/q} D_x(hq) + (Q(x) - 6x/pi^2) - 2x sum_{l=1}^q g(q,l) E(x;q,l)

holds exactly. The sum over h is empty if q > x.

*Risk:* Bookkeeping identity. Every term must cancel exactly; any slip leaves an O(x) or O(x^2/q) term, which would dominate.

Route:
1. sum_l Q(x;q,l)^2 = Q(x) + 2 sum_{h>=1} C_x(hq).
2. 2 sum_{1<=h<=x/q} A(hq)(x - hq) = 2 A_0 sum_t eta(t) sum_{1<=j<=H/m_t} q(H - j m_t), with H = x/q and m_t = m_t(q). Then use sum_{1<=j<=T}(T - j) = (T^2 - T + B(T))/2. This gives x^2/q · A_0 sum_t eta(t)/m_t - x A_0 sum_t eta(t) + MT(x;q).
3. By P1(iv) the first term equals x^2 sum_l g^2. By P1(v) the second equals -6x/pi^2.
4. Write sum_l g Q = sum_l g E + x sum_l g^2.

Numerically, sum_k f'(k) MT(x;f(k)) matches V_f to 0.1%, which supports the identity.

## P3: Uniform asymptotic for squarefree pairs with shift m

Depends on: none  
Cites: none

Notation: A_0 = prod_p (1 - 2/p^2) and eta(t) = mu^2(t) prod_{p|t} (p^2-2)^{-1}. For real x >= 2 and integer m >= 1:
- C_x(m) = #{n in N : n + m <= x, mu^2(n) = mu^2(n+m) = 1};
- A(m) = A_0 sum_{t: t^2 | m} eta(t);
- D_x(m) = C_x(m) - A(m)(x - m).

Claim. For every eps > 0 there is a constant c(eps), depending only on eps, such that

  |D_x(m)| <= c(eps) x^{2/3+eps}

for all real x >= 2 and all integers 1 <= m <= x.

*Risk:* Classical (Mirsky's method); the prover must prove it here.

Route:
1. Set z = x^{1/3}. Write mu^2 = mu_z^2 + nu_z, where mu_z^2(n) = sum_{d<=z, d^2|n} mu(d) and nu_z(n) = sum_{d>z, d^2|n} mu(d).
2. Use |mu_z^2(n)| <= tau(n) << x^eps and sum_{n<=x} |nu_z(n)| <= sum_{d>z} x/d^2 <= 2x/z. The terms involving nu_z cost O(x^{1+eps}/z).
3. For d, e <= z: #{n <= x - m : d^2 | n, e^2 | n+m} = (x - m) · 1[gcd(d^2,e^2) | m]/lcm(d^2,e^2) + O(1), which costs O(z^2).
4. Complete the (d,e)-sum, using sum_{d>z} sum_e gcd(d,e)^2/(d^2 e^2) << (log z)/z.
5. Check that sum_{d,e} mu(d) mu(e) 1[gcd(d^2,e^2) | m]/lcm(d^2,e^2) = A(m), by comparing Euler factors.

This bound is the bottleneck that limits the final range to f(y) >= x^{7/9+delta}.

## P4: Trivial-size error pieces

Depends on: P1  
Cites: none

Notation: Q(x) = #{n <= x : n squarefree}; g and E as in problem.md.

Claim. There is an absolute constant c_0 such that for all real x >= 1 and all integers 1 <= q <= x:

(i) |Q(x) - 6x/pi^2| <= c_0 sqrt(x);

(ii) |sum_{l=1}^q g(q,l) E(x;q,l)| <= c_0 sqrt(x)/q.

*Risk:* Low.

For (ii):
1. sum_l g E = sum_{n<=x} mu^2(n) g(q,n) - x sum_l g(q,l)^2.
2. By P1(iii), q g(q,n) = c_q sum_{a | gcd(n, q_1)} mu(a)/a for squarefree n, where q_1 = prod_{p||q} p and c_q = (6/pi^2) prod_{p|q} (1 - p^{-2})^{-1} <= 1.
3. Use #{m <= Z : mu^2(m) = 1, gcd(m,a) = 1} = (6/pi^2) Z prod_{p|a} p/(p+1) + O(2^{omega(a)} sqrt Z). Sum this with weight 1/a over a | q_1, using prod_p (1 + 2p^{-3/2}) < infinity.
4. The main terms must reproduce x sum_l g^2 exactly. They do, because both equal x times the same limit, by P1(i).

## P5: Sawtooth sums B(Z/t^2) with multiplicative weights (CRUX)

Depends on: none  
Cites: none

Notation:
- B(u) = {u}(1 - {u}) for real u >= 0.
- I = int_0^infty B(u^{-2}) du.
- kappa(t) = mu^2(t) prod_{p|t} p^2/(p^2-2).
- For q in N, delta_q = prod_p (1 - 1/p)(1 + 1[p∤q] · p/(p^2-2)). This product converges absolutely.

Claims.

(a) I = (1/2) int_0^infty B(v) v^{-3/2} dv = -4 zeta(-1/2) = 0.83154489990...

(b) There is an absolute constant c_1 such that |sum_{s>=1} B(Z/s^2) - I sqrt(Z)| <= c_1 Z^{1/3} for every real Z > 0.

(c) For every eps > 0 there is c(eps), depending only on eps, such that for all q in N and real Z > 0:
  |sum_{t>=1, gcd(t,q)=1} kappa(t) B(Z/t^2) - delta_q I sqrt(Z)| <= c(eps) q^eps Z^{1/3}.

*Risk:* (a) is a Mellin / Euler–Maclaurin computation. Use the periodic Bernoulli function: 1/6 - B(v) = {v}^2 - {v} + 1/6 = Bbar_2(v), together with the continuation of zeta(s) to Re s > -1 by second-order Euler–Maclaurin. Numerically I = 0.8315448999 = -4 zeta(-1/2).

(b) Split at S = Z^{1/3}. For s <= S, bound the sum and the integral trivially by S/4 each. For s > S, use Euler–Maclaurin with |d/ds B(Z/s^2)| <= 2Z/s^3. For Z < 1, both sides are << sqrt Z <= Z^{1/3}.

(c) Write 1[gcd(t,q)=1] kappa(t) = sum_{ab=t} beta(a), with beta multiplicative and supported on cube-free a:
- for p∤q: beta(p) = kappa(p) - 1 = 2/(p^2-2), beta(p^2) = -kappa(p);
- for p|q: beta(p) = -1.
Then apply (b) to each inner sum over b. This needs sum_a |beta(a)| a^{-2/3} << q^eps.

The risk lies in getting the q-dependence of the convolution uniform. The constant I must be exactly right, because it fixes C_f. It has been cross-checked: the resulting average over all moduli reproduces Vaughan's c_2 to 7 digits.

## P6: Asymptotic for MT(x;q)

Depends on: P5  
Cites: none

Notation:
- B(u) = {u}(1 - {u}).
- A_0 = prod_p (1 - 2/p^2); eta(t) = mu^2(t) prod_{p|t} (p^2-2)^{-1}.
- m_t(q) = t^2 / gcd(t^2, q).
- MT(x;q) = A_0 q sum_{t>=1} eta(t) m_t(q) B(x/(q m_t(q))).
- h(q) = -4 zeta(-1/2) · prod_{p∤q} (1 - 3/p^2 + 2/p^3) · prod_{p||q} (p-1)(p^2 - 2 + sqrt p)/p^3 · prod_{p^2|q} (p-1)^2 (p+1)/p^3.

Claim. For every eps > 0 there is c(eps), depending only on eps, such that for all real x >= 1 and integers 1 <= q <= x:

  |MT(x;q) - h(q) sqrt(xq)| <= c(eps) x^{1/3} q^{2/3+eps}.

*Risk:* Moderate bookkeeping.

1. Factor squarefree t = t_1 t_2 with t_1 | rad(q) and gcd(t_2, q) = 1. Then eta(t) m_t(q) = eta(t_1) m_{t_1}(q) kappa(t_2), where m_{t_1}(q) = prod_{p|t_1, p||q} p.
2. Apply P5(c) with Z = x/(q m_{t_1}(q)).
3. Main term: A_0 delta_q I sqrt(xq) prod_{p|q} (1 + sqrt(m_p)/(p^2-2)), with m_p = p if p||q and m_p = 1 if p^2|q. Multiplying out the Euler factors gives h(q):
   - p∤q: (1-1/p)(p+2)(p-1)/p^2 = 1 - 3/p^2 + 2/p^3;
   - p||q: (1-1/p)(p^2 - 2 + sqrt p)/p^2;
   - p^2|q: (1-1/p)(p^2-1)/p^2.
4. Error: q^{1+eps} (x/q)^{1/3} sum_{t_1 | rad q} eta(t_1) m_{t_1}^{2/3}, and that last sum is O(1).

As a check, (2/3) times the mean of h equals Vaughan's constant 0.1284787.

## P7: Single-modulus variance asymptotic

Depends on: P2, P3, P4, P6  
Cites: none

Notation: V(x;q) = sum_{l=1}^q E(x;q,l)^2, with E as in problem.md. MT(x;q) and h(q) are as follows:
- MT(x;q) = A_0 q sum_{t>=1} eta(t) m_t(q) B(x/(q m_t(q))), where B(u) = {u}(1 - {u}), A_0 = prod_p (1 - 2/p^2), eta(t) = mu^2(t) prod_{p|t} (p^2-2)^{-1} and m_t(q) = t^2/gcd(t^2,q);
- h(q) = -4 zeta(-1/2) · prod_{p∤q} (1 - 3/p^2 + 2/p^3) · prod_{p||q} (p-1)(p^2 - 2 + sqrt p)/p^3 · prod_{p^2|q} (p-1)^2 (p+1)/p^3.

Claim. For every eps > 0 there is c(eps), depending only on eps, such that for all real x >= 2 and integers 1 <= q <= x:

(i) |V(x;q) - MT(x;q)| <= c(eps) (x^{5/3+eps}/q + sqrt(x));

(ii) |V(x;q) - h(q) sqrt(xq)| <= c(eps) (x^{1/3} q^{2/3+eps} + x^{5/3+eps}/q + sqrt(x)).

*Risk:* Low once P2, P3, P4 and P6 hold.

Insert into P2:
- P3 bounds 2 sum_{h<=x/q} |D_x(hq)| <= 2 (x/q) c(eps) x^{2/3+eps};
- P4(i) bounds Q(x) - 6x/pi^2;
- P4(ii) gives 2x · c_0 sqrt(x)/q <= 2 c_0 x^{5/3}/q.
Then apply P6 for (ii).

## P8: Averages over polynomial moduli

Depends on: none  
Cites: Hooley 1964 (background on rho only; not needed for hypotheses)

Notation:
- f in Z[t] has degree d >= 1, with f(t) >= 2 and f'(t) >= 1 for t >= 1.
- rho(m) = #{a mod m : f(a) ≡ 0 mod m}.
- F(t) = f'(t) f(t)^{1/2}.
- h(q) = -4 zeta(-1/2) · prod_{p∤q} (1 - 3/p^2 + 2/p^3) · prod_{p||q} (p-1)(p^2 - 2 + sqrt p)/p^3 · prod_{p^2|q} (p-1)^2 (p+1)/p^3.
- tau_p = (1 - 3/p^2 + 2/p^3)(1 - rho(p)/p) + ((p-1)(p^2 - 2 + sqrt p)/p^3)(rho(p)/p - rho(p^2)/p^2) + ((p-1)^2 (p+1)/p^3)(rho(p^2)/p^2).
- C_f = (2/3)(-4 zeta(-1/2)) prod_p tau_p.

Claims.

(0) tau_p > 0 for every p, and prod_p tau_p converges absolutely. Hence 0 < C_f < infinity.

For every eps > 0 there are constants c(f), c(f,eps), depending only on f (and eps), such that for all real y >= 1, with Y = f(y):

(a) |sum_{1<=k<=y} F(k) h(f(k)) - C_f Y^{3/2}| <= c(f,eps) Y^{3/2+eps} y^{-1/2};

(b) sum_{1<=k<=y} f'(k)/f(k) <= c(f)(1 + log Y);

(c) sum_{1<=k<=y} f'(k) <= c(f) Y.

*Risk:* Moderate.

1. Write h(q) = h_0 sum_{m|q} etat(m), where h_0 = -4 zeta(-1/2) prod_p (1 - 3/p^2 + 2/p^3) and etat is multiplicative with:
   - etat(p) = (sqrt p - p)/((p+2)(p-1)), lying in (-1/p, 0];
   - etat(p^2) = (1 - sqrt p)/((p+2)(p-1)), with |etat(p^2)| <= p^{-3/2};
   - etat(p^j) = 0 for j >= 3.
2. Swap sums and split k into rho(m) classes mod m. F has at most 2d monotone pieces on [1, y], because F' has the sign of the polynomial 2 f'' f + f'^2. So each class sum equals (1/m) int_1^y F + O_f(max_{[1,y]} F), and max F << Y^{3/2}/y.
3. Use int_1^y F = (2/3)(Y^{3/2} - f(1)^{3/2}).
4. Truncate at m <= M = y^2. The tail costs tau(f(k)) M^{-1/2} << Y^eps/y, using |etat(m)| <= m^{-1/2}.
5. Use rho(p) <= d and rho(p^2) <= d p for p not dividing the content of f (Lagrange and Hensel). Primes dividing the content are finitely many and are absorbed into the constants. Rankin's trick then gives sum_{m<=M} |etat(m)| rho(m) << M^{1/4+eps}.

The pitfall is f with repeated factors or nontrivial content (rho(p^2) as large as p, or rho(p) = p). The bounds above still cover these, but the prover must not assume rho(p^2) = rho(p).

## P9: Assembly: main theorem

Depends on: P7, P8  
Cites: none

Notation: f, d, rho, C_f and Y = f(y) as in the main theorem. V_f(x,y) = sum_{k<=y} f'(k) sum_{l=1}^{f(k)} E(x;f(k),l)^2 (problem.md). MT(x;q) = A_0 q sum_{t>=1} eta(t) m_t(q) B(x/(q m_t(q))), with B(u) = {u}(1 - {u}), A_0 = prod_p (1 - 2/p^2), eta(t) = mu^2(t) prod_{p|t} (p^2-2)^{-1} and m_t(q) = t^2/gcd(t^2,q).

Claims. For every eps > 0 there is c(f,eps) such that for all real x >= 2 and y >= 1 with Y = f(y) <= x:

(i) |V_f(x,y) - C_f x^{1/2} Y^{3/2}| <= c(f,eps) (x^{1/3+eps} Y^{5/3} + x^{5/3+eps} + x^{1/2+eps} Y^{3/2 - 1/(2d)});

(ii) |V_f(x,y) - sum_{1<=k<=y} f'(k) MT(x;f(k))| <= c(f,eps) (x^{5/3+eps} + x^{1/2} Y).

Consequently, for fixed delta in (0, 1/9) and x^{7/9+delta} <= Y <= x^{1-delta}:
  V_f(x,y) = C_f x^{1/2} Y^{3/2} (1 + O_{f,delta}(x^{-eta})),   with eta = min(delta/12, 1/(6d)).

*Risk:* Low.

1. V_f(x,y) = sum_{k<=y} f'(k) V(x;f(k)), and f(k) <= Y <= x for k <= y because f is increasing on [1, infinity).
2. Apply P7(ii) with q = f(k). The main term is sqrt(x) sum_k F(k) h(f(k)); P8(a) evaluates it.
3. Errors:
   - x^{1/3} sum_k f'(k) f(k)^{2/3+eps} <= x^{1/3} Y^{2/3+eps} · P8(c);
   - x^{5/3+eps} · P8(b);
   - sqrt(x) · P8(c);
   - y^{-1/2} << Y^{-1/(2d)}.
4. (ii) follows the same way from P7(i).
5. For the corollary, take eps = delta/12 and compare each error with x^{1/2} Y^{3/2}.
