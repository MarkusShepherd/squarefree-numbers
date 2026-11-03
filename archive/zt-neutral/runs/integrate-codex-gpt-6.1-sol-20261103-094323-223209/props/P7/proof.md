# Proof of P7

The proof combines the black-box statements P2, P3, P4 and P6 from `deps/`. No external paper is cited and no numerical check was needed.

Fix $\varepsilon>0$. Let $c_3(\varepsilon)$ be the constant of P3, $c_6(\varepsilon)$ the constant of P6, and $c_0$ the absolute constant of P4. Let $x\ge 2$ and $1\le q\le x$.

## Proof of (i)

By P2 (valid for every real $x\ge1$ and every $q\in\mathbb N$, so in particular here),
$$
V(x;q)-MT(x;q)=2\sum_{1\le h\le x/q}D_x(hq)+\bigl(Q(x)-6x/\pi^2\bigr)-2x\sum_{l=1}^q g(q,l)E(x;q,l).
$$
Bound the three terms separately.

**First term.** For $1\le h\le x/q$ the integer $m=hq$ satisfies $1\le m\le x$. Since $x\ge2$, P3 applies and gives $|D_x(hq)|\le c_3(\varepsilon)\,x^{2/3+\varepsilon}$. The sum has $\lfloor x/q\rfloor\le x/q$ terms, so
$$
\Bigl|2\sum_{1\le h\le x/q}D_x(hq)\Bigr|\le 2\cdot\frac xq\cdot c_3(\varepsilon)x^{2/3+\varepsilon}=2c_3(\varepsilon)\,\frac{x^{5/3+\varepsilon}}{q}.
$$
The length of the sum is $\le x/q$ and the bound per term is $c_3x^{2/3+\varepsilon}$. The total is the product, and no further loss occurs.

**Second term.** P4(i) applies since $x\ge1$, and gives $|Q(x)-6x/\pi^2|\le c_0\sqrt x$.

**Third term.** P4(ii) applies since $1\le q\le x$, and gives
$$
\Bigl|2x\sum_{l=1}^q g(q,l)E(x;q,l)\Bigr|\le 2x\cdot\frac{c_0\sqrt x}{q}=2c_0\frac{x^{3/2}}{q}\le 2c_0\frac{x^{5/3+\varepsilon}}{q}.
$$
The last step holds because $x\ge 1$ and $3/2\le 5/3+\varepsilon$.

**Total.** By the triangle inequality,
$$
|V(x;q)-MT(x;q)|\le 2c_3(\varepsilon)\frac{x^{5/3+\varepsilon}}{q}+c_0\sqrt x+2c_0\frac{x^{5/3+\varepsilon}}{q}
\le c_7(\varepsilon)\Bigl(\frac{x^{5/3+\varepsilon}}{q}+\sqrt x\Bigr),
$$
with $c_7(\varepsilon)=2c_3(\varepsilon)+2c_0$. This is (i). The constant depends only on $\varepsilon$.

## Proof of (ii)

Let $x\ge2$ and $1\le q\le x$. P6 applies (it needs $x\ge1$ and $1\le q\le x$) and gives
$$
|MT(x;q)-h(q)\sqrt{xq}|\le c_6(\varepsilon)\,x^{1/3}q^{2/3+\varepsilon}.
$$
Combining this with (i) by the triangle inequality,
$$
|V(x;q)-h(q)\sqrt{xq}|\le |V(x;q)-MT(x;q)|+|MT(x;q)-h(q)\sqrt{xq}|
\le c_7(\varepsilon)\Bigl(\frac{x^{5/3+\varepsilon}}{q}+\sqrt x\Bigr)+c_6(\varepsilon)x^{1/3}q^{2/3+\varepsilon}.
$$
Put $c(\varepsilon)=\max\{c_6(\varepsilon),c_7(\varepsilon)\}$. Then the right side is at most
$$
c(\varepsilon)\bigl(x^{1/3}q^{2/3+\varepsilon}+x^{5/3+\varepsilon}/q+\sqrt x\bigr),
$$
which is (ii). $\qquad\blacksquare$

(Taking one $c(\varepsilon)=\max\{c_6(\varepsilon),c_7(\varepsilon)\}$ for both parts is legitimate, since the bound in (i) only weakens when the constant increases.)
