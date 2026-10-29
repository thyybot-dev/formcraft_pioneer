exec(open('v3.py').read().split("S={")[0])
def track(V,N,rng,hz,qmean,plateau,pg,lg):
    vs=list(V.values()); keys=list(V.keys()); K=len(vs)
    live=np.stack([rng.random(N)<v['p'] for v in vs]); m=np.stack([np.exp(rng.normal(-v['sd']**2/2,v['sd'],N)) for v in vs]).astype(np.float32)
    q=rng.normal(qmean,0.08,(K,N)).astype(np.float32); r=np.zeros((K,N),np.float32); pl=np.zeros((K,N),bool)
    alive={}; rec={}; cum=np.zeros((K,N))
    for t,y in enumerate(years):
        for k,v in enumerate(vs):
            j=y-v['start']
            if j<0: continue
            if j==0 and 'req' in v: live[k]&=live[keys.index(v['req'])]
            age=v['age0']+j; h=(0.16 if age<2 else 0.10 if age<5 else 0.07 if age<10 else 0.05)*hz
            live[k]&=~(rng.random(N)<h)
            if j<len(v['ramp']): r[k]=v['ramp'][j]*m[k]
            else:
                ya=j-len(v['ramp']); gm=v['g1'] if ya<v['n1'] else (v['g2'] if ya<v['n1']+10 else lg)
                pl[k]|=rng.random(N)<plateau; r[k]*=1+np.maximum(np.where(pl[k],pg,gm)+q[k]+rng.normal(0,0.15,N).astype(np.float32),-0.6)
            cum[k]+=np.where(live[k],r[k],0)
        alive[y]=live & np.array([[y>=v['start']] for v in vs])
        if y in (2031,2036,2041): rec[y]=np.where(live,r,0).copy()
    return keys,alive,rec,cum
c=B; keys,alive,rec,cum=track(c['V'],400_000,np.random.default_rng(5),c['hz'],c['qmean'],c['plateau'],c['pg'],c['lg'])
ki={k:i for i,k in enumerate(keys)}
G={'fc':['fc'],'sk':['sk','ski','skf','skp','sks'],'lg':['lgc','lgt'],'ny':['ny'],'ta':['ta'],'yt':['yt']}
out={}
for g,ks in G.items():
    idx=[ki[k] for k in ks]
    surv=[round(float(np.mean(np.any(alive[y][idx],axis=0))),3) for y in range(2027,2048)]
    d={}
    for y in (2031,2036,2041):
        a=rec[y][idx].sum(0); a=a[a>0]; d[y]=[round(float(np.percentile(a,p)),3) for p in (10,50,90)]
    cu=cum[idx].sum(0)
    out[g]=dict(surv=surv,cond=d,cum=[round(float(np.percentile(cu,p)),2) for p in (50,90,99)],p100=float(np.mean(cu>=100)),p1b=float(np.mean(cu>=1000)))
    print(g,surv[9],d,out[g]['cum'],round(out[g]['p100'],3),round(out[g]['p1b'],3))
# plan totals, goal-seek, combos
P={k:plan(v) for k,v in V3.items()}
PG={'Formcraft':P['fc'],'Soko Foods':sum(P[k] for k in G['sk']),'Logistics':P['lgc']+P['lgt'],'Nyumba':P['ny'],'Trade Assistant':P['ta'],'YouTube':P['yt']}
tot=sum(PG.values()); print('r31',round(tot[4],2),'plan cross',2027+int(np.argmax(np.cumsum(tot)>=1000)))
print({k:round(v[4],2) for k,v in PG.items()})
r31=tot[4]; cum30=tot[:4].sum()
def req(ty):
    lo,hi=0,2
    for _ in range(60):
        g=(lo+hi)/2; cc=cum30; x=r31
        for y in range(2031,ty+1): cc+=x; x*=1+g
        lo,hi=(lo,g) if cc>=1000 else (g,hi)
    return hi
goal={ty:round(req(ty),3) for ty in (2042,2047,2052)}; print('goal',goal)
g=goal[2047]; print([(y,round(r31*(1+g)**(y-2031),1)) for y in (2031,2034,2037,2040,2043,2046)])
def cross(a):
    cc=np.cumsum(a); return int(years[np.argmax(cc>=1000)]) if cc[-1]>=1000 else None
V5={k:v for k,v in PG.items() if k!='YouTube'}
comb={}
for n in range(1,6):
    res=[(cross(sum(V5[k] for k in s)+PG['YouTube']),s) for s in itertools.combinations(V5,n)]
    ok=sorted([r for r in res if r[0]]); allv=sorted([r[0] or 2100 for r in res])
    comb[n]=dict(best=ok[0][0] if ok else None,best_set=list(ok[0][1]) if ok else None,median=allv[len(allv)//2],worst=max(allv))
    print(n,comb[n])
print({k:cross(v+PG['YouTube']) for k,v in V5.items()})
json.dump(dict(groups=out,goal=goal,r31=float(r31),comb=comb,plan31={k:float(v[4]) for k,v in PG.items()}),open('v3detail.json','w'))
