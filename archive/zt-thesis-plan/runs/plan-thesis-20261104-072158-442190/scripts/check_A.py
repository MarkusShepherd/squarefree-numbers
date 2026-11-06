import json, numpy as np, mpmath as mp
from sympy import primerange
d=json.load(open('results.json'))
X=1000000
M0=200000
# squarefree m<=M0 and g(m)=prod 1/(p^2-2)
g=np.ones(M0+1); sq=np.ones(M0+1,bool); sq[0]=False
for p in primerange(2,M0+1):
    g[p::p]/= (p*p-2.0)
    sq[p*p::p*p]=False
ms=np.nonzero(sq)[0]; gm=g[ms]
C=1.0
for p in primerange(2,10**6): C*=1-2.0/p/p
gtot=1/(C*(np.pi**2/6))  # sum_m g(m) over squarefree m
tail=gtot-gm.sum()
m2=ms.astype(np.int64)**2
def Psi(x,u):
    dd=np.gcd(np.int64(u),m2)
    L=(u//dd)*m2
    r=x% L
    lam=r*(L-r)/L
    # tail m>M0: L>=m^2>x so Lambda = x - x^2/L ~ x
    return C*(np.dot(gm,lam)+x*tail)
CF={'k^2+1':0.138097517816,'k^3+2':0.135622148902,'2k+1':0.142628701450}
fs={'k^2+1':(lambda k:k*k+1,lambda k:2*k),'k^3+2':(lambda k:k**3+2,lambda k:3*k*k),'2k+1':(lambda k:2*k+1,lambda k:2)}
for name,(f,fp) in fs.items():
    rows=[r for r in d["polynomials"][name]["rows"] if r["x"]==X and r["y"]<=20000]
    ys=sorted(r['y'] for r in rows)
    A=0.0; k=0; out={}
    for yy in ys:
        while k<yy:
            k+=1; A+=fp(k)*Psi(X,f(k))
        out[yy]=A
    for r in sorted(rows,key=lambda r:r['y']):
        fy=r['fy']; V=r['V']; main=CF[name]*X**0.5*fy**1.5
        print(name, r['y'], fy, "V=%.6g A=%.6g (V-A)/V=%.2e  V/main=%.4f A/main=%.4f (V-A)/x^1.5=%.3f"%(V,out[r['y']],(V-out[r['y']])/V,V/main,out[r['y']]/main,(V-out[r['y']])/X**1.5))
