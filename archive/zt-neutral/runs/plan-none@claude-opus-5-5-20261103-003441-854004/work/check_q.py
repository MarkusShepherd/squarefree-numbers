import numpy as np, math, mpmath as mp
from sympy import factorint, primerange
X=10**6
N=X
mu2=np.ones(N+1,dtype=np.int64); mu2[0]=0
for p in primerange(2,int(N**0.5)+1): mu2[::p*p]=0
Qx=mu2[1:].sum()
P=list(primerange(2,10**6))
A0=mp.mpf(1)
for p in P: A0*=1-mp.mpf(2)/p**2
zeta2inv=1/mp.zeta(2)
def g(q,r,fq):
    val=mp.mpf(6)/mp.pi**2
    for p,v in fq.items():
        val/= (1-mp.mpf(1)/p**2)
        m=min(2,v)
        if r% (p**m)==0: val*= (1-mp.mpf(p)**(m-2))
    return val/q
def Vq(q):
    fq=factorint(q)
    counts=np.bincount((np.nonzero(mu2[1:])[0]+1)%q, minlength=q)
    tot=mp.mpf(0)
    cache={}
    for l in range(q):
        r=math.gcd(l,q)
        if r not in cache: cache[r]=g(q,r,fq)
        e=counts[l]-cache[r]*X
        tot+=e*e
    return tot
def Mq(q,E=200000):
    fq=factorint(q)
    H=mp.mpf(X)/q
    s=mp.mpf(0)
    # e squarefree
    sq=np.ones(E+1,dtype=bool); sq[0]=False
    for p in primerange(2,int(E**0.5)+1): sq[::p*p]=False
    for e in range(1,E+1):
        if not sq[e]: continue
        fe=factorint(e)
        beta=mp.mpf(1)
        for p in fe: beta/= (p*p-2)
        eq=e*e//math.gcd(e*e,q)
        Z=H/eq; t=Z-mp.floor(Z)
        s+=beta*eq*(t*t-t)/2
    # tail e>E: eq>H typically -> eq*B2* = H^2/(2eq)-H/2 ; approx sum beta*(..) ~ -H/2*sum_{e>E} beta
    return -2*A0*q*s
def kappa(q):
    fq=factorint(q); val=mp.mpf(1)
    for p in P[:5000]:
        v=fq.get(p,0); m=min(2,v)
        val*=(1-mp.mpf(1)/p)*(1+mp.mpf(p)**(1-m/2.0)/(p*p-2))
    return val
for q in [101,1000,5003,20000,99991]:
    V=Vq(q); M=Mq(q,E=30000 if q<5000 else 20000)
    pred=4*A0*(-mp.zeta(-0.5))*kappa(q)*mp.sqrt(X*q)
    print(q, float(V), float(M), float(pred), float(V/pred))
