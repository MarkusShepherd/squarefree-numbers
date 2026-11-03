import numpy as np, math, mpmath as mp
from sympy import primerange
P=list(primerange(2,10**6))
c2=float(np.prod([1-2.0/p**2 for p in P])); z=float(mp.zeta(-0.5))
def kappa(q):
    lp=0.0
    for p in P:
        lam = 1/p if q%(p*p)==0 else (p**-0.5 if q%p==0 else 1.0)
        lp+=math.log((1-1/p)*(1+lam*p/(p*p-2)))
    return -4*c2*z*math.exp(lp)
def F1(q):
    return float(np.prod([1+math.gcd(p*p,q)/p**2/(p*p-2) for p in P]))
Hmax=4*10**6
for q in [1,6,7,12]:
    N=q*Hmax
    # A(hq) for h<=Hmax: A(r)=c2*prod_{p^2|r} (p^2-1)/(p^2-2)
    A=np.full(Hmax+1,c2)
    for p in P:
        if p*p>N: break
        L=p*p//math.gcd(p*p,q)
        A[L::L]*= (p*p-1)/(p*p-2)
    h=np.arange(Hmax+1,dtype=float)
    cs=np.cumsum(A[1:]); chs=np.cumsum(A[1:]*h[1:])
    k=kappa(q); a2=c2*F1(q)/2
    out=[]
    for H in [10**4,10**5,10**6,4*10**6]:
        S=H*cs[H-1]-chs[H-1]
        rem=S-a2*H*H+3/math.pi**2*H
        out.append((H, rem/H**0.5, (rem-k/2*H**0.5)/H**0.25))
    print(q,'kappa/2=%.5f'%(k/2),[('%d'%H,'%.5f'%a,'%.3f'%b) for H,a,b in out])
