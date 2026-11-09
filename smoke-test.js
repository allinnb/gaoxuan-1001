const assert=require('assert');
const fs=require('fs');
const {JSDOM,VirtualConsole}=require('jsdom');
const html=fs.readFileSync(__dirname+'/index.html','utf8');
const errors=[];
const vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e));vc.on('error',e=>errors.push(e));
const dom=new JSDOM(html,{runScripts:'dangerously',resources:'usable',url:'https://example.test/',virtualConsole:vc,beforeParse(w){w.HTMLElement.prototype.scrollIntoView=function(){};w.alert=m=>errors.push(new Error('alert: '+m));w.HTMLCanvasElement.prototype.getContext=()=>({fillStyle:'',strokeStyle:'',lineWidth:0,textAlign:'',font:'',fillRect(){},strokeRect(){},fillText(){}});}});
const w=dom.window,d=w.document;
function submit(date,time,cityValue,cityLabel){
 d.getElementById('solarDate').value=date;d.getElementById('birthTime').value=time;
 const city=d.getElementById('birthCity');city.value=cityValue;city.dispatchEvent(new w.Event('change',{bubbles:true}));
 d.getElementById('birthForm').dispatchEvent(new w.Event('submit',{bubbles:true,cancelable:true}));
 assert.strictEqual(errors.length,0,`${cityLabel} 提交出现 JS 错误: ${errors.map(String).join('; ')}`);
 assert(d.getElementById('summary').classList.contains('show'),`${cityLabel} 总览未显示`);
 assert.strictEqual(d.querySelectorAll('#freePack .card').length,4,`${cityLabel} 简版卡片不完整`);
 assert.strictEqual(d.querySelectorAll('#cards .card').length,9,`${cityLabel} 规则结果卡片不完整`);
 assert(d.getElementById('cards').textContent.includes('稱骨算命'),`${cityLabel} 称骨卡未渲染`);
 console.log(`✓ ${date} ${time} ${cityLabel}：无 JS 错误，13 张结果卡全部渲染`);
}
submit('1980-06-06','12:00','121.55','寧波');
submit('2000-02-04','21:00','116.407','北京');
const headings=[...d.querySelectorAll('h2,h3')].map(x=>x.textContent);assert(!headings.some(x=>x.includes('小六壬')||x.includes('萬能男女算命套路')),'已移除界面模块仍存在');
console.log('界面冒烟测试全部通过。');
dom.window.close();
