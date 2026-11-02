import json, math
from sympy import factorint
from mpmath import zeta
d=json.load(open('../results.json'))
eta0=0.2384433666879889749964064
def L0(p): return 1-1/(p*p-1)**2+p**3/(p*p-1)**2
def L1(p): return 1-1/(p*p-1)**2+p**2.5/(p*p-1)**2
def L2(p): return p*p/(p*p-1)
def eta(q):
    v=eta0
    for p,b in factorint(q).items():
        v*= (L1(p) if b==1 else L2(p))/L0(p)
    return v
F={'k^2+1':(lambda k:k*k+1,lambda k:2*k),'k^3+2':(lambda k:k**3+2,lambda k:3*k*k),'2k+1':(lambda k:2*k+1,lambda k:2)}
C={'k^2+1':0.13808263,'k^3+2':0.13560751,'2k+1':0.14261331}
cache={}
for name,(f,fp) in F.items():
    print(name)
    ys=sorted(set(r['y'] for r in d['polynomials'][name]['rows']))
    ymax=max(ys)
    S=0.0; cum={}
    for k in range(1,ymax+1):
        q=f(k); S+=fp(k)*eta(q)*math.sqrt(q); cum[k]=S
    for r in d['polynomials'][name]['rows']:
        x,y,fy,V=r['x'],r['y'],r['fy'],r['V']
        model=math.sqrt(x)*cum[y]
        print(f"x={x:>10} r={fy/x:.3f} V/(x^.5fy^1.5)={V/(x**.5*fy**1.5):.5f} V/sum_eta={V/model:.5f} C_f-pred V/(C x^.5 fy^1.5)={V/(C[name]*x**.5*fy**1.5):.5f}")
