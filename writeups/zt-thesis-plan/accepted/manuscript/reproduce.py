#!/usr/bin/env python3
"""Reproduce every numerical table and plot of the manuscript.

Invoke from the workspace root:

    python3 manuscript/reproduce.py            # full snapshot grid (11-14 min, ~5 GB RAM)
    python3 manuscript/reproduce.py --quick    # x <= 4e6 only, for testing the pipeline

What it does
------------
1. Copies the accepted snapshot's supporting source code
   (source/numerics/snapshot/compute.py and counts.cpp) into a fresh
   temporary build directory outside manuscript/ (or into --build-dir),
   checks their SHA-256 hashes against source/numerics/accepted.json, and
   runs the snapshot pipeline there unchanged: compute.main() compiles
   counts.cpp with clang++, runs the snapshot's validations, recomputes
   V_f(x,y) for every x of the grid and every target ratio, and performs the
   snapshot's empirical fits.  The snapshot code writes its compiled worker,
   per-x caches, results.json and report.md into that build directory only;
   a temporary build directory is deleted at the end.  Nothing under source/
   is written, and inside manuscript/ only generated/ and reproduction.json
   are written.
2. Compares the recomputed rows with the archived results.json (exact integer
   counts, 70-digit V values).
3. Evaluates the theoretical quantities of the manuscript (R_f, B_f,
   H_f(-1/2), K_f, W_f(h), Theta_f(H), F_f(H)) from their Euler products and
   definitions, truncating the products at primes <= PMAX.
4. Writes LaTeX tables, pgfplots figures, plot data and constant macros to
   manuscript/generated/, and a machine-readable summary to
   manuscript/reproduction.json.

No value is copied from proof prose or from the archived results; the archived
results.json is only read for the consistency comparison in step 2.
"""
import argparse
import datetime
import decimal
import hashlib
import importlib.util
import json
import math
import pathlib
import platform
import shutil
import subprocess
import sys
import tempfile
import time

import numpy as np
import mpmath as mp

HERE = pathlib.Path(__file__).resolve().parent          # manuscript/
WORKSPACE = HERE.parent
SNAPSHOT = WORKSPACE / 'source' / 'numerics' / 'snapshot'
ACCEPTED = WORKSPACE / 'source' / 'numerics' / 'accepted.json'
GEN = HERE / 'generated'
BUILD = None   # snapshot build directory, set in main(); never inside manuscript/

FULL_XS = [250000, 500000, 1000000, 2000000, 4000000, 8000000, 16000000,
           32000000, 64000000, 128000000, 256000000]
QUICK_XS = [250000, 500000, 1000000, 2000000, 4000000]
PMAX_DEFAULT = 10**7
PCHECK = [10**5, 10**6]          # extra truncation points shown in the table

# Polynomials.  'snap' is the key used by the snapshot code.
POLYS = [
    dict(key='t2', snap='k^2+1', tex='t^2+1', deg=2, f=lambda k: k * k + 1),
    dict(key='t3', snap='k^3+2', tex='t^3+2', deg=3, f=lambda k: k ** 3 + 2),
    dict(key='lin', snap='2k+1', tex='2t+1', deg=1, f=lambda k: 2 * k + 1),
]
# f(t)=t+1 is used only for the comparison with Vaughan's constant c_2.
CHECK_POLY = dict(key='tp1', tex='t+1', deg=1, f=lambda k: k + 1)

# No mpmath precision is set here: the snapshot's compute.py sets mp.mp.dps = 85
# globally when it is imported (step 1), before any mpmath call below.  The
# precision actually in force is recorded in reproduction.json -> parameters.


# ---------------------------------------------------------------------------
# utilities
# ---------------------------------------------------------------------------
def sha256(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def log(msg):
    print(f'[reproduce {time.strftime("%H:%M:%S")}] {msg}', flush=True)


def fmt(v, digits=6):
    return f'{v:.{digits}f}'


def primes_upto(n):
    s = np.ones(n + 1, dtype=bool)
    s[:2] = False
    for i in range(2, math.isqrt(n) + 1):
        if s[i]:
            s[i * i::i] = False
    return np.nonzero(s)[0]


def rho_brute(fcoef, m):
    """Number of residues a mod m with f(a) = 0 mod m (fcoef: low->high)."""
    a = np.arange(m, dtype=np.int64)
    v = np.zeros(m, dtype=np.int64)
    for c in reversed(fcoef):
        v = (v * a + c) % m
    return int(np.sum(v == 0))


COEFFS = {'t2': [1, 0, 1], 't3': [2, 0, 0, 1], 'lin': [1, 2], 'tp1': [1, 1]}


def rho_tables(key, primes, brute_limit=1000, brute_limit_sq=300):
    """rho(p), rho(p^2) for all primes in `primes`.

    For p <= brute_limit, rho(p) is counted directly, and so is rho(p^2)
    for p <= brute_limit_sq.  For larger p the
    polynomials t^2+1, t^3+2, 2t+1, t+1 have only simple roots mod p
    (p does not divide the discriminant or leading coefficient), so
    rho(p^2) = rho(p) by Hensel's lemma and rho(p) is given by the classical
    rules below; the rules are checked against direct counts for
    p <= brute_limit.
    """
    p = primes.astype(np.int64)
    if key == 't2':
        r1 = np.where(p % 4 == 1, 2, 0)
    elif key == 't3':
        r1 = np.where(p % 3 == 2, 1, 0)
        for i in np.nonzero(p % 3 == 1)[0]:
            q = int(p[i])
            r1[i] = 3 if pow((-2) % q, (q - 1) // 3, q) == 1 else 0
    elif key == 'lin':
        r1 = np.ones_like(p)
    elif key == 'tp1':
        r1 = np.ones_like(p)
    r1 = r1.astype(float)
    r2 = r1.copy()
    coef = COEFFS[key]
    for i in np.nonzero(p <= brute_limit)[0]:
        q = int(p[i])
        b1 = rho_brute(coef, q)
        b2 = rho_brute(coef, q * q) if q <= brute_limit_sq else b1
        if q > 3:
            assert b1 == r1[i] and b2 == r2[i], (key, q, b1, r1[i], b2, r2[i])
        r1[i], r2[i] = b1, b2
    return r1, r2


# ---------------------------------------------------------------------------
# theoretical constants (Section "The Dirichlet series" of the manuscript)
# ---------------------------------------------------------------------------
class Theory:
    def __init__(self, key, primes, r1, r2):
        self.key = key
        p = primes.astype(float)
        self.p, self.r1, self.r2 = p, r1, r2
        self.alpha = 1 - 2 / p**2 + r2 / p**4
        self.beta = r1 / p**3 - r2 / p**4
        self.delta = 1 / p**2 - r1 / p**3
        z2 = float(mp.zeta(2))
        self.c = 1 / z2
        # R_f = zeta(2)^-2 prod (1 + (1-1/p)(rho(p)+rho(p^2))/(p^2-1)^2)
        T = (1 - 1 / p) * (r1 + r2) / (p**2 - 1)**2
        self.R = math.exp(math.fsum(np.log1p(T))) / z2**2
        # P_f'(1)/P_f(1) = sum L_p'(1)/L_p(1)
        L1 = self.alpha + self.beta / p + self.delta / p**2
        dL1 = -np.log(p) * (self.beta / p + 2 * self.delta / p**2)
        self.logderiv = math.fsum(dL1 / L1)
        gam = float(mp.euler)
        self.B = (gam - 1.5) * self.R + self.R * self.logderiv
        # H_f(-1/2) = prod M_p with M_p = (1-1/p)(alpha + beta sqrt p + delta p).
        # Since M_p = 1 - (3+rho(p))/p^2 + O(p^{-5/2}), we evaluate
        # zeta(2)^{-3} prod M_p (1-p^{-2})^{-3}, whose factors are 1 + O(p^{-2})
        # with a smaller constant; the value is the same product.
        M = (1 - 1 / p) * (self.alpha + self.beta * np.sqrt(p) + self.delta * p)
        self.Hhalf = math.exp(math.fsum(np.log(M) - 3 * np.log1p(-1 / p**2))) / z2**3
        self.zeta_mhalf = float(mp.zeta(-0.5))
        self.K = -8.0 / 3.0 * self.zeta_mhalf * self.Hhalf
        # W_f(1) = prod alpha_p = zeta(2)^-2 prod (1 + (rho(p^2)-1)/(p^2-1)^2)
        self.W1 = math.exp(math.fsum(np.log1p((r2 - 1) / (p**2 - 1)**2))) / z2**2
        # local ratios u_p(1), u_p(>=2) for W_f(h) = W_f(1) prod u_p(v_p(h))
        self.u1 = (self.alpha + self.beta) / self.alpha
        self.u2 = (self.alpha + self.beta + self.delta) / self.alpha
        self.index = {int(q): i for i, q in enumerate(primes[:20000])}
        self.pmax = int(primes[-1])
        # truncation bound for K: for p >= 5 with rho(p), rho(p^2) <= 3 one has
        # |M_p - 1| <= 10/p^2, hence |M_p (1-p^{-2})^{-3} - 1| <= 15/p^2, so the
        # omitted product lies within exp(15/N) - 1 (relative) of 1; see the
        # manuscript.  This ignores floating-point rounding.
        self.K_rel_trunc = math.expm1(15.0 / self.pmax)
        self._W = {}

    def W(self, h):
        if h in self._W:
            return self._W[h]
        val, m = self.W1, h
        q = 2
        while q * q <= m:
            if m % q == 0:
                e = 0
                while m % q == 0:
                    m //= q
                    e += 1
                i = self.index[q]
                val *= self.u1[i] if e == 1 else self.u2[i]
            q += 1
        if m > 1:
            i = self.index[m]
            val *= self.u1[i]
        self._W[h] = val
        return val

    def W_array(self, hmax):
        """W_f(h) for 1<=h<=hmax via a smallest-prime-factor sieve."""
        spf = np.zeros(hmax + 1, dtype=np.int64)
        for q in range(2, hmax + 1):
            if spf[q] == 0:
                spf[q::q] = np.where(spf[q::q] == 0, q, spf[q::q])
        W = np.empty(hmax + 1)
        W[0] = np.nan
        W[1] = self.W1
        for h in range(2, hmax + 1):
            q = int(spf[h])
            m, e = h, 0
            while m % q == 0:
                m //= q
                e += 1
            i = self.index[q]
            W[h] = W[m] * (self.u1[i] if e == 1 else self.u2[i])
        return W

    def Theta(self, H):
        n = int(math.floor(H))
        return math.fsum(self.W(h) * (H - h)**2 / h for h in range(1, n + 1))

    def F(self, H):
        return (self.R * math.log(H) + self.B + self.c / H
                - self.Theta(H) / H**2)

    def N_pred(self, H):
        """Predicted normalised value x^2 F(x/Y)/(x^{1/2}Y^{3/2}) at H=x/Y."""
        return self.F(H) * H**1.5


def theory_for(key, primes):
    r1, r2 = rho_tables(key, primes)
    return Theory(key, primes, r1, r2)


# ---------------------------------------------------------------------------
# snapshot pipeline
# ---------------------------------------------------------------------------
def load_snapshot_module():
    BUILD.mkdir(parents=True, exist_ok=True)
    accepted = json.loads(ACCEPTED.read_text())
    for name in ['compute.py', 'counts.cpp']:
        src = SNAPSHOT / name
        digest = sha256(src)
        if digest != accepted['artifacts'][name]:
            raise RuntimeError(f'{name}: hash {digest} differs from accepted.json')
        shutil.copyfile(src, BUILD / name)
    spec = importlib.util.spec_from_file_location('snapshot_compute', BUILD / 'compute.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod.ROOT == BUILD.resolve(), mod.ROOT
    return mod


def run_snapshot(mod, xs, reuse):
    argv = ['compute.py', '--xs', ','.join(map(str, xs))]
    if reuse:
        argv.append('--reuse')
    old = sys.argv
    sys.argv = argv
    t0 = time.monotonic()
    try:
        mod.main()
    finally:
        sys.argv = old
    elapsed = time.monotonic() - t0
    return json.loads((BUILD / 'results.json').read_text()), elapsed


def compare_with_archive(result):
    archived = json.loads((SNAPSHOT / 'results.json').read_text())
    out = {}
    for P in POLYS:
        new = {(r['x'], r['ratio_target']): r for r in result['polynomials'][P['snap']]['rows']
               + result['polynomials'][P['snap']]['diagnostic_rows']}
        old = {(r['x'], r['ratio_target']): r for r in archived['polynomials'][P['snap']]['rows']
               + archived['polynomials'][P['snap']]['diagnostic_rows']}
        common = sorted(set(new) & set(old))
        int_mismatch = sum(1 for k in common
                           if new[k]['sum_Q_squared_weighted'] != old[k]['sum_Q_squared_weighted']
                           or new[k]['y'] != old[k]['y'])
        maxrel = 0.0
        for k in common:
            a = mp.mpf(new[k]['V_decimal'])
            b = mp.mpf(old[k]['V_decimal'])
            maxrel = max(maxrel, float(abs(a - b) / abs(b)))
        out[P['snap']] = dict(rows_compared=len(common), integer_or_y_mismatches=int_mismatch,
                              max_relative_difference_V=maxrel)
    return out


# ---------------------------------------------------------------------------
# output helpers
# ---------------------------------------------------------------------------
def write(path, text, artifacts, what):
    path.write_text(text)
    rel = str(path.relative_to(HERE))
    artifacts.append(dict(path=rel, description=what))


def pct(v):
    return f'${100 * v:+.4f}$'


def round_out(v, places, up):
    """v rounded to `places` decimals towards +inf (up) or -inf, as a signed string.

    Used for bounds quoted in the text, so that 'between a and b' and
    'within b' stay true after rounding."""
    q = decimal.Decimal(repr(v)).quantize(decimal.Decimal(1).scaleb(-places),
                                          rounding=decimal.ROUND_CEILING if up else decimal.ROUND_FLOOR)
    return format(q, '+f')


def ceil_sig(v, sig=2):
    """Positive v rounded up to `sig` significant digits, as an unsigned string."""
    places = sig - 1 - math.floor(math.log10(v))
    return round_out(v, places, True).lstrip('+')


def grouped(n):
    """Integer with LaTeX thousands separators, e.g. 127{,}999{,}999."""
    return f'{n:,}'.replace(',', '{,}')


def ratio_list(qs):
    """Human-readable list of ratios for the text, e.g. '0.005' or '0.005 and 0.02'."""
    s = [f'{q:g}' for q in qs]
    if not s:
        return 'none'
    return s[0] if len(s) == 1 else ', '.join(s[:-1]) + ' and ' + s[-1]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--quick', action='store_true', help='use x <= 4e6 only (pipeline test)')
    ap.add_argument('--build-dir', type=pathlib.Path, default=None,
                    help='persistent snapshot build directory outside manuscript/ '
                         '(default: a temporary directory that is deleted afterwards)')
    ap.add_argument('--reuse', action='store_true', help='reuse per-x caches in --build-dir')
    ap.add_argument('--pmax', type=int, default=PMAX_DEFAULT, help='prime cutoff for Euler products')
    args = ap.parse_args()
    global BUILD
    if args.build_dir is None:
        if args.reuse:
            ap.error('--reuse requires --build-dir')
        tmp = tempfile.TemporaryDirectory(prefix='sqf-reproduce-')
        BUILD = pathlib.Path(tmp.name).resolve() / 'snapshot'
    else:
        tmp = None
        BUILD = args.build_dir.resolve()
    if BUILD == HERE or HERE in BUILD.parents:
        if tmp is not None:
            tmp.cleanup()
        ap.error('the snapshot build directory must lie outside manuscript/ '
                 '(use --build-dir or change $TMPDIR)')
    try:
        run(args)
    finally:
        if tmp is not None:
            tmp.cleanup()


def run(args):
    started = time.monotonic()
    xs = QUICK_XS if args.quick else FULL_XS
    GEN.mkdir(parents=True, exist_ok=True)
    artifacts = []
    log(f'snapshot build directory: {BUILD}')

    # ---- 1. snapshot pipeline ------------------------------------------------
    log(f'running the snapshot pipeline for x in {xs}')
    mod = load_snapshot_module()
    result, snap_seconds = run_snapshot(mod, xs, args.reuse)
    precision = dict(
        snapshot_V=('decimal arithmetic with decimal.getcontext().prec = '
                    f'{decimal.getcontext().prec} (set by the snapshot compute.py); the integer counts are exact'),
        mpmath_dps_in_force=mp.mp.dps,
        mpmath_dps_note=('set globally by the snapshot compute.py when it is imported; reproduce.py sets no '
                         'precision of its own. Used for the comparison of V with the archive and for '
                         'the values of zeta(2), zeta(3), zeta(-1/2) and Euler gamma, which are then '
                         'rounded to double precision'),
        theory_constants=('IEEE double precision (numpy float64, math.fsum) for R_f, B_f, H_f(-1/2), K_f, '
                          'W_f, Theta_f, F_f and Vaughan c_2; rounding is not certified'),
    )
    consistency = compare_with_archive(result)
    log(f'snapshot pipeline finished in {snap_seconds:.1f}s; archive comparison {consistency}')

    # ---- 2. theory -------------------------------------------------------------
    log(f'evaluating Euler products up to {args.pmax}')
    primes = primes_upto(args.pmax)
    theory = {P['key']: theory_for(P['key'], primes) for P in POLYS}
    theory['tp1'] = theory_for('tp1', primes)
    trunc = {}
    for N in PCHECK:
        pr = primes[primes <= N]
        trunc[N] = {k: theory_for(k, pr) for k in ['t2', 't3', 'lin']}

    # Vaughan's constant c_2 (Proc. LMS 2005, (1.14)-(1.15) with k=2)
    pf = primes.astype(float)
    C1 = math.exp(math.fsum(np.log1p(((pf - 1)**2 * pf**1.5 - 2 * pf**4 + pf**3 + 2 * pf**3 - pf)
                                       / (pf**2 * (pf**2 - 1)**2))))
    c2_vaughan = 2 * C1 * 4 * (-float(mp.zeta(-0.5))) / (float(mp.zeta(2))**2 * 3 * 1)

    # Consistency check of D_f(s) = zeta(s) P_f(s) at s = 3 (P5).
    dcheck = {}
    for P in POLYS:
        th = theory[P['key']]
        hmax = 200000
        W = th.W_array(hmax)
        h = np.arange(1, hmax + 1, dtype=float)
        partial = math.fsum(W[1:] / h**3)
        tail = 1.0 / (2 * hmax**2)            # 0 < W <= 1
        L3 = th.alpha + th.beta / th.p**3 + th.delta / th.p**6
        # P_f(3) = zeta(2)^{-2} prod L_p(3) (1-p^{-2})^{-2}; factors 1 + O(p^{-4})
        P3 = math.exp(math.fsum(np.log(L3) - 2 * np.log1p(-1 / th.p**2))) / float(mp.zeta(2))**2
        dcheck[P['key']] = dict(series_partial=partial, series_tail_bound=tail,
                                zeta3_P3=float(mp.zeta(3)) * P3)

    # Expansion of Theta_f (P6): (Theta - R H^2 log H - B H^2 - cH)/H^{1/2} -> -K_f
    Hs = [10**2, 10**3, 10**4, 10**5]
    theta_rows = {}
    for P in POLYS:
        th = theory[P['key']]
        W = th.W_array(max(Hs))
        rows = []
        for H in Hs:
            hh = np.arange(1, H + 1, dtype=float)
            Th = math.fsum(W[1:H + 1] * (H - hh)**2 / hh)
            rem = Th - (th.R * H * H * math.log(H) + th.B * H * H + th.c * H)
            rows.append((H, rem / math.sqrt(H)))
        theta_rows[P['key']] = rows

    # ---- 3. comparison of data with the profile -------------------------------
    xs_done = sorted({r['x'] for r in result['polynomials'][POLYS[0]['snap']]['rows']})
    xmax = xs_done[-1]
    profile = {}
    for P in POLYS:
        th = theory[P['key']]
        pdat = result['polynomials'][P['snap']]
        allrows = pdat['rows'] + pdat['diagnostic_rows']
        rows = []
        for r in sorted(allrows, key=lambda r: (r['x'], r['ratio_target'])):
            H = r['x'] / r['fy']
            npred = th.N_pred(H)
            rows.append(dict(x=r['x'], ratio_target=r['ratio_target'], y=r['y'], fy=r['fy'],
                             ratio_actual=r['ratio_actual'], H=H, N_data=r['normalised'],
                             N_pred=npred, rel_diff=r['normalised'] / npred - 1))
        profile[P['key']] = rows

    # Extrapolation: the snapshot's own fit, applied to the data and to the
    # exact predicted profile at the same actual ratios.
    extrap = {}
    for P in POLYS:
        pdat = result['polynomials'][P['snap']]
        ce = pdat['constant_extrapolated']
        cutoff_ratio = ce['ratio_cutoff']
        passing_idx = mod.RATIOS.index(cutoff_ratio) if cutoff_ratio is not None else None
        pseudo = []
        for r in pdat['rows'] + pdat['diagnostic_rows']:
            q = dict(r)
            q['normalised'] = theory[P['key']].N_pred(r['x'] / r['fy'])
            pseudo.append(q)
        pred_fit = None
        if passing_idx is not None:
            pe = mod.extrapolate(pseudo, xs_done, list(range(passing_idx, len(mod.RATIOS))))
            if pe['value'] is not None:
                pred_fit = dict(value=pe['value'], coefficients=pe['primary_fit']['coefficients'])
        extrap[P['key']] = dict(
            data_value=ce['value'], data_uncertainty=ce['uncertainty'], ratio_cutoff=cutoff_ratio,
            data_coefficients=ce['primary_fit']['coefficients'] if ce['value'] is not None else None,
            predicted_profile_fit=pred_fit, K=theory[P['key']].K)
        if ce['value'] is not None and pred_fit is not None:
            # C_data - K_f = (C_data - C_prof) + (C_prof - K_f): the first part is the finite-x
            # difference between data and profile as seen by the fit, the second the bias of the
            # fitting model applied to the exact profile.
            extrap[P['key']]['decomposition'] = dict(
                data_minus_profile_fit=ce['value'] - pred_fit['value'],
                profile_fit_minus_K=pred_fit['value'] - theory[P['key']].K)

    # ---- 4. write generated files -----------------------------------------
    T = theory
    # constants macros
    names = {'t2': 'Two', 't3': 'Three', 'lin': 'Lin', 'tp1': 'Vau'}
    mac = ['% generated by reproduce.py -- do not edit']
    for k, nm in names.items():
        mac.append(f'\\newcommand{{\\K{nm}}}{{{T[k].K:.6f}}}')
        mac.append(f'\\newcommand{{\\R{nm}}}{{{T[k].R:.6f}}}')
    mac.append(f'\\newcommand{{\\cVaughan}}{{{c2_vaughan:.6f}}}')
    mac.append(f'\\newcommand{{\\Pmax}}{{10^{{{round(math.log10(args.pmax))}}}}}')
    mac.append(f'\\newcommand{{\\xmaxdata}}{{{xmax:,}}}'.replace(',', '{,}'))
    mant, expo = f'{T["t2"].K_rel_trunc:.1e}'.split('e')
    mac.append(f'\\newcommand{{\\Ktrunc}}{{{mant}\\cdot10^{{{int(expo)}}}}}')
    for k, nm in names.items():
        if k in extrap:
            e = extrap[k]
            if e['data_value'] is not None and e['predicted_profile_fit'] is not None:
                mac.append(f'\\newcommand{{\\Cfit{nm}}}{{{e["data_value"]:.6f}}}')
                mac.append(f'\\newcommand{{\\Cunc{nm}}}{{{e["data_uncertainty"]:.6f}}}')
                mac.append(f'\\newcommand{{\\Cpred{nm}}}{{{e["predicted_profile_fit"]["value"]:.6f}}}')
                mac.append(f'\\newcommand{{\\Kgap{nm}}}{{{100 * (e["K"] / e["data_value"] - 1):+.2f}}}')
                # decomposition C_fit(data) - K_f = [C_fit(data) - C_fit(profile)] + [C_fit(profile) - K_f]
                mac.append(f'\\newcommand{{\\Cdiff{nm}}}{{{e["data_value"] - e["predicted_profile_fit"]["value"]:+.6f}}}')
                mac.append(f'\\newcommand{{\\Cbias{nm}}}{{{e["predicted_profile_fit"]["value"] - e["K"]:+.6f}}}')
    trends = {}
    for k, nm in names.items():
        if k in profile:
            big = [r for r in profile[k] if r['x'] == xmax]
            # bounds quoted in the text are rounded outwards (the tables round to nearest)
            mac.append(f'\\newcommand{{\\Devmin{nm}}}{{{round_out(100 * min(r["rel_diff"] for r in big), 4, False)}}}')
            mac.append(f'\\newcommand{{\\Devmax{nm}}}{{{round_out(100 * max(r["rel_diff"] for r in big), 4, True)}}}')
            mac.append(f'\\newcommand{{\\Devabs{nm}}}{{{ceil_sig(100 * max(abs(r["rel_diff"]) for r in big))}}}')
            mac.append(f'\\newcommand{{\\Ymin{nm}}}{{{grouped(min(r["y"] for r in big))}}}')
            mac.append(f'\\newcommand{{\\Ymax{nm}}}{{{grouped(max(r["y"] for r in big))}}}')
            # trends of the deviation in x, quoted in the text of Chapter 10
            if len(xs_done) >= 2:
                xprev, xfirst = xs_done[-2], xs_done[0]
                dev = {(r['x'], r['ratio_target']): r['rel_diff'] for r in profile[k]}
                qs_last = sorted(q for (x, q) in dev if x == xmax)
                qs_both = [q for q in qs_last if (xprev, q) in dev]
                decreased = [q for q in qs_both if abs(dev[(xmax, q)]) < abs(dev[(xprev, q)])]
                not_decreased = [q for q in qs_both if q not in decreased]
                sign_change = [q for q in qs_both if dev[(xmax, q)] * dev[(xprev, q)] < 0]
                factors = [abs(dev[(xfirst, q)]) / abs(dev[(xmax, q)]) for q in mod.RATIOS
                           if (xfirst, q) in dev and dev[(xmax, q)] != 0]
                small = max(abs(dev[(xfirst, q)]) for q in mod.RATIOS if (xfirst, q) in dev)
                trends[k] = dict(x_previous=xprev, x_largest=xmax, x_smallest=xfirst,
                                 ratios_compared=qs_both, abs_deviation_decreased=decreased,
                                 abs_deviation_not_decreased=not_decreased, sign_changed=sign_change,
                                 min_decrease_factor_target_ratios_smallest_to_largest_x=min(factors),
                                 max_abs_deviation_at_smallest_x_percent=100 * small)
                mac.append(f'\\newcommand{{\\Ndec{nm}}}{{{len(decreased)}}}')
                mac.append(f'\\newcommand{{\\Ncmp{nm}}}{{{len(qs_both)}}}')
                mac.append(f'\\newcommand{{\\Nondec{nm}}}{{{ratio_list(not_decreased)}}}')
                mac.append(f'\\newcommand{{\\Signch{nm}}}{{{ratio_list(sign_change)}}}')
                mac.append(f'\\newcommand{{\\Decfac{nm}}}{{{math.floor(min(factors))}}}')
                mac.append(f'\\newcommand{{\\Devsmall{nm}}}{{{100 * small:.1f}}}')
    # size of the proved additive error relative to the main term at r=1, x=xmax: x^{-eta_d}
    for P in POLYS:
        eta = min(0.2, 1 / (4 * P['deg'] - 1))
        mac.append(f'\\newcommand{{\\Errrel{names[P["key"]]}}}{{{xmax ** (-eta):.2f}}}')
    write(GEN / 'constants.tex', '\n'.join(mac) + '\n', artifacts,
          'LaTeX macros for constants quoted in the text (K_f, R_f, fits, deviations).')

    # Table: constants
    lines = [r'\begin{tabular}{@{}lrrrr@{}}', r'\toprule',
             r'$f$ & $R_f$ & $B_f$ & $H_f(-\tfrac12)$ & $K_f$ \\', r'\midrule']
    for k in ['t2', 't3', 'lin', 'tp1']:
        th = T[k]
        tex = {'t2': 't^2+1', 't3': 't^3+2', 'lin': '2t+1', 'tp1': 't+1'}[k]
        lines.append(f'${tex}$ & {th.R:.9f} & ${th.B:.9f}$ & {th.Hhalf:.9f} & {th.K:.9f} \\\\')
    lines += [r'\bottomrule', r'\end{tabular}']
    write(GEN / 'tab_constants.tex', '\n'.join(lines) + '\n', artifacts,
          'Table of R_f, B_f, H_f(-1/2), K_f from Euler products over p <= PMAX.')

    lines = [r'\begin{tabular}{@{}rrrr@{}}', r'\toprule',
             r'prime cutoff & $K_{t^2+1}$ & $K_{t^3+2}$ & $K_{2t+1}$ \\', r'\midrule']
    for N in PCHECK:
        lines.append(f'$10^{{{round(math.log10(N))}}}$ & ' + ' & '.join(f'{trunc[N][k].K:.10f}' for k in ['t2', 't3', 'lin']) + r' \\')
    lines.append(f'$10^{{{round(math.log10(args.pmax))}}}$ & ' + ' & '.join(f'{T[k].K:.10f}' for k in ['t2', 't3', 'lin']) + r' \\')
    lines += [r'\bottomrule', r'\end{tabular}']
    write(GEN / 'tab_truncation.tex', '\n'.join(lines) + '\n', artifacts,
          'Table of K_f computed with Euler products truncated at 1e5, 1e6 and PMAX.')

    # Table: Theta expansion
    lines = [r'\begin{tabular}{@{}rrrr@{}}', r'\toprule',
             r'$H$ & $f=t^2+1$ & $f=t^3+2$ & $f=2t+1$ \\', r'\midrule']
    for i, H in enumerate(Hs):
        lines.append(f'$10^{{{round(math.log10(H))}}}$ & ' + ' & '.join(f'${theta_rows[k][i][1]:.6f}$' for k in ['t2', 't3', 'lin']) + r' \\')
    lines.append(r'\midrule')
    lines.append(r'$-K_f$ & ' + ' & '.join(f'${-T[k].K:.6f}$' for k in ['t2', 't3', 'lin']) + r' \\')
    lines += [r'\bottomrule', r'\end{tabular}']
    write(GEN / 'tab_theta.tex', '\n'.join(lines) + '\n', artifacts,
          'Table of (Theta_f(H) - R_f H^2 log H - B_f H^2 - cH)/H^{1/2} against -K_f.')

    # Table: profile comparison at largest x
    lines = [r'\begin{tabular}{@{}lrrrrrr@{}}', r'\toprule',
             r'$f$ & $r$ & $y$ & $f(y)/x$ & $N_{\mathrm{data}}$ & $N_{\mathrm{pred}}$ & $N_{\mathrm{data}}/N_{\mathrm{pred}}-1$ (\%) \\',
             r'\midrule']
    for P in POLYS:
        rows = [r for r in profile[P['key']] if r['x'] == xmax]
        for j, r in enumerate(rows):
            lab = f'${P["tex"]}$' if j == 0 else ''
            lines.append(f'{lab} & {r["ratio_target"]:g} & {grouped(r["y"])} & {r["ratio_actual"]:.6f} & '
                         f'{r["N_data"]:.6f} & {r["N_pred"]:.6f} & {pct(r["rel_diff"])} \\\\')
        if P is not POLYS[-1]:
            lines.append(r'\midrule')
    lines += [r'\bottomrule', r'\end{tabular}']
    write(GEN / 'tab_profile.tex', '\n'.join(lines) + '\n', artifacts,
          f'Table comparing normalised V at x={xmax} with the predicted profile F_f(H)H^(3/2), H=x/f(y).')

    # Table: extrapolation
    lines = [r'\begin{tabular}{@{}lrrrrrrr@{}}', r'\toprule',
             r'& \multicolumn{2}{c}{data} & profile & & \multicolumn{2}{c}{decomposition} & relative gap \\',
             r'\cmidrule(lr){2-3}\cmidrule(lr){4-4}\cmidrule(lr){6-7}\cmidrule(l){8-8}',
             r'$f$ & $C_{\mathrm{data}}$ & envelope & $C_{\mathrm{prof}}$ & $K_f$ & '
             r'$C_{\mathrm{data}}-C_{\mathrm{prof}}$ & $C_{\mathrm{prof}}-K_f$ & $K_f/C_{\mathrm{data}}-1$ \\',
             r'\midrule']
    for P in POLYS:
        e = extrap[P['key']]
        if e['data_value'] is None or e['predicted_profile_fit'] is None:
            lines.append(f'${P["tex"]}$ & -- & -- & -- & {e["K"]:.6f} & -- & -- & -- \\\\')
            continue
        cp = e['predicted_profile_fit']['value']
        lines.append(f'${P["tex"]}$ & {e["data_value"]:.6f} & $\\pm${e["data_uncertainty"]:.6f} & '
                     f'{cp:.6f} & {e["K"]:.6f} & ${e["data_value"] - cp:+.6f}$ & ${cp - e["K"]:+.6f}$ & '
                     f'${100 * (e["K"] / e["data_value"] - 1):+.2f}\\%$ \\\\')
    lines += [r'\bottomrule', r'\end{tabular}']
    write(GEN / 'tab_extrapolation.tex', '\n'.join(lines) + '\n', artifacts,
          'Table of the snapshot extrapolation N(r)=C+a sqrt(r)+b r, applied to the data (C_data) and to the '
          'predicted profile at the same ratios (C_prof), versus K_f, with the decomposition '
          'C_data-K_f=(C_data-C_prof)+(C_prof-K_f).')

    # Table: empirical exponents
    lines = [r'\begin{tabular}{@{}lrrrrr@{}}', r'\toprule',
             r'$f$ & fixed-$x$ $\beta$ & fixed-ratio $\alpha+\beta$ & joint $\alpha$ & joint $\beta$ & joint $C$ \\',
             r'\midrule']
    for P in POLYS:
        pdat = result['polynomials'][P['snap']]
        fx, fr, j = pdat['fit_fixed_x'], pdat['fit_fixed_ratio'], pdat['fit_joint']
        lines.append(f'${P["tex"]}$ & {fx["beta"]:.4f} ({fx["beta_se"]:.4f}) & {fr["alpha_plus_beta"]:.4f} ({fr["se"]:.4f}) & '
                     f'{j["alpha"]:.4f} ({j["alpha_se"]:.4f}) & {j["beta"]:.4f} ({j["beta_se"]:.4f}) & {j["C"]:.4f} \\\\')
    lines += [r'\bottomrule', r'\end{tabular}']
    write(GEN / 'tab_fits.tex', '\n'.join(lines) + '\n', artifacts,
          'Table of the snapshot log-log regressions. In parentheses: formal OLS standard errors for the '
          'fixed-x and joint fits; for the fixed-ratio column, the standard error of the mean of the eight '
          'ratio-specific slopes (their sample standard deviation divided by sqrt(8)), not a regression SE.')

    # Tables: all normalised values
    ratios = mod.RATIOS
    for P in POLYS:
        pdat = result['polynomials'][P['snap']]
        lines = [r'\begin{tabular}{@{}r' + 'r' * len(ratios) + '@{}}', r'\toprule',
                 r'$x$ & ' + ' & '.join(f'{r:g}' for r in ratios) + r' \\', r'\midrule']
        for x in xs_done:
            vals = [next(r['normalised'] for r in pdat['rows'] if r['x'] == x and r['ratio_target'] == q) for q in ratios]
            m, e = f'{x:.3e}'.split('e')
            xs_tex = f'${float(m):g}\\cdot10^{{{int(e)}}}$'
            lines.append(xs_tex + ' & ' + ' & '.join(f'{v:.5f}' for v in vals) + r' \\')
        lines += [r'\bottomrule', r'\end{tabular}']
        write(GEN / f'tab_normalised_{P["key"]}.tex', '\n'.join(lines) + '\n', artifacts,
              f'Table of normalised values V/(x^(1/2) f(y)^(3/2)) for f={P["tex"]}, all x and target ratios.')

    # Plot data and figures
    curve_H = np.unique(np.concatenate([np.geomspace(1.0, 1000.0, 600), np.arange(1, 1001, dtype=float)]))
    groups = []
    for P in POLYS:
        th = T[P['key']]
        cpath = GEN / f'curve_{P["key"]}.dat'
        txt = ['r Npred'] + [f'{1 / H:.10g} {th.N_pred(H):.10g}' for H in curve_H[::-1]]
        write(cpath, '\n'.join(txt) + '\n', artifacts,
              f'Plot data: predicted profile F_f(1/r) r^(-3/2) for f={P["tex"]}, 1e-3<=r<=1.')
        dpath = GEN / f'data_{P["key"]}.dat'
        rows = [r for r in profile[P['key']] if r['x'] == xmax]
        txt = ['r Ndata'] + [f'{r["ratio_actual"]:.10g} {r["N_data"]:.10g}' for r in rows]
        write(dpath, '\n'.join(txt) + '\n', artifacts,
              f'Plot data: normalised V at x={xmax}, f={P["tex"]}, against actual ratio.')
        vpath = GEN / f'deviation_{P["key"]}.dat'
        txt = ['x ' + ' '.join(f'r{q:g}' for q in ratios)]
        for x in xs_done:
            vals = [next(100 * r['rel_diff'] for r in profile[P['key']] if r['x'] == x and r['ratio_target'] == q) for q in ratios]
            txt.append(f'{x} ' + ' '.join(f'{v:.8g}' for v in vals))
        write(vpath, '\n'.join(txt) + '\n', artifacts,
              f'Plot data: 100(N_data/N_pred - 1) for f={P["tex"]}, all x and target ratios.')
        groups.append((P, th))

    fig = [r'% generated by reproduce.py -- do not edit',
           r'\begin{tikzpicture}',
           r'\begin{groupplot}[group style={group size=3 by 1, horizontal sep=0.9cm},',
           r'  width=0.345\textwidth, height=0.34\textwidth, xmode=log, xmin=8e-4, xmax=1.2,',
           r'  xlabel={$r=f(y)/x$}, tick label style={font=\scriptsize}, label style={font=\small},',
           r'  title style={font=\small}, ymin=0.125, ymax=0.19]']
    for i, (P, th) in enumerate(groups):
        opts = 'ylabel={$V_f/(x^{1/2}f(y)^{3/2})$}, ' if i == 0 else ''
        fig += [f'\\nextgroupplot[{opts}title={{$f(t)={P["tex"]}$}}]',
                f'\\addplot[blue, thick, no markers] table[x=r, y=Npred] {{generated/curve_{P["key"]}.dat}};',
                f'\\addplot[only marks, mark=o, mark size=1.6pt, red] table[x=r, y=Ndata] {{generated/data_{P["key"]}.dat}};',
                f'\\addplot[densely dashed, black, domain=8e-4:1.2, samples=2] {{{th.K:.8f}}};']
    fig += [r'\end{groupplot}', r'\end{tikzpicture}']
    write(GEN / 'fig_profile.tex', '\n'.join(fig) + '\n', artifacts,
          'Figure (pgfplots): predicted profile, data at the largest x, and the constant K_f.')

    colors = ['black', 'red', 'blue', 'green!50!black', 'orange', 'violet', 'cyan!60!black', 'brown']
    marks = ['o', 'square', 'triangle', 'diamond', '*', 'x', '+', 'pentagon']
    fig = [r'% generated by reproduce.py -- do not edit',
           r'\begin{tikzpicture}',
           r'\begin{groupplot}[group style={group size=3 by 1, horizontal sep=1.1cm},',
           r'  width=0.345\textwidth, height=0.34\textwidth, xmode=log,',
           r'  xlabel={$x$}, tick label style={font=\scriptsize}, label style={font=\small},',
           r'  title style={font=\small}, scaled y ticks=false,',
           r'  yticklabel style={/pgf/number format/fixed, /pgf/number format/precision=4}]']
    for i, (P, th) in enumerate(groups):
        opts = 'ylabel={$100\\,(N_{\\mathrm{data}}/N_{\\mathrm{pred}}-1)$}, ' if i == 0 else ''
        if i == 1:
            opts += 'legend style={font=\\scriptsize, at={(0.5,-0.32)}, anchor=north, legend columns=8}, '
        fig.append(f'\\nextgroupplot[{opts}title={{$f(t)={P["tex"]}$}}]')
        for j, q in enumerate(ratios):
            fig.append(f'\\addplot[{colors[j]}, mark={marks[j]}, mark size=1.2pt] table[x=x, y=r{q:g}] {{generated/deviation_{P["key"]}.dat}};')
            if i == 1:
                fig.append(f'\\addlegendentry{{$r={q:g}$}}')
    fig += [r'\end{groupplot}', r'\end{tikzpicture}']
    write(GEN / 'fig_deviation.tex', '\n'.join(fig) + '\n', artifacts,
          'Figure (pgfplots): relative deviation of the data from the predicted profile as x grows.')

    # ---- 5. reproduction.json --------------------------------------------------
    clang = subprocess.run(['clang++', '--version'], capture_output=True, text=True).stdout.splitlines()[0]
    summary = dict(
        generated_at=datetime.datetime.now().isoformat(timespec='seconds'),
        command='python3 manuscript/reproduce.py' + (' --quick' if args.quick else '')
                + (' --build-dir <dir>' if args.build_dir is not None else '') + (' --reuse' if args.reuse else ''),
        environment=dict(python=sys.version.split()[0], numpy=np.__version__, mpmath=mp.__version__,
                         platform=platform.platform(), compiler=clang),
        snapshot=dict(
            source='source/numerics/snapshot (accepted snapshot, see source/numerics/accepted.json)',
            code_sha256={n: sha256(SNAPSHOT / n) for n in ['compute.py', 'counts.cpp']},
            how=('compute.py and counts.cpp copied unchanged to a build directory outside manuscript/ '
                 '(a temporary directory unless --build-dir is given) and run there via compute.main(); '
                 'counts.cpp compiled locally with clang++ -O3 -std=c++17; the snapshot\'s own outputs '
                 '(results.json, report.md, run_*.json) stay in that directory'),
            x_grid=xs_done, target_ratios=mod.RATIOS, diagnostic_ratio=0.005,
            runtime_seconds=snap_seconds, validation=result['validation'],
            consistency_with_archived_results=consistency,
            archived_grid_is_reproduced=(xs_done == FULL_XS)),
        parameters=dict(prime_cutoff=args.pmax, extra_truncations=PCHECK, theta_H=Hs,
                        precision=precision),
        constants={k: dict(R=T[k].R, B=T[k].B, H_minus_half=T[k].Hhalf, K=T[k].K, W1=T[k].W1,
                           K_relative_truncation_bound=T[k].K_rel_trunc)
                   for k in ['t2', 't3', 'lin', 'tp1']},
        constants_truncated={str(N): {k: trunc[N][k].K for k in trunc[N]} for N in PCHECK},
        vaughan_c2=dict(value=c2_vaughan, K_t_plus_1=T['tp1'].K,
                        note='c_2 from Vaughan (2005), (1.14)-(1.15) with k=2, Euler product truncated at the same cutoff'),
        dirichlet_series_check_s3=dcheck,
        theta_expansion={k: [dict(H=H, value=v) for H, v in theta_rows[k]] for k in theta_rows},
        extrapolation=extrap,
        fits={P['key']: dict(fixed_x=result['polynomials'][P['snap']]['fit_fixed_x'] | {'all_x': None},
                             fixed_ratio={k: v for k, v in result['polynomials'][P['snap']]['fit_fixed_ratio'].items() if k != 'by_ratio'},
                             joint=result['polynomials'][P['snap']]['fit_joint'])
              for P in POLYS},
        profile_comparison=profile,
        deviation_trends=trends,
        uncertainty_note=('Extrapolation uncertainties are the snapshot heuristic sensitivity envelope, not '
                          'confidence intervals. The standard errors of the fixed-x and joint regressions are '
                          'formal OLS values; the fixed-ratio standard error is the standard error of the mean '
                          'of the eight ratio-specific slopes (sample standard deviation divided by sqrt(8)), '
                          'not an OLS regression standard error. None of these is a rigorous error bound. The '
                          'K_f truncation bound is rigorous for the omitted primes but floating-point '
                          'rounding is not certified.'),
        artifacts=[a['path'] for a in artifacts],
        artifact_descriptions={a['path']: a['description'] for a in artifacts},
        total_runtime_seconds=time.monotonic() - started,
    )
    (HERE / 'reproduction.json').write_text(json.dumps(summary, indent=2, default=float) + '\n')
    log(f'wrote {len(artifacts)} artifacts and reproduction.json in {time.monotonic() - started:.1f}s')


if __name__ == '__main__':
    main()
