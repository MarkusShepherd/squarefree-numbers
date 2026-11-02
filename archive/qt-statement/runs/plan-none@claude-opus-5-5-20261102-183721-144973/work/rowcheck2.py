import json, math, sys
import numpy as np
from sympy import factorint, primerange
d=json.load(open('../results.json'))
eta0=0.2384433666879889749964064
def L0(p): return 1-1/(p*p-1)**2+p**3/(p*p-1)**2
def L1(p): return 1-1/(p*p-1)**2+p**2.5/(p*p-1)**2
def L2(p): return p*p/(p*p-1)
def eta(q):
    v=eta0
    for p,b in factorint(q).items():
        v*= (L1(p) if b==1 else L2(p))/L0(p)
    return v
C={'k^2+1':0.13808263,'k^3+2':0.13560751,'2k+1':0.14261331}
F={'k^2+1':(lambda k:k*k+1,lambda k:2*k),'k^3+2':(lambda k:k**3+2,lambda k:3*k*k)}
def report(name,cum):
    for r in d['polynomials'][name]['rows']:
        x,y,fy,V=r['x'],r['y'],r['fy'],r['V']
        if y not in cum: continue
        model=math.sqrt(x)*cum[y]
        print(f"{name} x={x:>10} r={fy/x:.3f} V/(x^.5fy^1.5)={V/(x**.5*fy**1.5):.5f} V/sum_eta={V/model:.5f} V/(C_f x^.5 fy^1.5)={V/(C[name]*x**.5*fy**1.5):.5f}",flush=True)
for name,(f,fp) in F.items():
    ymax=max(r['y'] for r in d['polynomials'][name]['rows'])
    S=0.0; cum={}
    for k in range(1,ymax+1):
        q=f(k); S+=fp(k)*eta(q)*math.sqrt(q); cum[k]=S
    report(name,cum)
# 2k+1 via sieve up to N
N=16000001
le=np.zeros(N+1)
for p in primerange(2,N+1):
    a=math.log(L1(p)/L0(p)); b=math.log(L2(p)/L0(p))
    le[p::p]+=a
    if p*p<=N: le[p*p::p*p]+= b-a
eta_arr=eta0*np.exp(le)
k=np.arange(1,(N-1)//2+1); q=2*k+1
cs=np.cumsum(2*eta_arr[q]*np.sqrt(q))
cum={int(kk):float(c) for kk,c in zip(k,cs)}
report('2k+1',{y:cum[y] for y in set(r['y'] for r in d['polynomials']['2k+1']['rows']) if y in cum})
