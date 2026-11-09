const {spawnSync}=require('child_process');
const zones=['Asia/Shanghai','UTC','America/Los_Angeles'];
for(const tz of zones){
 console.log(`\n===== TZ=${tz} =====`);
 const r=spawnSync(process.execPath,['test.js'],{cwd:__dirname,env:{...process.env,TZ:tz},stdio:'inherit'});
 if(r.status!==0)process.exit(r.status||1);
}
console.log('\n三個時區全部通過。');
