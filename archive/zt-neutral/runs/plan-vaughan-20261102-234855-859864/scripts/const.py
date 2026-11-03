import mpmath as mp
from sympy import primerange
mp.mp.dps=30
def rho(f,m):
    return sum(1 for a in range(m) if f(a)%m==0)
def cf(f,P=20000,name=''):
    # c_f = (16/3) C (-zeta(-1/2)) Res, Res = 1/2 prod_p (1-1/p)(1+ p^-1/(p^2-2)[...])
    C=mp.mpf(1); R=mp.mpf(1)
    for p in primerange(2,P):
        p=mp.mpf(p); pi=int(p)
        r1=rho(f,pi) if pi<400 else None
        if pi<400:
            r2=rho(f,pi*pi)
        else:
            r1=rho(f,pi); r2=None
        C*=1-2/p**2
        if r2 is None:
            # Hensel: for p not dividing disc, rho(p^2)=rho(p); assume large p unramified
            r2=r1
        br=p**2-p*r1+(p*r1-r2)*p**-0.5+r2/p
        R*=(1-1/p)*(1+br/(p*(p**2-2)))
    R/=2
    c=mp.mpf(16)/3*C*(-mp.zeta(-0.5))*R
    print(name,'C=',C,'Res=',R,'c_f=',c)
    return c
cf(lambda t:t,P=3000,name='f=k (Vaughan check)')
k=2
# Vaughan c_2
C1=mp.mpf(1)
for p in primerange(2,200000):
    p=mp.mpf(p)
    C1*=1+((p-1)**2*(p**(2-0.5)) -2*p**4+p**3+2*p**3-p)/(p**2*(p**2-1)**2)
c2=2*C1*k**2*(-mp.zeta(1/k-1))/(mp.zeta(k)**2*(2*k-1)*(k-1))
print('Vaughan c_2=',c2,'C1=',C1)
