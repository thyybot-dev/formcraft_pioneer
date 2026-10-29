from vec2 import *
exec(open('soko.py').read().split("SF=soko_full(V)")[0].split("from vec2 import *")[1])
SF=soko_full(V)
groups={'Formcraft':{'fc':V['fc']},'Soko core':{'sk':V['sk']},'Soko full':{k:SF[k] for k in ('sk','ski','skf','skp','sks')},
        'Logistics':{'lgc':V['lgc'],'lgt':V['lgt']},'Nyumba':{'ny':dict(V['ny'],ramp=[0.0335,0.321,0.827])},'Trade Assistant (tools sold)':{'ta':dict(V['ta'],p=0.4,start=2028,ramp=[0.01,0.04,0.12,0.3],g1=0.35,n1=6,g2=0.12)}}
out={}
for name,W in groups.items():
    rng=np.random.default_rng(3); N=400_000
    c,x,a,per=chunk(W,N,rng)
    rev36=sum(np.where(per[k][0],per[k][1],0) for k in per)
    alive=rev36>0; r=rev36[alive]
    res=dict(alive36=float(alive.mean()),mid36=float(np.median(r)) if len(r) else 0,best36=float(np.percentile(r,90)) if len(r) else 0,
             cum_med=float(np.median(c)),cum_p90=float(np.percentile(c,90)),p10m=float(np.mean(c>=10)),p100m=float(np.mean(c>=100)),p1b=float(np.mean(c>=1000)))
    c2,x2,a2,_=chunk(W,N,np.random.default_rng(4),hz=0.85,qmean=-0.03)
    res['ai_p100m']=float(np.mean(c2>=100)); res['ai_cum_med']=float(np.median(c2)); res['ai_p1b']=float(np.mean(c2>=1000))
    out[name]=res; print(name,{k:round(v,3) for k,v in res.items()})
json.dump(out,open('alone.json','w'))
