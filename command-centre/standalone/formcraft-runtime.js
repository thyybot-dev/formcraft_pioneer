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
  const AIC = C.ai || {};
  function aiKey() { if (AIC.provider === 'ollama' || AIC.provider === 'lmstudio') return ''; let k = localStorage.getItem('fc_ai_key');
    if (!k) { k = prompt('Paste the ' + (AIC.provider || 'AI') + ' API key for this PC. It stays on this PC only.'); if (k) localStorage.setItem('fc_ai_key', k.trim()); } return k || ''; }
  window.fcSetAIKey = k => k ? localStorage.setItem('fc_ai_key', k) : localStorage.removeItem('fc_ai_key');
  const model = tier => (AIC.models || {})[tier || 'default'] || (AIC.models || {}).default;
  const toB64 = b => new Promise(r => { const fr = new FileReader(); fr.onload = () => r(String(fr.result)); fr.readAsDataURL(b); });
  async function sample(prompt, o) {
    o = o || {}; const tools = o.tools || []; const imgs = await Promise.all((o.images || []).map(toB64));
    let text = '';
    if (AIC.provider === 'anthropic') {
      const content = imgs.map(u => ({ type: 'image', source: { type: 'base64', media_type: u.slice(5, u.indexOf(';')), data: u.split(',')[1] } })).concat([{ type: 'text', text: prompt }]);
      const msgs = [{ role: 'user', content }];
      for (let turn = 0; turn < 10; turn++) {
        const r = await fetch((AIC.baseUrl || 'https://api.anthropic.com') + '/v1/messages', { method: 'POST', headers: { 'content-type': 'application/json', 'x-api-key': aiKey(), 'anthropic-version': '2023-06-01', 'anthropic-dangerous-direct-browser-access': 'true' },
          body: JSON.stringify({ model: model(o.modelTier), max_tokens: 4096, messages: msgs, tools: tools.length ? tools.map(t => ({ name: t.name, description: t.description, input_schema: t.inputSchema })) : undefined }) });
        const j = await r.json(); if (!r.ok) throw new Error((j.error && j.error.message) || 'AI request failed');
        text = j.content.filter(b => b.type === 'text').map(b => b.text).join('\n') || text; if (o.onText) o.onText({ text });
        const calls = j.content.filter(b => b.type === 'tool_use'); if (!calls.length) break;
        msgs.push({ role: 'assistant', content: j.content });
        msgs.push({ role: 'user', content: await Promise.all(calls.map(async c => { const t = tools.find(x => x.name === c.name); let out; try { out = t ? await t.execute(c.input || {}) : 'Unknown tool'; } catch (e) { out = 'Error: ' + e.message; } return { type: 'tool_result', tool_use_id: c.id, content: typeof out === 'string' ? out : JSON.stringify(out) }; })) });
      }
    } else { // OpenAI-compatible: OpenAI, Gemini (OpenAI endpoint), Mistral, Ollama, LM Studio
      const base = AIC.baseUrl || (AIC.provider === 'ollama' ? 'http://localhost:11434/v1' : AIC.provider === 'lmstudio' ? 'http://localhost:1234/v1' : 'https://api.openai.com/v1');
      const msgs = [{ role: 'user', content: imgs.length ? [{ type: 'text', text: prompt }].concat(imgs.map(u => ({ type: 'image_url', image_url: { url: u } }))) : prompt }];
      const k = aiKey();
      for (let turn = 0; turn < 10; turn++) {
        const r = await fetch(base + '/chat/completions', { method: 'POST', headers: Object.assign({ 'content-type': 'application/json' }, k ? { authorization: 'Bearer ' + k } : {}),
          body: JSON.stringify({ model: model(o.modelTier), messages: msgs, tools: tools.length ? tools.map(t => ({ type: 'function', function: { name: t.name, description: t.description, parameters: t.inputSchema } })) : undefined }) });
        const j = await r.json(); if (!r.ok) throw new Error((j.error && (j.error.message || j.error)) || 'AI request failed');
        const m = j.choices[0].message; text = m.content || text; if (o.onText) o.onText({ text });
        if (!m.tool_calls || !m.tool_calls.length) break;
        msgs.push(m);
        for (const c of m.tool_calls) { const t = tools.find(x => x.name === c.function.name); let out; try { out = t ? await t.execute(JSON.parse(c.function.arguments || '{}')) : 'Unknown tool'; } catch (e) { out = 'Error: ' + e.message; }
          msgs.push({ role: 'tool', tool_call_id: c.id, content: typeof out === 'string' ? out : JSON.stringify(out) }); }
      }
    }
    return { text };
  }
  sample.json = async p => { const t = (await sample(p + '\nReturn only JSON.')).text; return JSON.parse(t.slice(t.indexOf('{'), t.lastIndexOf('}') + 1)); };

  window.claude = { use: async name => {
    if (name === 'downloads') return downloads;
    await ready;
    if (name === 'db') return db;
    if (name === 'user') return userCap;
    if (name === 'assets') return assets || null;
    if (name === 'sample') return AIC.provider ? sample : null; // no provider: the app runs in no-AI mode
    return null; } };
})();
