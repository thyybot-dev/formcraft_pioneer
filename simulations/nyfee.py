from vec2 import *
W=copy.deepcopy(V)
# USD 5 per landlord connection; connections ~ new tenancies: ~300 (y1), ~8,000 (y2), ~20,000 (y3)
W['ny']['ramp']=[0.032+0.0015,0.281+0.04,0.727+0.10]
r=run(W,N=1_000_000,seed=7); print('fee',r['p2047'],r['p2057'],r['p2072'],r['med'])
json.dump({k:v for k,v in r.items() if k!='curve'},open('nyfee.json','w'))
