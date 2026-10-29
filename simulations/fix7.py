s=open('fcrun7.py').read()
a="    devok = rng.random(N) < (0.75 if dev else 0.0)          # developer hired and retained in 2027\n    depok = np.zeros(N, bool)                               # deputy / technical lead, hired in 2028\n"
assert a in s
s=s.replace(a,"    devok = np.zeros(N, bool); depok = np.zeros(N, bool)    # developer and deputy, hired when revenue can carry them\n    devy = np.full(N, 9999); depy = np.full(N, 9999); prev = np.zeros(N)\n")
b="        if deputy and y == 2028: depok = rng.random(N) < 0.7\n"
assert b in s
s=s.replace(b,"        if dev:\n            nd = (~devok) & (prev >= 0.10) & (rng.random(N) < 0.75); devok |= nd; devy = np.where(nd, y, devy)\n        if deputy:\n            nq = (~depok) & (prev >= 0.25) & (rng.random(N) < 0.7); depok |= nq; depy = np.where(nq, y, depy)\n")
c="        extra = (0.012 if (dev and j < 3) else 0.0) * devok + (0.010 if (deputy and 1 <= j < 3) else 0.0) * depok   # hires ahead of revenue (USD M)"
assert c in s
s=s.replace(c,"        extra = 0.012 * (devok & (y - devy < 2)) + 0.010 * (depok & (y - depy < 2))   # first two years of each key hire run ahead of revenue (USD M)")
d="        cum += np.where(live, rc, 0)\n        # hire"
assert d in s
s=s.replace(d,"        cum += np.where(live, rc, 0); prev = rc\n        # hire")
open('fcrun7.py','w').write(s); print('ok')
