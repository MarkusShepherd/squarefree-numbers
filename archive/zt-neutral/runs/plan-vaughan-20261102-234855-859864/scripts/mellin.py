import numpy as np, mpmath as mp, sys, json
from sympy import primerange
poly=sys.argv[1]
co={'k^2+1':[1,0,1],'k^3+2':[1,0,0,2],'2k+1':[2,1],'k':[1,0]}[poly]
def rho(m):
    a=np.arange(m,dtype=np.int64); v=np.zeros(m,dtype=np.int64)
    for c in co: v=(v*a+c)%m
    return int((v==0).sum())
P=200000
ps=np.array(list(primerange(2,P)),dtype=float)
r1=np.array([rho(int(p)) for p in ps[:2000]]+[0]*0,dtype=float)
# for p>=ps[2000], rho(p) via numpy too (cheap for p<2e5)
r1=np.array([rho(int(p)) for p in ps],dtype=float)
r2=np.array([rho(int(p)**2) if p<1500 else r for p,r in zip(ps,r1)],dtype=float)
C=np.prod(1-2/ps**2)
def logD(s):
    # D(s)=prod_p (1 + p^{-4-2s}/(p^2-2) [ (p^2-p r1) + (p r1 - r2) p^{1+s} + r2 p^{2+2s} ])
    p=ps; ps_=np.exp(-s*np.log(p))  # p^{-s}
    br=(p**2-p*r1)+(p*r1-r2)*p/ps_+r2*p**2/ps_**2
    term=p**-4.0*ps_**2/(p**2-2)*br
    return np.sum(np.log1p(term))
sig=-1.25
ts=np.concatenate([np.linspace(0,20,2001)[:-1],np.linspace(20,400,3801)])
vals=[]
for t in ts:
    s=complex(sig,t)
    z=complex(mp.zeta(s+1))
    vals.append(z*np.exp(logD(s))/(s*(s+1)*(s+2)))
vals=np.array(vals)
def F(w):
    integ=vals*np.exp(complex(sig,0)*np.log(w))*np.exp(1j*ts*np.log(w))
    return -2*C*np.trapezoid(integ.real,ts)/np.pi
res={}
for r in [0.001,0.003,0.01,0.02,0.05,0.1,0.2,0.4,0.7,1.0]:
    w=1/r
    print(poly,'r=',r,' x^2F/(x^.5Y^1.5)=',F(w)*w**1.5)
