from mpmath import mp, mpf, zeta, pi, sqrt
from sympy import primerange
mp.dps=25
P=3*10**6
def L0(p): return 1-1/(p*p-1)**2+p**3/(p*p-1)**2
def L1(p): return 1-1/(p*p-1)**2+p**mpf(2.5)/(p*p-1)**2
def L2(p): return p*p/(p*p-1)
H=mpf(1); Eall=mpf(1)
def rho_k2p1(p): 
    if p==2: return (1,0)
    r=2 if p%4==1 else 0; return (r,r)
def rho_k3p2(p):
    if p==2: return (1,0)
    if p==3: return (1,0)
    if p%3==2: return (1,1)
    # p%3==1: -2 cube residue?
    r=sum(1 for k in range(p) if (k**3+2)%p==0); return (r,r)
def rho_2kp1(p):
    return (0,0) if p==2 else (1,1)
E={'k^2+1':mpf(1),'k^3+2':mpf(1),'2k+1':mpf(1)}
R={'k^2+1':rho_k2p1,'k^3+2':rho_k3p2,'2k+1':rho_2kp1}
for p in primerange(2,P):
    p=mpf(int(p)); pi_=int(p)
    l0=L0(p); la1=L1(p)/l0; la2=L2(p)/l0
    H*= (1-1/p)*l0
    Eall*= (1-1/p)+(1/p-1/p**2)*la1+la2/p**2
    for name,fn in R.items():
        if name=='k^3+2' and pi_%3==1 and pi_>10**4:
            r1,r2=(1,1)  # average heuristic placeholder (mean rho=1)
        else:
            r1,r2=fn(pi_)
        E[name]*= (1-r1/p)+(r1/p-r2/p**2)*la1+(r2/p**2)*la2
eta0=-4*zeta(-0.5)*(6/pi**2)**2*H
print('H',H,'eta0',eta0)
print('c2 from model',2*eta0*Eall/3,' Vaughan c2 0.1284786750')
for n,e in E.items(): print(n,'C_f=',2*eta0*e/3, 'ratio to c2', e/Eall)
print('mean eta all (3/2 c2)',eta0*Eall)
