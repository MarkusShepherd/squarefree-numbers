# Proof of P7

We use the supplied propositions P2–P6 as black boxes. No external literature
is used. Write
\[
c=\zeta(2)^{-1},\qquad
a=4d-1,\qquad \theta=\frac{2d}{a},\qquad
\eta=\min\left\{\frac15,\frac1a\right\}.
\]
Fix \(0<\varepsilon<\eta/2\), and set
\(\delta=\varepsilon/2\). Every constant below is independent of \(x,y\);
constants denoted by \(C_f\) depend only on \(f\), and those denoted by
\(C_{f,\varepsilon}\) depend only on \(f,\varepsilon\). Constants may be
enlarged from one occurrence to the next.

## Polynomial bounds and identification of the density

The assumptions in problem.md are \(f\in\mathbb Z[t]\), \(d\ge1\),
\(f(t)\ge2\), and \(f'(t)\ge1\) for every real \(t\ge1\).
The leading coefficient of \(f\) is positive, because \(f(t)\ge2\) on
this half-line. The functions \(f(t)/t^d\) and
\(f'(t)/t^{d-1}\) tend to positive limits as \(t\to\infty\).
Continuity on each bounded closed subinterval of \([1,\infty)\), and
the positivity assumptions, therefore give constants \(b_f,B_f^*>0\)
such that
\[
b_f t^d\le f(t)\le B_f^*t^d,
\qquad 0<f'(t)\le B_f^*t^{d-1}\quad(t\ge1).
\tag{1}
\]
Here \(B_f^*\) is just a bound, distinct from the constant \(B_f\)
in the statement. In particular,
\[
\frac{f'(k)}{f(k)}\le \frac{B_f^*}{b_f k}\quad(k\ge1),
\qquad y\le b_f^{-1/d}x^{1/d}\quad\text{if }f(y)\le x.
\tag{2}
\]

The coefficient of \(\log(Y/Z)\) in P4 is the \(R_f\) in the
statement. Indeed, P5 gives
\[
D_f(s)=\zeta(s)P_f(s),\qquad
P_f(1)=\sum_{r\ge1}\frac{\lambda(r)\rho(r)}r.
\]
Its asserted convergence makes \(P_f\) holomorphic near \(1\), so the
residue at \(1\) is \(P_f(1)\), which is exactly the coefficient in
P4. All the definitions of \(W_f,\Theta_f,F_f,R_f,B_f,K_f\) in P6
are those in P7. Thus P6 applies with these definitions and yields a
constant \(C_f\) such that
\[
\left|F_f(H)-K_fH^{-3/2}\right|\le C_fH^{-13/8}
\quad(H\ge1).
\tag{3}
\]
Since \(H^{-13/8}\le H^{-3/2}\) for \(H\ge1\), enlarging the
constant to include \(|K_f|\) gives
\[
|F_f(H)|\le C_fH^{-3/2}\quad(H\ge1).
\tag{4}
\]

## Reduction on an interval of moduli

For the moment let \(x\ge2\), \(1\le z\le y\),
\(2\le Z=f(z)\le Y=f(y)\le x\), and \(2\le R\le x\).
Put
\[
\begin{split}
M(x;z,y)&=\sum_{z<k\le y}f'(k)
  \sum_{1\le h\le x/f(k)}(x-hf(k))\mathfrak S(hf(k)),\\
I(x;Z,Y)&=\int_Z^Y
  \sum_{1\le h\le x/t}(x-ht)W_f(h)\,dt,\\
A(x,Z,R)&=Z^{-1/d}R^{1/2}(\log(2R))^2
       +R^{-1/2}(\log(2R))^2\log(2x).
\end{split}
\tag{5}
\]
All discrete variables in these expressions are positive integers.

We first record the correlation error with both summation lengths.
For a fixed integer \(k\) with \(z<k\le y\), there are
\(N_k=\lfloor x/f(k)\rfloor\le x/f(k)\) choices of \(h\).
For each choice, \(m=hf(k)\) is an integer satisfying
\(1\le m\le x\): integrality follows from \(f\in\mathbb Z[t]\),
and the upper bound follows from the restriction on \(h\).
Consequently P3 with exponent \(\delta\) bounds each unweighted
correlation error by \(C_\delta x^{4/5+\delta}\). After multiplication
by the positive weight \(f'(k)\) and summation over these \(N_k\)
values, the error is at most
\[
C_\delta f'(k)N_kx^{4/5+\delta}
\le C_\delta x^{9/5+\delta}\frac{f'(k)}{f(k)}.
\tag{6}
\]
There are \(\lfloor y\rfloor-\lfloor z\rfloor\le\lfloor y\rfloor
\le b_f^{-1/d}x^{1/d}\) possible values of \(k\). Use (2) to sum (6):
\[
\begin{split}
|S_f(x;z,y)-M(x;z,y)|
&\le C_{f,\varepsilon}x^{9/5+\delta}
       \sum_{1\le k\le y}\frac1k\\
&\le C_{f,\varepsilon}x^{9/5+\delta}(1+\log y)\\
&\le C_{f,\varepsilon}x^{9/5+\delta}\log(2x).
\end{split}
\tag{7}
\]
The last inequality uses \(y\le b_f^{-1/d}x^{1/d}\), with its
constant depending only on \(f\).

P4, applied with precisely the ranges preceding (5), gives the two
errors
\[
|M(x;z,y)-I(x;Z,Y)|\le C_fx^2A(x,Z,R),
\qquad
|T_f(z,y)-R_f\log(Y/Z)|\le C_fA(x,Z,R).
\tag{8}
\]
The hypotheses needed here are exactly \(x\ge2\), \(1\le z\le y\),
\(Z=f(z)\le Y=f(y)\le x\), and \(2\le R\le x\), together
with the polynomial assumptions already checked. No extra arithmetic
assumption on \(f\) is being introduced.

Use P2 with exponent \(\delta\), substitute (7) and (8), and retain
the factors \(2\) and \(x^2\) multiplying the errors of \(S_f\) and
\(T_f\). This gives
\[
\begin{split}
\big|V_f(x;z,y)-[cx(Y-Z)+2I(x;Z,Y)-x^2R_f\log(Y/Z)]\big|
\le C_{f,\varepsilon}\big[&x^{3/2+\delta}
  +xY^{1-1/d}\\
 &+x^{9/5+\delta}\log(2x)+x^2A(x,Z,R)\big].
\end{split}
\tag{9}
\]
More explicitly, the two substitutions in the \(S_f\) term contribute
at most \(2C_{f,\varepsilon}x^{9/5+\delta}\log(2x)
+2C_fx^2A(x,Z,R)\), and the substitution in the \(T_f\) term
contributes at most \(C_fx^2A(x,Z,R)\). These are the last two
terms on the right of (9), after enlarging its constant.

The integral identity in P6 is applicable because \(2\le Z\le Y\le x\).
It is exact:
\[
2I(x;Z,Y)=Z^2\Theta_f(x/Z)-Y^2\Theta_f(x/Y).
\tag{10}
\]
From the definition of \(F_f\), direct subtraction gives the exact
identity
\[
\begin{split}
x^2\big(F_f(x/Y)-F_f(x/Z)\big)
={}&-x^2R_f\log(Y/Z)+cx(Y-Z)\\
 &+Z^2\Theta_f(x/Z)-Y^2\Theta_f(x/Y).
\end{split}
\tag{11}
\]
In particular the \(B_f\) terms cancel. Combining (9)–(11) proves
\[
\begin{split}
\big|V_f(x;z,y)-x^2\big(F_f(x/Y)-F_f(x/Z)\big)\big|
\le C_{f,\varepsilon}\big[&x^{3/2+\delta}+xY^{1-1/d}\\
 &+x^{9/5+\delta}\log(2x)+x^2A(x,Z,R)\big].
\end{split}
\tag{12}
\]

## The cutoff and its error budget

Take
\[
Z=x^\theta=x^{2d/a},\qquad R=Z^{1/d}=x^{2/a}.
\tag{13}
\]
We have \(0<\theta<1\) and \(0<2/a<1\) for every integer
\(d\ge1\). Choose \(x_0=x_0(f,\varepsilon)\ge2\) large enough
that \(Z\ge\max\{2,f(1)\}\) and \(R\ge2\) whenever
\(x\ge x_0\). Then \(Z\le x\) and \(R\le x\).
Since \(f'(t)\ge1\) for \(t\ge1\), the polynomial is strictly
increasing there, continuous, and unbounded. Hence there is a unique
real \(z\ge1\) with \(f(z)=Z\). If \(Y\ge Z\), strict
monotonicity gives \(z\le y\), so every hypothesis used for (12)
holds for the choices (13).

The powers in \(A\) are
\[
Z^{-1/d}R^{1/2}=x^{-2/a}x^{1/a}=x^{-1/a},
\qquad R^{-1/2}=x^{-1/a}.
\]
As \(R\le x\), the two terms of \(A\), separately, satisfy
\[
\begin{split}
Z^{-1/d}R^{1/2}(\log(2R))^2
 &\le x^{-1/a}(\log(2x))^2,\\
R^{-1/2}(\log(2R))^2\log(2x)
 &\le x^{-1/a}(\log(2x))^3.
\end{split}
\]
It follows that
\[
x^2A(x,Z,R)\le Cx^{2-1/a}(\log(2x))^3.
\tag{14}
\]

The initial-modulus estimate in P2, with exponent \(\delta\), applies
to this \(z\), since \(z\ge1\) and \(f(z)=Z\le x\). It gives
\[
0\le V_f(x,z)
\le C_{f,\varepsilon}x^{1+\delta}Z^{2-1/d}
=C_{f,\varepsilon}x^{2-1/a+\delta},
\tag{15}
\]
where the exponent calculation is
\[
1+\theta(2-1/d)=1+\frac{4d-2}{a}=2-\frac1a.
\tag{16}
\]
The other boundary contribution is controlled by (4), because \(x/Z\ge1\):
\[
x^2|F_f(x/Z)|\le C_fx^{1/2}Z^{3/2}
=C_fx^{1/2+3d/a}.
\tag{17}
\]
For all \(d\ge1\),
\[
\left(2-\frac1a\right)-\left(\frac12+\frac{3d}{a}\right)
=\frac{6d-5}{2a}>0.
\tag{18}
\]
Thus (17) is at most \(C_fx^{2-1/a}\).

Here is the complete comparison of the errors in (12), (15), and
(17) with the target exponent. For \(x\ge2\),
\[
\begin{aligned}
x^{3/2+\delta}&\le x^{2-\eta+\varepsilon},
&&\text{since }\eta\le1/5\text{ and }\delta=\varepsilon/2,\\
xY^{1-1/d}&\le x^{2-1/d}\le x^{2-\eta},
&&\text{since }Y\le x,\ 1-1/d\ge0,\ 1/d\ge\eta,\\
x^{9/5+\delta}\log(2x)&\le
 C_\varepsilon x^{9/5+\varepsilon}
 \le C_\varepsilon x^{2-\eta+\varepsilon},
&&\text{since }\log(2x)\le C_\varepsilon x^{\varepsilon/2},\ \eta\le1/5,\\
x^{2-1/a}(\log(2x))^3&\le
 C_\varepsilon x^{2-1/a+\varepsilon/2}
 \le C_\varepsilon x^{2-\eta+\varepsilon},
&&\text{since }(\log(2x))^3\le C_\varepsilon x^{\varepsilon/2},\ \eta\le1/a,\\
x^{2-1/a+\delta}&\le x^{2-\eta+\varepsilon},
&&\text{since }\eta\le1/a,\ \delta=\varepsilon/2,\\
x^{1/2+3d/a}&\le x^{2-1/a}\le x^{2-\eta},
&&\text{by (18) and }\eta\le1/a.
\end{aligned}
\tag{19}
\]
The logarithm bounds used here follow, for any fixed positive power
\(u\), from boundedness of \((\log(2x))^j/x^u\) on \([2,\infty)\)
for \(j=1,3\). Their constants depend only on \(\varepsilon\).

For \(Y\ge Z\), the defining sums split exactly as
\[
V_f(x,y)=V_f(x,z)+V_f(x;z,y).
\]
Subtracting \(x^2F_f(x/Y)\), using (12), and then applying
(14)–(19) gives
\[
\begin{split}
|V_f(x,y)-x^2F_f(x/Y)|
&\le V_f(x,z)+x^2|F_f(x/Z)|\\
&\quad+C_{f,\varepsilon}\big[x^{3/2+\delta}+xY^{1-1/d}
       +x^{9/5+\delta}\log(2x)+x^2A(x,Z,R)\big]\\
&\le C_{f,\varepsilon}x^{2-\eta+\varepsilon}.
\end{split}
\tag{20}
\]

## Moduli below the cutoff

Suppose instead that \(Y<Z=x^\theta\). Apply the initial-modulus
bound in P2 directly with its argument \(z\) equal to \(y\).
Its hypotheses hold because \(y\ge1\) and \(f(y)=Y\le x\).
The exponent \(2-1/d\) is positive, so (16) gives
\[
0\le V_f(x,y)
\le C_{f,\varepsilon}x^{1+\delta}Y^{2-1/d}
\le C_{f,\varepsilon}x^{1+\delta}Z^{2-1/d}
=C_{f,\varepsilon}x^{2-1/a+\delta}.
\tag{21}
\]
Also \(x/Y\ge1\), so (4) and (18) imply
\[
x^2|F_f(x/Y)|
\le C_fx^{1/2}Y^{3/2}
\le C_fx^{1/2}Z^{3/2}
=C_fx^{1/2+3d/a}
\le C_fx^{2-1/a}.
\tag{22}
\]
The triangle inequality, (21), (22), and \(\eta\le1/a\) therefore
give
\[
|V_f(x,y)-x^2F_f(x/Y)|
\le C_{f,\varepsilon}x^{2-\eta+\varepsilon}.
\tag{23}
\]
Together, (20) and (23) prove the first assertion uniformly for all
the required \(x,y\).

## The power main term

For every \(Y\le x\), apply (3) with \(H=x/Y\ge1\) and multiply
by \(x^2\). Tracking the powers gives
\[
\begin{split}
\left|x^2F_f(x/Y)-K_fx^{1/2}Y^{3/2}\right|
&\le C_fx^2(x/Y)^{-13/8}\\
&=C_fx^{3/8}Y^{13/8},
\end{split}
\tag{24}
\]
where \(x^2(x/Y)^{-3/2}=x^{1/2}Y^{3/2}\) identifies the main term.
Combining (24) with the first assertion proves
\[
\left|V_f(x,y)-K_fx^{1/2}Y^{3/2}\right|
\le C_{f,\varepsilon}
\left[x^{3/8}Y^{13/8}+x^{2-\eta+\varepsilon}\right].
\]
Enlarge one constant to cover both asserted inequalities. The choices
of \(x_0\) and all constants made above depend only on \(f\) and
\(\varepsilon\), as required. No numerical sanity checks were used
in this proof.
