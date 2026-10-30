const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:950}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
const clk=async s=>{await p.$eval(s,e=>e.click());await p.waitForTimeout(350);};
await p.goto('file:///tmp/pt/index2.html#approvals');await p.waitForTimeout(3000);
const keys=await p.evaluate(()=>[...document.querySelectorAll('#nav a')].map(a=>a.getAttribute('href').slice(1)));for(const k of keys){await p.evaluate(x=>location.hash=x,k);await p.waitForTimeout(50);}
await p.evaluate(()=>location.hash='approvals');await p.waitForTimeout(300);
await clk('[data-apseed]');await p.waitForTimeout(800);
console.log('auth rows',await p.$$eval('#view tbody tr',x=>x.length));
await clk('[data-apopen]:not([data-apopen=""])');
await p.fill('form[data-f=apauth] textarea[name=steps]','1. Submit plans\n2. Committee review');await p.fill('form[data-f=apauth] textarea[name=docs]','Land title, plans');await p.fill('form[data-f=apauth] textarea[name=fees]','To verify');await p.selectOption('form[data-f=apauth] select[name=pub]','Yes');await p.fill('form[data-f=apauth] input[name=verified]','2026-10-30');await clk('form[data-f=apauth] button');
await clk('[data-apopen=""]');
await clk('[data-apt=times]');
for(const [s,d] of [['2026-06-01','2026-07-15'],['2026-05-01','2026-06-20'],['2026-04-01','2026-05-01']]){await p.fill('form[data-f=aprep] input[name=submitted]',s);await p.fill('form[data-f=aprep] input[name=decided]',d);await p.selectOption('form[data-f=aprep] select[name=outcome]','Approved');await clk('form[data-f=aprep] button');}
await clk('[data-apt=pros]');
await p.fill('form[data-f=pro] input[name=name]','Peter Okello');await p.fill('form[data-f=pro] input[name=phone]','0701 555777');await p.fill('form[data-f=pro] input[name=areas]','Mukono');await clk('form[data-f=pro] button');
await p.fill('form[data-f=pro] input[name=name]','Peter O. duplicate');await p.fill('form[data-f=pro] input[name=phone]','+256 701 555777');await clk('form[data-f=pro] button');console.log('dup msg',await p.textContent('#status'));
await clk('[data-prosend]');console.log('confirm text has link',await p.$$eval('a[href^="https://wa.me/256701555777"]',x=>x.length));
await clk('[data-prosent]');await p.selectOption('[data-prostat]','Confirmed');await p.waitForTimeout(400);
await clk('[data-apt=contrib]');await p.fill('form[data-f=contribpaste] textarea','For Kira plans try Jane Nansubuga 0772123456. Took 45 days.');await clk('form[data-f=contribpaste] button');await p.waitForTimeout(800);
const n=await p.$$eval('[data-capply]',x=>x.length);console.log('contribs',n);
await clk('[data-capply]');await p.waitForTimeout(400);await clk('[data-capply]');await p.waitForTimeout(400);
await clk('[data-apt=web]');await p.screenshot({path:'apweb.png',fullPage:true});
console.log('web text',await p.evaluate(()=>{const t=document.querySelector('#view').innerText;return [t.includes('median of 45 days')||t.match(/median of \d+ days/)?.[0],t.includes('Peter Okello'),t.includes('Jane Nansubuga')];}));
await clk('[data-apt=pros]');console.log('pros rows',await p.evaluate(()=>document.querySelector('#view').innerText.includes('Jane Nansubuga')));
await p.evaluate(()=>location.hash='standards');await p.waitForTimeout(300);await clk('[data-stdweb="1"]');await p.screenshot({path:'stdweb.png'});
console.log('ERR',JSON.stringify(errs));await b.close();})();
