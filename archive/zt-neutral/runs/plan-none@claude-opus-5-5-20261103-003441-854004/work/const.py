import mpmath as mp
from sympy import primerange
mp.mp.dps=30
# J = 1/2 int_0^inf B2*(u) u^{-3/2} du, B2*(u)=({u}^2-{u})/2
def B2s(u):
    t=u-mp.floor(u); return (t*t-t)/2
J0 = mp.quad(lambda u:(u*u-u)/2*u**-1.5,[0,1])
# for u>=1 sum over n of int_0^1 ((t^2-t)/2)(n+t)^-1.5 dt
def piece(n): return mp.quad(lambda t:(t*t-t)/2*(n+t)**-1.5,[0,1])
S=mp.nsum(piece,[1,mp.inf])
J=(J0+S)/2
print('J',J, ' compare zeta(-1/2)=',mp.zeta(-0.5))
P=list(primerange(2,200000))
A0=mp.mpf(1)
for p in P: A0*=1-mp.mpf(2)/p**2
print('A0',A0)
def h(p): return mp.mpf(p)**2/(p*p-2)
def kap(p,v): return (1-mp.mpf(1)/p)*(1+h(p)*mp.mpf(p)**(-min(2,v)/mp.mpf(2))/p)
# mean over all q
mean_full=mp.mpf(1)
for p in P:
    pr=[(1-mp.mpf(1)/p), (1-mp.mpf(1)/p)/p, mp.mpf(1)/p**2]  # v=0, v=1, v>=2
    mean_full*= pr[0]*kap(p,0)+pr[1]*kap(p,1)+pr[2]*kap(p,2)
pred_full = -2*A0*J*mp.mpf(2)/3*mean_full
print('pred full const', pred_full)
# Vaughan c2
C1=mp.mpf(1)
for p in P:
    p=mp.mpf(p)
    C1*=1+((p-1)**2*p**(1.5)-2*p**4+p**3+2*p**3-p)/(p**2*(p**2-1)**2)
c2=2*C1*4*(-mp.zeta(-0.5))/(mp.zeta(2)**2*3*1)
print('C1',C1,'Vaughan c2',c2)
for N in [1000,10000,100000,200000]:
    a=mp.mpf(1); b=mp.mpf(1); A=mp.mpf(1)
    for p in P:
        if p>N: break
        pr=[(1-mp.mpf(1)/p), (1-mp.mpf(1)/p)/p, mp.mpf(1)/p**2]
        a*= pr[0]*kap(p,0)+pr[1]*kap(p,1)+pr[2]*kap(p,2)
        pp=mp.mpf(p); b*=1+((pp-1)**2*pp**(1.5)-2*pp**4+pp**3+2*pp**3-pp)/(pp**2*(pp**2-1)**2)
        A*=1-2/pp**2
    print(N, -2*A*J*2/3*a, 2*b*4*(-mp.zeta(-0.5))/(mp.zeta(2)**2*3), a*A*mp.zeta(2)**2/b)
