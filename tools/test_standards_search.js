const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:950}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
const clk=async s=>{await p.$eval(s,e=>e.click());await p.waitForTimeout(350);};
await p.goto('file:///tmp/pt/index3.html#reg-standards');await p.waitForTimeout(3000);
// add a standard via register form
const f=await p.$('form[data-f^="reg"]');console.log('regform',!!f);
await p.evaluate(()=>location.hash='standards');await p.waitForTimeout(300);
await clk('[data-stdtab=digest]');
await p.selectOption('form[data-f=stddigest] select[name=kind]','Standard');await p.fill('form[data-f=stddigest] input[name=source]','KS 1234 Masonry');await p.selectOption('form[data-f=stddigest] select[name=juris]','Kenya');await p.fill('form[data-f=stddigest] textarea','5.2 Wall thickness ...');await clk('form[data-f=stddigest] button');await p.waitForTimeout(800);
await p.selectOption('form[data-f=stddigest] select[name=kind]','Law or regulation');await p.fill('form[data-f=stddigest] input[name=source]','Building Control Regulations 2020');await p.selectOption('form[data-f=stddigest] select[name=juris]','Uganda');await p.fill('form[data-f=stddigest] textarea','38. Boundary walls ...');await clk('form[data-f=stddigest] button');await p.waitForTimeout(800);
console.log('rows',await p.$$eval('[data-clpub]',x=>x.length));
console.log('copied text dropped',await p.evaluate(()=>!document.querySelector('#view').innerHTML.includes('COPIED WORDING')));
for(const b of await p.$$('[data-clpub]')){await b.evaluate(e=>e.click());await p.waitForTimeout(250);}
await clk('[data-stdtab=search]');await p.fill('form[data-f=stdtopic] input[name=q]','wall');await clk('form[data-f=stdtopic] button');
console.log('UG order',await p.evaluate(()=>[...document.querySelectorAll('#view h3')].map(h=>h.innerText)));
await p.selectOption('form[data-f=stdtopic] select[name=country]','Kenya');await clk('form[data-f=stdtopic] button');
console.log('KE order',await p.evaluate(()=>[...document.querySelectorAll('#view h3')].map(h=>h.innerText)));
await p.fill('form[data-f=stdtopic] input[name=q]','roofing');await clk('form[data-f=stdtopic] button');console.log('roof',await p.evaluate(()=>document.querySelector('#view').innerText.includes('Roof pitch')));
await clk('[data-stdtab=web]');await p.fill('form[data-f=stdtopic] input[name=q]','walls');await clk('form[data-f=stdtopic] button');await p.screenshot({path:'stdsearch.png',fullPage:true});
await clk('[data-stdtab=list]');
console.log('ERR',JSON.stringify(errs));await b.close();})();
