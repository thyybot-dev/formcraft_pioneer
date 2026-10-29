const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:950},timezoneId:'Africa/Nairobi',acceptDownloads:true});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file:///tmp/pt/index.html#today');await p.waitForTimeout(3500);
const keys=await p.evaluate(()=>[...document.querySelectorAll('#nav a')].map(a=>a.getAttribute('href').slice(1)));console.log(keys.length,'pages');
for(const k of keys){await p.evaluate(x=>location.hash=x,k);await p.waitForTimeout(120);const t=await p.evaluate(()=>document.querySelector('#view').innerText.length);if(t<30)console.log('EMPTY',k);}
for(const k of ['reg-standards','reg-recurring','reg-purchases','reg-rides','reg-accounts','reg-debts','reg-feedback','reg-toolstack','reg-subscribers']){await p.evaluate(x=>location.hash=x,k);await p.waitForTimeout(100);}
// actions
await p.evaluate(()=>location.hash='quotes');await p.waitForTimeout(200);await p.fill('form[data-f=enq] input[name=name]','Jane Diaspora');await p.fill('form[data-f=enq] input[name=area]','240');await p.click('form[data-f=enq] button');await p.waitForTimeout(300);await p.click('[data-enqmeet]');await p.waitForTimeout(300);await p.screenshot({path:'quotes.png'});
await p.evaluate(()=>location.hash='pricing');await p.waitForTimeout(200);await p.fill('form[data-f=pq] input[name=area]','200');await p.click('form[data-f=pq] button');await p.waitForTimeout(200);await p.screenshot({path:'pricing.png'});
await p.click('[data-pq2q]');await p.waitForTimeout(300);await p.fill('form[data-f=dq] input[name=client]','Jane');await p.click('form[data-f=dq] button[value=docx]');await p.waitForTimeout(300);
await p.evaluate(()=>location.hash='reach');await p.waitForTimeout(200);await p.fill('form[data-f=reach] input[name=place]','Germany');await p.selectOption('form[data-f=reach] select[name=type]','Tools or family sale');await p.click('form[data-f=reach] button');await p.waitForTimeout(150);await p.fill('form[data-f=reach] input[name=place]','Kampala');await p.selectOption('form[data-f=reach] select[name=type]','Project');await p.fill('form[data-f=reach] input[name=value]','5');await p.click('form[data-f=reach] button');await p.waitForTimeout(300);await p.screenshot({path:'reach.png'});
await p.evaluate(()=>location.hash='files');await p.waitForTimeout(200);await p.setInputFiles('#upfiles',{name:'poster.png',mimeType:'image/png',buffer:Buffer.from('iVBORw0KGgo=','base64')});await p.selectOption('#upfolder','Posters');await p.click('[data-upload]');await p.waitForTimeout(500);await p.screenshot({path:'files.png'});
await p.evaluate(()=>location.hash='licences');await p.waitForTimeout(200);await p.fill('form[data-f=lic] input[name=customer]','Studio X');await p.click('form[data-f=lic] button');await p.waitForTimeout(300);await p.click('[data-licexp]');await p.waitForTimeout(200);await p.screenshot({path:'lic.png'});
await p.evaluate(()=>location.hash='chat');await p.waitForTimeout(200);await p.fill('#chatin','Hello team');await p.press('#chatin','Enter');await p.waitForTimeout(300);
await p.evaluate(()=>location.hash='feas');await p.waitForTimeout(200);for(const [n,v] of [['name','Kira'],['area','600'],['land','200000000'],['cpm','2000000'],['units','6'],['price','450000000']])await p.fill('form[data-f=feas] [name='+n+']',v);await p.click('form[data-f=feas] button');await p.waitForTimeout(200);await p.screenshot({path:'feas.png'});
await p.evaluate(()=>location.hash='coach');await p.waitForTimeout(200);await p.screenshot({path:'coach.png'});
await p.evaluate(()=>location.hash='sim');await p.waitForTimeout(400);await p.screenshot({path:'sim.png'});
await p.evaluate(()=>location.hash='learn');await p.waitForTimeout(200);await p.click('[data-learnai]');await p.waitForTimeout(400);
await p.evaluate(()=>location.hash='reports');await p.waitForTimeout(200);await p.click('form[data-f=report] button:not([type])');await p.waitForTimeout(200);await p.click('[data-rx=xlsx]');await p.click('[data-rx=docx]');await p.waitForTimeout(200);
await p.evaluate(()=>location.hash='edge');await p.waitForTimeout(200);await p.screenshot({path:'edge.png'});
await p.evaluate(()=>location.hash='playbook');await p.waitForTimeout(200);
await p.evaluate(()=>location.hash='standards');await p.waitForTimeout(200);
await p.evaluate(()=>location.hash='outreach');await p.waitForTimeout(200);await p.screenshot({path:'out.png'});
await p.evaluate(()=>location.hash='money');await p.waitForTimeout(200);await p.screenshot({path:'money.png'});
console.log('ERR',JSON.stringify(errs));await b.close();})();
