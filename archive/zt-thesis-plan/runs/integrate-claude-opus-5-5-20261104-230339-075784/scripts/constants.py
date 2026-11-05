# Independent evaluation of R_f, B_f, K_f (P5/P6 definitions) and the profile x^2 F_f(x/Y) (P6/P7).
import numpy as np, json, sys, mpmath as mp
from sympy import primerange
P = int(sys.argv[1]) if len(sys.argv) > 1 else 10**7

def sieve(n):
    s = np.ones(n+1, bool); s[:2] = False
    for i in range(2, int(n**0.5)+1):
        if s[i]: s[i*i::i] = False
    return np.nonzero(s)[0]
pr = sieve(P)

def rho_brute(coeffs, m):
    a = np.arange(m, dtype=object)
    v = sum(c * a**i for i, c in enumerate(coeffs))
    return int(sum(1 for t in v if t % m == 0))

def rho_arrays(name):
    p = pr.astype(np.int64)
    r1 = np.zeros(len(p)); r2 = np.zeros(len(p))
    if name == 'k^2+1':
        r1[p % 4 == 1] = 2; r2[p % 4 == 1] = 2
        r1[p == 2] = 1; r2[p == 2] = 0
        coeffs = [1, 0, 1]
    elif name == 'k^3+2':
        one = p % 3 == 1
        r1[p % 3 == 2] = 1; r2[p % 3 == 2] = 1
        pp = p[one]
        cub = np.array([pow(int(q) - 2, (int(q) - 1)//3, int(q)) == 1 for q in pp])
        r1[np.nonzero(one)[0][cub]] = 3; r2[np.nonzero(one)[0][cub]] = 3
        r1[p == 2] = 1; r2[p == 2] = 0
        r1[p == 3] = 1; r2[p == 3] = 0
        coeffs = [2, 0, 0, 1]
    elif name == '2k+1':
        r1[:] = 1; r2[:] = 1; r1[p == 2] = 0; r2[p == 2] = 0
        coeffs = [1, 2]
    # brute-force check for small primes (including those dividing disc)
    for i, q in enumerate(pr[:40]):
        q = int(q)
        assert rho_brute(coeffs, q) == r1[i], (name, q)
        assert rho_brute(coeffs, q*q) == r2[i], (name, q)
    return p.astype(float), r1, r2

zeta2 = float(mp.zeta(2)); c = 1/zeta2
zm = float(mp.zeta(-0.5)); gE = float(mp.euler)
out = {}
for name in ['k^2+1', 'k^3+2', '2k+1']:
    p, r1, r2 = rho_arrays(name)
    q = 1 - 2/p**2
    alpha = 1 - 2/p**2 + r2/p**4
    beta = r1/p**3 - r2/p**4
    delta = 1/p**2 - r1/p**3
    # H_f(-1/2)
    M = (1 - 1/p) * (alpha + beta*np.sqrt(p) + delta*p)
    logH = np.sum(np.log(M))
    # tail: factor ~ 1-(3+rho)/p^2, mean rho = number of irreducible factors = 1
    tailH = -4/(P*np.log(P))
    Hm = np.exp(logH + tailH)
    K = -(8/3)*zm*Hm
    # R_f = P_f(1), alternative product from P5
    L1 = alpha + beta/p + delta/p**2
    R = np.exp(np.sum(np.log(L1)) - 2/(P*np.log(P)))
    R_alt = zeta2**-2 * np.exp(np.sum(np.log1p((1-1/p)*(r1+r2)/(p**2-1)**2)))
    dlog = np.sum(-np.log(p)*(beta/p + 2*delta/p**2)/L1)
    B = (gE - 1.5)*R + R*dlog
    out[name] = dict(K=K, H_m12=Hm, R=R, R_alt=R_alt, B=B,
                     alpha_prod=np.exp(np.sum(np.log(alpha))), pr=(p, r1, r2))
    print(f"{name}: K_f={K:.7f}  H_f(-1/2)={Hm:.7f}  R_f={R:.7f} (alt {R_alt:.7f})  B_f={B:.7f}")
import pickle
pickle.dump({k: {kk: vv for kk, vv in v.items() if kk != 'pr'} for k, v in out.items()},
            open('scripts/constants.pkl', 'wb'))
