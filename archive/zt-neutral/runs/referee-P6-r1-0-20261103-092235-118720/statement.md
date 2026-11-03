# P6: Asymptotic for MT(x;q)

Notation:
- B(u) = {u}(1 - {u}).
- A_0 = prod_p (1 - 2/p^2); eta(t) = mu^2(t) prod_{p|t} (p^2-2)^{-1}.
- m_t(q) = t^2 / gcd(t^2, q).
- MT(x;q) = A_0 q sum_{t>=1} eta(t) m_t(q) B(x/(q m_t(q))).
- h(q) = -4 zeta(-1/2) · prod_{p∤q} (1 - 3/p^2 + 2/p^3) · prod_{p||q} (p-1)(p^2 - 2 + sqrt p)/p^3 · prod_{p^2|q} (p-1)^2 (p+1)/p^3.

Claim. For every eps > 0 there is c(eps), depending only on eps, such that for all real x >= 1 and integers 1 <= q <= x:

  |MT(x;q) - h(q) sqrt(xq)| <= c(eps) x^{1/3} q^{2/3+eps}.
