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
| 3 | Windows shell with SQLite and sync | To build |
| 4 | Provider adapters and keychain keys | To build |
| 5 | Ollama offline mode | To build |
| 6 | MCP client registry | To build |
| 7 | Vector memory search | To build |
| 8 | Phone PWA | To build |
