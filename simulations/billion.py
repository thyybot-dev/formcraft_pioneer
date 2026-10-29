def path(ramp, start, g1, n1, g2, end=2075):
    r={}; y=start
    for v in ramp: r[y]=v; y+=1
    v=ramp[-1]; k=0
    while y<=end:
        v*= (1+g1) if k<n1 else (1+g2); r[y]=v; y+=1; k+=1
    return r
V={
 'Formcraft':path([0.046,0.135,0.324,0.625,1.03],2027,0.30,10,0.20),
 'Nyumba':path([0.032,0.281,0.727],2028,0.40,6,0.20),
 'Soko Foods':path([0.05,0.25,0.8,1.8,3.5],2027,0.35,6,0.15),
 'Trade Assistant':path([0.02,0.06,0.15],2029,0.40,6,0.15),
}
def cross(rs):
    t=0
    for y in range(2027,2076):
        t+=sum(r.get(y,0) for r in rs)
        if t>=1000: return y,t
    return None,t
for k,r in V.items(): print(k,cross([r]), [round(r.get(y,0),2) for y in (2031,2036,2041)])
print('all',cross(list(V.values())))
print('F+S',cross([V['Formcraft'],V['Soko Foods']]))
print('F+N',cross([V['Formcraft'],V['Nyumba']]))
for y in (2031,2036,2041,2046): 
  t=sum(sum(r.get(x,0) for r in V.values()) for x in range(2027,y+1)); print(y,round(t,1), round(sum(r.get(y,0) for r in V.values()),1))
S={
 'Formcraft':path([0.046,0.135,0.324,0.625,1.03],2027,0.40,10,0.25),
 'Nyumba':path([0.032,0.281,0.727],2028,0.55,6,0.25),
 'Soko Foods':path([0.05,0.25,0.8,1.8,3.5],2027,0.45,6,0.20),
 'Trade Assistant':path([0.02,0.06,0.15],2029,0.50,6,0.20),
}
print('strong all',cross(list(S.values())))
for k,r in S.items(): print('strong',k,cross([r]))
import json
out={}
for name,D in (('base',V),('strong',S)):
  for k,r in D.items():
    t=0;pts=[]
    for y in range(2027,2076):
      t+=r.get(y,0); pts.append(round(t,3))
    out[name+'|'+k]=pts
t=0;pts=[]
for y in range(2027,2076):
  t+=sum(r.get(y,0) for r in V.values()); pts.append(round(t,3))
out['base|All four']=pts
t=0;pts=[]
for y in range(2027,2076):
  t+=sum(r.get(y,0) for r in S.values()); pts.append(round(t,3))
out['strong|All four']=pts
json.dump(out,open('bn.json','w'))
