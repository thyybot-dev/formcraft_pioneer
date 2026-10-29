exec(open('vec2.py').read().split("if __name__")[0])
import itertools
rng=np.random.default_rng(11); N=1_000_000
# per-venture tracking: replicate chunk but record yearly revenue per venture for key years
def track(V,N,rng):
    vs=list(V.values()); keys=list(V.keys()); K=len(vs)
    live=np.stack([rng.random(N)<v['p'] for v in vs]); m=np.stack([np.exp(rng.normal(-v['sd']**2/2,v['sd'],N)) for v in vs]).astype(np.float32)
    q=rng.normal(-0.05,0.08,(K,N)).astype(np.float32); r=np.zeros((K,N),np.float32); pl=np.zeros((K,N),bool)
    rec={}; alive={}
    for t,y in enumerate(years):
        for k,v in enumerate(vs):
            j=y-v['start']
            if j<0: continue
            if j==0 and 'req' in v: live[k]&=live[keys.index(v['req'])]
            age=v['age0']+j; h=(0.16 if age<2 else 0.10 if age<5 else 0.07 if age<10 else 0.05)
            live[k]&=~(rng.random(N)<h)
            if j<len(v['ramp']): r[k]=v['ramp'][j]*m[k]
            else:
                ya=j-len(v['ramp']); gm=v['g1'] if ya<v['n1'] else (v['g2'] if ya<v['n1']+10 else 0.08)
                pl[k]|=rng.random(N)<0.08; r[k]*=1+np.maximum(np.where(pl[k],0.06,gm)+q[k]+rng.normal(0,0.15,N).astype(np.float32),-0.6)
        if y<=2047: alive[y]=live & np.array([[y>=v['start']] for v in vs])
        if y in (2031,2036): rec[y]=np.where(live,r,0).copy()
    return keys,rec,alive
keys,rec,alive=track(V,N,rng)
out={}
ki={k:i for i,k in enumerate(keys)}
def venture_rows(name,idx):
    s=[round(float(np.mean(np.any(alive[y][idx],axis=0))),3) for y in range(2027,2048)]
    d={}
    for y in (2031,2036):
        a=rec[y][idx].sum(0); a=a[a>0]; d[y]=[round(float(np.percentile(a,p)),2) for p in (10,50,90)]
    return s,d
groups={'fc':['fc'],'sk':['sk'],'lg':['lgc','lgt'],'ny':['ny'],'ta':['ta'],'lgc':['lgc'],'lgt':['lgt']}
for g,ks in groups.items():
    s,d=venture_rows(g,[ki[k] for k in ks]); out[g]={'surv':s,'cond':d}; print(g,s[4],s[9],s[20],d)
# combos deterministic with logistics as one
P={k:plan(v) for k,v in V.items()}; PG={'Formcraft':P['fc'],'Soko Foods':P['sk'],'Logistics':P['lgc']+P['lgt'],'Nyumba':P['ny'],'Trade Assistant':P['ta']}
def cross(a):
    c=np.cumsum(a); return int(years[np.argmax(c>=1000)]) if c[-1]>=1000 else None
comb={}
for n in range(1,6):
    res=[(cross(sum(PG[k] for k in s)),s) for s in itertools.combinations(PG,n)]
    ok=sorted([r for r in res if r[0]]); allv=sorted([r[0] or 2100 for r in res])
    comb[n]=dict(best=ok[0][0],best_set=ok[0][1],median=allv[len(allv)//2],worst=max(allv),never=len(res)-len(ok))
    print(n,comb[n])
print({k:cross(v) for k,v in PG.items()})
r31=sum(v[4] for v in PG.values()); cum30=sum(v[:4].sum() for v in PG.values())
def req(ty):
    lo,hi=0,2
    for _ in range(60):
        g=(lo+hi)/2; c=cum30; x=r31
        for y in range(2031,ty+1): c+=x; x*=1+g
        lo,hi=(lo,g) if c>=1000 else (g,hi)
    return hi
goal={ty:round(req(ty),3) for ty in (2047,2052,2057)}; print('r31',r31,goal)
g=goal[2047]; print([(y,round(r31*(1+g)**(y-2031),1)) for y in (2031,2034,2037,2040,2043,2046)])
print({k:round(v[4],3) for k,v in PG.items()}, {k:round(v[1],3) for k,v in PG.items()},{k:round(v[2],3) for k,v in PG.items()})
json.dump(dict(groups=out,comb={k:dict(v,best_set=list(v['best_set'])) for k,v in comb.items()},goal=goal,r31=r31),open('lgstats.json','w'))
