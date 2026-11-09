const assert=require('assert'),fs=require('fs'),vm=require('vm');
const html=fs.readFileSync(__dirname+'/index.html','utf8');
const m=html.match(/<script id="calendar-data" type="application\/json">([\s\S]*?)<\/script>[\s\S]*?<script id="app-core">([\s\S]*?)<\/script>/);
const ctx={console,CALENDAR_DATA:JSON.parse(m[1]),Date};vm.createContext(ctx);vm.runInContext(m[2],ctx);const C=ctx.GX;
const nb=C.trueSolar('1980-06-06','12:00',121.55);assert.strictEqual(nb.time,'12:08');assert.strictEqual(nb.date,'1980-06-06');
assert(html.includes('寧波:121.55'),'城市表缺少寧波');assert(html.includes('請選擇城市或輸入有效經度'),'缺少經度驗證');
const copy=JSON.parse(fs.readFileSync(__dirname+'/copy.json','utf8'));assert.strictEqual(Object.keys(copy).length,286);
for(const [key,row] of Object.entries(copy)){for(const f of ['tag','keywords','plain','tip','quote'])assert(row[f]&&row[f]!=='nan',`${key} 缺 ${f}`);assert(!Object.values(row).join('').includes('【待核】'),`${key} 含待核`)}
assert(html.includes('搞玄-${tag}.png'),'分享檔名未使用人設名');assert(html.includes("ratio==='1:1'?1080:1920"),'未提供 1:1 與 9:16 分享卡');
assert(!html.includes('古書資料庫'),'仍有舊資訊架構名稱');assert(!html.includes('【待核】'),'公開頁面含待核');
console.log('✓ 寧波、經度驗證、286 筆五層文案、雙比例分享卡與公開文案檢查全部通過');
