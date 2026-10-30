const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:950}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file:///tmp/pt/index.html#cplan');await p.waitForTimeout(3000);
console.log(await p.evaluate(()=>document.querySelector('.note').innerText.slice(0,200)));
await p.$eval('[data-cptut]',e=>e.click());await p.waitForTimeout(6000);
console.log(await p.evaluate(()=>[...document.querySelectorAll('.kpi')].slice(0,1).map(e=>e.innerText.replace(/\s+/g,' '))));
console.log('ERR',JSON.stringify(errs));await b.close();})();
