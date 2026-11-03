#include <algorithm>
#include <array>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <vector>

using u32=uint32_t; using u64=uint64_t; using u128=__uint128_t;
constexpr u32 P=3221225473u, ROOT=5;
u32 power(u32 a,u32 b){u64 r=1;for(;b;b>>=1,a=u64(a)*a%P)if(b&1)r=r*a%P;return r;}
void ntt(std::vector<u32>& a,bool inv){
 size_t n=a.size();
 for(size_t i=1,j=0;i<n;i++){size_t bit=n>>1;for(;j&bit;bit>>=1)j^=bit;j^=bit;if(i<j)std::swap(a[i],a[j]);}
 for(size_t len=2;len<=n;len<<=1){u32 wl=power(ROOT,(P-1)/len);if(inv)wl=power(wl,P-2);
  for(size_t i=0;i<n;i+=len){u64 w=1;for(size_t j=0;j<len/2;j++){
   u32 u=a[i+j],v=w*a[i+j+len/2]%P;u64 s=u64(u)+v;
   a[i+j]=s>=P?s-P:s;a[i+j+len/2]=u>=v?u-v:u64(u)+P-v;w=w*wl%P;
  }}
 }
 if(inv){u32 ni=power(n,P-2);for(auto& v:a)v=u64(v)*ni%P;}
}
void put128(std::array<u64,9>& r,int i,u128 n){r[i]=u64(n);r[i+1]=u64(n>>64);}
int main(int argc,char**argv){
 if(argc!=2&&argc!=3)return 2;u32 x=std::strtoul(argv[1],nullptr,10);assert(x< P);
 u32 cap=argc==3?std::strtoul(argv[2],nullptr,10):x;assert(cap<=x);
 size_t nn=1;while(nn<2ull*x+1)nn*=2;assert(nn<=(1ull<<30));
 std::vector<u32> spf(cap+1);std::vector<uint8_t> sf(x+1,1);sf[0]=0;
 for(u32 p=2;p<=cap;p++)if(!spf[p]){
  spf[p]=p;if(u64(p)*p<=cap)for(u64 n=u64(p)*p;n<=cap;n+=p)if(!spf[n])spf[n]=p;
 }
 for(u64 d=2;d*d<=x;d++)for(u64 n=d*d;n<=x;n+=d*d)sf[n]=0;
 std::vector<u32> a(nn);u64 total=0;for(u32 n=1;n<=x;n++){a[n]=sf[n];total+=sf[n];}
 std::fprintf(stderr,"x=%u NTT length=%zu squarefree=%llu\n",x,nn,(unsigned long long)total);
 ntt(a,false);
 for(size_t i=1;i<nn/2;i++){u32 v=u64(a[i])*a[nn-i]%P;a[i]=a[nn-i]=v;}
 a[0]=u64(a[0])*a[0]%P;a[nn/2]=u64(a[nn/2])*a[nn/2]%P;ntt(a,true);
 assert(a[0]==total);
 for(u32 h:std::array<u32,7>{1,2,7,31,x/3,x/2,x-1})if(h<=x){u32 check=0;for(u32 n=1;n+h<=x;n++)check+=sf[n]*sf[n+h];assert(a[h]==check);}
 std::vector<u32> sd(cap+1);
 for(u32 d=1;d<=cap;d++)if(sf[d]){u32 s=0;for(u32 n=d;n<=x;n+=d)s+=sf[n];sd[d]=s;}
 std::fprintf(stderr,"x=%u correlations and squarefree-divisibility counts ready\n",x);
 for(int poly=0;poly<3;poly++)for(u64 k=1;;k++){
  u64 q=poly==0?k*k+1:poly==1?k*k*k+2:2*k+1;
  u64 weight=poly==0?2*k:poly==1?3*k*k:2;if(q>cap)break;
  u64 s2=total;for(u64 h=q;h<=x;h+=q)s2+=2ull*a[h];
  u32 m=q;u128 an=1,ad=1,dn=1,dd=q;u64 rad1=1;
  std::vector<u32> singles;
  while(m>1){u32 p=spf[m],e=0;while(m%p==0){m/=p;e++;}
   an*=u64(p)*p;ad*=u64(p)*p-1;
   if(e==1){singles.push_back(p);rad1*=p;dn*=u128(p)*(u64(p)*p+p-1);dd*=u128(p-1)*(p+1)*(p+1);}
   else{dn*=u64(p)*p;dd*=u64(p)*p-1;}
  }
  // Integral numerator of sum_{d|rad1} mu(d) S_d / d.
  __int128 t=0;size_t subsets=1ull<<singles.size();
  for(size_t mask=0;mask<subsets;mask++){u64 d=1;int sign=1;for(size_t i=0;i<singles.size();i++)if(mask>>i&1){d*=singles[i];sign=-sign;}
   t+=__int128(sign)*sd[d]*(rad1/d);
  }
  assert(t>=0);std::array<u64,9> rec;
  assert((u128(rad1)*q)%an==0);
  rec[0]=s2*weight;put128(rec,1,u128(t)*weight);put128(rec,3,(u128(rad1)*q/an)*ad);
  put128(rec,5,dn*weight);put128(rec,7,dd);
  if(std::fwrite(rec.data(),sizeof(u64),rec.size(),stdout)!=rec.size())return 3;
 }
 std::fprintf(stderr,"x=%u completed exact coefficient stream\n",x);
}
