const {spawnSync}=require('child_process');
for(const tz of ['Asia/Shanghai','UTC','America/Los_Angeles']){
 console.log(`\n===== UI SMOKE TZ=${tz} =====`);
 const r=spawnSync(process.execPath,['smoke-test.js'],{cwd:__dirname,env:{...process.env,TZ:tz},stdio:'inherit'});
 if(r.status!==0)process.exit(r.status||1);
}
console.log('\n三個時區界面冒煙測試全部通過。');
