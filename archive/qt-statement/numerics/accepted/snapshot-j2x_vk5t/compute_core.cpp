#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>
using namespace std;
// Double-double: about 31 decimal digits, with error-free binary64 transforms.
struct DD {
 double hi,lo;
 DD(double h=0,double l=0):hi(h),lo(l){}
};
DD add(DD a,DD b){ double s=a.hi+b.hi,v=s-a.hi; double e=(a.hi-(s-v))+(b.hi-v)+a.lo+b.lo;double h=s+e;return DD(h,e-(h-s)); }
DD neg(DD a){return DD(-a.hi,-a.lo);}
DD sub(DD a,DD b){return add(a,neg(b));}
DD mul(DD a,DD b){double p=a.hi*b.hi;double e=fma(a.hi,b.hi,-p)+a.hi*b.lo+a.lo*b.hi+a.lo*b.lo;double h=p+e;return DD(h,e-(h-p));}
DD divdd(DD a,DD b){double q=a.hi/b.hi;DD r=sub(a,mul(b,DD(q)));double q2=(r.hi+r.lo)/b.hi;return add(DD(q),DD(q2));}
#ifndef NTT_MOD
#define NTT_MOD 3221225473U
#define NTT_ROOT 5
#endif
constexpr uint32_t MOD=NTT_MOD, ROOT=NTT_ROOT;
uint32_t modpow(uint32_t a,uint32_t e){uint64_t r=1;for(;e;e>>=1,a=uint64_t(a)*a%MOD)if(e&1)r=r*a%MOD;return r;}
void ntt(vector<uint32_t>& a,bool inv){
 size_t n=a.size();
 for(size_t i=1,j=0;i<n;i++){size_t b=n>>1;for(;j&b;b>>=1)j^=b;j^=b;if(i<j)swap(a[i],a[j]);}
 for(size_t len=2;len<=n;len<<=1){uint32_t wl=modpow(ROOT,(MOD-1)/len);if(inv)wl=modpow(wl,MOD-2);
  for(size_t i=0;i<n;i+=len){uint64_t w=1;for(size_t j=0;j<len/2;j++){
   uint32_t u=a[i+j],v=w*a[i+j+len/2]%MOD;
   uint64_t s=uint64_t(u)+v;a[i+j]=s>=MOD?s-MOD:s;
   a[i+j+len/2]=u>=v?u-v:uint64_t(u)+MOD-v;w=w*wl%MOD;
  }}
 }
 if(inv){uint64_t ni=modpow(n,MOD-2);for(auto& v:a)v=v*ni%MOD;}
}
uint64_t fv(int t,uint64_t k){if(t==0)return k*k+1;if(t==1)return k*k*k+2;return 2*k+1;}
uint64_t weight(int t,uint64_t k){if(t==0)return 2*k;if(t==1)return 3*k*k;return 2;}
struct State{uint64_t A=0;DD B,D;};
int main(int argc,char**argv){
 if(argc!=4){cerr<<"usage: core X output.csv validation_limit\n";return 1;}
 int x=stoi(argv[1]),validate=stoi(argv[3]);string out=argv[2];
 if(uint64_t(x)>=MOD||x>536870911){cerr<<"X exceeds exact transform range\n";return 1;}
 auto start=chrono::steady_clock::now();
 vector<uint32_t> spf(x+1);vector<uint8_t> sq(x+1,1);sq[0]=0;
 for(int p=2;p<=x;p++)if(!spf[p]){spf[p]=p;if(int64_t(p)*p<=x){for(int64_t n=int64_t(p)*p;n<=x;n+=p)if(!spf[n])spf[n]=p;for(int64_t n=int64_t(p)*p;n<=x;n+=int64_t(p)*p)sq[n]=0;}}
 uint32_t total=0;for(int n=1;n<=x;n++)total+=sq[n];
 size_t nn=1;while(nn<size_t(2*x+1))nn<<=1;if((MOD-1)%nn){cerr<<"Unsupported NTT length for prime\n";return 1;}vector<uint32_t>a(nn);
 for(int n=1;n<=x;n++)a[n]=sq[n];
 cerr<<"x="<<x<<" NTT length="<<nn<<" squarefree="<<total<<"\n";
 ntt(a,false);a[0]=uint64_t(a[0])*a[0]%MOD;
 for(size_t j=1;j<nn/2;j++){uint32_t v=uint64_t(a[j])*a[nn-j]%MOD;a[j]=a[nn-j]=v;}
 a[nn/2]=uint64_t(a[nn/2])*a[nn/2]%MOD;ntt(a,true);
 if(a[0]!=total){cerr<<"NTT zero-lag failure\n";return 2;}
 for(int h=1;h<x;h++)if(a[h]>uint32_t(x-h)){cerr<<"correlation bound failure\n";return 2;}
 vector<uint32_t> S(x+1);
 for(int d=1;d<=x;d++)if(sq[d]){uint32_t v=0;for(int n=d;n<=x;n+=d)v+=sq[n];S[d]=v;}
 ofstream file(out);file<<setprecision(17)<<"type,x,k,q,weight,S2,B_hi,B_lo,D_hi,D_lo,A_cum,B_cum_hi,B_cum_lo,D_cum_hi,D_cum_lo\n";
 vector<uint64_t> checkpoints[3];
 int numerators[8]={1,2,5,10,20,40,70,100};
 for(int t=0;t<3;t++)for(int r:numerators){uint64_t target=uint64_t(x)*r/100,k=0;while(fv(t,k+1)<=target)k++;if(k)checkpoints[t].push_back(k);}
 // No floating point in any counting stage.
 uint64_t nextk[3]={1,1,1};State states[3];
 for(int q=2;q<=x;q++){
  bool use[3];bool any=false;for(int t=0;t<3;t++){use[t]=fv(t,nextk[t])==uint64_t(q);any|=use[t];}
  if(!any && q>validate)continue;
  uint64_t s2=total;for(int h=q;h<x;h+=q)s2+=2ULL*a[h];
  int rem=q;vector<int>single;DD H(1),local(1);
  while(rem>1){int p=spf[rem],e=0;while(rem%p==0){rem/=p;e++;}
   DD pp=mul(DD(p),DD(p));
   H=mul(H,divdd(pp,sub(pp,DD(1))));
   if(e==1){single.push_back(p);local=mul(local,add(sub(DD(1),divdd(DD(2),pp)),divdd(DD(1),mul(pp,DD(p)))));}
   else local=mul(local,sub(DD(1),divdd(DD(1),pp)));
  }
  vector<pair<int,int>> ds={{1,1}};for(int p:single){int n=ds.size();for(int j=0;j<n;j++)ds.push_back({ds[j].first*p,-ds[j].second});}
  DD T;for(auto [d,sign]:ds)T=add(T,divdd(DD(double(sign)*S[d]),DD(d)));
  DD B=divdd(mul(H,T),DD(q)),D=divdd(mul(mul(H,H),local),DD(q));
  if(q<=validate){
   vector<uint32_t> counts(q);for(int n=1;n<=x;n++)if(sq[n])counts[n%q]++;
   uint64_t bs2=0,bs=0;for(auto c:counts){bs2+=uint64_t(c)*c;bs+=c;}
   if(bs!=total||bs2!=s2){cerr<<"brute-force count failure q="<<q<<"\n";return 2;}
   DD directB,directD;
   for(int l=0;l<q;l++){
    int r=q;DD fac=H;bool zero=false;
    while(r>1){int p=spf[r],e=0;while(r%p==0){r/=p;e++;}
     if(e>=2&&l%(p*p)==0){zero=true;break;}
     if(e==1&&l%p==0)fac=mul(fac,divdd(DD(p-1),DD(p)));
    }
    if(zero)fac=DD();fac=divdd(fac,DD(q));
    directB=add(directB,mul(DD(counts[l]),fac));directD=add(directD,mul(fac,fac));
   }
   if(abs(sub(directB,B).hi)>1e-23*max(1.,abs(B.hi))||abs(sub(directD,D).hi)>1e-23){cerr<<"density aggregation failure q="<<q<<"\n";return 2;}
  }
  for(int t=0;t<3;t++)if(use[t]){
   uint64_t k=nextk[t]++,w=weight(t,k);auto& st=states[t];st.A+=w*s2;st.B=add(st.B,mul(DD(w),B));st.D=add(st.D,mul(DD(w),D));
   if(x<=1000||find(checkpoints[t].begin(),checkpoints[t].end(),k)!=checkpoints[t].end())file<<t<<','<<x<<','<<k<<','<<q<<','<<w<<','<<s2<<','<<B.hi<<','<<B.lo<<','<<D.hi<<','<<D.lo<<','<<st.A<<','<<st.B.hi<<','<<st.B.lo<<','<<st.D.hi<<','<<st.D.lo<<'\n';
  }
 }
 cerr<<"finished x="<<x<<" seconds="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<" brute_checked_q="<<min(x,validate)<<"\n";
}
