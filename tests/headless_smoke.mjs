// Headless smoke test for the ML4T study app — verifies the client JS runs with no errors
// and the core flows render. Requires the app server running (python3 serve.py) + Playwright.
//
// Run:
//   1) In one terminal:  cd projects/ml4t_prep/app && python3 serve.py
//   2) In another, from a folder that has playwright installed (e.g. the api-discovery skill's
//      scripts dir), OR after `npm i playwright && npx playwright install chromium`:
//        node headless_smoke.mjs
//
import { chromium } from 'playwright';
const URL = process.env.ML4T_URL || 'http://127.0.0.1:8765/';
const errs=[];
const b=await chromium.launch();
const pg=await b.newPage();
pg.on('console',m=>{if(m.type()==='error')errs.push('console:'+m.text());});
pg.on('pageerror',e=>errs.push('pageerror:'+e.message));
await pg.goto(URL,{waitUntil:'networkidle'}); await pg.waitForTimeout(600);
const r={};
await pg.click('#nav button[data-k="study"]'); await pg.waitForTimeout(300);   // don't depend on the saved last tab
r.studyCards=await pg.$$eval('#list .card',e=>e.length);
r.stat=await pg.$eval('#stat',e=>e.textContent).catch(()=>'');
for(const k of ['cards','quiz','notes','split','progress','tips','study']){
  await pg.click(`#nav button[data-k="${k}"]`); await pg.waitForTimeout(250);
  r[k]=await pg.$eval('#view',e=>e.innerHTML.length).catch(()=>0);
}
await pg.click('#nav button[data-k="quiz"]'); await pg.waitForTimeout(150);
await pg.click('#qstart'); await pg.waitForTimeout(300);
r.quizCards=await pg.$$eval('#quizarea .card',e=>e.length);
console.log(JSON.stringify({errors:errs,results:r},null,2));
const pass = errs.length===0 && r.studyCards>0 && r.quizCards>0;
console.log('RESULT:', pass?'PASS ✅':'FAIL ❌');
await b.close();
process.exit(pass?0:1);
