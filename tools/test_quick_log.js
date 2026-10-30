const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:950}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
const clk=async s=>{await p.$eval(s,e=>e.click());await p.waitForTimeout(350);};
await p.goto('file:///tmp/pt/index.html#today');await p.waitForTimeout(3000);
await clk('[data-qlopen]');
await p.fill('form[data-f=ql] input[name=t]','Call surveyor');await clk('form[data-f=ql] button');
for(const [t,fill] of [['money',async()=>{await p.fill('form[data-f=ql] input[name=amount]','50000');}],['metric',async()=>{await p.fill('form[data-f=ql] input[name=value]','4');}],['note',async()=>{await p.fill('form[data-f=ql] input[name=t]','Use 40% deposits');await p.check('form[data-f=ql] input[name=mem]');}],['lead',async()=>{await p.fill('form[data-f=ql] input[name=client]','Mukasa');}],['diary',async()=>{await p.fill('form[data-f=ql] textarea[name=work]','Slab cast');}]]){
 await clk('[data-qlopen]');await clk('[data-qlt='+t+']');await fill();await clk('form[data-f=ql] button');console.log(t,await p.textContent('#status'));}
await clk('[data-qlopen]');await clk('[data-qlt=reg]');await p.screenshot({path:'ql.png'});console.log('reg links',await p.$$eval('[data-qlgo]',x=>x.length));
await p.evaluate(()=>location.hash='team');await p.waitForTimeout(300);console.log('task visible',await p.evaluate(()=>document.querySelector('#view').innerText.includes('Call surveyor')));
await p.evaluate(()=>location.hash='learn');await p.waitForTimeout(300);console.log('decision visible',await p.evaluate(()=>document.querySelector('#view').innerText.includes('Use 40% deposits')));
console.log('ERR',JSON.stringify(errs));await b.close();})();
