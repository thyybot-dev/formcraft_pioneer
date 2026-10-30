(function(){const store={};const subs=[];const fire=()=>setTimeout(()=>subs.forEach(f=>f()),0);window.__store=store;
const chk=v=>{if(Array.isArray(v)){if(v.some(Array.isArray))throw new Error('Nested arrays are not supported');v.forEach(chk);}else if(v&&typeof v==='object')Object.values(v).forEach(chk);else if(v===undefined)throw new Error('undefined');};
const clean=v=>JSON.parse(JSON.stringify(v));
const D=(c,i)=>({id:i,exists:!!(store[c]&&store[c][i]),data:()=>store[c]&&store[c][i]?clean(store[c][i]):undefined});
const fsI={settings(){},enablePersistence:()=>Promise.resolve(),
 collection:c=>({add:async d=>{chk(d);const i='m'+Math.random().toString(36).slice(2);(store[c]=store[c]||{})[i]=clean(d);fire();return {id:i};},get:async()=>({docs:Object.keys(store[c]||{}).map(i=>D(c,i))}),onSnapshot:(cb)=>{const f=()=>cb({docs:Object.keys(store[c]||{}).map(i=>D(c,i))});subs.push(f);f();return ()=>{};}}),
 doc:p=>{const [c,i]=p.split('/');return {set:async(d,o)=>{chk(d);store[c]=store[c]||{};store[c][i]=o&&o.merge?Object.assign({},store[c][i],clean(d)):clean(d);fire();},update:async d=>{chk(d);if(!store[c]||!store[c][i]){const e=new Error('no doc');e.code='not-found';throw e;}Object.assign(store[c][i],clean(d));fire();},delete:async()=>{delete store[c][i];fire();},get:async()=>D(c,i),onSnapshot:cb=>{const f=()=>cb(D(c,i));subs.push(f);f();return ()=>{};}};}};
let cb0=null,cur=null;const authI={onAuthStateChanged:f=>{cb0=f;setTimeout(()=>f(cur),10);},signInWithEmailAndPassword:async(e)=>{cur={uid:'u_emlyn',email:e,displayName:'Emlyn Atochon'};cb0(cur);},createUserWithEmailAndPassword:async()=>{},signInWithPopup:async()=>{},sendPasswordResetEmail:async()=>{},signOut:async()=>{cur=null;}};
window.firebase={initializeApp(){},auth:Object.assign(()=>authI,{GoogleAuthProvider:function(){}}),firestore:()=>fsI,storage:()=>({ref:p=>({put:async()=>{},getDownloadURL:async()=>'data:,x',delete:async()=>{},listAll:async()=>({items:[]})})})};
// mock OpenAI-compatible endpoint with one tool call round
let n=0;window.fetch=async(u,o)=>{const b=JSON.parse(o.body);window.__lastAI={u,auth:o.headers.authorization,model:b.model,tools:(b.tools||[]).length,msgs:b.messages.length};n++;
 const toolTurn=b.tools&&b.tools.length&&!b.messages.some(m=>m.role==='tool');
 const msg=toolTurn?{role:'assistant',content:null,tool_calls:[{id:'c1',type:'function',function:{name:'propose_actions',arguments:JSON.stringify({actions:[{type:'add_task',t:'Chase Ggaba deposit',due:'2026-11-02'}]})}}]}:{role:'assistant',content:'1. Chase the Ggaba deposit today (Emlyn).'};
 return {ok:true,json:async()=>({choices:[{message:msg}],usage:{prompt_tokens:1200,completion_tokens:300}})};};
})();
