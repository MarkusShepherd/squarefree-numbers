# Proof of P9 (assembly)

No external literature is used. The proof uses only P7, P8 and elementary estimates. No numerical checks were run, since none are needed.

Throughout, $f$ is fixed. "Constant" means a constant depending only on $f$, and on $\varepsilon$ or $\delta$ where indicated. Let $x\ge2$, $y\ge1$ and $Y=f(y)\le x$.

## 0. Preliminaries

**(P-a) Range of moduli.** Since $f'(t)\ge1>0$ for $t\ge1$, $f$ is increasing on $[1,\infty)$. So every integer $k$ with $1\le k\le y$ has $2\le f(k)\le f(y)=Y\le x$. Hence P7 applies to $q=f(k)$ for every $k\le y$, with the same $x$. Also $Y\ge f(1)\ge2$.

**(P-b) Decomposition.** By definition $V_f(x,y)=\sum_{1\le k\le y}f'(k)\,V(x;f(k))$, where $V(x;q)=\sum_{l=1}^qE(x;q,l)^2$.

**(P-c) Size of $y$ in terms of $Y$.** Write $f(t)=\sum_{i\le d}a_it^i$. For $y\ge1$,
$$Y=f(y)\le\Big(\sum_i|a_i|\Big)y^d=:c_1y^d .$$
So $y\ge(Y/c_1)^{1/d}$, and therefore
$$y^{-1/2}\le c_1^{1/(2d)}\,Y^{-1/(2d)}.\tag{0.1}$$

**(P-d) Logarithm.** Since $Y\le x$, we have $1+\log Y\le1+\log x\le c(\varepsilon)x^{\varepsilon}$. Likewise $Y^{\varepsilon}\le x^{\varepsilon}$.

**Consequences of P8(b),(c).**
$$\sum_{k\le y}\frac{f'(k)}{f(k)}\le c(f)(1+\log Y)\le c(f,\varepsilon)x^{\varepsilon},\qquad \sum_{k\le y}f'(k)\le c(f)Y.\tag{0.2}$$

## 1. Proof of (ii)

Apply P7(i) with $\varepsilon$ to each $q=f(k)$, $k\le y$. This is legitimate by (P-a). We get
$$|V(x;f(k))-MT(x;f(k))|\le c(\varepsilon)\Big(\frac{x^{5/3+\varepsilon}}{f(k)}+\sqrt x\Big).$$
Multiply by $f'(k)>0$, sum over the $\lfloor y\rfloor$ integers $1\le k\le y$, and use the triangle inequality and (P-b):
$$\Big|V_f(x,y)-\sum_{k\le y}f'(k)MT(x;f(k))\Big|\le c(\varepsilon)\Big(x^{5/3+\varepsilon}\sum_{k\le y}\frac{f'(k)}{f(k)}+\sqrt x\sum_{k\le y}f'(k)\Big).$$
By (0.2), the right side is at most
$$c(\varepsilon)\big(c(f,\varepsilon')x^{5/3+\varepsilon+\varepsilon'}+c(f)\sqrt x\,Y\big)$$
for any $\varepsilon'>0$. Choosing $\varepsilon=\varepsilon'=\varepsilon_0/2$, where $\varepsilon_0$ is the $\varepsilon$ in the claim, gives
$$\le c(f,\varepsilon_0)\big(x^{5/3+\varepsilon_0}+x^{1/2}Y\big).$$
This is (ii). $\square$

## 2. Proof of (i)

Apply P7(ii) with $\varepsilon/3$ for each $q=f(k)$, $k\le y$ (legitimate by (P-a)):
$$\big|V(x;f(k))-h(f(k))\sqrt{x f(k)}\big|\le c(\varepsilon)\Big(x^{1/3}f(k)^{2/3+\varepsilon/3}+\frac{x^{5/3+\varepsilon/3}}{f(k)}+\sqrt x\Big).$$
Multiply by $f'(k)$ and sum over $1\le k\le y$. Note that $f'(k)\sqrt{f(k)}=F(k)$. Then
$$\Big|V_f(x,y)-\sqrt x\sum_{k\le y}F(k)h(f(k))\Big|\le c(\varepsilon)\,(T_1+T_2+T_3),$$
where each $T_i$ is bounded as follows.

* **$T_1$.** Since $f(k)\le Y$, we have $f(k)^{2/3+\varepsilon/3}\le Y^{2/3+\varepsilon/3}$. So, by (0.2) and (P-d),
$$T_1=x^{1/3}\sum_{k\le y}f'(k)f(k)^{2/3+\varepsilon/3}\le x^{1/3}Y^{2/3+\varepsilon/3}\cdot c(f)Y\le c(f)\,x^{1/3+\varepsilon/3}Y^{5/3}.$$
* **$T_2$.** By (0.2), $T_2=x^{5/3+\varepsilon/3}\sum_{k\le y}f'(k)/f(k)\le c(f,\varepsilon)x^{5/3+2\varepsilon/3}\le c(f,\varepsilon)x^{5/3+\varepsilon}$.
* **$T_3$.** By (0.2), $T_3=\sqrt x\sum_{k\le y}f'(k)\le c(f)\sqrt xY$. Since $Y\ge2$ and $d\ge1$, $Y^{1/2-1/(2d)}\ge1$, so $Y\le Y^{3/2-1/(2d)}$. Hence $T_3\le c(f)\,x^{1/2}Y^{3/2-1/(2d)}$.

For the main term, P8(a) with $\varepsilon/3$ gives
$$\Big|\sum_{k\le y}F(k)h(f(k))-C_fY^{3/2}\Big|\le c(f,\varepsilon)Y^{3/2+\varepsilon/3}y^{-1/2}.$$
By (0.1) the right side is at most $c(f,\varepsilon)Y^{3/2-1/(2d)+\varepsilon/3}$. Multiplying by $\sqrt x$ and using $Y^{\varepsilon/3}\le x^{\varepsilon/3}$ gives
$$\Big|\sqrt x\sum_{k\le y}F(k)h(f(k))-C_fx^{1/2}Y^{3/2}\Big|\le c(f,\varepsilon)\,x^{1/2+\varepsilon/3}Y^{3/2-1/(2d)}.$$

Combine the bounds via the triangle inequality: the first error is at most $c(\varepsilon)(T_1+T_2+T_3)$, and this last bound controls the main-term error. This gives
$$|V_f(x,y)-C_fx^{1/2}Y^{3/2}|\le c(f,\varepsilon)\big(x^{1/3+\varepsilon}Y^{5/3}+x^{5/3+\varepsilon}+x^{1/2+\varepsilon}Y^{3/2-1/(2d)}\big),$$
which is (i). $\square$

## 3. The consequence

Fix $\delta\in(0,1/9)$ and assume $x^{7/9+\delta}\le Y\le x^{1-\delta}$ (with $y\ge1$, $x\ge2$). Put $\eta=\min(\delta/12,1/(6d))$ and take $\varepsilon=\min(\delta/12,\,1/(9d))$ in (i). Divide the error in (i) by $x^{1/2}Y^{3/2}$ and bound each of the three ratios.

1. $\dfrac{x^{1/3+\varepsilon}Y^{5/3}}{x^{1/2}Y^{3/2}}=x^{-1/6+\varepsilon}Y^{1/6}\le x^{-1/6+\varepsilon+(1-\delta)/6}=x^{-\delta/6+\varepsilon}\le x^{-\delta/12}\le x^{-\eta}$.
 Here we used $Y\le x^{1-\delta}$ and $\varepsilon\le\delta/12$.

2. $\dfrac{x^{5/3+\varepsilon}}{x^{1/2}Y^{3/2}}=x^{7/6+\varepsilon}Y^{-3/2}\le x^{7/6+\varepsilon-\frac32(7/9+\delta)}=x^{-3\delta/2+\varepsilon}\le x^{-\delta/12}\le x^{-\eta}$.
 Here we used $Y\ge x^{7/9+\delta}$, $\tfrac32\cdot\tfrac79=\tfrac76$ and $\varepsilon\le\delta/12$.

3. $\dfrac{x^{1/2+\varepsilon}Y^{3/2-1/(2d)}}{x^{1/2}Y^{3/2}}=x^{\varepsilon}Y^{-1/(2d)}\le x^{\varepsilon-\frac{7}{18d}-\frac{\delta}{2d}}\le x^{\frac1{9d}-\frac7{18d}}=x^{-\frac5{18d}}\le x^{-\frac1{6d}}\le x^{-\eta}$.
 Here we used $Y\ge x^{7/9+\delta}\ge x^{7/9}$, $\varepsilon\le1/(9d)$ and $\tfrac5{18}\ge\tfrac16=\tfrac3{18}$.

Summing the three ratios, (i) gives
$$|V_f(x,y)-C_fx^{1/2}Y^{3/2}|\le 3c(f,\delta)\,x^{-\eta}\,x^{1/2}Y^{3/2}.$$
By P8(0), $0<C_f<\infty$. So $3c(f,\delta)x^{-\eta}x^{1/2}Y^{3/2}=C_fx^{1/2}Y^{3/2}\cdot O_{f,\delta}(x^{-\eta})$, and
$$V_f(x,y)=C_fx^{1/2}Y^{3/2}\big(1+O_{f,\delta}(x^{-\eta})\big).\qquad\blacksquare$$

Remark: $\delta<1/9$ makes the range $x^{7/9+\delta}\le Y\le x^{1-\delta}$ non-empty, since $7/9+\delta<1-\delta$ exactly when $\delta<1/9$.
