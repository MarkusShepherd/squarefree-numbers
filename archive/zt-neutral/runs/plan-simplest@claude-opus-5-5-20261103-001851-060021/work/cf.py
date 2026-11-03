from mpmath import mp, mpf, sqrt, zeta
from sympy import primerange
mp.dps=20
P=list(primerange(2,3*10**5))
h0=-4*zeta(-0.5)
for p in P: h0*=(1-mpf(1)/p)**2*(1+mpf(2)/p)
def lam(p,j):
    p=mpf(p)
    return mpf(1) if j==0 else ((p**2-2+sqrt(p))/((p+2)*(p-1)) if j==1 else (p+1)/(p+2))
def rho(f,m):
    return sum(1 for a in range(m) if f(a)%m==0)
polys={'k^2+1':(lambda t:t*t+1,2,-4*1),'k^3+2':(lambda t:t**3+2,3,-108),'2k+1':(lambda t:2*t+1,1,2)}
for name,(f,deg,disc) in polys.items():
    prod=mpf(1)
    for p in P:
        if p<200 or disc%p==0:
            r1=rho(f,p); r2=rho(f,p*p)
        else:
            # Hensel: simple roots lift uniquely
            if deg==2: r1=1+ (0 if p==2 else (1 if pow(-1,(p-1)//2,p)==1 else -1)); 
            elif deg==3: r1=sum(1 for a in range(p) if (a**3+2)%p==0) if p<20000 else None
            else: r1=1
            if r1 is None: continue
            r2=r1
        prod*=1+(mpf(r1)/p-mpf(r2)/p**2)*(lam(p,1)-1)+mpf(r2)/p**2*(lam(p,2)-1)
    print(name,'C_f=',2*h0*prod/3)
print('full (f(t)=t) check:', end=' ')
prod=mpf(1)
for p in P: prod*=1+(mpf(1)/p-mpf(1)/p**2)*(lam(p,1)-1)+mpf(1)/p**2*(lam(p,2)-1)
print(2*h0*prod/3)
