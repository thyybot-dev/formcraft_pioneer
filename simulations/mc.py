import numpy as np, json
rng=np.random.default_rng(20261029)
N=10000; Y0=2027; Y1=2072; T=Y1-Y0+1; years=np.arange(Y0,Y1+1)
# plan: ramp (USD M), start year, early growth, early years, late growth, launch prob, age at 2027, ramp sd
V={
 'fc':dict(ramp=[0.046,0.135,0.324,0.625,1.03],start=2027,g1=0.30,n1=10,g2=0.20,p_launch=1.0,age0=2,sd=0.45),
 'ny':dict(ramp=[0.032,0.281,0.727],start=2028,g1=0.40,n1=6,g2=0.20,p_launch=0.6,age0=0,sd=0.7),
 'sk':dict(ramp=[0.05,0.25,0.8,1.8,3.5],start=2027,g1=0.35,n1=6,g2=0.15,p_launch=0.7,age0=0,sd=0.7),
 'ta':dict(ramp=[0.02,0.06,0.15],start=2029,g1=0.40,n1=6,g2=0.15,p_launch=0.10,age0=0,sd=0.8),
}
def hazard(age):
    return 0.16 if age<2 else 0.10 if age<5 else 0.07 if age<10 else 0.05
R={}
for k,v in V.items():
    rev=np.zeros((N,T))
    launched=rng.random(N)<v['p_launch']
    mult=np.exp(rng.normal(-v['sd']**2/2,v['sd'],N))   # mean-preserving execution multiplier
    q=rng.normal(-0.05,0.08,N)                          # persistent growth skill (plans run optimistic)
    for i in range(N):
        if not launched[i]: continue
        alive=True; r=None; k2=0; plateau=False
        for t,y in enumerate(years):
            if y<v['start']: continue
            age=v['age0']+(y-v['start'])
            if alive and rng.random()<hazard(age): alive=False
            if not alive: break
            j=y-v['start']
            if j<len(v['ramp']): r=v['ramp'][j]*mult[i]
            else:
                yrs_after=j-len(v['ramp'])
                gm=v['g1'] if yrs_after<v['n1'] else v['g2']
                if yrs_after>=v['n1']+10: gm=0.08
                if not plateau and rng.random()<0.08: plateau=True
                if plateau: gm=0.06
                g=max(gm+q[i]+rng.normal(0,0.15),-0.5)
                r=r*(1+g)
            rev[i,t]=r
    R[k]=rev
tot=sum(R.values())
cum=np.cumsum(tot,axis=1)
def first_cross(c):
    idx=np.argmax(c>=1000,axis=1); ok=c[:,-1]>=1000
    return np.where(ok,years[idx],0)
fc=first_cross(cum)
out={'p_by_year':[[int(y),round(float(np.mean((fc>0)&(fc<=y))),4)] for y in years]}
print('P(1bn by 2047)',np.mean((fc>0)&(fc<=2047)),'by 2057',np.mean((fc>0)&(fc<=2057)),'by 2072',np.mean(fc>0))
# single venture alone
for k in V:
    c=np.cumsum(R[k],axis=1); f=first_cross(c)
    alive36=np.mean(R[k][:,2036-Y0]>0); alive47=np.mean(R[k][:,2047-Y0]>0)
    pc=[np.percentile(c[:,-1],p) for p in (10,50,90)]
    out[k]={'p1bn':float(np.mean(f>0)),'alive2036':float(alive36),'alive2047':float(alive47),'cum2072_p10_50_90':[round(x,2) for x in pc],
            'yr_p':{str(y):[round(float(np.percentile(R[k][:,y-Y0],p)),3) for p in (10,50,90)] for y in range(2027,2037)},
            'mean2036':round(float(R[k][:,2036-Y0].mean()),2)}
    print(k,out[k]['p1bn'],alive36,alive47,pc,[out[k]['yr_p'][str(y)] for y in (2031,2036)])
print('total cum2072 p10/50/90',[round(np.percentile(cum[:,-1],p),1) for p in (10,25,50,75,90,95,99)])
print('total cum2047',[round(np.percentile(cum[:,2047-Y0],p),1) for p in (10,50,90,99)])
# share of runs with zero alive ventures in 2036
alive_count=sum((R[k][:,2036-Y0]>0).astype(int) for k in V)
print('alive count 2036 dist',[round(float(np.mean(alive_count==n)),3) for n in range(5)])
out['alive_count_2036']=[round(float(np.mean(alive_count==n)),3) for n in range(5)]
out['cum2072']=[round(float(np.percentile(cum[:,-1],p)),1) for p in (10,25,50,75,90,95,99)]
out['cum2047']=[round(float(np.percentile(cum[:,2047-Y0],p)),1) for p in (10,50,90,99)]
json.dump(out,open('mc.json','w'))
cond={}
for k in V:
    surv=[round(float(np.mean(R[k][:,y-Y0]>0)),3) for y in range(2027,2048)]
    st={}
    for y in (2029,2031,2036,2041):
        a=R[k][:,y-Y0]; a=a[a>0]
        st[y]=[round(float(np.percentile(a,p)),3) for p in (10,50,90)] if len(a) else None
    cond[k]={'surv':surv,'cond':st}
    print(k, st, surv[::5])
json.dump(cond,open('cond.json','w'))
c=cum[:,-1]; bins=[0,1,10,100,1000,1e12]
print('bins',[round(float(np.mean((c>=bins[i])&(c<bins[i+1]))),3) for i in range(5)])
