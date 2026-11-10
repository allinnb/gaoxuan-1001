import json,base64,re,sys
try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass
from pathlib import Path
from opencc import OpenCC
import pandas as pd

cc=OpenCC('s2tw')
p=Path(__file__).parent
cal=(p/'calendar-data.json').read_text('utf-8')
cities=(p/'cities.json').read_text('utf-8')
cover=base64.b64encode((p/'cover-01.jpg').read_bytes()).decode()
fu=base64.b64encode((p/'fu-04.jpg').read_bytes()).decode()
SPECIAL={'釵釧金':'釵釧金','井木犴':'井木犴','白蠟金':'白蠟金','長流水':'長流水','醜':'丑','六衝':'六沖','往裡掃':'往裏掃'}
def trad(s):
 s=cc.convert(str(s))
 for a,b in SPECIAL.items(): s=s.replace(a,b)
 return s

def safe_json(v): return json.dumps(v,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')

texts={}
for f in (p/'src').glob('src-*.txt'):
 key=f.stem[4:]
 if key.lower()=='wanneng': continue
 s=f.read_text('utf-8'); s=re.sub(r'\[[^\]]*https?://[^\]]*\]','',s); s=re.sub(r'https?://\S+','',s); texts[key]=trad(s.strip())
TAISUI_GUIDE='''值太歲：本命生肖與流年生肖相同，即為值太歲。\n沖太歲：本命生肖與流年生肖相沖，即為沖太歲。\n刑太歲：本命生肖與流年生肖相刑，即為刑太歲。\n害太歲：本命生肖與流年生肖相害，即為害太歲。\n破太歲：本命生肖與流年生肖相破，即為破太歲。\n\n十二太歲神：太歲、太陽、喪門、太陰、官符、死符、歲破、龍德、白虎、福德、弔客、病符。'''
texts['taisui']=TAISUI_GUIDE
content=safe_json(texts)

xlsx_path=p/'data/搞玄-白話文案表.xlsx'
if not xlsx_path.exists(): raise SystemExit('COPY VALIDATION FAILED: '+str(xlsx_path)+' not found')
copy={}; total=0; stats=[]
for sheet in pd.ExcelFile(xlsx_path).sheet_names:
 df=pd.read_excel(xlsx_path,sheet_name=sheet).fillna(''); copy[sheet]={}
 for _,row in df.iterrows():
  group=str(row.get('分組','')).strip() or '未分組'; key=trad(str(row.get('查表鍵','')).strip())
  if not key: raise SystemExit(f'COPY VALIDATION FAILED: empty key in {sheet}/{group}')
  bucket=copy[sheet].setdefault(group,{})
  if key in bucket: raise SystemExit(f'COPY VALIDATION FAILED: duplicate {sheet}/{group}/{key}')
  values={
   'tag':trad(str(row.get('人設標籤','')).strip()),'keywords':trad(str(row.get('關鍵詞','')).strip()),
   'plain':trad(re.sub(r'【待核[^】]*】','',str(row.get('白話解讀',''))).replace('□','').strip()),
   'tip':trad(str(row.get('林叔吐槽','')).strip()),'quote':trad(str(row.get('原文金句','')).strip())}
  # 公開頁不得帶人名、粗口；保留資料語義但改成中性措辭。
  for k,v in values.items():
   replacements=[('吳'+'亦凡','某藝人'),('鄭'+'爽','某藝人'),('馬'+'雲','某企業家'),('許'+'家印','某企業家'),('李'+'雲迪','某藝人'),('他'+'媽','粗口'),('仆'+'街','倒楣'),('泡'+'炮','玩樂')]
   for bad,repl in replacements: v=v.replace(bad,repl)
   values[k]=v
  if not all(values.values()): raise SystemExit(f'COPY VALIDATION FAILED: incomplete {sheet}/{group}/{key}')
  bucket[key]=values; total+=1
 for group,rows in copy[sheet].items(): stats.append((sheet,group,len(rows)))
if total!=300: raise SystemExit(f'COPY VALIDATION FAILED: expected base 300, got {total}')
full_copy_path=p/'data/搞玄-完整命書文案表.xlsx'
if not full_copy_path.exists(): raise SystemExit('COPY VALIDATION FAILED: '+str(full_copy_path)+' not found')
copy['完整命書']={}
for sheet in pd.ExcelFile(full_copy_path).sheet_names:
 df=pd.read_excel(full_copy_path,sheet_name=sheet,dtype=str).fillna(''); bucket=copy['完整命書'].setdefault(sheet,{})
 for _,row in df.iterrows():
  group=trad(str(row.get('group','')).strip()); key=trad(str(row.get('key','')).strip())
  if group!=sheet or not key: raise SystemExit(f'COPY VALIDATION FAILED: invalid complete-reading row {sheet}/{group}/{key}')
  if key in bucket: raise SystemExit(f'COPY VALIDATION FAILED: duplicate 完整命書/{sheet}/{key}')
  values={f:trad(str(row.get(f,'')).strip()) for f in ('tag','keywords','plain','tip','quote')}
  if sheet=='時辰': values.update({f:trad(str(row.get(f,'')).strip()) for f in ('ke_shang','ke_zhong','ke_xia')})
  if not all(values.values()): raise SystemExit(f'COPY VALIDATION FAILED: incomplete 完整命書/{sheet}/{key}')
  bucket[key]=values; total+=1
 for group,rows in copy['完整命書'].items():
  if group==sheet: stats.append(('完整命書',group,len(rows)))
if total!=432: raise SystemExit(f'COPY VALIDATION FAILED: expected 432, got {total}')
(p/'copy.json').write_text(json.dumps(copy,ensure_ascii=False,indent=2),'utf-8')
for sheet,group,n in stats: print(f'COPY {sheet} / {group}: {n}')
print('validated nested copy.json with',total,'entries (300 base + 132 complete-reading)')
copy_content=safe_json(copy)

rules=(p/'rules-v2/RULES-v2-part2.md').read_text('utf-8')
year_branch={trad(k):trad(v) for k,v in re.findall(r'^\*\*([子丑寅卯辰巳午未申酉戌亥])（[^）]+）\*\*\s*(.+)$',rules,re.M)}
month_text={i+1:trad(x) for i,x in enumerate(re.findall(r'^- ((?:正|二|三|四|五|六|七|八|九|十|子|臘|腊)月生人.+)$',rules,re.M)[:12])}
hour_text={trad(k):trad(v) for k,v in re.findall(r'^- ([子丑寅卯辰巳午未申酉戌亥])时生人[：:]\s*(.+)$',rules,re.M)}
nianzhu_raw=json.loads((p/'rules-v2/alt/nianzhu.json').read_text('utf-8'))
nianzhu={trad(k):{'命格':trad(v[1][0]) if len(v)>1 and len(v[1])>0 else '', '性情':trad(v[1][1]) if len(v)>1 and len(v[1])>1 else '', '季節晝夜':trad(v[1][2]) if len(v)>1 and len(v[1])>2 else '', '衣祿':trad(v[1][3]) if len(v)>1 and len(v[1])>3 else ''} for k,v in nianzhu_raw.items()}
hour_parts=[[trad(x) for x in row] for row in json.loads((p/'rules-v2/alt/110724.json').read_text('utf-8'))]
full={'nianzhu':nianzhu,'yearBranch':year_branch,'month':month_text,'hour':hour_text,'hourParts':hour_parts}
full_package=safe_json(full)

T=(p/'template.html').read_text('utf-8')
T=trad(T)
qr=(p/'node_modules/qrcode-generator/dist/qrcode.js').read_text('utf-8')
T=T.replace('__CALENDAR__',cal).replace('__CITIES__',cities).replace('__CONTENT__',content).replace('__COPY__',copy_content).replace('__FULL_PACKAGE__',full_package).replace('__QRCODE_LIB__',qr).replace('__COVER__',cover).replace('__FU__',fu)
banned=['吳亦凡','鄭爽','馬雲','許家印','李雲迪','他'+'媽','仆'+'街','泡'+'炮']
for bad in banned:
 if bad in T: raise SystemExit('CONTENT SAFETY FAILED: prohibited term')
(p/'index.html').write_text(T,'utf-8')
print('built index.html',(p/'index.html').stat().st_size,'bytes')
