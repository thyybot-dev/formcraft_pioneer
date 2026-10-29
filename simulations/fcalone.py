exec(open('v3.py').read().split("S={")[0])
def fc_only(c):
    d=dict(c); d['V']={'fc':c['V']['fc']}; return d
S={'none':fc_only(cfg(ai=False,yt=False,glob=False)),'ai':fc_only(cfg(ai=True,yt=False,glob=False)),
   'ai_yt':fc_only(cfg(ai=True,yt=True,glob=False)),'full':fc_only(cfg(ai=True,yt=True,glob=True)),
   'full_best':fc_only(cfg(ai=True,yt=True,glob=True,extra_hz=0.7))}
out={}
for k,a in S.items():
    rng=np.random.default_rng(9); N=400_000
    kw={x:a[x] for x in a if x!='V'}
    c,x,al,per=chunk(a['V'],N,rng,**kw)
    l,r=per['fc']; r36=r[l]
    out[k]=dict(alive36=float(l.mean()),mid36=float(np.median(r36)),best36=float(np.percentile(r36,90)),p100=float(np.mean(c>=100)),p1b=float(np.mean(c>=1000)),med=float(np.median(c)))
    print(k,{z:round(v,3) for z,v in out[k].items()})
json.dump(out,open('fcalone.json','w'))
