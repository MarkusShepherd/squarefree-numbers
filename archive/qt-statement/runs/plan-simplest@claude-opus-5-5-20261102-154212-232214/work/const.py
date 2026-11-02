from mpmath import mp, mpf, quad, zeta, inf, nsum, pi
from sympy import primerange
mp.dps=20
def Bint(n):
    return quad(lambda t: t*(1-t)*(n+t)**(-1.5),[0,1])
I = mpf(4)/3 + nsum(lambda n: Bint(int(n)), [1,inf])
print("I",I, " I/(-zeta(-1/2))", I/(-zeta(-0.5)))
PR=list(primerange(2,2*10**6))
P=mpf(1); a1=mpf(1)
for p in PR:
    p=mpf(p); h=p*p/(p*p-2)
    P*=1-2/p**2
    a1*=(1-1/p)*(1+h/p)
print("P",P,"alpha1",a1)
def Ep(p,d1,d2):
    p=mpf(p); h=p*p/(p*p-2)
    L1=(1+h*p**-1.5)/(1+h/p); L2=(1+h/p**2)/(1+h/p)
    return 1-d1+(d1-d2)*L1+d2*L2
def rho(f,m):
    return sum(1 for a in range(m) if f(a)%m==0)
def const(dens):
    prod=mpf(1)
    for p in PR:
        d1,d2=dens(p)
        prod*=Ep(p,d1,d2)
    return P*I/3*a1*prod
print("C_full",const(lambda p:(mpf(1)/p,mpf(1)/p**2)), "Vaughan c2 0.1284786749933")
def dens_poly(f,deg_roots):
    def d(p):
        if p<300:
            r1=rho(f,p); r2=rho(f,p*p)
        else:
            r1=deg_roots(p); r2=r1
        return mpf(r1)/p, mpf(r2)/p**2
    return d
def roots_k2p1(p): return 2 if p%4==1 else 0
def roots_k3p2(p):
    if p%3==2: return 1
    return 3 if pow((-2)%p,(p-1)//3,p)==1 else 0
def roots_lin(p): return 1
for name,f,r in [("k^2+1",lambda t:t*t+1,roots_k2p1),("k^3+2",lambda t:t**3+2,roots_k3p2),("2k+1",lambda t:2*t+1,roots_lin)]:
    print(name, const(dens_poly(f,r)))
