# Formcraft simulation suite (run 6): rulebook + staged tools + scripts + model-independent continuity.
# Monte Carlo by setting, survival curves, revenue fan, lifetime distribution, sensitivity, stress tests, deterministic plan.
import numpy as np, json, time, sys
years = np.arange(2027, 2073)
RAMP = [0.046, 0.135, 0.324, 0.625, 1.03]
COV = [0.0, 0.10, 0.30, 0.45, 0.60, 0.75, 0.85]
TRACK = list(range(2027, 2041))

def sim(N, seed, mode, pg=0.75, stack='lean', content=True, glob=True, hz=1.0, qmean=-0.05, script=False, cont=0.0,
        err=1.0, crit_p=0.08, shock_p=0.0, disrupt=1.0, HZB=0.6, plateau=None, track=False):
    rng = np.random.default_rng(seed)
    pl0, pgr, lg = (0.06, 0.09, 0.10) if glob else (0.08, 0.06, 0.08)
    if plateau is not None: pl0 = plateau
    q = rng.normal(qmean + (0.02 if content else 0.0), 0.08, N)
    m = np.exp(rng.normal(-0.45**2/2, 0.45, N))
    live = np.ones(N, bool); r = np.zeros(N); pl = np.zeros(N, bool)
    phase = np.zeros(N, np.int8); cum = np.zeros(N); kitage = np.zeros(N)
    errs = np.zeros(N); crit = np.zeros(N, bool); cashneg = np.zeros(N, bool)
    out = {'surv': [], 'p10': [], 'p50': [], 'p90': []}; snap = {}
    for y in years:
        j = y - 2027; age = 2 + j
        if mode == 'rule':
            for _ in range(2):
                phase = phase + ((phase < 6) & (rng.random(N) < pg))
            cov = np.take(COV, phase); kitage += (phase > 0)
        elif mode == 'adhoc': cov = np.full(N, 0.35)
        else: cov = np.zeros(N)
        shock = rng.random(N) < shock_p if shock_p > 0 else np.zeros(N, bool)
        if j < len(RAMP):
            r = RAMP[j] * m * (1 + (0.25 if mode == 'rule' else 0.12 if mode == 'adhoc' else 0) * cov * (j >= 1))
            r = r * np.where(shock, 0.75, 1.0)
        else:
            gm = 0.30 if j - 5 < 10 else (0.20 if j - 5 < 20 else lg)
            pl |= rng.random(N) < pl0
            boost = (0.06 if mode == 'rule' else 0.03 if mode == 'adhoc' else 0) * cov / 0.85
            g = np.where(pl, pgr, gm) + q + boost + rng.normal(0, 0.15, N) - np.where(shock, 0.25, 0)
            r = r * (1 + np.maximum(g, -0.6))
        lam = 0.35 * np.maximum(r / 0.1, 0.3) ** 0.4 * err
        if mode == 'adhoc': lam = lam * 1.4
        if mode == 'rule': lam = lam * (1 - 0.7 * cov) * np.maximum(0.88 ** kitage, 0.35)
        if script: lam = lam * (1 - 0.25 * cov)
        ne = rng.poisson(lam); errs += np.where(live & (y <= 2036), ne, 0)
        isc = rng.random(N) < 1 - (1 - crit_p) ** ne
        crit |= live & isc & (y <= 2036)
        # disruptions: key person out (all), AI vendor outage or price shock (AI modes); continuity softens both
        dp = 0.04 + (0.05 if mode != 'none' else 0.0)
        dis = rng.random(N) < dp * disrupt
        soft = 1 - 0.8 * cont
        rc = r * (0.92 ** ne) * np.where(dis, 1 - 0.25 * soft, 1.0); r = r * (0.98 ** ne)
        staff = np.maximum(r / (0.040 * (1 + 0.8 * cov)), 1.0); seats = np.maximum(0.4 * staff, 1.0)
        if mode == 'none': tool = 0.0015 * seats + 0.001
        elif mode == 'adhoc': tool = 0.0015 * seats + 0.0004 * staff + 0.001
        elif stack == 'lean':
            aic = (0.0005 * (1 - 0.7 * cov) + (0.0008 if j < 2 else 0.0)) if script else 0.0005
            tool = 0.0020 * seats + aic * staff + 0.003 * cov / 0.85 + 0.0005
        else: tool = 0.0055 * seats + 0.0005 * staff + 0.008
        margin = 0.10 + (0.10 * cov if mode == 'rule' else 0.04 if mode == 'adhoc' else 0) - 0.03 * ne - tool / np.maximum(rc, 1e-6)
        cashneg |= live & (margin < 0) & (y <= 2030)
        h = (0.16 if age < 2 else 0.10 if age < 5 else 0.07 if age < 10 else 0.05) * hz * HZB
        h = h + 0.02 * ne + np.where(isc, 0.20, 0) + np.where(margin < 0, 0.08, np.where(margin < 0.03, 0.03, 0)) \
              + np.where(shock, 0.08, 0) + np.where(dis, 0.05 * soft, 0)
        live &= rng.random(N) >= h
        cum += np.where(live, rc, 0)
        if track and y in TRACK:
            out['surv'].append(float(live.mean())); rr = rc[live]
            for p in (10, 50, 90): out[f'p{p}'].append(float(np.percentile(rr, p)) if rr.size else 0.0)
        if y in (2031, 2036): snap[y] = (live.copy(), rc.copy(), margin.copy())
    d = {}
    for y in (2031, 2036):
        al, rr, mg = snap[y]
        d[f'alive{y}'] = float(al.mean()); d[f'mid{y}'] = float(np.median(rr[al])); d[f'p10_{y}'] = float(np.percentile(rr[al], 10)); d[f'p90_{y}'] = float(np.percentile(rr[al], 90)); d[f'margin{y}'] = float(np.median(mg[al]))
    d.update(errs=float(errs.mean()), p_crit=float(crit.mean()), p_cashneg=float(cashneg.mean()),
             p10m=float(np.mean(cum >= 10)), p100=float(np.mean(cum >= 100)), p1b=float(np.mean(cum >= 1000)),
             med_life=float(np.median(cum)), p90_life=float(np.percentile(cum, 90)),
             bins=[float(np.mean((cum >= lo) & (cum < hi))) for lo, hi in ((0, 1), (1, 10), (10, 100), (100, 1000), (1000, 1e18))])
    if track: d['track'] = out
    return d

if __name__ == '__main__':
    HZB = 0.55   # run 6 used 0.55: calibrates 'No AI' to ~42% running in 2036
    N = 1_000_000
    if len(sys.argv) > 1 and sys.argv[1] == 'cal':
        for h in (0.5, 0.55, 0.6):
            print(h, round(sim(200_000, 3, 'none', content=False, glob=False, HZB=h)['alive2036'], 3));
        sys.exit()
    HZB = float(sys.argv[1]) if len(sys.argv) > 1 else HZB
    runs = 0; R = {}
    PIONEER = dict(mode='rule', script=True, cont=1.0)
    S = {
     'No AI': dict(mode='none', content=False, glob=False),
     'Ad hoc AI': dict(mode='adhoc'),
     'Rulebook, staged tools': dict(mode='rule', cont=0.5),
     'Rulebook, full stack day one': dict(mode='rule', stack='full', cont=0.5),
     'Rulebook, slow rollout': dict(mode='rule', pg=0.40, cont=0.5),
     'Rulebook + scripts': dict(mode='rule', script=True, cont=0.5),
     'Pioneer plan': PIONEER,
     'Pioneer plan, best practice': dict(PIONEER, pg=0.90, hz=0.85),
    }
    R['settings'] = {}
    for k, a in S.items():
        t = time.time(); R['settings'][k] = sim(N, 21, HZB=HZB, track=True, **a); runs += N
        d = R['settings'][k]; print(k, round(time.time()-t), 's', {z: (round(v, 3) if isinstance(v, float) else '') for z, v in d.items() if z not in ('track', 'bins')}, flush=True)
    base = R['settings']['Pioneer plan']
    sens = {
     'Rollout gates pass 40% vs 90% a year': (dict(pg=0.40), dict(pg=0.90)),
     'Error rate x1.5 vs x0.5': (dict(err=1.5), dict(err=0.5)),
     'Critical share of errors 12% vs 4%': (dict(crit_p=0.12), dict(crit_p=0.04)),
     'Growth 5 points lower vs higher': (dict(qmean=-0.10), dict(qmean=0.0)),
     'Stalling chance 12% vs 3% a year': (dict(plateau=0.12), dict(plateau=0.03)),
     'Base failure risk x1.3 vs x0.7': (dict(hz=1.3), dict(hz=0.7)),
     'Disruptions twice as often vs none': (dict(disrupt=2.0), dict(disrupt=0.0)),
     'Full stack day one vs staged': (dict(stack='full'), dict()),
     'No scripts vs scripts': (dict(script=False), dict()),
     'No continuity vs full continuity': (dict(cont=0.0), dict()),
    }
    R['sens'] = {}
    for k, (lo, hi) in sens.items():
        a = sim(N, 21, HZB=HZB, **dict(PIONEER, **lo)); b = base if not hi else sim(N, 21, HZB=HZB, **dict(PIONEER, **hi))
        runs += N * (1 if not hi else 2)
        R['sens'][k] = dict(lo100=a['p100'], hi100=b['p100'], lo36=a['alive2036'], hi36=b['alive2036'])
        print('sens', k, round(a['p100'], 3), round(b['p100'], 3), flush=True)
    R['stress'] = {}
    for k, sp in (('No market shocks', 0.0), ('Moderate shocks (7% a year)', 0.07), ('Severe shocks (15% a year)', 0.15)):
        R['stress'][k] = {}
        for s in ('No AI', 'Pioneer plan'):
            d = R['settings'][s] if sp == 0 else sim(N, 21, HZB=HZB, shock_p=sp, **S[s])
            if sp: runs += N
            R['stress'][k][s] = {z: d[z] for z in ('alive2036', 'p100', 'p1b', 'med_life')}
        print('stress', k, R['stress'][k], flush=True)
    # deterministic plan path
    x = None; cum = 0; path = []; c100 = c1b = None
    for y in years:
        j = y - 2027
        x = RAMP[j] if j < 5 else x * (1 + (0.30 if j - 5 < 10 else 0.20 if j - 5 < 20 else 0.08))
        cum += x; path.append([int(y), round(x, 3), round(cum, 2)])
        if c100 is None and cum >= 100: c100 = int(y)
        if c1b is None and cum >= 1000: c1b = int(y)
    R['plan'] = dict(path=path[:16], cross100=c100, cross1b=c1b)
    R['runs'] = runs; R['HZB'] = HZB
    print('plan', c100, c1b, 'runs', runs)
    json.dump(R, open('fcsuite.json', 'w'), indent=1)
