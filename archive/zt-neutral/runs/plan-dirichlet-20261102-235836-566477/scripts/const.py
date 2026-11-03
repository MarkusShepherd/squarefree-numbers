import mpmath as mp
from sympy import primerange
mp.mp.dps=30
z=mp.zeta(-0.5)
P=list(primerange(2,2*10**6))
def prod(fn):
    s=mp.mpf(0)
    for p in P: s+=mp.log(fn(mp.mpf(p)))
    return mp.e**s
C1=prod(lambda p: 1+((p-1)**2*p**1.5-2*p**4+p**3+2*p**3-p)/(p**2*(p**2-1)**2))
c2V=8*C1*(-z)/(3*mp.zeta(2)**2)
print('Vaughan c_2',c2V)
c2=prod(lambda p:1-2/p**2)
def M(rho1,rho2):
    def fac(p):
        p=int(p); r1=rho1(p); r2=rho2(p); p=mp.mpf(p)
        lam=(1-r1/p)+p**-0.5*(r1/p-r2/p**2)+(1/p)*r2/p**2
        return (1-1/p)*(1+p/(p**2-2)*lam)
    return prod(fac)
Mk=M(lambda p:1,lambda p:1)
print('model f=k', (mp.mpf(2)/3)*(-4*c2*z)*Mk)
