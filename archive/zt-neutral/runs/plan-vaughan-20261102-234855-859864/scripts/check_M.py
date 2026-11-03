import numpy as np, json, sys, math
from sympy import primerange
x=int(sys.argv[1]); poly=sys.argv[2]; M=int(sys.argv[3])
F={'k^2+1':(lambda k:k*k+1,lambda k:2*k),'k^3+2':(lambda k:k**3+2,lambda k:3*k*k),'2k+1':(lambda k:2*k+1,lambda k:2)}[poly]
f,fp=F
# squarefree indicator up to max(M, x)
N=max(M,x)+1
sf=np.ones(N,dtype=bool); sf[0]=False
for p in primerange(2,int(N**0.5)+1): sf[p*p::p*p]=False
Qx=int(sf[1:x+1].sum())
# g(m) for squarefree m<=M : prod 1/(p^2-2)
g=np.zeros(M+1); g[1:]=1.0
for p in primerange(2,M+1):
    g[p::p]*=1.0/(p*p-2)
g[~sf[:M+1]]=0; g[0]=0
ms=np.nonzero(g)[0].astype(np.int64); gm=g[ms]
C=1.0
for p in primerange(2,10**6): C*=1-2.0/p/p
z2=math.pi**2/6
# tail sum of g beyond M approx: sum_{m>M} g(m) ~ A/M with A = lim m-sum density
# estimate A from data: sum_{M/2<m<=M} g(m) ~ A(1/(M/2)-1/M)=A/M
A=gm[ms>M//2].sum()*M
tail=A/M
m2=ms*ms
def P(q):
    e=np.gcd(m2,q); r=m2//e
    th=x/(q*r.astype(float)); fr=th-np.floor(th)
    B=(fr*fr-fr)/2
    return Qx - x/z2 - 2*C*np.sum(gm*q*r*B) + C*x*tail   # tail: qr>x so qrB=x^2/(2qr)-x/2 ~ -x/2
d=json.load(open('results.json'))['polynomials'][poly]['rows']
for row in d:
    if row['x']!=x: continue
    y=row['y']; tot=0.0
    for k in range(1,y+1):
        tot+=fp(k)*P(f(k))
    Y=f(y); nrm=math.sqrt(x)*Y**1.5
    print(y,Y,'V=%.6e'%row['V'],'pred=%.6e'%tot,'rel diff=%.4f'%((tot-row['V'])/row['V']),'V/nrm=%.4f pred/nrm=%.4f'%(row['V']/nrm,tot/nrm))
