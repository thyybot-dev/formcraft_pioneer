import numpy as np, json, itertools, copy
Y0,Y1=2027,2072; years=np.arange(Y0,Y1+1); T=len(years)
V={
 'fc':dict(name='Formcraft',ramp=[0.046,0.135,0.324,0.625,1.03],start=2027,g1=0.30,n1=10,g2=0.20,p=1.0,age0=2,sd=0.45),
 'sk':dict(name='Soko Foods',ramp=[0.05,0.25,0.8,1.8,3.5],start=2027,g1=0.35,n1=6,g2=0.15,p=0.7,age0=0,sd=0.7),
 'lg':dict(name='Logistics',ramp=[0.08,0.4,1.0,2.0],start=2028,g1=0.30,n1=6,g2=0.12,p=0.6,age0=0,sd=0.7),
 'ny':dict(name='Nyumba',ramp=[0.032,0.281,0.727],start=2028,g1=0.40,n1=6,g2=0.20,p=0.6,age0=0,sd=0.7),
 'ta':dict(name='Trade Assistant',ramp=[0.02,0.06,0.15],start=2029,g1=0.40,n1=6,g2=0.15,p=0.10,age0=0,sd=0.8),
}
def plan_path(v):
    r={};y=v['start'];
    for x in v['ramp']: r[y]=x;y+=1
    x=v['ramp'][-1];k=0
    while y<=Y1:
        g=v['g1'] if k<v['n1'] else (v['g2'] if k<v['n1']+10 else 0.08); x*=1+g; r[y]=x; y+=1; k+=1
    return np.array([r.get(int(t),0) for t in years])
P={k:plan_path(v) for k,v in V.items()}
def cross(arr):
    c=np.cumsum(arr); i=np.argmax(c>=1000); return int(years[i]) if c[-1]>=1000 else None
# --- deterministic combos
combos={}
for n in range(1,6):
    res=[]
    for s in itertools.combinations(V,n):
        res.append((cross(sum(P[k] for k in s)),s))
    ok=[r for r in res if r[0]]; 
    combos[n]={'best':min(ok)[0] if ok else None,'best_set':[V[k]['name'] for k in min(ok)[1]] if ok else None,
               'worst':max(ok)[0] if len(ok)==len(res) else None,'n_never':len(res)-len(ok),'n':len(res),
               'median':sorted([r[0] or 2100 for r in res])[len(res)//2]}
    print(n,combos[n])
print('all5 cross',cross(sum(P.values())), {k:cross(P[k]) for k in P})
# --- goal seek: required combined path to cross by 2047 and by 2057 (constant growth after 2031 from plan 2031 level)
r31=sum(P[k][2031-Y0] for k in P); cum30=sum(P[k][:2031-Y0].sum() for k in P)
def req_g(target_year):
    lo,hi=0,2
    for _ in range(60):
        g=(lo+hi)/2; c=cum30; x=r31
        for y in range(2031,target_year+1): c+=x; x*=1+g
        if c>=1000: hi=g
        else: lo=g
    return hi
goal={}
for ty in (2047,2052,2057):
    g=req_g(ty); path={y: round(r31*(1+g)**(y-2031),2) for y in (2031,2036,2041,2046,2051,2056) if y<=ty}
    goal[ty]={'g':round(g,3),'path':path}
print('r31',r31,'goal',goal)
# --- Monte Carlo engine
def run(V,N=8000,seed=1,hz=1.0,plateau=0.08,qmean=-0.05,shock_p=0.0,kill=False,factory=False):
    rng=np.random.default_rng(seed); tot=np.zeros((N,T)); per={k:np.zeros((N,T)) for k in V}
    Vl=list(V.items())
    for i in range(N):
        shocks=rng.random(T)<shock_p
        state={}
        for k,v in Vl:
            state[k]=dict(live=rng.random()<v['p'],r=None,pl=False,q=rng.normal(qmean,0.08),m=np.exp(rng.normal(-v['sd']**2/2,v['sd'])),miss=0,v=v)
        boost=0.0; hzb=1.0; newv=[]
        for t,y in enumerate(years):
            if factory and y in (2032,2037,2042,2047,2052) :
                newv.append(dict(live=rng.random()<0.6,r=None,pl=False,q=rng.normal(qmean,0.08),m=np.exp(rng.normal(-0.245,0.7)),miss=0,
                    v=dict(ramp=[0.05,0.3,0.8,1.5],start=y,g1=0.30,n1=6,g2=0.12,age0=0)))
            items=list(state.items())+[(f'n{j}',s) for j,s in enumerate(newv)]
            for k,s in items:
                v=s['v']
                if not s['live'] or y<v['start']: continue
                age=v['age0']+(y-v['start'])
                h=(0.16 if age<2 else 0.10 if age<5 else 0.07 if age<10 else 0.05)*hz*hzb
                if shocks[t]: h+=0.08
                if rng.random()<h: s['live']=False; continue
                j=y-v['start']
                if j<len(v['ramp']): s['r']=v['ramp'][j]*s['m']*(0.75 if shocks[t] else 1)
                else:
                    ya=j-len(v['ramp']); gm=v['g1'] if ya<v['n1'] else v['g2']
                    if ya>=v['n1']+10: gm=0.08
                    if not s['pl'] and rng.random()<plateau: s['pl']=True
                    if s['pl']: gm=0.06
                    g=gm+s['q']+boost+rng.normal(0,0.15)-(0.25 if shocks[t] else 0)
                    s['r']*=1+max(g,-0.6)
                # kill rule: compare with plan
                if kill and k in P:
                    planv=P[k][t]
                    s['miss']=s['miss']+1 if s['r']<0.5*planv else 0
                    if s['miss']>=2 and age>=3:
                        s['live']=False; boost+=0.03; hzb*=0.85; continue
                tot[i,t]+=s['r']
                if k in per: per[k][i,t]=s['r']
    return tot,per
def stats(tot):
    c=np.cumsum(tot,axis=1)
    def p(y): return float(np.mean(c[:,y-Y0]>=1000))
    return dict(p2047=p(2047),p2057=p(2057),p2072=p(2072),med=float(np.median(c[:,-1])),p10=float(np.percentile(c[:,-1],10)),p90=float(np.percentile(c[:,-1],90)),
                curve=[[int(y),round(p(y),4)] for y in years if y>=2035])
out={'combos':combos,'goal':goal,'r31':r31}
tot,per=run(V,N=10000,seed=20261029)
out['mc']=stats(tot); print('MC',{k:v for k,v in out['mc'].items() if k!='curve'})
c=np.cumsum(tot,axis=1)[:,-1]; bins=[0,1,10,100,1000,1e12]
out['bins']=[round(float(np.mean((c>=bins[i])&(c<bins[i+1]))),3) for i in range(5)]
# how many ventures alive in 2036 vs success
alive=sum((per[k][:,2036-Y0]>0).astype(int) for k in per)
cc=np.cumsum(tot,axis=1)[:,-1]
out['by_alive']=[[n,round(float(np.mean(alive==n)),3),round(float(np.mean(cc[alive==n]>=1000)) if np.any(alive==n) else 0,3)] for n in range(6)]
print('by alive',out['by_alive'],out['bins'])
out['surv']={k:[round(float(np.mean(per[k][:,y-Y0]>0)),3) for y in range(2027,2048)] for k in per}
out['cond']={}
for k in per:
    d={}
    for y in (2031,2036):
        a=per[k][:,y-Y0]; a=a[a>0]; d[y]=[round(float(np.percentile(a,q)),2) for q in (10,50,90)]
    out['cond'][k]=d
print(out['cond'])
json.dump(out,open('sim5.json','w'))
