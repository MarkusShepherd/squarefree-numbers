import mpmath as mp
from sympy import primerange
mp.mp.dps=20
P=list(primerange(2,300000))
z=-mp.zeta(-0.5)
def lam(p,r1,r2):
    p=mp.mpf(p)
    return 1-1/p**2-(1-1/p)/p**2*(2+(1-p**-0.5)*(r1+r2*p**-1.5))
def rho_lin(p): return (1,1)
def rho_odd(p): return (0,0) if p==2 else (1,1)
def rho_sq1(p):
    if p==2: return (1,0)
    return (2,2) if p%4==1 else (0,0)
def rho_cub(p):
    if p==2: return (1,0)
    if p==3: return (1,0)
    if p%3==2: return (1,1)
    r=3 if pow((-2)%p,(p-1)//3,p)==1 else 0
    return (r,r)
# brute check small p for cubic and sq
def brute(f,m): return sum(1 for a in range(m) if f(a)%m==0)
for p in [2,3,5,7,11,13,31,43]:
    assert rho_cub(p)==(brute(lambda a:a**3+2,p),brute(lambda a:a**3+2,p*p)),p
    assert rho_sq1(p)==(brute(lambda a:a*a+1,p),brute(lambda a:a*a+1,p*p)),p
    assert rho_odd(p)==(brute(lambda a:2*a+1,p),brute(lambda a:2*a+1,p*p)),p
for name,R in [('t',rho_lin),('2k+1',rho_odd),('k^2+1',rho_sq1),('k^3+2',rho_cub)]:
    pr=mp.mpf(1)
    for p in P: pr*=lam(p,*R(p))
    print(name, 8*z/3*pr)
