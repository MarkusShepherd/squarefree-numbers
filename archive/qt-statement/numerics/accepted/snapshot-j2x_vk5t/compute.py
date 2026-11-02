#!/usr/bin/env python3
"""Reproducible exact-count experiment. No external literature or network used."""
import argparse
import csv
from fractions import Fraction
import json
import math
from pathlib import Path
import subprocess
import time
import numpy as np
import mpmath as mp
from scipy import stats

ROOT = Path(__file__).resolve().parent
NAMES = ['k^2+1', 'k^3+2', '2k+1']
RATIOS = [.01, .02, .05, .1, .2, .4, .7, 1.]
mp.mp.dps = 70
C0 = 6 / mp.pi**2

def factors(n):
    out = []
    p = 2
    while p*p <= n:
        if n % p == 0:
            e = 0
            while n % p == 0:
                n //= p
                e += 1
            out.append((p,e))
        p += 1
    if n > 1:
        out.append((n,1))
    return out

def density_coeff(q,l):
    z = Fraction(1,q)
    for p,e in factors(q):
        if e >= 2 and l % (p*p) == 0:
            return Fraction(0)
        z *= Fraction(p*p,p*p-1)
        if e == 1 and l % p == 0:
            z *= Fraction(p-1,p)
    return z

def mm(z):
    return mp.mpf(z.numerator)/z.denominator

def dd(row,key):
    return mp.mpf(float(row[key+'_hi']))+mp.mpf(float(row[key+'_lo']))

def squarefree(x):
    s = np.ones(x+1,dtype=np.bool_)
    s[0] = False
    for p in range(2, math.isqrt(x)+1):
        # Sieving composite squares also is harmless, and avoids another sieve.
        s[p*p::p*p] = False
    return s

def validate(raw):
    messages = []
    # Exact finite-period densities: sieve 2,3 and every prime dividing q.
    # Period at q <= 50 is small; no limiting approximation enters this test.
    checked = 0
    max_density_error = 0.
    sf = squarefree(1000000)
    ns = np.flatnonzero(sf)
    for q in range(1,51):
        ps = sorted({2,3} | {p for p,e in factors(q)})
        period = math.lcm(q, *[p*p for p in ps])
        arr = np.arange(1,period+1,dtype=np.int64)
        mask = np.ones(period,dtype=np.bool_)
        for p in ps:
            mask &= arr % (p*p) != 0
        counts = np.bincount(arr[mask] % q, minlength=q)
        prod = math.prod([Fraction(p*p-1,p*p) for p in ps])
        for l in range(q):
            assert Fraction(int(counts[l]),period) == prod*density_coeff(q,l)
            checked += 1
        finite = np.bincount(ns % q,minlength=q)/1000000
        infinite = np.array([float(C0*mm(density_coeff(q,l))) for l in range(q)])
        max_density_error = max(max_density_error,float(np.max(np.abs(finite-infinite))))
        assert int(np.bincount(ns % q,minlength=q).sum()) == len(ns)
    messages.append(f'g(q,l)/[6/pi^2] verified with exact Fraction arithmetic against complete finite-period sieves for all q <= 50 ({checked} residue classes); sieved primes are 2,3 and all primes dividing q. The finite-period product is removed exactly.')
    assert max_density_error < 1e-4
    messages.append(f'Actual squarefree densities at x=1000000 checked for every q <= 50; maximum absolute |Q/x-g| = {max_density_error:.12g}. This is a finite-density check, not an exact equality to the limiting density.')
    pilot = squarefree(1000)
    ns = np.flatnonzero(pilot)
    exact = {}
    max_rel = mp.mpf(0)
    # Validate every raw per-modulus density aggregation with independent exact fractions.
    for row in raw:
        q = int(row['q'])
        if q not in exact:
            Q = np.bincount(ns % q,minlength=q)
            assert int(Q.sum()) == len(ns)
            coeff = [density_coeff(q,l) for l in range(q)]
            b = sum((int(Q[l])*coeff[l] for l in range(q)),Fraction())
            d = sum((z*z for z in coeff),Fraction())
            a = sum(int(v)**2 for v in Q)
            exact[q] = a,b,d
        a,b,d = exact[q]
        assert a == int(row['S2'])
        for key,z in [('B',b),('D',d)]:
            rel = abs(dd(row,key)-mm(z))/max(mp.mpf(1),abs(mm(z)))
            max_rel = max(max_rel,rel)
            assert rel < mp.mpf('3e-29'),(q,key,str(rel))
    for t in range(3):
        aa=0; bb=Fraction(); ddd=Fraction()
        for row in raw:
            if int(row['type']) != t:
                continue
            a,b,d=exact[int(row['q'])];w=int(row['weight'])
            aa+=w*a;bb+=w*b;ddd+=w*d
            vexact=mp.mpf(aa)-2000*C0*mm(bb)+1000000*C0*C0*mm(ddd)
            vdd=mp.mpf(row['A_cum'])-2000*C0*dd(row,'B_cum')+1000000*C0*C0*dd(row,'D_cum')
            assert abs(vexact-vdd)/max(1,abs(vexact)) < mp.mpf('1e-23')
    messages.append(f'At x=1000 every selected modulus (union of all three polynomial sequences, including every odd q <= 999) was checked against direct integer Q counts and exact rational density coefficients. Maximum relative/absolute scaled double-double aggregation discrepancy {float(max_rel):.3g}; cumulative V discrepancies < 1e-23 relative.')
    messages.append('C++ checks sum_l Q(x;q,l)=Q(x;1,1) and sum_l Q^2 against direct counts for all q <= 50 at every production x, and for all 2 <= q <= 1000 at x=1000. Integer NTT zero lag equals Q(x;1,1), and every correlation coefficient satisfies 0 <= C(h) <= x-h. The NTT prime exceeds x, so modular coefficients lift uniquely to exact integer counts.')
    return messages

def validate_large(records, xs):
    messages=[]
    # Independent exact squarefree-divisibility counts by a Mobius floor sum.
    # This is used ONLY for validation; production uses integer divisor sums.
    xmax=xs[-1];limit=math.isqrt(xmax)
    mu=np.ones(limit+1,dtype=np.int64);mu[0]=0
    isprime=np.ones(limit+1,dtype=np.bool_);isprime[:2]=False
    for p in range(2,limit+1):
        if isprime[p]:
            mu[p::p]*=-1
            mu[p*p::p*p]=0
            isprime[p*p::p]=False
    aa=np.arange(1,limit+1,dtype=np.int64)**2
    active=mu[1:]!=0;aa=aa[active];mus=mu[1:][active]
    cache={}
    def count(d):
        if d not in cache:
            denominator=(aa//np.gcd(aa,d))*d
            cache[d]=int(np.sum(mus*(xmax//denominator),dtype=np.int64))
        return cache[d]
    maxerr=mp.mpf(0)
    for row in records:
        if int(row['x'])!=xmax:continue
        q=int(row['q']);H=Fraction(1);local=Fraction(1);divs=[(1,1)]
        for p,e in factors(q):
            H*=Fraction(p*p,p*p-1)
            if e==1:
                local*=1-Fraction(2,p*p)+Fraction(1,p**3)
                divs += [(d*p,-s) for d,s in list(divs)]
            else:local*=1-Fraction(1,p*p)
        T=sum((Fraction(s*count(d),d) for d,s in divs),Fraction())
        for key,z in [('B',H*T/q),('D',H*H*local/q)]:
            err=abs(dd(row,key)-mm(z))/max(mp.mpf(1),abs(mm(z)))
            maxerr=max(maxerr,err)
            assert err<mp.mpf('1e-27'),(q,key,str(err))
    messages.append(f'At the largest x={xmax}, all 24 grid-endpoint per-modulus density aggregations were independently checked against exact Fraction arithmetic. Squarefree-divisibility counts were recomputed by an integer Mobius floor sum ({len(cache)} distinct divisors). Maximum scaled discrepancy: {float(maxerr):.4g}.')
    subprocess.run(['c++','-O3','-std=c++17','-ffp-contract=off','-DNTT_MOD=469762049U','-DNTT_ROOT=3','compute_core.cpp','-o','compute_core_check'],cwd=ROOT,check=True)
    subprocess.run([str(ROOT/'compute_core_check'),'1000000',str(ROOT/'validation_other_modulus.csv'),'50'],check=True)
    with open(ROOT/'validation_other_modulus.csv') as f:check=list(csv.DictReader(f))
    ref=[r for r in records if int(r['x'])==1000000]
    if ref:
        assert len(ref)==len(check)
        for a,b in zip(ref,check):
            for key in ['type','x','k','q','S2','A_cum']:assert a[key]==b[key]
        messages.append('At x=1000000 the 24 grid-endpoint exact count sums were reproduced with an independent NTT prime/root (469762049,3), agreeing exactly with the production prime/root (3221225473,5).')
    return messages

def regression(x,y):
    fit=stats.linregress(x,y)
    return {'slope':float(fit.slope),'se':float(fit.stderr),'intercept':float(fit.intercept),
            'r_squared':float(fit.rvalue**2),'n':len(x)}

def extrapolate(normalised,xs):
    recent=[r for r in normalised if r['x']==xs[-1]]
    previous={r['ratio']:r for r in normalised if r['x']==xs[-2]}
    stability=[]
    for r in recent:
        p=previous[r['ratio']]
        change=abs(r['V_over_x12_fy32']/p['V_over_x12_fy32']-1)
        stability.append({'ratio':r['ratio'],'relative_change_two_largest_x':change,'passes_1_percent':change<.01})
    # A cutoff requires every grid ratio at or above it to pass.
    valid=[i for i in range(len(recent)) if all(s['passes_1_percent'] for s in stability[i:])]
    if not valid:
        return {'value':None,'uncertainty':None,'method':'No ratio cutoff passes the 1% stability criterion at every ratio above it. No extrapolated constant reported.','ratio_cutoff':None,'cutoff_sensitivity':'Not applicable.','stability':stability}
    cut=valid[0]
    def fit(c,degree=1,xval=None):
        dat=[r for r in normalised if r['x']==(xs[-1] if xval is None else xval)][c:]
        # The regressor sqrt(r) accommodates a first relative correction of size sqrt(Y/x).
        u=np.sqrt([r['actual_ratio'] for r in dat]);z=np.array([r['V_over_x12_fy32'] for r in dat])
        if len(z)<=degree+1:
            return None
        X=np.column_stack([u**j for j in range(degree+1)])
        coef,_,_,_=np.linalg.lstsq(X,z,rcond=None)
        resid=z-X@coef;df=len(z)-degree-1
        cov=np.linalg.inv(X.T@X)*(resid@resid)/df
        return {'value':float(coef[0]),'se':float(np.sqrt(cov[0,0])),
                'coefficients':coef.tolist(),'residual_rms':float(np.sqrt(np.mean(resid**2))),
                'n':len(z),'ratio_cutoff':dat[0]['ratio'],'degree_in_sqrt_ratio':degree,
                'includes_unstable_rows':c<cut}
    central=fit(cut)
    if central is None:
        return {'value':None,'uncertainty':None,'method':'Stable cutoff found, but too few stable rows remain to fit a two-parameter extrapolation with a residual standard error.','ratio_cutoff':recent[cut]['ratio'],'cutoff_sensitivity':'Insufficient rows.','stability':stability}
    sensitivity=[]
    for ci in [cut-1,cut,cut+1]:
        if 0<=ci<len(recent):
            f=fit(ci)
            if f:sensitivity.append(f)
    alternate=fit(cut,2)
    dat=[r for r in normalised if r['x']==xs[-1]][cut:]
    rfit=regression([r['actual_ratio'] for r in dat],[r['V_over_x12_fy32'] for r in dat])
    linear_ratio={'value':rfit['intercept'],'se':float(stats.linregress([r['actual_ratio'] for r in dat],[r['V_over_x12_fy32'] for r in dat]).intercept_stderr),'slope':rfit['slope'],'r_squared':rfit['r_squared']}

    prevfit=fit(cut,1,xs[-2])
    spread=max(abs(f['value']-central['value']) for f in sensitivity)
    model_shift=max(abs(linear_ratio['value']-central['value']),abs(alternate['value']-central['value']) if alternate else 0.)
    x_shift=abs(prevfit['value']-central['value']) if prevfit else 0.
    uncertainty=max(2*central['se'],spread,model_shift,x_shift)
    return {'value':central['value'],'uncertainty':uncertainty,
            'method':'Unweighted OLS z(r)=C+a*sqrt(r), using actual r=f(y)/x at the largest x and only target ratios at or above the stable cutoff. Uncertainty is max(2*intercept_SE, adjacent-cutoff shift, linear-in-r / quadratic-in-sqrt(r) model shifts, change on fitting the second-largest x); it is a sensitivity envelope, not a confidence interval. Functional form is empirical and not identified by these finite ratios.',
            'ratio_cutoff':recent[cut]['ratio'],'cutoff_sensitivity':sensitivity,
            'cutoff_spread':spread,'intercept_se':central['se'],'central_fit':central,
            'alternative_quadratic_in_sqrt_ratio':alternate,'alternative_linear_ratio':linear_ratio,'second_largest_x_fit':prevfit,
            'cutoff_sensitivity_note':'The lower adjacent cutoff is unavailable when the chosen cutoff is 0.01, the bottom of the requested grid.' if cut==0 else 'The lower adjacent fit includes an unstable row intentionally as a sensitivity diagnostic.',
            'model_shift':model_shift,'x_shift':x_shift,'stability':stability}

def analyse(records,xs):
    output={}
    for t,name in enumerate(NAMES):
        rows=[];norm=[]
        for x in xs:
            selected=[r for r in records if int(r['type'])==t and int(r['x'])==x]
            selected.sort(key=lambda r:int(r['q']))
            for target,row in zip(RATIOS,selected):
                q=int(row['q']); y=int(row['k'])
                fpoly=[lambda k:k*k+1,lambda k:k*k*k+2,lambda k:2*k+1][t]
                assert q==fpoly(y)
                assert q<=x*round(target*100)//100<fpoly(y+1)
                V=mp.mpf(row['A_cum'])-2*x*C0*dd(row,'B_cum')+mp.mpf(x)**2*C0**2*dd(row,'D_cum')
                assert V>0
                rows.append({'x':x,'y':y,'fy':q,'V':float(V),'V_decimal':mp.nstr(V,20),'target_ratio':target,
                             'count_square_sum_weighted_exact':int(row['A_cum'])})
                norm.append({'x':x,'ratio':target,'actual_ratio':q/x,'V_over_x12_fy32':float(V/(mp.sqrt(x)*mp.mpf(q)**mp.mpf('1.5')))})
            assert len(selected)==8,(name,x,len(selected))
        fixed=[]
        for x in xs:
            rr=[r for r in rows if r['x']==x];f=regression(np.log([r['fy'] for r in rr]),np.log([r['V'] for r in rr]))
            fixed.append({'x':x,'beta':f['slope'],'beta_se':f['se'],'prefactor_C_times_x_alpha':math.exp(f['intercept']),'r_squared':f['r_squared']})
        slopes=[]
        for ratio in RATIOS:
            rr=[r for r in rows if r['target_ratio']==ratio]
            f=regression(np.log([r['x'] for r in rr]),np.log([r['V'] for r in rr]))
            slopes.append({'ratio':ratio,'alpha_plus_beta':f['slope'],'se':f['se'],'r_squared':f['r_squared'],
                           'actual_ratio_min':min(r['fy']/r['x'] for r in rr),'actual_ratio_max':max(r['fy']/r['x'] for r in rr)})
        X=np.column_stack([np.ones(len(rows)),np.log([r['x'] for r in rows]),np.log([r['fy'] for r in rows])])
        z=np.log([r['V'] for r in rows]);coef=np.linalg.lstsq(X,z,rcond=None)[0];res=z-X@coef
        cov=np.linalg.inv(X.T@X)*(res@res)/(len(rows)-3)
        b=fixed[-1]['beta'];delta=float(np.mean([f['alpha_plus_beta'] for f in slopes]))
        delta_se=float(np.std([f['alpha_plus_beta'] for f in slopes],ddof=1)/math.sqrt(8))
        alpha=delta-b
        logcs=np.array([math.log(r['V'])-alpha*math.log(r['x'])-b*math.log(r['fy']) for r in rows])
        combined={'alpha':alpha,'alpha_se':math.hypot(delta_se,fixed[-1]['beta_se']),
                  'beta':b,'beta_se':fixed[-1]['beta_se'],'alpha_plus_beta':delta,'alpha_plus_beta_se':delta_se,
                  'C':float(np.exp(np.mean(logcs))),'log_C_residual_se':float(np.std(logcs,ddof=1)/math.sqrt(len(logcs))),
                  'note':'Combines the largest-x beta with the mean fixed-ratio delta=alpha+beta, then fits C with those exponents. alpha_se combines marginal SEs in quadrature and ignores correlation; C residual SE is conditional on fitted exponents.'}
        output[name]={'rows':rows,'fit_combined_two_ways':combined,
            'fit_fixed_x':{'beta':fixed[-1]['beta'],'beta_se':fixed[-1]['beta_se'],'x':xs[-1],'by_x':fixed,
                           'note':'Log-log OLS over all eight ratios; curvature in the ratio biases a pure power fit. Standard errors describe OLS residuals only.'},
            'fit_fixed_ratio':{'alpha_plus_beta':float(np.mean([f['alpha_plus_beta'] for f in slopes])),
                               'se':float(np.std([f['alpha_plus_beta'] for f in slopes],ddof=1)/math.sqrt(8)),
                               'by_ratio':slopes,'note':'Top-level estimate is the mean of eight slopes; its SE is their dispersion/sqrt(8). By-ratio OLS SEs are reported separately. Fits hold the target ratio fixed; actual ratios differ because y is integral.'},
            'fit_joint':{'C':math.exp(coef[0]),'C_log_se':float(np.sqrt(cov[0,0])),
                         'alpha':float(coef[1]),'alpha_se':float(np.sqrt(cov[1,1])),
                         'beta':float(coef[2]),'beta_se':float(np.sqrt(cov[2,2])),
                         'log_residual_rms':float(np.sqrt(np.mean(res**2))),
                         'note':'Joint unweighted OLS log V=log C+alpha log x+beta log f(y). This power-law C is distinct from the small-ratio asymptotic-normalisation intercept.'},
            'normalised':norm,'constant_extrapolated':extrapolate(norm,xs)}
    return output

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--xs',nargs='+',type=int,default=[1000000,4000000,16000000,64000000,256000000])
    ap.add_argument('--reuse',action='store_true',help='Reuse raw CSV files, but repeat Python validations and fits.')
    args=ap.parse_args();xs=sorted(set(args.xs));start=time.monotonic()
    previous_metadata={}
    if args.reuse and (ROOT/'results.json').exists():
        with open(ROOT/'results.json') as f:previous_metadata=json.load(f).get('metadata',{})
    assert len(xs)>=2 and max(xs)<=536870911
    if not args.reuse:
        subprocess.run(['c++','-O3','-std=c++17','-ffp-contract=off','compute_core.cpp','-o','compute_core'],cwd=ROOT,check=True)
    runs=[]
    for x in [1000]+xs:
        fname=ROOT/f'raw_{x}.csv'
        if not (args.reuse and fname.exists()):
            t=time.monotonic()
            subprocess.run([str(ROOT/'compute_core'),str(x),str(fname),'1000' if x==1000 else '50'],check=True)
            runs.append({'x':x,'elapsed_seconds':time.monotonic()-t})
    def read(x):
        with open(ROOT/f'raw_{x}.csv') as f:return list(csv.DictReader(f))
    validation=validate(read(1000))
    records=[r for x in xs for r in read(x)]
    validation+=validate_large(records,xs)
    out={'polynomials':analyse(records,xs),'validation':validation,
         'notes':'All Q and autocorrelation counts and weighted count-square sums are exact integers. Density rational coefficients are evaluated using double-double arithmetic (~31 decimal digits); 6/pi^2 and final V are evaluated with mpmath at 70 digits. V is not an integer or exact rational: V=A-2*x*(6/pi^2)*B+x^2*(6/pi^2)^2*D. Decimal strings are rounded to 20 significant digits, conservatively below the roughly 31-digit double-double working precision to allow for accumulation and cancellation; small-x values are independently checked against exact rational arithmetic. All grid y are the largest integers with f(y)<=target_ratio*x. No paper, website or external source was consulted. Normalised values have persistent dependence on the ratio across the x grid, so fixed-x slopes can absorb ratio curvature. Stability can be nonmonotone in ratio; the cutoff requires every higher grid row to pass. Fits are empirical and their OLS SEs do not account for finite-x bias, ratio curvature, polynomial sampling, or extrapolation misspecification. Adjacent lower-cutoff fits are sensitivity diagnostics and may intentionally include an unstable row; the central fit excludes all rows below its cutoff.',
         'metadata':{'x_grid':xs,'target_ratios':RATIOS,'runtime_seconds_this_invocation':time.monotonic()-start,'core_runs':runs or previous_metadata.get('core_runs',[]),'reused_csv':args.reuse,
                     'integer_ntt_prime':3221225473,'ntt_primitive_root':5,'max_supported_x':536870911,'external_sources':[]}}
    with open(ROOT/'results.json','w') as f:json.dump(out,f,indent=2,allow_nan=False)
    print(json.dumps({'runtime_seconds':time.monotonic()-start,'summary':{name:{'joint':p['fit_joint'],'constant':p['constant_extrapolated']} for name,p in out['polynomials'].items()}},indent=2))
if __name__=='__main__':main()
