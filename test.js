const assert = require('assert');
const fs = require('fs');
const vm = require('vm');
const html = fs.readFileSync(__dirname + '/index.html','utf8');
const m = html.match(/<script id="calendar-data" type="application\/json">([\s\S]*?)<\/script>[\s\S]*?<script id="app-core">([\s\S]*?)<\/script>/);
assert(m, 'index.html 必须内嵌 calendar-data 与 app-core');
const ctx={console, CALENDAR_DATA:JSON.parse(m[1]), Date}; vm.createContext(ctx); vm.runInContext(m[2],ctx);
const C=ctx.GX;
function eq(actual, expected, label){assert.strictEqual(actual,expected,`${label}: ${actual} !== ${expected}`); console.log(`✓ ${label}: ${actual}`)}
const cases=[
 ['1980-06-06','12:00',{lunar:'庚申年四月廿四',year:'庚申',month:'午',day:'庚戌',nayin:'釵釧金',hour:'午'}],
 ['1990-01-15','08:00',{lunar:'己巳年十二月十九',year:'己巳',month:'丑',day:'庚辰',nayin:'白蠟金',hour:'辰'}],
 ['2025-06-30','12:00',{lunar:'乙巳年六月初六',year:'乙巳',month:'午',day:'庚午',nayin:'路旁土',hour:'午'}],
 ['2000-02-04','21:00',{lunar:'己卯年十二月廿九',year:'庚辰',month:'寅',day:'壬辰',nayin:'長流水',hour:'亥'}],
 ['1964-09-10','10:00',{lunar:'甲辰年八月初五',year:'甲辰',month:null,day:'壬戌',nayin:'大海水',hour:'巳'}],
 ['1990-01-03','12:00',{lunar:null,year:null,month:'子',day:null,nayin:null,hour:null}],
 ['2024-01-03','12:00',{lunar:null,year:null,month:'子',day:null,nayin:null,hour:null}]
];
for(const [d,t,e] of cases){const r=C.calculateSolar(d,t); if(e.lunar)eq(r.lunarText,e.lunar,`${d} 农历`); if(e.year)eq(r.yearPillar,e.year,`${d} 年柱`); if(e.month)eq(r.monthBranch,e.month,`${d} 月支`); if(e.day)eq(r.dayPillar,e.day,`${d} 日柱`); if(e.nayin)eq(r.dayNayin,e.nayin,`${d} 纳音`); if(e.hour)eq(r.hourBranch,e.hour,`${d} 时辰`)}
eq(C.boneAnimal(5,6).bone,'鼠骨','巳年六月骨格'); eq(C.boneAnimal(5,6).animal,'鳳凰','巳年六月禽兽');
eq(C.farm(5,6),'建','巳年六月田猪牛'); eq(C.star(5,6),'驛馬','巳年六月吉星');
eq(C.calamity('火',6).join('/'),'51/69','乙巳六月劫数'); eq(C.deathStage('火',6),'衰','乙巳六月断气');
eq(C.mansion('未',6),'井木犴','未月初六二十八宿'); eq(C.lifeLu('庚',10),'旺祿','庚年十月终身禄');
console.log(`\n全部 ${cases.length*6-1+8} 项验收断言通过。`);
