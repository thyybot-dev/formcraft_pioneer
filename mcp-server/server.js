#!/usr/bin/env node
// Formcraft Command Centre MCP server (stdio, no dependencies).
// Serves a Command Centre data file (the JSON from "Download full backup", or the Windows app's export)
// to any MCP client: Claude Desktop, other agent tools, local models through an MCP-capable runner.
// Usage: FORMCRAFT_DATA=/path/formcraft-backup.json node server.js
// Writes go to the same file. Changes from AI are queued in `pending` and only applied by apply_approved.
'use strict';
const fs = require('fs'), path = require('path'), readline = require('readline');
const FILE = process.env.FORMCRAFT_DATA || path.join(__dirname, 'formcraft-data.json');
const load = () => { try { return JSON.parse(fs.readFileSync(FILE, 'utf8')); } catch (e) { return {}; } };
// Atomic save: write a temp file, then rename, so a crash never leaves a half-written file.
const save = d => { const tmp = FILE + '.' + process.pid + '.tmp'; fs.writeFileSync(tmp, JSON.stringify(d, null, 1)); fs.renameSync(tmp, FILE); };
// Cross-process lock so two MCP clients on the same file cannot overwrite each other's changes.
const LOCK = FILE + '.lock';
function withLock(fn) {
  const t0 = Date.now(); let fd;
  for (;;) {
    try { fd = fs.openSync(LOCK, 'wx'); break; } catch (e) {
      if (e.code !== 'EEXIST') throw e;
      try { if (Date.now() - fs.statSync(LOCK).mtimeMs > 10000) { fs.unlinkSync(LOCK); continue; } } catch (_) { continue; }
      if (Date.now() - t0 > 5000) throw new Error('data file is busy, try again');
      Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 25);
    }
  }
  try { return fn(); } finally { fs.closeSync(fd); try { fs.unlinkSync(LOCK); } catch (_) {} }
}
// Allowed AI actions and their required fields. Anything else is rejected before it reaches the queue.
const ACTIONS = { add_task: ['t'], post_notice: ['title'], log_metric: ['metric', 'value'], add_register_row: ['register', 'row'], add_deal: ['client'], add_learning: ['t'] };
function checkAction(x) {
  if (!x || typeof x !== 'object') return 'not an object';
  const need = ACTIONS[x.type]; if (!need) return 'unknown type "' + x.type + '" (allowed: ' + Object.keys(ACTIONS).join(', ') + ')';
  const miss = need.filter(f => x[f] === undefined || x[f] === null || x[f] === ''); if (miss.length) return x.type + ' is missing ' + miss.join(', ');
  if (x.type === 'log_metric' && !isFinite(Number(x.value))) return 'log_metric value must be a number';
  if (x.type === 'add_deal' && x.value !== undefined && !isFinite(Number(x.value))) return 'add_deal value must be a number';
  if (x.type === 'add_register_row' && (!REGS.includes(x.register) || typeof x.row !== 'object')) return 'add_register_row needs a known register and a row object';
  if (x.due && !/^\d{4}-\d{2}-\d{2}$/.test(x.due)) return 'due must be YYYY-MM-DD';
  return null;
}
// Ranked search: share of query words found (prefix match), so partial matches still come back, best first.
function score(q, text) { const w = String(q).toLowerCase().split(/\W+/).filter(x => x.length > 1); if (!w.length) return 0; const t = String(text).toLowerCase(); const toks = t.split(/\W+/);
  return w.filter(x => t.includes(x) || toks.some(k => k.startsWith(x.slice(0, Math.max(4, x.length - 2))))).length / w.length; }
const today = () => new Date().toISOString().slice(0, 10);
const id = () => Math.random().toString(36).slice(2, 12);
const arr = (d, k) => (d[k] = Array.isArray(d[k]) ? d[k] : []);
const REGS = ['clients','professionals','contractors','suppliers','partners','investors','candidates','prospects','subscribers','lenders','contracts','pricebook','tenders','po','drawings','rfis','variations','sitediary','defects','permits','qa','hse','models','plant','inventory','knowledge','training','leave','ip','grants','support','media','standards','feedback','accounts','debts','recurring','purchases','rides','toolstack','releases','kits','recipes'];
const AGENTS = { general: 'Chief of staff', finance: 'Finance', sales: 'Sales and marketing', projects: 'Projects and site', design: 'Design and BIM', software: 'Software and automation', people: 'People and admin', legal: 'Legal and risk' };

function brief(d) {
  const td = today(), A = [];
  arr(d, 'todos').filter(t => t.status !== 'Done' && t.due && t.due < td).forEach(t => A.push('Overdue task: ' + t.t + ' (' + t.due + ')'));
  arr(d, 'deadlines').filter(x => !x.done && x.due && x.due <= td).forEach(x => A.push('Deadline: ' + x.title + ' (' + x.due + ')'));
  arr(d, 'invoices').filter(i => !i.paid && i.due && i.due < td).forEach(i => A.push('Overdue invoice: ' + i.client + ' USD ' + i.amount));
  arr(d, 'meetings').filter(m => m.date === td).forEach(m => A.push('Meeting today ' + (m.time || '') + ': ' + m.title));
  const inc = arr(d, 'ledger').filter(e => e.type === 'Income' && (e.date || '').startsWith(td.slice(0, 7))).reduce((a, e) => a + Number(e.amountUSD || 0), 0);
  return { date: td, income_this_month_usd: Math.round(inc), alerts: A, open_tasks: arr(d, 'todos').filter(t => t.status !== 'Done').length };
}
const TOOLS = [
  { name: 'get_brief', description: 'Morning brief: overdue tasks, deadlines, invoices, meetings today, income this month.', inputSchema: { type: 'object', properties: {} },
    run: (a, d) => brief(d) },
  { name: 'read_data', description: 'Read a collection: todos, deals, projects, targets, log, meetings, notices, issues, deadlines, risks, ledger, invoices, staff, settings, memory, learn, enq, files, docs.', inputSchema: { type: 'object', properties: { area: { type: 'string' }, limit: { type: 'number' } }, required: ['area'] },
    run: (a, d) => a.area === 'settings' ? (d.settings || {}) : arr(d, a.area).slice(-(a.limit || 200)) },
  { name: 'query_register', description: 'Search a register by words. Registers: ' + REGS.join(', '), inputSchema: { type: 'object', properties: { register: { type: 'string' }, query: { type: 'string' } }, required: ['register'] },
    run: (a, d) => { const q = String(a.query || '').toLowerCase(); return arr(d, 'reg_' + a.register).filter(r => !q || JSON.stringify(r).toLowerCase().includes(q)).slice(0, 200); } },
  { name: 'propose_actions', description: 'Queue changes for a person to approve. Each action: {type: add_task|post_notice|log_metric|add_register_row|add_deal|add_learning, ...fields}. Nothing changes until apply_approved.', inputSchema: { type: 'object', properties: { actions: { type: 'array', items: { type: 'object' } }, agent: { type: 'string' } }, required: ['actions'] },
    run: (a, d) => { const P = arr(d, 'pending'), bad = []; let n = 0; (a.actions || []).forEach((x, i) => { const err = checkAction(x); if (err) bad.push({ index: i, error: err }); else { P.push(Object.assign({}, x, { id: id(), at: new Date().toISOString(), agent: a.agent || 'general', status: 'pending' })); n++; } }); save(d); return { queued: n, rejected: bad }; } },
  { name: 'reject_pending', description: 'Reject pending actions by id (a person decided not to apply them).', inputSchema: { type: 'object', properties: { ids: { type: 'array', items: { type: 'string' } }, reason: { type: 'string' } }, required: ['ids'] },
    run: (a, d) => { let n = 0; arr(d, 'pending').filter(p => a.ids.includes(p.id) && p.status === 'pending').forEach(p => { p.status = 'rejected'; p.reason = a.reason || ''; n++; }); save(d); return { rejected: n }; } },
  { name: 'list_pending', description: 'List actions waiting for approval.', inputSchema: { type: 'object', properties: {} }, run: (a, d) => arr(d, 'pending').filter(p => p.status === 'pending') },
  { name: 'apply_approved', description: 'Apply pending actions by id. Only call when the person has approved them.', inputSchema: { type: 'object', properties: { ids: { type: 'array', items: { type: 'string' } } }, required: ['ids'] },
    run: (a, d) => { let n = 0; arr(d, 'pending').filter(p => a.ids.includes(p.id) && p.status === 'pending').forEach(p => { apply(d, p.a || p); p.status = 'applied'; n++; }); save(d); return { applied: n }; } },
  { name: 'remember', description: 'Save a long-term memory that every future AI model will see. kind: Fact|Decision|Preference|Lesson|Rule|Summary. scope: general or an agent key (' + Object.keys(AGENTS).join(', ') + ').', inputSchema: { type: 'object', properties: { text: { type: 'string' }, kind: { type: 'string' }, scope: { type: 'string' } }, required: ['text'] },
    run: (a, d) => { arr(d, 'memory').push({ id: id(), text: a.text, kind: a.kind || 'Fact', scope: a.scope || 'general', date: today(), by: 'AI (MCP)', ai: true }); save(d); return { saved: true }; } },
  { name: 'recall', description: 'Search long-term memory and past AI exchanges.', inputSchema: { type: 'object', properties: { query: { type: 'string' }, scope: { type: 'string' } }, required: ['query'] },
    run: (a, d) => { const rank = (L, f) => L.map(x => [score(a.query, f(x)), x]).filter(r => r[0] >= 0.5).sort((p, q) => q[0] - p[0] || (q[1].pin ? 1 : 0) - (p[1].pin ? 1 : 0)).slice(0, 20).map(r => Object.assign({ match: Math.round(r[0] * 100) / 100 }, r[1]));
      return { memory: rank(arr(d, 'memory').filter(m => !m.archived && (!a.scope || m.scope === a.scope || m.scope === 'general')), m => m.text + ' ' + (m.kind || '')), exchanges: rank(arr(d, 'ailog'), x => x.q + ' ' + x.a).slice(0, 10) }; } },
  { name: 'log_exchange', description: 'Record a short-term memory entry (question and answer) for an agent.', inputSchema: { type: 'object', properties: { agent: { type: 'string' }, q: { type: 'string' }, a: { type: 'string' } }, required: ['q', 'a'] },
    run: (a, d) => { arr(d, 'ailog').push({ id: id(), agent: a.agent || 'general', q: a.q, a: a.a, at: new Date().toISOString(), by: 'AI (MCP)' }); save(d); return { saved: true }; } },
  { name: 'handover_pack', description: 'Everything a new model needs to continue: company, agents, memory, targets, open work.', inputSchema: { type: 'object', properties: {} },
    run: (a, d) => ({ format: 'formcraft-handover/1', company: (d.settings || {}).company || {}, agents: AGENTS, memory: arr(d, 'memory').filter(m => !m.archived), targets: arr(d, 'targets'), open_tasks: arr(d, 'todos').filter(t => t.status !== 'Done'), deadlines: arr(d, 'deadlines').filter(x => !x.done), recent_exchanges: arr(d, 'ailog').slice(-30) }) },
  { name: 'log_metric', description: 'Log a business number (metric key, value, date). Applied directly.', inputSchema: { type: 'object', properties: { metric: { type: 'string' }, value: { type: 'number' }, date: { type: 'string' } }, required: ['metric', 'value'] },
    run: (a, d) => { arr(d, 'log').push({ id: id(), metric: a.metric, value: a.value, date: a.date || today(), note: 'MCP' }); save(d); return { logged: true }; } }];
function apply(d, p) {
  const td = today();
  if (p.type === 'add_task') arr(d, 'todos').push({ id: id(), t: p.t, kind: p.kind || 'Task', due: p.due || '', pri: p.pri || 'P2', status: 'To do', date: td, ai: true });
  else if (p.type === 'post_notice') arr(d, 'notices').push({ id: id(), title: p.title, body: p.body || '', aud: 'All', date: td, ai: true });
  else if (p.type === 'log_metric') arr(d, 'log').push({ id: id(), metric: p.metric, value: Number(p.value), date: p.date || td });
  else if (p.type === 'add_register_row') arr(d, 'reg_' + p.register).push(Object.assign({ id: id(), added: td, ai: true }, p.row || {}));
  else if (p.type === 'add_deal') arr(d, 'deals').push({ id: id(), client: p.client, value: Number(p.value) || 0, stage: p.stage || 'Lead', next: p.next || '', nextDate: p.nextDate || '' });
  else if (p.type === 'add_learning') arr(d, 'learn').push({ id: id(), kind: p.kind || 'Improvement', t: p.t, d: p.d || '', status: 'Suggested', date: td, ai: true });
}
const RES = () => [{ uri: 'formcraft://company', name: 'Company record', mimeType: 'application/json' }, { uri: 'formcraft://memory', name: 'Long-term memory', mimeType: 'application/json' }, { uri: 'formcraft://projects', name: 'Projects', mimeType: 'application/json' }, { uri: 'formcraft://handover', name: 'Handover pack', mimeType: 'application/json' }];
function readRes(uri, d) { if (uri === 'formcraft://company') return (d.settings || {}).company || {}; if (uri === 'formcraft://memory') return arr(d, 'memory'); if (uri === 'formcraft://projects') return arr(d, 'projects'); if (uri === 'formcraft://handover') return TOOLS.find(t => t.name === 'handover_pack').run({}, d); throw new Error('unknown resource'); }
function agentPrompt(k) { const f = path.join(__dirname, '..', 'rulebooks', 'agents', k + '.md'); return fs.existsSync(f) ? fs.readFileSync(f, 'utf8') : 'You are the ' + (AGENTS[k] || k) + ' agent for Formcraft.'; }
function handle(m) {
  const d = load();
  switch (m.method) {
    case 'initialize': return { protocolVersion: (m.params && m.params.protocolVersion) || '2025-06-18', capabilities: { tools: {}, resources: {}, prompts: {} }, serverInfo: { name: 'formcraft-command-centre', version: '1.0.0' } };
    case 'ping': return {};
    case 'tools/list': return { tools: TOOLS.map(({ name, description, inputSchema }) => ({ name, description, inputSchema })) };
    case 'tools/call': { const t = TOOLS.find(x => x.name === m.params.name); if (!t) throw new Error('unknown tool ' + m.params.name);
      try { const out = withLock(() => t.run(m.params.arguments || {}, load())); return { content: [{ type: 'text', text: JSON.stringify(out) }] }; } catch (e) { return { content: [{ type: 'text', text: 'Error: ' + e.message }], isError: true }; } }
    case 'resources/list': return { resources: RES() };
    case 'resources/read': return { contents: [{ uri: m.params.uri, mimeType: 'application/json', text: JSON.stringify(readRes(m.params.uri, d)) }] };
    case 'prompts/list': return { prompts: Object.entries(AGENTS).map(([k, n]) => ({ name: 'agent_' + k, description: n + ' agent rulebook and memory' })) };
    case 'prompts/get': { const k = m.params.name.replace(/^agent_/, ''); const mem = arr(d, 'memory').filter(x => !x.archived && (x.scope === k || x.scope === 'general')).map(x => '- ' + x.text).join('\n');
      return { description: AGENTS[k], messages: [{ role: 'user', content: { type: 'text', text: agentPrompt(k) + '\n\nLong-term memory:\n' + mem } }] }; }
    default: throw Object.assign(new Error('Method not found: ' + m.method), { code: -32601 });
  }
}
readline.createInterface({ input: process.stdin }).on('line', line => {
  if (!line.trim()) return; let m; try { m = JSON.parse(line); } catch (e) { return; }
  if (m.id === undefined) return; // notification
  let out; try { out = { jsonrpc: '2.0', id: m.id, result: handle(m) }; } catch (e) { out = { jsonrpc: '2.0', id: m.id, error: { code: e.code || -32603, message: e.message } }; }
  process.stdout.write(JSON.stringify(out) + '\n');
});
