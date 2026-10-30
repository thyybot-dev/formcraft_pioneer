const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:950}});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push('console:'+m.text());});
await p.goto('http://localhost:8765/index.html');await p.waitForTimeout(800);
console.log('signin visible',await p.isVisible('#fc-signin'));await p.screenshot({path:'signin.png'});
await p.fill('#fc-e','emlyn@example.com');await p.fill('#fc-p','pw');await p.click('#fc-in');await p.waitForTimeout(3500);
console.log('signin gone',!(await p.isVisible('#fc-signin')),'status',await p.textContent('#status'));
const keys=await p.evaluate(()=>[...document.querySelectorAll('#nav a')].map(a=>a.getAttribute('href').slice(1)));console.log(keys.length,'pages');
for(const k of keys){await p.evaluate(x=>location.hash=x,k);await p.waitForTimeout(60);}
// write paths
await p.evaluate(()=>location.hash='onboard');await p.waitForTimeout(200);await p.fill('form[data-f=onb] input[name=client]','Nakato');await p.$eval('form[data-f=onb] button',e=>e.click());await p.waitForTimeout(400);
await p.evaluate(()=>location.hash='daily');await p.waitForTimeout(300);
await p.click('[data-aiopen]');await p.waitForTimeout(200);await p.fill('#aiq','plan my day');await p.$eval('form[data-f=ai] button:not([type])',e=>e.click());await p.waitForTimeout(1500);
console.log('ai',JSON.stringify(await p.evaluate(()=>window.__lastAI)));
console.log('pending docs',await p.evaluate(()=>Object.values(window.__store.pending||{}).length),'ailog',await p.evaluate(()=>Object.keys(window.__store.ailog||{}).length),'usage',await p.evaluate(()=>Object.keys(window.__store.usage||{})),'who',JSON.stringify(await p.evaluate(()=>window.__store.who)));
console.log('aiuse',await p.evaluate(()=>JSON.stringify(Object.values(window.__store.aiuse||{}).map(u=>[u.provider,u.tier,u.inTok,u.outTok,u.est,u.cost]))));console.log('collections',await p.evaluate(()=>Object.keys(window.__store).join(',')));
console.log('ERR',JSON.stringify(errs.slice(0,8)));await b.close();})();
