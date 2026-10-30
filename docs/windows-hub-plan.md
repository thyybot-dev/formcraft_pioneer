# Formcraft Hub for Windows: design and build plan

*Written 30 October 2026. Owner: Emlyn (development and the main PC).*

The goal is a **fully automated business**. People approve, check, handle exceptions and look after clients. Everything else runs as scripts, or as AI working through scripts.

The Formcraft Hub is the Windows app that runs Formcraft. **Only the three founders have it**, and all three copies stay in sync. Employees use the **web version** (section 14). It holds all Formcraft data: projects, registers, money, people, social posts, newsletters and the website. It connects to AI models, offline or in the cloud, and it is the MCP hub that every app connects through, so Formcraft can run on automations. Each founder has a role in monitoring and checking the AI's work. Emlyn's PC is the main hub. It also does development, runs the Revit jobs and hosts the local AI model.

## 1. Decisions

| Area | Decision | Why |
|---|---|---|
| App stack | C# .NET 8 with WPF, the same style as Revit. Screens are built on `Formcraft.Shell` from the Revit tools, and the Command Centre pages are shown inside through WebView2 | One language and one look across the Revit tools and the hub. The official C# MCP SDK is Tier 1 |
| Online database | **Firebase**: Firestore, Auth, Storage, Functions, Hosting | The website and the standalone Command Centre already run on it |
| Local database | **PostgreSQL** on each hub | Years of history, SQL reports and the change log, without per-read costs |
| Offline AI | 7–8B model (Q4) for the default tier and 3–4B for the quick tier, on the main PC | Fits 16 GB RAM and a 4 GB graphics card (see `architecture-ai-hub.md` §10) |
| Cloud AI | Any provider through one adapter, selected by tier | Swapping models is a settings change |
| Revit | The existing add-in. Each Revit window takes a port from 8080 to 8089 and registers itself in `%APPDATA%\Formcraft\instances` | Two or more Revit windows are already supported |

## 2. How the three hubs work together

| | Main hub (Emlyn, development PC) | Founder hubs (the other two founders) |
|---|---|---|
| Data | Full local PostgreSQL copy, synced with Firestore | Full local copy, synced |
| Screens | Everything, including Development and tests, Connections, Models and Routing | Everything their role allows |
| Runs jobs | Revit jobs (both Revit windows), local AI, scheduled automations, builds and tests | Cloud-only jobs when they are the standby hub; their own AI requests through cloud models |
| Main job | Running automations and development | Monitoring, approving and checking AI work, and running their areas |

**When the main PC is off.** The main hub writes a heartbeat to Firestore every 30 seconds (`hub/lease`). If the heartbeat is more than 5 minutes old, the standby hub (one named founder PC) takes the lease. It then runs only the jobs that don't need the main PC: email, social posts, newsletters, reminders and cloud AI. Revit and local-AI jobs wait for the main PC to come back. Jobs that must never wait (Flutterwave payment confirmations, website form auto-replies) run in Firebase Functions in the cloud, so they keep working when every PC is off.

## 3. Roles: who monitors and checks what

Proposed from the pitch deck. To be confirmed by the founders.

| Founder | Role in the hub | Approves and checks |
|---|---|---|
| Emlyn Atochon | Admin, development, design and BIM | Revit and model jobs, automations, connections, AI settings, releases of the Revit tools and the website, software agent work |
| Peter Isingoma | Projects, Concrete and real estate, finance | Site and project jobs, purchase orders, supplier payments, contracts (jointly with Emlyn), finance agent work |
| Esther Ahumuza | Marketing, sales and interior design | Social posts, newsletters, enquiries and quotes, website content, sales agent work |

**Approval rules**

| Risk | Examples | Needs |
|---|---|---|
| Low | Tags, summaries, internal tasks, drafts | Runs automatically, logged |
| Medium | Posting to social media, client emails, register changes | 1 approval from the owning founder |
| High | Money out, contracts, prices, website releases, model changes in Revit | 1 approval from the owner plus a second founder for money over USD 500 and for contracts |

**Checking.** Each founder reviews a sample of the AI's finished work in their area every week (10% to start). The share with a serious error becomes a KPI: the target is under 2%. If an agent is above target, its autonomy level drops one step until it recovers.

**Monitor screen (all founders).** It shows what each agent is doing now, what's waiting for approval and for whom, what failed and why, what was posted or sent today, and each founder's approval backlog.

## 4. Data

**Firestore (online master).** It holds:
- the Command Centre collections (projects, deals, registers, ledger, staff, todos, memory, ailog, pending, usage, onb and the rest);
- the website collections (copy, settings, team, socialPosts, socialTopics, subscribers, quotes, messages, investorLeads);
- new collections:
  - `jobs`: shared job queue and status;
  - `hub`: lease, hub registry and capabilities;
  - `campaigns`: newsletters;
  - `content`: posts with their state and metrics;
  - `releases`: website and tools.

**PostgreSQL on each hub (local)**

| Part | Purpose |
|---|---|
| Mirror tables | One table per Firestore collection, kept current by live listeners |
| `change_log` (append-only) | Every change: collection, id, before, after, who, when, source (hub, website, AI). Gives undo, audit and the ability to rebuild any table to any moment |
| `outbox` | Changes made on this hub wait here and are sent to Firestore in order. They survive crashes and offline time |
| `jobs`, `job_runs` | Local copy of jobs plus every run's log, duration and result |
| `test_runs`, `builds` | Development and test history (main hub) |
| Reports | SQL views for the reports Firestore cannot do: margins by project, cash by week, AI error rates, content performance |

**Memory cache (hash tables).** Hot data sits in memory (`ConcurrentDictionary`) for instant reads by agents and screens. It is rebuilt from PostgreSQL on startup and is never the only copy.

**Recovery**

| Layer | Setting |
|---|---|
| Firestore | Point-in-time recovery switched on, plus scheduled daily backups |
| PostgreSQL | Write-ahead log, a nightly `pg_dump` to an office drive and to cloud storage (two places), and an automatic test restore every month |
| Change log | Rebuild or undo any record without a full restore |
| Targets | Lose at most 5 minutes of data. Back running within 1 hour |

**Firestore limits the design respects.** About one write per second on any single document. Documents up to 1 MB, so big files go to Storage. No joins, so reports run in PostgreSQL.

## 5. Jobs, routing and load balancing

- **Job record:** type, area, risk, priority, needs (`revit:<document>`, `ollama`, `cloud-ai`, `email`, `social`, `build`), deadline, retries, state, assigned hub and worker.
- **States:** queued → waiting approval → ready → running → done, failed, or retrying, with a full log.
- **Capabilities:** each hub advertises what it can do (the main PC has `revit`, `ollama` and `build`). The router assigns each job to a hub that has what it needs.
- **Revit:** one queue per Revit window. Jobs go to the window with the right model open. If none has it, the idle window opens it read-only first. The two windows work in parallel. Two documents in one window run one after the other.
- **AI:** local model first for quick and default work, unless Revit is busy on that PC. Cloud models for deep work, or when the local model is overloaded. Work continues on the cloud when the main PC is off.
- **Building blocks:** Hangfire, with jobs stored in PostgreSQL, for queues and schedules. YARP to route the hub's local endpoints. Polly for retries, timeouts and circuit breakers. Health checks on every connection every 30 seconds.

## 6. Connections (MCP hub)

| Connection | Address | Notes |
|---|---|---|
| Revit windows | 127.0.0.1:8080–8089, through the Formcraft Revit MCP server | Found from the instances file. One queue each |
| Rhino, Navisworks, Robot | Through the Revit tools' connectors | As built |
| Ollama | 127.0.0.1:11434 | Offline models |
| Cloud AI | HTTPS | Keys kept in Windows Credential Manager |
| Formcraft MCP server (the hub's own) | stdio, plus local HTTP on 127.0.0.1:7420 | For Claude Desktop, Claude Code and other AI tools. Every tool has a risk level |
| Gmail and Calendar, WhatsApp, social platforms, email service, Flutterwave, mobile money, GitHub | Their official APIs | Added one at a time, each with its risk level |

The guard rules from the Revit tools (`fmc_guard`) are the single source for model-safety rules. The hub reads them; it does not keep a copy.

## 7. Content, newsletters and the website

- **Social:** a calendar of posts moving through draft → approved → scheduled → posted (or failed, with a retry). Automatic posting through each platform's API, and views, clicks and leads pulled back for each post. Esther approves.
- **Newsletters:** subscribers from the website, segments, AI drafts from templates, sending through an email service, automatic unsubscribes, and opens and clicks logged.
- **Website:** edit copy, projects, templates, products and prices, then publish. The site reads the content live. Enquiries, quotes and messages land in Sales. Orders and Flutterwave payments are tracked. Code releases go through the Development screen: checks, preview, approve, deploy and roll back. The site's Admin page is retired.

## 8. Development and tests (main PC only)

- GitHub: commits, branches and build status for the website, the Revit tools and this repo.
- One-click test runs (`dotnet test`, `node --test`, the Revit tests with Revit open, the website checks), with history and charts.
- Build the Revit add-in for each Revit version, stage it on the pilot PC, and move releases through test → beta → stable.
- Feature switches per licence or channel. Crash reports and test findings go into GitHub issues.

## 9. Solution layout

```
Formcraft.Hub.sln
  src/Hub.Core        domain types, job and connection interfaces, roles and risk policy
  src/Hub.Data        PostgreSQL (Npgsql + EF Core), change log, outbox, report views, memory cache
  src/Hub.Sync        Firestore (Google.Cloud.Firestore) listeners and the outbox sender, lease and heartbeat
  src/Hub.Jobs        Hangfire queues, router, capability matching, Polly policies
  src/Hub.Mcp         MCP client registry and the hub's own MCP server (official C# SDK)
  src/Hub.Models      model router: Ollama and cloud adapters, tiers, keys in Credential Manager
  src/Hub.Revit       instance discovery, per-window queues, guard policy reader
  src/Hub.Content     social posting, newsletters, website publishing
  src/Hub.Dev         GitHub, test runner, builds, releases (main PC)
  src/Hub.Service     background host: starts with Windows, runs everything above
  src/Hub.App         WPF on Formcraft.Shell: Monitor, Approvals, Connections, Models, Dev; Command Centre in WebView2
  tests/              unit and integration tests for each project
  installer/          Velopack installer and auto-update
```

## 10. Build phases

Estimates are part-time, for one developer.

| Phase | Weeks | Delivers | Test checklist |
|---|---|---|---|
| 0. Skeleton | 1–2 | The solution above. Service and tray app start with Windows. PostgreSQL installed and migrated. Sign-in with Firebase. Command Centre shown in WebView2 | Starts on boot. Restarts after a crash. Sign-in works for all three founders |
| 1. Data and sync | 3–5 | Firestore ↔ PostgreSQL mirror, change log, outbox, roles, nightly backups | Edit on one hub shows on the others within 5 seconds. 50 offline edits all sync in order. A restore drill passes |
| 2. Approvals and the monitor | 6–7 | Shared approval queue with risk rules and the second-founder check, monitor screen, weekly review sampling, the purpose and context pack format (15.1), and the ledger | A high-risk action waits for two founders. The monitor matches Firestore |
| 3. Models and agents | 8–9 | The level router (15.2), escalation, answer cache, budgets, employee AI requests run as jobs, the 8 agents, memory and handover | Works with no internet using the local model. Falls back to the cloud. Unloads the model when Revit starts |
| 4. MCP hub and Revit | 10–12 | Connection registry, the hub's MCP server, two Revit windows with their own queues, router, lease and failover | Jobs run in parallel on both Revits. A frozen Revit's jobs move to the other. Turning the main PC off hands cloud jobs to the standby |
| 5. Content and website | 13–15 | Social calendar and posting, newsletters, website publishing, enquiries, orders | A post goes from draft to posted with metrics. A newsletter sends with unsubscribe. A website edit goes live without a redeploy |
| 6. Development room and installer | 16–18 | GitHub, test runs, builds and releases, script promotion (15.4), balance measures, Velopack installer and auto-update | A one-click test run is stored. An update reaches all three hubs |

**Gate before phase 4:** all three founders use phases 0–3 at least 5 days a week (the 60-day habit check).

## 11. Risks

- **Scope.** This is a large build for one developer. Build in phase order, ship each phase to the founders, and don't start phase 4 before the habit gate.
- **Service account power.** The hub's Firestore credentials skip the access rules. Keep them in Credential Manager, give them only the Firestore user role, have the hub enforce roles itself, and log every write in the change log.
- **Platform APIs.** Social and email APIs change and need app review (Meta in particular). Allow time, and keep manual posting as a fallback.
- **Single main PC.** Revit and local-AI work stop when it is off. Critical cloud jobs keep running through the standby hub and Firebase Functions.

## 12. Open questions

1. Confirm the founders' roles and the USD 500 two-founder threshold.
2. Which founder PC is the standby hub?
3. Which email service sends the newsletters (for example Brevo, Mailchimp or Resend)?

## 13. A simpler Revit plugin: what moves to the hub

**Rule.** The plugin keeps only what needs the live model: the open document, the current view or selection, or a one-click action while modelling. Anything that is administration, settings, data, queues, reports or work across several apps moves out.

**A caution about customers.** Formcraft Tools is also a product sold to other firms, and they will not have the hub. So the plugin must stay complete for paying customers on its own:
- Internal controls move to the hub.
- Customer account, licence and seat management move to the customer's account page on the website. Payments already happen there, never in Revit.

| Area today (in the plugin) | Keep in Revit | Move to the hub (internal) | Move to the website account (customers) |
|---|---|---|---|
| Core: sign-in, account, connect, log, search | Sign-in, connection status light, search inside the model | Logs, connections and port registry, AI involvement levels, admin | Account, plan, invoices |
| Admin: licences and seats | — | Issuing and checking licences (Formcraft side), feature switches | Seats and licence keys for the customer's own team |
| Settings (General, Manage, Flow, Model, Build) | 3–5 per-user basics: theme, units, touch on/off | Company standards, defaults, rules, folder maps, pushed to every plugin | — |
| Manage: templates, families, issue, review, workshare, links, QA, rules, reports | Apply template, load family, place, check this model, issue sheets from this model | Template and family library management, the family factory queue and Gate A results, issue and review registers, QA dashboards, rules editor, reports | Family store downloads |
| Check › Automation, Scripts | Run a script on this model | Script library, schedules, automation runs, AI-versus-script balance | — |
| Flow: sheets, annotate, touch, overlays, gestures | All of it (it is in-model work) | — | — |
| Model: start from brief, systems, structural | Modelling steps | The brief itself, held with the project in the hub | — |
| Engineer: casework and ceilings (steps 1–4) | Room, options, checks and dry run, unit and feature editing | Step 5 outputs: workshop pack, cut lists, nesting, cost, set-out, BoQ, which feed procurement and the workshop | — |
| Engineer: options | Showing options in the model | Comparing options and decisions | — |
| Build: Build pane, web workspace | Revit views for cost and 4D | The cost and BoQ workspace (built on the price book), which is already a web workspace | — |
| Engineering hub (Navisworks, Rhino, Robot, Power BI, exchange) | — | All orchestration: federating, clash runs, Rhino exchange, Power BI feeds | — |

**The plugin after the split**
- **Ribbon:** four groups: Model, Flow, Engineer, Check.
- **Pane:** five pages.
  - **Now:** this model's status, open jobs from the hub and quick tools.
  - **Model**, **Flow** and **Engineer**.
  - **Check:** run checks on this model. Results go to the hub.
- **Ask:** the AI working on this model, through the hub when it is running, or directly for customers.
- **Settings:** a few personal settings. Company settings arrive from the hub, or from the website account for customers.

**What this gains**
- Lighter add-in: faster Revit start-up and fewer things that can fail inside Revit.
- Fewer screens to rebuild and test for each Revit version (2020–2026).
- One place for settings and data across the three founders.
- A cleaner product for customers.

**How the two talk.** The existing local socket per Revit window (ports 8080–8089) through the Revit MCP server. The hub pushes settings and jobs. The plugin sends results, checks and events: model opened, saved, synced.

**Order of work**
1. Move administration and settings (licences, AI involvement, logs, connections) once hub phase 1 is done.
2. Move registers, QA dashboards and the script library with hub phase 2.
3. Move the engineering hub orchestration and the Build workspace with hub phase 4.
4. Move the casework and ceilings outputs with hub phase 5.

Each move ends by removing the old screen from the plugin, so nothing exists in two places.


## 14. Who uses what: founders' apps and employees' web version

| | Founders (3) | Employees |
|---|---|---|
| App | Formcraft Hub for Windows | The web version (`command-centre/standalone`), installable on PCs and phones |
| Data | Local PostgreSQL copy, synced with Firestore | Firestore directly, with an offline cache on the device |
| Screens | Everything their role allows, plus the hub screens (monitor, approvals, connections, models, development on the main PC) | Only their role's screens: Site, Sales and content, Finance, Design and BIM, or Staff, with only their own tasks and registers |
| AI | Through the hub's router | **Never holds an AI key.** Each AI request becomes a job in Firestore `jobs`. The main hub runs it on the cheapest path within the employee's role budget. If the hub is off, the standby hub or a Firebase Function runs the cloud levels |
| Access | Service account in the hub. The hub applies roles and logs every change | Firestore rules apply to every read and write. No admin data is reachable |
| Typical work | Approving, checking, development, clients, strategy | Doing their role's tasks, logging site work and photos, answering what automations cannot, sending exceptions up |

Adding an employee:
1. They sign in once on the web version.
2. A founder gives them a role in the hub.
3. Their screens, tasks, AI budget and approval rights follow from the role.

When someone leaves, removing the role closes everything at once.

## 15. The cheapest path: scripts first, AI as the bridge

**Rule.** For every task, use the cheapest thing that can do it correctly. A script beats a model. A small offline model beats a large one. A large model is for reasoning, development and review. AI uses scripts as its tools and acts as the bridge between them, so most work is exact, repeatable and free.

### 15.1 Every connection declares its purpose

Every call into the hub carries a request: from an agent, Claude Desktop, the Revit pane, an employee on the web version, or an automation. The Revit MCP server and the hub share this one format.

```json
{
  "purpose": "chase invoice FMC-INV-0142 that is 30 days overdue",
  "intent": "finance.invoice.chase",
  "area": "finance",
  "started_by": "ai | person | job | schedule | web",
  "agent": "finance",
  "project": "F26001",
  "risk": "low | medium | high",
  "budget_usd": 0.05
}
```

The hub replies with a context pack before any work starts. It holds references and short extracts, never data dumps:

```json
{
  "task_id": "T-2026-11-0042",
  "scripts": [{"id": "fin.invoice_reminder", "inputs": ["invoice_id", "channel"], "tested": true}],
  "tools": ["read_register", "draft_message", "propose_actions"],
  "memory": ["Client prefers WhatsApp (sales, 2026-10-12)", "Never threaten stop-work before 45 days (rule)"],
  "rulebook": "rulebooks/agents/finance.md#invoices",
  "journal": "Last chase 2026-10-15 by email, no reply",
  "level": 0,
  "limits": {"max_level": 4, "budget_usd": 0.05, "approval": "owner"}
}
```

When the task ends, the hub writes the journal note, any lesson to memory, and a ledger line: purpose, intent, level used, escalations, cost, time, result. It reuses the Revit server's call ledger format, with `started_by` extended to `web`.

### 15.2 The levels

| Level | Runs on | Does | Cost |
|---|---|---|---|
| 0. Scripts and tools | Code | Anything already scripted | Free |
| 1. Rules and lookups | Code: hash tables of intent → script, templates, formulas, regex | Routing, matching, filling templates | Free |
| 2. Worker bots | 3–4B, offline | Sorting, tagging, extracting fields, filling script inputs. Output must pass a schema | Free |
| 3. Area agents | 7–8B, offline | Drafts, summaries, simple tool chains, first-line replies | Free |
| 4. Senior agents | Mid cloud model | Client-facing writing, multi-step reasoning, what level 3 failed | Low |
| 5. Chief, developer, reviewer | Top cloud model | Planning, writing scripts and tests, development, hard reasoning, reviewing | Highest, used least |

**Routing**
1. Look up the intent in the script table. If a tested script exists, run it, with level 2 filling inputs if needed.
2. Otherwise, start at the lowest level allowed for the intent (a table kept in the hub) and check the result.
3. On a failed check, go up one level, up to `max_level`. Every escalation is logged with its reason.
4. If the budget runs out, stop and ask the owning founder. Never overspend silently.

### 15.3 Checks: nobody grades their own work

| Work by | Checked by |
|---|---|
| Scripts | Their tests on every change. Promoted scripts carry their tests |
| Levels 2–3 | Schema check every time. A sample (10% to start) is reviewed by level 4–5 from a different model family |
| Levels 4–5 | The reviewer model on medium and high risk, then the owning person |
| High risk (money, contracts, releases, Revit model changes) | Always a founder. Two founders above USD 500 |

### 15.4 Promotion: AI work becomes scripts

- The ledger groups AI runs by intent. When an intent has been done by AI 3 times with similar inputs, the developer agent (level 5) writes a script plus tests from those runs. It names inputs and outputs and refuses edge cases instead of guessing.
- Emlyn approves it in the development room. It joins the script table at level 0.
- A promoted script that later fails a check is paused, and the intent goes back to AI until the script is fixed.

### 15.5 Keeping it cheap

- **Answer cache:** a hash of intent, inputs and context version maps to a stored answer. A repeat costs nothing.
- **Context diet:** tools return only the fields asked for. No whole-database dumps. The Command Centre's current 60,000-character context per question is retired.
- **Budgets:** a monthly AI budget per agent and per employee role. At 80% of a budget, routing drops one level, except for high-risk work.
- **Offline first:** levels 2–3 run on the main PC whenever Revit isn't busy there.

### 15.6 Measures (weekly, on the monitor and in the Friday report)

| Measure | Target |
|---|---|
| Share of runs done by scripts (levels 0–1) | 50% by month 6, 80% by month 18 (KISIC baseline: 63% of calls were AI-written code) |
| Cost per task and AI spend per month | Falling each quarter |
| Escalation rate by intent | Under 10%. Higher marks the next script to write |
| Serious error rate in reviewed samples | Under 2% |
| Automation share of all business tasks (runs without a person) | Rising every month. This is the "fully automated business" measure |

## 16. Standards bank: licensing rules

- **What the public sees:** for any topic, which standards and laws cover it, the clause and page, Formcraft's own short explanation, the key values, and a link to buy the full standard from its publisher.
- **No PDF files are shared.** Not paid standards and not free downloads. Each standard records its licence (public law, open licence, free to download, paid, or not known), and the website never serves files.
- **Standards never show their wording.** Laws and government regulations are public documents, so their section text may be shown.
- **Paid standards stay with their licence holder.** Copies Formcraft buys are for Formcraft's own use under their licence terms.
- **Opportunity:** ask UNBS, KEBS and the East African standards office about a reseller, affiliate or library-access arrangement. The bank sends buyers to them, which can earn a referral income and makes access easier for professionals.
- *Planning note, not legal advice: confirm the licence terms with each publisher.*
