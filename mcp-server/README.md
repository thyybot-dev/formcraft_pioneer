# Formcraft Command Centre MCP server

A small MCP server with no dependencies (Node 18 or later). It lets any MCP-capable AI read and work on Formcraft data: Claude Desktop, Claude Code, other agent apps, or a local model through an MCP-capable runner.

## Run

1. In the Command Centre, use **Download full backup** (or the Windows app's export) and save it as `formcraft-data.json`.
2. Point the server at that file:

```
FORMCRAFT_DATA=C:\Formcraft\formcraft-data.json node server.js
```

## Claude Desktop config (`claude_desktop_config.json`)

```json
{
  "mcpServers": {
    "formcraft": {
      "command": "node",
      "args": ["C:\\Formcraft\\formcraft_pioneer\\mcp-server\\server.js"],
      "env": { "FORMCRAFT_DATA": "C:\\Formcraft\\formcraft-data.json" }
    }
  }
}
```

## What it exposes

- **Tools:** get_brief, read_data, query_register, propose_actions, list_pending, apply_approved, reject_pending, remember, recall, log_exchange, handover_pack, log_metric
- **Resources:** formcraft://company, formcraft://memory, formcraft://projects, formcraft://handover
- **Prompts:** agent_general, agent_finance, agent_sales, agent_projects, agent_design, agent_software, agent_people, agent_legal. Each one is built from `rulebooks/agents/<key>.md` plus that agent's long-term memory.

## Safety

- Changes proposed by an AI are queued in `pending`. Only `apply_approved`, called after a person approves, writes them into the data.
- Memory and metrics are written directly.
- The server holds no API keys.

## Test

```
printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | FORMCRAFT_DATA=test.json node server.js
```

## Reliability (October 2026 review)

- **Atomic writes and a lock:** saves go to a temp file, then a rename. A lock file stops two clients writing at once (tested with 20 writers in parallel: no lost writes). This covers several clients on one PC. For several PCs, use the central server described in `docs/architecture-ai-hub.md`.
- **Checked AI actions:** `propose_actions` accepts only six action types, each with its required fields. Bad actions are returned with the reason and never reach the queue.
- **Ranked recall:** a memory matches if half or more of the query words match (partial word stems count). Results come best first, with pinned memories ahead on ties.
