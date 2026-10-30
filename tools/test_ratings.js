const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:950}});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('dialog',d=>d.accept('Sarah'));
const clk=async s=>{await p.$eval(s,e=>e.click());await p.waitForTimeout(350);};
await p.goto('file:///tmp/pt/index2.html#approvals');await p.waitForTimeout(3000);
await clk('[data-apt=pros]');
await p.fill('form[data-f=pro] input[name=name]','Peter Okello');await p.fill('form[data-f=pro] input[name=phone]','0701 555777');await clk('form[data-f=pro] button');
await p.selectOption('[data-prostat]','Confirmed');await p.waitForTimeout(300);
await p.click('[data-proref]');await p.waitForTimeout(400);
for(let i=0;i<3;i++){await clk('[data-prorate]');await p.check('form[data-f=prorev] input[value=Fast]');await p.fill('form[data-f=prorev] input[name=comment]','Approved in 5 weeks '+i);await p.fill('form[data-f=prorev] input[name=who]','Sarah');if(i===0){const o=await p.$$eval('form[data-f=prorev] select[name=ref] option',x=>x.map(e=>e.value));if(o[1])await p.selectOption('form[data-f=prorev] select[name=ref]',o[1]);}await clk('form[data-f=prorev] button');}
await clk('[data-apt=contrib]');console.log('pending reviews',await p.$$eval('[data-capply]',x=>x.length));
for(let i=0;i<3;i++)await clk('[data-capply]');
await clk('[data-apt=pros]');console.log('table',await p.evaluate(()=>document.querySelector('#view tbody').innerText.replace(/\s+/g,' ').slice(0,200)));
await clk('[data-apt=web]');console.log('web',await p.evaluate(()=>{const t=document.querySelector('#view').innerText;return [t.includes('from 3 people referred here'),t.includes('Fast · 3')];}));await p.screenshot({path:'rev.png',fullPage:true});
console.log('ERR',JSON.stringify(errs));await b.close();})();
