from vec3 import *
import itertools
exec(open('soko.py').read().split("SF=soko_full(V)")[0].split("from vec2 import *")[1])
V3=soko_full(V)
V3['ny']=dict(V3['ny'],ramp=[0.0335,0.321,0.827])                                   # USD 5 landlord fee
V3['ta']=dict(V3['ta'],p=0.4,start=2028,ramp=[0.01,0.04,0.12,0.3],g1=0.35,n1=6,g2=0.12)  # tools sold
V3['yt']=dict(ramp=[0.002,0.01,0.03,0.06,0.10],start=2027,g1=0.35,n1=8,g2=0.08,p=0.8,age0=0,sd=1.0)  # 5 YouTube channels: ads+sponsors
AI=0.85; FUN=0.92
GLOBAL=dict(plateau=0.06,pg=0.09,lg=0.10); LOCAL=dict(plateau=0.08,pg=0.06,lg=0.08)
def cfg(ai=True,yt=True,glob=True,extra_hz=1.0,**kw):
    W=copy.deepcopy(V3)
    if not yt: W.pop('yt')
    if not ai:
        W['lgt'].update(p=0.2,start=2030); W['ta'].update(p=0.15); W['fc']['ramp']=[x*0.85 for x in W['fc']['ramp']]
    hz=(AI if ai else 1.10)*(FUN if yt else 1.0)*extra_hz
    q=(-0.03 if ai else -0.07)+(0.02 if yt else 0.0)
    d=dict(V=W,hz=hz,qmean=q); d.update(GLOBAL if glob else LOCAL); d.update(kw); return d
def mod(d,f):
    d=dict(d); d['V']=copy.deepcopy(d['V']); f(d['V']); return d
B=cfg()
S={'base':B,'no_yt':cfg(yt=False),'no_ai':cfg(ai=False),'no_ai_no_yt':cfg(ai=False,yt=False),'uganda_only':cfg(glob=False),
   'over':cfg(extra_hz=1.25),'shock7':cfg(shock_p=0.07),'shock15':cfg(shock_p=0.15),
   'kill':cfg(kill=True),'factory':cfg(factory=True),'best':cfg(kill=True,factory=True,extra_hz=0.7),
   'lev_surv':cfg(extra_hz=0.5),
   'drop_sk':mod(B,lambda W:[W.pop(k) for k in ('sk','ski','skf','skp','sks')]),'drop_fc':mod(B,lambda W:W.pop('fc')),
   'drop_lg':mod(B,lambda W:[W.pop(k) for k in ('lgc','lgt')]),'drop_ny':mod(B,lambda W:W.pop('ny')),'drop_ta':mod(B,lambda W:W.pop('ta')),'drop_yt':mod(B,lambda W:W.pop('yt')),
}
out={}
for k,a in S.items():
    t=time.time(); r=run(N=1_000_000,**a); out[k]=r
    print(k,round(time.time()-t),'s',round(r['p2047'],4),round(r['p2057'],4),round(r['p2072'],4),'med',round(r['med'],1),'bins',[round(x,3) for x in r['bins']],flush=True)
json.dump(out,open('v3.json','w'))
