import mpmath as mp
from sympy import primerange
mp.mp.dps=30
# Phi-hat(1/2) = 4/3 + int_1^inf {t}(1-{t}) t^{-3/2} dt
J=mp.mpf(0)
for n in range(1,200000):
    J+=mp.quad(lambda u: u*(1-u)*(n+u)**(-1.5),[0,1])
    if n>2000: break
# tail via asymptotic: {t}(1-{t}) avg 1/6
tail = mp.mpf(1)/6*2*(2001)**(-0.5)
print("Phihat approx", 4/mp.mpf(3)+J+tail, " -8zeta(-1/2)=", -8*mp.zeta(-0.5))
def rho(f,m):
    return sum(1 for a in range(m) if f(a)%m==0)
def Cf(f,P=20000):
    prod=mp.mpf(1)
    for p in primerange(2,P):
        r1=rho(f,p) if p<3000 else None
        if p>=3000:
            # rho(p^2)=rho(p) for unramified p; use rho(p) via roots
            r1=rho(f,p); r2=r1
        else:
            r2=rho(f,p*p) if p<400 else r1
        p=mp.mpf(p)
        e=1-r1/p+(r1/p-r2/p**2)*p**-0.5+r2/p**3
        prod*=(1-1/p)*(1-2/p**2+e/p)
    return -mp.mpf(8)/3*mp.zeta(-0.5)*prod
import sys
for name,f in [("t",lambda t:t),("k^2+1",lambda t:t*t+1),("k^3+2",lambda t:t**3+2),("2k+1",lambda t:2*t+1)]:
    print(name, Cf(f,4000))
