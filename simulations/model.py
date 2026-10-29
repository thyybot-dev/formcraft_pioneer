import json
Y=[1,2,3,4,5]
# revenue USD thousands, base case
rev={
 'Stores (furniture, joinery, interiors)':[60,80,110,140,175],
 'Studio design fees':[20,59,126,210,330],
 'Subcontract CAD/BIM drafting':[15,45,80,110,140],
 'Family factory & content services':[10,30,60,90,120],
 'Formcraft Tools licences & BIM setup':[0,17,51,114,209],
 'B2B services (render, cloud, hosting)':[3,20,45,80,120],
 'Template builds (plan sales)':[0,8,24,54,90],
 'Construction management & bids':[0,5,15,40,75],
 'Concrete (partner supply)':[0,0,30,80,150],
 'Academy':[0,8,20,35,50],
 'Bench premium & suppliers':[0,0,0,5,15],
}
cogs_pct={'Stores (furniture, joinery, interiors)':.55,'Studio design fees':.25,'Subcontract CAD/BIM drafting':.05,
'Family factory & content services':.10,'Formcraft Tools licences & BIM setup':.15,'B2B services (render, cloud, hosting)':.45,
'Template builds (plan sales)':.35,'Construction management & bids':.10,'Concrete (partner supply)':.85,'Academy':.30,'Bench premium & suppliers':.15}
# share earned in USD from outside Uganda
fx_share={'Subcontract CAD/BIM drafting':.9,'Family factory & content services':.7,'Formcraft Tools licences & BIM setup':.4,'B2B services (render, cloud, hosting)':.3,'Template builds (plan sales)':.1}
staff=[40,100,170,280,400]
opex=[48,70,95,125,155]   # software, AI, cloud, rent, utilities, marketing, legal, travel
capex=[14,20,25,35,40]
def run(mult=1.0, delay_soft=False):
    out=[]
    cash=0
    for i in range(5):
        r=0;c=0;usd=0
        for k,v in rev.items():
            x=v[i]*mult
            if delay_soft and k in ('Formcraft Tools licences & BIM setup','B2B services (render, cloud, hosting)','Family factory & content services','Template builds (plan sales)'):
                x=(v[i-1] if i>0 else 0)*mult  # one-year slip
            r+=x;c+=x*cogs_pct[k];usd+=x*fx_share.get(k,0)
        gp=r-c
        ebitda=gp-staff[i]-opex[i]
        tax=max(0,ebitda)*0.30
        fcf=ebitda-tax-capex[i]
        cash+=fcf
        out.append(dict(year=i+1,revenue=round(r,1),gross=round(gp,1),gm=round(gp/r*100,1) if r else 0,staff=staff[i],opex=opex[i],ebitda=round(ebitda,1),margin=round(ebitda/r*100,1),capex=capex[i],fcf=round(fcf,1),cum=round(cash,1),usd_share=round(usd/r*100,1)))
    return out
base=run();down=run(0.7,True);up=run(1.3)
for n,s in (('base',base),('down',down),('up',up)):
    print(n)
    for o in s: print(o)
    print('min cum',min(o['cum'] for o in s))
tot=[sum(v[i] for v in rev.values()) for i in range(5)]
print(tot)
json.dump(dict(rev=rev,base=base,down=down,up=up),open('model.json','w'))
