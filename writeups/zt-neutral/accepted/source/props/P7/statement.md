# P7: Single-modulus variance asymptotic

Notation: V(x;q) = sum_{l=1}^q E(x;q,l)^2, with E as in problem.md. MT(x;q) and h(q) are as follows:
- MT(x;q) = A_0 q sum_{t>=1} eta(t) m_t(q) B(x/(q m_t(q))), where B(u) = {u}(1 - {u}), A_0 = prod_p (1 - 2/p^2), eta(t) = mu^2(t) prod_{p|t} (p^2-2)^{-1} and m_t(q) = t^2/gcd(t^2,q);
- h(q) = -4 zeta(-1/2) · prod_{p∤q} (1 - 3/p^2 + 2/p^3) · prod_{p||q} (p-1)(p^2 - 2 + sqrt p)/p^3 · prod_{p^2|q} (p-1)^2 (p+1)/p^3.

Claim. For every eps > 0 there is c(eps), depending only on eps, such that for all real x >= 2 and integers 1 <= q <= x:

(i) |V(x;q) - MT(x;q)| <= c(eps) (x^{5/3+eps}/q + sqrt(x));

(ii) |V(x;q) - h(q) sqrt(xq)| <= c(eps) (x^{1/3} q^{2/3+eps} + x^{5/3+eps}/q + sqrt(x)).
