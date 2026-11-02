import numpy as np, math
from sympy import factorint, primerange
x=10**6
V=np.load('V_1000000_10000.npy')
C=1.0
for p in primerange(2,10**6): C*=1-2/p**2
# A(n) = C prod_{p^2|n} (p^2-1)/(p^2-2) ; precompute for n<=x via sieve
N=x
logA=np.zeros(N+1)
for p in primerange(2,int(N**.5)+1):
    logA[p*p::p*p]+=math.log((p*p-1)/(p*p-2))
A=C*np.exp(logA)
six=6/math.pi**2
eta0=0.2384433666879889749964064
def L0(p): return 1-1/(p*p-1)**2+p**3/(p*p-1)**2
def L1(p): return 1-1/(p*p-1)**2+p**2.5/(p*p-1)**2
def L2(p): return p*p/(p*p-1)
def eta(q):
    v=eta0
    for p,b in factorint(q).items(): v*=(L1(p) if b==1 else L2(p))/L0(p)
    return v
def sumg2(q):
    # sum_l g(q,l)^2 = q^{-1} sum_{s|q} phi(s) tau(s)^2, tau(s)^2=six^2 prod (p^2-1)^-2 for cubefree s
    fac=factorint(q); tot=1.0
    for p,b in fac.items():
        t=1/(p*p-1)**2
        tot*= 1 + (p-1)*t + (p*p-p)*t*(1 if b>=2 else 0)
    return six**2*tot/q
for q in [1001,2000,2048,3001,4096,5000,7919,9973,9999,10000]:
    v=np.arange(1,x//q+1)
    Vs=six*x+2*np.sum(A[v*q]*(x-v*q))-x*x*sumg2(q)
    print(q, 'V*=%.1f'%Vs, 'eta*sqrt=%.1f'%(eta(q)*math.sqrt(x*q)), 'actual V=%.1f'%V[q], 'ratio V*/eta=%.4f'%(Vs/(eta(q)*math.sqrt(x*q))), '(V*-eta sqrt)/q=%.3f'%((Vs-eta(q)*math.sqrt(x*q))/q))
