const assert=require('assert'),fs=require('fs'),{webcrypto}=require('crypto'),{JSDOM}=require('jsdom'),jsQR=require('jsqr'),{PNG}=require('pngjs');
const html=fs.readFileSync(__dirname+'/index.html','utf8');
assert(!html.includes('"wanneng"'),'source-content 不得含 wanneng');
assert(html.includes('monthPillar}月'),'分享卡必须使用 monthPillar');
assert(!html.includes('function drawQR(ctx,text,x,y,size){let n=29,seed='),'不得保留杂凑二维码');
const png=PNG.sync.read(fs.readFileSync(__dirname+'/share-card-sample.png')),code=jsQR(new Uint8ClampedArray(png.data),png.width,png.height,{inversionAttempts:'attemptBoth'});assert(code,'分享卡二维码应可解码');assert.strictEqual(code.data,'https://allinnb.github.io/gaoxuan-1001/');
console.log('✓ 分享卡 QR 可由 jsQR 解码为网站 URL');
const dom=new JSDOM(html,{runScripts:'dangerously',url:'https://example.test/',beforeParse(w){Object.defineProperty(w,'crypto',{value:webcrypto});w.HTMLElement.prototype.scrollIntoView=()=>{};w.alert=()=>{};w.HTMLCanvasElement.prototype.getContext=()=>({fillRect(){},strokeRect(){},fillText(){},beginPath(){},moveTo(){},lineTo(){},stroke(){},fill(){},arc(){},save(){},restore(){},translate(){},rotate(){}})}});const W=dom.window;
(async()=>{const K=Uint8Array.from([1,2,3,4,5,6,7,8,9,10]),birth='1980-06-06|午|男',other='2000-02-04|亥|男',code=await W.makeUnlockCode(K,birth),payload=await W.encryptFullPayload(K,{ok:'完整版'}),good=await W.decryptFullPayload(code,birth,payload);assert.strictEqual(good.ok,'完整版');await assert.rejects(()=>W.decryptFullPayload(code,other,payload));let bad=code.slice(0,-1)+(code.at(-1)==='A'?'B':'A');await assert.rejects(()=>W.decryptFullPayload(bad,birth,payload));console.log('✓ 本人生辰解锁成功、他人生辰失败、改一字失败');dom.window.close()})().catch(e=>{console.error(e);process.exit(1)});
