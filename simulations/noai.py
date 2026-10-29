from vec2 import *
exec(open('soko.py').read().split("SF=soko_full(V)")[0].split("from vec2 import *")[1])
def noai(V):
    W=copy.deepcopy(V)
    # software built without AI: slower, costlier, later
    W['lgt'].update(p=0.2,start=2030); W['ta'].update(p=0.05)
    W['fc']['ramp']=[x*0.85 for x in W['fc']['ramp']]   # Formcraft Tools later, less output per person
    return W
for name,W in (('core',V),('soko_full',soko_full(V))):
    r=run(noai(W),N=1_000_000,hz=1.10,qmean=-0.07); print(name,'noAI',round(r['p2047'],4),round(r['p2072'],4),round(r['med'],1))
