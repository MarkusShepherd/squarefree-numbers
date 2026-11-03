# P8: Averages over polynomial moduli

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
