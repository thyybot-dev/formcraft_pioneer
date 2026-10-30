const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:950}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
const clk=async s=>{await p.$eval(s,e=>e.click());await p.waitForTimeout(350);};
await p.goto('file:///tmp/pt/index.html#approvals');await p.waitForTimeout(3000);await clk('[data-apt=pros]');
for(const [n,a,ph,pr] of [['Akello Gulu','Gulu, Amuru','0701000001','Physical or town planner'],['Okot Lira','Lira','0701000002','Physical or town planner'],['National Planners Ltd','Nationwide','0701000003','Physical or town planner'],['Kato Kampala','Kampala, Wakiso','0701000004','Physical or town planner'],['Opio Welder','Gulu','0701000005','Welder or metal fabricator']]){
 await p.fill('form[data-f=pro] input[name=name]',n);await p.selectOption('form[data-f=pro] select[name=prof]',pr);await p.fill('form[data-f=pro] input[name=areas]',a);await p.fill('form[data-f=pro] input[name=phone]',ph);await clk('form[data-f=pro] button');}
await p.selectOption('form[data-f=proq] select[name=prof]','Physical or town planner');await p.fill('form[data-f=proq] input[name=place]','Gulu');await clk('form[data-f=proq] button');
console.log('internal order',await p.$$eval('#view tbody tr td:first-child b',x=>x.map(e=>e.innerText)));
for(let i=0;i<3;i++){const s=(await p.$$('[data-prostat]'))[i];await s.selectOption('Confirmed');await p.waitForTimeout(300);}await p.selectOption('form[data-f=proq] select[name=prof]','All');await p.fill('form[data-f=proq] input[name=place]','');await clk('form[data-f=proq] button');for(let i=0;i<5;i++){const s=(await p.$$('[data-prostat]'))[i];if(s){await s.selectOption('Confirmed');await p.waitForTimeout(300);}}
await clk('[data-apt=web]');await p.selectOption('form[data-f=proq] select[name=prof]','Trades and crafts');await p.fill('form[data-f=proq] input[name=place]','Gulu');await clk('form[data-f=proq] button');
console.log('web trades gulu',await p.evaluate(()=>[...document.querySelectorAll('#view .grid .card b')].map(e=>e.innerText)));
console.log('ERR',JSON.stringify(errs));await b.close();})();
