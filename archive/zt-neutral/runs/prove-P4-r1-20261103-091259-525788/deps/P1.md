# P1: Closed form and moments of g(q,l)

Notation: mu is the Mobius function, A_0 = prod_p (1 - 2/p^2), eta(t) = mu^2(t) prod_{p|t} (p^2-2)^{-1}. For q in N and l in Z, g(q,l) = lim_{x->oo} Q(x;q,l)/x (problem.md).

Claims. For every q in N and l in Z:

(i) The limit g(q,l) exists, and g(q,l) = sum_{d>=1} mu(d) · gcd(d^2,q)/(d^2 q) · 1[gcd(d^2,q) | l]. The series converges absolutely. Also 0 <= g(q,l) <= 1/q, and g(q,l) depends only on l mod q.

(ii) sum_{l=1}^q g(q,l) = 6/pi^2.

(iii) For squarefree n,
  g(q,n) = (6/pi^2) · q^{-1} · prod_{p|q} (1 - p^{-2})^{-1} · prod_{p | gcd(n,q), p||q} (1 - 1/p).

(iv) sum_{l=1}^q g(q,l)^2 = (A_0/q) · sum_{t>=1} eta(t) gcd(t^2,q)/t^2.

(v) sum_{t>=1} eta(t) = 6/(pi^2 A_0).

No implied constants occur.
