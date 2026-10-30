"""Builds the branded Formcraft feasibility report and the branded professional profile.
Run: python3 tools/build_report.py   (needs pypdf, reportlab, playwright with Chromium, pdftotext)"""
import json, subprocess, io, os, base64, datetime
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from playwright.sync_api import sync_playwright
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAVY, TEAL = '#1b2532', '#7fc7be'
def b64(p): return base64.b64encode(open(p, 'rb').read()).decode()
LOGO = b64(f'{R}/branding/logos/Formcraft-main.png'); LOGOW = b64(f'{R}/branding/logos/Formcraft-white.png')
DIVS = [b64(f'{R}/branding/logos/{n}.png') for n in ('Studio', 'Construction', 'Concrete', 'Stores')]
TODAY = datetime.date.today().strftime('%d %B %Y')

def page_of(pdf, headings):
    out = {}
    n = len(PdfReader(pdf).pages)
    for i in range(1, n + 1):
        t = subprocess.run(['pdftotext', '-f', str(i), '-l', str(i), '-layout', pdf, '-'], capture_output=True, text=True).stdout
        flat = ' '.join(t.split())
        for h in headings:
            if h not in out and ' '.join(h.split()) in flat: out[h] = i
    return out

def html_pdf(html, path):
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(); pg.set_content(html, wait_until='load')
        pg.pdf(path=path, format='A4', print_background=True, margin={'top': '0', 'bottom': '0', 'left': '0', 'right': '0'}); b.close()

CSS = f"""@page{{size:A4;margin:0}}*{{box-sizing:border-box}}body{{margin:0;font-family:'Segoe UI',Inter,Helvetica,Arial,sans-serif;color:{NAVY}}}
.pg{{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;padding:22mm 20mm}}
.cover{{background:{NAVY};color:#fff;padding:0}}.cover .band{{position:absolute;left:0;right:0;bottom:0;height:9mm;background:{TEAL}}}
.cover .logo{{position:absolute;left:20mm;top:22mm;width:78mm}}.cover h1{{position:absolute;left:20mm;top:96mm;font-size:34pt;line-height:1.08;margin:0;font-weight:700;letter-spacing:-.5px}}
.cover .sub{{position:absolute;left:20mm;top:150mm;font-size:13pt;color:{TEAL};max-width:150mm;line-height:1.45}}
.cover .meta{{position:absolute;left:20mm;bottom:20mm;font-size:10pt;color:#cfd6dc;line-height:1.7}}
.cover .shape{{position:absolute;right:-30mm;top:40mm;width:120mm;height:120mm;border:2px solid rgba(127,199,190,.35);border-radius:28mm;transform:rotate(18deg)}}
.cover .shape2{{position:absolute;right:10mm;top:70mm;width:70mm;height:70mm;background:rgba(127,199,190,.12);border-radius:16mm;transform:rotate(18deg)}}
.hdr{{display:flex;justify-content:space-between;align-items:center;border-bottom:1.5px solid {TEAL};padding-bottom:4mm;margin-bottom:8mm}}.hdr img{{height:7mm}}.hdr span{{font-size:8.5pt;color:#6b7680}}
h2{{font-size:20pt;margin:0 0 5mm}}h3{{font-size:12pt;margin:6mm 0 2mm}}p,li{{font-size:10.3pt;line-height:1.55}}
table{{width:100%;border-collapse:collapse;font-size:9.4pt;margin:3mm 0}}th{{background:{NAVY};color:#fff;text-align:left;padding:2.2mm 2.5mm;font-weight:600}}td{{padding:2mm 2.5mm;border-bottom:1px solid #dde3e7}}td.n{{text-align:right;font-variant-numeric:tabular-nums}}
.kpis{{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin:4mm 0}}.kpi{{border:1px solid #dde3e7;border-left:4px solid {TEAL};border-radius:2mm;padding:3mm}}.kpi b{{display:block;font-size:17pt}}.kpi span{{font-size:8.5pt;color:#5b6670}}
.note{{background:#eef6f5;border-left:4px solid {TEAL};padding:3mm 4mm;font-size:9.6pt;line-height:1.5;margin:4mm 0}}
.toc a{{display:flex;justify-content:space-between;border-bottom:1px dotted #b9c3ca;padding:1.6mm 0;font-size:10.5pt;color:{NAVY};text-decoration:none}}
.foot{{position:absolute;left:20mm;right:20mm;bottom:12mm;font-size:8pt;color:#6b7680;display:flex;justify-content:space-between}}
.divs{{position:absolute;left:20mm;right:20mm;bottom:58mm;display:flex;gap:9mm;align-items:center;opacity:.95}}.divs img{{height:8mm;filter:brightness(0) invert(1)}}"""

def overlay(src, dst, label, start_no=1):
    rd = PdfReader(src); wr = PdfWriter()
    mark = ImageReader(f'{R}/branding/logos/Formcraft-main.png')
    for i, p in enumerate(rd.pages):
        w, h = float(p.mediabox.width), float(p.mediabox.height)
        buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(w, h))
        c.drawImage(mark, w - 36 - 74, h - 30, width=74, height=74 / 4.604, mask='auto')
        c.setStrokeColor(TEAL); c.setLineWidth(1.2); c.line(36, 28, w - 150, 28)
        c.setFont('Helvetica', 7.2); c.setFillColor('#6b7680'); c.drawString(36, 18, f'Formcraft Design and Construction  ·  {label}  ·  Confidential')
        c.save(); buf.seek(0)
        p.merge_page(PdfReader(buf).pages[0]); wr.add_page(p)
    wr.write(dst)

def merge(parts, dst):
    wr = PdfWriter()
    for f in parts:
        for p in PdfReader(f).pages: wr.add_page(p)
    wr.add_metadata({'/Title': os.path.basename(dst), '/Author': 'Formcraft Design and Construction'})
    wr.write(dst)

def build_feasibility():
    body = f'{R}/feasibility/source/Formcraft-Pioneer.pdf'
    heads = [l[3:].strip() for l in open(f'{R}/feasibility/source/Formcraft-Pioneer.md', encoding='utf-8') if l.startswith('## ')]
    pages = page_of(body, heads)
    S = json.load(open(f'{R}/simulations/fcrun11.json'))
    order = ['Run 10 plan (no Command Centre)', 'Plan + Command Centre (65% chance it is fully used)', 'Plan + Command Centre used every day', 'Plan + Command Centre, best practice', 'Plan + Command Centre, sceptic', 'Plan + Command Centre, growth capped at 10% a year after 2036']
    pc = lambda v: f'{v*100:.1f}%'
    rows = ''.join(f"<tr><td>{k}</td><td class=n>{pc(S[k]['alive2036'])}</td><td class=n>{pc(S[k]['p1m2031'])}</td><td class=n>{pc(S[k]['p100'])}</td><td class=n><b>{pc(S[k]['p1b'])}</b></td></tr>" for k in order)
    FRONT = 4
    toc = ''.join(f"<a><span>{h}</span><span>{pages[h] + FRONT if h in pages else ''}</span></a>" for h in heads)
    k = S[order[1]]
    bars = ''.join(f"<div style='display:flex;align-items:center;gap:3mm;margin:1.6mm 0;font-size:9pt'><span style='width:62mm'>{lab}</span><div style='flex:1;background:#eef1f3;height:5mm;border-radius:1mm'><div style='width:{S[key]['p1b']/0.4*100:.0f}%;max-width:100%;height:5mm;background:{col};border-radius:1mm'></div></div><b style='width:13mm;text-align:right'>{pc(S[key]['p1b'])}</b></div>" for lab, key, col in [('Sceptic settings', order[4], '#c0392b'), ('Growth capped after 2036', order[5], '#b7791f'), ('Run 10 plan, no Command Centre', order[0], '#8a96a0'), ('With the Command Centre (likely use)', order[1], TEAL), ('Command Centre used every day', order[2], TEAL), ('Command Centre and best practice', order[3], NAVY)])
    hdr = f"<div class=hdr><img src='data:image/png;base64,{LOGO}'><span>Feasibility report · {TODAY}</span></div>"
    html = f"""<html><head><meta charset=utf-8><style>{CSS}</style></head><body>
<div class='pg cover'><div class=shape></div><div class=shape2></div><img class=logo src='data:image/png;base64,{LOGOW}'>
<h1>Feasibility Report<br>and Pioneer Plan</h1><div class=sub>Making Formcraft Design and Construction a leading firm in East Africa: strategy, systems, AI plan, legal and financial plans, and Monte Carlo simulations of the road to a billion.</div>
<div class=divs>{''.join(f"<img src='data:image/png;base64,{d}'>" for d in DIVS)}</div>
<div class=meta>Prepared by Formcraft Design and Construction Co. Ltd<br>Kampala, Uganda · {TODAY}<br>For partners, investors and advisers</div><div class=band></div></div>
<div class=pg>{hdr}<h2>About this report</h2>
<p>This report sets out how Formcraft Design and Construction can become a leading design, BIM and construction firm in East Africa, and what it would take to reach USD 1 billion of lifetime revenue. It brings together the Formcraft Pioneer plan: where Formcraft stands, the Formcraft Tools and Revit system, the client portal, AI in every function under the rulebook method, Porter's value chain, the content engine, the legal, financial, sales and project-management plans, the standards bank and the Formcraft Command Centre.</p>
<p>Every forecast in it comes from Monte Carlo simulations of about one million possible futures per scenario, built on the plan's own assumptions. They are tools for comparing choices, not promises. The near-term figures (survival, revenue by 2031 and 2036) are the most reliable; lifetime figures to 2072 rest on decades of assumed growth and should be read as soft.</p>
<h3>How to read it</h3><ul><li>Front pages: this introduction, the latest simulation (run 11, including the Command Centre) and the contents.</li><li>Main body: the full Pioneer plan, with every chart and simulation run.</li></ul>
<div class=note>Figures for tax, law and incentives in Uganda were checked at the time of writing and change with each budget. Confirm with a tax adviser or lawyer before acting.</div>
<div class=foot><span>Formcraft Design and Construction</span><span>2</span></div></div>
<div class=pg>{hdr}<h2>Run 11: the chance of a billion, with the Command Centre</h2>
<p>Run 11 repeats run 10 (the full plan with the standards bank) and adds the Formcraft Command Centre. If it is used, it improves execution, quoting speed, error rates, cash control and key-person cover. It also costs build time in 2027 and 2028, and there is a real chance it is only half used. Six scenarios, 1,000,000 simulated futures each.</p>
<div class=kpis><div class=kpi><b>{pc(k['alive2036'])}</b><span>still running in 2036</span></div><div class=kpi><b>{pc(k['p1m2031'])}</b><span>at USD 1M a year by 2031</span></div><div class=kpi><b>{pc(k['p100'])}</b><span>reach USD 100M lifetime</span></div><div class=kpi><b>{pc(k['p1b'])}</b><span>reach USD 1B lifetime</span></div></div>
<table><tr><th>Scenario</th><th>Running 2036</th><th>USD 1M/yr by 2031</th><th>USD 100M life</th><th>USD 1B life</th></tr>{rows}</table>
<h3>Chance of USD 1 billion lifetime revenue</h3>{bars}
<div class=note><b>Reading it honestly.</b> The Command Centre adds about 1 point to the billion odds ({pc(S[order[0]]['p1b'])} to {pc(k['p1b'])}): it is a multiplier on execution, not a strategy. The biggest levers are still practices (best practice: {pc(S[order[3]]['p1b'])}) and whether growth keeps going for decades: capping growth at 10% a year after 2036 drops the odds to {pc(S[order[5]]['p1b'])}, and sceptic settings to {pc(S[order[4]]['p1b'])}. The model is calibrated to the plan, not to the record of real firms; across all companies, reaching USD 1 billion of lifetime revenue is far rarer than these numbers suggest. Treat 2031 and 2036 results as the real test: about one future in four reaches USD 1M a year by 2031.</div>
<div class=foot><span>Formcraft Design and Construction</span><span>3</span></div></div>
<div class=pg>{hdr}<h2>Contents</h2><div class=toc>{toc}</div><div class=foot><span>Formcraft Design and Construction</span><span>4</span></div></div>
</body></html>"""
    os.makedirs('/tmp/fr', exist_ok=True)
    html_pdf(html, '/tmp/fr/front.pdf')
    overlay(body, '/tmp/fr/body.pdf', 'Feasibility report and Pioneer plan')
    back = f"""<html><head><meta charset=utf-8><style>{CSS}</style></head><body><div class='pg cover'><div class=shape></div><img class=logo src='data:image/png;base64,{LOGOW}' style='top:120mm;left:66mm'>
<div class=meta style='left:0;right:0;text-align:center'>Formcraft Design and Construction · Kampala, Uganda<br>formcraftdesignconstruction.com</div><div class=band></div></div></body></html>"""
    html_pdf(back, '/tmp/fr/back.pdf')
    merge(['/tmp/fr/front.pdf', '/tmp/fr/body.pdf', '/tmp/fr/back.pdf'], f'{R}/feasibility/Formcraft-Feasibility-Report-2026.pdf')

def build_profile():
    src = f'{R}/profile/Emlyn-Atochon--Professional-Profile-and-Development-Plan.pdf'
    html = f"""<html><head><meta charset=utf-8><style>{CSS}</style></head><body><div class='pg cover'><div class=shape></div><div class=shape2></div><img class=logo src='data:image/png;base64,{LOGOW}'>
<h1>Emlyn Atochon</h1><div class=sub style='top:122mm'>Professional profile and development plan<br>Co-founder and lead designer, Formcraft Design and Construction</div>
<div class=meta>Kampala, Uganda · {TODAY}<br>Confidential</div><div class=band></div></div></body></html>"""
    html_pdf(html, '/tmp/fr/pcover.pdf')
    overlay(src, '/tmp/fr/pbody.pdf', 'Emlyn Atochon: professional profile')
    merge(['/tmp/fr/pcover.pdf', '/tmp/fr/pbody.pdf'], f'{R}/profile/Emlyn-Atochon-Professional-Profile-2026.pdf')

if __name__ == '__main__':
    import sys
    build_feasibility()
    if 'profile' in sys.argv: build_profile()
    print('built')
