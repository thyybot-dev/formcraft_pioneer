"""Builds 'The Formcraft Command Centre: founders' guide' PDF.
python3 build.py  -> out/Formcraft-Command-Centre-Guide.pdf"""
import json, os, re, io, subprocess, sys, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import PAGES, REGISTERS
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from playwright.sync_api import sync_playwright

G = '/tmp/guide'; R = '/home/claude/repo'; IM = '/home/claude/imgs'
NAVY, TEAL, DT = '#1b2532', '#7fc7be', '#3f8f86'
LOGO = f'{R}/branding/logos/Formcraft-main.png'; LOGOW = f'{R}/branding/logos/Formcraft-white.png'
DIVS = [f'{R}/branding/logos/{n}.png' for n in ('Studio', 'Construction', 'Concrete', 'Stores')]
PJ = json.load(open(f'{G}/pages.json'))
e = H.escape
DATE = '30 October 2026'

CSS = f"""
@page {{ size: A4; margin: 21mm 17mm 19mm 17mm; }}
@page full {{ margin: 0; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; font-family: Inter, sans-serif; color: {NAVY}; font-size: 9.7pt; line-height: 1.55; }}
.full {{ page: full; width: 210mm; height: 297mm; position: relative; overflow: hidden; break-after: page; }}
.mk {{ font-size: 1pt; color: transparent; letter-spacing: 0; }}
.mark {{ position: absolute; left: 2mm; top: 2mm; font-size: 1pt; color: transparent; }}
h1 {{ font-family: 'Inter Display', Inter; font-size: 24pt; line-height: 1.1; margin: 0 0 4mm; letter-spacing: -.4px; break-before: page; }}
h1 .num {{ color: {DT}; font-weight: 600; margin-right: 3mm; }}
h1.cont {{ break-before: auto; }}
h2 {{ font-family: 'Inter Display', Inter; font-size: 15pt; margin: 8mm 0 2.5mm; letter-spacing: -.2px; break-after: avoid; }}
h3 {{ font-size: 11pt; margin: 5mm 0 1.5mm; break-after: avoid; }}
p {{ margin: 0 0 2.6mm; }}
.lead {{ font-size: 11.2pt; line-height: 1.55; color: #33414d; margin-bottom: 5mm; }}
.muted {{ color: #6b7680; }}
ul, ol {{ margin: 0 0 3mm; padding-left: 5mm; }} li {{ margin: 0 0 1.2mm; }}
table {{ width: 100%; border-collapse: collapse; font-size: 8.8pt; margin: 2mm 0 4mm; break-inside: auto; }}
th {{ background: {NAVY}; color: #fff; text-align: left; padding: 1.8mm 2.2mm; font-weight: 600; }}
td {{ padding: 1.7mm 2.2mm; border-bottom: 1px solid #dde3e7; vertical-align: top; }}
tr {{ break-inside: avoid; }}
.kpis {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 3mm; margin: 3mm 0 5mm; }}
.kpi {{ border: 1px solid #dde3e7; border-left: 4px solid {TEAL}; border-radius: 2mm; padding: 2.6mm 3mm; break-inside: avoid; }}
.kpi b {{ display: block; font-family: 'Inter Display'; font-size: 19pt; line-height: 1.1; }} .kpi span {{ font-size: 8pt; color: #5b6670; }}
.note {{ background: #eef6f5; border-left: 4px solid {TEAL}; padding: 3mm 4mm; margin: 3mm 0 4mm; break-inside: avoid; border-radius: 0 2mm 2mm 0; }}
.warn {{ background: #fdf3e3; border-left: 4px solid #c98a2b; padding: 3mm 4mm; margin: 3mm 0 4mm; break-inside: avoid; border-radius: 0 2mm 2mm 0; }}
.hood {{ background: {NAVY}; color: #dfe7ea; padding: 3mm 4mm; border-radius: 2mm; font-size: 8.4pt; line-height: 1.5; break-inside: avoid; }}
.hood b.t {{ display: block; color: {TEAL}; font-size: 7.6pt; letter-spacing: 1.2px; text-transform: uppercase; margin-bottom: 1mm; }}
.hood code, code {{ font-family: 'DejaVu Sans Mono', monospace; font-size: 7.8pt; }}
code {{ background: #eef1f3; padding: 0 1mm; border-radius: 1mm; }} .hood code {{ background: rgba(255,255,255,.08); }}
.tag {{ display: inline-block; font-size: 7.4pt; letter-spacing: 1.2px; text-transform: uppercase; color: {DT}; font-weight: 700; margin-bottom: 1mm; }}
.shot {{ width: 100%; border: 1px solid #d5dde1; border-radius: 2.5mm; display: block; box-shadow: 0 1.5mm 4mm rgba(27,37,50,.10); }}
.cap {{ font-size: 7.8pt; color: #6b7680; margin: 1.6mm 0 3mm; }}
.entry {{ margin: 0 0 6mm; padding-bottom: 4mm; border-bottom: 1px solid #e3e8eb; }} .ehead {{ break-inside: avoid; }} .entry .what {{ margin-top: 3mm; }}
.entry h3 {{ font-family: 'Inter Display'; font-size: 13.5pt; margin: 0 0 2mm; display: flex; align-items: baseline; gap: 2.5mm; }}
.entry h3 .grp {{ font-family: Inter; font-size: 7.4pt; letter-spacing: 1px; text-transform: uppercase; color: {DT}; font-weight: 700; }}
.cols {{ display: grid; grid-template-columns: 1.15fr 1fr; gap: 5mm; margin-top: 3mm; }}
.steps {{ list-style: none; padding: 0; counter-reset: s; }}
.steps li {{ counter-increment: s; position: relative; padding-left: 7mm; }}
.steps li:before {{ content: counter(s); position: absolute; left: 0; top: .2mm; width: 4.6mm; height: 4.6mm; border-radius: 50%; background: {TEAL}; color: {NAVY}; font-size: 7.2pt; font-weight: 700; text-align: center; line-height: 4.6mm; }}
.chain {{ break-inside: avoid; display: grid; grid-template-columns: repeat(4, 1fr); gap: 4mm 6mm; margin: 4mm 0 5mm; }}
.chain .s {{ position: relative; border: 1px solid #cfd9dd; border-radius: 2.5mm; padding: 2.6mm 3mm; background: #fff; break-inside: avoid; min-height: 19mm; }}
.chain .s b {{ display: block; font-size: 8.8pt; line-height: 1.3; margin-bottom: .8mm; }} .chain .s span {{ font-size: 7.8pt; color: #5b6670; line-height: 1.35; display: block; }}
.chain .s i {{ font-style: normal; position: absolute; top: -2.4mm; left: 2.5mm; background: {NAVY}; color: #fff; font-size: 6.8pt; font-weight: 700; border-radius: 2mm; padding: .3mm 1.8mm; }}
.chain .s.k {{ background: #eef6f5; border-color: {TEAL}; }} .chain .s.d {{ background: {NAVY}; border-color: {NAVY}; }} .chain .s.d b {{ color: #fff; }} .chain .s.d span {{ color: #b9c6cc; }} .chain .s.d i {{ background: {TEAL}; color: {NAVY}; }}
.chain .s:not(.last):after {{ content: '›'; position: absolute; right: -4.6mm; top: 50%; transform: translateY(-55%); font-size: 15pt; color: {DT}; font-weight: 700; }}
.chain .s.eor:after {{ content: '↵'; right: -5mm; font-size: 11pt; }}
.fig {{ break-inside: avoid; margin: 3mm 0 4mm; text-align: center; }} .fig img {{ max-width: 100%; }}
.grid2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 5mm; }} .grid3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 4mm; }}
.card {{ border: 1px solid #dde3e7; border-radius: 2.5mm; padding: 3.5mm 4mm; break-inside: avoid; }}
.card h4 {{ margin: 0 0 1.5mm; font-size: 10.5pt; }} .card.dk {{ background: {NAVY}; color: #e3eaed; border-color: {NAVY}; }} .card.dk h4 {{ color: {TEAL}; }}
.card.tl {{ background: #eef6f5; border-color: {TEAL}; }}
.toc a {{ display: flex; justify-content: space-between; border-bottom: 1px dotted #b9c3ca; padding: 1.25mm 0; color: {NAVY}; text-decoration: none; font-size: 9.6pt; }}
.toc a.p {{ font-weight: 700; font-size: 10.4pt; margin-top: 2.5mm; border-bottom: 1.5px solid {TEAL}; }}
.toc a.s {{ padding-left: 5mm; color: #33414d; }}
.ladder {{ margin: 3mm 0 5mm; }}
.ladder .r {{ display: grid; grid-template-columns: 22mm 1fr 38mm 22mm; align-items: center; gap: 3mm; border-radius: 2mm; padding: 2.2mm 3mm; margin-bottom: 1.6mm; break-inside: avoid; }}
.ladder .r b.l {{ font-family: 'Inter Display'; font-size: 13pt; }}
.layer {{ border-radius: 3mm; padding: 3mm; margin-bottom: 2mm; break-inside: avoid; }}
.layer .lt {{ font-size: 7.4pt; letter-spacing: 1.3px; text-transform: uppercase; font-weight: 700; margin-bottom: 2mm; }}
.layer .bx {{ display: flex; gap: 2.5mm; flex-wrap: wrap; }}
.layer .bx div {{ color: #1b2532; flex: 1; min-width: 26mm; background: #fff; border: 1px solid #cfd9dd; border-radius: 2mm; padding: 2mm 2.4mm; font-size: 8pt; line-height: 1.35; }}
.layer .bx div b {{ display: block; font-size: 8.8pt; }}
.arrow {{ text-align: center; color: {DT}; font-size: 8pt; font-weight: 600; margin: -0.5mm 0 1.5mm; }}
.org {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 4mm; }}
.org .f {{ background: {NAVY}; color: #fff; border-radius: 2.5mm; padding: 2.5mm 3mm; margin-bottom: 2mm; }} .org .f b {{ display: block; font-size: 10.5pt; }} .org .f span {{ color: {TEAL}; font-size: 7.8pt; }}
.org .d {{ font-size: 7.2pt; letter-spacing: 1px; text-transform: uppercase; color: {DT}; font-weight: 700; margin: 2.5mm 0 1mm; }}
.org .r {{ border: 1px solid #cfd9dd; border-left: 3px solid {TEAL}; border-radius: 1.5mm; padding: 1.2mm 2mm; font-size: 8pt; margin-bottom: 1.2mm; display: flex; justify-content: space-between; }}
.org .r em {{ font-style: normal; color: #6b7680; font-size: 7.2pt; }}
.tour {{ position: relative; break-inside: avoid; }} .tour .m {{ position: absolute; width: 6.5mm; height: 6.5mm; margin: -3.25mm 0 0 -3.25mm; border-radius: 50%; background: #e4572e; color: #fff; font-weight: 700; font-size: 9pt; text-align: center; line-height: 6.5mm; box-shadow: 0 0 0 1.2mm rgba(228,87,46,.25); }}
.legend {{ display: grid; grid-template-columns: 7mm 1fr; gap: 1.5mm 2.5mm; align-items: start; }} .legend .n {{ width: 6mm; height: 6mm; border-radius: 50%; background: #e4572e; color: #fff; font-weight: 700; font-size: 8.5pt; text-align: center; line-height: 6mm; }}
.gantt {{ margin: 3mm 0 5mm; font-size: 8pt; }} .gantt .row {{ display: grid; grid-template-columns: 55mm 1fr; align-items: center; gap: 3mm; margin-bottom: 1.6mm; break-inside: avoid; }}
.gantt .track {{ position: relative; height: 6mm; background: #f1f4f5; border-radius: 1.5mm; }} .gantt .bar {{ position: absolute; top: 0; height: 6mm; border-radius: 1.5mm; color: #fff; font-size: 7pt; line-height: 6mm; padding-left: 2mm; white-space: nowrap; overflow: hidden; }}
.gantt .scale {{ display: grid; grid-template-columns: 55mm 1fr; gap: 3mm; color: #6b7680; font-size: 7pt; margin-bottom: 1mm; }} .gantt .scale div:last-child {{ display: flex; justify-content: space-between; }}
.pill {{ display: inline-block; border-radius: 9mm; padding: .4mm 2.4mm; font-size: 7.6pt; font-weight: 600; background: #eef1f3; }}
"""

def img(p): return 'file://' + p
def shot(k, cap=None, h=None):
    p = f'{G}/crop/{k}.png'
    st = f' style="height:{h}mm;object-fit:cover;object-position:top"' if h else ''
    return f'<img class="shot" src="{img(p)}"{st}>' + (f'<div class="cap">{cap}</div>' if cap else '')

def hood(t, title='Under the hood'): return f'<div class="hood"><b class="t">{title}</b>{t}</div>'
def chain(items, cols=4):
    out = []
    for i, it in enumerate(items):
        t, d = it[0], it[1]; c = it[2] if len(it) > 2 else ''
        last = ' last' if i == len(items) - 1 else (' eor' if (i + 1) % cols == 0 else '')
        out.append(f'<div class="s {c}{last}"><i>{i+1}</i><b>{t}</b><span>{d}</span></div>')
    return f'<div class="chain" style="grid-template-columns:repeat({cols},1fr)">' + ''.join(out) + '</div>'

def fig(svg, cap, w=100, maxh=None):
    mh = f';max-height:{maxh}mm' if maxh else ''
    return f'<div class="fig"><img src="{img(G + "/mm/" + svg)}" style="width:{w}%{mh}"><div class="cap">{cap}</div></div>'

HEADS = []
def h1(num, t, kind='p'):
    HEADS.append((num, t, kind)); return f'<h1 id="h{len(HEADS)}"><span class="mk">@@H{len(HEADS)}@@</span><span class="num">{num}</span>{t}</h1>'
def h2(t):
    HEADS.append(('', t, 's')); return f'<h2><span class="mk">@@H{len(HEADS)}@@</span>{t}</h2>'

def divider(n, title, blurb, photo):
    return f"""<section class="full" style="background:{NAVY}"><span class="mark">FCFULLPAGE</span>
<div style="position:absolute;left:0;top:0;right:0;height:150mm;background:url('{img(photo)}') center/cover"></div>
<div style="position:absolute;left:0;top:0;right:0;height:150mm;background:linear-gradient(180deg,rgba(27,37,50,.05) 40%,rgba(27,37,50,1) 100%)"></div>
<div style="position:absolute;left:20mm;top:165mm;color:{TEAL};font-size:12pt;font-weight:600;letter-spacing:3px">PART {n}</div>
<div style="position:absolute;left:20mm;top:177mm;right:20mm;color:#fff;font-family:'Inter Display';font-size:38pt;line-height:1.05;font-weight:700;letter-spacing:-.8px">{title}</div>
<div style="position:absolute;left:20mm;top:222mm;right:30mm;color:#c7d2d7;font-size:12pt;line-height:1.55">{blurb}</div>
<img src="{img(LOGOW)}" style="position:absolute;left:20mm;bottom:16mm;height:7mm">
<div style="position:absolute;left:0;right:0;bottom:0;height:5mm;background:{TEAL}"></div></section>"""

# ----------------------------------------------------------------------------------
def build(toc_pages=None):
    HEADS.clear()
    tp = toc_pages or {}
    o = []
    # ---------- cover ----------
    o.append(f"""<section class="full" style="background:{NAVY}"><span class="mark">FCFULLPAGE</span>
<div style="position:absolute;right:-18mm;top:-10mm;width:120mm;height:175mm;transform:rotate(8deg);display:grid;grid-template-columns:1fr 1fr;gap:4mm">
 <div style="background:url('{img(IM+'/residence.jpg')}') center/cover;border-radius:5mm"></div><div style="background:url('{img(IM+'/white_kitchen.jpg')}') center/cover;border-radius:5mm;margin-top:22mm"></div>
 <div style="background:url('{img(IM+'/school.jpg')}') center/cover;border-radius:5mm"></div><div style="background:url('{img(IM+'/mvule_wardrobe.jpg')}') center/cover;border-radius:5mm;margin-top:22mm"></div></div>
<div style="position:absolute;inset:0;background:linear-gradient(90deg,{NAVY} 48%,rgba(27,37,50,.35) 100%)"></div>
<img src="{img(LOGOW)}" style="position:absolute;left:20mm;top:22mm;width:68mm">
<div style="position:absolute;left:20mm;top:92mm;color:{TEAL};font-size:11pt;font-weight:600;letter-spacing:3px">FOUNDERS' GUIDE · VERSION 1.0</div>
<div style="position:absolute;left:20mm;top:104mm;width:125mm;color:#fff;font-family:'Inter Display';font-size:42pt;line-height:1.02;font-weight:700;letter-spacing:-1px">The Formcraft Command Centre</div>
<div style="position:absolute;left:20mm;top:160mm;width:118mm;color:#cbd6da;font-size:12.5pt;line-height:1.55">The system that runs Formcraft: what it is, why we built it, how every part works, how to use it every day, and the plan to finish it.</div>
<div style="position:absolute;left:20mm;top:205mm;display:flex;gap:8mm;align-items:center">{''.join(f'<img src="{img(d)}" style="height:6.5mm;filter:brightness(0) invert(1);opacity:.9">' for d in DIVS)}</div>
<div style="position:absolute;left:20mm;bottom:20mm;color:#aebbc1;font-size:9.5pt;line-height:1.7">For Emlyn Atochon, Peter Isingoma and Esther Ahumuza<br>Formcraft Design and Construction · Kampala · {DATE}<br>Confidential: for the founders</div>
<div style="position:absolute;left:0;right:0;bottom:0;height:6mm;background:{TEAL}"></div></section>""")

    # ---------- how to read + contents ----------
    o.append(h1('', 'How to read this guide').replace('<h1', '<h1 style="break-before:auto"'))
    o.append(f"""<p class="lead">This guide is for the three of us. It teaches you the Command Centre from nothing, and it also holds the whole logic behind it, so anyone we hire, or any AI we connect, can learn from the same book. Read Parts 1 to 3 in one sitting (about an hour). Use Parts 4 to 8 as a reference when you open a page for the first time.</p>
<div class="grid3">
<div class="card"><h4>Plain text</h4>What a part is for and why it matters. Written for someone who has never seen the app.</div>
<div class="card tl"><h4>Do this</h4><ol class="steps" style="margin:0"><li>Numbered steps</li><li>are how to use it.</li></ol></div>
<div class="card dk"><h4>Under the hood</h4>The technical logic: which data it stores, which rules and automations drive it. For whoever builds or fixes it.</div></div>
<div class="note"><b>About the screenshots.</b> Every screenshot is the real Command Centre, taken on {DATE}. To make the screens readable they show a small set of <b>example data</b> (the Okello quote, a clinic lead, a sketch of a house). The live system does not hold that data. Entering our real business is the first job (Part 3).</div>""")
    o.append('<h2 style="margin-top:6mm">Contents</h2><div class="toc">@@TOC@@</div>')

    # ================= PART 1: PITCH =================
    o.append(divider(1, 'The pitch', 'Why Formcraft needs one system, what it does for each of us, and how it serves the five-year goal: the top design and construction firm in East Africa.', IM + '/residence.jpg'))
    o.append(h1('1', 'One system that runs Formcraft').replace('<h1', '<h1 style="break-before:auto"'))
    o.append("""<p class="lead">Formcraft is three founders running five businesses at once: Studio (design), Construction, Concrete, Stores and Formcraft Tools for Revit. Each one has clients, money, deadlines, suppliers, content and compliance. Kept in heads, WhatsApp chats and spreadsheets, that work grows faster than three people can carry it. The Command Centre is the answer: <b>one place where the whole business lives, where AI agents do the routine work, and where the founders decide and check.</b></p>""")
    o.append('<div class="grid2">')
    o.append("""<div class="card"><h4>The problem</h4><ul><li>Leads arrive by website, WhatsApp, calls and events, and some are never answered within a day.</li><li>Quotes take days; prices are guessed instead of tied to the plan.</li><li>Money, tax dates and cash runway are checked only when there is a problem.</li><li>Content, the YouTube channel and the website need daily work nobody has time for.</li><li>Everything depends on what each founder remembers.</li></ul></div>""")
    o.append("""<div class="card dk"><h4>The answer</h4><ul><li>Every lead, quote, project, shilling, task and document in one database.</li><li>A morning brief that tells each founder what needs them today.</li><li>AI agents and scripts that draft, chase, price, post and log, with nothing applied until a founder approves.</li><li>The company's rules and memory written down, so any model, and any new hire, continues from them.</li><li>Built to grow into a fully automated business.</li></ul></div></div>""")
    o.append(h2('What it does for each founder'))
    o.append("""<table><tr><th style="width:24%">Founder</th><th style="width:38%">Runs and approves</th><th>What the Command Centre takes off them</th></tr>
<tr><td><b>Emlyn Atochon</b><br><span class="muted">Design, BIM, software, admin</span></td><td>Revit and model jobs, automations, connections, AI settings, releases of Formcraft Tools and the website</td><td>The design studio, family factory, tutorials, development room and the main hub on his PC</td></tr>
<tr><td><b>Peter Isingoma</b><br><span class="muted">Projects, Concrete, real estate, finance</span></td><td>Site and project jobs, purchase orders, supplier payments, contracts (jointly with Emlyn), finance agent work</td><td>Site diaries, project flags, price book, supplier price calls, payroll, tax calendar, cash forecast</td></tr>
<tr><td><b>Esther Ahumuza</b><br><span class="muted">Marketing, sales, interiors</span></td><td>Social posts, newsletters, enquiries and quotes, website content, sales agent work</td><td>Auto-quotes, follow-ups, the content plan, events, the professionals directory and campaigns</td></tr></table>
<p class="muted" style="font-size:8.4pt">Roles as proposed in the pitch deck; to be confirmed by the founders (Part 8).</p>""")
    o.append(h2('The goal it serves'))
    o.append("""<p>The feasibility study sets the target: <b>the top design and construction firm in East Africa within five years</b>, which in numbers means about <b>USD 1 million of revenue a year by 2031</b>, on the way to a much longer journey (Formcraft Tools sold worldwide). The Command Centre tracks that journey in six phases.</p>""")
    phases = [('P0', 'Foundation sprint', 'Nov 2026 to Jan 2027', 'Core coding done, IP and shareholders\' agreement signed, USD 15,000 buffer', 'd'),
              ('P1', 'Prove the model', '2027', 'About USD 46,000 revenue, 20 then 50 leads a month, 2,000 YouTube subscribers', 'k'),
              ('P2', 'Kampala leader', '2028 to 2029', 'The firm people in Kampala name first', ''),
              ('P3', 'East Africa', 'to 2031', 'Offices and partners across the region; about USD 1M a year', ''),
              ('P4', 'Africa', 'after 2031', 'Formcraft Tools and services across Africa', ''),
              ('P5', 'Global software', 'long term', 'Formcraft Tools as a global product', '')]
    o.append(chain([(f'{a} · {b}', f'<b style="font-size:7.6pt;color:inherit;display:inline">{c}</b><br>{d}', k) for a, b, c, d, k in phases], cols=3))
    o.append(h2('By the numbers'))
    o.append("""<div class="kpis"><div class="kpi"><b>67</b><span>pages in the app</span></div><div class="kpi"><b>128</b><span>automations planned in 13 groups</span></div><div class="kpi"><b>28</b><span>AI staff roles, one per planned hire</span></div><div class="kpi"><b>8</b><span>AI agents with their own rulebooks</span></div>
<div class="kpi"><b>78</b><span>business systems mapped to the value chain</span></div><div class="kpi"><b>7</b><span>service lines with client on and offboarding</span></div><div class="kpi"><b>173</b><span>templates in the master register</span></div><div class="kpi"><b>5</b><span>AI tiers: scripts, offline, DeepSeek, Claude, Grok</span></div></div>""")
    o.append(h2('Why it makes the plan more likely'))
    o.append("""<p>The simulations behind the feasibility study are honest about software: on its own, a system adds only a little to the odds. What moves the odds is <b>cash discipline, steady sales, deposits and stage payments, and signed legal papers</b>. The Command Centre earns its place by making those things happen every day without relying on memory: the cash buffer is watched, every quote is priced to the plan, every lead gets a next step, every tax date is on the calendar, and every AI hour is spent on the cheapest tool that can do the job.</p>
<div class="warn"><b>Where it stands today (30 October 2026).</b> The app is built and running, but it holds almost no real business yet: no deals, no projects, no ledger entries and no logged numbers. None of the 128 automations is live yet; they are designed, with recipes, and waiting to be built. The system becomes valuable the day we put the real business into it. Part 8 lists the honest gaps and the next 30 days.</div>""")

    # ================= PART 2: HOW IT WORKS =================
    o.append(divider(2, 'How the system works', 'The big picture, the four principles, the work loop, the AI ladder, who approves what, and where the data lives.', IM + '/coffee_factory.jpg'))
    o.append(h1('2', 'The big picture').replace('<h1', '<h1 style="break-before:auto"'))
    o.append('<p class="lead">Read the picture from top to bottom: people use the Command Centre, the Command Centre keeps everything in one database, AI and scripts propose work, founders approve it, and approved work goes out through the connections.</p>')
    o.append(f"""<div class="layer" style="background:#f3f5f6"><div class="lt" style="color:#5b6670">People</div><div class="bx">
<div><b>Emlyn</b>main hub (development PC)</div><div><b>Peter</b>founder hub</div><div><b>Esther</b>founder hub</div><div><b>Employees</b>web version, phone or PC</div><div><b>Clients and professionals</b>website and client portal</div></div></div>
<div class="arrow">↓ open pages, log, ask, approve</div>
<div class="layer" style="background:{NAVY};color:#fff"><div class="lt" style="color:{TEAL}">Formcraft Command Centre</div><div class="bx">
<div><b>67 pages</b>briefs, sales, projects, money, studio, standards, content</div><div><b>Approvals queue</b>risk rules, one or two founders</div><div><b>Registers</b>clients, suppliers, price book, contracts and more</div><div><b>Memory and rulebooks</b>owned by Formcraft, not by any AI</div></div></div>
<div class="arrow">↓ everything reads and writes one database ↓</div>
<div class="grid2" style="gap:3mm"><div class="layer" style="background:#eef6f5"><div class="lt" style="color:{DT}">Data</div><div class="bx"><div><b>Firebase</b>online master: Firestore, Auth, Storage, Functions</div><div><b>PostgreSQL</b>local copy on each founder hub: history, reports, recovery</div></div></div>
<div class="layer" style="background:#eef6f5"><div class="lt" style="color:{DT}">AI layer: cheapest path</div><div class="bx"><div><b>Scripts</b>free, exact</div><div><b>Offline 7-8B</b>free, on the main PC</div><div><b>Cloud</b>DeepSeek, Claude, Grok by tier</div></div></div></div>
<div class="arrow">↓ approved work goes out through the MCP hub ↓</div>
<div class="layer" style="background:#f3f5f6"><div class="lt" style="color:#5b6670">Connections</div><div class="bx">
<div><b>Revit</b>up to 10 windows, ports 8080-8089</div><div><b>Website</b>enquiries, standards, directory, store</div><div><b>Messages</b>email, WhatsApp, social, calls</div><div><b>Payments</b>mobile money, Flutterwave</div><div><b>GitHub</b>code, tests, releases</div></div></div>""")
    o.append(h2('Four principles'))
    o.append("""<div class="grid2">
<div class="card"><h4>1. Rules before automation</h4>Every job is first written as a rulebook recipe: what to do, what to check, who approves. Only then is it scripted or handed to AI. A recipe that is not written does not get automated.</div>
<div class="card"><h4>2. Scripts first, AI as the bridge</h4>A script beats a model; a small offline model beats a large one; the large cloud models are kept for reasoning, development and review. AI uses scripts as its tools.</div>
<div class="card"><h4>3. Nothing applied without approval</h4>Agents propose; founders decide. Low-risk work runs and is logged, medium needs one founder, money over USD 500, contracts and releases need two.</div>
<div class="card"><h4>4. The memory belongs to Formcraft</h4>Memory, rulebooks and data live in our database, not inside any AI. We can switch Claude for Grok, DeepSeek or an offline model at any time and the new one continues from the same place.</div></div>""")

    o.append(h1('', 'The work loop: how a job gets done', 's').replace('<h1', '<h1 class="cont" style="break-before:page"'))
    o.append('<p class="lead">Every piece of work, whether a reminder to chase an invoice or a new wall layout, goes through the same loop. This is the logic of the whole system on one page.</p>')
    o.append(fig('loop.svg', 'Figure 2.1 · The work loop. Teal boxes are free or automatic; dark boxes need a founder.', 92, 215))

    o.append(h1('', 'The cheapest path: six levels', 's').replace('<h1', '<h1 class="cont" style="break-before:page"'))
    o.append('<p class="lead">For every task we use the cheapest thing that can do it correctly. Work starts at the bottom of the ladder and climbs one level only when a check fails. Every climb is logged with its reason, so we know which script to write next.</p>')
    lv = [('5', 'Chief, developer, reviewer', 'Planning, writing scripts and tests, development, hard reasoning, reviewing', 'Top cloud model (Claude)', 'Highest', NAVY, '#fff'),
          ('4', 'Senior agents', 'Client-facing writing, multi-step reasoning, what level 3 failed', 'Mid cloud model (DeepSeek, Grok)', 'Low', '#33505a', '#fff'),
          ('3', 'Area agents', 'Drafts, summaries, simple tool chains, first-line replies', 'Offline 7-8B model', 'Free', '#5fa9a0', '#fff'),
          ('2', 'Worker bots', 'Sorting, tagging, extracting fields, filling script inputs; output must pass a schema', 'Offline 3-4B model', 'Free', '#7fc7be', NAVY),
          ('1', 'Rules and lookups', 'Routing, matching, filling templates: tables, formulas, regex', 'Code', 'Free', '#b7e0da', NAVY),
          ('0', 'Scripts and tools', 'Anything already scripted and tested', 'Code', 'Free', '#e3f3f1', NAVY)]
    o.append('<div class="ladder">' + ''.join(f'<div class="r" style="background:{bg};color:{fg};margin-left:{(5-int(n))*0}mm"><b class="l">Level {n}</b><div><b>{t}</b><br><span style="font-size:8pt;opacity:.85">{d}</span></div><div style="font-size:8pt">{m}</div><div style="text-align:right;font-weight:700">{c}</div></div>' for n, t, d, m, c, bg, fg in lv) + '</div>')
    o.append("""<div class="grid2"><div><h3>How a job is routed</h3><ol class="steps"><li>Look up the intent in the script table. If a tested script exists, run it.</li><li>Otherwise start at the lowest level allowed for that intent and check the result.</li><li>On a failed check go up one level, up to the maximum allowed. Log why.</li><li>If the budget runs out, stop and ask the owning founder. Never overspend silently.</li></ol></div>
<div><h3>How AI work becomes free</h3><p>When the same intent has been done by AI three times with similar inputs, the developer agent (level 5) writes a script and its tests from those runs. Emlyn approves it; it joins level 0. If a promoted script later fails a check it is paused and the job goes back to AI until it is fixed.</p><p><b>Target:</b> 50% of runs done by scripts by month 6, 80% by month 18.</p></div></div>""")
    o.append(hood("Every call carries a <b>purpose</b> (purpose, intent, area, started_by, agent, project, risk, budget_usd). The hub answers with a <b>context pack</b> (task id, scripts, tools, memory lines, rulebook link, journal, level, limits) holding references and short extracts, never data dumps. When the task ends the hub writes a journal note, any lesson to memory, and a ledger line (purpose, intent, level used, escalations, cost, time, result). Answers are cached by a hash of intent, inputs and context version. At 80% of a monthly budget, routing drops one level except for high-risk work. Spec: <code>docs/windows-hub-plan.md §15</code>."))

    o.append(h1('', 'AI models, agents and memory', 's').replace('<h1', '<h1 class="cont" style="break-before:page"'))
    o.append("""<p class="lead">We use three cloud families and one offline model, each for what it does best. Changing a model is a setting, not a rebuild.</p>
<table><tr><th>Tier</th><th>Default model</th><th>Used for</th><th>Cost</th></tr>
<tr><td><b>Offline</b></td><td>7-8B model through Ollama on the main PC (3-4B for the quick jobs)</td><td>Sorting, tagging, drafts, summaries when Revit is not busy; works without internet</td><td>Free</td></tr>
<tr><td><b>Quick</b></td><td>DeepSeek</td><td>Cheap cloud work: extraction, standards summaries, simple replies</td><td>Lowest</td></tr>
<tr><td><b>Default</b></td><td>Claude</td><td>Daily agent work, client-facing writing, the morning brief</td><td>Medium</td></tr>
<tr><td><b>Complex</b></td><td>Claude (top model)</td><td>Design assistant, planning, development, reviewing</td><td>Highest</td></tr>
<tr><td><b>Second opinion</b></td><td>Grok</td><td>Reviewing another model's work: nobody grades their own work</td><td>Medium</td></tr></table>""")
    o.append(h2('The eight agents'))
    o.append("""<table><tr><th style="width:30%">Agent</th><th>Looks after</th></tr>
<tr><td><b>Chief of staff</b> (general)</td><td>The whole business: keeps the founders accountable to the plan, joins up the other agents, runs the morning brief and the weekly review, decides which agent acts</td></tr>
<tr><td><b>Finance</b></td><td>Money, budget, cash forecast, payroll (PAYE, NSSF), tax calendar, invoices, receipts, debts, pricing. Never moves money; prepares and proposes</td></tr>
<tr><td><b>Sales and marketing</b></td><td>Leads, enquiries and auto-quotes, follow-ups, email list and campaigns, content, SEO, global reach</td></tr>
<tr><td><b>Projects and site</b></td><td>Projects, building playbook, drawings, RFIs, variations, site diary, defects, permits, quality</td></tr>
<tr><td><b>Design and BIM</b></td><td>Design studio, models, families, templates, standards checks</td></tr>
<tr><td><b>Software and automation</b></td><td>Formcraft Tools, the MCP server, automations, recipes, tests</td></tr>
<tr><td><b>People and admin</b></td><td>Staff, hiring, leave, training, the AI workforce scorecards</td></tr>
<tr><td><b>Legal and risk</b></td><td>Contracts, compliance calendar, data protection, risk register</td></tr></table>""")
    o.append(h2('Memory: why switching AI loses nothing'))
    o.append("""<div class="grid3"><div class="card"><h4>Short-term</h4>Every exchange with the AI is kept for 7 days in the AI log.</div><div class="card"><h4>Long-term</h4>Once a week the AI consolidates what mattered into long-term memory: decisions, client preferences, lessons. Founders can pin lines.</div><div class="card"><h4>Rulebooks</h4>Each agent's written rules (<code>rulebooks/agents/*.md</code>). Errors become new rules so they never repeat.</div></div>
<p>A <b>handover pack</b> (JSON or Markdown) holds memory, rules and the current state. Give it to any AI tool and it continues where the last one stopped. The same pack is how an AI staff member hands its role to a new human hire.</p>""")
    o.append(hood("Collections <code>memory</code>, <code>ailog</code>, <code>aistaff</code>, <code>aiuse</code>, <code>pending</code>. The Formcraft MCP server (<code>mcp-server/server.js</code>, Node, stdio JSON-RPC) gives any outside AI the same tools: <code>get_brief, read_data, query_register, propose_actions, list_pending, apply_approved, reject_pending, remember, recall, log_exchange, handover_pack, log_metric</code>. <code>propose_actions</code> validates every action against a schema; nothing is written until <code>apply_approved</code>. API keys never go into the shared database: they stay on each PC (Windows Credential Manager or the browser's local storage)."))

    o.append(h1('', 'The AI workforce', 's').replace('<h1', '<h1 class="cont" style="break-before:page"'))
    o.append('<p class="lead">Every role in the hiring plan has an AI version working now, reporting to the founder who owns that department. Each starts on probation, suggesting only, with a USD 10 monthly AI budget, and earns autonomy through its scorecard. When we hire a person for the role, the AI hands over its journal, scripts and memory and becomes that person\'s assistant.</p>')
    from collections import OrderedDict
    import importlib
    src = open('/home/claude/dash/index.html').read()
    i = src.find('const PLAN27'); j = src.find('];', i)
    roles = re.findall(r"\['(\w+)','([^']*)','([^']*)','([^']*)','(\w+)'", src[i:j])
    org = OrderedDict([('Emlyn', OrderedDict()), ('Peter', OrderedDict()), ('Esther', OrderedDict())])
    for _, name, dept, f, tier in roles: org[f].setdefault(dept, []).append((name, tier))
    full = {'Emlyn': ('Emlyn Atochon', 'Design, BIM and software'), 'Peter': ('Peter Isingoma', 'Engineering, construction, concrete, finance'), 'Esther': ('Esther Ahumuza', 'Sales, marketing and stores')}
    tl = {'quick': 'quick', 'default': 'standard', 'complex': 'deep'}
    o.append('<div class="org">' + ''.join(f'<div><div class="f"><b>{full[f][0]}</b><span>{full[f][1]}</span></div>' + ''.join(f'<div class="d">{d}</div>' + ''.join(f'<div class="r"><span>{n}</span><em>{tl.get(t,t)}</em></div>' for n, t in rs) for d, rs in ds.items()) + '</div>' for f, ds in org.items()) + '</div>')
    o.append(f'<p class="cap">{len(roles)} roles. The small label is the model size each role uses by default: quick (offline or DeepSeek), standard (Claude), deep (top Claude model).</p>')

    o.append(h1('', 'Approvals, roles and who uses what', 's').replace('<h1', '<h1 class="cont" style="break-before:page"'))
    o.append("""<table><tr><th style="width:14%">Risk</th><th style="width:43%">Examples</th><th>Needs</th></tr>
<tr><td><span class="pill" style="background:#d9f5e3">Low</span></td><td>Tags, summaries, internal tasks, drafts</td><td>Runs automatically and is logged</td></tr>
<tr><td><span class="pill" style="background:#fdecd2">Medium</span></td><td>Posting to social media, client emails, register changes</td><td>One approval from the owning founder</td></tr>
<tr><td><span class="pill" style="background:#f9d6d1">High</span></td><td>Money out, contracts, prices, website releases, Revit model changes</td><td>The owner, plus a second founder for money over USD 500 and for every contract</td></tr></table>
<div class="note"><b>Checking.</b> Each founder reviews a sample of the AI's finished work in their area every week (10% to start). The share with a serious error is a KPI with a target under 2%. If an agent is above target, its autonomy drops one level until it recovers.</div>""")
    o.append(fig('hubs.svg', 'Figure 2.2 · Three founder hubs and the employees\' web version share one online database.', 62, 105))
    o.append("""<table><tr><th></th><th>Founders (3)</th><th>Employees</th></tr>
<tr><td><b>App</b></td><td>Formcraft Hub for Windows (planned; today the Command Centre in claude.ai)</td><td>The web version on phone or PC</td></tr>
<tr><td><b>Sees</b></td><td>Everything their role allows; Emlyn chooses which tabs Peter and Esther see</td><td>Only their role's pages, tasks and registers</td></tr>
<tr><td><b>AI</b></td><td>Through the hub's router</td><td>Never holds an AI key: each request becomes a job the main hub runs within the role's budget</td></tr>
<tr><td><b>Does</b></td><td>Approving, checking, development, clients, strategy</td><td>Their tasks, site logs and photos, what automations cannot do; exceptions go up</td></tr></table>""")

    o.append(h1('', 'Where the data lives', 's').replace('<h1', '<h1 class="cont" style="break-before:page"'))
    o.append("""<p class="lead">Everything is in one database, organised as collections (think: one sheet per kind of record). The Data explorer page shows every one of them. Money, payroll, contracts, investors and candidates are locked to admins by the database itself, whatever a person's role says.</p>
<table><tr><th style="width:24%">Area</th><th>Collections</th></tr>
<tr><td><b>Daily work</b></td><td><code>todos</code> tasks · <code>notices</code> · <code>meetings</code> · <code>chat</code> · <code>events</code> calendar · <code>deadlines</code> · <code>log</code> numbers · <code>targets</code> · <code>wins</code></td></tr>
<tr><td><b>Sales and clients</b></td><td><code>deals</code> · <code>enq</code> enquiries · <code>onb</code> journeys · <code>campaigns</code> · <code>reg_clients</code> · <code>reg_prospects</code> · <code>reg_subscribers</code></td></tr>
<tr><td><b>Projects and design</b></td><td><code>projects</code> · <code>boards</code>, <code>bel</code>, <code>brev</code> design studio · <code>reg_models</code> · <code>reg_drawings</code> · <code>reg_rfis</code> · <code>reg_variations</code> · <code>reg_sitediary</code> · <code>reg_defects</code> · <code>reg_permits</code></td></tr>
<tr><td><b>Money (admin)</b></td><td><code>ledger</code> · <code>invoices</code> · <code>budget</code> · <code>staff</code> · <code>payruns</code> · <code>hires</code> · <code>lic</code> · <code>reg_accounts</code> · <code>reg_debts</code> · <code>reg_contracts</code> · <code>reg_lenders</code></td></tr>
<tr><td><b>Knowledge</b></td><td><code>std_clauses</code> standards · <code>appr_auth</code>, <code>appr_rep</code> approvals · <code>pros</code>, <code>pro_reviews</code>, <code>referrals</code>, <code>contrib</code> directory · <code>reg_pricebook</code> · <code>reg_knowledge</code></td></tr>
<tr><td><b>AI and systems</b></td><td><code>memory</code> · <code>ailog</code> · <code>pending</code> approvals · <code>aistaff</code> · <code>aiuse</code> AI cost · <code>autos</code> · <code>issues</code> · <code>learn</code> · <code>decisions</code> · <code>risks</code></td></tr>
<tr><td><b>Content</b></td><td><code>cplan</code> content plan · <code>xevents</code> events · <code>seokw</code> · <code>files</code>, <code>assets</code> · <code>reach</code> · <code>impact</code></td></tr></table>""")
    o.append(h2('How the data is kept safe'))
    o.append("""<ul><li><b>Today:</b> the database lives with the Command Centre in claude.ai, under Emlyn's account. A full backup (one JSON file) is one click on Team and access; restore is on the same page.</li><li><b>Next:</b> Firebase becomes the online master (the web version is already built for it: <code>command-centre/standalone</code>), and each founder hub keeps a full PostgreSQL copy with a change log and an outbox, so nothing is lost if one copy fails.</li><li><b>Rule:</b> a weekly backup and a restore drill every quarter. A backup that has never been restored is not a backup.</li></ul>""")

    # ================= PART 3: GETTING STARTED =================
    o.append(divider(3, 'Getting started', 'A tour of the screen, the first week, and the daily, weekly and monthly routine for each founder.', IM + '/white_kitchen.jpg'))
    o.append(h1('3', 'A tour of the screen').replace('<h1', '<h1 style="break-before:auto"'))
    marks = [(1, 9, 30), (2, 9, 6.5), (3, 66.6, 6.5), (4, 72.2, 6.5), (5, 90, 6.5), (6, 42, 26), (7, 80, 28), (8, 42, 82), (9, 96.4, 93)]
    o.append(f'<div class="tour"><img class="shot" src="{img(G + "/full_daily.png")}">' + ''.join(f'<div class="m" style="left:{x}%;top:{y}%">{n}</div>' for n, x, y in marks) + '</div><div class="cap">The Founders\' daily page with the menu open. Example data.</div>')
    o.append("""<div class="legend">
<div class="n">1</div><div><b>The menu.</b> Five groups: Main menu (daily work), Business (money, sales, projects, design, content), Build and AI (agents, automations, standards, tools), Registers (lists) and Control (targets, risk, access). You only see the pages your role allows. The button at the top folds it away.</div>
<div class="n">2</div><div><b>Where you are.</b> The page name. Every page has the same header.</div>
<div class="n">3</div><div><b>+ Log.</b> Log anything by hand from any page: a number, an expense, a task, a note. Marked as manual so you can always tell it from automation.</div>
<div class="n">4</div><div><b>Ask AI.</b> Ask a question about the page you are on. The AI reads the data you can see and proposes actions; you approve them.</div>
<div class="n">5</div><div><b>Date, week of the plan and Live.</b> 'Live' means you are connected and every change is saved for everyone at once.</div>
<div class="n">6</div><div><b>Morning brief.</b> Cash, income, team, today's plan, then alerts in order: Act now, This week, Note.</div>
<div class="n">7</div><div><b>Approvals.</b> What the agents propose. Approve, reject, or approve all.</div>
<div class="n">8</div><div><b>Today's register.</b> The pipeline, projects and client journeys you can change in place.</div>
<div class="n">9</div><div><b>The AI button.</b> Opens the agent chat from anywhere. The red number is how many approvals are waiting.</div></div>""")

    o.append(h1('', 'Your first week: put the real business in', 's').replace('<h1', '<h1 class="cont" style="break-before:page"'))
    o.append('<p class="lead">The Command Centre is only as good as what is in it. Before anything else, these eight jobs give every page real numbers to work with. Each takes under an hour.</p>')
    o.append(chain([('Company', 'Fill the Company page: URSB, TIN, NSSF, addresses. Upload certificates to Files.', 'd'),
                    ('Cash and money', 'Log cash in hand. Enter this month\'s income and expenses in Money. Add unpaid invoices.', 'k'),
                    ('Pipeline', 'Every live lead and quote into Sales, each with a next step and date.', 'k'),
                    ('Projects', 'Every running job, with budget, cost so far and due date.', 'k'),
                    ('Registers', 'Paste clients, suppliers and the price book from Excel.', ''),
                    ('Numbers', 'Log leads, subscribers and the other metrics on Log and deadlines.', ''),
                    ('People and roles', 'Founders confirm roles; Emlyn sets tabs on Team and access.', ''),
                    ('Backup', 'Download the first full backup on Team and access.', 'd')]))
    o.append(h2('The routine'))
    o.append("""<div class="grid3"><div class="card tl"><h4>Every day · 10 minutes</h4><ol class="steps"><li>Open Founders' daily.</li><li>Read the brief, red items first.</li><li>Decide every approval waiting for you.</li><li>Log anything that happened (+ Log).</li><li>Check My day.</li></ol></div>
<div class="card"><h4>Every week · 45 minutes, together</h4><ol class="steps"><li>Weekly founders review meeting (Meetings).</li><li>Sales: every deal has a next step.</li><li>Cash: log cash, read the forecast.</li><li>Check a 10% sample of AI work.</li><li>Approve next week's content.</li><li>Download a backup.</li></ol></div>
<div class="card dk"><h4>Every month · 2 hours</h4><ol class="steps"><li>Monthly management pack (Reports).</li><li>Live simulation: are we on plan?</li><li>Targets and Accountability.</li><li>Compliance calendar ticked.</li><li>AI cost: is the cheap path working?</li><li>Raise or lower each agent's autonomy.</li></ol></div></div>""")
    o.append(h2('Logging by hand and talking to the AI'))
    o.append("""<p>You never have to wait for an automation. <b>+ Log</b> in the header records a number, an expense, a task or a note from any page, marked <i>manual</i>. <b>Ask AI</b> answers questions about the page you are on (for example on Sales: <i>"which deals have gone quiet for two weeks?"</i>) and can propose actions, which land in Approvals. On the AI hub page you can talk to one agent directly, for example the Finance agent about the cash forecast.</p>
<div class="note">Good questions are specific and name the outcome: <i>"Draft the follow-up for the Okello quote, friendly, mention the site visit slot on Tuesday"</i> works better than <i>"help with Okello"</i>.</div>""")

    # ================= PART 4: EVERY PAGE =================
    o.append(divider(4, 'Every page, explained', 'All 67 pages in menu order: what each is for, how to use it, and the logic under it. Use this part as a reference.', IM + '/kitchen_refit.jpg'))
    MENU = [('Main menu', ['daily', 'today', 'company', 'coach', 'learn', 'myday', 'notices', 'meetings', 'chat', 'calendar', 'team', 'plan', 'gantt', 'flows', 'reports']),
            ('Business', ['money', 'budget', 'sales', 'projects', 'studio', 'onboard', 'approvals', 'models', 'people', 'tools', 'content', 'cplan', 'xevents', 'seo', 'outreach', 'licences', 'pricing', 'feas', 'reach', 'edge', 'playbook']),
            ('Build and AI', ['aihub', 'autos', 'devkits', 'sysmap', 'aistaff', 'dbx', 'aicost', 'build', 'standards', 'quotes', 'plugins', 'templates', 'docs', 'files', 'sim']),
            ('Control', ['targets', 'impact', 'risk', 'log', 'wins', 'access'])]
    blurbs = {'Main menu': 'Daily work: the brief, your tasks, meetings, the calendar, the plan and reports.', 'Business': 'Running the five businesses: money, sales, projects, design, clients, content, pricing and growth.', 'Build and AI': 'The machine room: agents, automations, AI cost, the standards bank, templates, files and the Revit link.', 'Control': 'Targets, impact, legal and risk, numbers, wins, and who can see what.'}
    sec = 4
    for gi, (g, keys) in enumerate(MENU):
        if g == 'Control':
            o.append(h1(f'{sec}.{gi+1}', 'Registers'))
            o.append('<p class="lead">Registers are the lists the business runs on: 30 of them. Each one takes a paste from Excel or Google Sheets (copy the cells with the header row), exports to CSV or Excel, can be asked questions by the AI, and feeds its dates into the morning brief and the calendar. These nine are in the menu; All registers shows the rest (drawings, RFIs, variations, site diary, defects, permits, HSE, inventory, knowledge, training, leave, releases, recipes and more).</p>')
            o.append('<div class="entry">' + shot('regs', 'All registers. Example data.', 80) + '</div>')
            o.append('<table><tr><th style="width:24%">Register</th><th>What it holds</th></tr>' + ''.join(f'<tr><td><b>{n}</b></td><td>{d}</td></tr>' for k, n, d in REGISTERS) + '</table>')
            o.append('<div class="entry">' + shot('reg-pricebook', 'The Price book register: add an entry, paste from Excel, search, export, or ask the AI about the list.', 78) + '</div>')
            o.append(hood('One generic register engine drives all of them from schema strings (<code>REGS</code>): each register is a collection <code>reg_&lt;name&gt;</code> with typed fields. Dates in any register (expiry, due, next service) become alerts in the brief. Admin-only registers are locked in the database rules.'))
        o.append(h1(f'{sec}.{gi+1 + (1 if g == "Control" else 0)}', g + (' pages' if g != 'Main menu' else '')))
        o.append(f'<p class="lead">{blurbs[g]}</p>')
        for k in keys:
            what, steps, under = PAGES[k]
            name = PJ[k]['name'].split('\n')[0]
            HEADS.append(('', name, 'x'))
            o.append(f'<div class="entry"><div class="ehead"><h3><span class="mk">@@H{len(HEADS)}@@</span>{e(name)} <span class="grp">{g}</span></h3>' + shot(k, None, 78) +
                     f'<p class="what">{e(what)}</p></div><div style="break-inside:avoid"><span class="tag">How to use it</span><ol class="steps">' + ''.join(f'<li>{e(s)}</li>' for s in steps) +
                     f'</ol></div>{hood(e(under))}</div>')
    o.append('<h3 style="margin-top:4mm">Standards bank: a search in action</h3>' + shot('standards_search', 'Searching "walls" with Uganda first: the clause, the page and a short summary in our own words. The standard itself is never shared.', 88))

    # ================= PART 5: WORKFLOWS =================
    o.append(divider(5, 'How the work flows', 'The main journeys through the system, step by step: from a lead to cash, from a sketch to a building, from a topic to a subscriber.', IM + '/landscape.jpg'))
    o.append(h1('5', 'Lead to cash').replace('<h1', '<h1 style="break-before:auto"'))
    o.append('<p class="lead">The journey that pays for everything. Every arrow is measured on the Flowcharts page; the weakest one is where to work this week.</p>')
    o.append(chain([('A lead arrives', 'From content, the website, a referral or an event', 'd'), ('Enquiry logged', 'Enquiries and auto-quotes; lead score', ''), ('Reply in 5 minutes', 'Auto-reply with the cost guide and a booking link (EM-02)', 'k'), ('Meeting booked', 'First free slot in the calendar', ''),
                    ('Quote or proposal', 'Priced from Pricing and efficiency, as a Word document; under 4 hours', 'k'), ('Won or lost', 'Lost: reason logged, reactivation in 90 days (SL-12)', ''), ('Onboarding', 'Contract, deposit invoice (40%), project and portal created', 'k'), ('Project runs', 'Playbook, site diary, weekly client update', ''),
                    ('Milestone billing', 'Invoices at each stage, receipts, ledger (FN-09)', 'k'), ('Handover', 'Final drawings and invoice, offboarding journey', ''), ('Review and referral', 'Satisfaction pulse, referral link, rating', 'k'), ('Next lead', 'Happy clients refer the next one', 'd')]))
    o.append(h2('Client onboarding, step by step (Studio design)'))
    src_obl = src[src.find("const OBL="):]
    steps = re.findall(r"\['([^']*)','([^']*)',(\d+),'([^']*)','([^']*)'\]", src_obl[:src_obl.find('off:[')])
    o.append('<table><tr><th>Step</th><th style="width:13%">Owner</th><th style="width:8%">Day</th><th style="width:16%">Template or register</th><th style="width:18%">Automated</th></tr>' + ''.join(f'<tr><td>{e(a)}</td><td>{e(b)}</td><td>{c}</td><td>{e(d)}</td><td>{e(x) or "<span class=muted>by hand</span>"}</td></tr>' for a, b, c, d, x in steps) + '</table>')
    o.append('<p class="muted" style="font-size:8.4pt">The same kind of journey, with its own steps, exists for Construction and design-and-build, Concrete, Stores, BIM services, Formcraft Tools and families, and Advisory, each with an offboarding journey.</p>')

    o.append(h1('', 'Sketch to building', 's').replace('<h1', '<h1 class="cont" style="break-before:page"'))
    o.append('<p class="lead">Design moves from a fast 2D sketch, which the client can see and comment on, to a Revit model, checked drawings and the authority approval, without retyping anything.</p>')
    o.append(chain([('Brief and site', 'Questionnaire, survey, planning rules', 'd'), ('Sketch in the studio', 'Walls, rooms with target areas, doors, windows, dimensions', ''), ('Client comments', 'On the same board, as pins', ''), ('Design assistant', '"Move the kitchen wall 300 mm left": edits are logged and undoable', 'k'),
                    ('Revision sheets', 'Rev A, B, C with a decision log', ''), ('Hand-off file', 'fmc-cis/0.2: outline, walls, openings, decisions', 'k'), ('Revit builds it', 'The plugin creates walls and rooms (planned command)', 'k'), ('BIM model', 'Families from the factory; Gate A model check', ''),
                    ('Standards check', 'Clauses from the standards bank', ''), ('Approval guide', 'Steps, documents, fees for the authority', ''), ('Approval', 'Real approval times reported back', 'k'), ('Construction', 'Playbook and site diary', 'd')]))
    o.append(shot('studio', 'The Design studio: a sketch at Rev B with a client comment pinned in the kitchen. Example data.'))

    o.append(h1('', 'The content factory', 's').replace('<h1', '<h1 class="cont" style="break-before:page"'))
    o.append('<p class="lead">The goal: <b>2,000 YouTube subscribers by 31 December 2027</b>, about 143 new subscribers a month. The engine is three Revit Shorts and one longer tutorial a week, produced mostly by automation, with Esther approving.</p>')
    o.append(chain([('Topic list', '52 weeks of Revit topics plus guides for each Formcraft tool', 'd'), ('Script', 'Drafted by the content agent from the topic', ''), ('Recorded in Revit', 'VC-08 tutorial recorder runs the steps', 'k'), ('Assembled', 'Voice-over, captions, thumbnail (VC-09)', 'k'),
                    ('Approved', 'Esther approves or sends back', ''), ('Posted', 'YouTube, Shorts, Reels, TikTok, LinkedIn on schedule', 'k'), ('Measured', 'Views, click-through, subscribers, leads per 1,000 views', ''), ('Target', '2,000 subscribers; leads into Sales', 'd')]))
    o.append(h2('Events'))
    o.append('<p>One event a month for Formcraft, one a quarter for each founder. The event finder (DD-14) searches weekly; you pick, go, and mark Attended; a follow-up task makes sure the people you met reach Sales and the directory.</p>')
    o.append(h2('Standards bank'))
    o.append(chain([('A standard we own', 'Bought legally; the file stays private', 'd'), ('Sections added', 'Clause, page, topics, a summary in our words', ''), ('Topic search', '"walls", "setbacks", "fire escape"', ''), ('Country first', 'Uganda first in Uganda, Kenya first in Kenya, then EAC, then international', 'k'), ('What it says', 'Clause and page reference', ''), ('Where to buy it', 'Link to the publisher; never the PDF', 'k')], cols=3))
    o.append(h2('Professionals directory'))
    o.append(fig('dir.svg', 'Figure 5.1 · Confirm first: nobody is public until they agree or their registration is checked.', 70, 150))

    o.append(h1('', 'The money cycle', 's').replace('<h1', '<h1 class="cont" style="break-before:page"'))
    o.append(chain([('Price', 'Pricing sets the rate the plan needs', 'd'), ('Quote', 'Auto-quote, deposit 40%', ''), ('Invoice', 'Numbered from the template register', ''), ('Paid', 'Mobile money or bank; receipt sent', 'k'),
                    ('Ledger', 'Income and expenses with receipts', ''), ('Forecast', '12 months; USD 15,000 buffer', 'k'), ('Tax', 'PAYE, NSSF, WHT by the 15th; VAT once registered', ''), ('Report', 'Monthly pack; profit and cash', 'd')]))
    o.append(h2('How AI work becomes scripts'))
    o.append(chain([('AI does a job', 'Logged with its intent, inputs and result', ''), ('Third time', 'Same intent, similar inputs, three times', ''), ('Script written', 'Developer agent writes it with tests', 'k'), ('Approved', 'Emlyn approves in the development room', 'd'), ('Runs free', 'Level 0 from now on', 'k'), ('Watched', 'A failed check pauses it; AI takes over until fixed', '')], cols=3))

    # ================= PART 6: AUTOMATIONS =================
    o.append(divider(6, 'Automations and bots', 'All 128 automations on the journey, by group, and how each one moves from an idea to live.', IM + '/sofa.jpg'))
    o.append(h1('6', 'The automation catalogue').replace('<h1', '<h1 style="break-before:auto"'))
    o.append('<p class="lead">Each automation is written once as a recipe (trigger, steps, checks, who reviews), then built, tested and switched on. Seventy of them have an upgrade that adds context from another register, so they reason instead of only reminding. Build the basic version first.</p>')
    o.append(chain([('Idea', 'Described with a trigger and hours saved', ''), ('Planned', 'Recipe written; phase set', ''), ('Building', 'Script or flow made', 'k'), ('Testing', 'Runs alongside a person', 'k'), ('Live', 'Runs on its own; sampled weekly', 'd'), ('Paused', 'Stopped after a failed check', '')], cols=6))
    AG = ['Email', 'Social media', 'Video and content', 'Founder voice and brand', 'Sales and leads', 'Clients and projects', 'Finance', 'People', 'Software and data', 'Website and SEO', 'Operations', 'Data, scrapers and documents', 'Alerts and accountability']
    from collections import defaultdict
    A = defaultdict(list)
    for m in re.finditer(r"A\('([A-Z]{2}-\d\d)',(\d+),'([^']*)','([^']*)'", src): A[int(m.group(2))].append((m.group(1), m.group(3), m.group(4)))
    rows = ''
    for gi2 in range(len(AG)):
        L = sorted(A[gi2])
        rows += f'<tr><td><b>{AG[gi2]}</b><br><span class="muted">{len(L)} automations</span></td><td>' + ' · '.join(f'<b>{c}</b> {e(n)}' for c, n, d in L) + '</td></tr>'
    o.append(f'<table><tr><th style="width:22%">Group</th><th>Automations (code and name)</th></tr>{rows}</table>')
    o.append(f'<p class="muted" style="font-size:8.4pt">Total: {sum(len(v) for v in A.values())}. The full description, trigger, tools and hours saved for each are on the Automations and bots page.</p>')
    o.append(h2('The first ten to switch on'))
    o.append("""<p>The automations that bring in or protect cash come first: they pay for the rest.</p><table><tr><th style="width:12%">Code</th><th>Automation</th><th>Why first</th></tr>""" +
             ''.join(f'<tr><td><b>{c}</b></td><td>{e(n)}</td><td>{w}</td></tr>' for c, n, w in [
                 ('EM-02', 'Lead reply in 5 minutes', 'Speed wins leads'), ('SL-01', 'Lead capture to CRM', 'No lead is lost'), ('SM-02', 'DM and WhatsApp assistant', 'Where Ugandan clients write'),
                 ('EM-01', 'Inbox triage', 'Frees founder hours every day'), ('FN-09', 'Milestone billing', 'Cash arrives on time'),
                 ('SM-03', 'Scheduled posting', 'Content goes out without a person'), ('VC-08', 'Revit tutorial recorder', 'The subscriber engine'),
                 ('AL-09', 'KPI snapshot against the plan', 'The founders see the truth weekly'), ('SD-09', 'System health and AI check', 'Catches failures early'), ('DD-01', 'Price scraper', 'Quotes on current prices')]) + '</table>')

    # ================= PART 7: DEVELOPMENT PLAN =================
    o.append(divider(7, 'The development plan', 'What is built, what comes next, and the rules for building it: from the Command Centre today to the Formcraft Hub for Windows.', IM + '/school.jpg'))
    o.append(h1('7', 'Where we are').replace('<h1', '<h1 style="break-before:auto"'))
    o.append("""<table><tr><th style="width:27%">Part</th><th style="width:15%">State</th><th>What it is</th></tr>
<tr><td><b>Command Centre</b></td><td><span class="pill" style="background:#d9f5e3">Running</span></td><td>The app in this guide: one file, running in claude.ai with its own database. Tested with automated browser tests before every release.</td></tr>
<tr><td><b>Web version</b></td><td><span class="pill" style="background:#fdecd2">Built, not deployed</span></td><td>The same app on Firebase (Firestore, Auth, Storage) with an AI adapter for any provider, installable on phones and PCs. For employees.</td></tr>
<tr><td><b>Formcraft MCP server</b></td><td><span class="pill" style="background:#fdecd2">Built, not in daily use</span></td><td>Lets Claude Desktop or any AI tool read the brief, query registers, propose actions and keep memory, with approvals.</td></tr>
<tr><td><b>Formcraft Tools for Revit</b></td><td><span class="pill" style="background:#d9f5e3">In development</span></td><td>C# add-in plus its own MCP server; supports several Revit windows.</td></tr>
<tr><td><b>Website</b></td><td><span class="pill" style="background:#d9f5e3">Live</span></td><td>React and Firebase; will host the standards bank, approvals guides and directory.</td></tr>
<tr><td><b>Formcraft Hub for Windows</b></td><td><span class="pill">Planned</span></td><td>The founders' app and the MCP hub for everything (below).</td></tr>
<tr><td><b>Automations</b></td><td><span class="pill" style="background:#f9d6d1">0 of 128 live</span></td><td>All designed with recipes; none switched on yet.</td></tr></table>""")
    o.append(h2('The roadmap'))
    M = ['Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
    bars = [('Put the real business in', 0, 0.5, '#c0392b'), ('90-day focus: cash features only', 0, 3, DT), ('Foundation sprint (P0)', 0, 2.3, NAVY),
            ('First 10 automations live', 0.5, 3, '#5fa9a0'), ('Web version on Firebase + backups', 0.5, 1.5, '#5fa9a0'),
            ('Hub phase 0-1: skeleton, data and sync', 3, 1.2, NAVY), ('Hub phase 2-3: approvals, models, agents', 4.2, 1, NAVY), ('Gate: 60-day review check passed', 5.2, 0.15, '#b7791f'),
            ('Hub phase 4: MCP hub and Revit', 5.3, 0.8, NAVY), ('Hub phase 5-6: content, website, dev room', 6.1, 1.4, NAVY), ('Voice: notes, talk back, supplier calls', 6.5, 2, '#5fa9a0'), ('Prove the model (P1) runs all 2027', 2.3, 7.7, '#9aa8af')]
    o.append('<div class="gantt"><div class="scale"><div></div><div>' + ''.join(f'<span>{m}</span>' for m in M) + '</div></div>' + ''.join(
        f'<div class="row"><div>{e(t)}</div><div class="track"><div class="bar" style="left:{s/10*100:.1f}%;width:{max(w/10*100,1.5):.1f}%;background:{c}"></div></div></div>' for t, s, w, c in bars) + '</div><p class="cap">November 2026 to August 2027. The hub is about 18 weeks of part-time work for one developer; it starts after the 90-day focus, and phase 4 waits for the review gate.</p>')
    o.append(h2('The 90-day focus rule'))
    o.append('<div class="warn">For the next 90 days we build <b>only what brings in or protects cash</b>: the proposals and pricing engine, the first ten automations, the Revit tutorials for the channel, the family store, backups and the Firebase move. Everything else waits. The audit found the plan\'s biggest risk is building tools instead of selling.</div>')
    o.append(h2('Foundation sprint, week by week'))
    wk = [('2 Nov', 'Server tests, rulebook data model, IP and accounts'), ('9 Nov', 'Server tests, journal and handover, standards register'), ('16 Nov', 'Server release, funnel pages, first recipes'), ('23 Nov', 'WhatsApp assistant, CRM, standards bank model'), ('30 Nov', 'Client portal v1: accounts, project page, sign-off'), ('7 Dec', 'Portal model viewer, content scripts, standards catalogue'), ('14 Dec', 'Finance automation, script library, edge tests'), ('21 Dec', 'Kit 1 release and swap drill'), ('28 Dec', 'Gate review and plan Q1 2027')]
    o.append('<table><tr><th style="width:16%">Week of</th><th>Work</th></tr>' + ''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in wk) + '</table>')

    o.append(h1('', 'The Formcraft Hub for Windows', 's').replace('<h1', '<h1 class="cont" style="break-before:page"'))
    o.append('<p class="lead">The Hub is the founders\' app: the Command Centre inside a Windows program built the same way as Revit, holding all Formcraft data, connecting to AI models offline or in the cloud, and acting as the MCP hub every app connects through. Only the three founders have it; employees use the web version.</p>')
    o.append("""<table><tr><th style="width:20%">Area</th><th style="width:40%">Decision</th><th>Why</th></tr>
<tr><td>App</td><td>C# .NET 8 with WPF on <code>Formcraft.Shell</code>; Command Centre pages inside WebView2</td><td>One language and one look with the Revit tools; official C# MCP SDK</td></tr>
<tr><td>Online data</td><td>Firebase: Firestore, Auth, Storage, Functions, Hosting</td><td>The website and the web version already use it</td></tr>
<tr><td>Local data</td><td>PostgreSQL on each hub</td><td>Years of history, SQL reports, change log, recovery</td></tr>
<tr><td>Offline AI</td><td>7-8B model (Q4) for the default tier, 3-4B for quick, on the main PC</td><td>Fits 16 GB RAM and a 4 GB graphics card</td></tr>
<tr><td>Cloud AI</td><td>Any provider through one adapter, by tier</td><td>Swapping is a setting</td></tr>
<tr><td>Jobs</td><td>Hangfire queues, YARP routing, Polly retries</td><td>Load balancing, retries, health checks every 30 s</td></tr>
<tr><td>Revit</td><td>Existing add-in; each window on a port 8080-8089</td><td>Two or more Revit windows run jobs in parallel</td></tr>
<tr><td>Updates</td><td>Velopack installer and auto-update</td><td>All three hubs stay on the same version</td></tr></table>""")
    o.append("""<table><tr><th style="width:24%">Phase</th><th style="width:9%">Weeks</th><th>Delivers</th><th style="width:30%">Done when</th></tr>
<tr><td><b>0 Skeleton</b></td><td>1-2</td><td>Solution, service and tray app, PostgreSQL, Firebase sign-in, Command Centre in WebView2</td><td>Starts on boot; restarts after a crash; all three founders sign in</td></tr>
<tr><td><b>1 Data and sync</b></td><td>3-5</td><td>Firestore ↔ PostgreSQL mirror, change log, outbox, roles, nightly backups</td><td>An edit shows on the others in 5 s; 50 offline edits sync in order; a restore drill passes</td></tr>
<tr><td><b>2 Approvals and monitor</b></td><td>6-7</td><td>Shared approval queue with risk rules, the monitor screen, review sampling, purpose and context packs</td><td>A high-risk action waits for two founders</td></tr>
<tr><td><b>3 Models and agents</b></td><td>8-9</td><td>Level router, escalation, answer cache, budgets, the 8 agents, memory and handover</td><td>Works with no internet; falls back to the cloud; unloads the model when Revit starts</td></tr>
<tr><td><b>Gate</b></td><td></td><td colspan="2">Founders decide every proposal within 24 hours, nothing waits over 48 (the 60-day review check)</td></tr>
<tr><td><b>4 MCP hub and Revit</b></td><td>10-12</td><td>Connection registry, the hub's MCP server, per-window Revit queues, lease and failover</td><td>Jobs run on both Revits; a frozen Revit's jobs move; the standby takes over</td></tr>
<tr><td><b>5 Content and website</b></td><td>13-15</td><td>Social calendar and posting, newsletters, website publishing, enquiries, orders</td><td>A post goes from draft to posted with metrics</td></tr>
<tr><td><b>6 Dev room and installer</b></td><td>16-18</td><td>GitHub, test runs, builds and releases, script promotion, installer and auto-update</td><td>An update reaches all three hubs</td></tr></table>""")
    o.append(hood("Solution <code>Formcraft.Hub.sln</code>: <code>Hub.Core</code> (types, roles, risk policy) · <code>Hub.Data</code> (Npgsql + EF Core, change log, outbox) · <code>Hub.Sync</code> (Firestore listeners, lease and heartbeat) · <code>Hub.Jobs</code> (Hangfire, router, Polly) · <code>Hub.Mcp</code> (MCP client registry and server) · <code>Hub.Models</code> (Ollama and cloud adapters, keys in Credential Manager) · <code>Hub.Revit</code> (instances, per-window queues, guard rules) · <code>Hub.Content</code> · <code>Hub.Dev</code> · <code>Hub.Service</code> (background host) · <code>Hub.App</code> (WPF). Main hub writes a heartbeat to <code>hub/lease</code> every 30 s; if it is 5 minutes old the standby founder PC takes the lease and runs cloud-only jobs. Payment confirmations and website auto-replies run in Firebase Functions so they never wait for a PC. Full plan: <code>docs/windows-hub-plan.md</code>."))

    o.append(h1('', 'Revit, voice and the rules for building', 's').replace('<h1', '<h1 class="cont" style="break-before:page"'))
    o.append(h2('A simpler Revit plugin'))
    o.append('<p>The plugin keeps only what needs the live model: the open document, the current view or selection, or a one-click action while modelling. Settings, data, queues, reports and work across apps move to the Hub. Designers get a lighter plugin; the Hub controls development and testing of the tools.</p>')
    o.append(h2('Voice'))
    o.append("""<div class="grid2"><div><ul><li><b>Transcription and voice notes:</b> speak a site note or a meeting; it becomes text, tasks and log entries.</li><li><b>Talk to the system:</b> ask aloud, hear the answer.</li><li><b>Founder voices:</b> cloned only with the founder's written consent, used for tutorials and voice-overs.</li></ul></div>
<div><ul><li><b>Supplier price calls:</b> an automated call asks today's price; the answer updates the price book.</li><li><b>Directory checks:</b> a call asks a professional to confirm their details and consent to show their number.</li><li><b>Rules:</b> every automated call says it is an automated assistant for Formcraft, and recordings follow the data protection law.</li></ul></div></div>""")
    o.append(h2('Rules for building'))
    o.append("""<div class="grid2"><div class="card"><h4>Build only what gets used</h4>A feature is built when someone will use it this month. Otherwise it waits in the Build list.</div>
<div class="card"><h4>Test every change</h4>Every release of the app passes the syntax check and the browser tests (no page errors) before it is published.</div>
<div class="card"><h4>One source of rules</h4>Rulebooks and guard rules live in one place; every app reads them, none keeps a copy.</div>
<div class="card"><h4>Write it down</h4>Every request and decision is logged (<code>docs/requests-log.md</code>, Decisions and learning), so the next person, or the next AI, knows why.</div></div>""")

    # ================= PART 8: GAPS =================
    o.append(divider(8, 'The honest gaps', 'What is missing between the plan and the system, and the next 30 days that close the most important ones.', IM + '/mvule_wardrobe.jpg'))
    o.append(h1('8', 'The gaps, ranked').replace('<h1', '<h1 style="break-before:auto"'))
    o.append('<p class="lead">An honest audit of the live system on 30 October 2026, ranked by how much each gap could stop the plan.</p>')
    gaps = [('The system holds no real business yet', 'No deals, projects, ledger entries or logged numbers. Every dashboard and simulation runs on nothing.', 'One week: put the real business in (Part 3).'),
            ('More is being built than sold', 'About 65 pages, 128 automations and 28 AI roles designed; none live; one developer who also runs Revit tools, the website and client work.', 'The 90-day focus rule.'),
            ('Legal papers not proven done', 'IP assignment to the company, shareholders\' agreement with vesting, registration confirmed, Personal Data Protection Office registration.', 'Sign and upload them; tick them on Legal and risk.'),
            ('No professional sign-off workflow', 'AI drafts layouts, BOQs and checks, but nothing records who signs drawings; no professional indemnity or contractor\'s all-risks insurance recorded.', 'Add a sign-off step for drawings; buy the insurance.'),
            ('One account, one PC', 'All data under one claude.ai account; backups not routine yet.', 'Weekly backup; move to Firebase.')]
    o.append('<table><tr><th style="width:4%">#</th><th style="width:26%">Gap</th><th>What we found</th><th style="width:27%">Fix</th></tr>' + ''.join(f'<tr><td><b>{i+1}</b></td><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>' for i, (a, b, c) in enumerate(gaps)) + '</table>')
    o.append(h2('Real, but not plan-stopping'))
    o.append("""<ul><li><b>Revenue engine:</b> the USD 1M target is not yet turned into weekly numbers per division (leads, quotes, wins, job size); the proposals engine is not built; family pricing and checkout are not decided.</li>
<li><b>Cash:</b> no real 13-week cash forecast and no funding pipeline entered.</li>
<li><b>Construction capacity:</b> AI cannot pour slabs: crews, foremen, subcontractors and equipment for a second site are not planned.</li>
<li><b>The founders' review rhythm:</b> roles not confirmed, standby PC not chosen, and the review queue needs decisions within 24 hours.</li>
<li><b>Clients:</b> the client portal, client access to the studio and after-sales follow-up are planned, not built.</li>
<li><b>The app's size:</b> one large file; a feature freeze and tests on every change are now in place. (This guide's own checks found and fixed a bug that blanked the money totals.)</li></ul>""")
    o.append(h2('The next 30 days'))
    o.append(chain([('Real data in', 'Pipeline, projects, cash, this month\'s money, leads and subscribers', 'd'), ('Legal papers', 'IP assignment, shareholders\' agreement, registration, data protection', 'k'), ('Sales numbers', 'Weekly targets per division from the USD 1M goal; build the proposals engine', 'k'),
                    ('Backups and Firebase', 'Weekly backup; move the data', ''), ('Founders reviewing', 'Confirm roles; agree a daily review time', ''), ('Feature freeze', 'Only what feeds cash until February', 'd')], cols=3))
    o.append(h2('Decisions we need from the founders'))
    o.append("""<ol class="steps"><li>Confirm each founder's role and the USD 500 two-founder threshold.</li><li>Choose the standby PC (Peter's or Esther's).</li><li>Choose the newsletter email service (for example Brevo, Mailchimp or Resend).</li><li>Agree the daily review time and who covers when someone travels.</li><li>Agree family and Formcraft Tools pricing (subscriptions and checkout).</li><li>Agree what the design studio shows clients (their own boards only).</li></ol>""")

    # ================= APPENDIX =================
    o.append(h1('A', 'Appendix: glossary and technical reference'))
    gl = [('Agent', 'An AI given one area (finance, sales...), its rulebook and tools. It proposes; founders approve.'), ('Approval', 'A founder\'s yes or no to something an agent proposed. Stored in the pending queue.'),
          ('Automation', 'A job that runs by itself on a trigger: an email, a date, a form. Built from a recipe.'), ('BIM', 'Building Information Modelling: a 3D model that carries data (quantities, cost, time).'),
          ('Collection', 'One kind of record in the database, like one sheet in a workbook.'), ('Context pack', 'What the hub gives an AI before a job: the scripts, memory lines and rules it needs, nothing more.'),
          ('Family', 'A Revit component (a door, a bed, a clinic fitting). The family factory makes them in batches.'), ('Firebase', 'Google\'s online database and sign-in service, used by the website and the web version.'),
          ('Gate A', 'The model check every Revit model and family passes before it is used.'), ('Handover pack', 'Memory, rules and state in one file, so another AI or a new hire continues from it.'),
          ('MCP', 'Model Context Protocol: the standard way AI tools connect to apps. Our MCP server gives AIs Formcraft\'s tools.'), ('Offline model', 'An AI that runs on our own PC, free and without internet (7-8B parameters).'),
          ('Recipe', 'A written rule for a job: trigger, steps, checks, reviewer. Every automation starts as one.'), ('Register', 'A list the business runs on: clients, suppliers, price book, contracts...'),
          ('RIBA stages', 'The standard design and construction stages 0 to 7 used for projects.'), ('Rulebook', 'An agent\'s written rules, kept in our repository so any model can follow them.'),
          ('Tier', 'Which AI model size does a job: offline, quick, default, complex, second opinion.'), ('Token', 'The unit AI providers charge by: about four characters of text.')]
    o.append('<table><tr><th style="width:20%">Term</th><th>Meaning</th></tr>' + ''.join(f'<tr><td><b>{a}</b></td><td>{e(b)}</td></tr>' for a, b in gl) + '</table>')
    o.append(h2('Where everything is'))
    o.append("""<table><tr><th style="width:36%">Path (repository formcraft_pioneer)</th><th>What it is</th></tr>
<tr><td><code>command-centre/index.html</code></td><td>The Command Centre app (one file)</td></tr><tr><td><code>command-centre/standalone/</code></td><td>Web version: Firebase runtime, AI adapter, rules, installable app files</td></tr>
<tr><td><code>mcp-server/server.js</code></td><td>The Formcraft MCP server</td></tr><tr><td><code>rulebooks/agents/*.md</code></td><td>Each agent's rulebook</td></tr><tr><td><code>rulebooks/client-onboarding-offboarding.md</code></td><td>The 7 client journeys</td></tr>
<tr><td><code>docs/command-centre.md</code></td><td>Feature reference for every page</td></tr><tr><td><code>docs/windows-hub-plan.md</code></td><td>The Hub plan (sections 1-17)</td></tr><tr><td><code>docs/architecture-ai-hub.md</code></td><td>AI hub architecture and the offline model</td></tr>
<tr><td><code>tools/test_*.js</code>, <code>tools/check_syntax.sh</code></td><td>Browser tests and the syntax check run before each release</td></tr><tr><td><code>simulations/</code>, <code>feasibility/</code></td><td>The simulations and the feasibility report</td></tr></table>""")
    o.append(h2('Design studio keys'))
    o.append('<table><tr><th>Key</th><th>Tool</th><th>Key</th><th>Tool</th></tr>' + ''.join(f'<tr><td><b>{a}</b></td><td>{b}</td><td><b>{c}</b></td><td>{d}</td></tr>' for a, b, c, d in [('V', 'Select and move', 'M', 'Dimension'), ('W', 'Wall', 'T', 'Text'), ('R', 'Room', 'P', 'Sketch'), ('D', 'Door', 'C', 'Comment'), ('N', 'Window', 'I', 'Import image'), ('Shift', 'Straight lines', 'Space', 'Pan (or middle button)')]) + '</table>')
    o.append(f'<div style="margin-top:12mm;text-align:center"><img src="{img(LOGO)}" style="height:9mm"><p class="muted" style="margin-top:3mm">Formcraft Design and Construction · Kampala · {DATE}<br>This guide is updated with each release of the Command Centre.</p></div>')

    body = ''.join(o)
    toc = ''
    for num, t, kind in HEADS:
        if kind == 'x': continue
        pg = tp.get(t, '')
        cls = 'p' if kind == 'p' else 's'
        label = (f'{num} ' if num else '') + t
        toc += f'<a class="{cls}"><span>{e(label)}</span><span>{pg}</span></a>'
    body = body.replace('@@TOC@@', toc)
    return f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>'

def render(htmlstr, path):
    open(f'{G}/guide.html', 'w').write(htmlstr)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(); pg.goto(f'file://{G}/guide.html', wait_until='networkidle')
        pg.pdf(path=path, format='A4', print_background=True, prefer_css_page_size=True); b.close()

def page_texts(pdf):
    n = len(PdfReader(pdf).pages); out = []
    for i in range(1, n + 1):
        out.append(' '.join(subprocess.run(['pdftotext', '-f', str(i), '-l', str(i), pdf, '-'], capture_output=True, text=True).stdout.split()))
    return out

def find_pages(pdf):
    T = page_texts(pdf); res = {}
    for idx, (num, t, kind) in enumerate(HEADS):
        m = f'@@H{idx+1}@@'
        for i, tx in enumerate(T):
            if m in tx: res.setdefault(t, i + 1); break
    return res, T

def overlay(src, dst, T):
    pdfmetrics.registerFont(TTFont('Inter', '/usr/share/fonts/opentype/inter/Inter-Regular.otf')) if False else None
    rd = PdfReader(src); wr = PdfWriter(); mark = ImageReader(LOGO)
    for i, pg in enumerate(rd.pages):
        if 'FCFULLPAGE' in T[i]: wr.add_page(pg); continue
        w, h = float(pg.mediabox.width), float(pg.mediabox.height)
        buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(w, h))
        c.drawImage(mark, w - 48 - 70, h - 38, width=70, height=70 / 4.604, mask='auto')
        c.setFont('Helvetica', 7.2); c.setFillColor('#6b7680'); c.drawString(48, h - 34, 'The Formcraft Command Centre · Founders\' guide')
        c.setStrokeColor(TEAL); c.setLineWidth(1); c.line(48, 34, w - 48, 34)
        c.drawString(48, 22, 'Formcraft Design and Construction · Confidential'); c.drawRightString(w - 48, 22, str(i + 1))
        c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); wr.add_page(pg)
    wr.add_metadata({'/Title': 'The Formcraft Command Centre: founders\' guide', '/Author': 'Formcraft Design and Construction'})
    wr.write(dst)

if __name__ == '__main__':
    os.makedirs(f'{G}/out', exist_ok=True)
    h = build(); render(h, f'{G}/out/pass1.pdf')
    pages, _ = find_pages(f'{G}/out/pass1.pdf')
    h = build(pages); render(h, f'{G}/out/pass2.pdf')
    pages2, T = find_pages(f'{G}/out/pass2.pdf')
    if pages2 != pages:
        h = build(pages2); render(h, f'{G}/out/pass2.pdf'); _, T = find_pages(f'{G}/out/pass2.pdf')
    overlay(f'{G}/out/pass2.pdf', f'{G}/out/Formcraft-Command-Centre-Guide.pdf', T)
    print('pages', len(T))
