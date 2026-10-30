# Formcraft Command Centre

One self-contained HTML file (`command-centre/index.html`, vanilla JavaScript, no build step). It runs as a claude.ai artifact and uses these platform capabilities through `window.claude.use(name)`:

| Capability | Used for |
|---|---|
| `db` | All business data (collections listed below), live updates through `onSnapshot`, access rules per collection |
| `user` | Who is signed in (owner = admin), names for people |
| `sample` | The AI assistant (with tools that read data and propose actions for approval), meeting minutes, captions from images, template filling, standards summaries, improvement suggestions |
| `assets` | Uploads (posters, photos, PDFs, receipts) |
| `downloads` | Word (.docx) and Excel (.xlsx) files written in the page itself (own zip writer), CSV, JSON backups, print-ready HTML |

To run it outside claude.ai (Windows app), replace those five with your own backend: a database API with the same collection names, an auth provider, an AI API, file storage and file saving. `tools/fake_claude_runtime.js` shows the exact surface the page expects (it is the in-memory fake used in tests).

## Pages (57)
Overview, Company, Accountability, Decisions and learning, My day, Notice board, Meetings, Team chat, Calendar, Team tasks, Plan and tasks, Gantt timeline, Flowcharts, Reports · Money, Budget and cash, Sales, Projects (with a full page per project), Models and BIM, People and payroll, Formcraft Tools, Content, Website and SEO, Leads and email, Licences and subscribers, Pricing and efficiency, Feasibility studies, Global reach, Incentives and funding, Building playbook · Automations and bots (100 automations), Dev and kits, Systems map (78 systems on Porter's value chain), Build list, Standards bank, Revit and plugins, Enquiries and auto-quotes, Templates (173), Documents, Files and media, Live simulation · Registers (about 40) · Targets, Impact, Legal and risk, Log and deadlines, Wins, Team and access.

## Data model (collections)
Core: `targets, log, deadlines, wins, deals, projects, systems, hires, ledger, invoices, impact, weeks, events, staff, payruns, budget, risks, decisions, assets, compliance`.
Team: `todos, notices, meetings, chat, roles, who, learn`. Software: `issues, lic, autos, bizsys, tpl`. Website: `seo, seokw, reach, campaigns, enq`. Files and documents: `files, docs, timelog, feas`. Settings: `meta/settings` (company record, pricing, plans, playbook ticks, rhythm, simulation history).
Registers: `reg_<key>` for clients, professionals, contractors, suppliers, partners, investors, candidates, prospects, subscribers, lenders, contracts, pricebook, tenders, po, drawings, rfis, variations, sitediary, defects, permits, qa, hse, models, plant, inventory, knowledge, training, leave, ip, grants, support, media, standards, feedback, accounts, debts, recurring, purchases, rides, toolstack, releases, kits, recipes.

## Access rules
Default: signed-in people read; Contributors write. Admin only (read and write): staff, payruns, ledger, budget, invoices, hires, lic, contracts, investors, candidates, accounts, debts, recurring, lenders. Admin write: meta (settings), roles. Prospects and subscribers need Contributor to read. Pages per role are set in `ROLE_PAGES`.

## Scheduled task
"Formcraft morning accountability brief", weekdays 06:50 Kampala time: reads the data, posts the brief to the notice board and pushes it to Emlyn's phone.

## Testing
`node tools/test_command_centre.js` with Playwright: loads the page with the fake runtime, clicks through every page and the main actions, and fails on any page error.


## AI hub and memory (added October 2026)

- **Page:** AI hub and memory, under Build and AI.
- **Agents:** a general agent plus 7 area agents. Each has a model tier, an autonomy level (L0 to L4) and extra instructions. You can pick the agent in the floating AI panel.
- **Collections:**
  - `memory`: long-term memory. Fields: text, kind, scope, pinned, archived.
  - `ailog`: short-term memory. Fields: agent, q, a, at, done.
- **AI tools:** read_data, propose_actions, remember, recall.
- **Handover pack:** JSON or Markdown, used to switch AI provider.
- **MCP manifest:** a download from the AI hub page.
- See `docs/architecture-ai-hub.md` and `mcp-server/`.

## Client on and offboarding (added October 2026)

- **Page:** Client on and offboarding, under Business.
- **Playbooks:** one onboarding and one offboarding playbook for each of 7 services and products: design, construction and design-and-build, Concrete, Stores, BIM services, Formcraft Tools licences, and advisory. Each step has an owner, a due day, the template or register to use, and its automation. You can add your own steps per service (saved in `settings.obExtra`).
- **Collection `onb`:** client, line, kind (Onboarding or Offboarding), start, owner, project, done (step index → date and who), status, closed.
- **Suggestions:** journeys are suggested from won deals, completed projects, and expired or revoked licences.
- **Actions:** tick steps, put the open steps on the task board, download a Word checklist, have the AI draft the welcome or close-out message, close a journey, or start offboarding from an onboarding.
- **Alerts:** overdue steps appear in the morning brief.
- **AI action:** `start_journey`. New automations: CS-01, CS-02 and CS-03.
- The full playbooks are in `rulebooks/client-onboarding-offboarding.md`.

## Founders' daily, shared approvals and smarter automations (October 2026)

- **Founders' daily** (first in the menu, and the landing page for founders) is one screen with:
  - the morning brief;
  - the approval queue;
  - one live register: the sales pipeline, projects or client journeys;
  - the 60-day habit check. The rule: each founder opens the Command Centre at least 5 days a week. If they all do, expand the system; if not, stop building and fix the habit.
- **Collections:**
  - `pending`: shared AI proposals. Fields: `a` (the action), status (pending, approved or rejected), agent, at, by, decided, decidedBy. Any founder on any device can approve or reject. The MCP server accepts the same shape.
  - `usage`: one record per person per day they open the app. It feeds the habit check.
- **Settings:** `founders` (who counts in the check), `dailyStart` and `dailyReg`.
- **Automations:** there are now 122 automations (29 new, for example tender deadlines, RFI ageing, milestone billing, the 8-week cash forecast and defect close-out checks). 62 of them have an "upgrade": a second version that pulls context from another register. The upgrade is shown in green and is included in the AI recipe prompt.
- **Restore:** under Access, a backup JSON can be restored into any database. Use it to move from claude.ai to the company Firebase project (`command-centre/standalone/`).

## Approvals and professionals, and the public standards bank (October 2026)

- **Approvals and professionals** (under Business) has five tabs:
  - **Approval guides:** one per authority, with steps, documents, fees and their source, official time and the date last checked. There is a button to add the 14 Kampala-area authorities. Fees and times start blank until verified.
  - **Approval times:** reports from Formcraft projects and from other architects.
  - **Professionals:** the directory.
  - **Contributions:** submissions waiting for review, including AI extraction from a pasted group chat.
  - **Website preview.**
- **Confirm first.** Listings start Private. A confirmation message (SMS or WhatsApp text, with a WhatsApp link) asks the person to reply YES with their code. Only listings marked Confirmed or Register-checked are public. Removal deletes the phone number and email and keeps a fingerprint, so the person is not added again. Duplicates are caught by phone number or registration number. A repeat recommendation adds to the "added by N architects" count.
- **Public approval times** show only medians and ranges, and only once an authority has 3 or more reports. Contributors are never named.
- **Collections:** `appr_auth`, `appr_rep`, `pros`, `contrib`.
- **Standards bank:** new fields `pub`, `webnote` and `buy`. There is a publish button on each standard and a website preview, and the public view shows reference details and Formcraft's own note only.
- **Website data:** a "Download website data (JSON)" button exports exactly what the public pages may show. The website should read only published copies (automation WS-07 publishes them to public collections), never `pros` directly, because that collection holds private phone numbers.
- **New automations:** WS-05 (confirmation sender), WS-06 (approval times digest), WS-07 (public data publish).

## Standards bank: search by topic, country first (October 2026)

- **Tabs:** Search by topic, Standards and laws, Add sections, and Website preview.
- **Search by topic:** a search such as "walls" or "roofs" returns every relevant section across standards and building laws. Synonyms are understood ("roofing" finds roof pitch). Results are grouped with the chosen country first (Uganda by default), then East African standards, then international, then other East African countries. On the website, the country will come from the visitor's location.
- **Each result** shows the standard or law, its clause and page, Formcraft's own explanation, the key values and the topics, with a link to buy the full standard or to the official source. Law and regulation sections can show their text. Standards never show their wording.
- **Add sections:** paste text from a PDF you own, and the AI splits it into sections. For standards, the pasted wording is never saved. New sections start hidden until checked.
- **Collection** `std_clauses`. Its fields are std or source, kind, juris, ref, page, heading, topics, summary, values, text (laws only) and pub.
- **No PDF files are ever shared.** Each standard records its licence (`licence` field). The website shows only references, page numbers, Formcraft's explanations and buy links.
