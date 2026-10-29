from vec2 import *
def mod(f):
    W=copy.deepcopy(V); f(W); return W
TAM=mod(lambda W:W['ta'].update(p=0.4,start=2028,ramp=[0.01,0.04,0.12,0.3],g1=0.35,n1=6,g2=0.12,sd=0.8))
S={
 'base':dict(V=V),
 'lev_surv':dict(V=V,hz=0.5),'lev_exec':dict(V=V,qmean=0.0),'lev_plat':dict(V=V,plateau=0.04),
 'lev_sk1':dict(V=mod(lambda W:W['sk'].update(p=1.0))),'lev_lg1':dict(V=mod(lambda W:(W['lgc'].update(p=1.0),W['lgt'].update(p=1.0)))),'lev_ny1':dict(V=mod(lambda W:W['ny'].update(p=1.0))),
 'lev_tam':dict(V=TAM),'drop_ta':dict(V=mod(lambda W:W.pop('ta'))),'drop_ny':dict(V=mod(lambda W:W.pop('ny'))),'drop_lg':dict(V=mod(lambda W:(W.pop('lgc'),W.pop('lgt')))),'drop_sk':dict(V=mod(lambda W:W.pop('sk'))),
 'shock7':dict(V=V,shock_p=0.07),'shock15':dict(V=V,shock_p=0.15),
 'kill':dict(V=V,kill=True),'factory':dict(V=V,factory=True),'kill_factory':dict(V=V,kill=True,factory=True),'best':dict(V=V,kill=True,factory=True,hz=0.7),
}
out={}
for k,a in S.items():
    t=time.time(); out[k]=run(N=1_000_000,**a)
    print(k,round(time.time()-t,1),'s',round(out[k]['p2047'],4),round(out[k]['p2057'],4),round(out[k]['p2072'],4),'±',round(out[k]['se2072'],5),'med',round(out[k]['med'],1),flush=True)
json.dump(out,open('run1m_v2.json','w'))
