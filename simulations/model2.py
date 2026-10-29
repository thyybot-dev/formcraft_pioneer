import json
rev={
 'Stores':[20,35,55,80,110],
 'Studio':[12,32,75,140,220],
 'Drafting':[8,25,50,80,110],
 'Families':[5,15,35,60,90],
 'Tools':[0,8,25,60,120],
 'B2B':[1,8,20,40,70],
 'Templates':[0,4,12,30,55],
 'Public bids':[0,0,15,40,70],
 'Construction':[0,3,10,25,50],
 'Concrete':[0,0,15,45,90],
 'Academy':[0,5,12,22,35],
 'Bench':[0,0,0,3,10],
}
cogs={'Stores':.55,'Studio':.35,'Drafting':.05,'Families':.10,'Tools':.15,'B2B':.45,'Templates':.35,'Public bids':.35,'Construction':.10,'Concrete':.85,'Academy':.30,'Bench':.15}
fx={'Drafting':.9,'Families':.7,'Tools':.4,'B2B':.3,'Templates':.1}
def run(staff,opex,capex,mult=1,slip=False):
    cash=0;out=[]
    for i in range(5):
        r=c=u=0
        for k,v in rev.items():
            x=v[i]*mult
            if slip and k in('Tools','B2B','Families','Templates'): x=(v[i-1] if i else 0)*mult
            r+=x;c+=x*cogs[k];u+=x*fx.get(k,0)
        e=r-c-staff[i]-opex[i];tax=max(0,e)*.3;f=e-tax-capex[i];cash+=f
        out.append([i+1,round(r,1),round(r-c,1),round((r-c)/r*100),staff[i],opex[i],round(e,1),round(tax,1),capex[i],round(f,1),round(cash,1),round(u/r*100)])
    return out
S=[14,35,75,130,200];O=[15,22,35,50,70];C=[6,8,12,18,25]
base=run(S,O,C)
for o in base:print(o)
print('up');[print(o) for o in run(S,O,C,1.3)]
print('down frozen');[print(o) for o in run([14,28,50,85,130],[15,18,26,38,52],[6,6,8,12,16],.7,True)]
print([sum(v[i] for v in rev.values()) for i in range(5)])
