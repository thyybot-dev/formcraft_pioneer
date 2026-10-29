exec(open('sim5.py').read().split("out={'combos'")[0])
import json
res={}
base=stats(run(V,seed=2)[0]); res['base']=base
def S(**kw): return stats(run(**kw)[0])
def mod(f):
    W=copy.deepcopy(V); f(W); return W
lev={
 'Halve the yearly failure risk':dict(V=V,hz=0.5),
 'Grow at the planned rates':dict(V=V,qmean=0.0),
 'Halve the chance of stalling':dict(V=V,plateau=0.04),
 'Soko Foods surely launches':dict(V=mod(lambda W:W['sk'].update(p=1.0))),
 'Logistics surely launches':dict(V=mod(lambda W:W['lg'].update(p=1.0))),
 'Nyumba surely launches':dict(V=mod(lambda W:W['ny'].update(p=1.0))),
 'Drop the Trade Assistant':dict(V=mod(lambda W:W.pop('ta'))),
 'Drop Nyumba':dict(V=mod(lambda W:W.pop('ny'))),
 'Drop Logistics':dict(V=mod(lambda W:W.pop('lg'))),
 'Drop Soko Foods':dict(V=mod(lambda W:W.pop('sk'))),
}
res['lev']={k:S(seed=2,**a)['p2072'] for k,a in lev.items()}
print('base',base['p2072'],res['lev'])
res['shock']={'none':base, 'moderate':S(V=V,seed=2,shock_p=0.07), 'severe':S(V=V,seed=2,shock_p=0.15)}
print('shock',{k:(v['p2072'],v['med']) for k,v in res['shock'].items()})
res['kill']=S(V=V,seed=2,kill=True); print('kill',res['kill']['p2072'],res['kill']['med'])
res['factory']=S(V=V,seed=2,factory=True); print('factory',res['factory']['p2072'],res['factory']['med'])
res['kill_factory']=S(V=V,seed=2,kill=True,factory=True); print('kill+factory',res['kill_factory']['p2072'],res['kill_factory']['med'])
res['best_practice']=S(V=V,seed=2,kill=True,factory=True,hz=0.7); print('best practice',res['best_practice']['p2072'],res['best_practice']['p2047'],res['best_practice']['med'])
json.dump(res,open('sims_more.json','w'))
