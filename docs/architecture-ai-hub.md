# AI hub, memory, agents and model independence

**Goal:** the Command Centre works with no AI, and works offline. When you add an AI subscription or API key, it becomes fully AI-assisted. You can change AI provider at any time and carry on from all your data and memory.

## 1. Three modes

| Mode | What works |
|---|---|
| No AI | Everything by hand: registers, plans, money, documents, templates, the calendar, and every automation that is a script, not a model. |
| Offline AI | A local model (Ollama or LM Studio) on the PC answers, drafts and summarises. It is slower and less capable, but private and free. |
| Online AI | You add a subscription or API key (Anthropic, OpenAI, Google Gemini, Mistral, or any OpenAI-compatible service). Agents, automations, document drafting and consolidation run fully. |

The app chooses for itself:
- It uses the online provider when there is internet and a key.
- Otherwise it uses the local model.
- Otherwise it falls back to no-AI mode, and tasks are queued until a model is available.

## 2. Where it runs

- **Today:** the claude.ai Command Centre artifact. It uses Claude through your claude.ai account, and its data lives in the artifact database.
- **Windows app (to build):** the same `index.html` inside a desktop shell (Tauri or Electron). It adds:
  - A local SQLite database, so it works offline, with sync to the cloud copy when online.
  - Provider adapters, described below.
  - API keys kept in the Windows Credential Manager, never in the database or in backups.
  - The MCP server (`mcp-server/`) running in the background.
- **Phone:** the same page as an installable web app (PWA), reading the synced data.

## 3. Provider adapter (swap models without changing anything else)

Every provider is wrapped in one interface:

```
chat({system, messages, tools, tier}) -> {text, tool_calls}
embed(texts) -> vectors          // optional, used for memory search
```

| Provider | Quick tier | Default tier | Complex tier |
|---|---|---|---|
| Anthropic | Haiku | Sonnet | Opus |
| OpenAI | small | main | reasoning |
| Gemini | Flash | Pro | Pro (thinking) |
| Ollama (offline) | 3B to 8B model | 8B to 14B model | largest that fits the PC |

- Agents ask for a **tier** (quick, default or complex), never a model name. Changing provider is one setting.
- The tool format (read_data, propose_actions, remember, recall) is the same for every provider. Each adapter translates it to that provider's function-calling format.

## 4. Memory

| Layer | Where | What |
|---|---|---|
| Short-term | `ailog` collection | Every exchange: agent, question, answer, time and who asked. The last 8 per agent are sent with each new question. |
| Long-term | `memory` collection | Facts, decisions, preferences, lessons, rules and summaries. Each is one short idea, with a scope (general or one agent), and can be pinned. Up to 60 per agent go into every prompt; pinned ones go first. |
| Consolidation | AI hub button (or a weekly scheduled task) | Turns unprocessed exchanges into long-term memories, then marks them done. |
| Business data | All other collections | The single source of truth. Agents read it live; it is never copied into memory. |
| Search (Windows app) | Local vector index (for example sqlite-vec) | When memory grows past a few hundred items, recall uses embeddings from the active provider, or a local embedding model offline. |

Memory belongs to Formcraft, not to any AI provider. It is plain JSON, included in every backup.

## 5. Agents

There is one general agent (chief of staff) and one agent per area:
- finance
- sales and marketing
- projects and site
- design and BIM
- software and automation
- people and admin
- legal and risk

Each agent has:
- A rulebook (`rulebooks/agents/<key>.md`).
- Its own memory scope, plus the general scope.
- A model tier.
- An autonomy level, from L0 to L4:

| Level | What the agent may do |
|---|---|
| L0 | Read only |
| L1 | Suggest |
| L2 | Propose for approval (the default) |
| L3 | Act on low-risk items and report |
| L4 | Act on approved routines |

Money, people, contracts and anything sent outside the company always need approval, at every level.

Agents can run on different providers. For example, the design agent on Claude, the sales agent on a cheaper model, and the people agent on an offline model for privacy.

## 6. Changing AI provider (handover protocol)

1. In the AI hub, click **Handover pack** (JSON or Markdown, format `formcraft-handover/1`). It contains:
   - the company record and rules
   - agents
   - all long-term memory
   - the last exchanges
   - plan targets and practices
   - open work
   - systems and automations
   - the tool list
2. Give it to the new model, either as a file or through the MCP resource `formcraft://handover`.
3. The new model continues with the same agents, memory and tools. Nothing is lost, because nothing lived inside the old provider.

## 7. MCP hub

- **Formcraft as a server:** `mcp-server/` exposes tools, resources and agent prompts to any MCP client.
- **Formcraft as a client (Windows app):** it connects out to other MCP servers, so agents can use them with the same approval rules:
  - the Revit plugin MCP
  - Gmail and Calendar
  - file folders
  - accounting
  - a web scraper
- **Registry:** the AI hub lists the connected servers and their tools. Each tool has a risk level, and that level decides whether it needs approval.

## 8. Build order

| Order | Item | Status |
|---|---|---|
| 1 | AI hub, memory, agents, handover pack | Done in the Command Centre |
| 2 | MCP server over backup JSON | Done in this repo |
| 3 | Many PCs, one dataset: Firebase runtime, offline cache, sign-in, rules, installable app (`command-centre/standalone/`) | Built, not yet deployed |
| 4 | Provider adapters (Anthropic and OpenAI-compatible, keys kept on each PC) | Built in the standalone runtime |
| 5 | Ollama and LM Studio offline mode | Built in the adapter (set `provider: 'ollama'`) |
| 6 | MCP client registry | To build |
| 7 | Vector memory search | To build |
| 8 | Phone and Windows app (installable PWA) | Built, not yet deployed |


## 9. Decision: one central database for many PCs (October 2026)

Formcraft needs many PCs and phones on the same data. A JSON file or a SQLite file on one PC cannot safely take writes from several machines.

**Options considered**

| Option | Verdict |
|---|---|
| Own server (Node, with SQLite or Postgres) | Rejected for now: it means building and running sign-in, sync, backups and offline support ourselves. |
| Firebase (Firestore, Auth, Storage, Hosting) | **Chosen.** The team already uses Firebase for the website, and the Command Centre's data calls (`collection().add`, `doc().set`, `onSnapshot`) already match Firestore's. |

**What Firebase gives us without new building**
- live sync across every device
- an offline cache on each device
- sign-in
- access rules on the server
- hosting

**Safeguards**
- It runs as a separate Firebase project from the website.
- The `pending` collection is the only way AI changes data.
- Regular JSON backups can be restored.

**Revisit when** reporting needs SQL. At that point, add a nightly export to BigQuery or Postgres for analysis, and keep Firestore as the live store.

**MCP server**
- On one PC it still works over a backup file. It now has atomic writes and a lock.
- For many PCs, the next step is a version that reads and writes Firestore using a service account.


## 10. Decision: offline model target is 7–8B (30 October 2026)

**Hardware it is sized for:** the main PC has 16 GB RAM and a 4 GB graphics card.

**Why 7–8B**
- A 14B model runs on this PC, but only about a third of it fits on the graphics card. That gives roughly 3–8 words a second, and memory is nearly full.
- A 7–8B model in Q4 form (about 5 GB) runs almost fully on the graphics card, at roughly 15–25 words a second.

| Tier | Online | Offline |
|---|---|---|
| Quick | Small cloud model | 3–4B model, fully on the graphics card |
| Default | Mid cloud model | **7–8B model (Q4_K_M)** |
| Deep | Large cloud model | 7–8B model. A 14B model only for queued overnight jobs, never live chat |

**Settings**
- Context window: 4,096–8,192 tokens. Larger windows use memory fast.
- Keep one model loaded at a time.
- The hub unloads the local model when Revit starts and reloads it when Revit closes.
- Offline models are an optional download in the app's settings, so PCs that only use cloud AI stay light.

**Choosing the model:** run `tools/offline-model-test/` on 2–3 current 7–8B models that support tool calling. Pick the one that passes the most Formcraft tasks: valid tool calls, valid JSON, sensible actions. Speed is the tie-breaker. Repeat the test whenever a new model family is released. Because agents ask for a tier, not a model name, switching means changing one setting.
