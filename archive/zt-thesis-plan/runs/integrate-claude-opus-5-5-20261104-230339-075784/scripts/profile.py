# Profile x^2 F_f(x/Y) from P6/P7 vs. results.json; plus snapshot's fit model applied to the exact predicted profile.
import numpy as np, json, mpmath as mp
from sympy import factorint
P = 10**7
s = np.ones(P+1, bool); s[:2] = False
for i in range(2, int(P**0.5)+1):
    if s[i]: s[i*i::i] = False
pr = np.nonzero(s)[0].astype(float)
F = {'k^2+1': [1, 0, 1], 'k^3+2': [2, 0, 0, 1], '2k+1': [1, 2]}
def rho(co, m):
    return sum(1 for a in range(m) if sum(c*pow(a, i, m) for i, c in enumerate(co)) % m == 0)
def rho_vec(name):
    p = pr.astype(np.int64); r1 = np.zeros(len(p)); r2 = np.zeros(len(p))
    if name == 'k^2+1':
        m = p % 4 == 1; r1[m] = 2; r2[m] = 2
    elif name == 'k^3+2':
        r1[p % 3 == 2] = 1; r2[p % 3 == 2] = 1
        idx = np.nonzero(p % 3 == 1)[0]
        cub = np.array([pow(int(q)-2, (int(q)-1)//3, int(q)) == 1 for q in p[idx]])
        r1[idx[cub]] = 3; r2[idx[cub]] = 3
    else:
        r1[:] = 1; r2[:] = 1
    for i in range(30):  # exact small primes
        q = int(p[i]); r1[i] = rho(F[name], q); r2[i] = rho(F[name], q*q)
    return r1, r2
c = 1/float(mp.zeta(2)); gE = float(mp.euler); zm = float(mp.zeta(-0.5))
d = json.load(open('results.json'))
p = pr
summary = {}
for name, co in F.items():
    r1, r2 = rho_vec(name)
    alpha = 1 - 2/p**2 + r2/p**4; beta = r1/p**3 - r2/p**4; delta = 1/p**2 - r1/p**3
    # A = prod alpha_p, with exact factor prod(1-p^-2)^2 = c^2 pulled out (tail O(p^-4))
    logA = 2*np.log(c) + np.sum(np.log(alpha) - 2*np.log1p(-1/p**2))
    A = np.exp(logA)
    R = c**2*np.exp(np.sum(np.log1p((1-1/p)*(r1+r2)/(p**2-1)**2)))
    L1 = alpha + beta/p + delta/p**2
    B = R*(gE - 1.5 + np.sum(-np.log(p)*(beta/p + 2*delta/p**2)/L1))
    M = (1-1/p)*(alpha + beta*np.sqrt(p) + delta*p)
    K = -(8/3)*zm*np.exp(np.sum(np.log(M)) - 4/(P*np.log(P)))
    def a_(q): return 1 + rho(co, q*q)/(q*q*(q*q-2))
    def b_(q): return 1 + rho(co, q)/(q*(q*q-2))
    def c_(q): return 1 + 1/(q*q-2)
    Wc = {}
    def W(h):
        w = A
        for q, e in factorint(h).items():
            w *= (b_(q) if e == 1 else c_(q))/a_(q)
        return w
    Hmax = 1000
    Wv = np.array([0.0] + [W(h) for h in range(1, Hmax+1)])
    def Ff(H):
        h = np.arange(1, int(np.floor(H))+1)
        Th = np.sum(Wv[h]*(H-h)**2/h)
        return R*np.log(H) + B + c/H - Th/H**2
    # sanity: D_f(0) relation implied numerically? check W average ~ R/h
    rows = d['polynomials'][name]['rows'] + d['polynomials'][name]['diagnostic_rows']
    xmax = max(r['x'] for r in rows)
    print(f"\n{name}: K={K:.7f} R={R:.7f} B={B:.7f} A={A:.7f}")
    print("   x        ratio      N_data      N_pred(profile)  rel.diff")
    big = [r for r in rows if r['x'] == xmax]
    prev = [r for r in rows if r['x'] == xmax//2]
    for rr in sorted(big + prev, key=lambda r: (r['x'], r['ratio_target'])):
        x, Y, V = rr['x'], rr['fy'], float(rr['V_decimal'])
        H = x/Y
        Nd = V/(x**0.5*Y**1.5); Np = Ff(H)*H**1.5
        print(f"{x:>10} {Y/x:9.6f}  {Nd:.7f}   {Np:.7f}      {Nd/Np-1:+.5%}")
    # snapshot fit model N(r)=C+a sqrt r + b r on the 8 largest-x rows: data vs exact predicted profile
    pts = [r for r in d['polynomials'][name]['rows'] if r['x'] == xmax]
    rr_ = np.array([r['fy']/r['x'] for r in pts])
    Nd = np.array([float(r['V_decimal'])/(r['x']**0.5*r['fy']**1.5) for r in pts])
    Np = np.array([Ff(r['x']/r['fy'])*(r['x']/r['fy'])**1.5 for r in pts])
    X = np.vstack([np.ones_like(rr_), np.sqrt(rr_), rr_]).T
    Cd = np.linalg.lstsq(X, Nd, rcond=None)[0][0]; Cp = np.linalg.lstsq(X, Np, rcond=None)[0][0]
    # dense-grid profile limit check
    Hs = np.array([200., 400., 700., 1000.])
    lim = [Ff(H)*H**1.5 for H in Hs]
    print(f"   fit C+a√r+br: data -> {Cd:.6f}, predicted profile -> {Cp:.6f}; profile at H=200,400,700,1000: "
          + ", ".join(f"{v:.6f}" for v in lim))
    summary[name] = dict(K=K, R=R, B=B, fit_data=Cd, fit_pred=Cp)
json.dump(summary, open('scripts/profile_summary.json', 'w'), indent=1)
