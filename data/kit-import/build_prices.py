"""Builds the Formcraft price database from (1) the kit's researched prices (Ogala field review, Oct 2026)
and (2) the quantity surveyor's rate build-ups (Civil_Material_Price_List.xlsx, saved 24 Jun 2026).
Output: prices.json (rows for the Command Centre price book) and Formcraft_Price_Database_2026-10.xlsx (review)."""
import json, re, openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
KIT = '/home/claude/formcraft/formcraft-kit/FMC_Kit_v2.2/07_Materials/FMC_Materials.json'
QS = '/tmp/qs/qs.xlsx'
QSDATE = '2026-06-24'
wb = openpyxl.load_workbook(QS, data_only=True)

def val(sheet, label, col=1, nth=0):
    """Value next to the nth row whose first cell starts with label."""
    n = 0
    for row in wb[sheet].iter_rows(values_only=True):
        if row[0] and str(row[0]).strip().lower().startswith(label.lower()):
            if n == nth: return row[col]
            n += 1
    raise KeyError((sheet, label))

rows = []
def add(item, cat, unit, rate, date, source, notes, origin, low=None, high=None, flag=''):
    rows.append(dict(item=item, category=cat, unit=unit, rate=round(rate), supplier='', region='Kampala', date=date, source=source,
                     notes=notes, _origin=origin, _low=low, _high=high, _flag=flag))

# ---------------- 1. Kit prices (Ogala field review research) ----------------
CAT = {'Concrete': 'Cement and concrete', 'Cement': 'Cement and concrete', 'Metal': 'Steel', 'Masonry': 'Blocks', 'Ceramic': 'Finishes',
       'Timber': 'Timber', 'Wood': 'Timber', 'Board': 'Timber', 'Roofing': 'Roofing', 'Paint': 'Finishes', 'Glass': 'Finishes', 'Stone': 'Aggregates',
       'Aggregate': 'Aggregates', 'Plastic': 'Plumbing', 'Gypsum': 'Finishes', 'Tile': 'Finishes', 'Insulation': 'Roofing', 'Membrane': 'Roofing'}
def kcat(m, name):
    c = m.get('class', '') or ''
    for k, v in CAT.items():
        if k.lower() in c.lower(): return v
    n = name.lower()
    for w, v in [('cement', 'Cement and concrete'), ('sand', 'Aggregates'), ('aggregate', 'Aggregates'), ('stone', 'Aggregates'), ('ballast', 'Aggregates'), ('hardcore', 'Aggregates'),
                 ('steel', 'Steel'), ('rebar', 'Steel'), ('wire', 'Steel'), ('nail', 'Steel'), ('timber', 'Timber'), ('plywood', 'Timber'), ('block', 'Blocks'), ('brick', 'Blocks'),
                 ('lime', 'Cement and concrete'), ('sheet', 'Roofing'), ('tile', 'Finishes'), ('paint', 'Finishes'), ('pipe', 'Plumbing'), ('cable', 'Electrical')]:
        if w in n: return v
    return 'Finishes'
def nums(s):
    out = []
    for p in re.split(r'\s*[-–]\s*', s):
        p = re.sub(r'[^\d.]', '', p)
        if p: out.append(float(p))
    return out
def kdate(d):
    if re.match(r'^\d{4}-\d{2}-\d{2}$', d): return d
    if re.match(r'^\d{4}-\d{2}$', d): return d + '-01'
    return ''
K = json.load(open(KIT))
for kind, L in (('material', K['materials']), ('raw', K['raw_materials'])):
    for m in L:
        p = m.get('price')
        if not p or not p.get('ugx'): continue
        v = nums(str(p['ugx']).split(' ')[0] if ' ' in str(p['ugx']).strip() and not re.search(r'\d\s*[-–]\s*\d', str(p['ugx'])) else str(p['ugx']))
        if not v: continue
        lo, hi = v[0], v[-1]
        name = m['name'] if kind == 'material' else m['name']
        spec = m.get('spec', '') if kind == 'raw' else ''
        st = p.get('status', '')
        src = p.get('source', '')
        notes = f"Kit {'material' if kind=='material' else 'raw material'} {m['name'] if kind=='material' else ''}".strip()
        notes = (f"Range UGX {int(lo):,}-{int(hi):,}; rate is the midpoint. " if hi != lo else '') + f"Price {st}. Unit detail: {p.get('unit','')}. {('Spec: ' + spec + '. ') if spec else ''}From the Formcraft kit (researched for the Ogala Residence review, Oct 2026). Source: {src}"
        add(name if kind == 'raw' else name, kcat(m, name), p.get('unit', '').split(',')[0].split('(')[0].strip()[:40] or 'unit', (lo + hi) / 2,
            kdate(p.get('date', '')), 'Website', notes, 'kit-' + kind, lo, hi, '' if st == 'verified' else 'secondary source')

# ---------------- 2. QS: base prices, labour, plant ----------------
q = 'QS rate analysis, Civil_Material_Price_List.xlsx (saved 24 Jun 2026)'
lab_s = val('Built up labour rate', 'Total cost per day', 5) if False else None
LAB = wb['Built up labour rate']
lr = [r for r in LAB.iter_rows(values_only=True)]
skilled = [r[5] for r in lr if r[4] == 'Total cost per day'][0]
semi = [r[1] for r in lr if r[0] == 'Total cost per day'][0]
unsk = [r[1] for r in lr if r[0] == 'Total cost per day'][1]
add('Skilled labour (mason, carpenter), per day', 'Labour', 'day', skilled, QSDATE, 'Market survey', f'Basic UGX 30,000 a day plus NSSF 7.5%, third-party assurance 2.5%, guaranteed time 2%, sick benefit 0.5% (spread weekly). {q}', 'qs-labour')
add('Semi-skilled labour, per day', 'Labour', 'day', semi, QSDATE, 'Market survey', f'Basic UGX 15,000 a day plus the same statutory add-ons. {q}', 'qs-labour')
add('Unskilled labour (porter), per day', 'Labour', 'day', unsk, QSDATE, 'Market survey', f'Basic UGX 10,000 a day plus the same statutory add-ons. {q}', 'qs-labour')
add('Excavator hire (0.5 m3 bucket), per day', 'Plant hire', 'day', val('Excavator rates', 'excavator hire price'), QSDATE, 'Market survey', f'Dry hire. Fuel about 120 L a day extra; operator UGX 150,000 a day. Output about 498 m3 a day. {q}', 'qs-plant')
add('Excavator operator, per day', 'Labour', 'day', val('Excavator rates', 'Operator'), QSDATE, 'Market survey', q, 'qs-plant')
add('Diesel for plant, per litre', 'Plant hire', 'litre', val('Excavator rates', 'Fuel (litre)'), QSDATE, 'Market survey', q, 'qs-plant')

base = [
 ('Cement 50 kg bag (concrete works)', 'Cement and concrete', 'bag', val('Concrete rate', 'Cost of a cement bag'), 'Delivered UGX 49,000 with transport UGX 1,000 and offloading UGX 1,000 a bag (truck of 100 bags).', 'cement-high'),
 ('Cement 50 kg bag (blockwork sheet)', 'Cement and concrete', 'bag', val('Blockwork', 'Cement bag cost'), 'Delivered UGX 34,000 (UGX 200,000 transport for 100 bags).', 'cement-low'),
 ('Cement 50 kg bag (plaster and lime sheets)', 'Cement and concrete', 'bag', val('Plastering', 'Cement bag cost'), 'Delivered UGX 38,000 in the plastering sheet.', 'cement-mid'),
 ('Sand, per lorry trip (concrete sheets)', 'Aggregates', 'trip', val('Concrete rate', 'Cost of a sand'), 'Plus UGX 80,000 transport; about 3 tonnes a trip. Works out at about UGX 149,000 per m3 delivered.', ''),
 ('Sand, per Elf trip delivered (about 2 t)', 'Aggregates', 'trip', val('Plastering', 'Cost of sand'), 'Transport included; about UGX 190,000 a tonne.', ''),
 ('Aggregates (stone), per lorry trip', 'Aggregates', 'trip', val('Concrete rate', 'Cost of a sand', 1, 1), 'Plus UGX 100,000 transport; about 4 tonnes a trip. About UGX 131,000 per m3 delivered.', ''),
 ('Hardcore, per Elf trip delivered (about 2.5 t)', 'Aggregates', 'trip', val('Hardcore', 'Cost of hadcore'), 'Transport included; about UGX 152,000 a tonne.', ''),
 ('Pozzolana natural stone, per trip (about 2.5 t)', 'Aggregates', 'trip', val('Natural stone (Pozzolana)', 'cost'), 'About UGX 260,000 a tonne.', ''),
 ('Concrete block 400 x 200 x 200, at the yard', 'Blocks', 'block', val('Blockwork', 'Cost of brick/blocks'), 'Delivered about UGX 1,500 each after transport (UGX 100,000 for 200) and loading UGX 500. About 11.2 blocks per m2.', ''),
 ('Hydrated lime, 25 kg bag', 'Cement and concrete', 'bag', val('Pigmented lime plaster', 'Lime bag cost'), 'Plus about UGX 3,333 transport a bag (UGX 100,000 for 30).', ''),
 ('Termidor anti-termite concentrate, 200 ml', 'Finishes', 'bottle', val('Anti-termite', 'Termidor price'), 'About UGX 3,750 per m2 treated at 5 L of solution per m2.', ''),
 ('Timber 100 x 50 mm, 3.6 m (formwork)', 'Timber', 'piece', val('Formwork timber', 'Timber cost'), '', ''),
 ('Plywood 18 mm, 1.2 x 2.4 m (formwork sheet)', 'Timber', 'sheet', val('Formwork sheets', 'Timber cost'), 'About UGX 22,600 per m2.', ''),
 ('Eucalyptus rafter 40 x 100 mm, 3.6 m', 'Timber', 'piece', val('Rafters', 'Cost of rafter'), 'Transport about UGX 500 a rafter (UGX 100,000 for 200) plus loading UGX 1,000.', ''),
 ('BRC mesh sheet 2.44 x 1.22 m (G-10)', 'Steel', 'sheet', val('BRC MESH', 'Timber cost'), 'About UGX 11,400 per m2 delivered.', ''),
 ('Reinforcement bar Y10, 12 m', 'Steel', 'bar', val('Reinforcements', 'rc cost'), 'About 7.4 kg a bar, UGX 3,780 a kg.', ''),
 ('Mild steel plate 4 mm, 1.22 x 2.44 m', 'Steel', 'plate', val('Mild steel plates', 'Cost per plate'), 'About 93.5 kg a plate, UGX 4,050 a kg delivered.', ''),
 ('Steel hollow section 70 x 70 x 6 mm, 6 m', 'Steel', 'length', val('Steel Hollow sections', 'rc cost'), 'About 37.9 kg a length, UGX 6,250 a kg delivered.', ''),
 ('PVC fascia board 220 mm, 5.8 m', 'Roofing', 'length', val('Fascia board', 'Cost of Fascia board'), 'About UGX 11,050 per m delivered.', ''),
 ('Iron roofing sheet G26, 5 m x 0.7 m cover', 'Roofing', 'sheet', val('Iron sheets', 'Cost per sheet'), 'About UGX 39,000 per m2 delivered.', ''),
 ('Floor finish (90 x 20 x 900 boards), supply', 'Finishes', 'm2', val('Finishes', 'Cost per square meter'), 'Transport about UGX 1,250 per m2. Product not named in the sheet (likely timber decking or flooring): confirm with the QS.', 'unnamed'),
 ('Emulsion paint, 3 coats, materials per m2', 'Finishes', 'm2', val('Paint', 'Coverage per square meter'), 'UGX 94,800 per litre for 3 coats at 10 m2 a litre; labour UGX 9,000 per m2 extra.', ''),
]
for it, cat, unit, r, n, fl in base:
    flag = {'cement-high': 'cement price differs between sheets (32,000-47,000)', 'cement-low': 'cement price differs between sheets (32,000-47,000)', 'cement-mid': 'cement price differs between sheets (32,000-47,000)', 'unnamed': 'product not named'}.get(fl, '')
    add(it, cat, unit, r, QSDATE, 'Market survey', (n + ' ' if n else '') + q, 'qs-material', flag=flag)

# ---------------- 3. QS: built-up unit rates (all-in) ----------------
def last(sheet, label):
    return val(sheet, label)
unit_rates = [
 ('Concrete 1:3:6 (C15 blinding / mass), all-in', 'Cement and concrete', 'm3', last('Concrete rate', 'Add profits and overheads'), 'Materials, labour, plant 5%, profit and overheads 20%. Note: the sheet adds 54% shrinkage on the materials.', 'check'),
 ('Concrete 1:1:1.5 (structural), all-in', 'Cement and concrete', 'm3', last('Concrete materials', 'Profit and overheads 20%') if False else [r for r in wb['Concrete materials'].iter_rows(values_only=True) if r[0] == 'Profit and overheads 20%'][0][4], 'Materials (cement at UGX 50,000 delivered), labour, plant 5%, profit and overheads 20%. Mix 1:1:1.5 as entered: confirm the intended grade with the QS.', 'check'),
 ('Blockwork 200 mm in 1:3 mortar, all-in', 'Blocks', 'm2', [r for r in wb['Blockwork'].iter_rows(values_only=True) if r[5] == 'Profit and overheads 20%'][0][9], 'About 11.2 blocks per m2 at UGX 1,500 delivered, mortar, labour, plant 3%, profit 20%.', ''),
 ('Cement-sand plaster 20 mm (1:4), all-in', 'Finishes', 'm2', last('Plastering', 'Profit 15%'), 'Materials, labour, plant 3%, wastage, profit 15%. Note: the sheet swaps the mason and labourer wages.', 'check'),
 ('Emulsion paint, 3 coats, supply and apply', 'Finishes', 'm2', val('Paint', 'Coverage per square meter') + val('Paint', 'Labour per square meter'), 'Materials UGX 9,480 plus labour UGX 9,000 per m2. No profit added.', ''),
 ('Anti-termite treatment (Termidor)', 'Finishes', 'm2', val('Anti-termite', 'Cost per square meter'), 'Chemical only, at 5 L of solution per m2. No labour or profit added.', ''),
 ('Hardcore filling, compacted, all-in', 'Aggregates', 'm3', last('Hardcore', 'Profit 15%'), 'Hardcore and sand blinding, labour, plant 3%, wastage 10%, profit 15%.', ''),
 ('Excavation by machine, all-in', 'Plant hire', 'm3', last('Excavator rates', 'Add profit 20%'), 'Excavator, fuel, operator, labourer; profit 20%.', ''),
 ('Stone plinth wall (rubble in 1:4 mortar), all-in', 'Blocks', 'm3', last('Stone plinth wall', 'Profit 20%'), 'Mortar 30%, stone 70%, labour, plant 3%, wastage 10%, profit 20%.', ''),
 ('Pozzolana natural stone cladding, all-in', 'Finishes', 'm2', last('Natural stone (Pozzolana)', 'Profit 15%'), 'Stone, mortar, labour, plant 3%, wastage 10%, profit 15%.', ''),
 ('Formwork, timber 100 x 50, all-in', 'Timber', 'm', last('Formwork timber', 'Profit 15%'), 'Timber, labour, plant 3%, wastage 10%, profit 15%. Unit as given in the sheet: confirm per m or per m2.', 'check'),
 ('Formwork, 18 mm plywood, all-in', 'Timber', 'm2', last('Formwork sheets', 'Profit 15%'), 'Plywood, labour, plant 3%, wastage 10%, profit 15%. Single use assumed.', ''),
 ('BRC mesh in slabs, fix, all-in', 'Steel', 'm2', last('BRC MESH', 'Profit 20%'), 'Mesh, plant 3%, wastage 10%, profit 20%. Note: the sheet does not add the labour it works out.', 'check'),
 ('Reinforcement, cut, bend and fix, all-in', 'Steel', 'kg', last('Reinforcements', 'Profit 20%'), 'Bar, labour UGX 1,000 per kg, plant 3%, wastage 10%, profit 20%.', ''),
 ('Mild steel plate work, all-in', 'Steel', 'kg', last('Mild steel plates', 'Profit 20%'), 'Plate, labour, plant 3%, wastage 10%, profit 20%.', ''),
 ('Steel hollow section work, all-in', 'Steel', 'kg', last('Steel Hollow sections', 'Profit 20%'), 'Section, labour UGX 1,400 per kg, plant 3%, wastage 10%, profit 20%.', ''),
 ('PVC fascia board 220 mm, fixed, all-in', 'Roofing', 'm', last('Fascia board', 'Profit 20%'), 'Board, labour, plant 3%, wastage 10%, profit 20%.', ''),
 ('Eucalyptus rafters 40 x 100, fixed, all-in', 'Timber', 'm', last('Rafters', 'Profit 15%'), 'Rafter, labour, plant 3%, wastage 10%, profit 15%.', ''),
 ('Iron sheet roofing G26, fixed, all-in', 'Roofing', 'm2', last('Iron sheets', 'Profit 20%'), 'Sheet, labour, plant 5%, wastage 10%, profit 20%.', ''),
 ('Floor finish (90 x 20 boards), laid, before profit', 'Finishes', 'm2', last('Finishes', 'Add material wastage 10%'), 'Supply, transport, labour, plant 3%, wastage 10%. The sheet stops before profit.', 'check'),
]
for it, cat, unit, r, n, fl in unit_rates:
    add(it, cat, unit, r, QSDATE, 'Market survey', f'All-in unit rate. {n} {q}', 'qs-unitrate', flag='check with the QS' if fl else '')

# general percentages and insurance as notes rows (kept out of the rate list but recorded)
INS = {'car': val('Insurance', 'Market rate %', 1, 0), 'tpl': val('Insurance', 'Market rate %', 1, 1), 'wc': val('Insurance', 'Market rate %', 1, 2), 'pi': val('Insurance', 'Market rate %', 1, 3), 'all': val('Insurance', 'Insurance %')}
json.dump({'rows': rows, 'insurance': INS}, open('/tmp/qs/prices.json', 'w'), indent=1)

# ---------------- review workbook ----------------
out = openpyxl.Workbook(); ws = out.active; ws.title = 'Price database'
H = ['Item', 'Category', 'Unit', 'Rate (UGX)', 'Low', 'High', 'Price date', 'Source type', 'From', 'Check', 'Notes']
ws.append(H)
for r in rows:
    ws.append([r['item'], r['category'], r['unit'], r['rate'], r['_low'], r['_high'], r['date'], r['source'], {'kit-material': 'Kit (Ogala review)', 'kit-raw': 'Kit (Ogala review)'}.get(r['_origin'], 'QS workbook'), r['_flag'], r['notes']])
for c in ws[1]: c.font = Font(bold=True, color='FFFFFF'); c.fill = PatternFill('solid', fgColor='1B2532')
for col, w in zip('ABCDEFGHIJK', [46, 20, 12, 13, 11, 11, 12, 14, 18, 30, 110]): ws.column_dimensions[col].width = w
for row in ws.iter_rows(min_row=2):
    for c in row[3:6]: c.number_format = '#,##0'
    if row[9].value: row[9].fill = PatternFill('solid', fgColor='FDECD2')
ws.freeze_panes = 'A2'; ws.auto_filter.ref = ws.dimensions
w2 = out.create_sheet('Insurance (QS)')
w2.append(['Cover', 'Market rate %']); [w2.append(x) for x in [("Contractor's All Risks", INS['car']), ('Third-party liability', INS['tpl']), ("Workmen's compensation", INS['wc']), ('Professional indemnity', INS['pi']), ('All-in insurance as % of contract sum (sample project)', round(INS['all'], 2))]]
w2.column_dimensions['A'].width = 52
out.save('/tmp/qs/Formcraft_Price_Database_2026-10.xlsx')
from collections import Counter
print(len(rows), Counter(r['_origin'] for r in rows), 'flags', sum(1 for r in rows if r['_flag']))
