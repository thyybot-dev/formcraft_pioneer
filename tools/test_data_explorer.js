const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:950}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file:///tmp/pt/index.html#dbx');await p.waitForTimeout(3000);
await p.$eval('[data-dbxc="targets"]',e=>e.click());await p.waitForTimeout(300);
console.log(await p.evaluate(()=>document.querySelector('#view').innerText.match(/\d+ of \d+ records/)[0]));
await p.$eval('[data-dbxs="target"]',e=>e.click());await p.waitForTimeout(300);await p.$eval('[data-dbxo]',e=>e.click());await p.waitForTimeout(300);
await p.$eval('[data-dbxexp=xlsx]',e=>e.click());await p.screenshot({path:'dbx.png'});
console.log('ERR',JSON.stringify(errs));await b.close();})();
