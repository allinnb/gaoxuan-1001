const assert=require('assert'),fs=require('fs'),vm=require('vm');
const html=fs.readFileSync(__dirname+'/index.html','utf8');
const m=html.match(/<script id="calendar-data" type="application\/json">([\s\S]*?)<\/script>[\s\S]*?<script id="app-core">([\s\S]*?)<\/script>/);
const ctx={console,CALENDAR_DATA:JSON.parse(m[1]),Date};vm.createContext(ctx);vm.runInContext(m[2],ctx);const C=ctx.GX;
let n=0;function eq(a,b,s){n++;assert.deepStrictEqual(JSON.parse(JSON.stringify(a)),b,s);console.log('✓ '+s)}
eq(C.trueSolarTime('1980-06-06','12:00',121.55).time,'12:08','寧波真太陽時');
eq(C.trueSolarTime('2000-01-01','12:00',87.6).time,'09:47','烏魯木齊真太陽時');
let p=C.fourPillars('1980-06-06','12:00',121.55);eq(p.hourBranch,'午','真太陽時午時');eq(p.monthPillar,'壬午','五虎遁月柱');eq(p.hourPillar,'壬午','五鼠遁時柱');
eq(C.hourPart('12:00'),'中','午時中');eq(C.hourPart('23:20'),'初','子時初');eq(C.hourPart('00:30'),'末','子時末');
eq(C.baBai(5,1),true,'巳年正月犯八敗');eq(C.baBai(8,6),true,'申年六月犯八敗');
eq(C.guGua(0,['寅','戌','午']),{孤辰:true,寡宿:true},'子年見寅戌帶孤寡');
eq(C.ironBroom(8,1,'男','巳'),{犯:true,方向:'往外掃'},'申年正月男命鐵掃帚');
eq(C.nineStar(14,'男'),'太陽','男命虛歲十四太陽');eq(C.nineStar(16,'女'),'太陽','女命虛歲十六太陽');
console.log(`\nRULES-v2 全部 ${n} 項斷言通過。`);
