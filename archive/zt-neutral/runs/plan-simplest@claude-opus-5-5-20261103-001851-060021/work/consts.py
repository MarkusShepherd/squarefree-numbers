from mpmath import mp, mpf, quad, sqrt, zeta, pi, inf, floor
from sympy import primerange, factorint
mp.dps=20
B=lambda t: (t-floor(t))*(1-(t-floor(t)))
# I = 1/2 int_0^inf B(t) t^{-3/2} dt
I=mpf(1)/2*(mpf(4)/3 + sum(quad(lambda t: B(t)*t**-1.5,[n,n+1]) for n in range(1,2000)) + 2*mpf(1)/6/sqrt(2000))
print('I',I, ' 2zeta(-1/2)/(s(s-1)) guess', -8*zeta(-0.5)*mpf(1)/2, ' -4zeta(-1/2)=',-4*zeta(-0.5))
P=list(primerange(2,10**6))
A0=mpf(1);d1=mpf(1)
for p in P:
    p=mpf(p);A0*=1-2/p**2; d1*=(1-1/p)*(1+p/(p**2-2))
h0=A0*I*d1
print('A0',A0,'delta1',d1,'h0',h0)
def lam(p,j):
    p=mpf(p)
    if j==0: return mpf(1)
    if j==1: return (p**2-2+sqrt(p))/((p+2)*(p-1))
    return (p+1)/(p+2)
def eta(p,j):
    if j>=3: return 0
    return lam(p,j)-lam(p,j-1)
# full mean
M=mpf(1)
for p in P:
    M*=1+eta(p,1)/p+eta(p,2)/p**2
print('full c = 2/3 h0 M =', 2*h0*M/3, ' Vaughan c2=0.128478675')
