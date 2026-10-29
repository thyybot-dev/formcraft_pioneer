# Formcraft rulebook simulation: recipes + MCP-connected tool stack, phased gates, tool costs, errors, margin.
import numpy as np, json, time
years = np.arange(2027, 2073); T = len(years)
RAMP = [0.046, 0.135, 0.324, 0.625, 1.03]           # USD M plan, 2027-2031
COV = [0.0, 0.10, 0.30, 0.45, 0.60, 0.75, 0.85]     # value-chain coverage after k phases passed

def sim(N, seed, mode, pg=0.75, stack='lean', content=True, glob=True, hz=1.0, qmean=-0.05, script=False):
    rng = np.random.default_rng(seed)
    plateau, pgr, lg = (0.06, 0.09, 0.10) if glob else (0.08, 0.06, 0.08)
    q = rng.normal(qmean + (0.02 if content else 0.0), 0.08, N)
    m = np.exp(rng.normal(-0.45**2/2, 0.45, N))
    live = np.ones(N, bool); r = np.zeros(N); pl = np.zeros(N, bool)
    phase = np.zeros(N, np.int8); cum = np.zeros(N); kitage = np.zeros(N)
    errs = np.zeros(N); crit = np.zeros(N, bool); cashneg = np.zeros(N, bool)
    out = {}; reach75 = np.zeros(N, np.int16)
    for t, y in enumerate(years):
        j = y - 2027; age = 2 + j
        # rollout gates (rulebook modes): up to two phases a year, each passes with prob pg
        if mode == 'rule':
            for _ in range(2):
                adv = (phase < 6) & (rng.random(N) < pg); phase = phase + adv
            cov = np.take(COV, phase)
            kitage += (phase > 0)
        elif mode == 'adhoc':
            cov = np.full(N, 0.35)
        else:
            cov = np.zeros(N)
        reach75[(cov >= 0.75) & (reach75 == 0)] = y
        # revenue path
        if j < len(RAMP):
            r = RAMP[j] * m
            r = r * (1 + (0.25 if mode == 'rule' else 0.12 if mode == 'adhoc' else 0) * cov * (j >= 1))
        else:
            ya = j - len(RAMP); gm = 0.30 if ya < 10 else (0.20 if ya < 20 else lg)
            pl |= rng.random(N) < plateau
            boost = (0.06 if mode == 'rule' else 0.03 if mode == 'adhoc' else 0) * cov / 0.85
            g = np.where(pl, pgr, gm) + q + boost + rng.normal(0, 0.15, N)
            r = r * (1 + np.maximum(g, -0.6))
        # serious errors: more output without checks raises them; recipes, tests and learning cut them
        lam = 0.35 * np.maximum(r / 0.1, 0.3) ** 0.4
        if mode == 'adhoc': lam = lam * 1.4
        if mode == 'rule': lam = lam * (1 - 0.7 * cov) * np.maximum(0.88 ** kitage, 0.35) + lam * 0.0
        if script: lam = lam * (1 - 0.25 * cov)   # tested scripts repeat exactly; AI only handles exceptions
        ne = rng.poisson(lam); errs += np.where(live & (y <= 2036), ne, 0)
        isc = rng.random(N) < 1 - (1 - 0.08) ** ne       # any critical error this year
        crit |= live & isc & (y <= 2036)
        rc = r * (0.92 ** ne); r = r * (0.98 ** ne)   # most of the hit is that year; a little is lasting
        # margin and tool stack cost (USD M)
        staff = np.maximum(r / (0.040 * (1 + 0.8 * cov)), 1.0)
        seats = np.maximum(0.4 * staff, 1.0)
        if mode == 'none':
            tool = 0.0015 * seats + 0.001
        elif mode == 'adhoc':
            tool = 0.0015 * seats + 0.0004 * staff + 0.001
        elif stack == 'lean':
            aic = (0.0005 * (1 - 0.7 * cov) + (0.0008 if j < 2 else 0.0)) if script else 0.0005   # AI spend per staff: build-heavy early, then mostly scripts
            tool = 0.0020 * seats + aic * staff + 0.003 * cov / 0.85 + 0.0005   # staged: pay as phases need it
        else:
            tool = 0.0055 * seats + 0.0005 * staff + 0.008
        base_m = 0.10 + (0.10 * cov if mode == 'rule' else 0.04 if mode == 'adhoc' else 0) - 0.03 * ne
        margin = base_m - tool / np.maximum(rc, 1e-6)
        cashneg |= live & (margin < 0) & (y <= 2030)
        # hazard
        h = (0.16 if age < 2 else 0.10 if age < 5 else 0.07 if age < 10 else 0.05) * hz * HZB
        h = h + 0.02 * ne + np.where(isc, 0.20, 0) + np.where(margin < 0, 0.08, np.where(margin < 0.03, 0.03, 0))
        live &= rng.random(N) >= h
        cum += np.where(live, rc, 0)
        if y in (2028, 2031, 2036):
            out[y] = dict(alive=live.copy(), r=r.copy(), margin=margin.copy(), toolshare=tool / np.maximum(r, 1e-6), cov=cov.copy())
    return cum, out, errs, crit, cashneg, reach75

S = {
 'none':        dict(mode='none', content=False, glob=False),
 'adhoc':       dict(mode='adhoc'),
 'rule_lean':   dict(mode='rule', pg=0.75, stack='lean'),
 'rule_full':   dict(mode='rule', pg=0.75, stack='full'),
 'rule_slow':   dict(mode='rule', pg=0.40, stack='lean'),
 'rule_script': dict(mode='rule', pg=0.75, stack='lean', script=True),
 'rule_best':   dict(mode='rule', pg=0.90, stack='lean', hz=0.85),
}
import sys
HZB=float(sys.argv[1]) if len(sys.argv)>1 else 0.6   # 0.6 calibrates 'none' to ~42% running in 2036, as in the earlier model
ONLY=sys.argv[2].split(',') if len(sys.argv)>2 else list(S)
res = {}
for k, a in S.items():
    if k not in ONLY: continue
    t0 = time.time(); N = 1_000_000 if len(ONLY)>1 else 200_000
    cum, o, errs, crit, cashneg, r75 = sim(N, 11, **a)
    d = {}
    for y in (2031, 2036):
        al = o[y]['alive']; rr = o[y]['r'][al]; mg = o[y]['margin'][al]
        d[f'alive{y}'] = float(al.mean()); d[f'mid{y}'] = float(np.median(rr)); d[f'p10_{y}'] = float(np.percentile(rr, 10)); d[f'p90_{y}'] = float(np.percentile(rr, 90))
        d[f'margin{y}'] = float(np.median(mg)); d[f'cov{y}'] = float(np.median(o[y]['cov'][al]))
    d['toolshare2028'] = float(np.median(o[2028]['toolshare'][o[2028]['alive']]))
    d['errs_med'] = float(np.median(errs)); d['errs_mean'] = float(errs.mean()); d['p_crit'] = float(crit.mean()); d['p_cashneg'] = float(cashneg.mean())
    d['p100'] = float(np.mean(cum >= 100)); d['p1b'] = float(np.mean(cum >= 1000)); d['med_life'] = float(np.median(cum)); d['p90_life'] = float(np.percentile(cum, 90))
    d['reach75_med'] = float(np.median(r75[r75 > 0])) if np.any(r75 > 0) else 0; d['p_reach75_2029'] = float(np.mean((r75 > 0) & (r75 <= 2029)))
    res[k] = d; print(k, round(time.time() - t0), 's', {z: round(v, 3) for z, v in d.items()}, flush=True)
if len(ONLY)>1: json.dump(res, open('fcrule.json', 'w'), indent=1)
