/*
 * sqf.c -- exact computation of V_f(x,y) = sum_{k<=y} f'(k) sum_{l<=f(k)} E(x;f(k),l)^2
 * for squarefree numbers.
 *
 * usage: sqf <poly> <x> <method> <dump> y1 y2 ...
 *   poly   : 0 -> f=k^2+1, 1 -> f=k^3+2, 2 -> f=2k+1
 *   method : direct (O(x) bincount per modulus) | fft (autocorrelation, all moduli at once)
 *   dump   : 1 -> also print one line per modulus
 *
 * Maths (see README.md):
 *   T(q)  = sum_l Q(x;q,l)^2   (exact integer)
 *   g(q,l)= c * R_q / q * prod_{p||q, p|l}(1-1/p) * [no p^2 | gcd(l,q)],  c=6/pi^2,
 *           R_q = prod_{p|q} p^2/(p^2-1)
 *   For squarefree n the bracket is 1, so
 *     sum_l g(q,l) Q(x;q,l) = (c R_q/q) * M_q/q',   M_q/q' = sum_{e|q'} mu(e)/e * N(x/e, e)
 *   with q' = prod_{p||q} p and N(X,e) = #{m<=X squarefree, (m,e)=1}.
 *   sum_l g^2 = (c R_q/q)^2 * prod_{p^a||q} s_p,  s_p = p^a-p^(a-2) (a>=2), (p-1)(p^2+p-1)/p^2 (a=1).
 *   With u = x c R_q/q :  sum_l E^2 = T - 2 u M/q' + u^2 S.   Done in double-double arithmetic.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>

typedef struct { double h, l; } dd;
static inline dd two_sum(double a, double b){ double s=a+b, bb=s-a; dd r={s,(a-(s-bb))+(b-bb)}; return r; }
static inline dd qts(double a, double b){ double s=a+b; dd r={s,b-(s-a)}; return r; }
static inline dd dd_add(dd a, dd b){
  dd s=two_sum(a.h,b.h), t=two_sum(a.l,b.l);
  s.l+=t.h; s=qts(s.h,s.l); s.l+=t.l; return qts(s.h,s.l);
}
static inline dd dd_neg(dd a){ dd r={-a.h,-a.l}; return r; }
static inline dd dd_mul(dd a, dd b){
  double p=a.h*b.h, e=fma(a.h,b.h,-p);
  e+=a.h*b.l+a.l*b.h; return qts(p,e);
}
static inline dd dd_d(double a){ dd r={a,0}; return r; }
static inline dd dd_div(dd a, dd b){
  double q1=a.h/b.h; dd r=dd_add(a,dd_neg(dd_mul(dd_d(q1),b)));
  double q2=r.h/b.h; r=dd_add(r,dd_neg(dd_mul(dd_d(q2),b)));
  double q3=r.h/b.h; dd q=qts(q1,q2); return dd_add(q,dd_d(q3));
}

static const dd C6PI2 = {0.6079271018540267, -2.379773927663665e-17};

static int64_t X;
static int32_t *sq;      /* sq[n] = #squarefree <= n */
static uint8_t *isq;     /* squarefree flag */
static uint32_t *spf;

static int64_t Nrec(int64_t Xv, const int64_t *pr, int k){
  if(Xv<=0) return 0;
  if(k==0) return sq[Xv];
  int64_t p=pr[k-1], s=0; int sign=1;
  for(int64_t t=Xv; t>=1; t/=p){ s+=sign*Nrec(t,pr,k-1); sign=-sign; }
  return s;
}

/* M_q = sum_{e|q'} mu(e) (q'/e) N(X/e, e) */
static int64_t compute_M(const int64_t *pr1, int n1, int64_t qp){
  int64_t M=0;
  for(int mask=0; mask<(1<<n1); mask++){
    int64_t e=1; int64_t sub[16]; int ns=0;
    for(int i=0;i<n1;i++) if(mask>>i&1){ e*=pr1[i]; sub[ns++]=pr1[i]; }
    int64_t term=(qp/e)*Nrec(X/e,sub,ns);
    if(ns&1) M-=term; else M+=term;
  }
  return M;
}

/* ---------- FFT autocorrelation: Cs[h] = #{n<=X-h : n, n+h squarefree}, and
   Hsum[q] needed lazily: T(q) = S + 2 sum_{j>=1} C(jq) ---------- */
static int64_t *Cauto=NULL;
static void fft(double *re, double *im, int64_t N, int inv, const double *cs, const double *sn){
  for(int64_t i=1,j=0;i<N;i++){
    int64_t bit=N>>1; for(; j&bit; bit>>=1) j^=bit; j^=bit;
    if(i<j){ double t=re[i];re[i]=re[j];re[j]=t; t=im[i];im[i]=im[j];im[j]=t; }
  }
  for(int64_t len=2; len<=N; len<<=1){
    int64_t half=len>>1, step=N/len;
    for(int64_t i=0;i<N;i+=len){
      for(int64_t j=0;j<half;j++){
        double wr=cs[j*step], wi=inv? sn[j*step] : -sn[j*step];
        double xr=re[i+j+half]*wr-im[i+j+half]*wi, xi=re[i+j+half]*wi+im[i+j+half]*wr;
        re[i+j+half]=re[i+j]-xr; im[i+j+half]=im[i+j]-xi;
        re[i+j]+=xr; im[i+j]+=xi;
      }
    }
  }
}
static double fft_maxdev=0;
static void build_autocorr(void){
  int64_t N=1; while(N<2*(X+1)) N<<=1;
  double *re=calloc(N,sizeof(double)), *im=calloc(N,sizeof(double));
  double *cs=malloc(N/2*sizeof(double)), *sn=malloc(N/2*sizeof(double));
  if(!re||!im||!cs||!sn){ fprintf(stderr,"oom fft\n"); exit(1); }
  for(int64_t j=0;j<N/2;j++){ long double a=2*3.14159265358979323846264338327950288L*j/N; cs[j]=cosl(a); sn[j]=sinl(a); }
  for(int64_t n=1;n<=X;n++) re[n]=isq[n];
  fft(re,im,N,0,cs,sn);
  for(int64_t i=0;i<N;i++){ re[i]=re[i]*re[i]+im[i]*im[i]; im[i]=0; }
  fft(re,im,N,1,cs,sn);
  Cauto=malloc((X+1)*sizeof(int64_t));
  for(int64_t h=0;h<=X;h++){
    double v=re[h]/N; double r=nearbyint(v); double d=fabs(v-r); if(d>fft_maxdev) fft_maxdev=d;
    Cauto[h]=(int64_t)r;
  }
  free(re);free(im);free(cs);free(sn);
}

static int32_t *cnt=NULL; static int64_t cnt_cap=0;
static int64_t T_direct(int64_t q, int64_t *Ssum){
  if(q>cnt_cap){ free(cnt); cnt=malloc(q*sizeof(int32_t)); cnt_cap=q; }
  memset(cnt,0,q*sizeof(int32_t));
  int64_t r=0;
  for(int64_t n=1;n<=X;n++){ if(++r==q) r=0; cnt[r]+=isq[n]; }
  int64_t T=0, S=0; for(int64_t i=0;i<q;i++){ T+=(int64_t)cnt[i]*cnt[i]; S+=cnt[i]; }
  *Ssum=S; return T;
}
static int64_t T_fft(int64_t q){
  int64_t T=sq[X];
  for(int64_t h=q; h<=X; h+=q) T+=2*Cauto[h];
  return T;
}

int main(int argc, char **argv){
  if(argc<6){ fprintf(stderr,"usage\n"); return 1; }
  int poly=atoi(argv[1]); X=atoll(argv[2]); int use_fft=!strcmp(argv[3],"fft"); int dump=atoi(argv[4]);
  int ny=argc-5; int64_t *ys=malloc(ny*sizeof(int64_t)); for(int i=0;i<ny;i++) ys[i]=atoll(argv[5+i]);
  int64_t ymax=0; for(int i=0;i<ny;i++) if(ys[i]>ymax) ymax=ys[i];
  spf=calloc(X+1,sizeof(uint32_t)); isq=malloc(X+1); sq=malloc((X+1)*sizeof(int32_t));
  for(int64_t i=2;i<=X;i++) if(!spf[i]) for(int64_t j=i;j<=X;j+=i) if(!spf[j]) spf[j]=i;
  memset(isq,1,X+1); isq[0]=0;
  for(int64_t p=2;p*p<=X;p++) if(spf[p]==p) for(int64_t j=p*p;j<=X;j+=p*p) isq[j]=0;
  sq[0]=0; for(int64_t n=1;n<=X;n++) sq[n]=sq[n-1]+isq[n];
  if(use_fft) build_autocorr();
  fprintf(stderr,"# fft_maxdev=%g\n",fft_maxdev);

  dd W={0,0}; int64_t kk=0;
  for(int64_t k=1;k<=ymax;k++){
    int64_t q,fp;
    if(poly==0){ q=k*k+1; fp=2*k; } else if(poly==1){ q=k*k*k+2; fp=3*k*k; } else { q=2*k+1; fp=2; }
    if(q>X){ fprintf(stderr,"f(%lld)=%lld > x\n",(long long)k,(long long)q); return 2; }
    int64_t T,Ssum=-1;
    if(use_fft) T=T_fft(q); else { T=T_direct(q,&Ssum); if(Ssum!=sq[X]){ fprintf(stderr,"SUM CHECK FAIL q=%lld\n",(long long)q); return 3; } }
    /* factor q */
    int64_t pr1[16]; int n1=0; dd Rn=dd_d(1), Rd=dd_d(1), S=dd_d(1); int64_t qp=1;
    int64_t m=q;
    while(m>1){
      int64_t p=spf[m]; int a=0; while(m%p==0){ m/=p; a++; }
      Rn=dd_mul(Rn,dd_d((double)p*(double)p)); Rd=dd_mul(Rd,dd_d((double)p*(double)p-1));
      if(a==1){
        pr1[n1++]=p; qp*=p;
        dd num=dd_mul(dd_d((double)(p-1)),dd_d((double)p*(double)p+(double)p-1));
        S=dd_mul(S,dd_div(num,dd_d((double)p*(double)p)));
      } else {
        double pa=1; for(int i=0;i<a;i++) pa*=p;
        S=dd_mul(S,dd_d(pa-pa/((double)p*(double)p)));
      }
    }
    int64_t M=compute_M(pr1,n1,qp);
    dd u=dd_mul(C6PI2,dd_d((double)X)); u=dd_mul(u,Rn); u=dd_div(u,dd_d((double)q)); u=dd_div(u,Rd);
    dd mf=dd_div(dd_d((double)M),dd_d((double)qp));
    dd V=dd_add(dd_d((double)T), dd_neg(dd_mul(dd_d(2.0),dd_mul(u,mf))));
    V=dd_add(V,dd_mul(dd_mul(u,u),S));
    if(dump) printf("K %lld %lld %lld %lld %lld %.17g %.17g\n",(long long)k,(long long)q,(long long)T,(long long)M,(long long)qp,V.h,V.l);
    W=dd_add(W,dd_mul(dd_d((double)fp),V));
    for(int i=0;i<ny;i++) if(ys[i]==k){ printf("Y %lld %lld %.17g %.17g\n",(long long)k,(long long)q,W.h,W.l); }
    kk=k;
  }
  (void)kk;
  return 0;
}
