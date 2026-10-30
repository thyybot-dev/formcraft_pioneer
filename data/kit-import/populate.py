"""Turns the Formcraft kit (v2.2 r4) and the QS workbook into Command Centre records, in chunks of up to 50 write ops."""
import json, re, csv, glob, os, collections
K = '/home/claude/formcraft/formcraft-kit/FMC_Kit_v2.2'
GH = 'https://github.com/formcraft/formcraft-kit/blob/main/FMC_Kit_v2.2/'
TODAY = '2026-10-30'
P = json.load(open('/tmp/qs/prices.json'))
ops = []
def put(coll, id_, data):
    data = {k: v for k, v in data.items() if v not in (None, '')}
    data.update(by='', added=TODAY, src='kit import')
    ops.append({'op': 'set', 'path': f'{coll}/{id_}', 'data': data})
import hashlib
def slug(s):
    b = re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
    return b if len(b) <= 60 else b[:52] + '-' + hashlib.md5(b.encode()).hexdigest()[:6]
def readable(code):
    c = code.replace('FMC_', '')
    parts = c.split('_')
    return ' '.join(re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', p) for p in parts)

# ---- price book ----
for r in P['rows']:
    if r['_origin'].startswith('kit'):
        code = r['item']
        name = readable(code) if code.startswith('FMC_') else code
        m = re.search(r'Unit detail: (.*?)\. (?:Spec: (.*?)\. )?From the Formcraft kit', r['notes'])
        unit_detail = m.group(1) if m else ''
        spec = m.group(2) if m and m.group(2) else ''
        src = r['notes'].split('Source: ')[-1]
        rng = f"Range UGX {int(r['_low']):,}-{int(r['_high']):,}, midpoint used. " if r['_high'] != r['_low'] else ''
        st = 'Verified price' if not r['_flag'] else 'Secondary source: get a supplier quote before a BoQ'
        notes = f"{rng}{unit_detail}. {('Spec: ' + spec + '. ') if spec else ''}{st}. Kit: {code if code.startswith('FMC_') else 'raw material'} (Ogala review research, Oct 2026). {src}"
        put('reg_pricebook', 'kit-' + slug(code), dict(item=name, category=r['category'], unit=r['unit'], rate=r['rate'], region='Kampala', date=r['date'], source='Website', notes=notes))
    else:
        notes = r['notes'].replace(' QS rate analysis, Civil_Material_Price_List.xlsx (saved 24 Jun 2026)', ' From the QS workbook (24 Jun 2026).').replace('QS rate analysis, Civil_Material_Price_List.xlsx (saved 24 Jun 2026)', 'From the QS workbook (24 Jun 2026).')
        if r['_flag']: notes += ' CHECK: ' + r['_flag'] + '.'
        put('reg_pricebook', 'qs-' + slug(r['item']), dict(item=r['item'], category=r['category'], unit=r['unit'], rate=r['rate'], region='Kampala', date=r['date'], source='Market survey', notes=notes))
n_price = len(ops)

# ---- standards register ----
D = json.load(open(K + '/07_Materials/FMC_Materials.json'))
M = D['materials'] + D['raw_materials']
std = collections.defaultdict(list)
for m in M:
    s = (m.get('standard') or '').strip()
    if s: std[s].append(m['name'] if m['name'].startswith('FMC_') else m['name'])
def body(code):
    c = code.upper()
    if 'EAS' in c or c.startswith('DEAS'): return 'EAS'
    if c.startswith('US') : return 'UNBS (US)'
    if 'BS ' in c: return 'BS'
    return 'Other'
def disc(code, mats):
    t = ' '.join(mats).lower()
    for w, d in [('rebar', 'Steel'), ('steel', 'Steel'), ('cement', 'Concrete'), ('concrete', 'Concrete'), ('cable', 'MEP'), ('electrical', 'MEP'), ('pipe', 'MEP'), ('brick', 'Masonry'), ('block', 'Masonry'),
                 ('clay', 'Masonry'), ('timber', 'Timber'), ('pole', 'Timber'), ('roof', 'Materials'), ('road', 'Roads'), ('murram', 'Roads'), ('paint', 'Materials')]:
        if w in t or w in code.lower(): return d
    return 'Materials'
for code, mats in std.items():
    yr = re.search(r':(\d{4})', code) or re.search(r'(?:Code|Specifications for Road and Bridge Works) (\d{4})', code)
    put('reg_standards', 'kit-' + slug(code), dict(code=code, title=f"Cited in the kit for: {', '.join(readable(x) if x.startswith('FMC_') else x for x in mats[:6])}{' and more' if len(mats) > 6 else ''}",
        body=body(code), discipline=disc(code, mats), year=yr.group(1) if yr else '', status='Current', keywords=', '.join(sorted({readable(x).split(' ')[0] if x.startswith('FMC_') else x.split(' ')[0] for x in mats}))[:200],
        summary=f"Referenced by {len(mats)} kit material(s). Title and status not yet checked against the UNBS catalogue (the kit notes UNBS blocked automated access)."))
n_std = len(ops) - n_price

# ---- the full standards bank (319 documents, revit-tools feat/frame-v2 scripts/standards/bank, 27-28 Oct) ----
BANK = json.load(open('/tmp/stdb/bank.json'))
DMAP = {'Structural': 'Structural', 'Geotechnical': 'Geotechnical', 'Fire safety': 'Fire', 'Electrical and lighting': 'MEP', 'Plumbing, drainage and water': 'Water', 'Mechanical, HVAC and lifts': 'MEP',
        'Environment and sustainability': 'Energy', 'Accessibility': 'Accessibility', 'Site safety': 'Health and safety', 'Products: materials': 'Materials', 'Materials (UNBS)': 'Materials',
        'Construction testing and tolerances': 'Materials', 'VDC and BIM management': 'BIM and information', 'BIM data and classification': 'BIM and information', 'CAD and drawing production': 'BIM and information',
        'BIM and documentation': 'BIM and information', 'Revit, Robot and Navisworks': 'BIM and information', 'Products: data for families': 'BIM and information', 'Commissioning and handover': 'BIM and information'}
def sbody(t):
    for p, b in (('ISO', 'ISO'), ('IEC', 'IEC'), ('EN ', 'EN (Eurocode)'), ('Eurocode', 'EN (Eurocode)'), ('BS ', 'BS'), ('ASTM', 'ASTM'), ('ACI', 'ACI'), ('ASCE', 'ASCE'), ('NFPA', 'NFPA'), ('EAS', 'EAS'), ('KS ', 'KEBS'), ('KEBS', 'KEBS'), ('US ', 'UNBS (US)'), ('UNBS', 'UNBS (US)')):
        if t.startswith(p) or (' ' + p) in (' ' + t[:12]): return b
    return 'Other'
CODE = re.compile(r'^((?:ISO/TS|ISO|IEC|EN|BS EN|BS|ACI|ASCE|NFPA|ASTM|US EAS|US|EAS|KS|TZS|RS|AS/NZS|AS|NZS|SANS|IS|GB|JIS|ICC A\d+)\s?[\w\-./:]+(?:[-\u2013]\d+)?)')
seen = {x['data']['code'] for x in ops if x['path'].startswith('reg_standards/')}
nb = 0
for g, title, what, prio, cost, where, have in BANK:
    m = CODE.match(title); code = (m.group(1) if m else title)[:90]
    if code in seen: code = title[:90]
    seen.add(code)
    law = bool(re.search(r'\b(Act|Regulations?|Rules|Code 20\d\d|By-?laws?|Ordinance)\b', title))
    lic = 'Public law or regulation' if law and cost == 'Free' else 'Free to download (link only)' if cost == 'Free' else 'Paid (our licensed copy only)'
    yr = re.search(r'\b(19[5-9]\d|20[0-2]\d)\b', title)
    put('reg_standards', 'bank-' + slug(title), dict(code=code, title=title, body=sbody(title), discipline=DMAP.get(g, 'Architecture'), year=yr.group(1) if yr else '', status='Current',
        keywords=f"{g}; {prio}; {cost}; {'In the bank' if have else 'To get'}", summary=what, uses=f"Priority: {prio}. Group: {g}. {'Formcraft already has this document.' if have else 'Still to get.'}",
        licence=lic, pub='No', buy=where))
    nb += 1
n_std += nb

# ---- suppliers ----
sup = collections.defaultdict(lambda: {'mats': [], 'cat': collections.Counter()})
CATMAP = {'Masonry': 'Blocks and bricks', 'Ceramic': 'Blocks and bricks', 'Roofing': 'Roofing', 'Metal': 'Steel', 'Paint': 'Finishes', 'Plastic': 'Plumbing', 'Board': 'Timber', 'Timber': 'Timber', 'Tile': 'Finishes', 'Stone': 'Finishes', 'Glazing': 'Finishes', 'Window': 'Finishes', 'Electrical': 'Electrical'}
for m in M:
    names = list(m.get('makers') or [])
    if m.get('supplier'): names.append(m['supplier'])
    cls = m.get('class', '') or ''
    for nm in set(n if isinstance(n, str) else n.get('name', '') for n in names):
        if not nm: continue
        key = re.sub(r'\s*\(.*?\)', '', nm).replace(' Ltd', '').replace(' (U)', '').strip()
        key = {'Uganda Baati': 'Uganda Baati (Safal)', 'Crown Paints EA': 'Crown Paints', 'Roofings Polypipes': 'Roofings'}.get(key, key)
        sup[key]['mats'].append(m['name']); sup[key]['cat'][next((v for k, v in CATMAP.items() if k.lower() in cls.lower() or k.lower() in m['name'].lower()), 'Other')] += 1
raw_sup = {'Tororo Cement': 'Cement and aggregates', 'Hima Cement': 'Cement and aggregates'}
for k, c in raw_sup.items():
    if k not in sup: sup[k]['mats'].append('cement'); sup[k]['cat'][c] += 3
for k, v in sup.items():
    if k.startswith('Lion King'): continue
    cat = v['cat'].most_common(1)[0][0] if v['cat'] else 'Other'
    put('reg_suppliers', 'kit-' + slug(k), dict(name=k, category=cat, location='Uganda', notes=f"Named in the Formcraft kit as maker or supplier of: {', '.join(readable(x) if x.startswith('FMC_') else x for x in v['mats'][:8])}. No contact, terms or rating yet."))
n_sup = len(ops) - n_price - n_std

# ---- knowledge base ----
def kb(id_, title, area, body_, link='', recipe='', version='kit 2.2 r4'):
    put('reg_knowledge', id_, dict(title=title, area=area, recipe=recipe, version=version, owner='Emlyn', link=link, body=body_[:9000]))
idx = open(K + '/03_Master_Data/FMC_Rulebook/FMC_Rulebook_Index.md').read()
for f in sorted(glob.glob(K + '/03_Master_Data/FMC_Rulebook/*.json')):
    d = json.load(open(f)); rules = d.get('rules') or d.get('limits') or []
    nm = os.path.basename(f)[:-5].replace('FMC_Rulebook_', '')
    if isinstance(rules, list) and rules and isinstance(rules[0], dict) and 'id' in rules[0]:
        lines = [f"{x['id']} {x.get('title','')}: {x.get('rule','')}" for x in rules]
        srcs = d.get('sources') if isinstance(d.get('sources'), list) else []
        srcs = ', '.join(s if isinstance(s, str) else str(s.get('code') or s.get('name') or s.get('id') or '') for s in srcs)
        b = f"{len(rules)} rules. Sources: {srcs}\n" + '\n'.join(lines)
    else:
        b = json.dumps({k: v for k, v in d.items() if k not in ('schema',)}, ensure_ascii=False)[:6000]
    kb('kit-rulebook-' + slug(nm), f'BIM rulebook: {re.sub(r"(?<=[a-z])(?=[A-Z])", " ", nm)}', 'BIM', b, GH + '03_Master_Data/FMC_Rulebook/' + os.path.basename(f))
kb('kit-rulebook-index', 'BIM rulebook index, gaps and conflicts', 'BIM', idx, GH + '03_Master_Data/FMC_Rulebook/FMC_Rulebook_Index.md')
for f in sorted(glob.glob(K + '/10_Notes/*.txt')):
    nm = os.path.basename(f)[10:-4].split('_', 1)
    kb('kit-notes-' + slug(os.path.basename(f)), f'Drawing general notes: {nm[1] if len(nm) > 1 else nm[0]} ({nm[0]})', 'Studio', open(f).read(), GH + '10_Notes/' + os.path.basename(f))
B = json.load(open(K + '/03_Master_Data/FMC_Standards_Building.json'))
lines = []
for k, v in B['standards'].items():
    s = f"{k}: {v.get('value')}" + (f" (range {v['range'][0]}-{v['range'][1]})" if v.get('range') else '') + (f"; by use {', '.join(f'{a} {b}' for a, b in v['uses'].items())}" if v.get('uses') else '') + (f"; code {v['kit_code']}" if v.get('kit_code') else '') + (f". {v['note']}" if v.get('note') else '')
    lines.append(s)
kb('kit-design-values', 'Typical building design values (proposed, mm)', 'Studio', f"Status: {B['status']}. {B['how']}\n" + '\n'.join(lines), GH + '03_Master_Data/FMC_Standards_Building.json')
fr = list(csv.DictReader(open(K + '/03_Master_Data/FMC_Family_Register.csv')))
roles = collections.Counter(x['Role'] for x in fr); pri = collections.Counter(x['Priority'] for x in fr)
staged = len([p for p in glob.glob(K + '/04_Families/_Staging/*/*.recipe.json')])
S = json.load(open(K + '/03_Master_Data/FMC_Family_Specs.json'))['summary']
kb('kit-family-library', 'Family library: register, recipes and specs', 'BIM',
   f"Family register: {len(fr)} families planned. By role: {', '.join(f'{a} {b}' for a, b in roles.most_common())}. Priority: {', '.join(f'{a} {b}' for a, b in sorted(pri.items()))}.\n"
   f"Specs summary: {json.dumps(S)}.\nStaged family recipes in 04_Families/_Staging: {staged}. Built .rfa files ship as GitHub release zips (latest tag v2.2-2026-10-26), not in git.\n"
   "Each register row: Role, Family, Category, Template, Host, Connectors, KeyParameters, Types, Priority, Why. Full list in FMC_Family_Register.csv.", GH + '03_Master_Data/FMC_Family_Register.csv')
sr = list(csv.DictReader(open(K + '/03_Master_Data/FMC_Sheet_Register.csv')))
kb('kit-sheet-set', 'Standard sheet set (194 sheets in 12 roles)', 'Studio',
   'Sheet roles: ' + ', '.join(f'{a} {b}' for a, b in collections.Counter(x['Role'] for x in sr).most_common()) + '\n' + '\n'.join(f"{x['SheetNumber']} {x['SheetName']} ({x['Scale']}; {x['IssueSet']})" for x in sr), GH + '03_Master_Data/FMC_Sheet_Register.csv')
codes = json.load(open(K + '/03_Master_Data/FMC_Master_Data.json'))['codes']
kb('kit-work-codes', f'Kit work codes (keynotes): {len(codes)} items with units', 'BIM',
   'Element codes X.YYY_ZZ used for keynotes, quantities and BoQ. Rates are not yet filled in the kit (rate, waste, rate_source are empty): the Price book holds the rates for now.\n' + '\n'.join(f"{k} [{v['unit']}] {v['description']}" for k, v in codes.items()), GH + '03_Master_Data/FMC_Master_Data.json')
scripts = [('pyRevit FMC tab', '05_Scripts/pyRevit/FMC.extension', 'Buttons: 1 Setup electrical, 2 Create sheets, 3 Sheet QA, 4 Project metrics, 5 Linked loads.'),
           ('Dynamo scripts', '05_Scripts/Dynamo', 'FMC_ExportQTO (quantities out), FMC_BindSharedParameters, FMC_ModelHealth, FMC_SyncMasterData.'),
           ('Kit tools', '05_Scripts/tools', 'fmc_new_project (project folder and model start), fmc_boq_build (BoQ from quantities and codes), fmc_name_check (naming rules), fmc_publish_master (publish master data). Template: steel_mass_template.csv.')]
kb('kit-scripts', 'Kit scripts: pyRevit, Dynamo and tools', 'Software', '\n'.join(f'{a} ({b}): {c}' for a, b, c in scripts), GH + '05_Scripts')
kb('kit-ifc-ids', 'IFC property sets and IDS checks (design and handover)', 'BIM', 'FMC_IFC_PropertySets.txt maps Formcraft parameters to IFC. FMC_Design_Base.ids and FMC_Handover_Base.ids are the information-delivery checks for the design stage and the handover model.', GH + '07_IFC_IDS')
kb('kit-materials-library', f"Material library: {len(D['materials'])} materials and {len(D['raw_materials'])} raw materials", 'BIM',
   f"Each material has class, keynote code, cost code, graphics, texture maps, discipline, description, makers, origin, standard and price. {sum(1 for m in M if m.get('price'))} have prices (now in the Price book). {len(D['new_keynotes'])} new keynotes proposed.\nResearch gaps recorded in the kit:\n- " + '\n- '.join(D['gaps']), GH + '07_Materials/FMC_Materials.json')
kb('kit-overview', 'Formcraft BIM kit v2.2 r4: what is in it', 'BIM',
   "Standard: FMC-BIM-MAN-001 v2.2 (Master Manual and BEP) and FMC-BIM-STD-002 v2.2 (families, sheets, annotation). Folders: 01 shared parameters (178 in 30 groups), 02 keynotes, 03 master data (codes, family register and specs, sheet register, legends, rulebooks, design values, recipes), 04 families (staged recipes; built families in releases), 05 scripts, 06 patterns and templates (Base + 12 role templates), 07 IFC/IDS and materials (with textures), 08 Navisworks, 09 manual and training, 10 drawing notes, 11 brand lockups. Build and test: _build/build_all.py and test_kit.py. Update packages r1-r6 in _updates.", 'https://github.com/formcraft/formcraft-kit')
n_kb = len(ops) - n_price - n_std - n_sup

# ---- rulebook kit ----
put('reg_kits', 'fmc-kit-2-2', dict(code='FMC-KIT-2.2', name='Formcraft BIM kit v2.2 r4 (2026-10-15; tag v2.2-2026-10-26)', level='L2 AI does - human checks all', recipes=f'{staged} staged family recipes; 344 BIM rules in 13 rulebooks', approver='Emlyn', notes='Rulebook kit for Revit work: rules, codes, families, templates, materials and scripts. Its rules feed the Revit plugin and the AI.'))

# ---- tasks from the gaps ----
unpriced = [m['name'] for m in D['materials'] if not m.get('price')]
T = [('Get supplier quotes for the secondary prices in the Price book', 'P1', f"{sum(1 for r in P['rows'] if r['_flag']=='secondary source')} kit prices come from websites (Aura Build, Smeaton, Lexa, Jiji). Confirm them with real quotes before using them in a BoQ."),
     ('Ask the QS to confirm the flagged rates', 'P1', 'Cement varies 32,000-47,000 between sheets; concrete adds 54% shrinkage; plaster swaps mason and labourer wages; BRC rate leaves out labour; floor finish stops before profit; concrete mix 1:1:1.5 grade; timber formwork unit.'),
     (f'Price the {len(unpriced)} kit materials that have no price', 'P2', 'Examples: ' + ', '.join(readable(x) for x in unpriced[:12]) + '...'),
     ('Fill rates for the kit work codes from the Price book', 'P2', '303 codes in FMC_Master_Data.json have empty rate fields. Map the QS all-in rates (blockwork, concrete, plaster, roofing...) to their codes in a kit update.'),
     ('Make the formcraft-kit repository private', 'P1', 'The kit README says it is private firm data, but github.com/formcraft/formcraft-kit is public. Same check for formcraft-revit-tools.')]
for i, (t, pr, d) in enumerate(T):
    put('todos', f'kit-task-{i+1}', dict(t=t, kind='Task', owner='', due='2026-11-13', area='Projects' if i < 4 else 'Software', pri=pr, status='To do', date=TODAY, notes=d))
print(dict(price=n_price, standards=n_std, suppliers=n_sup, knowledge=n_kb, total=len(ops)))
out = collections.defaultdict(list)
for o in ops:
    c, i = o['path'].split('/'); out[c].append(dict(id=i, **o['data']))
json.dump(out, open('/tmp/qs/Formcraft-Kit-Import-2026-10-30.json', 'w'), ensure_ascii=False, indent=1)
print({k: len(v) for k, v in out.items()}, os.path.getsize('/tmp/qs/Formcraft-Kit-Import-2026-10-30.json'))
