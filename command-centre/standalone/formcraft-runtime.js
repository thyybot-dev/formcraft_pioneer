/* Formcraft Command Centre: standalone runtime.
   Gives the Command Centre the same five services it has inside claude.ai (db, user, sample, assets, downloads),
   backed by Firebase, so every PC and phone works on one live dataset:
   - Firestore with offline cache: works without internet and syncs when back online.
   - Firebase Auth: each person signs in; roles come from the roles collection and firestore.rules.
   - Firebase Storage: files and receipt photos.
   - AI: any provider through one adapter (Anthropic, or any OpenAI-compatible API: OpenAI, Gemini, Mistral, Ollama, LM Studio).
     API keys stay on each PC (browser storage), never in the shared database.
   Needs: the Firebase compat SDK scripts and formcraft-config.js loaded before this file. */
(function () {
  'use strict';
  const C = window.FORMCRAFT_CONFIG || {};
  if (!window.firebase || !C.firebase) { console.warn('Formcraft: Firebase is not configured; running in offline view.'); return; }
  firebase.initializeApp(C.firebase);
  const auth = firebase.auth(), fs = firebase.firestore();
  const storage = firebase.storage ? firebase.storage() : null;
  fs.settings({ ignoreUndefinedProperties: true });
  fs.enablePersistence({ synchronizeTabs: true }).catch(() => {}); // offline cache on this device

  // Firestore cannot store arrays inside arrays: store those as JSON and restore them on read.
  const enc = v => Array.isArray(v) ? (v.some(Array.isArray) ? { __fcjson: JSON.stringify(v) } : v.map(enc))
    : (v && typeof v === 'object' && !(v instanceof Date) && !(v instanceof Blob)) ? Object.fromEntries(Object.entries(v).map(([k, x]) => [k, enc(x)])) : v;
  const dec = v => Array.isArray(v) ? v.map(dec)
    : (v && typeof v === 'object') ? (typeof v.__fcjson === 'string' ? JSON.parse(v.__fcjson) : (typeof v.toDate === 'function' ? v.toDate().toISOString() : Object.fromEntries(Object.entries(v).map(([k, x]) => [k, dec(x)])))) : v;
  const fix = p => p.catch(e => { if (e && e.code === 'permission-denied') e.code = 'invalid_argument'; throw e; }); // same error the app already handles
  const snap = d => ({ id: d.id, exists: d.exists, data: () => dec(d.data()) });
  const db = {
    collection: c => ({
      add: d => fix(fs.collection(c).add(enc(d))).then(r => ({ id: r.id })),
      onSnapshot: (cb, err) => fs.collection(c).onSnapshot(s => cb({ docs: s.docs.map(snap) }), err)
    }),
    doc: p => { const r = fs.doc(p); return {
      set: d => fix(p.startsWith('who/') ? r.set(enc(d), { merge: true }) : r.set(enc(d))), update: d => fix(r.update(enc(d))), delete: () => fix(r.delete()),
      get: () => r.get().then(snap), onSnapshot: (cb, err) => r.onSnapshot(d => cb(snap(d)), err) }; }
  };

  // ---- Sign-in screen ----
  let resolveReady; const ready = new Promise(r => resolveReady = r);
  function gate() {
    const el = document.createElement('div'); el.id = 'fc-signin';
    el.innerHTML = '<style>#fc-signin{position:fixed;inset:0;z-index:99999;background:#0f2a2e;display:flex;align-items:center;justify-content:center;font-family:system-ui,sans-serif}#fc-signin .b{background:#fff;border-radius:14px;padding:28px;width:340px;box-shadow:0 10px 40px #0005}#fc-signin h1{font-size:20px;margin:0 0 4px}#fc-signin p{color:#666;font-size:13px;margin:0 0 16px}#fc-signin input{width:100%;box-sizing:border-box;padding:10px;margin:0 0 8px;border:1px solid #ccc;border-radius:8px}#fc-signin button{width:100%;padding:10px;border-radius:8px;border:0;background:#0f766e;color:#fff;font-weight:600;margin:4px 0;cursor:pointer}#fc-signin button.g{background:#fff;color:#222;border:1px solid #ccc}#fc-signin .e{color:#c0392b;font-size:12px;min-height:16px}</style>' +
      '<div class="b"><h1>Formcraft Command Centre</h1><p>Sign in to work on the shared company data.</p><button class="g" id="fc-g">Continue with Google</button><div style="text-align:center;color:#999;font-size:12px;margin:8px 0">or</div><input id="fc-e" type="email" placeholder="Email" autocomplete="username"><input id="fc-p" type="password" placeholder="Password" autocomplete="current-password"><button id="fc-in">Sign in</button><button class="g" id="fc-up">Create account</button><button class="g" id="fc-rs">Forgot password</button><div class="e" id="fc-x"></div></div>';
    document.body.appendChild(el);
    const err = e => document.getElementById('fc-x').textContent = (e && e.message) || String(e);
    const ev = () => [document.getElementById('fc-e').value.trim(), document.getElementById('fc-p').value];
    document.getElementById('fc-g').onclick = () => auth.signInWithPopup(new firebase.auth.GoogleAuthProvider()).catch(err);
    document.getElementById('fc-in').onclick = () => auth.signInWithEmailAndPassword(...ev()).catch(err);
    document.getElementById('fc-up').onclick = () => auth.createUserWithEmailAndPassword(...ev()).catch(err);
    document.getElementById('fc-rs').onclick = () => auth.sendPasswordResetEmail(ev()[0]).then(() => err('Reset email sent.')).catch(err);
  }
  let user = null, roleDoc = null;
  auth.onAuthStateChanged(async u => {
    if (!u) { if (!document.getElementById('fc-signin')) (document.body ? gate() : addEventListener('DOMContentLoaded', gate)); return; }
    if (user && user.uid !== u.uid) location.reload();
    user = u; const g = document.getElementById('fc-signin'); if (g) g.remove();
    try { const r = await fs.doc('roles/' + u.uid).get(); roleDoc = r.exists ? r.data() : null; } catch (e) { roleDoc = null; }
    fs.doc('who/' + u.uid).set({ name: u.displayName || (u.email || '').split('@')[0] }, { merge: true }).catch(() => {});
    resolveReady();
  });
  window.fcSignOut = () => auth.signOut().then(() => location.reload());
  const isOwner = () => !!user && (C.owners || []).map(x => x.toLowerCase()).includes((user.email || '').toLowerCase());

  const userCap = {
    id: async () => user.uid,
    me: async () => ({ id: user.uid, name: user.displayName || (user.email || '').split('@')[0] }),
    isOwner: async () => isOwner(),
    canEdit: async () => isOwner() || !!roleDoc,
    profiles: async ids => { const o = {}; await Promise.all(ids.map(async i => { try { const d = await fs.doc('who/' + i).get(); if (d.exists && d.data().name) o[i] = { name: d.data().name }; } catch (e) {} })); return o; },
    search: async q => { const s = await fs.collection('who').get(); q = String(q || '').toLowerCase(); return s.docs.map(d => ({ id: d.id, name: d.data().name || '' })).filter(x => x.name.toLowerCase().includes(q)).slice(0, 20); }
  };

  const downloads = { save: async ({ filename, data }) => {
    const blob = data instanceof Blob ? data : new Blob([data]);
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = filename; document.body.appendChild(a); a.click();
    setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 2000); } };

  const assets = storage && {
    upload: async f => { const path = 'assets/' + Date.now().toString(36) + '_' + String(f.name || 'file').replace(/[^\w.\-]+/g, '_'); const r = storage.ref(path);
      await r.put(f, { contentType: f.type || 'application/octet-stream' }); return { id: path, url: await r.getDownloadURL(), sizeBytes: f.size, contentType: f.type }; },
    delete: async id => storage.ref(id).delete(),
    list: async () => { const L = await storage.ref('assets').listAll(); return { assets: await Promise.all(L.items.map(async r => ({ id: r.fullPath, url: await r.getDownloadURL() }))) }; }
  };

  // ---- AI adapter: one interface for every provider ----
  // Each model size (quick, default, complex) can use a different provider: for example DeepSeek for quick work,
  // Claude for deep work, Grok where chosen, and an offline model when there is no internet.
  const AIC = C.ai || {};
  const BASE = { anthropic: 'https://api.anthropic.com', claude: 'https://api.anthropic.com', openai: 'https://api.openai.com/v1', grok: 'https://api.x.ai/v1', xai: 'https://api.x.ai/v1', deepseek: 'https://api.deepseek.com', gemini: 'https://generativelanguage.googleapis.com/v1beta/openai', mistral: 'https://api.mistral.ai/v1', ollama: 'http://localhost:11434/v1', lmstudio: 'http://localhost:1234/v1' };
  function route(tier) { // returns {provider, model, baseUrl}
    const t = (AIC.tiers || {})[tier || 'default'] || (AIC.tiers || {}).default;
    if (t) return { provider: t.provider, model: t.model, baseUrl: t.baseUrl || BASE[t.provider] };
    return { provider: AIC.provider, model: (AIC.models || {})[tier || 'default'] || (AIC.models || {}).default, baseUrl: AIC.baseUrl || BASE[AIC.provider] };
  }
  function aiKey(provider) { if (provider === 'ollama' || provider === 'lmstudio') return ''; const k0 = 'fc_ai_key_' + provider; let k = localStorage.getItem(k0) || (provider === AIC.provider ? localStorage.getItem('fc_ai_key') : '');
    if (!k) { k = prompt('Paste the ' + provider + ' API key for this PC. It stays on this PC only.'); if (k) localStorage.setItem(k0, k.trim()); } return k || ''; }
  window.fcSetAIKey = (provider, k) => k ? localStorage.setItem('fc_ai_key_' + provider, k) : localStorage.removeItem('fc_ai_key_' + provider);
  const toB64 = b => new Promise(r => { const fr = new FileReader(); fr.onload = () => r(String(fr.result)); fr.readAsDataURL(b); });
  async function callModel(R, prompt, o) {
    const tools = o.tools || []; const imgs = await Promise.all((o.images || []).map(toB64));
    let text = '', inT = 0, outT = 0;
    if (R.provider === 'anthropic' || R.provider === 'claude') {
      const content = imgs.map(u => ({ type: 'image', source: { type: 'base64', media_type: u.slice(5, u.indexOf(';')), data: u.split(',')[1] } })).concat([{ type: 'text', text: prompt }]);
      const msgs = [{ role: 'user', content }];
      for (let turn = 0; turn < 10; turn++) {
        const r = await fetch(R.baseUrl + '/v1/messages', { method: 'POST', headers: { 'content-type': 'application/json', 'x-api-key': aiKey(R.provider), 'anthropic-version': '2023-06-01', 'anthropic-dangerous-direct-browser-access': 'true' },
          body: JSON.stringify({ model: R.model, max_tokens: 4096, messages: msgs, tools: tools.length ? tools.map(t => ({ name: t.name, description: t.description, input_schema: t.inputSchema })) : undefined }) });
        const j = await r.json(); if (!r.ok) throw new Error((j.error && j.error.message) || 'AI request failed');
        if (j.usage) { inT += j.usage.input_tokens || 0; outT += j.usage.output_tokens || 0; }
        text = j.content.filter(b => b.type === 'text').map(b => b.text).join('\n') || text; if (o.onText) o.onText({ text });
        const calls = j.content.filter(b => b.type === 'tool_use'); if (!calls.length) break;
        msgs.push({ role: 'assistant', content: j.content });
        msgs.push({ role: 'user', content: await Promise.all(calls.map(async c => { const t = tools.find(x => x.name === c.name); let out; try { out = t ? await t.execute(c.input || {}) : 'Unknown tool'; } catch (e) { out = 'Error: ' + e.message; } return { type: 'tool_result', tool_use_id: c.id, content: typeof out === 'string' ? out : JSON.stringify(out) }; })) });
      }
    } else { // OpenAI-compatible: Grok (xAI), DeepSeek, OpenAI, Gemini, Mistral, Ollama, LM Studio
      const msgs = [{ role: 'user', content: imgs.length ? [{ type: 'text', text: prompt }].concat(imgs.map(u => ({ type: 'image_url', image_url: { url: u } }))) : prompt }];
      const k = aiKey(R.provider);
      for (let turn = 0; turn < 10; turn++) {
        const r = await fetch(R.baseUrl + '/chat/completions', { method: 'POST', headers: Object.assign({ 'content-type': 'application/json' }, k ? { authorization: 'Bearer ' + k } : {}),
          body: JSON.stringify({ model: R.model, messages: msgs, tools: tools.length ? tools.map(t => ({ type: 'function', function: { name: t.name, description: t.description, parameters: t.inputSchema } })) : undefined }) });
        const j = await r.json(); if (!r.ok) throw new Error((j.error && (j.error.message || j.error)) || 'AI request failed');
        if (j.usage) { inT += j.usage.prompt_tokens || 0; outT += j.usage.completion_tokens || 0; }
        const m = j.choices[0].message; text = m.content || text; if (o.onText) o.onText({ text });
        if (!m.tool_calls || !m.tool_calls.length) break;
        msgs.push(m);
        for (const c of m.tool_calls) { const t = tools.find(x => x.name === c.function.name); let out; try { out = t ? await t.execute(JSON.parse(c.function.arguments || '{}')) : 'Unknown tool'; } catch (e) { out = 'Error: ' + e.message; }
          msgs.push({ role: 'tool', tool_call_id: c.id, content: typeof out === 'string' ? out : JSON.stringify(out) }); }
      }
    }
    return { text, usage: { input_tokens: inT, output_tokens: outT, provider: R.provider, model: R.model } };
  }
  async function sample(prompt, o) {
    o = o || {}; const R = route(o.modelTier);
    try { return await callModel(R, prompt, o); }
    catch (e) { // no internet or provider down: fall back to the offline model if one is set
      const off = (AIC.tiers || {}).offline; if (off && R.provider !== off.provider) return callModel({ provider: off.provider, model: off.model, baseUrl: off.baseUrl || BASE[off.provider] }, prompt, o);
      throw e; }
  }
  sample.json = async (p, o) => { const r = await sample(p + '\nReturn only JSON.', o); const t = r.text; const out = JSON.parse(t.slice(t.indexOf('{'), t.lastIndexOf('}') + 1)); Object.defineProperty(out, '__usage', { value: r.usage, enumerable: false }); return out; };

  window.claude = { use: async name => {
    if (name === 'downloads') return downloads;
    await ready;
    if (name === 'db') return db;
    if (name === 'user') return userCap;
    if (name === 'assets') return assets || null;
    if (name === 'sample') return (AIC.provider || AIC.tiers) ? sample : null; // no provider: the app runs in no-AI mode
    return null; } };
})();
