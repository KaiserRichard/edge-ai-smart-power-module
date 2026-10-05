// Project-authored resistor mesh solver. Builds only in /tmp; no dependencies.
#include <vector>
#include <cmath>
#include <algorithm>
using namespace std;
extern "C" double solve(int n,int m,const int* ei,const int* ej,const double* g,const int* fixed,double* out,int maxit,double tol,int* iterations,double* residual){
 vector<double>d(n,0),b(n,0),x(n,0),r(n),z(n),p(n),ap(n);
 for(int e=0;e<m;e++){int i=ei[e],j=ej[e];d[i]+=g[e];d[j]+=g[e];if(!fixed[i]&&fixed[j]>0)b[i]+=g[e];if(!fixed[j]&&fixed[i]>0)b[j]+=g[e];}
 auto mv=[&](const vector<double>& a,vector<double>& c){for(int i=0;i<n;i++)c[i]=fixed[i]?a[i]:d[i]*a[i];for(int e=0;e<m;e++){int i=ei[e],j=ej[e];if(!fixed[i]&&!fixed[j]){c[i]-=g[e]*a[j];c[j]-=g[e]*a[i];}}};
 double rz=0,bnorm=0;for(int i=0;i<n;i++){r[i]=b[i];z[i]=d[i]>0?r[i]/d[i]:0;p[i]=z[i];rz+=r[i]*z[i];bnorm+=b[i]*b[i];}
 int it=0;double rr=bnorm;
 for(;it<maxit&&rr>tol*tol*bnorm;it++){
  mv(p,ap);double den=0;for(int i=0;i<n;i++)den+=p[i]*ap[i];if(den<=0)break;
  double alpha=rz/den;rr=0;for(int i=0;i<n;i++){x[i]+=alpha*p[i];r[i]-=alpha*ap[i];rr+=r[i]*r[i];z[i]=d[i]>0?r[i]/d[i]:0;}
  double rn=0;for(int i=0;i<n;i++)rn+=r[i]*z[i];double beta=rn/rz;for(int i=0;i<n;i++)p[i]=z[i]+beta*p[i];rz=rn;
 }
 for(int i=0;i<n;i++)out[i]=fixed[i]>0?1:fixed[i]<0?0:x[i];
 double current=0;for(int e=0;e<m;e++){int i=ei[e],j=ej[e];if(fixed[i]>0&&fixed[j]<=0)current+=g[e]*(1-out[j]);if(fixed[j]>0&&fixed[i]<=0)current+=g[e]*(1-out[i]);}
 *iterations=it;*residual=sqrt(rr/std::max(bnorm,1e-300));return current;
}
