import numpy as np, copy
exec(open('mc.py').read().split("def hazard")[0])  # gets V, N, years etc
def run(V, hz=1.0, plateau_p=0.08, qmean=-0.05, seed=1, N=6000):
    rng=np.random.default_rng(seed); T=len(years); tot=np.zeros((N,T))
    for k,v in V.items():
        launched=rng.random(N)<v['p_launch']; mult=np.exp(rng.normal(-v['sd']**2/2,v['sd'],N)); q=rng.normal(qmean,0.08,N)
        for i in range(N):
            if not launched[i]: continue
            alive=True; r=None; plateau=False
            for t,y in enumerate(years):
                if y<v['start']: continue
                age=v['age0']+(y-v['start'])
                h=(0.16 if age<2 else 0.10 if age<5 else 0.07 if age<10 else 0.05)*hz
                if rng.random()<h: break
                j=y-v['start']
                if j<len(v['ramp']): r=v['ramp'][j]*mult[i]
                else:
                    ya=j-len(v['ramp']); gm=v['g1'] if ya<v['n1'] else v['g2']
                    if ya>=v['n1']+10: gm=0.08
                    if not plateau and rng.random()<plateau_p: plateau=True
                    if plateau: gm=0.06
                    r=r*(1+max(gm+q[i]+rng.normal(0,0.15),-0.5))
                tot[i,t]+=r
    c=np.cumsum(tot,axis=1); return float(np.mean(c[:,-1]>=1000)), float(np.mean(c[:,2047-2027]>=1000)), float(np.median(c[:,-1]))
base=run(V); print('base',base)
def mod(f):
    W=copy.deepcopy(V); f(W); return W
tests={
 'Survive better (failure risk halved)':dict(V=V,hz=0.5),
 'Avoid plateaus (half as likely)':dict(V=V,plateau_p=0.04),
 'Execute to plan (no optimism discount)':dict(V=V,qmean=0.0),
 'Soko Foods launched for sure':dict(V=mod(lambda W:W['sk'].update(p_launch=1.0))),
 'Nyumba launched for sure':dict(V=mod(lambda W:W['ny'].update(p_launch=1.0))),
 'Drop the Trade Assistant':dict(V=mod(lambda W:W.pop('ta'))),
 'Drop Nyumba':dict(V=mod(lambda W:W.pop('ny'))),
 'Drop Soko Foods':dict(V=mod(lambda W:W.pop('sk'))),
 'Formcraft only':dict(V={'fc':V['fc']}),
}
for k,a in tests.items(): print(k, run(**a))
