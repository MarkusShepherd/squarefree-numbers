# P2: Exact decomposition of the single-modulus variance

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
