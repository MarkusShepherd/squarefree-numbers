import numpy as np, math, sys
from sympy import factorint, primerange
x=int(sys.argv[1]) if len(sys.argv)>1 else 10**7
# squarefree sieve
sf=np.ones(x+1,dtype=bool); sf[0]=False
for d in range(2,int(x**0.5)+1):
    sf[d*d::d*d]=False
P=1.0
for p in primerange(2,10**6): P*=1-2.0/p/p
zeta2=math.pi**2/6
def g(q,l):
    fq=factorint(q)
    v=1/q
    prod=1/zeta2
    for p,e in fq.items():
        prod/= (1-1/p**2)
        pe=p**min(e,2)
        if l%pe==0: prod*=(1-pe/p**2)
    return prod/q
# mu^2 and h up to C
C=2*10**6
sfc=np.ones(C+1,dtype=bool); sfc[0]=False
for d in range(2,int(C**0.5)+1): sfc[d*d::d*d]=False
# h(c)=prod p|c p^2/(p^2-2): compute via log sieve
logh=np.zeros(C+1)
for p in primerange(2,C+1):
    logh[p::p]+=math.log(p*p/(p*p-2.0))
cs=np.arange(C+1)
def B(u): fr=u-np.floor(u); return fr*(1-fr)
def M(q):
    N=x/q
    fq=factorint(q)
    # weight omega and m_c
    w=np.ones(C+1); m=cs.astype(float)**2
    for p,e in fq.items():
        e2=min(e,2)
        idx=cs[p::p]
        w[p::p]*= p**2/p**e2   # c^{-2} m_c factor relative: we use weight=h*c^{-2}*m_c
        m[p::p]/= p**e2
    wt=sfc*np.exp(logh)*w
    # weight function includes c^{-2}m_c = prod p|c p^{-min(2,e)}; for p not|q this is 1
    # above: w initialised 1, for p|q multiply by p^2/p^e2 then divide all by c^2*... fix:
    return wt, m
def Mval(q):
    N=x/q
    fq=factorint(q)
    w=np.ones(C+1); m=cs.astype(float)**2
    for p,e in fq.items():
        e2=min(e,2)
        w[p::p]/= p**e2
        m[p::p]/= p**e2
    w=w*(cs.astype(float)**2)/np.maximum(m,1)  # placeholder
    return None
def Mq(q):
    N=x/q
    fq=factorint(q)
    om=np.ones(C+1); m=cs.astype(float)**2
    for p,e in fq.items():
        e2=min(e,2)
        # for p|c: c^{-2}m_c gets p^{-e2}, m_c gets p^{2-e2}
        om[p::p]*= 1.0   # handled below
        m[p::p]/= p**e2
    om=m/np.maximum(cs.astype(float)**2,1)  # = c^{-2} m_c
    wt=sfc*np.exp(logh)*om
    wt[0]=0
    val=np.sum(wt[1:]*B(N/m[1:]))
    # tail c>C: B~N/m, m~c^2 roughly -> approx sum wt*N/m over c>C ~ alpha*N/C
    tail=0.4*N/C
    return q*P*val, q*P*tail
def exact(q):
    n=np.nonzero(sf)[0]
    cnt=np.bincount(n%q,minlength=q).astype(float)
    gl=np.array([g(q,l) for l in range(q)])
    E=cnt-gl*x
    return np.sum(E*E)
for q in [int(a) for a in sys.argv[2:]]:
    ex=exact(q); mq,tl=Mq(q)
    print(q, factorint(q), "exact",ex,"M",mq,"ratio",ex/mq,"tail~",tl, "sqrt(xq)",math.sqrt(x*q))
