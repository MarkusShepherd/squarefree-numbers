# P5: Sawtooth sums B(Z/t^2) with multiplicative weights

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
