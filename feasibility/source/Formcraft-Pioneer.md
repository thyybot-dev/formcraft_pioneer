# Formcraft Pioneer

Oct 29, 2026 · @emlyn

Formcraft is the template: every system that can be planned, checked or run with AI is built here first, proven on real projects, then copied to Soko Foods, Logistics, Nyumba and the Trade Assistant. The method is the one already proven in Formcraft Tools: AI works only through Formcraft's own tools and by Formcraft's written rules, and a named person checks the result before release.

## Where Formcraft stands today

Formcraft already has more systems than most firms ten times its size, but almost none of them run automatically yet. The building blocks exist; the work in 2027 is wiring them together.

**The business.**

- **Four divisions under one point of accountability:** Studio (BIM and CAD design, permits, renders), Construction (with partner contractors), Concrete (precast and green concrete) and Stores (furniture and joinery from the Kampala workshop), plus the Academy for artisans and students.
- **2026 revenue:** about UGX 50M, mostly design work; the Ogala project paid UGX 10M for architecture, structure, MEP and renders.
- **Team:** Emlyn builds; co-founders review and test; professionals are engaged per project.

**What is already built.**

- **Formcraft Tools:** a Revit add-in, a tools server and an AI agent working inside Revit through MCP, with written rules, dry runs and named human approval. The server is being rebuilt cleanly with tests F-001 to F-074.
- **Standards:** a 101-page BIM manual, 204 shared parameters, 412 keynote codes, ISO 19650 document control, RIBA stages 0–7, FIDIC-based contract forms.
- **Templates:** about 240 templates covering about 140 documents in nine families, all numbered FMC-\[FAMILY\]-\[TYPE\] from one brand kit, with slots for URA's EFRIS invoices.
- **Catalogues:** the healthcare family collection and 23 MEP calculation systems.
- **Website:** React and Firebase, 38 boards designed, mobile money (MTN, Airtel) and card payments through Flutterwave.

**What is missing.**

- No automated lead capture or follow-up; enquiries arrive by phone and social media and are handled by hand.
- Social media is small (about 65 followers) and posts are irregular; there is no YouTube channel yet.
- Quotes, invoices and reports are filled in by hand from the templates.
- Workshop and site data (cut lists, progress, photos) are not linked to the model.
- No dashboard: cash, pipeline and project health are not visible in one place.

## The technical stack: Formcraft Tools and the Revit system

The Pioneer plan rests on technology Formcraft has already built for itself. Formcraft Tools is the clearest proof that the rulebook method works: an AI agent works inside Revit, but only through Formcraft's own tools and by Formcraft's written rules. Everything on this page copies that pattern to the rest of the business.

&#91;embedded content: The connectors layer (Revit add-in and MCP server) is where the rulebook method was first proven\]

### Formcraft Tools: the five modules

- **Manage:** standards, templates, sheets, quality checks, worksharing and reviews. It applies the BIM Master Manual to every project.
- **Model:** the family factory, casework, MEP and structure help.
- **Flow:** everyday speed tools for every Revit user.
- **Build:** bills of quantities, progress, and 4D and 5D for quantity surveyors and managers. (4D and 5D are parked until the owner gives the go-ahead.)
- **Bench:** a phone app for craftsmen, which also captures workshop and site data for the metrics register.

All modules share one account and one settings page; buying happens on the website. The pilot runs on Revit 2025.

### The engine room: add-in, MCP server and AI agent

- **Revit add-in (C#, Revit API):** the code that runs inside Revit and carries out each action.
- **MCP server:** 50+ tools that Claude can call. Each tool does one checked job, such as placing a family, building a sheet, applying parameters or running a model check. Claude cannot touch the model any other way.
- **The rules:** written rules, a dry run before every change, and named human approval. This is the autonomy ladder and the "one door" rule, already working in Revit.
- **The rebuild:** the server is being rebuilt cleanly from November 2026 to February 2027, with numbered tests F-001 to F-074. In the 12-week foundation build (Part 7 of the AI plan), the first business recipes are released on the same rebuilt server.

### The family factory and the Formcraft standard

The family factory is the rulebook method in its purest form: **in** (a photo, a datasheet or a maker visit) → **core** (a written family recipe with sizes, materials and clearances) → **check** (flex tests and a named reviewer) → **out** (Revit, ArchiCAD, web 3D, cut list and render from the same recipe). Its engine built 371+ Revit families overnight, so it is also the first example of AI building a tool once and letting the tool do the repeat work (Part 8).

Every Formcraft family follows six rules from the healthcare catalogue:

1. Driven by labelled reference planes, so a new size is a new type, not a remodel.
2. Flex-tested at 80% and 125% of every size before release.
3. LOD 300 detail at Fine, a light envelope at Coarse.
4. MEP connectors on labelled planes with systems set (water, waste, medical gases, air, power, data).
5. Clearance zones from HBN, HTM and BS guidance on their own subcategories.
6. Full project data as shared parameters: keynote, IFC class, cost unit, power risk grade, supply source and more.

The first collection is the healthcare pack for Lubowa International Hospital: 604 families catalogued, built from the same recipes for Revit and ArchiCAD.

### Standards and data inside the stack

- **BIM Master Manual** (101 pages), **204 shared parameters**, **412 keynote codes**, **340 annotation families**: the shared language every model uses, and the template for the business's shared codes (RB-02).
- **ISO 19650** document control and status codes, shared with the template register, so BIM records and business records use one numbering logic.
- **Open BIM:** IFC for models, BCF for issues, COBie for handover. Every job has a main tool, a backup and a free fallback: Revit / ArchiCAD / Bonsai or FreeCAD for models; Robot / ETABS or Tekla / OpenSees for structures; Navisworks / Solibri / IfcOpenShell for clash checks; Blender Cycles / D5 Render / Blender for renders; One Click LCA / EnergyPlus for energy and carbon (main tool still to choose).

&#91;embedded content: Counts as reported in the pitch deck; the build queue moves weekly\]

### Formcraft cloud

- **Hosted central models:** one sandbox per client, with an AI model manager for audits and backups.
- **Cloud workstations:** extra modellers join big projects by a link, and Academy students learn on any laptop. Over two years, the deck estimates an own PC at about USD 119 a month (USD 2,500 upfront), a full-time cloud seat at about USD 211, and cloud for heavy jobs only (20 hours) at about USD 24. The rule: keep PCs for daily work and rent the cloud for peaks and rendering.
- **Blender render service:** a 4K still costs about USD 0.80 of GPU time and a 30-second walkthrough about USD 165 (AWS GPU prices, October 2026).
- The office runs on fibre with Starlink as backup.

### The stack as a business

The same stack is also a product. The revenue streams it supports, with their proposed start dates, are: healthcare and custom families (Q4 2026), BIM system setup for other firms (Q1 2027), Formcraft Tools licences (Q1 2027), the Blender render service (Q1 2027), model hosting and the AI manager (Q2 2027), cloud workstations (Q2 2027), and Bench premium with supplier partners (Q2 2027). Roadmap items include the family editor and hospital pack, the Manage beta, the cloud pilot and latency test, the Blender render pipeline, the first version of Bench, ArchiCAD parity with an IFC hub, and expansion to Kenya, Rwanda and South Africa.

### Honest limits of the stack today

- **Early stage:** 7 of 120 build-queue tasks are done; 56 wait on other tasks.
- **Version lock:** families are Revit 2025 files and do not open in older versions; each yearly Revit release can change the API the add-in depends on, so every release needs the F-series tests re-run.
- **Not yet professionally signed off:** the healthcare families are an evaluation sample, and discipline professionals' review is part of their sign-off.
- **Known Revit limits:** the Medical Equipment category cannot join pipe systems, so medical gas and water reach those items through a nested service point.
- **One builder:** most of the code and the recipes come from Emlyn. The work journal, handover notes and swap drill (Part 9) apply to the code as much as to the business.
- **Licence cost:** Revit and the wider Autodesk tools are the most expensive part of the stack, which is why licences are bought only when a rollout phase needs them.

## The client portal: one account, one federated model, 1D to 7D

This is the system Formcraft is developing for its customers. A client opens an account on the Formcraft website and, from then on, sees their whole project in one place. That includes a federated 3D model they can open in a browser, a cost estimate drawn from the Revit data, and live progress through the design stages and then on site. The same account carries the documents, approvals and payments. It turns Formcraft's internal data spine into something the client can see, and that transparency is Formcraft's main point of difference in Kampala.

&#91;embedded content: Built on the existing website (React and Firebase), Formcraft cloud and the Revit add-in\]

### The client's journey

1. **Open an account.** The client signs up on the website (one Formcraft account, as in the pitch deck), fills in the brief questionnaire (FMC-STD-BRF) and uploads plot details and photos. The AI assistant helps them complete it.
2. **Get a first review.** Within 48 hours, the client receives a project page with the brief summarised (1D), the plot and any existing drawings (2D), a first cost range for their budget, and the recommended package and fee.
3. **Follow the design.** Through RIBA stages 2 to 4, each design issue appears as a new version of the federated model in the viewer. The cost estimate is updated from the model's quantities, and a stage sign-off button (FMC-STD-STG) records the client's approval before the next stage starts.
4. **Tender and award.** The priced model and bill of quantities go to partner contractors in a bid session; the client sees a line-by-line comparison and approves the award.
5. **Watch construction.** The model shows what has been built week by week (4D), with site photos from the Bench app, valuations, change orders and budget against actual cost (5D). Milestone payments are made in the portal by mobile money or card.
6. **Receive the building.** At handover the client keeps the as-built model, the manuals, the warranties and a maintenance calendar (7D). Aftercare check-ins come through the same account.

### 1D to 7D, as Formcraft uses the terms

&#91;embedded content: Each dimension is a layer of data on the same federated model, not a separate file\]

- **1D – brief and data:** the client's needs, budget and site facts, stored as structured data, not just notes.
- **2D – drawings:** plans, sections, elevations and the permit set, generated from the model.
- **3D – the federated model:** architecture, structure and MEP (and any partner models in IFC) combined into one model the client can turn, cut and walk through.
- **4D – time:** each model element linked to a schedule task, so the client sees the planned and actual build sequence.
- **5D – cost:** quantities from the model multiplied by the rate library: estimates, the bill of quantities, valuations, change orders and budget against actual cost.
- **6D – sustainability:** energy, carbon and material choices (One Click LCA or EnergyPlus once chosen). In some countries 6D means operations instead; Formcraft records its own definitions in RB-02.
- **7D – operations:** the as-built model, COBie handover data, warranties and a maintenance plan for the life of the building.

**By stage of the project.** The level of detail grows with the RIBA stages. Stages 0–1 work in 1D and 2D with a cost range from similar buildings. Stages 2–3 bring the 3D concept and developed models with 5D estimates and a first 6D check. Stage 4 brings the full technical model, the bill of quantities and the 4D construction schedule. Stage 5 (construction) runs live 4D and 5D. Stages 6–7 deliver 7D handover and aftercare.

### How the data flows from Revit

- **Rich data at source.** Every Formcraft family already carries a keynote, IFC class, cost unit, supply source and more as shared parameters. The cost engine reads these directly, so quantities come from the model, not from re-measuring drawings.
- **Federation in the cloud.** Models are published to the client's hosted sandbox in Formcraft cloud (one sandbox per client, as in the pitch deck). The IFC engine combines the disciplines, runs clash checks and keeps each version under its ISO 19650 status code, so the client only sees issued versions.
- **A web viewer.** The browser viewer shows IFC models without Revit installed. Open-source viewers (such as That Open Engine or xeokit) or Autodesk Platform Services are the options; the choice follows the main, backup and free fallback rule.
- **Scripts, not hand work.** Cost updates, schedule links, progress percentages and the client summary are produced by tested scripts (Part 8 of the AI plan), so every client gets the same quality every time.
- **AI where it helps.** The AI assistant explains the client's model and costs in plain language, answers questions about their own project, and drafts the weekly update. It reads only that client's data, and anything about money or design changes goes to a named person (L2).

### The cost estimate: always a range

&#91;embedded content: Proposed targets; replace with Formcraft's measured estimate accuracy after the first projects\]

A cost shown to a client is a promise in their eyes, so the portal never shows a single figure before there is a priced bill of quantities. It shows a range that narrows stage by stage, with the assumptions listed beside it. Every project's final cost is compared with each earlier estimate, and that record becomes the KPI "final cost against estimate". It also lets Formcraft tighten the ranges over time.

### Rollout

The portal is built in steps that follow the pitch deck roadmap. The 4D and 5D items there are parked until the owner gives the go-ahead, so each step below is a proposal.

1. **Portal v1 (with the website build and the Manage beta, by Q2 2027):** account, brief, documents, stage sign-off, payments, and the 3D viewer for issued models. 5D shows cost ranges only.
2. **Portal v2 (with the cloud pilot, Q3–Q4 2027):** a federated model with clash checks, a live 5D estimate from model quantities, and bid sessions for partners.
3. **Portal v3 (2028):** 4D construction tracking with Bench site data, valuations and budget against actual cost.
4. **Portal v4 (2028 onwards):** 6D carbon and energy views, and 7D handover with COBie and a maintenance calendar. Later, it becomes a product other firms can license.

### What to measure

- Accounts opened and the share that become paying projects.
- Time from sign-up to first review (target under 48 hours).
- Client logins per month and questions answered by the assistant.
- Final cost against each stage's estimate.
- Stage sign-offs on time.
- Disputes and change orders per project (the transparency should reduce both).
- Referral rate from portal clients against non-portal clients.

### Honest limits

- **Bandwidth and devices.** Many clients will open the portal on phones over mobile data. Models must be simplified for the web, with a light view by default and the full view on demand.
- **Estimate liability.** An estimate shown on screen can be read as a quote. Every view states the stage, the range and the assumptions, and the contract figure comes only from the signed agreement.
- **Data privacy.** Client plans, budgets and photos are personal data under the Data Protection and Privacy Act 2019; each client sees only their own project, and consent is recorded before anything is used in content.
- **Partner models.** Federation depends on consultants delivering clean IFC, which is not yet common in Uganda; Formcraft's BIM execution rules must be in every appointment.
- **4D and 5D are the hardest part** and are currently parked on the roadmap. The portal is still valuable at v1 without them, but the full promise depends on them.

## AI in every function

Every part of Formcraft gets an AI job, and every job runs from a written recipe in the Formcraft rulebook, the same way every Revit family is built from a recipe. How far the AI may act depends on what a mistake would cost. Low-risk, reversible work runs on its own and is audited. Anything a client pays for or relies on is drafted by AI and approved by a named person. Anything signed, stamped, paid or safety-related stays with people.

&#91;embedded content: Autonomy levels are defined in the rules section below\]

**Function by function: what AI does, who approves, the number to watch.**

1. **Content and social.** AI turns site, workshop and Revit footage into edited videos, Shorts, captions, translations and posts. Emlyn or the brand lead approves each video. Watch: leads per month from content.
2. **Website and funnel.** AI writes and tests landing pages, keeps SEO current and sends follow-up messages. Runs alone within approved offers. Watch: visitor-to-sign-up rate.
3. **Sales assistant.** An AI assistant on WhatsApp and the website answers questions day and night, qualifies leads and books site visits. A person approves any price or promise. Watch: replies within 5 minutes; qualified leads per week.
4. **Quotes.** AI builds fixed-package proposals from the model's quantities and the price list. The studio lead approves every quote. Watch: quote sent within 48 hours; win rate 30%+.
5. **Briefs and design.** AI turns site-visit notes and voice memos into a written brief, suggests layout options and produces renders. The designer chooses. Watch: design rounds per project.
6. **BIM modelling.** The Revit agent places families, builds sheets and schedules, applies the 204 parameters and 412 keynotes, and checks the model against the BIM manual. Every change is a dry run first, then a named approval. Watch: errors found per sheet at review.
7. **Engineering checks.** AI pre-sizes members, runs the MEP calculations and flags clashes. The registered engineer always decides and stamps. Watch: RFIs per project.
8. **Estimating and buying.** AI produces bills of quantities from the model, compares supplier prices and drafts purchase orders. A person approves orders above a set limit. Watch: final cost within 5% of the estimate.
9. **Workshop.** AI generates cut lists, nests sheets to cut waste, writes CNC files and schedules production. The workshop lead checks the first piece of every batch. Watch: material waste and on-time delivery.
10. **Concrete.** AI drafts quotes from quantities and keeps mix and cube-test records. Test results and acceptance stay with the engineer. Watch: test failures.
11. **Site.** AI writes the daily site diary from photos and voice notes, compares progress with the 4D model and drafts RFIs and toolbox talks. Site instructions and variations are issued by the project manager. Watch: schedule slip in days; incidents (target zero).
12. **Finance and tax.** AI issues invoices through EFRIS, reconciles mobile money and bank, chases late payers and writes the monthly cash report. Payments and tax filings are approved by a person and the accountant. Watch: receivable days under 45; cash runway.
13. **People and Academy.** AI writes training modules, onboarding packs and skills tests, and screens applications. Hiring decisions are human. Watch: weeks for a new hire to work to the BIM standard.
14. **Aftercare.** AI sends handover manuals, warranty reminders, 3- and 12-month check-ins and referral asks. Runs alone. Watch: referrals per completed project.
15. **Document control.** AI fills templates, numbers every issued document and keeps ISO 19650 status codes current. Runs alone with weekly audit. Watch: documents reissued because of errors.

## Porter's value chain: the frame for every system

Michael Porter's value chain (from *Competitive Advantage*, 1985) splits a company into the activities that create value for the customer. **Primary activities** make and deliver the product: inbound logistics, operations, outbound logistics, marketing and sales, and service. **Support activities** run across all of them: firm infrastructure, people (HR), technology development and procurement. The **margin** is what is left when the customer pays more than all these activities cost.

Porter's point is that advantage comes from two places only: doing an activity **cheaper** than rivals (cost leadership) or doing it **differently enough** that customers pay more (differentiation). The strongest advantage comes from **linkages**, where one activity makes another cheaper or better. Rivals can copy a single activity; they struggle to copy a set of linked ones.

&#91;embedded content: Porter's value chain (1985) mapped to Formcraft\]

**How Formcraft uses it.**

- **One chain, one map.** Every system, template, AI job and KPI on this page belongs to one of the nine boxes. If a new tool fits no box, it probably creates no value and is not built.
- **Cost and value per activity.** Each month, Formcraft records the hours, money and AI spend that go into each activity, and the value it produces (leads, quotes won, hours saved, defects avoided). This shows where the margin is made and where it leaks.
- **The linkage is the moat.** The BIM model is the spine: it feeds quotes (sales), cut lists (operations), purchase orders (inbound), site progress (operations), transmittals (outbound) and handover manuals (service). A competitor can hire a designer or buy a CNC machine; copying a connected chain takes years.
- **Strategy choice.** In Kampala, Formcraft competes on **differentiation** (design quality, speed, transparency, one point of accountability), not on being cheapest. AI is used on the cost side too, so the extra quality comes without a higher cost base.
- **Where AI pays most.** Operations (the Revit agent and workshop automation) and marketing and sales (the content engine and assistant) are the shaded boxes. These two carry most of the hours, so they carry most of the savings.

**Using it in the other ventures, honestly.** Porter designed the chain for firms that make physical things. It fits Formcraft and Soko Foods well: grain moves through sourcing, silos, milling, distribution, shops and service. It fits less well for Nyumba, the logistics app and the Trade Assistant. These businesses earn by connecting people (a network) or solving problems (a service). For them, the later "value network" and "value shop" versions of Porter's idea (Stabell and Fjeldstad, 1998) describe the work better. The same discipline still applies: list the activities, cost each one, find the linkages, and put AI where the hours are.

## The rulebook method: run the business the way Formcraft Tools runs Revit

Formcraft Tools already proves how Formcraft works with AI. Claude works inside Revit, but only through the 50+ tools on Formcraft's MCP server and only by Formcraft's rules. The rules and data live in the Formcraft app, not in Revit and not in the AI. Every family is made from a written recipe, flex-tested, checked by a named reviewer and released in a numbered kit. The Pioneer applies exactly this method to the whole business: quotes, content, invoices, site diaries, purchase orders and hiring packs.

&#91;embedded content: The family factory method from Formcraft Tools, applied to every business task\]

**The same method, from Revit to the business.**

- **Family recipe → business recipe.** Each task gets one written recipe: its inputs, steps, rates, codes, limits, output template, autonomy level and approver. Claude follows the recipe; it does not improvise.
- **BIM Master Manual → Business Rulebook.** The 101-page manual says how a Formcraft model is built. The Business Rulebook says how Formcraft quotes, sells, buys, builds, invoices and hires. Claude reads it before every task, just as the Revit agent reads the manual.
- **Shared parameters and keynotes → shared business codes.** The 204 parameters and 412 keynotes give every model one language. The business gets one list of client, project, cost, rate and status codes, using the FMC numbering already in the template register. Every recipe uses the same codes, so the model, the quote, the purchase order and the invoice match.
- **MCP tools → business tools.** Claude acts only through approved tools on the same server: create a quote, issue an EFRIS invoice, post a video, log a site diary, raise a purchase order. It cannot reach money, files or clients in any other way. A tool that does not exist cannot be misused.
- **Flex test at 80% and 125% → edge tests.** A family is stretched to its limits before release. A recipe is tested at its extremes before release: the smallest and the largest job, missing information, a late payer, a price change, a client writing in Luganda.
- **Named reviewer → named approver.** Every recipe names the person who signs off its output, and that person's name is logged on every approval.
- **Kit v2.2 → rulebook kits.** Recipes are released together in numbered kits. Nothing runs from an unreleased or edited-in-place recipe; changes go into the next kit.
- **Build queue → one queue for every automation.** The same statuses used for the 120-task Revit build queue: done, in progress, ready to start, waiting on other tasks, needs a decision.
- **Tests F-001 to F-074 → tests for every recipe.** Each recipe carries numbered tests, and a failing test blocks the kit.
- **Main, backup, free fallback → the same for AI and software.** Every job has a main tool, a backup and a free or manual fallback. Because the rules live in the Formcraft app, switching AI provider, accounting system or social platform loses nothing.
- **Open BIM (IFC, BCF, COBie) → open business data.** Records are kept in open formats (CSV, PDF, standard accounting exports, EFRIS records), so no vendor can lock the data in.
- **"Strengths and limits" page → one for every recipe.** Like the healthcare catalogue, each recipe states plainly what it does well, what it cannot do yet, and the fix on the way.

**Example recipe: the package quote.**

- **Code:** FMC-RCP-SAL-001, released in rulebook kit 1.
- **In:** the qualified lead record, the site-visit brief, the chosen package and the model quantities.
- **Steps:** take quantities from the model, apply the current rate list, add the package fee, check against the two-source rule, fill the FMC-SAL quotation template, number it, and draft the cover message.
- **Limits:** no discounts above 5%; no quote above UGX 150M without a director; no promise of dates the build queue cannot meet.
- **Edge tests:** a one-room job, a five-storey job, a missing quantity, a changed cement price, a client asking in Luganda.
- **Level and approver:** L2; the studio lead approves, and the name and time are logged.
- **Fallback:** if the AI tool is down, the same recipe is followed by hand using the same template.

**The rules that hold it together.**

1. **No recipe, no automation.** A task is automated only after its recipe is written, tested and released in a kit.
2. **Tools only.** AI acts only through Formcraft's MCP tools, never directly on files, accounts or messages.
3. **Never alone.** Stamping drawings, signing contracts, paying money, structural and safety sign-off, and hiring stay with people, always.
4. **Dry run first.** Every change is previewed before it is applied, and can be undone.
5. **Two sources for numbers.** Quantities, prices and loads are checked against a second source before they reach a client.
6. **Logs and weekly audits.** Every AI action is logged with its recipe code and kit number; each week a person checks 10 random items per function.
7. **Every error becomes a test.** A mistake gets a root cause, a recipe fix and a new test in the next kit.
8. **Client data stays private.** Client files stay in Formcraft's own storage; tools get only what a recipe needs; clients agree in writing before their projects appear in content.
9. **Cost caps.** Each function has a monthly AI budget and an alert when spend passes it.
10. **Climbing the ladder.** A recipe moves up one autonomy level only after three months with no serious error; one serious error moves it down one level.

&#91;embedded content: Every recipe states its level and its named approver\]

## The tool stack behind the MCP server

An MCP server is only as useful as the applications it connects to. Claude does not draw, analyse or invoice by itself; it drives real software (Revit, Robot, Navisworks, Power BI, Blender and others) through tools on the Formcraft server. So every business function needs its applications chosen in advance, the same way the pitch deck already chooses a main tool, a backup and a free fallback for each BIM job.

&#91;embedded content: Main, backup and free fallback for every job, all behind the Formcraft MCP server\]

**Function by function: main tool, backup, free fallback.**

- **Design and BIM:** Revit; ArchiCAD; Bonsai or FreeCAD. Connected through the Formcraft Revit add-in and the existing MCP tools.
- **Visuals and walkthroughs:** Blender (Cycles); D5 Render; Blender. Feeds renders to the content engine.
- **Structural analysis:** Robot Structural Analysis; ETABS or Tekla; OpenSees. AI sets up the model and checks results; the engineer signs.
- **MEP calculations:** Revit MEP with the 23 Formcraft calculation systems; spreadsheets as fallback.
- **Clash checks and 4D:** Navisworks Manage; Solibri; IfcOpenShell. Issues travel as BCF.
- **Estimating and buying:** Revit schedules and the Formcraft rate library; spreadsheet with Power Query; the same template by hand.
- **Workshop:** Fusion CAM for CNC files, a cut-list nesting optimiser, and the Bench phone app for craftsmen.
- **Site:** the Bench app and site photos linked to Navisworks 4D; Google Drive folders as fallback.
- **Sales and CRM:** WhatsApp Business API and a CRM (HubSpot or Zoho); a shared spreadsheet as fallback.
- **Content:** DaVinci Resolve or CapCut for editing; YouTube, Meta and TikTok for publishing; the website on React and Firebase.
- **Finance and tax:** QuickBooks or Zoho Books; URA EFRIS; Flutterwave, MTN and Airtel for payments; spreadsheet fallback.
- **Dashboards and documents:** Power BI; Looker Studio; Autodesk Docs as the ISO 19650 common data environment, with Google Drive as fallback.

**Rules for the stack.**

- **One door.** Every application is reached only through a Formcraft MCP tool that carries a recipe code, so the rulebook applies whatever the software.
- **Buy at the gate.** A licence is bought when the rollout phase that needs it starts, not before. Revit or the AEC Collection costs roughly USD 3,000–3,800 per seat a year at list price, and Power BI Pro about USD 14 per user a month. In 2027 Formcraft's planned revenue is about USD 46,000, so tools bought too early take a large share of the year's income.
- **Free fallback ready.** Each recipe names its fallback tool, so a price rise, an outage or a lost licence slows the work but does not stop it.
- **Open formats between tools.** IFC, BCF and COBie for models and issues; CSV and PDF for business records. No single vendor holds the data.

## The Formcraft AI Plan

This is the plan for building the AI foundation properly, in order. It has seven parts: the rulebook's structure, the standards to collect, the source documents that hold the data, the risks a construction business must watch, the metrics to record, the KPIs, and the feedback loop. A 12-week foundation build at the end turns it into dated tasks. It runs alongside the MCP server rebuild (November 2026 to February 2027), so the first recipes and the first tools are released together.

### Part 1. The Business Rulebook: its structure

The rulebook is one set of numbered chapters in the Formcraft app, coded FMC-RB-00 to FMC-RB-13 and following the same numbering logic as the template register. Each chapter has one named owner, a version number and a list of the recipes inside it.

&#91;embedded content: Each layer is a chapter of the Business Rulebook with its own FMC-RB code and owner\]

- **RB-00 Policy.** Why Formcraft uses AI, the autonomy ladder, the never-alone list, who owns each chapter, and how a recipe is approved and released.
- **RB-01 Standards register.** Every law, code and standard Formcraft follows: its version, its source PDF, which chapters depend on it, and when it was last checked.
- **RB-02 Shared codes and data dictionary.** Client, project, cost, rate, status and metric codes. Every metric's exact definition, unit and source. This is the business equivalent of the 204 shared parameters.
- **RB-03 to RB-11 Recipe chapters.** One chapter per value chain activity: inbound and buying; Studio and BIM (which points to the BIM Master Manual); site and construction; workshop and concrete; outbound and handover; sales and content; service and aftercare; finance and tax; people, Academy and HSE.
- **RB-12 Technology.** The MCP tools, the tool stack with main, backup and fallback, data security, the test series and the kit release log.
- **RB-13 Metrics and reviews.** The KPI tree, the review calendar, the audit method and the corrective action process.

**Every recipe follows one template:** code, purpose, value chain activity, inputs, steps, rates and codes used, limits, output template, autonomy level, named approver, MCP tools used, fallback, edge tests, metrics it writes, the standards it relies on (with page references), and its "strengths and limits" note.

### Part 2. Standards to collect

The template register already uses ISO 19650-2, URA EFRIS, FIDIC, PPDA, the RIBA Plan of Work, ISO 8601, ISO 216 and WCAG 2.2 AA. The list below adds what a design-and-build firm using AI also needs. Items marked **(have)** are already referenced in Formcraft's documents.

**Ugandan law and regulation (collect first).**

- **Building Control Act 2013, Building Control Regulations 2020 and National Building Code 2019.** These set when professionals must be engaged, what plans must contain, the permit and occupation-permit steps, inspections and fees. Feeds RB-04, RB-05 and the permit tracker.
- **Engineers Registration Act and Architects Registration Act.** Who may sign and stamp drawings. Feeds the never-alone list.
- **Occupational Safety and Health Act 2006 (have).** Site and workshop safety duties, incident reporting. Feeds RB-11.
- **National Environment Act 2019 and NEMA guidelines.** When an environmental assessment is needed. Feeds RB-05.
- **Physical planning rules and the KCCA permit checklists and fee schedules.** Feeds the permit recipe.
- **Data Protection and Privacy Act 2019 and its 2021 Regulations.** Formcraft will hold client data and run a WhatsApp assistant, so it must register with the Personal Data Protection Office and follow the consent rules. Feeds RB-00 and RB-12.
- **VAT Act, Income Tax Act and the URA EFRIS guides (have).** Feeds RB-10.
- **Employment Act 2006 and the NSSF Act.** Contracts, PAYE and NSSF deductions. Feeds RB-11.
- **PPDA Act, regulations and standard bidding documents (have).** For public tenders. Feeds RB-08.

**Design and technical.**

- **One structural code family, chosen and written down:** Eurocodes (EN 1990, 1991, 1992 for concrete, 1993 for steel, 1997 for ground) or the British Standards still used locally. Mixing codes on one project is a common source of errors.
- **BS EN 206 for concrete (have)** and the UNBS-adopted standards for cement, reinforcing steel, blocks and timber. Get the current list from UNBS rather than relying on memory.
- **MEP standards** for the 23 calculation systems (CIBSE guides, wiring regulations as applied in Uganda), and **HBN, HTM and BS guidance (have)** for healthcare.
- **Accessibility standards** in the National Building Code.

**Information, BIM and measurement.**

- **ISO 19650 parts 1 and 2 (have), IFC (ISO 16739), BCF and COBie.** How models, issues and handover data move between tools.
- **A classification system:** Uniclass 2015 (based on ISO 12006-2), so cost codes, keynotes and specifications line up.
- **A measurement standard for bills of quantities:** RICS NRM 2, or whatever Ugandan quantity surveyors and clients expect. Record the choice in RB-02.
- **FIDIC contract forms (have):** Short Form for small jobs, Red or Yellow Book for larger ones.

**Management systems (use as structure now, certify later).**

- **ISO 9001 (quality):** the skeleton for recipes, audits and corrective action.
- **ISO/IEC 42001 (AI management):** the first certifiable standard for managing AI, built on the same structure as ISO 9001. Use its clauses to check that RB-00, RB-12 and RB-13 are complete.
- **ISO 45001 (safety), ISO 14001 (environment), ISO 31000 (risk) and ISO/IEC 27001 (information security):** for when contracts or investors ask for them.
- **IFRS for SMEs:** so the accounts can be read by banks and investors.

### Part 3. The PDFs and records that give the AI its data

**Formcraft's own (already in the project).** The BIM Master Manual, the Template Master Register and catalogue, the pitch deck, company profile, brand guide and healthcare catalogue.

**Formcraft's own (to collect).**

- Every past project file, starting with Ogala: drawings, models, BoQs, quotes, invoices, receipts, messages, site photos and the hours spent.
- Every quote sent since 2025, won or lost, with the reason.
- Bank, mobile money and EFRIS records for 2025–2026.
- Supplier invoices and price lists.
- Timesheets, or the best possible reconstruction of hours per project.

**Official PDFs.** The acts and regulations above (ULII publishes Ugandan acts free; KCCA publishes the Building Control Regulations), KCCA permit checklists and fee schedules, URA EFRIS user guides, NEMA guidelines and PPDA bidding documents.

**Market data.** UBOS construction price indices and the statistical abstract; a monthly price list for cement, steel, timber, blocks and fuel from at least two suppliers; professional fee guidelines from the Uganda Society of Architects and the Uganda Institution of Professional Engineers where published; competitor price lists; manufacturer datasheets for the families.

**How each PDF enters the system.**

1. It gets a source code (FMC-SRC-####), a version date and an owner, and is filed in the standards register.
2. AI extracts candidate rules from it, each with a page reference.
3. The chapter owner accepts or rejects each rule before it enters a recipe.
4. When a source changes (a new regulation, a new price list), every recipe that cites it is automatically flagged for review.

### Part 4. What a construction business must watch

These are the ways small design-and-build firms usually fail, with the control in the rulebook and the number that warns early.

- **Running out of cash while profitable on paper.** Control: deposits, staged payments tied to milestones, firm payment terms. Watch: receivable days, cash runway.
- **Under-pricing.** Control: model quantities, the two-source rule, a contingency line. Watch: final cost against estimate on every project.
- **Unpaid extra work.** Control: no work on a change until a variation order is signed (FIDIC). Watch: value of unsigned changes.
- **Material price swings and exchange rates.** Control: quotes valid 14–30 days, price adjustment clauses, monthly price tracking. Watch: cement and steel price change against quote.
- **Structural failure and defects.** Uganda has seen deadly building collapses and excavation failures. Control: engineer sign-off, inspection requests before covering work, concrete cube tests, non-conformance reports. Watch: failed inspections, cube test failures, defects at handover.
- **Site accidents.** Control: inductions, toolbox talks, PPE register, near-miss reporting. Watch: lost-time incidents, near misses reported.
- **Permit and compliance breaches.** Control: a permit tracker per project under the Building Control Regulations. Watch: days of work done without a valid permit (target zero).
- **Weak partner contractors.** Control: vetting, scorecards, retention. Watch: partner scores, rework by partner.
- **Theft and material loss.** Control: delivery notes, material requisitions, weekly stock counts. Watch: stock variance.
- **Design liability.** Control: only registered professionals sign; professional indemnity insurance. Watch: claims and disputes.
- **Tax and statutory penalties.** Control: monthly EFRIS, VAT, PAYE and NSSF checklist. Watch: filings on time.
- **Client data and AI misuse.** Control: PDPO registration, consent forms, MCP-only access. Watch: data incidents (target zero).
- **Depending on one person.** Emlyn runs five ventures; recipes must let others do the work. Watch: share of recipes run by someone other than Emlyn.
- **Depending on one client.** Watch: share of revenue from the largest client (keep under 40%).

### Part 5. The metrics register: what to record

Every record carries five tags so the AI can connect them: **project code, client code, recipe code, kit number, date.** Most metrics are captured automatically by the MCP tools; the rest are entered once, on the Bench app or the website.

**Inbound and buying.** Supplier price per item per month; delivery on time; quantity received against ordered; stock variance; share of buying through approved suppliers.

**Studio and BIM.** Hours per design stage; design rounds per project; errors found per sheet at review; model checks passed against the BIM manual; days from brief to stage sign-off.

**Site and construction.** Milestones on time; schedule slip in days; RFIs per project; inspection requests passed first time; non-conformance reports; daily diary completed; lost-time incidents and near misses; permit status.

**Workshop and concrete.** Material waste per sheet; orders delivered on time; first-piece rejections; cube tests passed; concrete delivered against ordered.

**Outbound and handover.** Documents issued with the correct ISO 19650 status; documents reissued because of errors; handover packs complete; snag items per project and days to close them.

**Marketing and sales.** Videos published; views, watch time and subscribers per channel; visitors and sign-ups on the website; leads by source; first reply time; qualified leads; site visits; quotes sent; quote turnaround; win rate; reasons for losing.

**Service.** Check-ins done; warranty claims; referrals per completed project; client score at close and at 12 months.

**Finance.** Revenue and gross margin per project; overhead per month; cash balance and runway; receivable days; invoices issued the same day; EFRIS errors; tool stack and AI cost per month.

**People and Academy.** Hours by person and project; utilisation; training hours; weeks for a new hire to reach the BIM standard; staff turnover.

**AI health (from RB-12).** Recipes released; value chain coverage; tasks run per recipe; approval turnaround; errors found in the weekly audit per recipe; tests passing; AI cost per output; fallback used.

### Part 6. KPIs and targets

Metrics are the raw records; KPIs are the few numbers reviewed every month. Each KPI has an owner, a target, an amber line and a red line.

&#91;embedded content: Every KPI has a definition in RB-02 and is fed by the metrics register below\]

**Targets for the end of 2027 (first year of the plan).**

- **Growth:** 20 qualified leads a month; quote win rate 30% or more; revenue at or above the plan's USD 135,000.
- **Profit and cash:** gross margin 25% or more per project; final cost within 5% of estimate; at least 3 months of cash runway.
- **Delivery and quality:** 85% of milestones on time; under 10 snag items per handover; RFIs falling project by project.
- **Safety and trust:** zero lost-time incidents; one referral for every two completed projects; client score of 8 out of 10 or more.
- **AI health:** rulebook kit 1 and kit 2 released; under 2% of audited outputs with a serious error; approvals within 24 hours; AI and tool costs under 5% of revenue.

These are starting targets. After six months of real data, each target is reset from Formcraft's own numbers, not from guesses.

### Part 7. The feedback loop

Implementation, testing, feedback and improvement are one loop, run at five speeds. Nothing improves unless it goes all the way round.

&#91;embedded content: Seven steps, run at five speeds: daily, weekly, monthly, quarterly, yearly\]

- **Daily:** the AI logs every task with its recipe code; the Bench app captures site and workshop data; any blocked approval is flagged by the next morning.
- **Weekly (Monday, 30 minutes):** audit 10 random outputs per function; review leads, quotes and cash; open a corrective action report (FMC-CAR) for every serious error.
- **Monthly:** the KPI review against amber and red lines; the value chain scorecard (cost and value per activity); decide which recipes need changing.
- **Quarterly:** release the next rulebook kit with its changed recipes and new tests; review autonomy levels (up after three clean months, down after a serious error); check the standards register for new laws or prices.
- **Yearly:** a full rulebook review against ISO 9001 and ISO/IEC 42001; reset targets from real data; decide which proven recipes to copy to the other ventures.

**Automatic triggers.**

- A KPI red for two months in a row opens a corrective action report with a named owner and a 30-day deadline.
- A serious error moves its recipe down one autonomy level at once; a root cause and a new test are due within 7 days.
- A changed source PDF flags every recipe that cites it.
- A recipe unused for 90 days is reviewed: keep it, change it or retire it.

### The foundation build: 12 weeks, November 2026 to January 2027

1. **Week 1:** create the rulebook in the Formcraft app with chapters RB-00 to RB-13; name an owner for each; write RB-00 (policy, ladder, never-alone list).
2. **Week 2:** collect the Ugandan law PDFs in Part 2; give each a source code; start the PDPO registration.
3. **Week 3:** collect the technical and management standards; choose the structural code family and the measurement standard; record both in RB-01.
4. **Week 4:** write RB-02: client, project, cost, rate and status codes, plus definitions for every metric in Part 5.
5. **Week 5:** back-fill 2025–2026 data from past projects, quotes, bank and EFRIS records, to give a starting point for every KPI.
6. **Weeks 6–7:** write the first five recipes: lead reply, package quote, EFRIS invoice, document numbering and issue, and weekly video cut.
7. **Week 8:** write edge tests for the five recipes; connect them to MCP tools in the server rebuild; run dry runs.
8. **Week 9:** release rulebook kit 1 at level L2, with named approvers.
9. **Week 10:** build dashboard v1 in Power BI (or Looker Studio, free) with the 12 outcome KPIs and 5 AI health KPIs.
10. **Week 11:** run the first weekly audits and the first corrective action reports.
11. **Week 12:** gate review. Kit 1 passes if all its tests pass, the audit shows under 5% serious errors, and every KPI has a starting figure. Then scope kit 2.

**Honest view.** This foundation is slow, unglamorous work: about 12 weeks before AI saves much time. That is the point. The simulation above shows the gain comes from stopping errors, and errors are stopped by rules written before automation starts. Worst case: the foundation takes twice as long because project work keeps interrupting it. Even then, a half-built rulebook still helps: every recipe written can be run by hand.

### Part 8. Build once, run free: AI builds the tools, scripts do the work

The cheapest AI task is the one that never needs AI again. Formcraft uses AI mainly as a **toolmaker**. The first time a job is done, AI does it by the recipe. Once the same job has been done three times, AI writes a script that does it, with tests, and the script becomes an MCP tool. From then on the job runs as code at almost no cost, and AI is called only for the parts that need judgment. This is how the family factory already works: Formcraft did not ask AI to model 371 families one by one; it wrote an engine that builds them overnight from recipes.

&#91;embedded content: Top: the promotion ladder from AI to script. Bottom: model-independent continuity.\]

**The promotion rule (added to RB-00).**

1. **Three repeats, then a script.** The work journal counts how often a recipe runs with the same steps. At three, the recipe is flagged "script candidate".
2. **AI builds, a person checks.** AI writes the script and its edge tests; a named reviewer reads the test results, not every line of code.
3. **One library.** Every script gets a code (FMC-SCR-###), a version, an owner and its tests. It is stored in the Formcraft code repository and wrapped as an MCP tool. The recipe then points to the script instead of describing the steps.
4. **AI on exceptions only.** When the script meets a case it cannot handle, it stops and hands that case to AI with the context. If the same exception happens three times, the script is extended.
5. **Script first.** For any task, the order is: existing script, then recipe run by AI, then a person.

**What gets scripted, and what stays with AI.**

- **Script it:** document numbering and issue, EFRIS invoices, bank and mobile money matching, cut lists and nesting, schedules and sheet sets from the model, quantity take-off, quote assembly from the rate list, report building, video cutting and captioning presets, posting to platforms, reminders and follow-ups, dashboard refresh.
- **AI with a script around it:** reading a client brief, answering a new WhatsApp question, suggesting design options, drafting a variation letter, root-cause analysis of an error.
- **People only:** the never-alone list does not change.

**Why this is cheaper and safer.** A script costs AI money once, when it is built. Then it repeats exactly: it cannot misread an instruction it read correctly yesterday. In the rulebook simulation, adding the promotion rule to the staged rulebook setting cut serious errors from about 1.5 to 1.3 per decade and critical-error risk from 11.5% to 9.6%. It also lifted the chance of USD 1B lifetime revenue from 14.0% to 15.5% (and USD 100M from 36.0% to 36.7%), with survival unchanged at 56%.

**Honest limits.**

- **Building costs first, saves later.** The simulation charges the extra AI spend of building scripts in 2027–2028, and the chance of a loss-making year before 2031 rises from 31% to 46%. Mitigation: script only what has repeated three times, and build in order of hours saved.
- **A wrong script repeats its error a thousand times.** That is why every script has edge tests and stays in the weekly audit sample.
- **Scripts need upkeep.** Revit versions, APIs and EFRIS formats change. Every script has an owner and is re-tested at each kit release.
- **Not everything repeats.** Design judgment, client conversations and site problems will always need AI or people.

**Metrics added to the register.** Share of task volume run by scripts (target 50% by end 2027, 75% by end 2028); AI cost per output; scripts built per quarter; script failures and exceptions per script; hours saved per script.

### Part 9. Any AI can continue the work

Formcraft relies on AI and automation, so it must never depend on one AI model or one AI company. The rule: **the know-how of the business lives in the Formcraft app, not inside any AI.** Any model that is plugged in, whether Claude, a backup model or a future one, reads the same rulebook, uses the same tools and continues from exactly where the last one stopped.

**How continuity is built in.**

- **Shared memory in files.** Rulebook kits, recipes, the script library, shared codes and project data all live in the Formcraft app as plain, versioned files, readable by any model and any person.
- **The work journal.** Every task writes one entry: who or what ran it, the recipe and kit, inputs, steps done, outputs, status and **the next step**. No task is left without a next step.
- **Handover notes.** Every open job has a short note (current state, decisions made, open questions, files touched), updated at the end of every AI session, in a fixed template (FMC-ADM-HND).
- **Start and end protocol.** Every AI session starts by reading RB-00, the recipe, the job's journal and its handover note. It ends by writing the journal entry and updating the note. This is written into RB-12 and enforced by the MCP server: a task cannot close without them.
- **Tools, not memory.** Because AI acts only through MCP tools, a new model gets the same abilities and the same limits the moment it connects.
- **Model-neutral recipes.** Recipes are written in plain language, with no tricks that only work on one vendor's model.
- **The swap drill.** Every quarter, each new kit's edge tests are run on the backup model as well as the main one. The backup must pass at least 95% of what the main model passes, or the recipe is rewritten until it does.
- **People can continue too.** The same journal and handover note let a new staff member pick up a job, which also answers the risk of depending on Emlyn.

**Metrics added to the register.** Swap-drill pass rate; share of open jobs with a current handover note (target 100%); time for a new model or person to resume a job; tasks closed without a journal entry (target zero).

**Changes to the 12-week foundation build.** Week 4 adds the journal and handover templates to RB-02. Week 8 builds the start and end protocol into the MCP server. Week 12's gate adds a swap drill on the five kit 1 recipes and a list of the first script candidates from the journal.

## The content engine and sales funnel

In value chain terms, this is the marketing and sales activity. The idea: Formcraft is already doing interesting work every day (designs, models, a workshop, building sites). The engine films that work once and turns it into a week of content, so content costs minutes, not days.

&#91;embedded content: Marketing and sales in the value chain, automated end to end\]

**The weekly rhythm.**

- **Monday:** AI reviews last week's numbers and proposes 3 topics; Emlyn picks them.
- **Every working day:** site, workshop and Revit screen recordings are captured as part of the job, not as extra work.
- **Tuesday and Thursday:** one long YouTube video each (a project walkthrough, a design explained, a cost breakdown, a Revit tutorial).
- **Daily:** 1–2 Shorts or Reels cut by AI from the long videos, posted to every platform with captions in English and Luganda.
- **Friday:** a newsletter and a blog post written by AI from the week's videos, reviewed by a person.
- **Always on:** the AI assistant answers within minutes, day and night, and hands warm leads to a person.

**Funnel targets for the first year (to be measured, not promised).**

- **Reach:** 2,000 YouTube subscribers and 5,000 followers across platforms by end of 2027 (from about 65 today).
- **Leads:** 20 qualified leads a month by the Q2 2027 gate; 50 a month by end of 2027.
- **Conversion:** 30% of qualified leads get a site visit; 30% of quotes are won.
- **Speed:** first reply under 5 minutes; quote within 48 hours.

**Honest view.** Best case: one video catches on (a low-cost house design, a cost breakdown) and leads exceed what the team can serve; then the bottleneck becomes delivery, not marketing. Worst case: views stay low for 12–18 months, which is normal for new channels. The engine still pays because the same footage serves as the portfolio, the sales deck and the training library.

## Rollout plan

The order follows the value chain. Technology and rules (support activities) come first, because every other automation depends on them. Next comes marketing and sales, because it brings the cash and projects needed to test the rest. Operations, finance and site follow.

&#91;embedded content: Phases follow the value chain: support first, then sales, then operations\]

**Why this order.**

- **Rules before speed.** The Business Rulebook, the shared codes and rulebook kit 1 come first, so every later automation is built from a tested recipe.
- **Demand before efficiency.** Automating design for projects that do not exist yet wastes time; the funnel goes live before the design engine.
- **One spine.** From Q3 2027, the BIM model feeds quotes, purchase orders, cut lists, site progress and invoices. That is the linkage Porter describes, and it is the hardest part for a competitor to copy.
- **Package last.** Only recipes proven at Formcraft go into the playbook and are sold as Formcraft Tools.

## The outcome: the rulebook simulation

The Formcraft simulation was rebuilt to test this rulebook way of working, not just "AI or no AI". Each of 1 million futures per setting now tracks four things the earlier run did not:

- **Rollout gates.** Six phases, each passing its gate with a set chance per year. Value-chain coverage rises from 0% to 85% as phases pass.
- **Errors.** Serious errors happen at a rate that grows with workload. Ad hoc AI raises the rate (more output, no checks). Recipes, tests and named approval cut it as coverage rises, and keep cutting it as each kit learns from past errors. 8% of serious errors are critical: a structural problem, a legal claim or a tax penalty.
- **Tool stack cost.** Licences per seat plus AI and server costs, set against each year's revenue.
- **Margin and cash.** A year with negative margin, or a critical error, raises the chance of closing that year.

The base survival rates were recalibrated so that "no AI" matches the earlier model: about 42% of futures still running in 2036.

&#91;embedded content: Rulebook simulation, 1 million runs per setting; engine saved to the project as formcraft\_rulebook\_sim.py\]

**The six settings.**

1. **No AI:** manual work, no content strategy, Uganda only.
2. **Ad hoc AI:** AI chat used freely, with content and global reach, but no recipes, no MCP tools, no tests.
3. **Rulebook, tools staged:** recipes, MCP tools and tests; each phase passes its gate with a 75% chance a year; licences bought as phases need them.
4. **Rulebook, full stack day one:** the same, but every licence is bought in 2027.
5. **Rulebook, slow rollout:** gates pass with only a 40% chance a year, for example because Emlyn's time is split across five ventures.
6. **Rulebook, best practice:** gates pass with a 90% chance a year, and execution is stronger than average.

**What the results show.**

- **The rulebook is the difference, not AI alone.** Ad hoc AI does slightly worse than no AI: 37% still running in 2036 against 41%. It averages 7 serious errors in ten years against 5, and the chance of a critical error rises from 33% to 42%. With the rulebook, serious errors fall to about 1.5 per decade and critical-error risk to about 11%.
- **Staged rulebook (the plan):** 56% still running in 2036. Survivors earn USD 3.9M a year in the middle case (worst 10%: USD 1.6M; best 10%: USD 8.7M). Net margin is about 16%, against 5% with no AI. Chance of USD 100M lifetime revenue: 36%; of USD 1B: 14%.
- **Buying the full stack on day one hurts.** Tools take 11% of revenue in 2028, against 4% when staged. A loss-making year before 2031 becomes almost certain (99%, against 31%). Survival falls by about 5 points.
- **Speed matters less than discipline.** A slow rollout reaches 75% coverage around 2032 instead of 2029, but costs only about 1.5 points of survival and 2 points of the USD 100M chance. Rushing a recipe through its gate is worse than waiting.
- **Best practice:** 61% still running in 2036, 40% chance of USD 100M and 16.5% of USD 1B.

**Honest reading.** This model is stricter than the earlier chart because it charges for errors and tool costs directly. That is why "no AI" now reaches USD 100M in only 3% of futures (10.5% in the earlier run), while the staged rulebook lands close to the earlier "full" setting (36% against 30%). Even in the best setting, about 4 futures in 10 see Formcraft close or sold by 2036. Most of the gain comes from avoiding the mistakes that kill small firms, not from AI working faster. The error rates, cost per seat and margin effects are assumptions, set out in the engine file. Replace them with Formcraft's own logged numbers once the rulebook audits start.

**Estimated time saved per task (estimates to check against real logs, not measured yet).**

- Turning a site visit into a written brief: from about 3 hours to 30 minutes.
- A package quote: from 1–2 days to under 2 hours.
- A sheet set and schedules from the model: about half the hours.
- A cut list and CNC files for a furniture order: from half a day to under an hour.
- A daily site diary: from 45 minutes to 10 minutes.
- Month-end invoicing and reconciliation: from 2 days to half a day.
- One long video edited into a week of posts: from 2 days to about 2 hours.

## The Formcraft simulation lab: every run, every chart

This section collects every simulation run for Formcraft. Run 6 is the latest, run on 29 October 2026, and it includes everything decided on this page: the rulebook, staged tools, scripts built by AI, model-independent continuity, disruptions (a key person out, an AI vendor outage or price rise), errors, tool costs and rollout gates. It used **29 million simulated futures**: 8 settings, 17 sensitivity runs and 4 stress tests, each of 1 million futures. The engine is saved in the project as `formcraft_sim_suite.py`.

**The simulation log.**

1. **Run 1, first Monte Carlo (all ventures):** 10,000 futures per scenario, 4 scenarios. Superseded.
2. **Run 2, five simulation types (all ventures):** deterministic plan, Monte Carlo, levers, survival and conditional runs, 6,000–10,000 futures each. Superseded.
3. **Run 3, vectorised engine (all ventures):** 1 million futures per scenario, 6 scenarios, run twice (about 12 million). Superseded.
4. **Run 4, AI, YouTube and global reach (all ventures, then Formcraft alone):** 18 group scenarios of 1 million futures each (Formcraft as part of the group: 54.5% running in 2036, 30% reach USD 100M, 12.4% reach USD 1B), plus Formcraft alone in 5 settings of 400,000 futures each. Its chart is below for reference.
5. **Run 5, rulebook model (Formcraft alone):** 6 settings of 1 million futures, run three times while the model was calibrated and corrected, plus a 2-million-future test of scripts (about 21 million). Its chart is in the outcome section above.
6. **Run 6, the full Pioneer suite (Formcraft alone):** 29 million futures. The charts below.

In total, about 83 million simulated futures have been run, about 52 million of them for Formcraft alone.

**How run 6 works, in short.** Each future starts in 2027 with the planned revenue ramp, shifted by luck (some starts are bigger, some smaller). Each year the model draws: whether a rollout gate passes, how many serious errors happen and whether any is critical, whether a disruption or market shock hits, whether growth stalls, what tools cost against revenue, and whether the firm survives the year. Base failure rates come from US business survival statistics and were calibrated so that "No AI" keeps about 42% of futures running in 2036, the same as earlier runs.

### Chart 1. The eight settings

&#91;embedded content: Run 6, 8 settings x 1 million futures\]

- **Pioneer plan (rulebook, staged tools, scripts, continuity):** 58% still running in 2036; 38.5% reach USD 100M lifetime revenue; 16.5% reach USD 1B. Serious errors average 1.3 per decade; critical-error risk is 9.7%.
- **Best practice** adds faster gates and stronger execution: 62%, 43.0% and 19.2%.
- **No AI:** 42%, 3.1% and almost zero. **Ad hoc AI:** 37%, 2.4% and almost zero, because errors rise faster than revenue.
- **Each part of the plan adds a little:** the rulebook does most of the work (3.1% → 36.1%); scripts add 0.9 points; continuity adds 1.5 more.

### Chart 2. Survival year by year

&#91;embedded content: Run 6, tracked year by year from 2027 to 2040\]

The plan pays off slowly. In 2027 the Pioneer plan is slightly *behind* No AI (89% against 91% still running) because building the rulebook, scripts and tools costs money before it saves any. The lines cross in 2029. By 2040, half of Pioneer futures are still running, against 28% with no AI.

### Chart 3. Revenue range over time

&#91;embedded content: Revenue among firms still running that year; closed firms are not in the band\]

Among firms still running, the Pioneer plan's middle case reaches USD 1.1M a year in 2031, USD 3.9M in 2036 and USD 9.2M in 2040. Even its worst 10% (USD 2.3M in 2040) matches the No AI middle case. The best 10% reach USD 28M a year by 2040.

### Chart 4. Where the futures end up

&#91;embedded content: Run 6 lifetime revenue bands\]

About a quarter of futures stay under USD 1M lifetime revenue in every setting. These are the futures that close early, and no plan removes them. The plan's effect is on the rest: with no AI, almost every surviving future tops out between USD 1M and USD 100M. With the Pioneer plan, 39% go above USD 100M.

### Chart 5. Which assumptions matter most

&#91;embedded content: Run 6 sensitivity: 17 extra runs of 1 million futures\]

- **The biggest driver is staying alive**, not AI: if the basic yearly failure risk is 30% higher than assumed, the chance of USD 100M falls to 31%; if 30% lower, it rises to 47%. That risk is mostly cash, clients, health and focus.
- **Growth comes second** (33% to 42%): the funnel and content engine matter.
- **Error rate comes third** (35% to 42%): the rulebook's main job.
- **The tool choices matter less one at a time** (1 to 3 points each), but together they are the whole gap between No AI and the plan.

### Chart 6. Stress test

&#91;embedded content: Run 6 stress test: 4 extra runs of 1 million futures\]

Market shocks (a year in which revenue drops by a quarter and growth by 25 points, as in a construction slowdown or a currency crisis) hurt both settings. With severe shocks, the Pioneer plan's chance of USD 100M falls from 38.5% to 26.5%, and No AI's from 3.1% to 1.5%. The plan still keeps a large lead.

### The deterministic plan

If every year goes exactly to plan (the ramp to USD 1.03M in 2031, then 30% growth a year for ten years, then 20%), Formcraft alone earns USD 14.3M in total by 2036, crosses USD 100M lifetime revenue in 2044 and USD 1B in 2056. Few simulated futures follow this exact path: the Pioneer plan's middle future earns about USD 31M in total by 2072. The plan is the target line, not the expected result.

### Run 4, for reference

&#91;embedded content: Run 4 (superseded): Formcraft alone, 5 settings x 400,000 futures, before errors, tool costs and gates were modelled\]

**Honest reading of runs 1 to 6.** Every run since run 3 tells the same story with different precision. AI used freely does little. AI under written rules roughly multiplies the chance of a USD 100M Formcraft by ten or more. The biggest remaining risk is the ordinary one of a small firm failing.

## Run 7: an objective review of the whole Pioneer page

Run 7 reads the full page (the rulebook, the tool stack, the Revit system, the client portal, scripts and continuity) and asks what the earlier runs left out. Five things were missing, so run 7 adds them: **team capacity and hiring** (work can be turned away), **key-person risk** (Emlyn), **founder focus** (five ventures), **the developer who speeds up the build queue**, and **the client portal**. It also adds a second kind of simulation: a **month-by-month cash and capacity model** of the first 36 months. Run 7 used 11.8 million futures (10 annual runs of 1 million, 4 monthly runs of 200,000), bringing the total for this page to about 95 million.

### First, the objective review

**What is strong.** The method is right and already proven in Revit: rules before automation, one door for AI, recipes, tests, named approval. The data spine (shared parameters, keynotes, FMC numbering) is rare for a firm of this size. The portal turns that data into trust, which is what Kampala and diaspora clients lack most. The plan is honest about limits.

**What is weak or risky.**

- **Too much for one builder.** The build queue shows 7 of 120 tasks done, the server rebuild, the rulebook, the portal, the content engine and five ventures all depend on Emlyn. Run 7 cuts the rollout speed by 20% unless a developer is hired.
- **The revenue plan is steep.** It rises from about USD 46,000 in 2027 to USD 1.03M in 2031, more than 20 times in four years. The monthly simulation's middle case reaches USD 240,000 in 2029, about 26% behind the plan's USD 324,000.
- **Cash is thin.** With about USD 3,000 in hand and no buffer, cash goes below zero in at least one month in more than half of the simulated futures.
- **Capacity limits growth.** At about USD 30,000 of revenue per person, the plan's 2031 revenue needs 20 to 25 people. Hiring trained BIM staff in Kampala is slow, and work turned away hurts reputation.
- **Legal sign-off.** Building plans need registered professionals, so Formcraft needs registered architects and engineers in the team or on retainer from the start.

### Run 7 results

&#91;embedded content\]

- **The hiring plan beats building alone, but only modestly:** 59.6% against 58.3% still running in 2036; 41.7% against 39.1% for USD 100M; 19.7% against 17.8% for USD 1B. Its main gain is lower key-person risk: the chance of an Emlyn shock by 2036 falls from 36% to 29%.
- **Hiring too early hurts.** In a first version of run 7, the developer and deputy were paid from 2027, and the hiring plan did *worse* than building alone because salaries ran ahead of revenue. Hiring when revenue passes USD 100,000 and USD 250,000 turned that around. Hire on triggers, not on dates.
- **The client portal adds about 2.4 points** to the chance of USD 100M and lifts 2036 revenue by about 12%, through trust, conversion and fewer critical disputes.
- **Splitting Emlyn across five ventures** costs about 3 points of survival and 3 points of the USD 100M chance, and raises key-person risk to 40%.
- **Best practice** (fast gates, strong execution, the hiring plan): 64% still running in 2036, 46% chance of USD 100M, 23% of USD 1B.

### Key-person risk and hiring success

&#91;embedded content\]

- **If Emlyn is out for a full year in 2028,** survival to 2036 falls by about 6 points in every setting. The deputy cannot help yet, because the trigger for hiring one (USD 250,000 revenue) is rarely reached by 2028. What protects Formcraft early is the work journal, handover notes and recipes that let others continue (Part 9).
- **Hiring success matters more than any single AI lever.** If only half of planned hires work out, the chance of USD 100M falls to 38% and about USD 2.1M of work is turned away by 2036. At 90% success, it rises to 43%. The Academy is the hiring pipeline: train people in Formcraft Tools before they are needed.

### The first 36 months, month by month

&#91;embedded content\]

The monthly model draws leads from the content funnel, wins at about 10% (12.5% once the portal is live), project fees, delivery capacity per person, late payments (35% paid two months late, 8% never paid), salaries, tools and hires. The results:

- **Revenue (middle case):** solo, USD 41,000 in 2027, USD 96,000 in 2028 and USD 170,000 in 2029. With the hiring plan and portal: USD 45,000, USD 131,000 and USD 240,000. That is close to the plan in 2027 and 2028 and behind it in 2029.
- **Cash below zero in at least one month:** solo 58%; hiring a developer from month 3, 69%; from month 12, 57%; from month 12 with a USD 15,000 buffer (about UGX 55M), only 1%.
- **The single most useful money decision** in the first year is a working-capital buffer of about USD 15,000, from savings, a small investor, a grant or prepaid Tools licences, before adding salaries.
- **First hire:** around month 11–16. Team at the end of 2029: about 5 people solo, about 8 with the plan.

### The system behind the numbers: feedback loops

&#91;embedded content\]

This causal loop view is the third kind of simulation used on this page (after Monte Carlo and the monthly model). It shows why the numbers move. Two loops make Formcraft grow: content leads to projects, which give footage for more content (R1), and good work brings referrals (R2). Two loops slow it: overload causes errors that damage reputation (B1), and hiring costs drain cash (B2). Every system on this page exists to strengthen R1 and R2 or to weaken B1 and B2.

**The improvement loops written into the rulebook (RB-13).**

1. **Quality loop:** weekly audit → corrective action → recipe change → new test → next kit.
2. **Estimate loop:** final cost compared with every earlier estimate → rate library and ranges updated each quarter.
3. **Content loop:** views, watch time and leads per video → next week's topics (Monday review).
4. **Pricing loop:** win rate above 50% for a quarter → raise prices; below 20% → review offer and price.
5. **Capacity loop:** utilisation above 85% for two months → start hiring; below 60% → pause hiring and push sales.
6. **Cash loop:** runway under 3 months → freeze hires and tool spend; over 6 months → release the next hire or system.
7. **Key-person loop:** share of recipes run by someone other than Emlyn, and the quarterly swap drill → recipes rewritten until others can run them.
8. **Client loop:** client score and referrals at close → service and portal changes.
9. **Script loop:** tasks repeated three times → script candidates → built, tested and released.

### Business metrics: which system captures them automatically

The goal is that by the end of 2027 at least 80% of the metrics in the register (Part 5) are captured without anyone typing them in.

- **Website, CRM and WhatsApp assistant (S05):** visitors, sign-ups, leads by source and segment, first reply time, qualified leads, site visits, cost per lead.
- **Content engine (S04):** videos published, views, watch time, click-through rate, subscribers, leads per video, YouTube income.
- **Client portal (S07, S10):** accounts opened, logins, stage sign-offs and how long they take, questions answered, change orders, client score.
- **MCP server and rulebook app (S01, S02):** tasks per recipe, approvals and approval time, audit errors, tests passing, AI cost per output, fallbacks used, scripts built and script share of work, journal and handover completeness.
- **Cost engine (S08):** estimate per stage, final cost against estimate, margin per project, supplier price changes.
- **Finance automation (S09):** revenue, gross margin, overhead, cash and runway, receivable days, EFRIS errors, tool spend.
- **Bench app (S11):** hours by person and project, site diary completion, inspections, incidents and near misses, workshop waste, delivery on time.
- **Schedule engine (S12):** milestones on time, schedule slip, 4D progress against plan.
- **People records:** utilisation, hires, time to competence, turnover, training hours.

### Who to hire, and which professionals to add

&#91;embedded content\]

- **From the start, by law and by risk:** registered architect and registered engineers (structural, MEP) on retainer to sign plans, because the Building Control Regulations 2020 make professional engagement mandatory; a part-time accountant for EFRIS, VAT, PAYE and NSSF; and an HSE officer on every site.
- **Key-person hires:** a software developer (C# for Revit, React for the website and portal) when revenue passes about USD 100,000 a year, and a deputy or BIM manager who can run Studio when it passes about USD 250,000.
- **Capacity hires:** BIM modellers from the Academy, a quantity surveyor to own the cost engine, a project manager for sites, and a client success lead for the portal and referrals.
- **Later:** in-house engineers, a workshop manager, a data engineer and a finance manager.
- **The rule:** hire when utilisation stays above 85% for two months and cash covers three months of the new salary. Each new role gets its recipes and handover notes from day one.

### Which systems to build, in order

&#91;embedded content\]

1. **S01 MCP server rebuild and S02 rulebook app** (with work journal and handover notes): the foundation for everything else.
2. **S03 data dictionary and dashboard v1:** so every metric is defined before it is collected.
3. **S04 content engine and S05 website funnel, CRM and WhatsApp assistant:** demand comes before efficiency.
4. **S06 script library and promotion pipeline:** runs continuously from Q1 2027.
5. **S07 client portal v1:** account, brief, documents, sign-offs, payments and the 3D viewer.
6. **S08 cost engine (5D) and S09 finance automation (EFRIS):** money first, then speed.
7. **S10 portal v2 (federation)** and **S11 Bench app v1:** site and workshop data flow in.
8. **S12 schedule engine (4D) and portal v3:** live construction tracking.

## Marketing, YouTube and target markets

### Who Formcraft sells to

**Services (Studio, Construction, Concrete, Stores).**

- **Kampala homeowners building a first house,** often on standard 50 x 100 ft plots: template homes and Studio packages, plot to permit in 9–14 weeks, fees priced in the open (10%, 15% or 25% of the construction budget, paid 30/40/30).
- **Ugandans abroad building at home:** the strongest fit for the client portal, because their main problem is trust at a distance. Card payments and time-zone-friendly updates matter.
- **Developers and real estate firms:** BIM design, renders from the Blender service, tender packs and bid management.
- **Businesses, factories and clinics:** commercial and industrial design (the Karwani coffee factory) and healthcare (the Lubowa hospital pack).
- **Schools, NGOs and public bodies:** through PPDA tenders once the track record is built.
- **Furniture and joinery buyers:** homes, offices and hotels through Stores.

**Software and services for the industry (Formcraft Tools, families, cloud, Academy).**

- **Architecture and engineering firms in East Africa that use Revit:** BIM system setup, Formcraft Tools licences, custom families and model hosting.
- **Students and graduates:** Academy courses on cloud workstations, the future hiring pipeline and future Tools users.
- **Product manufacturers and suppliers:** the family matching service (their products modelled as Formcraft families, starting with medical equipment).
- **Partner contractors:** bid sessions and the Bench app.
- **Revit users worldwide:** the family store and tutorials, once the East African base is proven.

### The YouTube and content strategy

&#91;embedded content\]

- **Two channels, not five, to start.** One Formcraft channel in English and Luganda for clients (pillars 1, 2, 4 and 5), and one Formcraft Tools channel in English for professionals (pillar 3). More channels split a small audience.
- **Rhythm:** two long videos a week and one or two Shorts a day, cut by the content engine from footage captured during normal work (see the content engine section).
- **Each video has one job:** one audience and one call to action. Examples: "get a free plot review", "open a portal account", "download the free family", "join the Academy".
- **Lead magnets:** a construction cost calculator, a free plot review, sample families from the healthcare pack, and a short Revit standards guide.
- **YouTube income is a bonus, not the plan.** As noted in the YouTube research earlier in this document, most channels earn little from ads; the value is in visibility, trust and leads. The Revit tutorials pillar is the one most likely to earn meaningful ad income, because its audience is global and professional.
- **Paid boost:** a small monthly budget (for example USD 100–300) only on the posts that already perform best, aimed at diaspora and Kampala audiences.
- **Positioning line:** "Plot to permit, priced in the open, with your project live in your browser."

**Marketing metrics (all automatic through S04 and S05):** leads by segment and source; cost per lead and per client by segment; conversion at each funnel step; revenue and lifetime value by segment; for YouTube, views, watch time, click-through rate, subscribers and leads per video.

**Honest view.** The services market in Kampala is crowded and price-driven, and most clients still choose by word of mouth. Content and the portal take 12–18 months to change that. The software market is smaller but has higher margins and goes beyond Uganda. Run 7 assumes the portal and content lift conversion modestly (from 10% to 12.5%); if they do better, the monthly model's 2029 revenue moves toward the plan.

## A MrBeast-level content strategy, made by AI under the rulebook

The goal is not MrBeast's budget or his view counts. It is his **discipline**, applied to construction and design, with AI producing most of the work under Formcraft's recipe and rulebook method. The ambition: the most-watched construction and design channel in East Africa within three years, and the one that brings in the most clients.

### What we take from MrBeast

His production guide (leaked in 2024 and widely published) is blunt. The goal is to make the best *YouTube* videos possible, not the best-looking or highest-quality ones. He names three numbers to care about: click-through rate (CTR), average view duration (AVD) and average view percentage (AVP).

- **Package first.** The title and thumbnail are decided before filming. They set the viewer's expectations, and the video must meet them.
- **The first minute is everything.** It must show at once that the thumbnail's promise is real. Then comes the move from "hype" to "action": stop telling people what they will see and start showing it.
- **Re-engage** at about minute 3 and minute 6 with a twist, a new rule or a bigger reveal, so viewers do not drift away.
- **Repeatable formats** that viewers learn to love, built up step by step.
- **A "wow factor":** something no one else on YouTube can do.
- **A-players:** a small team of obsessive, coachable people, judged on results, not hours.

**Formcraft's wow factor** is something no other channel in the region has: real BIM models, real costs from a bill of quantities, a workshop, live building sites, an AI agent working inside Revit, and a client portal that shows a diaspora client their house being built. Formcraft can show, with true numbers, what other channels can only talk about.

### The retention map

&#91;embedded content\]

Every long video follows this map. Recipe MKT-02 makes AI write the script against these beats, and the editor checks the retention graph in YouTube Studio after publishing to see exactly where viewers left.

### Nine repeatable series

&#91;embedded content\]

- **Same Plot, 3 Budgets** (launch first): the same 50 x 100 ft plot designed at UGX 50M, 150M and 500M, with every cost from the model. This series sells template homes and Studio packages.
- **Every Shilling:** a real client build (with consent) and a live cost counter on screen from foundation to keys. It sells construction and the portal.
- **Plot to Permit Race:** a countdown from first visit to approved permit in 9–14 weeks. It sells Studio packages.
- **AI vs Architect:** Formcraft Tools and the Revit agent racing a skilled human on a real task, with honest results either way. It sells Tools and the Academy.
- **Built From Abroad:** a client in London, Boston or Dubai watching their house rise through the portal. It sells the portal to the diaspora.
- **Rescue Build:** finishing one of Kampala's many abandoned shells, with an engineer's checks shown on camera. It sells construction and concrete.
- **One Log to a Living Room:** a Shorts series from the workshop. It sells Stores furniture.
- **Revit Speedruns:** families, sheets and bills of quantities in minutes with Formcraft Tools, for a global professional audience. It sells Tools and the family store.
- **We Built It For Free:** once or twice a year, a classroom or clinic built for a community and sponsored by suppliers (cement, steel, paint, roofing). This is Formcraft's version of MrBeast's generosity, and it builds trust and partnerships.

### How AI makes it: the content recipes

&#91;embedded content\]

Every step is a recipe in the rulebook (chapter RB-08, codes FMC-RCP-MKT-01 to 06), run by AI through MCP tools, with the same rules as every other recipe: written steps, edge tests, a named approver, logs and a fallback.

1. **MKT-01 Idea and package.** Each week AI proposes 25 ideas from comments, search trends, site and workshop events and past performance, and writes 3 titles and a thumbnail brief for each. Emlyn picks.
2. **MKT-02 Script.** AI writes the script against the retention map, pulling every number from the model, the bill of quantities and the rate library, never from memory.
3. **MKT-03 Visuals.** Renders and fly-throughs come straight from the Revit model through the Blender pipeline; AI animates cost counters, plans and before-and-after sequences; site and workshop footage comes from the Bench app and phones.
4. **MKT-04 Edit and voice.** AI cuts to the script, removes dead time, adds captions, and dubs into English, Luganda and Swahili. A real person's voice is cloned only with their written consent.
5. **MKT-05 Thumbnails.** AI produces three thumbnail variants for each video, tested with YouTube's thumbnail test feature where available.
6. **MKT-06 Publish and clip.** AI publishes on schedule, cuts 5–10 Shorts, Reels and TikToks from each long video, writes descriptions and pinned comments with one call to action, and logs everything with the recipe code.

**The rules that keep it honest (added to RB-08).**

- **True numbers only.** Every cost, time and quantity on screen comes from the model or the books, and the facts check (L2) traces each one back.
- **The thumbnail must be delivered.** No promise in a title or thumbnail that the video does not keep. MrBeast's own rule, and the rule that protects Formcraft's reputation.
- **Label AI scenes.** Realistic AI-generated or altered scenes (a render shown as if built, a cloned voice) are disclosed, as YouTube's rules require for realistic synthetic content, and marked on screen.
- **Consent first (L0).** No client, worker, child or home appears without written consent; budgets are shown only with the client's agreement.
- **Safety on camera.** Every site shot follows the HSE rules: PPE on, no unsafe stunts.
- **Giveaways done properly.** Sponsored builds and competitions follow Uganda's promotion rules and are run through a written agreement with each sponsor.

### The production system

&#91;embedded content\]

- **Cadence:** one hero video a month (the wow moment); two series episodes a week; one or two Shorts a day; one live stream a month (a design review or Q&A).
- **The team (A-players):** Emlyn as on-camera lead and final approver; a content producer from the Academy who runs the recipes; an editor-thumbnail designer; a second presenter for Luganda content. AI does the rest.
- **Budget:** about USD 300–1,000 a month for the hero video and paid boosts, funded mostly by supplier sponsors once views are proven. Sponsors get product placement in real builds, never false claims.
- **Two channels:** Formcraft for clients (most series) and Formcraft Tools for professionals (AI vs Architect, Revit Speedruns).

### The numbers that matter

- **Per video:** CTR, AVD, AVP and the retention graph, compared with the channel's own average; every video should beat the last ten on at least one of them.
- **Formcraft's fourth number:** leads per 1,000 views, by series. A series that wins views but no leads is changed or dropped.
- **Monthly:** subscribers, watch hours, returning viewers, Shorts-to-long-video conversion, sponsor revenue, and cost per lead from content against cost per lead from paid ads.
- **The loop:** analytics from MKT-06 feed MKT-01 every Monday. A format that works is repeated and pushed further; one that fails is fixed once and then retired.

### Honest view

MrBeast-level views are not a realistic target: his channel has hundreds of millions of subscribers, a large team and very large budgets. What is realistic is his method: package first, a gripping first minute, re-engagement, repeatable formats and ruthless review of the numbers. AI makes that affordable for a small firm, because the costly parts (scripting, renders, editing, captions, translation, thumbnails and clipping) become recipes. The risk is sameness. AI content can look like everyone else's. Formcraft's protection is that its videos are built on its own true data, real sites and real people, which no one else can copy.

## The legal plan

This plan lists what Formcraft needs legally, in the order to put it in place. It is a planning checklist, not legal advice: every structure and contract here should be drafted or reviewed by a Ugandan advocate, and every tax point confirmed with a Ugandan accountant.

### Company structure

&#91;embedded content\]

- **Now:** one private limited company under the Companies Act 2012, registered with URSB, with a written shareholders' agreement between the co-founders.
- **Assign the IP first.** Formcraft Tools, the rulebook, the scripts, the families and the template library were largely written by Emlyn. Until a signed IP assignment (or exclusive licence) moves them into the company, the company does not own its most valuable asset, and no investor or buyer will value it. This is the single most urgent legal task.
- **Later, when investors, large contracts or a second venture arrive:** a holding company that owns (1) an operating company that signs client and contractor contracts and carries site and design liability, and (2) a technology company that owns the IP and licenses it to the group and to the market. A building claim then cannot reach the software, and the software can be sold or funded separately. Soko Foods, Logistics, Nyumba and the Trade Assistant each become their own company under the same holding company.

**The shareholders' agreement must cover:** each founder's role and time commitment (especially with five ventures); vesting of founder shares over about four years with a one-year cliff; what happens if a founder leaves, falls ill or dies (key-person clauses, buy-back, insurance); decision rights and deadlock; IP assignment; non-compete and non-solicit; an option pool for key hires such as the developer and deputy; and how new investors come in.

### Registrations and licences

- **URSB:** company registration, business names for the four divisions, annual returns.
- **URA:** tax registration (TIN), EFRIS for invoices, PAYE, withholding tax, and VAT once over the threshold. The threshold rose in 2026 from UGX 150M; sources differ on whether the new figure is UGX 250M or UGX 300M, so confirm it with URA or the accountant. Consider registering voluntarily: corporate and public clients often want VAT invoices, and registration lets Formcraft recover VAT on materials.
- **NSSF:** employer registration; 10% employer and 5% employee contributions.
- **KCCA:** trading licence; building permits per project under the Building Control Act 2013 and Regulations 2020.
- **PDPO:** registration as a data collector and controller under the Data Protection and Privacy Act 2019, before the portal and WhatsApp assistant go live.
- **Professional registration:** registered architects and engineers who sign plans (in the team or on retainer), and a company profile with the professional bodies.
- **PPDA:** provider registration on the government e-procurement system before bidding for public work.
- **Trademarks:** register "Formcraft" and the division marks with URSB under the Trademarks Act 2010, then in Kenya, Rwanda and other markets before entering them.

### The contract library

&#91;embedded content\]

Every contract is a template in the FMC numbering system (proposed family code FMC-LEG), with a version, an owner and a yearly review, and is issued through the same recipe method as every other document.

**With clients.**

- **Design appointment (Studio):** scope by RIBA stage, fee as a share of the construction budget, payment 30/40/30, stage sign-offs, what is excluded, a licence to use the drawings for one site only (Formcraft keeps copyright), a cap on liability (for example the fee or the insurance cover), and how changes are priced.
- **Design-and-build and construction management:** based on FIDIC (Short Form for small jobs; Red Book where the client's design is built; Yellow Book where Formcraft designs and builds), with milestone payments, retention, variations only by signed order, delay notices, defects period and dispute resolution.
- **Stores sales terms:** quotation validity, deposit, delivery, warranty and returns.
- **Concrete supply terms:** mix grade, delivery tickets, testing, and acceptance on site.
- **Template home licence:** the right to build one house from a template design, with no resale of the drawings.
- **Portal and website terms:** account rules, privacy policy, consent to electronic sign-off under the Electronic Transactions Act 2011, the statement that an on-screen estimate is a range and not a quote, and consent before any project appears in content.
- **AI disclosure:** a plain statement in every appointment that Formcraft uses AI tools under its rulebook, that registered professionals review and sign all design, and that client data is not used outside the project without consent.

**With partner contractors.** Bid session rules; a subcontract on FIDIC lines with scope from the priced model, retention (commonly 5–10%), performance security, insurance and HSE obligations, the right to inspect, and back-to-back terms with the client contract.

**With professionals.** A retainer for registered architects and engineers: scope, fees per project, sign-off responsibility, their own professional indemnity cover, and response times.

**With staff, makers and freelancers.** Employment contracts under the Employment Act 2006 (role, pay, hours, leave, NSSF), with IP assignment, confidentiality and non-solicit; service agreements for makers and freelancers, with IP assignment for anything they create for Formcraft.

**For software and services sold to the market.** An end-user licence for Formcraft Tools; SaaS terms for the portal, hosting and cloud workstations (uptime, support, data ownership, exit); family store licence terms; a data processing agreement for firms whose data Formcraft hosts; and Academy course terms.

**With suppliers and manufacturers.** Supply terms, and for the family-matching service a mutual NDA plus clear rules on who owns the modelled families.

**Inside the group and with investors.** Intercompany service and IP licence agreements with the other ventures (so Formcraft is paid for the systems it builds for them); NDAs; MoUs with partners; and investor papers (term sheet, convertible note or SAFE, subscription and shareholders' agreements) when funding is raised.

### Intellectual property

- **Copyright** (Copyright and Neighbouring Rights Act 2006) protects the code, drawings, families, templates, videos and the rulebook automatically, but only if the company owns it: hence the assignments above.
- **Trade secrets:** the recipes, rate library and scripts stay private, behind confidentiality clauses and access controls.
- **Trademarks:** Formcraft and the division names, registered before expansion.
- **Third-party licences:** check that Autodesk's terms allow a commercial Revit add-in and its distribution; respect open-source licences in the stack (some, such as GPL, can force code to be shared); follow each AI provider's commercial terms.

### Insurance

- Professional indemnity (design errors), sized to the largest project.
- Contractor's all risks for each construction project, usually required by FIDIC contracts.
- Public liability, and employer's liability or workers' compensation under the Workers' Compensation Act.
- Property and equipment cover for the workshop, machines and computers.
- Product liability for Stores furniture and precast concrete.
- Cyber cover once the portal holds client data and payments.
- Key-person cover on Emlyn, as the simulations show the business depends on him.

### Disputes

Every contract names a ladder: negotiation, then mediation or adjudication (a dispute board under FIDIC for larger jobs), then arbitration under Uganda's Arbitration and Conciliation Act, for example through the Centre for Arbitration and Dispute Resolution (CADER) in Kampala. Courts are the last resort. The portal's record of sign-offs, change orders and site photos is Formcraft's best evidence.

### Compliance calendar

&#91;embedded content\]

The finance automation system (S09) tracks every date, prepares the filings for the accountant, and raises an alert seven days before each deadline. Late PAYE and NSSF carry interest and penalties, so these filings are the highest-priority scripts in RB-10.

### Legal risks to watch

- **Unassigned IP:** the company does not own Formcraft Tools until it is assigned. Fix in the first month.
- **Unsigned changes:** work done before a variation order is signed. The portal makes signing instant; the rulebook makes it compulsory.
- **Estimates read as quotes:** every estimate states its stage, range and assumptions.
- **Professional sign-off:** never issue plans for permit without a registered professional's signature.
- **Data protection:** register with PDPO and record client consent before launch.
- **Founder disputes:** a signed shareholders' agreement before any outside money or big contract.

## The financial plan

Again, this is a plan for discussion with Formcraft's accountant, not financial advice. The numbers come from the plan and the run 7 simulations.

### Revenue: plan against simulation

&#91;embedded content\]

The plan is a target line. The simulations' middle case tracks it in 2027 and 2028 and then falls behind: about 26% behind in 2029, and about 27% behind in 2031 among firms still running. The financial plan is therefore built on the simulated middle case, with the plan as the upside.

### How Formcraft earns

The pitch deck lists fourteen revenue streams; the plan groups them by when they start and how they are paid.

- **Earning today:** design and permit fees (10% residential, 15% commercial, 25% commercial with full BIM, as a share of the construction budget, paid 30/40/30); furniture, joinery and interiors.
- **From Q4 2026 to Q2 2027:** healthcare and custom families; BIM system setup for other firms; Formcraft Tools licences; the Blender render service; model hosting and the AI manager; cloud workstations; template plans; Bench premium.
- **From Q3 2027:** bid management and supervision fees; precast and green concrete with partners; Academy courses.
- **Billing:** clients are billed in USD, as the deck states, with mobile money and card payments through Flutterwave. Software and hosting are billed monthly or yearly in advance, which helps cash.

### The first-year budget (2027, middle case)

- **Revenue:** about USD 45,000.
- **Direct project costs** (consultants, materials, printing, transport): about 25% of revenue, about USD 11,000.
- **Overheads** (office, internet with Starlink backup, utilities, software and AI): about USD 11,000.
- **People:** founder stipends and the first hire, about USD 8,000–10,000.
- **Result:** a thin surplus in the middle case, but cash falls below zero in at least one month in more than half of futures, because clients pay late.
- **Working-capital buffer:** about USD 15,000 (about UGX 55M) before adding salaries. In the monthly model this cut the chance of a cash shortfall from 57% to 1%.

### Funding plan

In order of preference, cheapest and least dilutive first:

1. **Customer money:** deposits on every job, stage payments, and software and hosting paid in advance. Prepaid Tools licences and family packs can fund the developer hire.
2. **Grants and programmes:** innovation, digital and youth-enterprise programmes for the software and the Academy.
3. **Asset finance:** for workshop machines and computers, paid from the work they produce.
4. **An overdraft or invoice finance:** for timing gaps on large projects, once there is a track record.
5. **Angel or seed investment:** for the technology company, once IP is assigned, the shareholders' agreement is signed, and the first Tools customers are paying.

Every offer of money is judged by the cash loop: it must extend runway past six months or pay for a hire or system with a clear gate.

### Project finance and payment terms

- **No work without a deposit:** 30% on Studio appointments, and a mobilisation advance on construction, backed by an advance payment guarantee if the client asks for one.
- **Stage payments** tied to signed milestones in the portal.
- **Retention:** expect 5–10% held by clients; hold the same from partner contractors so cash stays matched.
- **Diaspora clients:** consider an escrow or milestone account for construction money, so funds are released only against signed progress. This builds the trust that is the portal's main selling point.
- **Price validity:** quotes valid 14–30 days, with a price adjustment clause for cement, steel and fuel on longer projects.

### Tax plan (confirm with the accountant)

- **Corporate income tax:** 30% of chargeable income, with provisional returns and instalments during the year.
- **VAT:** 18%; decide on voluntary registration (see above).
- **Withholding tax:** clients who are designated agents, and payers of professional fees, may withhold 6% from Formcraft's invoices. Track every certificate, because it is a credit against Formcraft's income tax. Payments to non-residents (for example some foreign software or services) can carry withholding tax of up to 15%; check each subscription.
- **Payroll:** PAYE (bands changed from July 2026), NSSF and Local Service Tax.
- **Group structure:** once there are several companies, intercompany charges must be at fair prices and documented.

### Financial controls (automated by S09)

- One bank and mobile money account per company, in UGX and USD; no personal accounts for business money.
- Every transaction carries a project code and a cost code from RB-02.
- Two people approve any payment above a set limit; nobody approves their own spending.
- Bank and mobile money reconciliation runs as a script every week; the month closes within five working days.
- Monthly pack: profit and loss, balance sheet, cash flow, 13-week cash forecast, margin per project, receivables by age.
- Yearly accounts prepared under IFRS for SMEs; an external audit once investors, banks or large tenders require it.

### Financial KPIs

- **Cash runway:** at least 3 months now, 6 months from 2028.
- **Gross margin per project:** 25% or more.
- **Final cost against estimate:** within 5%.
- **Receivable days:** under 45.
- **Revenue per person:** tracked against the USD 30,000 assumption in run 7.
- **Share of revenue from recurring software and hosting:** rising each year.
- **Largest client's share of revenue:** under 40%.

### Getting ready for investors

- A clean cap table and signed shareholders' agreement.
- IP assigned to the company, with a register of code, families and templates.
- Twelve months of monthly accounts from the finance system, and the KPI dashboard.
- A data room: company documents, contracts, licences, insurance, the rulebook and the simulation models.

### Financial risks

- **Cash gaps from late payment:** deposits, stage payments, the buffer and the 13-week forecast.
- **Under-pricing:** model quantities, two-source checks and the estimate loop.
- **Currency:** USD billing for clients; watch UGX costs against USD income.
- **Tool and AI costs rising:** buy at the gate, keep free fallbacks, scripts instead of repeated AI.
- **Over-hiring:** hire on revenue triggers, not dates.

## Run 8: everything on the page, read critically

Run 8 takes run 7 and adds what the legal and financial plans change:

- **The USD 15,000 cash buffer.**
- **Deposits and stage payments.**
- **Insurance:** it halves the damage from a critical error, at a premium of about 1.2% of revenue.
- **A signed shareholders' agreement and IP assignment:** founder or partner disputes drop from 2% to 0.5% a year and do less harm. Without them, outside investment is impossible.
- **Funding:** once IP is assigned and revenue passes USD 150,000, a seed round has a 25% chance each year from 2028 to 2032. It adds growth and cash for three to four years.
- **Automated compliance:** the yearly chance of a tax or statutory penalty falls from 5% to 1%.

Run 8 then adds two deliberately harsher settings to test how much the results depend on optimistic assumptions. It used 10.6 million futures (10 annual settings of 1 million, 3 monthly runs of 200,000), bringing the page total to about 106 million.

&#91;embedded content\]

### What run 8 shows

- **The legal and financial plan adds as much as the AI plan did.** Pioneer plus hiring alone gives 60% still running in 2036 and a 41.7% chance of USD 100M. Adding the legal and financial plan lifts these to 67% and 49%; the USD 1B chance rises from 19.7% to 25.3%.
- **The cash buffer is the most valuable single item:** without it, survival falls by 4.6 points.
- **IP assignment and the shareholders' agreement come next.** Without them, Formcraft cannot raise money, and the chance of a founder or partner dispute by 2036 rises from 4% to 15%. The USD 100M chance falls by 2.9 points.
- **Insurance** costs margin every year but adds about 1 point of survival and 1.5 points of the USD 100M chance.
- **Funding:** about 48% of full-plan futures raise a seed round by 2032; none can without the IP assignment.
- **Penalties:** automated compliance cuts the chance of at least one tax or statutory penalty by 2036 from 35–38% to 8%.

&#91;embedded content\]

In the monthly model, 30% deposits alone cut the chance of a cash shortfall from 57% to 45%. Deposits together with the buffer cut it to 0.6%. Neither changes revenue; they change when the money arrives.

### My critical reading of the results

These simulations are careful arithmetic on assumptions, and some of the assumptions are generous. This is where I think the model is too kind, where it may be too harsh, and how much to trust it.

**Where the model is probably too optimistic.**

- **"Lifetime revenue by 2072" is a soft target.** Reaching USD 100M over 45 years needs an average of only about USD 2.2M a year. That is why even the sceptic setting (15% growth instead of 30%) still gives 38%. These lifetime figures are useful for comparing settings, but they flatter the plan. They are not the chance of becoming a USD 100M-a-year company, which is far lower and closer to the base rates in the scenarios tab.
- **30% yearly growth for a decade after 2031** is rare for any firm. The sceptic setting is closer to what most surviving small firms achieve.
- **The AI effects are assumptions, not evidence:** errors cut by up to 70%, growth lifted by 6 points, revenue per person up 80%. No Ugandan construction firm has published such data. Formcraft's own audit logs are the first real evidence there will be.
- **The funding chance** (25% a year once eligible) may be high for Uganda's small venture market.
- **Hiring success of 75%** assumes the Academy produces people trained in Formcraft Tools; without it, run 7 showed the USD 100M chance falling to 38%.
- **Survival rates come from US small-business data,** adjusted, not from Ugandan construction firms. Local failure rates may be higher.

**Where the model may be too harsh.**

- **It treats Formcraft as one business growing smoothly.** One large contract (for example the Lubowa hospital pack or a factory) could jump revenue in a single year.
- **Software is modelled like services.** If Formcraft Tools sells well outside Uganda, its growth would not be limited by staff the way design work is.
- **No help from the other ventures** is counted, such as cross-selling with Nyumba or Soko Foods.

**What to trust, and how much.**

- **Trust the comparisons more than the absolute numbers.** Every run gives the same answers: rules beat ad hoc AI, staged tools beat buying everything at once, hire on triggers rather than dates, a cash buffer and signed legal papers are cheap insurance, and Emlyn is the biggest single risk.
- **Trust the near-term numbers more than the long-term ones.** The middle case of about USD 46,000 in 2027, USD 134,000 in 2028 and USD 238,000 in 2029, and a 55–60% chance of a cash shortfall without a buffer, rest on assumptions that can be checked within months.
- **Distrust the USD 1B figures most.** They are 45-year cumulative totals built on growth assumptions few firms achieve.

**Against this project's own goal** ("a top firm in East Africa in the next five years"): by 2031 the middle case is a firm with about USD 0.7M a year in revenue and 20–30 people, still running in about three futures out of four with the full plan. That is a strong, respected Kampala firm, and very possibly East Africa's leader in BIM and AI-driven design. It is not yet a top East African firm by size, since the largest contractors in the region earn many times more. Reaching the top by size in five years would need one or more of: a much larger funding round, a merger or partnership with an established contractor, or Formcraft Tools becoming a regional software business in its own right. The plan positions Formcraft for any of these; it does not deliver them by itself.

**What would change my view fastest:** six months of real data from the rulebook audits, the funnel and the first portal clients. Replace these assumptions with Formcraft's own numbers and rerun the engine, saved in the project as `formcraft_run8_full_plan.py`.

## The sales plan

Sales is a recipe chain, like everything else: every enquiry follows the same steps, and every step is measured in the Command Centre.

**The sales funnel and its targets.**

1. **Lead** (from content, the portal, the standards bank, referrals, walk-ins and tenders): answered within 5 minutes by the WhatsApp assistant.
2. **Qualified** (budget, plot, timing, decision-maker): about half of leads.
3. **Site visit or video call:** booked by the assistant; about 30% of qualified leads.
4. **Quote sent within 48 hours:** from the package-quote recipe (FMC-RCP-SAL-001), with a portal preview of the project.
5. **Won:** target 30% of quotes, with a 30% deposit before work starts.

**What Formcraft sells, as packages.**

- **Template home packages:** fixed price, plot to permit in 9–14 weeks.
- **Studio design packages:** 10%, 15% or 25% of the construction budget, paid 30/40/30.
- **Design-and-build and supervision:** priced on the model's bill of quantities, with bid sessions for partner contractors.
- **Stores furniture and joinery:** catalogue prices with 3D product pages.
- **Software and services for firms:** Formcraft Tools licences, BIM setup, family packs, hosting and Academy seats, sold by demo and free trial.

**The rules of selling.**

- **Follow-up cadence:** day 1, day 3, day 7 and day 14 after a quote, then monthly; the assistant drafts each message and a person sends it.
- **No discount without a reason:** scope comes out before price comes down (the 5% limit in the quote recipe).
- **Diaspora sales:** video calls across time zones, card payments, escrow or milestone accounts, and the portal as proof.
- **B2B and software sales:** a target list of East African firms using Revit, a 30-minute demo, a 14-day trial, and a case study from Formcraft's own projects.
- **Public tenders:** PPDA registration, a bid library of past documents, and only tenders the firm can win and deliver.
- **Lost deals are data:** every lost quote records a reason; the pricing loop reviews them each quarter.

**Sales numbers (in the Command Centre):** leads by source, qualified leads, visits, quotes sent, quote turnaround, win rate, average deal size, pipeline value and weighted forecast, cost per lead, and revenue by segment.

## The project management plan

One method for every project, with the portal as the shared record.

- **Design projects follow the RIBA stages** (0–7): a gate and a client sign-off at the end of each stage, recorded in the portal.
- **Construction follows FIDIC**: a baseline schedule linked to the model (4D), a budget from the bill of quantities (5D), signed variation orders, inspection requests before covering work, and a defects period.
- **Software and systems projects** (the coding sprint) run as weekly sprints in the Command Centre's Plan and tasks view, ticked off daily.

**Project recipes (RB-05).** Project setup (codes, folders, model, portal page); kick-off meeting; weekly client update (written by AI from the site diary and model, approved by the project manager); RFI; variation order; inspection request; non-conformance report; monthly valuation; practical completion; handover pack.

**Controls.**

- **Schedule:** baseline set at kick-off, re-baselined only by signed change; a project is flagged at risk when progress trails time by more than 10 points.
- **Cost:** cost to date against budget and progress; flagged when cost runs more than 5% ahead of progress.
- **Change:** no work on a change without a signed variation order.
- **Quality:** an inspection and test plan per project; snag lists closed before handover.
- **Safety:** inductions, daily toolbox talks, an HSE officer on every site, near-miss reporting in the Bench app.
- **Risk:** a short risk register per project, reviewed weekly.

**Cadence.** A 15-minute daily site check-in; a weekly site meeting and automatic client update; a monthly project review against budget and schedule; a lessons-learned note at handover, feeding the rulebook.

**Project numbers (in the Command Centre):** milestones on time, schedule slip, cost against budget, final cost against estimate, RFIs, variations, snags per handover, incidents and client score.

## The standards bank

The standards bank is a page on the Formcraft website where architects, engineers, quantity surveyors, contractors and students can search building standards by keyword, number or name. It turns the standards register Formcraft is already building for its own rulebook (RB-01) into a public product: build once, use twice.

**What it contains.**

- **One entry per standard:** number, title, edition and status, the body that publishes it, the discipline, and a short scope note written by Formcraft in its own words.
- **Uganda notes:** whether and how it applies in Uganda, and which law or code refers to it.
- **Where to get it:** a link to the official seller (UNBS, ISO, BSI, CEN and others) or, for Ugandan laws, the free official text.
- **How Formcraft uses it:** the recipes, families, templates and checklists that rely on it.
- **Search** by keyword, number, title, discipline, project type and body, with filters and related standards.

**The legal line (important).** Most technical standards (ISO, BS, EN, Eurocodes and UNBS-adopted standards) are copyrighted and sold by their publishers. The bank shows **metadata, Formcraft's own notes and links**, never the standards' full texts, unless a publisher licenses that. Ugandan acts and regulations can be linked to their free official sources. Run 10 shows why this matters: hosting copyrighted texts raised the chance of a legal dispute by 2036 from 4% to 25% and lowered every result. Each entry also carries a disclaimer: notes are guidance, and professionals must check the current official edition.

**How it helps Formcraft.**

- **A magnet for professionals:** engineers and architects searching for a standard find Formcraft, and are the audience for Formcraft Tools, family packs and the Academy.
- **Authority and trust:** a firm that maintains the region's best standards index is a firm clients and partners trust.
- **Search traffic:** each entry is a page that search engines can find.
- **Revenue:** free search for everyone; a paid membership for professionals (notes, compliance checklists, alerts when a standard changes, and links from each standard to Formcraft families and templates); possibly affiliate or reseller arrangements with publishers.
- **Better recipes:** the same register keeps Formcraft's own rulebook current, because a change to a standard flags every recipe that cites it.

**What it costs and needs.** A part-time standards curator (an engineer or QS) once v1 launches; about 100 standards indexed for v1 (by March 2027) and search with membership in v2 (by September 2027); system S13 in the build list. **Metrics:** searches, entries viewed, registered professionals, paid members, and leads for Tools and services from the bank.

## The Formcraft Command Centre

The Command Centre is the live system for running Formcraft: [Formcraft Command Centre](https://claude.ai/artifact/QZwNFsyfC1TNZJeJu5PiRG). It is where the plan on this page meets real data. It is already loaded with the targets, deadlines, systems and hiring triggers from this page, and it holds no invented figures: every number comes from what Formcraft records.

- **Today:** reminders for overdue and upcoming deadlines, the next statutory filing date, fast-track actions for any target behind pace (each linked to the rulebook's playbook), pinned targets, money, pipeline, projects at risk, wins, the live simulation and the task plan.
- **Plan and tasks:** the journey to a billion in six phases with milestones; the foundation sprint as weekly task lists (about 260 hours, with all core coding planned inside 2026); and an hour-by-hour plan for each day. Overdue tasks are carried forward, and when there is time, tasks are pulled forward so Formcraft runs ahead of plan. Tick a task when it is done; the page works out whether Formcraft is ahead or behind.
- **Money:** income and expenses in UGX or USD, by category, division and project, with withholding tax recorded; invoices with ageing, which add the income to the ledger when marked paid.
- **Reports:** profit and loss, cash flow, expenses, receivables, tax summary, sales, marketing, projects, impact, AI and systems, and a monthly management pack, for any period, to view, copy or download.
- **Live simulation:** a smaller version of the run 9 engine that reruns in the browser whenever data changes. It reads the actual revenue run-rate, cash buffer, signed legal papers, finished systems, hires and lead performance, and reports the chances of survival, USD 1M a year by 2031, and the lifetime milestones, with a saved history.
- **Targets, Sales, Projects, Content, Impact, Systems and hiring, Log, Wins:** the trackers behind all of it.

**What it cannot do by itself, and how to add it.** The page cannot read GitHub, the bank or YouTube directly, because pages here cannot call other websites. Two ways to automate it: connect those services to Claude, and set up a scheduled weekly AI task that reads them (commits, issues, statements, channel stats) and writes the numbers and ticks into the Command Centre; or, as each system is built (S05 CRM, S09 finance automation), have those systems write their figures into it. Until then, Monday's review takes about 30 minutes of logging.

## Runs 9 and 10: content, sales, project management and the standards bank

Run 9 added the AI content factory (a 45% chance that a series format takes off, and a content budget that is small and sponsor-funded early, then about 1% of revenue), the sales process (better pricing and conversion) and project management discipline (fewer errors, delays and rework). Run 10 added the standards bank: more professional leads and search traffic, membership income, a curator's cost, and, in a risky variant, the copyright exposure of hosting full texts. Together they used 13 million futures, bringing the page total to about 119 million.

&#91;embedded content\]

- **Sales and project management are the best value of the four:** together they lift survival by about 1 point, the USD 100M chance by 1.8 points and revenue in 2036 by about 5%, at almost no cost.
- **The content factory raises the upside more than the middle.** The USD 1B chance rises by about 1.4 points and revenue in 2036 by 5%, but survival dips slightly, because content costs money every year whether a series takes off or not. Its real value is in the leads it brings, which this model counts only roughly.
- **The standards bank (index model)** adds about 5% to revenue by 2036 and lifts the USD 1B chance from 28.9% to 30.0%, with a small early cost. Hosting copyrighted texts makes everything worse.
- **Everything together, today's Pioneer plan:** about 67% still running in 2036, 52% chance of USD 100M lifetime revenue, 30% of USD 1B; best practice 70%, 56% and 33%; sceptic assumptions 64%, 43% and 21%.
- **The honest reading has not changed.** Each new system adds a little; none changes the picture alone. The big moves are still the cash buffer, signed legal papers, the rulebook, hiring on triggers, and Emlyn's focus. The lifetime revenue figures remain soft targets, and the Command Centre's live simulation will show, month by month, whether Formcraft is beating them or falling behind.

## Copying the pioneer to the other ventures

Formcraft builds each system first, proves it against its gate, and only then copies it. Every venture gets the same value chain map, so the same questions are asked everywhere: what are our nine activities, what does each cost, where is the margin, and where does AI take the hours.

**What carries over unchanged.**

- The rulebook method: written recipes, shared codes, MCP-only tools, edge tests, named approvers, numbered kits and one build queue.
- The autonomy ladder and the weekly audit.
- The content engine and the website funnel template.
- The WhatsApp and web AI assistant (new knowledge base, same system).
- Finance automation: EFRIS invoicing, mobile money reconciliation, the monthly cash report.
- The document system: FMC-style numbering, templates and version control.
- The value chain scorecard and management dashboard.

**What each venture adds to its own chain.**

- **Soko Foods (classic chain).** Inbound: farmer and plantation sourcing, silo stock levels. Operations: drying, milling, quality tests. Outbound: deliveries to schools, the army and shops. Marketing and sales: community buying and online orders. Service: the food-bank shop model and franchise support. AI focus: demand forecasting, stock and price alerts, quality records.
- **Logistics (chain plus network).** Its operations are outbound logistics for others. AI focus: routing, rider scheduling, battery and maintenance tracking, then matching loads to trucks in the app.
- **Nyumba (value network).** Value comes from connecting tenants and landlords. AI focus: listing checks, fraud screening, matching, the USD 5 landlord fee flow.
- **Trade Assistant (value shop).** Value comes from solving each trader's problem. AI focus: research, back-testing, risk rules, and support for the tools sold to the market.

**The rule for copying:** a system moves to another venture only after it has passed its gate at Formcraft, and it arrives with its tests, its rulebook entry and its owner.
