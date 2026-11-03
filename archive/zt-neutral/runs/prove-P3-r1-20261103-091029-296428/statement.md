# P3: Uniform asymptotic for squarefree pairs with shift m

Notation: A_0 = prod_p (1 - 2/p^2) and eta(t) = mu^2(t) prod_{p|t} (p^2-2)^{-1}. For real x >= 2 and integer m >= 1:
- C_x(m) = #{n in N : n + m <= x, mu^2(n) = mu^2(n+m) = 1};
- A(m) = A_0 sum_{t: t^2 | m} eta(t);
- D_x(m) = C_x(m) - A(m)(x - m).

Claim. For every eps > 0 there is a constant c(eps), depending only on eps, such that

  |D_x(m)| <= c(eps) x^{2/3+eps}

for all real x >= 2 and all integers 1 <= m <= x.
