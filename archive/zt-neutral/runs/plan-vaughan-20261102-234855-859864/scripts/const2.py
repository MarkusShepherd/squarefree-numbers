import mpmath as mp, numpy as np
from sympy import primerange
mp.mp.dps=25
def rho_np(coeffs,m):
    a=np.arange(m,dtype=object) if m>3e9 else np.arange(m,dtype=np.int64)
    v=np.zeros(m,dtype=np.int64)
    for c in coeffs: v=(v*a+c)%m
    return int(np.sum(v==0))
def cf(coeffs,name,P=100000):
    C=mp.mpf(1); R=mp.mpf(1); A=mp.mpf(1)
    for p in primerange(2,P):
        r1=rho_np(coeffs,p)
        r2=rho_np(coeffs,p*p) if p<3000 else r1
        pm=mp.mpf(p)
        C*=1-2/pm**2
        br=pm**2-pm*r1+(pm*r1-r2)*pm**-0.5+r2/pm
        R*=(1-1/pm)*(1+br/(pm*(pm**2-2)))
    R/=2
    c=mp.mpf(16)/3*C*(-mp.zeta(-0.5))*R
    print(name,'c_f=',mp.nstr(c,10),' ratio to Vaughan c_2:',mp.nstr(c/mp.mpf('0.1284787643'),8))
cf([1,0],'k')
cf([1,0,1],'k^2+1')
cf([1,0,0,2],'k^3+2')
cf([2,1],'2k+1')
