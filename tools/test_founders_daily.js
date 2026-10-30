const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:950},timezoneId:'Africa/Nairobi'});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file:///tmp/pt/index.html');await p.waitForTimeout(4000);
console.log('landing',await p.evaluate(()=>document.querySelector('#view h1,#view h2')&&document.querySelector('#view').innerText.slice(0,60)));
const keys=await p.evaluate(()=>[...document.querySelectorAll('#nav a')].map(a=>a.getAttribute('href').slice(1)));for(const k of keys){await p.evaluate(x=>location.hash=x,k);await p.waitForTimeout(60);}
await p.evaluate(()=>location.hash='daily');await p.waitForTimeout(300);
await p.click('[data-aiopen]');await p.waitForTimeout(200);
await p.fill('#aiq','plan my day').catch(()=>{});await p.click('form[data-f=ai] button[type=submit], form[data-f=ai] button:not([type])');await p.waitForTimeout(1200);
await p.evaluate(()=>location.hash='today');await p.waitForTimeout(200);await p.evaluate(()=>location.hash='daily');await p.waitForTimeout(400);
let n=await p.$$eval('#view [data-aiok]',x=>x.length);console.log('pending in daily',n);
await p.click('#view [data-aiok]');await p.waitForTimeout(500);await p.click('#view [data-aino]');await p.waitForTimeout(500);
n=await p.$$eval('#view [data-aiok]',x=>x.length);console.log('pending after',n);
await p.click('[data-dstart]');await p.waitForTimeout(400);
await p.fill('form[data-f=dqd] input[name=client]','Ggaba Apartments');await p.fill('form[data-f=dqd] input[name=value]','42000');await p.$eval('form[data-f=dqd] button',e=>e.click());await p.waitForTimeout(400);
await p.selectOption('[data-dstage]','Quote sent');await p.waitForTimeout(300);
await p.screenshot({path:'daily.png',fullPage:true});
console.log('ERR',JSON.stringify(errs));await b.close();})();
