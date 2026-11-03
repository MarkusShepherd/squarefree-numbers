import mpmath as mp
mp.mp.dps=25
# int_0^1 (t^2-t)/2 (n+t)^{-3/2} dt analytically via antiderivative using mp.quad per piece but sum with richardson via mp.nsum on B2 part only
J0 = mp.quad(lambda u:(u*u-u)/2*u**-1.5,[0,1])
def pieceB2(n): return mp.quad(lambda t:((t*t-t)/2+mp.mpf(1)/12)*(n+t)**-1.5,[0,1])
S=mp.nsum(pieceB2,[1,mp.inf]) - mp.mpf(1)/12*2   # int_1^inf u^-1.5 = 2
print((J0+S)/2, 2*mp.zeta(-0.5))
