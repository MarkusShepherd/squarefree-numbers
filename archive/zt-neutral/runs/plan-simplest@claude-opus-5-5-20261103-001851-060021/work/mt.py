import numpy as np, json, sys
from sympy import factorint
from mpmath import zeta
R=json.load(open(sys.argv[1]))
T=2_000_000
# squarefree t and eta(t)=prod 1/(p^2-2), plus prime factor list for gcd with q
mu2=np.ones(T+1,bool); mu2[0]=False
for p in range(2,int(T**.5)+1): mu2[p*p::p*p]=False
eta=np.ones(T+1)
isp=np.ones(T+1,bool); isp[:2]=False
for p in range(2,int(T**.5)+1):
    if isp[p]: isp[p*p::p]=False
primes=np.nonzero(isp)[0]
for p in primes: eta[p::p]/= (p*p-2.0)
ts=np.nonzero(mu2)[0]; et=eta[ts]
A0=np.prod([1-2.0/p**2 for p in primes])
h0=-4*float(zeta(-0.5))*np.prod([(1-1.0/p)**2*(1+2.0/p) for p in primes])
def B(u): fr=u-np.floor(u); return fr*(1-fr)
def MT(q,x):
    f=factorint(q)
    m=ts.astype(float)**2
    for p,a in f.items():
        sel=(ts%p==0)
        m[sel]/= p**min(a,2)
    X=x/q
    s=np.sum(et*m*B(X/m))
    # tail t>T: B~X/m, eta*m*X/m = X*eta ; sum eta(t) for t>T ~ ∏... ~ 6/pi^2/A0 /T roughly
    s+= X*(6/np.pi**2/A0)/T
    return A0*q*s
def h(q):
    v=h0
    for p,a in factorint(q).items():
        v*= (p*p-2+p**.5)/((p+2)*(p-1)) if a==1 else (p+1)/(p+2)
    return v
f=lambda k:k*k+1; fp=lambda k:2*k
for row in R['polynomials']['k^2+1']['rows']:
    x,y,V=row['x'],row['y'],row['V']
    if x not in (1000000,4000000): continue
    mt=sum(fp(k)*MT(f(k),x) for k in range(1,y+1))
    hh=sum(fp(k)*h(f(k))*np.sqrt(x*f(k)) for k in range(1,y+1))
    print(x,y,row['ratio_actual'],'V/MTsum=%.5f'%(V/mt),'V/hsum=%.5f'%(V/hh),'(V-MT)/x^(5/3)=%.4f'%((V-mt)/x**(5/3)))
