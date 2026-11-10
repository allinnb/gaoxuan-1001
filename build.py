import json,base64,re,html,os,hashlib
from pathlib import Path
from opencc import OpenCC
import pandas as pd
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

# === 第五輪白話文案表 → copy.json ===
xlsx_path = Path(r'C:\Users\heyia\Downloads\搞玄-白話文案表.xlsx')
if xlsx_path.exists():
    copy = {}
    for sheet in pd.ExcelFile(xlsx_path).sheet_names:
        df = pd.read_excel(xlsx_path, sheet_name=sheet)
        for _,row in df.iterrows():
            k = str(row.get('查表鍵','')).strip().replace('往裏掃','往里扫')
            if not k or k=='nan': continue
            copy[k] = {
                'tag': str(row.get('人設標籤','')).strip(),
                'keywords': str(row.get('關鍵詞','')).replace('往裏掃','往里扫').strip(),
                'plain': re.sub(r'【待核[^】]*】','',str(row.get('白話解讀',''))).replace('□','').replace('往裏掃','往里扫').strip(),
                'tip': str(row.get('林叔吐槽','')).replace('往裏掃','往里扫').strip(),
                'quote': str(row.get('原文金句','')).replace('往裏掃','往里扫').strip()
            }
    (p/'copy.json').write_text(json.dumps(copy,ensure_ascii=False,indent=2),'utf-8')
    print('generated copy.json with', len(copy), 'entries')
    # 必須鍵與五層卡片欄位檢查；只驗證文案表實際涵蓋的查法。
    required = {'角木蛟','鼠骨','鳳凰','子','頭','二兩一錢','建田','建學','官人','向祿','驛馬','值太歲','千手觀音菩薩','八敗-犯','羅睺'}
    missing = required - copy.keys()
    incomplete = [k for k,v in copy.items() if not all(v.get(x) and v[x] != 'nan' for x in ('tag','keywords','plain','tip','quote'))]
    if missing or incomplete:
        raise SystemExit('COPY VALIDATION FAILED: missing='+','.join(sorted(missing))+' incomplete='+','.join(incomplete[:20]))
    if any('【待核】' in str(v) for row in copy.values() for v in row.values()):
        raise SystemExit('COPY VALIDATION FAILED: 文案仍含【待核】')
    copy_content=json.dumps(copy,ensure_ascii=False).replace('</','<\\/')
    print('validated copy.json with', len(copy), 'entries')
else:
    raise SystemExit('COPY VALIDATION FAILED: '+str(xlsx_path)+' not found')
rules=(p/'rules-v2/RULES-v2-part2.md').read_text('utf-8')
year_branch=dict(re.findall(r'^\*\*([子丑寅卯辰巳午未申酉戌亥])（[^）]+）\*\*\s*(.+)$',rules,re.M))
month_text={i+1:x for i,x in enumerate(re.findall(r'^- ((?:正|二|三|四|五|六|七|八|九|十|子|腊)月生人.+)$',rules,re.M)[:12])}
hour_text=dict(re.findall(r'^- ([子丑寅卯辰巳午未申酉戌亥])时生人[：:]\s*(.+)$',rules,re.M))
full={"nianzhu":json.loads((p/'rules-v2/alt/nianzhu.json').read_text('utf-8')),"yearBranch":year_branch,"month":month_text,"hour":hour_text,"hourParts":json.loads((p/'rules-v2/alt/110724.json').read_text('utf-8'))}
full_package=json.dumps(full,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
# placeholders replaced into external template string
T=(p/'template.html').read_text('utf-8')
T=cc.convert(T)
# 人工校對專名與品牌名稱
for a,b in {'釵釧金':'釵釧金','井木犴':'井木犴','白蠟金':'白蠟金','長流水':'長流水','醜':'丑','六衝':'六冲','往裏掃':'往里扫','搞玄-分享卡.png':'壹仟林壹夜-分享卡.png'}.items(): T=T.replace(a,b)
qr=(p/'node_modules/qrcode-generator/dist/qrcode.js').read_text('utf-8')
T=T.replace('__CALENDAR__',cal).replace('__CONTENT__',content).replace('__COPY__',copy_content).replace('__FULL_PACKAGE__',full_package).replace('__QRCODE_LIB__',qr).replace('__COVER__',cover).replace('__FU__',fu)
(p/'index.html').write_text(T,'utf-8')
print('built index.html', (p/'index.html').stat().st_size, 'bytes')
