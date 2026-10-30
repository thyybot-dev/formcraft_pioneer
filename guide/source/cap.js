const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:900},deviceScaleFactor:1.5,timezoneId:'Africa/Nairobi'});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file:///tmp/guide/index.html#today');await p.waitForTimeout(3500);
const keys=await p.evaluate(()=>[...document.querySelectorAll('#nav a')].map(a=>[a.getAttribute('href').slice(1),a.innerText.trim()]));
const out={};
for(const [k,n] of keys){await p.evaluate(x=>location.hash=x,k);await p.waitForTimeout(k==='studio'?1200:350);
 out[k]={name:n,text:await p.evaluate(()=>document.querySelector('#view').innerText.slice(0,2500))};
 await p.screenshot({path:'shots/'+k+'.png'});}
fs.writeFileSync('pages.json',JSON.stringify(out,null,1));console.log(keys.length,'ERR',JSON.stringify(errs.slice(0,5)));await b.close();})();
