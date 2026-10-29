# Run 8: the full Pioneer page - run 7 (capacity, hiring, key person, focus, portal) plus the legal and financial plan
# (cash buffer, deposits and stage payments, insurance, shareholders' agreement and IP assignment, funding, automated
# compliance), with cautious and sceptic settings. Run with: python3 fcrun8.py 0.36  (0.36 calibrates 'No AI' to ~42% in 2036)
import numpy as np, json, time, sys
years = np.arange(2027, 2073)
RAMP = [0.046, 0.135, 0.324, 0.625, 1.03]
COV = [0.0, 0.10, 0.30, 0.45, 0.60, 0.75, 0.85]

def sim8(N, seed, mode='rule', pg=0.75, hz=1.0, qmean=-0.05, script=True, cont=1.0, content=True, glob=True,
         dev=False, deputy=False, p_hire=0.75, portal=0.0, focus=1.0, km_p=0.06, km_force=None, crit_p=0.08,
         HZB=0.55, track=False, buffer=False, terms=False, insure=False, legal=False, comply=False, funding=False, gcap=None, rps0=0.030, g1=0.30, g2=0.20):
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
    raised = np.zeros(N, bool); ry = np.full(N, 9999); dispute = np.zeros(N, bool); pens = np.zeros(N)
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
            gm = g1 if j - 5 < 10 else (g2 if j - 5 < 20 else lg)
            if gcap is not None and y > 2036: gm = min(gm, gcap)
            pl |= rng.random(N) < pl0
            boost = (0.06 if mode == 'rule' else 0) * cov / 0.85 + np.where(port, 0.02, 0.0) + np.where(raised & (y - ry < 3), 0.05, 0.0)
            g = np.where(pl, pgr, gm) + q + boost + rng.normal(0, 0.15, N)
            d = d * (1 + np.maximum(g, -0.6))
        # capacity and hiring
        rps = rps0 * (1 + 0.8 * cov)                       # USD M of revenue one full-time person can deliver
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
        # legal and financial plan effects
        if terms: margin = margin + 0.01                          # deposits, stage payments, less bad debt
        if insure: margin = margin - 0.012                        # premiums
        pen = rng.random(N) < (0.01 if comply else 0.05)          # tax or statutory penalty in the year
        margin = margin - 0.02 * pen; pens += pen & live & (y <= 2036)
        dsp = rng.random(N) < (0.005 if legal else 0.02)          # founder or partner dispute
        dispute |= dsp & live & (y <= 2036)
        if funding and legal:
            can_raise = (~raised) & (prev >= 0.15) & (y >= 2028) & (y <= 2032)
            nr = can_raise & (rng.random(N) < 0.25); raised |= nr; ry = np.where(nr, y, ry)
        cash_stress = np.where(margin < 0, 0.08, np.where(margin < 0.03, 0.03, 0))
        if buffer: cash_stress = np.where(j < 3, cash_stress * 0.25, cash_stress)
        cash_stress = np.where(raised & (y - ry < 4), cash_stress * 0.4, cash_stress)
        crit_h = 0.10 if insure else 0.20
        h = (0.16 if age < 2 else 0.10 if age < 5 else 0.07 if age < 10 else 0.05) * hz * HZB
        h = h + 0.02 * ne + np.where(isc, crit_h, 0) + cash_stress + np.where(km, 0.12 * (1 - cover), 0) + np.where(dsp, 0.06 if legal else 0.15, 0)
        live &= rng.random(N) >= h
        cum += np.where(live, rc, 0); prev = rc
        # hire for next year if demand will outrun capacity and cash allows
        need = np.ceil(np.maximum(d * 1.25 / (rps0 * (1 + 0.8 * cov)) - fte, 0))
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
    res.update(p_raised=float(raised.mean()), p_dispute=float(dispute.mean()), pens=float(pens.mean()), errs=float(errs.mean()), p_crit=float(crit.mean()), p_km=float(kmhit.mean()), lost_med=float(np.median(lost)),
               p100=float(np.mean(cum >= 100)), p1b=float(np.mean(cum >= 1000)), med_life=float(np.median(cum)))
    if track: res['track'] = out
    return res

# ---------- monthly cash and capacity simulation, Jan 2027 - Dec 2029 ----------
def monthly(N, seed, hiring_plan, portal, cash0=0.003, dev_month=3, seed_cash=0.0, deposit=0.0):
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
        dep = value * deposit
        cap = staff * 0.0026 * (1 + 0.3 * min(t / 24, 1))   # USD M a person delivers a month, rising with AI
        done = np.minimum(backlog, cap); backlog -= done
        late = rng.random(N) < 0.35
        bd = 0.08 * (1 - deposit / 0.3 * 0.6) if deposit else 0.08; pay = done * (1 - deposit - bd)
        receiv[:, 0] += pay * 0.55; receiv[:, 1] += np.where(late, 0, pay * 0.45); receiv[:, 3] += np.where(late, pay * 0.45, 0)
        cashin = receiv[:, 0].copy() + dep; receiv[:, :-1] = receiv[:, 1:]; receiv[:, -1] = 0
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
        for h in (0.36, 0.38, 0.41):
            print(h, round(sim8(200_000, 3, mode='none', script=False, cont=0.0, content=False, glob=False, HZB=h)['alive2036'], 3))
        sys.exit()
    HZB = float(sys.argv[1]); N = 1_000_000; runs = 0; R = {}
    NONE = dict(mode='none', script=False, cont=0.0, content=False, glob=False)
    PLAN = dict(mode='rule', dev=True, deputy=True, p_hire=0.75, portal=0.6)
    FULL = dict(PLAN, buffer=True, terms=True, insure=True, legal=True, comply=True, funding=True)
    S = {'No AI, no legal or financial plan': NONE,
         'Pioneer + hiring, no legal or financial plan': PLAN,
         'Full plan (Pioneer + hiring + legal + financial)': FULL,
         'Full plan without the cash buffer': dict(FULL, buffer=False),
         'Full plan without IP assignment and SHA': dict(FULL, legal=False),
         'Full plan without insurance': dict(FULL, insure=False),
         'Full plan, best practice': dict(FULL, pg=0.9, hz=0.85),
         'Reality check (cautious assumptions)': dict(FULL, gcap=0.12, rps0=0.022, hz=1.15),
         'Sceptic: no AI': dict(NONE, g1=0.15, g2=0.08, rps0=0.022, hz=1.15),
         'Sceptic: full plan': dict(FULL, g1=0.15, g2=0.08, rps0=0.022, hz=1.15)}
    R['settings'] = {}
    for k, a in S.items():
        t = time.time(); R['settings'][k] = sim8(N, 51, HZB=HZB, track=True, **a); runs += N
        print(k, round(time.time() - t), {z: round(v, 3) for z, v in R['settings'][k].items() if z != 'track'}, flush=True)
    R['monthly'] = {}
    for k, dpst, sc in (('Hiring plan, no deposits, no buffer', 0.0, 0.0), ('Hiring plan, 30% deposits', 0.3, 0.0), ('Hiring plan, 30% deposits + USD 15k buffer', 0.3, 0.015)):
        R['monthly'][k] = monthly(200_000, 61, True, True, dev_month=12, seed_cash=sc, deposit=dpst); runs += 200_000
        mm = R['monthly'][k]; print('monthly', k, round(mm['p_neg'], 3), [round(x * 1000, 1) for x in mm['rev_year']], [round(x * 1000, 1) for x in mm['c10'][::3]], flush=True)
    R['runs'] = runs; R['HZB'] = HZB
    json.dump(R, open('fcrun8.json', 'w'), indent=1); print('runs', runs)
