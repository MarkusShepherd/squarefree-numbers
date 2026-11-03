import numpy as np, math
from sympy import primerange, factorint
P=list(primerange(2,200000))
c2=np.prod([1-2.0/p**2 for p in P])
def g(q,l):
    # sum over squarefree m of mu(m)(m^2,q)/(m^2 q) with (m^2,q)|l ; truncate m by Euler product
    # multiplicative: product over p
    pr=1.0
    for p in P:
        d=math.gcd(p*p,q)
        term = -d/(p*p) if l % d==0 else 0.0
        pr*=1+term
        if p>5000: break
    return pr/q
def G(q):
    from collections import Counter
    c=Counter(math.gcd(l,q) for l in range(1,q+1))
    return sum(n*g(q,r)**2 for r,n in c.items())
def F1(q):
    pr=1.0
    for p in P:
        if p>5000: break
        pr*=1+math.gcd(p*p,q)/p**2/(p*p-2)
    return pr
for q in [1,2,4,6,12,18,25,30]:
    print(q, c2*F1(q), q*G(q))
