#!/usr/bin/env python3
"""Exact counts, 70-digit density aggregates, empirical fits. See README.md."""
import argparse
import decimal
import fractions
import json
import math
import pathlib
import struct
import subprocess
import time
import numpy as np
from scipy.stats import linregress
import mpmath as mp

ROOT = pathlib.Path(__file__).resolve().parent
RATIOS = [.01, .02, .05, .1, .2, .4, .7, 1.]
NAMES = ['k^2+1', 'k^3+2', '2k+1']
decimal.getcontext().prec = 70
mp.mp.dps = 85
D = decimal.Decimal
C0 = D(str(6/mp.pi**2))
RECORD = struct.Struct('<9Q')

def fy(p, k):
    return [lambda: k*k+1, lambda: k*k*k+2, lambda: 2*k+1][p]()

def choose_y(p, x, ratio):
    target = int(D(str(ratio))*x)
    lo, hi = 0, x
    while lo < hi:
        mid = (lo+hi+1)//2
        if fy(p, mid) <= target: lo = mid
        else: hi = mid-1
    return lo

def compile_worker():
    subprocess.run(['clang++', '-O3', '-std=c++17', str(ROOT/'counts.cpp'), '-o', str(ROOT/'counts')], check=True)

def run_x(x, validate=False, ratios=RATIOS):
    starts = time.monotonic()
    cap=int(D(str(max(ratios)))*x)
    proc = subprocess.Popen([str(ROOT/'counts'), str(x),str(cap)], stdout=subprocess.PIPE)
    output = {}
    for p, name in enumerate(NAMES):
        points = {choose_y(p,x,r): r for r in ratios}
        s2, b, c = 0, D(0), D(0)
        rows = []
        for k in range(1, choose_y(p,x,max(ratios))+1):
            data = proc.stdout.read(RECORD.size)
            if len(data) != RECORD.size: raise RuntimeError('Incomplete worker output')
            z = RECORD.unpack(data)
            bn, bd, cn, cd = [z[j]+(z[j+1]<<64) for j in [1,3,5,7]]
            s2 += z[0]
            b += D(bn)/D(bd)
            c += D(cn)/D(cd)
            if validate:
                brute_record_check(x,p,k,z[0],bn,bd,cn,cd)
            if k in points:
                v = D(s2)-2*C0*x*b+C0*C0*x*x*c
                yval=fy(p,k)
                norm=v/(D(x).sqrt()*D(yval)*D(yval).sqrt())
                rows.append(dict(x=x,y=k,fy=yval,V=float(v),V_decimal=str(v),
                                 ratio_target=points[k],ratio_actual=yval/x,
                                 sum_Q_squared_weighted=s2,
                                 B_decimal=str(b),D_decimal=str(c),
                                 normalised=float(norm)))
        output[name]=rows
    if proc.stdout.read(1): raise RuntimeError('Unexpected worker output')
    if proc.wait(): raise RuntimeError('Worker failed')
    output['_runtime_seconds']=time.monotonic()-starts
    return output

def squarefree(x):
    a=np.ones(x+1,dtype=np.int8);a[0]=0
    for n in range(2,math.isqrt(x)+1): a[n*n::n*n]=0
    return a

def primes_to(n):
    return [p for p in range(2,n+1) if all(p%d for d in range(2,math.isqrt(p)+1))]

def rational_density(q,l):
    # g(q,l) = (6/pi^2) times the returned exact rational.
    a=fractions.Fraction(1,q)
    for p in primes_to(q):
        if q%p: continue
        if q%(p*p)==0 and l%(p*p)==0:return fractions.Fraction(0)
        a*=fractions.Fraction(p*p,p*p-1)
        if q%(p*p) and l%p==0:a*=fractions.Fraction(p-1,p)
    return a

def brute_record_check(x,p,k,s2,bn,bd,cn,cd):
    q=fy(p,k); w=[2*k,3*k*k,2][p]
    sf=squarefree(x)
    counts=np.bincount(np.arange(x+1)%q,weights=sf,minlength=q).astype(np.int64)
    assert int(counts.sum())==int(sf.sum())
    assert int(counts@counts)*w==s2
    gg=[rational_density(q,l) for l in range(q)]
    assert sum((int(counts[l])*gg[l] for l in range(q)),fractions.Fraction())*w==fractions.Fraction(bn,bd)
    assert sum((v*v for v in gg),fractions.Fraction())*w==fractions.Fraction(cn,cd)

def validations():
    modulus=3221225473
    assert all(modulus%d for d in range(2,math.isqrt(modulus)+1))
    assert (modulus-1)==3*(1<<30)
    assert pow(5,(modulus-1)//2,modulus)!=1 and pow(5,(modulus-1)//3,modulus)!=1
    # Independently enumerate residues for each local prime-square condition.
    ps=primes_to(50)
    baseline=math.prod([fractions.Fraction(p*p-1,p*p) for p in ps])
    checked=0
    for q in range(1,51):
        for l in range(q):
            conditional=fractions.Fraction(1,q)
            for p in ps:
                period=math.lcm(q,p*p)
                vals=range(l,period,q)
                allowed=sum(n%(p*p)!=0 for n in vals)
                conditional*=fractions.Fraction(allowed,len(vals))
            assert conditional/baseline==rational_density(q,l)
            checked+=1
    a=squarefree(1_000_000); total=int(a.sum()); maxerr=0.
    for q in range(1,51):
        counts=np.bincount(np.arange(len(a))%q,weights=a,minlength=q).astype(np.int64)
        assert int(counts.sum())==total
        for l,count in enumerate(counts):
            frac=rational_density(q,l)
            gg=float(C0)*float(frac)
            maxerr=max(maxerr,abs(count/1_000_000-gg))
    run_x(257,validate=True)
    return ['NTT modulus 3221225473 verified prime by trial division; primitive root 5 verified using both prime factors 2 and 3 of modulus-1.',
            f'Exact rational g/(6/pi^2) agrees with independent brute local-residue densities for all {checked} pairs q<=50; finite Euler product over primes<=50 divided out exactly.',
            f'Brute squarefree frequencies at x=1000000, q<=50: maximum absolute density discrepancy {maxerr:.12g}.',
            f'sum_l Q(x;q,l)=Q(x;1,1) exactly for every q<=50 at x=1000000 (Q={total}).',
            'At x=257 every generated modulus for all three polynomials: exact sum Q^2 and both rational density coefficients agree with direct residue counts.',
            'Every production x: NTT autocorrelation C(0) and seven direct lag sums checked with exact integers. NTT prime 3221225473 (primitive root 5, up to length 2^30) exceeds every autocorrelation coefficient; no modular ambiguity.']

def regression(x,y):
    r=linregress(np.asarray(x),np.asarray(y))
    return dict(slope=float(r.slope),se=float(r.stderr),intercept=float(r.intercept),r_squared=float(r.rvalue**2))

def analyse(allruns, validation):
    result={'polynomials':{},'validation':validation,'notes':''}
    for name in NAMES:
        allrows=[r for run in allruns for r in run[name]]
        rows=[r for r in allrows if r['ratio_target'] in RATIOS]
        xs=sorted({r['x'] for r in rows})
        fixed=[]
        for x in xs:
            rr=[r for r in rows if r['x']==x]
            fit=regression(np.log([r['fy'] for r in rr]),np.log([r['V'] for r in rr]))
            fixed.append(dict(x=x,beta=fit['slope'],beta_se=fit['se'],C_x_alpha=math.exp(fit['intercept']),C_assuming_alpha_half=math.exp(fit['intercept'])/math.sqrt(x),r_squared=fit['r_squared']))
        ratiofits=[]
        for ratio in RATIOS:
            rr=[r for r in rows if r['ratio_target']==ratio]
            fit=regression(np.log([r['x'] for r in rr]),np.log([r['V'] for r in rr]))
            large=rr[-4:]
            fl=regression(np.log([r['x'] for r in large]),np.log([r['V'] for r in large]))
            quant=regression(np.log([r['x'] for r in rr]),np.log([r['V']/(r['ratio_actual']/ratio)**1.5 for r in rr]))
            ratiofits.append(dict(ratio=ratio,alpha_plus_beta=fit['slope'],se=fit['se'],C_times_ratio_beta=math.exp(fit['intercept']),C_assuming_beta_threehalves=math.exp(fit['intercept'])/ratio**1.5,r_squared=fit['r_squared'],largest_four_x={'alpha_plus_beta':fl['slope'],'se':fl['se']},ratio_quantisation_adjusted_assuming_beta_threehalves={'alpha_plus_beta':quant['slope'],'se':quant['se']}))
        # Joint log regression; formal OLS SE describe scatter, not rigorous uncertainty.
        A=np.array([[1,math.log(r['x']),math.log(r['fy'])] for r in rows]); yy=np.log([r['V'] for r in rows])
        coef=np.linalg.lstsq(A,yy,rcond=None)[0]; resid=yy-A@coef
        cov=np.linalg.inv(A.T@A)*(resid@resid)/(len(rows)-3)
        ses=np.sqrt(np.diag(cov))
        stability=[]
        for ratio in RATIOS:
            rr=[next(r for r in rows if r['x']==x and r['ratio_target']==ratio) for x in xs[-2:]]
            change=rr[-1]['normalised']/rr[-2]['normalised']-1
            stability.append(dict(ratio=ratio,x_previous=xs[-2],x_largest=xs[-1],relative_change=change,passes_1_percent=abs(change)<.01))
        diagnostic_stability=[]
        for ratio in sorted({r['ratio_target'] for r in allrows if r['ratio_target'] not in RATIOS}):
            rr=[r for r in allrows if r['ratio_target']==ratio and r['x'] in xs[-2:]]
            if len(rr)==2:
                rr.sort(key=lambda r:r['x'])
                change=rr[1]['normalised']/rr[0]['normalised']-1
                diagnostic_stability.append(dict(ratio=ratio,relative_change=change,passes_1_percent=abs(change)<.01))
        # A cutoff requires ALL grid rows at and above it to be stable.
        passing=[i for i in range(len(RATIOS)) if all(s['passes_1_percent'] for s in stability[i:])]
        extrap=extrapolate(allrows,xs,passing)
        last=[r for r in rows if r['x']==xs[-1]]
        smallest=next(r for r in last if r['ratio_target']==RATIOS[0])
        largest=next(r for r in last if r['ratio_target']==RATIOS[-1])
        ratio_effect=dict(x=xs[-1],normalised_at_smallest_ratio=smallest['normalised'],
                          normalised_at_largest_ratio=largest['normalised'],
                          relative_rise_across_ratio_grid=largest['normalised']/smallest['normalised']-1,
                          max_absolute_relative_change_between_two_largest_x=max(abs(s['relative_change']) for s in stability),
                          all_requested_ratios_stable=all(s['passes_1_percent'] for s in stability))
        result['polynomials'][name]=dict(rows=rows,
            fit_fixed_x={**{k:v for k,v in fixed[-1].items() if k!='x'},'x':xs[-1],'all_x':fixed},
            fit_fixed_ratio={'alpha_plus_beta':float(np.mean([r['alpha_plus_beta'] for r in ratiofits])),
                'se':float(np.std([r['alpha_plus_beta'] for r in ratiofits],ddof=1)/math.sqrt(len(ratiofits))),
                'aggregation':'Mean of eight ratio-specific log-log slopes; SE is across-ratio SE. Individual regression SEs below.',
                'by_ratio':ratiofits},
            fit_joint={'C':math.exp(coef[0]),'C_se_delta_method':math.exp(coef[0])*ses[0],
                'alpha':coef[1],'alpha_se':ses[1],'beta':coef[2],'beta_se':ses[2],
                'log_residual_rms':float(np.sqrt(np.mean(resid**2)))},
            normalised=[dict(x=r['x'],ratio=r['ratio_target'],ratio_actual=r['ratio_actual'],V_over_x12_fy32=r['normalised']) for r in rows],
            diagnostic_rows=[r for r in allrows if r['ratio_target'] not in RATIOS],diagnostic_stability=diagnostic_stability,
            stability=stability,ratio_dependence=ratio_effect,constant_extrapolated=extrap)
    result['notes']='No external sources read or used. Counts and coefficient numerators/denominators use exact integer arithmetic; g and V evaluated with 70 decimal digits and 85-digit 6/pi^2. V is inherently irrational; V_decimal retains its evaluated precision. Ratios label target grid: actual f(y)/x is recorded and used for normalisation and extrapolation. Cutoffs refer to the eight requested ratios; the extra .005 row checks lower-neighbor sensitivity. Formal regression standard errors measure residual scatter, not a proven asymptotic error. Persistent ratio dependence can bias the fixed-x exponent relative to a small-ratio limiting exponent; see ratio_dependence for its size and compare it to changes in x. Extrapolation model error need not be captured by the heuristic uncertainty envelope. No proofs are claimed.'
    result['runtime_by_x']=[dict(x=run[NAMES[0]][0]['x'],seconds=run['_runtime_seconds']) for run in allruns]
    result['diagnostic_runtime_by_x']=[dict(x=run[NAMES[0]][0]['x'],seconds=run['_diagnostic_runtime_seconds']) for run in allruns if '_diagnostic_runtime_seconds' in run]
    return result

def write_report(result):
    lines=['# Numerical evidence','',
           'Counts are exact integers; density terms and variance are evaluated at 70 decimal digits. The numerical fits below are empirical and their errors are heuristic. No external literature was used.','',
           'The primary grid is the eight ratios requested in the task. The extra ratio 0.005 at the two largest sizes is a lower-neighbor sensitivity diagnostic; it does not redefine the cutoff on the requested grid.','',
           '| polynomial | largest x | fixed-x beta (SE) | fixed-ratio alpha+beta (SE) | joint-fit C | extrapolated constant (uncertainty) | ratio cutoff |',
           '|---|---:|---:|---:|---:|---:|---:|']
    for name,p in result['polynomials'].items():
        fx=p['fit_fixed_x'];fr=p['fit_fixed_ratio'];ce=p['constant_extrapolated'];j=p['fit_joint']
        est='not reported' if ce['value'] is None else f"{ce['value']:.8f} ± {ce['uncertainty']:.8f}"
        lines.append(f"| {name} | {fx['x']} | {fx['beta']:.7f} ({fx['beta_se']:.7f}) | {fr['alpha_plus_beta']:.7f} ({fr['se']:.7f}) | {j['C']:.7f} | {est} | {ce['ratio_cutoff']} |")
    lines+=['','The fixed-ratio summary is the mean of the eight separate slopes; its SE is the across-ratio standard error. Every individual slope and its regression SE, the largest-four-size fits, and a quantisation-adjusted diagnostic are in results.json. The fixed-x intercept identifies C*x^alpha; results.json also gives C after imposing alpha=1/2 and the unrestricted joint log-linear fit.','',
            'The fixed-x beta is a fit over finite ratios, where the normalized value itself depends on the ratio. It should not be interpreted as the limiting small-ratio exponent.','']
    for name,p in result['polynomials'].items():
        lines += [f'## {name}','','Normalized values V / (sqrt(x) * f(y)^(3/2)); column headings are target ratios. Actual ratios and integer y are in results.json.','',
                  '| x | '+ ' | '.join(map(str,RATIOS))+' |','|---:|'+ '---:|'*len(RATIOS)]
        xs=sorted({r['x'] for r in p['rows']})
        for x in xs:
            vals=[next(r['normalised'] for r in p['rows'] if r['x']==x and r['ratio_target']==ratio) for ratio in RATIOS]
            lines.append('| '+str(x)+' | '+' | '.join(f'{v:.9f}' for v in vals)+' |')
        lines+=['','Percent change between the two largest sizes: '+', '.join(f"r={s['ratio']}: {100*s['relative_change']:+.4f}%" for s in p['stability'])+'.','']
        ce=p['constant_extrapolated'];lines += [ce['method'],'',ce['cutoff_sensitivity'],'']
        if ce.get('cutoff_fits'):
            lines+=['Cutoff fits: '+', '.join(f"cutoff {v['ratio_cutoff']}: C={v['value']:.9f}" for v in ce['cutoff_fits'])+'.','']
        if p['diagnostic_rows']:
            lines+=['Ratio 0.005 diagnostic: '+', '.join(f"x={r['x']}: N={r['normalised']:.9f}" for r in p['diagnostic_rows'])+'.','']
    lines+=['## Validation','']+['- '+s for s in result['validation']]
    lines+=['','## Runtime','',f"Primary computations: {sum(r['seconds'] for r in result['runtime_by_x']):.2f} seconds. Lower-neighbor diagnostics: {sum(r['seconds'] for r in result['diagnostic_runtime_by_x']):.2f} seconds. Compilation, fitting, and validation are additional.",'']
    (ROOT/'report.md').write_text('\n'.join(lines))

def extrapolate(rows,xs,passing):
    if not passing:
        return {'value':None,'uncertainty':None,'method':'No suffix of ratio grid passes the 1% stability test; no empirical limit reported.','ratio_cutoff':None,'cutoff_sensitivity':'Not applicable.'}
    cutoff=passing[0]
    def one_fit(idx,x,model,upper_ratio=1.):
        threshold=.005 if idx<0 else RATIOS[idx]
        rr=[r for r in rows if r['x']==x and threshold<=r['ratio_target']<=upper_ratio]
        t=np.array([r['ratio_actual'] for r in rr]);z=np.array([r['normalised'] for r in rr])
        if model=='sqrt+linear': A=np.column_stack([np.ones(len(t)),np.sqrt(t),t])
        elif model=='sqrt': A=np.column_stack([np.ones(len(t)),np.sqrt(t)])
        else: A=np.column_stack([np.ones(len(t)),np.sqrt(t),t,t**1.5])
        if len(t)<=A.shape[1]:return None
        cf=np.linalg.lstsq(A,z,rcond=None)[0];e=z-A@cf
        cov=np.linalg.inv(A.T@A)*(e@e)/(len(t)-A.shape[1])
        return dict(value=float(cf[0]),intercept_se=float(math.sqrt(cov[0,0])),coefficients=cf.tolist(),residual_rms=float(np.sqrt(np.mean(e*e))),n=len(t),x=x,model=model,ratio_cutoff=threshold,upper_ratio=upper_ratio)
    primary=one_fit(cutoff,xs[-1],'sqrt+linear')
    if primary is None:
        return {'value':None,'uncertainty':None,'method':'Stable suffix has too few points for the three-parameter extrapolation plus residual degrees of freedom.','ratio_cutoff':RATIOS[cutoff],'cutoff_sensitivity':'No adequately determined fit.'}
    variants=[]
    lower=-1 if cutoff==0 and any(r['ratio_target']==.005 and r['x']==xs[-1] for r in rows) else max(0,cutoff-1)
    for idx in sorted(set([lower,cutoff,min(len(RATIOS)-1,cutoff+1)])):
        fit=one_fit(idx,xs[-1],'sqrt+linear')
        if fit:variants.append(fit)
    previous=one_fit(cutoff,xs[-2],'sqrt+linear')
    alternatives=[one_fit(cutoff,xs[-1],m) for m in ['sqrt','sqrt+linear+threehalves']]
    alternatives=[v for v in alternatives if v]
    windowfits=[one_fit(cutoff,xs[-1],'sqrt+linear',upper) for upper in [.1,.2,.4]]
    windowfits=[v for v in windowfits if v]
    deviations=[abs(v['value']-primary['value']) for v in variants+alternatives+windowfits+([previous] if previous else [])]
    sensitivity=max([abs(v['value']-primary['value']) for v in variants]+[0])
    spread=max(v['value'] for v in variants)-min(v['value'] for v in variants)
    uncertainty=max([2*primary['intercept_se'],spread]+deviations)
    return dict(value=primary['value'],uncertainty=uncertainty,method='Unweighted least squares N(r)=C+a*sqrt(r)+b*r using only largest-x rows at/above stable-suffix cutoff. Uncertainty=max(2 formal intercept SE, full neighboring-cutoff spread, previous-x shift, alternative-model shifts, upper-ratio-window shifts for r_max=.1,.2,.4 when determined); heuristic, not a confidence interval.',ratio_cutoff=RATIOS[cutoff],cutoff_sensitivity=f'Maximum absolute intercept shift upon moving cutoff one grid step: {sensitivity:.12g}; full range across cutoff fits: {spread:.12g}. See cutoff_fits (lower adjacent cutoff may fail stability).',cutoff_spread=spread,primary_fit=primary,cutoff_fits=variants,previous_x_fit=previous,alternative_models=alternatives,upper_ratio_window_fits=windowfits)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--xs',default='250000,500000,1000000,2000000,4000000,8000000,16000000,32000000,64000000,128000000,256000000')
    parser.add_argument('--reuse',action='store_true');parser.add_argument('--skip-validation',action='store_true');args=parser.parse_args()
    compile_worker()
    validation=[] if args.skip_validation else validations()
    runs=[]
    for x in map(int,args.xs.split(',')):
        cache=ROOT/f'run_{x}.json'
        if args.reuse and cache.exists():run=json.loads(cache.read_text())
        else:
            run=run_x(x);cache.write_text(json.dumps(run,indent=2)+'\n')
        runs.append(run)
        if len(runs)>=2:
            (ROOT/'results.json').write_text(json.dumps(analyse(runs,validation),indent=2)+'\n')
        print(f'x={x} completed in {run["_runtime_seconds"]:.2f}s',flush=True)
    # One extra lower neighbor makes cutoff sensitivity two-sided when the
    # smallest requested ratio .01 is already stable.
    for run in runs[-2:]:
        x=run[NAMES[0]][0]['x']
        if not any(r['ratio_target']==.005 for r in run[NAMES[0]]):
            diagnostic_cache=ROOT/f'diagnostic_{x}.json'
            if args.reuse and diagnostic_cache.exists():diag=json.loads(diagnostic_cache.read_text())
            else:
                diag=run_x(x,ratios=[.005])
                diagnostic_cache.write_text(json.dumps(diag,indent=2)+'\n')
            for name in NAMES:run[name].extend(diag[name])
            run['_diagnostic_runtime_seconds']=diag['_runtime_seconds']
            (ROOT/f'run_{x}.json').write_text(json.dumps(run,indent=2)+'\n')
    result=analyse(runs,validation)
    (ROOT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    write_report(result)

if __name__=='__main__':main()
