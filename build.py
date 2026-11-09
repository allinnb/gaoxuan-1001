import json,base64,re,html,os,hashlib,secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from pathlib import Path
from opencc import OpenCC
cc=OpenCC('s2t')
p=Path(__file__).parent
cal=(p/'calendar-data.json').read_text('utf-8')
cover=base64.b64encode((p/'cover-01.jpg').read_bytes()).decode()
fu=base64.b64encode((p/'fu-04.jpg').read_bytes()).decode()
texts={}
for f in (p/'src').glob('src-*.txt'):
 key=f.stem[4:]
 if key.lower()=='wanneng': continue
 s=f.read_text('utf-8'); s=re.sub(r'\[[^\]]*https?://[^\]]*\]','',s); s=re.sub(r'https?://\S+','',s); texts[key]=cc.convert(s.strip())
content=json.dumps(texts,ensure_ascii=False).replace('</','<\\/')
rules=(p/'rules-v2/RULES-v2-part2.md').read_text('utf-8')
year_branch=dict(re.findall(r'^\*\*([子丑寅卯辰巳午未申酉戌亥])（[^）]+）\*\*\s*(.+)$',rules,re.M))
month_text={i+1:x for i,x in enumerate(re.findall(r'^- ((?:正|二|三|四|五|六|七|八|九|十|子|腊)月生人.+)$',rules,re.M)[:12])}
hour_text=dict(re.findall(r'^- ([子丑寅卯辰巳午未申酉戌亥])时生人[：:]\s*(.+)$',rules,re.M))
full={"nianzhu":json.loads((p/'rules-v2/alt/nianzhu.json').read_text('utf-8')),"yearBranch":year_branch,"month":month_text,"hour":hour_text,"hourParts":json.loads((p/'rules-v2/alt/110724.json').read_text('utf-8'))}
raw_k=os.getenv('GAOXUAN_MASTER_KEY','')
blob={}
if raw_k:
 k=base64.b32decode(re.sub(r'[^A-Z2-7]','',raw_k.upper())+'='*((8-len(re.sub(r'[^A-Z2-7]','',raw_k.upper()))%8)%8))
 if len(k)!=10: raise ValueError('GAOXUAN_MASTER_KEY must be 16 Base32 chars / 80 bit')
 key=HKDF(algorithm=hashes.SHA256(),length=32,salt=b'gaoxuan-1001-v2',info=b'full-package').derive(k)
 iv=secrets.token_bytes(12); ct=AESGCM(key).encrypt(iv,json.dumps(full,ensure_ascii=False).encode(),None)
 blob={"iv":base64.b64encode(iv).decode(),"ciphertext":base64.b64encode(ct).decode()}
full_blob=json.dumps(blob,separators=(',',':'))
# placeholders replaced into external template string
T=(p/'template.html').read_text('utf-8')
T=cc.convert(T)
# 人工校對專名與品牌名稱
for a,b in {'搞玄*壹仟林壹夜':'搞玄*壹仟林壹夜','釵釧金':'釵釧金','井木犴':'井木犴','白蠟金':'白蠟金','長流水':'長流水','醜':'丑','六衝':'六冲','往裏掃':'往里扫','搞玄*壹仟林壹夜':'壹仟林壹夜','搞玄-分享卡.png':'壹仟林壹夜-分享卡.png'}.items(): T=T.replace(a,b)
qr=(p/'node_modules/qrcode-generator/dist/qrcode.js').read_text('utf-8')
T=T.replace('__CALENDAR__',cal).replace('__CONTENT__',content).replace('__FULL_BLOB__',full_blob).replace('__QRCODE_LIB__',qr).replace('__COVER__',cover).replace('__FU__',fu)
(p/'index.html').write_text(T,'utf-8')
print('built index.html', (p/'index.html').stat().st_size, 'bytes')
