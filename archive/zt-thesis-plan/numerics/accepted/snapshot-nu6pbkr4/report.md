# Numerical evidence

Counts are exact integers; density terms and variance are evaluated at 70 decimal digits. The numerical fits below are empirical and their errors are heuristic. No external literature was used.

The primary grid is the eight ratios requested in the task. The extra ratio 0.005 at the two largest sizes is a lower-neighbor sensitivity diagnostic; it does not redefine the cutoff on the requested grid.

| polynomial | largest x | fixed-x beta (SE) | fixed-ratio alpha+beta (SE) | joint-fit C | extrapolated constant (uncertainty) | ratio cutoff |
|---|---:|---:|---:|---:|---:|---:|
| k^2+1 | 256000000 | 1.5454471 (0.0038749) | 2.0007782 (0.0006319) | 0.1730825 | 0.13447471 ± 0.00728496 | 0.01 |
| k^3+2 | 256000000 | 1.5382976 (0.0037296) | 1.9977580 (0.0021171) | 0.1957374 | 0.13632126 ± 0.00240361 | 0.01 |
| 2k+1 | 256000000 | 1.5511714 (0.0074838) | 2.0001222 (0.0000871) | 0.1783993 | 0.14168635 ± 0.00821778 | 0.01 |

The fixed-ratio summary is the mean of the eight separate slopes; its SE is the across-ratio standard error. Every individual slope and its regression SE, the largest-four-size fits, and a quantisation-adjusted diagnostic are in results.json. The fixed-x intercept identifies C*x^alpha; results.json also gives C after imposing alpha=1/2 and the unrestricted joint log-linear fit.

The fixed-x beta is a fit over finite ratios, where the normalized value itself depends on the ratio. It should not be interpreted as the limiting small-ratio exponent.

## k^2+1

Normalized values V / (sqrt(x) * f(y)^(3/2)); column headings are target ratios. Actual ratios and integer y are in results.json.

| x | 0.01 | 0.02 | 0.05 | 0.1 | 0.2 | 0.4 | 0.7 | 1.0 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 250000 | 0.142648677 | 0.146052371 | 0.146549203 | 0.152224407 | 0.157416355 | 0.163777441 | 0.170588878 | 0.171642034 |
| 500000 | 0.142564640 | 0.143624585 | 0.145049411 | 0.151488808 | 0.157419438 | 0.163281045 | 0.170310845 | 0.171371952 |
| 1000000 | 0.141854642 | 0.143161710 | 0.144885731 | 0.151912137 | 0.156975277 | 0.163179299 | 0.170250449 | 0.171362352 |
| 2000000 | 0.141894716 | 0.143860028 | 0.145329552 | 0.151304362 | 0.156883958 | 0.163051200 | 0.170097740 | 0.171268856 |
| 4000000 | 0.141686346 | 0.143301940 | 0.144687127 | 0.151276060 | 0.156752126 | 0.162938441 | 0.170032492 | 0.171220325 |
| 8000000 | 0.141162009 | 0.143155077 | 0.144704261 | 0.151198910 | 0.156711763 | 0.162890009 | 0.170034262 | 0.171183118 |
| 16000000 | 0.141174926 | 0.143090387 | 0.144621967 | 0.151153499 | 0.156632016 | 0.162834521 | 0.169986248 | 0.171152613 |
| 32000000 | 0.141046372 | 0.143020696 | 0.144584194 | 0.151055827 | 0.156600887 | 0.162811753 | 0.169957408 | 0.171141344 |
| 64000000 | 0.140949173 | 0.142966188 | 0.144504804 | 0.151012480 | 0.156577514 | 0.162792315 | 0.169935005 | 0.171119756 |
| 128000000 | 0.140908763 | 0.142911838 | 0.144472120 | 0.150993421 | 0.156556369 | 0.162788781 | 0.169925633 | 0.171106413 |
| 256000000 | 0.140857664 | 0.142919105 | 0.144457333 | 0.150975676 | 0.156549605 | 0.162775241 | 0.169925129 | 0.171101329 |

Percent change between the two largest sizes: r=0.01: -0.0363%, r=0.02: +0.0051%, r=0.05: -0.0102%, r=0.1: -0.0118%, r=0.2: -0.0043%, r=0.4: -0.0083%, r=0.7: -0.0003%, r=1.0: -0.0030%.

Unweighted least squares N(r)=C+a*sqrt(r)+b*r using only largest-x rows at/above stable-suffix cutoff. Uncertainty=max(2 formal intercept SE, full neighboring-cutoff spread, previous-x shift, alternative-model shifts, upper-ratio-window shifts for r_max=.1,.2,.4 when determined); heuristic, not a confidence interval.

Maximum absolute intercept shift upon moving cutoff one grid step: 0.00105314171015; full range across cutoff fits: 0.00204570371069. See cutoff_fits (lower adjacent cutoff may fail stability).

Cutoff fits: cutoff 0.005: C=0.135467267, cutoff 0.01: C=0.134474705, cutoff 0.02: C=0.133421564.

Ratio 0.005 diagnostic: x=128000000: N=0.140423850, x=256000000: N=0.140391181.

## k^3+2

Normalized values V / (sqrt(x) * f(y)^(3/2)); column headings are target ratios. Actual ratios and integer y are in results.json.

| x | 0.01 | 0.02 | 0.05 | 0.1 | 0.2 | 0.4 | 0.7 | 1.0 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 250000 | 0.159912890 | 0.160232313 | 0.160970668 | 0.159910160 | 0.163172467 | 0.161392328 | 0.169393655 | 0.172386665 |
| 500000 | 0.155112231 | 0.162671103 | 0.156355357 | 0.161316737 | 0.159403506 | 0.159027993 | 0.167784715 | 0.170861702 |
| 1000000 | 0.153561931 | 0.149407312 | 0.154181812 | 0.155026333 | 0.155087215 | 0.158578474 | 0.166277675 | 0.170712799 |
| 2000000 | 0.148040930 | 0.147909290 | 0.151134320 | 0.150023761 | 0.154647682 | 0.157691179 | 0.166923471 | 0.169598894 |
| 4000000 | 0.144715978 | 0.147762669 | 0.146249612 | 0.151597897 | 0.154779807 | 0.157140811 | 0.165213976 | 0.168421803 |
| 8000000 | 0.141957839 | 0.144833270 | 0.145866722 | 0.149564402 | 0.154211017 | 0.157510113 | 0.165584590 | 0.168244639 |
| 16000000 | 0.142398504 | 0.144360445 | 0.144416267 | 0.149752933 | 0.153583509 | 0.156699469 | 0.164843729 | 0.167874558 |
| 32000000 | 0.142148684 | 0.142777757 | 0.144311058 | 0.149048356 | 0.153051180 | 0.156095603 | 0.164600938 | 0.167379216 |
| 64000000 | 0.140427132 | 0.142955118 | 0.143924999 | 0.149586386 | 0.152599641 | 0.155833116 | 0.164525335 | 0.167243657 |
| 128000000 | 0.141268290 | 0.141954414 | 0.144385424 | 0.148961494 | 0.152464244 | 0.155936468 | 0.164234477 | 0.166987438 |
| 256000000 | 0.139989779 | 0.141202318 | 0.143911976 | 0.148477411 | 0.152338675 | 0.155498711 | 0.163990356 | 0.166705566 |

Percent change between the two largest sizes: r=0.01: -0.9050%, r=0.02: -0.5298%, r=0.05: -0.3279%, r=0.1: -0.3250%, r=0.2: -0.0824%, r=0.4: -0.2807%, r=0.7: -0.1486%, r=1.0: -0.1688%.

Unweighted least squares N(r)=C+a*sqrt(r)+b*r using only largest-x rows at/above stable-suffix cutoff. Uncertainty=max(2 formal intercept SE, full neighboring-cutoff spread, previous-x shift, alternative-model shifts, upper-ratio-window shifts for r_max=.1,.2,.4 when determined); heuristic, not a confidence interval.

Maximum absolute intercept shift upon moving cutoff one grid step: 0.000958582687495; full range across cutoff fits: 0.000976883979907. See cutoff_fits (lower adjacent cutoff may fail stability).

Cutoff fits: cutoff 0.005: C=0.137279840, cutoff 0.01: C=0.136321257, cutoff 0.02: C=0.136302956.

Ratio 0.005 diagnostic: x=128000000: N=0.140189035, x=256000000: N=0.140760935.

## 2k+1

Normalized values V / (sqrt(x) * f(y)^(3/2)); column headings are target ratios. Actual ratios and integer y are in results.json.

| x | 0.01 | 0.02 | 0.05 | 0.1 | 0.2 | 0.4 | 0.7 | 1.0 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 250000 | 0.143760978 | 0.148092592 | 0.149307130 | 0.156697614 | 0.161734291 | 0.162453103 | 0.182395567 | 0.183695914 |
| 500000 | 0.144153434 | 0.148231972 | 0.149326725 | 0.156722795 | 0.161716288 | 0.162464969 | 0.182393285 | 0.183693831 |
| 1000000 | 0.144392418 | 0.148302006 | 0.149319591 | 0.156699952 | 0.161695661 | 0.162452265 | 0.182387713 | 0.183689771 |
| 2000000 | 0.144437354 | 0.148283047 | 0.149305371 | 0.156686474 | 0.161700755 | 0.162445918 | 0.182389304 | 0.183691204 |
| 4000000 | 0.144507462 | 0.148326996 | 0.149321031 | 0.156694497 | 0.161706466 | 0.162449054 | 0.182390432 | 0.183693455 |
| 8000000 | 0.144592975 | 0.148371862 | 0.149349205 | 0.156705515 | 0.161712812 | 0.162451848 | 0.182390265 | 0.183691718 |
| 16000000 | 0.144608559 | 0.148375497 | 0.149350189 | 0.156705548 | 0.161711788 | 0.162452348 | 0.182390204 | 0.183690979 |
| 32000000 | 0.144592292 | 0.148364838 | 0.149340641 | 0.156702005 | 0.161708551 | 0.162451472 | 0.182390029 | 0.183691221 |
| 64000000 | 0.144592998 | 0.148365508 | 0.149340680 | 0.156701657 | 0.161708862 | 0.162451056 | 0.182390192 | 0.183691541 |
| 128000000 | 0.144597630 | 0.148368020 | 0.149341884 | 0.156702556 | 0.161709387 | 0.162451305 | 0.182390171 | 0.183691472 |
| 256000000 | 0.144597566 | 0.148368345 | 0.149342615 | 0.156702821 | 0.161709574 | 0.162451402 | 0.182390141 | 0.183691458 |

Percent change between the two largest sizes: r=0.01: -0.0000%, r=0.02: +0.0002%, r=0.05: +0.0005%, r=0.1: +0.0002%, r=0.2: +0.0001%, r=0.4: +0.0001%, r=0.7: -0.0000%, r=1.0: -0.0000%.

Unweighted least squares N(r)=C+a*sqrt(r)+b*r using only largest-x rows at/above stable-suffix cutoff. Uncertainty=max(2 formal intercept SE, full neighboring-cutoff spread, previous-x shift, alternative-model shifts, upper-ratio-window shifts for r_max=.1,.2,.4 when determined); heuristic, not a confidence interval.

Maximum absolute intercept shift upon moving cutoff one grid step: 0.00144447574551; full range across cutoff fits: 0.00144447574551. See cutoff_fits (lower adjacent cutoff may fail stability).

Cutoff fits: cutoff 0.005: C=0.141878026, cutoff 0.01: C=0.141686350, cutoff 0.02: C=0.143130826.

Ratio 0.005 diagnostic: x=128000000: N=0.144844272, x=256000000: N=0.144844772.

## Validation

- NTT modulus 3221225473 verified prime by trial division; primitive root 5 verified using both prime factors 2 and 3 of modulus-1.
- Exact rational g/(6/pi^2) agrees with independent brute local-residue densities for all 1275 pairs q<=50; finite Euler product over primes<=50 divided out exactly.
- Brute squarefree frequencies at x=1000000, q<=50: maximum absolute density discrepancy 3.17040894156e-05.
- sum_l Q(x;q,l)=Q(x;1,1) exactly for every q<=50 at x=1000000 (Q=607926).
- At x=257 every generated modulus for all three polynomials: exact sum Q^2 and both rational density coefficients agree with direct residue counts.
- Every production x: NTT autocorrelation C(0) and seven direct lag sums checked with exact integers. NTT prime 3221225473 (primitive root 5, up to length 2^30) exceeds every autocorrelation coefficient; no modular ambiguity.

## Runtime

Primary computations: 753.00 seconds. Lower-neighbor diagnostics: 176.84 seconds. Compilation, fitting, and validation are additional.
