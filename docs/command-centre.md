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
