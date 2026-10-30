const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:950}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file:///tmp/pt/index6.html#access');await p.waitForTimeout(3000);
const n=await p.$$eval('form[data-f=tabs]',x=>x.length);console.log('people with tab control',n);
if(n){await p.$eval('details',d=>d.open=true);const boxes=await p.$$('form[data-f=tabs] input[type=checkbox]');for(const bx of boxes)await bx.evaluate(e=>e.checked=false);await p.check('form[data-f=tabs] input[name=t_daily]');await p.check('form[data-f=tabs] input[name=t_cplan]');await p.$eval('form[data-f=tabs] button:not([name])',e=>e.click());await p.waitForTimeout(500);
console.log(await p.evaluate(()=>document.querySelector('details summary').innerText));}
console.log('ERR',JSON.stringify(errs));await b.close();})();
