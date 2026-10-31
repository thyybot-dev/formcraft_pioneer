# Formcraft Radar: 5-year Monte Carlo (planning assumptions, USD). 100,000 futures.
import numpy as np, json
rng=np.random.default_rng(31); N=100_000; Y=[2027,2028,2029,2030,2031]
U=lambda a,b:rng.uniform(a,b,N)
# Lane 1: Studio clients from intent signals (monthly averages per year)
sig0=U(150,500); sig_g=U(0.45,0.9)                      # public intent signals a month in 2027, yearly growth
q=U(0.05,0.12)                                          # share that qualify after research
win=U(0.06,0.14)                                        # qualified -> signed design (plan: 30% visit x 30% won = 9%)
fee=U(1500,4000)                                        # design fee per client
db=U(0.12,0.30); cval=U(40_000,120_000); cmar=U(0.08,0.14)  # design clients who build with Formcraft, contract value, margin
smar=U(0.40,0.55)                                       # studio margin after design staff time
# Lane 2: maker jobs
mk0=U(50,200); mk_g=U(0.5,1.0); sub=U(3,6)              # paying makers in 2027, growth, USD a month
pl0=U(3,10); pl_g=U(0.5,1.0); plfee=U(50,150)           # placements a month in 2027, growth, fee per placement
# Lane 3: radar data sold to suppliers, banks, contractors (from 2029)
dc=U(2,8); dc_g=U(0.4,0.9); dfee=U(150,500)
out={}
for i,y in enumerate(Y):
    sig=np.minimum(sig0*(1+sig_g)**i,6000); ql=sig*q; clients=np.minimum(ql*win*12,[20,45,90,160,260][i]*U(0.8,1.2))  # studio capacity cap
    studio=clients*fee; build=clients*db*cval*cmar*(0.5 if i==0 else 1)   # first-year builds lag
    makers=np.minimum(mk0*(1+mk_g)**i,5000); places=np.minimum(pl0*(1+pl_g)**i,400)*12
    jobs=makers*sub*12+places*plfee
    data=np.where(y>=2029,np.minimum(dc*(1+dc_g)**(y-2029),60)*dfee*12,0)
    # running costs
    people=np.where(i==0,U(3600,6000),U(6000,12000)*(1+0.5*i))      # researcher/sales, then a small team
    ai=U(1200,4800)*(1+0.6*i); sat=np.where(y>=2028,U(3000,12000),0); scouts=places*U(1,3)*1.5+U(500,1500)
    msg=(ql*12+clients*20)*U(0.02,0.06); legal=U(500,1500)
    cost=people+ai+sat+scouts+msg+legal+(U(8000,20000) if i==0 else 0)  # year-1 build
    rev=studio+build+jobs+data; deliver=studio*(1-smar)+jobs*0.1+data*0.1; net=rev-deliver-cost
    p=lambda a:[round(float(np.percentile(a,k))) for k in (10,50,90)]
    out[y]=dict(qualified_month=p(ql),clients=p(clients),studio=p(studio),build=p(build),jobs=p(jobs),data=p(data),rev=p(rev),cost=p(cost),net=p(net),p_net_pos=round(float((net>0).mean()),3),cap_bound=round(float((ql*win*12>=[20,45,90,160,260][i]*0.8).mean()),2),makers=p(makers),placements=p(places))
cum=None
print(json.dumps(out,indent=0))
