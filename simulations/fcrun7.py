# Run 7: objective review of the full Pioneer page.
# Annual Monte Carlo (2027-2072) adding team capacity and hiring, key-person risk, founder focus, client portal,
# developer hire (build queue speed) - plus a monthly cash-and-capacity simulation for 2027-2029.
import numpy as np, json, time, sys
years = np.arange(2027, 2073)
RAMP = [0.046, 0.135, 0.324, 0.625, 1.03]
COV = [0.0, 0.10, 0.30, 0.45, 0.60, 0.75, 0.85]

def sim7(N, seed, mode='rule', pg=0.75, hz=1.0, qmean=-0.05, script=True, cont=1.0, content=True, glob=True,
         dev=False, deputy=False, p_hire=0.75, portal=0.0, focus=1.0, km_p=0.06, km_force=None, crit_p=0.08,
         HZB=0.55, track=False):
    rng = np.random.default_rng(seed)
    pl0, pgr, lg = (0.06, 0.09, 0.10) if glob else (0.08, 0.06, 0.08)
    q = rng.normal(qmean + (0.02 if content else 0.0), 0.08, N)
    m = np.exp(rng.normal(-0.45**2/2, 0.45, N))
    live = np.ones(N, bool); d = np.zeros(N); pl = np.zeros(N, bool)
    phase = np.zeros(N, np.int8); kitage = np.zeros(N); cum = np.zeros(N)
    fte = np.full(N, 2.0)                                   # effective full-time staff at start of 2027
    devok = np.zeros(N, bool); depok = np.zeros(N, bool)    # developer and deputy, hired when revenue can carry them
    devy = np.full(N, 9999); depy = np.full(N, 9999); prev = np.zeros(N)
    port = np.zeros(N, bool)
    errs = np.zeros(N); crit = np.zeros(N, bool); kmhit = np.zeros(N, bool); lost = np.zeros(N)
    out = {'surv': [], 'fte': [], 'util': []}; snap = {}
    for y in years:
        j = y - 2027; age = 2 + j
        if dev:
            nd = (~devok) & (prev >= 0.10) & (rng.random(N) < 0.75); devok |= nd; devy = np.where(nd, y, devy)
        if deputy:
            nq = (~depok) & (prev >= 0.25) & (rng.random(N) < 0.7); depok |= nq; depy = np.where(nq, y, depy)
        if portal > 0: port |= rng.random(N) < (portal if y >= 2027 else 0)
        # key person event (Emlyn): illness, burnout or pulled into other ventures
        km = rng.random(N) < km_p * (1.5 if focus < 0.8 else 1.0) * np.where(depok, 0.5, 1.0)
        if km_force and y == km_force: km = np.ones(N, bool)
        kmhit |= km & live & (y <= 2036)
        cover = np.clip(0.45 * cont + 0.35 * depok + 0.10 * devok, 0, 0.9)    # how much of Emlyn's work others can carry
        if mode == 'rule':
            pe = pg * focus * np.where(devok, 1.0, 0.8) * np.where(km, cover, 1.0)
            for _ in range(2):
                phase = phase + ((phase < 6) & (rng.random(N) < pe))
            cov = np.take(COV, phase); kitage += (phase > 0)
        else:
            cov = np.zeros(N)
        # latent demand
        if j < len(RAMP):
            d = RAMP[j] * m * (1 + (0.25 if mode == 'rule' else 0) * cov * (j >= 1)) * np.where(port, 1.05, 1.0)
        else:
            gm = 0.30 if j - 5 < 10 else (0.20 if j - 5 < 20 else lg)
            pl |= rng.random(N) < pl0
            boost = (0.06 if mode == 'rule' else 0) * cov / 0.85 + np.where(port, 0.02, 0.0)
            g = np.where(pl, pgr, gm) + q + boost + rng.normal(0, 0.15, N)
            d = d * (1 + np.maximum(g, -0.6))
        # capacity and hiring
        rps = 0.030 * (1 + 0.8 * cov)                       # USD M of revenue one full-time person can deliver
        cap = fte * rps
        over = np.maximum(d / cap - 1, 0)
        r = np.minimum(d, cap * 1.15)
        lostd = np.maximum(d - cap * 1.15, 0); lost += np.where(live & (y <= 2036), lostd, 0)
        d = d - 0.3 * lostd                                 # turned-away work hurts reputation
        util = r / cap
        # errors (overload raises them)
        lam = 0.35 * np.maximum(r / 0.1, 0.3) ** 0.4 * (1 + 1.5 * np.minimum(over, 1))
        if mode == 'rule': lam = lam * (1 - 0.7 * cov) * np.maximum(0.88 ** kitage, 0.35)
        if script and mode == 'rule': lam = lam * (1 - 0.25 * cov)
        ne = rng.poisson(lam); errs += np.where(live & (y <= 2036), ne, 0)
        cp = crit_p * np.where(port, 0.85, 1.0)
        isc = rng.random(N) < 1 - (1 - cp) ** ne; crit |= live & isc & (y <= 2036)
        rc = r * (0.92 ** ne) * np.where(km, 1 - 0.4 * (1 - cover), 1.0)
        # margin
        staffc = fte * 0.009 / np.maximum(rc, 1e-6) * 0.0     # salaries sit inside base margin; idle staff cost below
        tool = 0.0 if mode == 'none' else (0.0020 * np.maximum(0.4 * fte, 1) + (0.0005 * (1 - 0.7 * cov) + (0.0008 if j < 2 else 0)) * fte + 0.003 * cov / 0.85 + 0.0005)
        extra = 0.012 * (devok & (y - devy < 2)) + 0.010 * (depok & (y - depy < 2))   # first two years of each key hire run ahead of revenue (USD M)
        margin = 0.10 + (0.10 * cov if mode == 'rule' else 0) - 0.03 * ne - (tool + extra) / np.maximum(rc, 1e-6) - 0.25 * np.maximum(0.75 - util, 0)
        h = (0.16 if age < 2 else 0.10 if age < 5 else 0.07 if age < 10 else 0.05) * hz * HZB
        h = h + 0.02 * ne + np.where(isc, 0.20, 0) + np.where(margin < 0, 0.08, np.where(margin < 0.03, 0.03, 0)) + np.where(km, 0.12 * (1 - cover), 0)
        live &= rng.random(N) >= h
        cum += np.where(live, rc, 0); prev = rc
        # hire for next year if demand will outrun capacity and cash allows
        need = np.ceil(np.maximum(d * 1.25 / (0.030 * (1 + 0.8 * cov)) - fte, 0))
        can = margin > 0.03
        hires = rng.binomial(need.astype(np.int64), p_hire) * can
        fte = fte + hires - rng.binomial(np.round(fte).astype(np.int64), 0.08)   # 8% staff turnover a year
        fte = np.maximum(fte, 1.0)
        if track and y <= 2040:
            out['surv'].append(float(live.mean())); out['fte'].append(float(np.median(fte[live]))); out['util'].append(float(np.median(util[live])))
        if y in (2031, 2036): snap[y] = (live.copy(), rc.copy(), margin.copy(), fte.copy())
    res = {}
    for y in (2031, 2036):
        al, rr, mg, ff = snap[y]
        res[f'alive{y}'] = float(al.mean()); res[f'mid{y}'] = float(np.median(rr[al])); res[f'margin{y}'] = float(np.median(mg[al])); res[f'fte{y}'] = float(np.median(ff[al]))
    res.update(errs=float(errs.mean()), p_crit=float(crit.mean()), p_km=float(kmhit.mean()), lost_med=float(np.median(lost)),
               p100=float(np.mean(cum >= 100)), p1b=float(np.mean(cum >= 1000)), med_life=float(np.median(cum)))
    if track: res['track'] = out
    return res

# ---------- monthly cash and capacity simulation, Jan 2027 - Dec 2029 ----------
def monthly(N, seed, hiring_plan, portal, cash0=0.003, dev_month=3, seed_cash=0.0):
    rng = np.random.default_rng(seed)
    M = 36; cash = np.full(N, cash0 + seed_cash); staff = np.full(N, 2.0); backlog = np.zeros(N)
    receiv = np.zeros((N, 4))                                # money due in 0,1,2,3 months
    funnel = np.exp(rng.normal(0, 0.35, N))                  # how well content and the funnel work
    out = {k: [] for k in ('c10', 'c50', 'c90', 'rev50', 'staff50', 'leads50')}
    neg = np.zeros(N, bool); first_hire = np.full(N, -1); revs = np.zeros((N, 3))
    devc = 0.0007 if hiring_plan else 0.0                    # developer salary USD M per month from month 3
    for t in range(M):
        leads = rng.poisson(np.minimum(5 * 1.09 ** t, 30) * funnel)
        conv = 0.10 * (1.25 if (portal and t >= 6) else 1.0)
        wins = rng.binomial(leads, conv)
        value = wins * np.exp(rng.normal(np.log(0.0042), 0.6, N))   # USD M of fees won this month
        backlog += value
        cap = staff * 0.0026 * (1 + 0.3 * min(t / 24, 1))   # USD M a person delivers a month, rising with AI
        done = np.minimum(backlog, cap); backlog -= done
        late = rng.random(N) < 0.35
        receiv[:, 0] += done * 0.5; receiv[:, 1] += np.where(late, 0, done * 0.42); receiv[:, 3] += np.where(late, done * 0.42, 0)  # 8% never paid
        cashin = receiv[:, 0].copy(); receiv[:, :-1] = receiv[:, 1:]; receiv[:, -1] = 0
        cost = 0.0006 + staff * 0.0003 + (devc if t >= dev_month else 0) + (0.0006 if (hiring_plan and t >= 12) else 0) + 0.0003 + done * 0.25
        cash = cash + cashin - cost
        neg |= cash < 0
        revs[:, t // 12] += done
        # hire when backlog exceeds two months of capacity and cash covers three months of a salary
        trig = (backlog > 2 * cap) & (cash > 3 * 0.0003)
        hire = trig & (rng.random(N) < (0.5 if hiring_plan else 0.25))
        first_hire = np.where(hire & (first_hire < 0), t, first_hire)
        staff = staff + hire
        for k, a in (('c10', np.percentile(cash, 10)), ('c50', np.median(cash)), ('c90', np.percentile(cash, 90)), ('rev50', np.median(done)), ('staff50', np.median(staff)), ('leads50', np.median(leads))):
            out[k].append(float(a))
    out['p_neg'] = float(neg.mean()); out['first_hire_med'] = float(np.median(first_hire[first_hire >= 0])) if np.any(first_hire >= 0) else -1
    out['p_hired'] = float(np.mean(first_hire >= 0)); out['rev_year'] = [float(np.median(revs[:, i])) for i in range(3)]
    out['rev_year_p10'] = [float(np.percentile(revs[:, i], 10)) for i in range(3)]; out['rev_year_p90'] = [float(np.percentile(revs[:, i], 90)) for i in range(3)]
    out['staff_end'] = float(np.median(staff))
    return out

if __name__ == '__main__':
    if sys.argv[1:] == ['cal']:
        for h in (0.45, 0.5, 0.55):
            print(h, round(sim7(200_000, 3, mode='none', script=False, cont=0.0, content=False, glob=False, HZB=h)['alive2036'], 3))
        sys.exit()
    HZB = float(sys.argv[1]); N = 1_000_000; runs = 0; R = {}
    NONE = dict(mode='none', script=False, cont=0.0, content=False, glob=False)
    SOLO = dict(mode='rule', portal=0.35)
    PLAN = dict(mode='rule', dev=True, deputy=True, p_hire=0.75, portal=0.6)
    S = {'No AI': NONE,
         'Pioneer, Emlyn builds alone': SOLO,
         'Pioneer + hiring plan': PLAN,
         'Pioneer + hiring plan, no portal': dict(PLAN, portal=0.0),
         'Pioneer + hiring plan, Emlyn split five ways': dict(PLAN, focus=0.7),
         'Pioneer + hiring plan, best practice': dict(PLAN, pg=0.9, hz=0.85)}
    R['settings'] = {}
    for k, a in S.items():
        t = time.time(); R['settings'][k] = sim7(N, 31, HZB=HZB, track=True, **a); runs += N
        print(k, round(time.time() - t), {z: round(v, 3) for z, v in R['settings'][k].items() if z != 'track'}, flush=True)
    R['keyman'] = {}
    for k in ('No AI', 'Pioneer, Emlyn builds alone', 'Pioneer + hiring plan'):
        a = sim7(N, 31, HZB=HZB, km_force=2028, **S[k]); runs += N
        R['keyman'][k] = {z: a[z] for z in ('alive2031', 'alive2036', 'p100', 'p1b')}
        print('km', k, R['keyman'][k], flush=True)
    R['hire_sens'] = {}
    for p in (0.5, 0.9):
        a = sim7(N, 31, HZB=HZB, **dict(PLAN, p_hire=p)); runs += N
        R['hire_sens'][str(p)] = {z: a[z] for z in ('alive2036', 'p100', 'p1b', 'fte2036', 'lost_med')}
        print('hire', p, R['hire_sens'][str(p)], flush=True)
    R['monthly'] = {}
    for k, hp, po, dm, sc in (('Solo, no portal', False, False, 99, 0.0), ('Hiring plan, developer from month 3', True, True, 3, 0.0),
                              ('Hiring plan, developer from month 12', True, True, 12, 0.0), ('Hiring plan, month 12, USD 15k buffer', True, True, 12, 0.015)):
        R['monthly'][k] = monthly(200_000, 41, hp, po, dev_month=dm, seed_cash=sc); runs += 200_000
        mm = R['monthly'][k]; print('monthly', k, mm['p_neg'], mm['first_hire_med'], mm['p_hired'], mm['rev_year'], mm['staff_end'], flush=True)
    R['runs'] = runs; R['HZB'] = HZB
    json.dump(R, open('fcrun7.json', 'w'), indent=1); print('runs', runs)
