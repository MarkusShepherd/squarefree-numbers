# Problem: squarefree numbers in arithmetic progressions to polynomial moduli

## Notation

- $\mu^2(n)$ is the indicator of squarefree $n$.
- $Q(x;q,l) = \#\{n \le x : n \equiv l \pmod q,\ n \text{ squarefree}\}$.
- $g(q,l) = \lim_{x\to\infty} Q(x;q,l)/x$ (exists; derive its closed form yourself if you need it).
- $E(x;q,l) = Q(x;q,l) - g(q,l)\,x$.
- $f \in \mathbb{Q}[t]$ is an integer-valued polynomial of degree $d \ge 1$ with $f(t) \ge 2$ and $f'(t) \ge 1$ for $t \ge 1$.
- $\rho(m) = \#\{a \bmod m : f(a) \equiv 0 \pmod m\}$.

## Object of study

$$
V_f(x,y) = \sum_{k \le y} f'(k) \sum_{l=1}^{f(k)} E(x; f(k), l)^2 ,
\qquad f(y) \le x .
$$

The weight $f'(k)$ makes the sparse sum over moduli comparable to the full
Montgomery–Hooley variance $V(x,Y) = \sum_{q\le Y}\sum_{l\le q} E(x;q,l)^2$ with
$Y = f(y)$.

## Question

Determine the asymptotic behaviour of $V_f(x,y)$: a main term with an explicit
constant depending on $f$, and error terms, in as large a range of
$f(y) \le x$ as you can justify.

A weaker range or a weaker error term is acceptable **if it is correct**.
You may change the weight $f'(k)$ or restrict the class of $f$ if you state the
change explicitly and justify it.

## Context

The `papers/` folder contains:

- Brüdern–Wooley (2011), *Sparse variance for primes in arithmetic progression*:
  the analogue of this problem for primes, with moduli $f(k)$.
- Brüdern–Granville–Perelli–Vaughan–Wooley (1998), *On the exponential sum over
  k-free numbers*: major-arc estimates for the exponential sum over squarefree
  numbers.
- arXiv:1912.04683, *A variance for k-free numbers in arithmetic progressions of
  given modulus*: the variance for a single fixed modulus. Background only; it
  does not treat the sum over moduli.

**Not included:** R. C. Vaughan, *A variance for k-free numbers in arithmetic
progressions*, Proc. London Math. Soc. (3) 91 (2005), 573–597. It gives the
asymptotic for the full variance $V(x,Y)$ over all moduli $q \le Y$, and is the
natural starting point, but it is paywalled. Use what you can find about it in
the published literature, or reconstruct the parts you need.

The expected approach is to adapt the method for all moduli (Vaughan 2005) to
sparse moduli, as Brüdern–Wooley did for primes. You are not required to follow
it.

`numerics/results.json`, once present, holds exact computations of $V_f(x,y)$
for small $x$. It is ground truth: a predicted main term that disagrees with it
is wrong.
