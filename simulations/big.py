from vec import *
import sys
seed=int(sys.argv[1]); N=int(sys.argv[2])
rng=np.random.default_rng(seed); hits=np.zeros(4,np.int64); n=0; meds=[]
cnt=np.zeros(5,np.int64)
for s in range(0,N,500_000):
    c,x,a,_=chunk(V,500_000,rng)
    for i,y in enumerate((2047,2052,2057,2072)): hits[i]+=np.sum((x>0)&(x<=y))
    cnt+=np.array([np.sum((c>=lo)&(c<hi)) for lo,hi in ((0,1),(1,10),(10,100),(100,1000),(1000,1e15))])
    meds.append(np.median(c)); n+=len(c)
json.dump(dict(n=n,hits=hits.tolist(),cnt=cnt.tolist(),med=float(np.median(meds))),open(f'big_{seed}.json','w'))
