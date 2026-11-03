import random
for _ in range(5):
    p=random.choice([2,3,5,7,11]); r1=random.randint(0,p); r2=random.randint(0,p*p)
    k=lambda j:(1-1/p)*(1+p**(1-j/2)/(p*p-2))
    E=(1-r1/p)*k(0)+(r1/p-r2/p**2)*k(1)+(r2/p**2)*k(2)
    lam=1-p**-2-(1-1/p)*p**-2*(2+(1-p**-0.5)*(r1+r2*p**-1.5))
    print(p,r1,r2,(1-2/p**2)*E,lam)
