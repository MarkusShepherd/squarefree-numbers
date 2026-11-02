import numpy as np, sys, math
from sympy import factorint
x=int(sys.argv[1]); Qmax=int(sys.argv[2])
N=x
mu2=np.ones(N+1,dtype=bool); mu2[0]=False
d=2
while d*d<=N:
    mu2[d*d::d*d]=False; d+=1
sq=np.nonzero(mu2)[0]
six=6/math.pi**2
out=np.zeros(Qmax+1)
for q in range(1,Qmax+1):
    cnt=np.bincount(sq%q,minlength=q).astype(np.float64)
    fac=factorint(q)
    base=six/q
    for p in fac: base/= (1-p**-2)
    a=np.arange(q)
    g=np.full(q,base)
    for p,e in fac.items():
        s=np.zeros(q,dtype=int)
        aa=a.copy(); 
        # p-adic valuation capped at e (a=0 -> e)
        v=np.zeros(q,dtype=int)
        m=np.ones(q,dtype=bool)
        for j in range(1,e+1):
            m &= (a % p**j==0); v+=m
        me=min(2,e)
        g*= np.where(v>=me, 1-p**(me-2.0), 1.0)
    E=cnt-g*x
    out[q]=(E*E).sum()
np.save(f"V_{x}_{Qmax}.npy",out)
