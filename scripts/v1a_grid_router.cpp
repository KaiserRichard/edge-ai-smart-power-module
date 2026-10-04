// Project-authored signal maze router; power geometry is specified in Python.
// Build to /tmp only: clang++ -O3 -std=c++17 -dynamiclib ... -o /tmp/v1a-router.dylib
#include <vector>
#include <queue>
#include <cmath>
#include <algorithm>
#include <cstdint>
#include <cstdio>
using namespace std;
static int W,H,N;static double S,X0,Y0;
static vector<int16_t> occ,viaocc;
static vector<int> distv,prevv,stamp;static int serial=0;
static inline int id(int x,int y,int z){return (z*H+y)*W+x;}
static inline void writecell(vector<int16_t>& a,int i,int n){if(a[i]==0||a[i]==n)a[i]=n;else a[i]=-1;}
extern "C" {
void init(int w,int h,double s,double x,double y){W=w;H=h;N=W*H;S=s;X0=x;Y0=y;occ.assign(3*N,0);viaocc.assign(3*N,0);distv.resize(3*N);prevv.resize(3*N);stamp.assign(3*N,0);}
void capsule(int z,int net,double ax,double ay,double bx,double by,double rad,int via){
 auto &a=via?viaocc:occ;
 int x1=max(0,(int)floor((min(ax,bx)-rad-X0)/S)),x2=min(W-1,(int)ceil((max(ax,bx)+rad-X0)/S));
 int y1=max(0,(int)floor((min(ay,by)-rad-Y0)/S)),y2=min(H-1,(int)ceil((max(ay,by)+rad-Y0)/S));
 double dx=bx-ax,dy=by-ay,len=dx*dx+dy*dy;
 for(int y=y1;y<=y2;y++)for(int x=x1;x<=x2;x++){double px=X0+x*S,py=Y0+y*S;double t=len?clamp(((px-ax)*dx+(py-ay)*dy)/len,0.,1.):0;double ex=px-ax-t*dx,ey=py-ay-t*dy;if(ex*ex+ey*ey<=rad*rad)writecell(a,id(x,y,z),net);}
}
void polygon(int z,int net,double*pts,int cnt,double rad,int via){
 auto &a=via?viaocc:occ;double minx=1e9,miny=1e9,maxx=-1e9,maxy=-1e9;
 for(int i=0;i<cnt;i++){minx=min(minx,pts[2*i]);maxx=max(maxx,pts[2*i]);miny=min(miny,pts[2*i+1]);maxy=max(maxy,pts[2*i+1]);}
 int x1=max(0,(int)floor((minx-rad-X0)/S)),x2=min(W-1,(int)ceil((maxx+rad-X0)/S));
 int y1=max(0,(int)floor((miny-rad-Y0)/S)),y2=min(H-1,(int)ceil((maxy+rad-Y0)/S));
 for(int y=y1;y<=y2;y++)for(int x=x1;x<=x2;x++){
 double px=X0+x*S,py=Y0+y*S;bool in=false,near=false;
 for(int i=0,j=cnt-1;i<cnt;j=i++){
 double ax=pts[2*i],ay=pts[2*i+1],bx=pts[2*j],by=pts[2*j+1];
 if(((ay>py)!=(by>py))&&(px<(bx-ax)*(py-ay)/(by-ay)+ax))in=!in;
 double dx=bx-ax,dy=by-ay,len=dx*dx+dy*dy,t=len?clamp(((px-ax)*dx+(py-ay)*dy)/len,0.,1.):0;double ex=px-ax-t*dx,ey=py-ay-t*dy;
 if(ex*ex+ey*ey<=rad*rad)near=true;
 }if(in||near)writecell(a,id(x,y,z),net);
 }
}
int freecell(int x,int y,int z,int net,int isvia){
 if(x<0||x>=W||y<0||y>=H)return 0;
 if(isvia){for(int l=0;l<3;l++){int c=viaocc[id(x,y,l)];if(c!=0&&c!=net)return 0;}return 1;}
 int c=occ[id(x,y,z)];return c==0||c==net;
}
struct Node{int i,g,f;bool operator<(Node const&o)const{return f>o.f;}};
int route(int sx,int sy,int sz,int tx,int ty,int tz,int net,int allowvia,int *out,int maxout,int limit){
 if(!freecell(sx,sy,sz,net,0)||!freecell(tx,ty,tz,net,0))return -1;
 serial++;priority_queue<Node>q;
 int src=id(sx,sy,sz),dst=id(tx,ty,tz),nvisit=0;
 auto heur=[&](int x,int y,int z){int dx=abs(x-tx),dy=abs(y-ty);return 10*max(dx,dy)+4*min(dx,dy)+(z==tz?0:120);};
 q.push({src,0,heur(sx,sy,sz)});distv[src]=0;prevv[src]=-1;stamp[src]=serial;
 const int dxs[8]={1,-1,0,0,1,1,-1,-1},dys[8]={0,0,1,-1,1,-1,1,-1};
 while(!q.empty()){
  Node cur=q.top();q.pop();if(cur.g!=distv[cur.i])continue;
  if(++nvisit>limit)return -2;
  if(cur.i==dst){vector<int>path;for(int i=dst;i>=0;i=prevv[i])path.push_back(i);if((int)path.size()>maxout)return -3;reverse(path.begin(),path.end());for(int j=0;j<(int)path.size();j++){int i=path[j];out[3*j]=i%W;out[3*j+1]=(i/W)%H;out[3*j+2]=i/N;}return path.size();}
  int x=cur.i%W,y=(cur.i/W)%H,z=cur.i/N;
  auto relax=[&](int xx,int yy,int zz,int cost){int ii=id(xx,yy,zz),ng=cur.g+cost;if(stamp[ii]!=serial||ng<distv[ii]){distv[ii]=ng;prevv[ii]=cur.i;stamp[ii]=serial;q.push({ii,ng,ng+heur(xx,yy,zz)});}};
  for(int d=0;d<8;d++){int xx=x+dxs[d],yy=y+dys[d];if(!freecell(xx,yy,z,net,0))continue;if(d>=4&&(!freecell(xx,y,z,net,0)||!freecell(x,yy,z,net,0)))continue;relax(xx,yy,z,d<4?10:14);}
  if(allowvia&&freecell(x,y,z,net,1))for(int zz=0;zz<3;zz++)if(zz!=z)relax(x,y,zz,120);
 }
 return 0;
}
}
