"""Copies command-centre/ai-layers.js (with the agent rulebooks from rulebooks/agents/*.md) into command-centre/index.html,
then rebuilds the standalone app. Run after editing either, then run the AI checks:
  python3 tools/sync_ai_layers.py && sh tools/check_syntax.sh && node tools/test_ai_layers.js && node tools/test_mcp_layers.js"""
import os, re, json, glob, subprocess, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
books = {os.path.basename(f)[:-3]: open(f, encoding='utf-8').read() for f in sorted(glob.glob(f'{R}/rulebooks/agents/*.md'))}
block = open(f'{R}/command-centre/ai-layers.js', encoding='utf-8').read()
block = re.sub(r'/\*RULEBOOKS\*/.*?/\*END RULEBOOKS\*/', lambda m: '/*RULEBOOKS*/' + json.dumps(books, ensure_ascii=False) + '/*END RULEBOOKS*/', block, flags=re.S)
if '</script' in block.lower(): sys.exit('ai-layers.js must not contain a closing script tag')
p = f'{R}/command-centre/index.html'; s = open(p, encoding='utf-8').read()
A, Z = '// ==== AI LAYERS ====', '// ==== END AI LAYERS ===='
if A in s:
    i = s.index(A); j = s.index(Z, i) + len(Z) + 1
    s = s[:i] + block.strip() + '\n' + s[j:]
else:  # first sync: retire the old unguarded askAI, add the access filters, and place the block after agentTools()
    i = s.index('async function askAI(q){'); j = s.index('function aiPanel(', i); s = s[:i] + s[j:]
    i = s.index('function agentTools(){'); j = s.index('\nfunction', i + 10) + 1
    s = s[:j] + block.strip() + '\n' + s[j:]
    reps = [("<select data-agsel=\"1\" style=\"font-size:12px\">'+AGS().map(", "<select data-agsel=\"1\" style=\"font-size:12px\">'+AGS().filter(a=>agentOk(a[0])).map("),
            ("memory:S.memory.filter(m=>hit(m.text))", "memory:S.memory.filter(m=>!m.archived&&agentOk(m.scope||'general')&&hit(m.text))"),
            ("exchanges:S.ailog.filter(x=>hit(x.q+' '+x.a))", "exchanges:S.ailog.filter(x=>agentOk(x.agent||'general')&&hit(x.q+' '+x.a))"),
            ("h+='<h2>Long-term memory</h2>", "h+=aiChecksHTML();h+='<h2>Long-term memory</h2>"),
            ("if(k==='aiprice'){", "if(k==='aiguard'){w(()=>db.doc('meta/settings').set(Object.assign({},S.settings,{aiMask:d.aiMask==='off'?'off':'on',aiCap:Math.max(0,Number(d.aiCap)||0)})));return;}\n if(k==='aiprice'){")]
    for a, b in reps:
        if s.count(a) != 1: sys.exit('patch anchor not found exactly once: ' + a[:60])
        s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s)
print('synced AI layers and', len(books), 'rulebooks into command-centre/index.html')
subprocess.run([sys.executable, f'{R}/tools/build_standalone.py'], check=True)
