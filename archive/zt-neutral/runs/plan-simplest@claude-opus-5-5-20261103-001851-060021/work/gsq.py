from fractions import Fraction as Fr
from sympy import factorint, primerange
import math
# g(q,l)/(6/pi^2) = prod_{p^a||q} loc ; loc from local densities; compare sum_l g^2 with A0/q sum_t eta(t)(t^2,q)/t^2
def loc(p,a,l):
    # density of n≡l mod p^a with p^2∤n, divided by (1-p^-2)
    v=0; L=l% p**a
    # count residues n mod p^(a+2) congruent to l mod p^a with p^2 ∤ n
    M=p**(max(a,2)); c=sum(1 for n in range(M) if n%(p**a)==L and n%(p*p)!=0)
    return Fr(c,M)/(1-Fr(1,p*p))
for q in [2,3,4,6,8,9,12,18,25,36,50]:
    f=factorint(q)
    S=1.0
    for p,a in f.items():
        S*=float(sum(loc(p,a,l)**2 for l in range(p**a)))
    lhs=S*(6/math.pi**2)**2
    # rhs: A0/q * prod_{p|q}(1+eta(p)(p^2,q)/p^2) * prod_{p∤q}(1+eta(p)/p^2)
    A0=1.0;r=1.0
    for p in primerange(2,200000):
        A0*=1-2/p**2
        e=1/(p*p-2); g=math.gcd(p*p,q)
        r*=1+e*g/p**2
    rhs=A0/q*r
    print(q,lhs,rhs,lhs/rhs)
