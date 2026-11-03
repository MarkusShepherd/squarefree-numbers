# P9: Assembly: main theorem

Notation: f, d, rho, C_f and Y = f(y) as in the main theorem. V_f(x,y) = sum_{k<=y} f'(k) sum_{l=1}^{f(k)} E(x;f(k),l)^2 (problem.md). MT(x;q) = A_0 q sum_{t>=1} eta(t) m_t(q) B(x/(q m_t(q))), with B(u) = {u}(1 - {u}), A_0 = prod_p (1 - 2/p^2), eta(t) = mu^2(t) prod_{p|t} (p^2-2)^{-1} and m_t(q) = t^2/gcd(t^2,q).

Claims. For every eps > 0 there is c(f,eps) such that for all real x >= 2 and y >= 1 with Y = f(y) <= x:

(i) |V_f(x,y) - C_f x^{1/2} Y^{3/2}| <= c(f,eps) (x^{1/3+eps} Y^{5/3} + x^{5/3+eps} + x^{1/2+eps} Y^{3/2 - 1/(2d)});

(ii) |V_f(x,y) - sum_{1<=k<=y} f'(k) MT(x;f(k))| <= c(f,eps) (x^{5/3+eps} + x^{1/2} Y).

Consequently, for fixed delta in (0, 1/9) and x^{7/9+delta} <= Y <= x^{1-delta}:
  V_f(x,y) = C_f x^{1/2} Y^{3/2} (1 + O_{f,delta}(x^{-eta})),   with eta = min(delta/12, 1/(6d)).
