# Proof of P6

We use P5 as a black box, with the notation in `statement.md` and
`deps/P5.md`. In particular,
\[
D_f(s)=\zeta(s)\zeta(2s+2)H_f(s)\qquad(\Re s>-3/4),
\tag{1}
\]
as an identity of meromorphic functions. The Euler product defining
\(H_f\) is holomorphic in this half-plane. All constants constructed below
are independent of the real variable \(H\geq1\).

## 1. The external statements used

The only external source used is H. L. Montgomery and R. C. Vaughan,
*Multiplicative Number Theory I. Classical Theory* (2007), Chapter 10,
pp. 329–330, [doi:10.1017/CBO9780511618314.012](https://doi.org/10.1017/CBO9780511618314.012),
as supplied in
`papers/montgomery-vaughan-2007/analytic_properties_of_the_zeta_function_and_lfunctions.pdf`.
Here are the two statements used, quoted verbatim, with mathematical
typesetting transcribed from the PDF.

> **Corollary 10.4** For all \(s\ne1\),
> \[
> \zeta(s)=\zeta(1-s)2^s\pi^{s-1}\Gamma(1-s)\sin\frac{\pi s}{2}.
> \tag{10.9}
> \]

> **Corollary 10.5** Suppose that \(A>0\) is fixed. Then
> \[
> |\zeta(s)|\asymp\tau^{1/2-\sigma}|\zeta(1-s)|
> \]
> uniformly for \(|\sigma|\leq A\) and \(|t|\geq1\). Here
> \(\tau=|t|+4\), as usual.

Both quotations were checked against rendered pages of the supplied PDF.
For Corollary 10.4 we will only need \(-5/8\leq\Re s<0\) and a
neighborhood of zero. These points satisfy \(s\ne1\). In the negative
strip \(\Re(1-s)>1\), so \(\zeta(1-s)\) is analytic there;
\(\Gamma(1-s)\) is analytic there because its argument has positive real
part. At zero, the pole of \(\zeta(1-s)\) is canceled by
\(\sin(\pi s/2)\). Thus \(\zeta(s)\) is analytic in the negative strip
and at zero. In the positive half-plane its only pole is the simple pole
at one with residue one; this also follows directly from (3) below.

For Corollary 10.5 we fix \(A=2\), and use it only when
\(-5/8\leq\sigma\leq1/4\) and \(|t|\geq2\). Hence \(A>0\),
\(|\sigma|\leq A\), and \(|t|\geq1\) all hold throughout its use.
Let \(Q>0\) be a constant such that its upper inequality reads
\[
|\zeta(\sigma+it)|
\leq Q(|t|+4)^{1/2-\sigma}|\zeta(1-\sigma-it)|
\tag{2}
\]
in this range. No conditional estimate for zeta is used.

## 2. Bounds throughout the contour strip

We first derive a positive-half-plane estimate, including its dependence
on the imaginary part. For an integer \(N\geq1\), partial summation of
the tail of the defining series gives, initially for \(\Re s>1\),
\[
\zeta(s)=\sum_{n\leq N}n^{-s}
       +\frac{N^{1-s}}{s-1}
       -s\int_N^\infty\{u\}u^{-s-1}\,du.
\tag{3}
\]
Indeed, write the tail as \(\int_N^\infty u^{-s}\,d\lfloor u\rfloor\),
replace \(\lfloor u\rfloor\) by \(u-\{u\}\), and integrate the second
term by parts. The boundary term at \(N\) vanishes because \(N\) is an
integer. The integral in (3) converges locally uniformly for
\(\Re s>0\), since \(0\leq\{u\}<1\); hence (3) holds there by analytic
continuation, away from \(s=1\). It also shows that the residue at one is
one and that there are no other poles in that half-plane.

Let \(s=\alpha+iv\), \(V=|v|\geq2\),
\(\delta\leq\alpha\leq6\), and \(\delta\in\{1/4,3/4\}\). Choose
\(N=\lceil V\rceil\), so \(V\leq N\leq3V/2\). The finite sum in (3)
has exactly \(N\) terms. Each term has modulus at most \(n^{-\delta}\),
and after summation its modulus is at most
\[
\sum_{n\leq N}n^{-\delta}
\leq1+\int_1^N u^{-\delta}\,du
\leq\frac{N^{1-\delta}}{1-\delta}
\leq\frac{(3/2)^{1-\delta}}{1-\delta}V^{1-\delta}.
\]
The other two terms satisfy
\[
\left|\frac{N^{1-s}}{s-1}\right|
\leq\frac{N^{1-\delta}}{V}
\leq(3/2)^{1-\delta}V^{-\delta}
\leq(3/2)^{1-\delta}V^{1-\delta}
\]
and
\[
\left|s\int_N^\infty\{u\}u^{-s-1}\,du\right|
\leq\frac{|s|}{\alpha}N^{-\alpha}
\leq\frac{V+6}{\delta}V^{-\delta}
\leq\frac4\delta V^{1-\delta}.
\]
Consequently, with the explicit constants
\[
C_\delta=(3/2)^{1-\delta}
              \left(\frac1{1-\delta}+1\right)+\frac4\delta,
\]
we have
\[
|\zeta(\alpha+iv)|\leq C_\delta V^{1-\delta}
\quad(\delta\leq\alpha\leq6,\ V\geq2).
\tag{4}
\]

Now put \(s=\sigma+it\), \(-5/8\leq\sigma\leq2\), and \(T=|t|\geq2\).
For \(1/4\leq\sigma\leq2\), (4) with \(\delta=1/4\) gives
\[
|\zeta(s)|\leq C_{1/4}T^{3/4}\leq C_{1/4}T^{11/8}.
\]
For \(-5/8\leq\sigma\leq1/4\), the real part of \(1-s\) lies in
\([3/4,13/8]\), so (4) with \(\delta=3/4\), followed by (2), gives
\[
\begin{aligned}
|\zeta(s)|
&\leq Q(T+4)^{1/2-\sigma}C_{3/4}T^{1/4}\\
&\leq Q3^{9/8}C_{3/4}T^{3/4-\sigma}
\leq Q3^{9/8}C_{3/4}T^{11/8}.
\end{aligned}
\]
Here \(T+4\leq3T\) and \(1/4\leq1/2-\sigma\leq9/8\).
Also \(3/4\leq\Re(2s+2)\leq6\), and its imaginary part has modulus
\(2T\geq4\). Thus
\[
|\zeta(2s+2)|\leq C_{3/4}(2T)^{1/4}.
\tag{5}
\]

We next obtain a bound for \(H_f(s)\) uniform on this whole strip.
This is a uniformity supplement to the fixed-line bound in P5; we do not
need to strengthen its domain of continuation. Write \(d=\deg f\), and
let \(\mathcal B\) be the finite set of primes dividing every coefficient
of \(f\). For \(p\notin\mathcal B\), its reduction is a nonzero
polynomial over \(\mathbb F_p\), with at most \(d\) roots. Each residue
modulo \(p\) has exactly \(p\) lifts modulo \(p^2\), whence
\[
0\leq\rho(p)\leq d,\qquad0\leq\rho(p^2)\leq dp.
\tag{6}
\]
Use the quantities \(a_p,b_p,c_p\) defined in P5, and put
\(u_p=b_p-a_p\), \(q_p=c_p-b_p\). Since \(p^2-2\geq p^2/2\), (6)
gives
\[
\begin{gathered}
|a_p-1|\leq2dp^{-3},\qquad |u_p|\leq4dp^{-3},
\qquad |q_p|\leq(d+2)p^{-2},\\
|q_p-p^{-2}|\leq(2+2d)p^{-3},
\qquad |q_p-a_pp^{-2}|\leq(2+4d)p^{-3},\\
|(1-2p^{-2})a_p-1|\leq(2+4d)p^{-2}.
\end{gathered}
\tag{7}
\]
For the fourth inequality, the exact difference is
\[
q_p-p^{-2}=\frac{2-p\rho(p)}{p^2(p^2-2)},
\]
whose modulus is at most \(4p^{-4}+2dp^{-3}\leq(2+2d)p^{-3}\).
The fifth follows by adding \(|a_p-1|p^{-2}\leq2dp^{-5}\).
For the last inequality, the bound before collecting powers is
\(2dp^{-3}+2p^{-2}+4dp^{-5}\), which is at most the stated bound.

Set \(z=p^{-s}\). The local factor of \(H_f\) is exactly
\[
L_p(s)=(1-2p^{-2})
 \left[a_p+u_pz+(q_p-a_pp^{-2})z^2
                    -u_pp^{-2}z^3-q_pp^{-2}z^4\right].
\]
Since \(|z|=p^{-\sigma}\leq p^{5/8}\), (7) implies
\[
\begin{aligned}
|L_p(s)-1|\leq{}& (2+4d)p^{-2}+4dp^{-19/8}
 +(2+4d)p^{-7/4}\\
&+4dp^{-25/8}+(d+2)p^{-3/2}
\leq(6+17d)p^{-3/2}.
\end{aligned}
\tag{8}
\]
The prime sum of these bounds is at most
\[
(6+17d)\sum_{n=2}^\infty n^{-3/2}
\leq(6+17d)\int_1^\infty u^{-3/2}\,du
=2(6+17d).
\]
Thus the product over \(p\notin\mathcal B\) has modulus at most
\(\exp(2(6+17d))\). The remaining product has exactly
\(|\mathcal B|\) factors. Before multiplication each such factor is
bounded by the following finite number:
\[
U_p=(1-2p^{-2})(1+p^{-3/4})
       \left(|a_p|+|u_p|p^{5/8}+|q_p|p^{5/4}\right).
\]
After multiplication their modulus is at most
\(\prod_{p\in\mathcal B}U_p\), with the empty product equal to one.
Therefore
\[
|H_f(s)|\leq M_H,
\qquad
M_H=\exp(2(6+17d))\prod_{p\in\mathcal B}U_p,
\quad -5/8\leq\Re s\leq2.
\tag{9}
\]
Combining (1), (4), (5), and (9), define
\[
C_D=M_H\max\{C_{1/4},Q3^{9/8}C_{3/4}\}
                    2^{1/4}C_{3/4}.
\]
We then have the explicit growth estimate
\[
|D_f(\sigma+it)|\leq C_D|t|^{13/8}
\quad(-5/8\leq\sigma\leq2,\ |t|\geq2),
\tag{10}
\]
where the exponent is \(11/8+1/4=13/8\).

## 3. Mellin representation and contour displacement

The elementary kernel identity needed here is, for \(v>0\),
\[
\frac1{2\pi i}\int_{1-i\infty}^{1+i\infty}
             \frac{2v^z}{z(z+1)(z+2)}\,dz
=\begin{cases}(1-v^{-1})^2,&v\geq1,\\0,&0<v<1.\end{cases}
\tag{11}
\]
For completeness, close a finite rectangle to the left when \(v\geq1\),
and to the right when \(v<1\). On a fixed horizontal segment at height
\(T\), the denominator has modulus at least \(T^3\), so those integrals
tend to zero as \(T\) tends to infinity. A new left edge
\(\Re z=-N-1/2\), \(N\geq3\), has normalized integral in modulus at most
\[
\frac{v^{-N-1/2}}{\pi}
\int_{-\infty}^{\infty}
       \frac{dt}{((N-3/2)^2+t^2)^{3/2}}
=\frac{2v^{-N-1/2}}{\pi(N-3/2)^2},
\]
because each of
\(|z|,|z+1|,|z+2|\) is at least
\(\sqrt{(N-3/2)^2+(\Im z)^2}\). This tends to zero also at \(v=1\).
A new right edge \(\Re z=N\) has normalized integral at most
\(2v^N/(\pi N^2)\), which tends to zero for \(v<1\). The left-hand residues
are \(1,-2v^{-1},v^{-2}\), respectively, at \(0,-1,-2\). Their sum is
the first expression in (11), including its value zero at \(v=1\).

Apply (11) with \(v=H/h\), multiply by \(H^2W_f(h)/h\), and sum over
positive integers \(h\). P5 gives
\(A_2:=\sum_{h=1}^\infty|W_f(h)|h^{-2}<\infty\).
On putting \(s=z+1\), the sum of absolute values of the integrands on
\(\Re s=2\) is bounded by
\[
\frac{2H^3 A_2}{|(s-1)s(s+1)|}.
\]
Its integral over the entire vertical line is finite: for \(|\Im s|\geq1\)
it is at most \(2H^3A_2|\Im s|^{-3}\), and on the remaining compact
segment the denominator does not vanish. Absolute convergence therefore
justifies the exchange of the infinite sum and integral. It gives
\[
\Theta_f(H)=\frac1{2\pi i}\int_{2-i\infty}^{2+i\infty}G_H(s)\,ds,
\qquad
G_H(s)=\frac{2D_f(s)H^{s+1}}{(s-1)s(s+1)}.
\tag{12}
\]
The equality holds for all real \(H\geq1\); an integer endpoint has
weight zero in both (11) and the definition of \(\Theta_f\).

Shift the contour to \(\Re s=-5/8\). The only possible poles of
\(D_f\) in the intervening strip are at \(1\) and \(-1/2\), from
\(\zeta(s)\) and \(\zeta(2s+2)\), respectively. This follows from
(1), the analyticity of \(H_f\) supplied by P5, and the zeta properties
checked in Section 1. The kernel additionally has a pole at zero; its
pole at \(-1\) lies outside the strip.

Here are explicit bounds justifying the displacement. At heights
\(\pm T\), \(T\geq2\), each denominator factor in (12) has modulus at
least \(T\), while \(H^{\sigma+1}\leq H^3\) because \(H\geq1\).
Thus (10) gives the bound
\[
|G_H(\sigma\pm iT)|\leq2C_DH^3T^{13/8-3}
                         =2C_DH^3T^{-11/8}.
\]
Each horizontal segment has length \(2+5/8=21/8\). After integration
over both segments, the bound is at most
\[
\frac{21}{2}C_DH^3T^{-11/8},
\]
which tends to zero for each fixed \(H\). This limit is taken before
asserting the uniform bound for the resulting left vertical integral.

For that vertical line define the finite constant
\[
M_0=\max_{|t|\leq2}|D_f(-5/8+it)|.
\]
It is finite because the line contains no poles. Its denominator in
(12) satisfies, for all real \(t\),
\[
|(s-1)s(s+1)|\geq\frac{13}{8}\frac58\frac38=\frac{195}{512}.
\]
The compact part of the line has length four; before integration its
integrand is bounded by
\((1024/195)M_0H^{3/8}\), so after integration it contributes at most
\((4096/195)M_0H^{3/8}\) to the absolute integral. On either infinite
tail, (10) gives
\[
|G_H(-5/8+it)|\leq2C_DH^{3/8}|t|^{-11/8}
\qquad(|t|\geq2).
\]
After integration over both tails the bound is
\[
4C_DH^{3/8}\int_2^\infty t^{-11/8}\,dt
=\frac{32}{3}C_D2^{-3/8}H^{3/8}.
\]
In particular, the left integral is absolutely convergent, and
\[
\left|\frac1{2\pi i}\int_{-5/8-i\infty}^{-5/8+i\infty}
                                      G_H(s)\,ds\right|
\leq C_*H^{3/8},
\tag{13}
\]
where the finite constant depending only on \(f\) can be taken to be
\[
C_* =\frac1{2\pi}
       \left(\frac{4096}{195}M_0+
                         \frac{32}{3}C_D2^{-3/8}\right).
\tag{14}
\]
The residue theorem on the finite rectangles, followed by the limits
just justified, now gives (12) as the sum of the three residues and the
left integral.

## 4. Residues and the two estimates

Write the Laurent expansion at one as
\[
D_f(s)=\frac{R_f}{s-1}+L_f+(s-1)J_f(s),
\]
Here P5 identifies \(R_f=P_f(1)\), and the definition in the statement
gives \(B_f=L_f-3R_f/2\). Here \(J_f\) is analytic on a fixed disk
about one. On a smaller closed disk choose a finite constant \(A_f\)
with \(|J_f(s)|\leq A_f\); the local remainder is therefore bounded
by \(A_f|s-1|\). No such
local remainder is summed or integrated in the argument.

Set \(q(s)=2/[s(s+1)]\). Direct differentiation gives
\(q(1)=1\), \(q'(1)=-3/2\). Hence the residue of
\(q(s)D_f(s)H^{s+1}/(s-1)\) at one is exactly
\[
H^2\left(L_f+R_f\log H-\frac32R_f\right)
=R_fH^2\log H+B_fH^2.
\tag{15}
\]
At zero, P5 gives \(D_f(0)=-1/(2\zeta(2))=-c/2\), and consequently
\[
\mathop{\rm Res}_{s=0}G_H(s)
=-2D_f(0)H=cH.
\tag{16}
\]
At \(-1/2\), the denominator \((s-1)s(s+1)\) equals \(3/8\).
Using exactly the definition of \(K_f\) in the statement, we obtain
\[
\mathop{\rm Res}_{s=-1/2}G_H(s)
=\frac{16}{3}H^{1/2}\mathop{\rm Res}_{s=-1/2}D_f(s)
=-K_fH^{1/2}.
\tag{17}
\]
This definition agrees with the one in P5: the simple pole of
\(\zeta(2s+2)\) has residue \(1/2\), so (1) gives
\[
-\frac{16}{3}\mathop{\rm Res}_{s=-1/2}D_f(s)
=-\frac83\zeta(-1/2)H_f(-1/2).
\]

Let \(E_f(H)\) denote the normalized left vertical integral in (13).
Equations (12)–(17) establish the exact formula
\[
\Theta_f(H)=R_fH^2\log H+B_fH^2+cH-K_fH^{1/2}+E_f(H),
\qquad |E_f(H)|\leq C_*H^{3/8}
\tag{18}
\]
for every real \(H\geq1\). Thus no loss depending on whether \(H\) is
an integer is present. Choose \(C(f)=1+C_*\), which is strictly positive.
The first asserted inequality follows from (18). Substituting (18) into
the definition of \(F_f\) gives the exact identity
\[
F_f(H)=K_fH^{-3/2}-\frac{E_f(H)}{H^2}.
\]
Therefore
\[
|F_f(H)-K_fH^{-3/2}|
\leq C_*H^{3/8-2}=C_*H^{-13/8}
\leq C(f)H^{-13/8},
\]
which proves the second assertion with the same constant.

## 5. The integral identity

Fix real \(x\geq2\) and \(2\leq Z\leq Y\leq x\), and put
\(r_+=\max(r,0)\). Throughout \(Z\leq t\leq Y\), every nonzero
term of the integrand has \(h\leq x/Z\). Thus only
\(\lfloor x/Z\rfloor\) integers can occur, and we may write the
finite sum identity
\[
2\int_Z^Y\sum_{1\leq h\leq x/t}(x-ht)W_f(h)\,dt
=\sum_{h=1}^{\lfloor x/Z\rfloor}W_f(h)
                                  2\int_Z^Y(x-ht)_+\,dt.
\tag{19}
\]
For each such positive integer \(h\), the function
\((x-ht)_+^2\) is continuously differentiable, including at
\(t=x/h\), and its derivative is \(-2h(x-ht)_+\). Therefore its
integral is exactly
\[
2\int_Z^Y(x-ht)_+\,dt
=\frac{(x-hZ)_+^2-(x-hY)_+^2}{h}.
\tag{20}
\]
Multiplying out the definition of \(\Theta_f\) gives
\[
Z^2\Theta_f(x/Z)
=\sum_{h=1}^{\lfloor x/Z\rfloor}\frac{W_f(h)}h(x-hZ)_+^2,
\]
and
\[
Y^2\Theta_f(x/Y)
=\sum_{h=1}^{\lfloor x/Z\rfloor}\frac{W_f(h)}h(x-hY)_+^2.
\]
In the second equality, terms with \(h>x/Y\) vanish, so the indicated
extension of its finite summation range changes its value by exactly
zero. Subtract these two equalities and use (19)–(20). The result is
\[
2\int_Z^Y\sum_{1\leq h\leq x/t}(x-ht)W_f(h)\,dt
=Z^2\Theta_f(x/Z)-Y^2\Theta_f(x/Y).
\]
This is exact throughout the requested range, and has no error term.

Exact symbolic checks in Python/SymPy verified the local-factor
expansion, the kernel coefficient at \(-1/2\), the kernel residue at
zero, and \(q(1)=1\), \(q'(1)=-3/2\). No numerical sanity check was
used. No excluded source or previous-run write-up was consulted, and no
objections file was supplied for this attempt.
