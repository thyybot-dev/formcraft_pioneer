import numpy as np, json, copy, time, sys
Y0,Y1=2027,2072; years=np.arange(Y0,Y1+1); T=len(years)
V={
 'fc':dict(ramp=[0.046,0.135,0.324,0.625,1.03],start=2027,g1=0.30,n1=10,g2=0.20,p=1.0,age0=2,sd=0.45),
 'sk':dict(ramp=[0.05,0.25,0.8,1.8,3.5],start=2027,g1=0.35,n1=6,g2=0.15,p=0.7,age0=0,sd=0.7),
 'lgc':dict(ramp=[0.005,0.025,0.06,0.12],start=2027,g1=0.25,n1=6,g2=0.08,p=0.85,age0=0,sd=0.6),
 'lgt':dict(ramp=[0.02,0.12,0.4,1.0],start=2029,g1=0.40,n1=6,g2=0.15,p=0.30,age0=0,sd=0.9,req='lgc'),
 'ny':dict(ramp=[0.032,0.281,0.727],start=2028,g1=0.40,n1=6,g2=0.20,p=0.6,age0=0,sd=0.7),
 'ta':dict(ramp=[0.02,0.06,0.15],start=2029,g1=0.40,n1=6,g2=0.15,p=0.10,age0=0,sd=0.8),
}
def plan(v):
    r=np.zeros(T); x=None
    for t,y in enumerate(years):
        j=y-v['start']
        if j<0: continue
        if j<len(v['ramp']): x=v['ramp'][j]
        else:
            ya=j-len(v['ramp']); g=v['g1'] if ya<v['n1'] else (v['g2'] if ya<v['n1']+10 else 0.08); x*=1+g
        r[t]=x
    return r
def chunk(V,N,rng,hz=1.0,plateau=0.08,qmean=-0.05,shock_p=0.0,kill=False,factory=False,track=None,pg=0.06,lg=0.08):
    vs=list(V.values()); keys=list(V.keys())
    if factory:
        for y in (2032,2037,2042,2047,2052):
            vs.append(dict(ramp=[0.05,0.3,0.8,1.5],start=y,g1=0.30,n1=6,g2=0.12,p=0.6,age0=0,sd=0.7)); keys.append(f'new{y}')
    K=len(vs); P=[plan(v) for v in vs]
    live=np.stack([rng.random(N)<v['p'] for v in vs]).astype(bool)
    m=np.stack([np.exp(rng.normal(-v['sd']**2/2,v['sd'],N)) for v in vs]).astype(np.float32)
    q=rng.normal(qmean,0.08,(K,N)).astype(np.float32)
    r=np.zeros((K,N),np.float32); pl=np.zeros((K,N),bool); miss=np.zeros((K,N),np.int8)
    boost=np.zeros(N,np.float32); hzb=np.ones(N,np.float32)
    cum=np.zeros(N,np.float64); cross=np.zeros(N,np.int16)
    alive36=None; per36=None
    for t,y in enumerate(years):
        shock=rng.random(N)<shock_p if shock_p>0 else np.zeros(N,bool)
        tot=np.zeros(N,np.float64)
        for k,v in enumerate(vs):
            j=y-v['start']
            if j<0: continue
            if j==0 and 'req' in v: live[k]&=live[keys.index(v['req'])]
            age=v['age0']+j
            h=(0.16 if age<2 else 0.10 if age<5 else 0.07 if age<10 else 0.05)*hz*hzb+np.where(shock,0.08,0)
            die=rng.random(N)<h; live[k]&=~die
            if j<len(v['ramp']):
                r[k]=v['ramp'][j]*m[k]*np.where(shock,0.75,1.0)
            else:
                ya=j-len(v['ramp']); gm=v['g1'] if ya<v['n1'] else (v['g2'] if ya<v['n1']+10 else lg)
                pl[k]|=rng.random(N)<plateau
                g=np.where(pl[k],pg,gm)+q[k]+boost+rng.normal(0,0.15,N).astype(np.float32)-np.where(shock,0.25,0)
                r[k]*=1+np.maximum(g,-0.6)
            if kill and k<len(V):
                bad=live[k]&(r[k]<0.5*P[k][t]); miss[k]=np.where(bad,miss[k]+1,0)
                cut=(miss[k]>=2)&(age>=3)&live[k]
                live[k]&=~cut; boost+=0.03*cut; hzb*=np.where(cut,0.85,1.0)
            tot+=np.where(live[k],r[k],0)
        cum+=tot; newly=(cum>=1000)&(cross==0); cross[newly]=y
        if y==2036:
            alive36=live[:len(V)].sum(0); per36={keys[k]:(live[k].copy(),r[k].copy()) for k in range(len(vs))}
    return cum,cross,alive36,per36
def run(V,N=1_000_000,seed=7,chunk_n=250_000,**kw):
    rng=np.random.default_rng(seed); C=[];X=[];A=[]
    for s in range(0,N,chunk_n):
        c,x,a,_=chunk(V,min(chunk_n,N-s),rng,**kw); C.append(c);X.append(x);A.append(a)
    c=np.concatenate(C);x=np.concatenate(X);a=np.concatenate(A)
    p=lambda y: float(np.mean((x>0)&(x<=y)))
    se=lambda pp: float(np.sqrt(pp*(1-pp)/len(c)))
    return dict(N=len(c),p2047=p(2047),p2057=p(2057),p2072=p(2072),se2072=se(p(2072)),
        med=float(np.median(c)),p10=float(np.percentile(c,10)),p25=float(np.percentile(c,25)),p75=float(np.percentile(c,75)),p90=float(np.percentile(c,90)),p99=float(np.percentile(c,99)),
        bins=[float(np.mean((c>=lo)&(c<hi))) for lo,hi in ((0,1),(1,10),(10,100),(100,1000),(1000,1e15))],
        curve=[[int(y),round(p(y),5)] for y in range(2035,2073)],
        by_alive=[[n,float(np.mean(a==n)),float(np.mean(c[a==n]>=1000)) if np.any(a==n) else 0.0] for n in range(6)])
if __name__=='__main__':
    t=time.time(); r=run(V,N=200_000); print('200k',time.time()-t, r['p2072'], r['med'])
