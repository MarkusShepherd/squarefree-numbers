import numpy as np, math, mpmath as mp
from sympy import primerange, divisors
x=4*10**7
sf=np.ones(x+1,dtype=bool); sf[0]=False
for d in range(2,int(x**0.5)+1):
    sf[d*d::d*d]=False
n=np.nonzero(sf)[0]
P=list(primerange(2,10**6))
c2=float(np.prod([1-2.0/p**2 for p in P]))
z=float(mp.zeta(-0.5))
def g(q,l):
    pr=1.0
    for p in P:
        if p>20000: break
        d=math.gcd(p*p,q)
        if l % d==0: pr*=1-d/(p*p)
    return pr/q
def kappa(q):
    lp=0.0
    for p in P:
        if q%(p*p)==0: lam=1/p
        elif q%p==0: lam=p**-0.5
        else: lam=1.0
        lp+=math.log((1-1/p)*(1+lam*p/(p*p-2)))
    return -4*c2*z*math.exp(lp)
for q in [10007, 30000, 100003, 100000, 300007, 360360, 1000003, 3000017]:
    Q=np.bincount(n%q,minlength=q).astype(float)
    gl=np.empty(q); cache={}
    for l in range(q):
        r=math.gcd(l,q)
        if r not in cache: cache[r]=g(q,r)
        gl[l]=cache[r]
    V=np.sum((Q-gl*x)**2)
    k=kappa(q)
    print(q, 'V/(x^.5 q^.5)=%.4f'%(V/(x*q)**0.5), 'kappa=%.4f'%k, 'q/x=%.4f'%(q/x))
