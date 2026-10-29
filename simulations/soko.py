from vec2 import *
def soko_full(V):
    W=copy.deepcopy(V)
    W['ski']=dict(ramp=[0.1,0.5,1.5,3.0],start=2028,g1=0.25,n1=6,g2=0.10,p=0.5,age0=0,sd=0.8,req='sk')   # schools, army, institutions (tenders)
    W['skf']=dict(ramp=[0.05,0.3,1.0,2.5],start=2029,g1=0.40,n1=6,g2=0.15,p=0.4,age0=0,sd=0.9,req='sk')  # franchise bulk food shops + online
    W['skp']=dict(ramp=[0.05,0.2,0.6,1.2],start=2030,g1=0.20,n1=10,g2=0.08,p=0.5,age0=0,sd=0.6)         # plantations: coffee, cocoa, vanilla (investor-funded)
    W['sks']=dict(ramp=[0.03,0.15,0.4],start=2029,g1=0.20,n1=8,g2=0.08,p=0.5,age0=0,sd=0.6,req='sk')    # silos: storage fees, warehouse receipts
    return W
SF=soko_full(V)
S={'base':dict(V=V),'soko_full':dict(V=SF),'soko_full_ai':dict(V=SF,hz=0.85,qmean=-0.03),
   'soko_full_over':dict(V=SF,hz=1.25),'soko_full_ai_best':dict(V=SF,hz=0.85*0.7,qmean=-0.03,kill=True,factory=True)}
out={}
for k,a in S.items():
    r=run(N=1_000_000,**a); out[k]={x:r[x] for x in ('p2047','p2057','p2072','med','p10','p90')}
    print(k,round(r['p2047'],4),round(r['p2057'],4),round(r['p2072'],4),'med',round(r['med'],1),flush=True)
P={k:plan(v) for k,v in SF.items()}
sk=sum(P[k] for k in ('sk','ski','skf','skp','sks'))
for y in (2031,2036): print(y,{k:round(P[k][y-2027],2) for k in ('sk','ski','skf','skp','sks')}, round(sk[y-2027],2))
c=np.cumsum(sk); print('soko alone cross', 2027+int(np.argmax(c>=1000)))
tot=sum(P.values()); c=np.cumsum(tot); print('all cross',2027+int(np.argmax(c>=1000)), 'r31',tot[4])
json.dump(out,open('soko.json','w'))
