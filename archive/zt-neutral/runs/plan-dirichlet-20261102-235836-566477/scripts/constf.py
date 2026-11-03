import mpmath as mp
from sympy import primerange
mp.mp.dps=20
z=mp.zeta(-0.5)
P=list(primerange(2,2*10**6))
def rho(f,m):
    return sum(1 for a in range(m) if f(a)%m==0)
def r1_large(name,p):
    if name=='k^2+1': return 2 if p%4==1 else 0
    if name=='k^3+2':
        if p%3==2: return 1
        return 3 if pow((-2)%p,(p-1)//3,p)==1 else 0
    return 1
polys={'k^2+1':lambda t:t*t+1,'k^3+2':lambda t:t**3+2,'2k+1':lambda t:2*t+1,'k':lambda t:t}
c2=mp.mpf(1)
for p in P: c2*=1-mp.mpf(2)/p**2
pref=(mp.mpf(2)/3)*(-4*c2*z)
print('prefactor (2/3)(-4 c2 zeta(-1/2)) =',pref, 'c2=',c2)
for name,f in polys.items():
    tot=0.0
    for p in P:
        if p<60: r1=rho(f,p); r2=rho(f,p*p)
        else: r1=r1_large(name,p); r2=r1
        pp=float(p)
        lam=(1-r1/pp)+pp**-0.5*(r1/pp-r2/pp**2)+(1/pp)*r2/pp**2
        tot+=mp.log((1-1/pp)*(1+pp/(pp**2-2)*lam))
    M=mp.e**tot
    print(name,'kappa_f=',pref*M, 'M=',M)
