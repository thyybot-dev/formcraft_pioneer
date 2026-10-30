const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:900},deviceScaleFactor:1.6,timezoneId:'Africa/Nairobi'});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file:///tmp/guide/index.html#today');await p.waitForTimeout(3500);
const keys=await p.evaluate(()=>[...document.querySelectorAll('#nav a')].map(a=>a.getAttribute('href').slice(1)));
const box=await p.evaluate(()=>{const r=document.querySelector('#nav').getBoundingClientRect();return r.right;});
console.log('navright',box);
for(const k of keys){await p.evaluate(x=>location.hash=x,k);await p.waitForTimeout(k==='studio'?1200:400);
 await p.screenshot({path:'crop/'+k+'.png',clip:{x:box+4,y:8,width:1440-box-12,height:640}});}
// special states
await p.evaluate(()=>location.hash='standards');await p.waitForTimeout(400);
const si=await p.$('form[data-f] input[name=q], #stdq, input[placeholder*="topic"]'); if(si){await si.fill('walls');await si.press('Enter');await p.waitForTimeout(500);}
await p.screenshot({path:'crop/standards_search.png',clip:{x:box+4,y:8,width:1440-box-12,height:640}});
await p.evaluate(()=>location.hash='daily');await p.waitForTimeout(400);await p.screenshot({path:'full_daily.png'});
console.log('ERR',JSON.stringify(errs.slice(0,5)));await b.close();})();
