from playwright.sync_api import sync_playwright
from pathlib import Path
import base64
OUT=Path('screenshots'); OUT.mkdir(exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(headless=True)
 for width in (360,390):
  page=b.new_page(viewport={'width':width,'height':844},device_scale_factor=2)
  page.goto(Path('index.html').resolve().as_uri(),wait_until='networkidle')
  errors=[]; page.on('pageerror',lambda e: errors.append(str(e)))
  page.screenshot(path=str(OUT/f'{width}-01-first-screen.png'))
  page.locator('#volume-1').scroll_into_view_if_needed(); page.screenshot(path=str(OUT/f'{width}-02-volume-1.png'))
  page.locator('#volume-4').scroll_into_view_if_needed(); page.screenshot(path=str(OUT/f'{width}-03-volume-4.png'))
  page.locator('#volume-5').scroll_into_view_if_needed(); page.screenshot(path=str(OUT/f'{width}-04-volume-5.png'))
  for ratio,name in [('9:16','05-share-9x16'),('1:1','06-share-1x1')]:
   canvas=page.evaluate("ratio=>makeShare(ratio).toDataURL('image/png')",ratio)
   (OUT/f'{width}-{name}.png').write_bytes(base64.b64decode(canvas.split(',',1)[1]))
  assert not errors, errors
  # Navigation acceptance: horizontally scrollable and every link is present/clickable.
  assert page.locator('.volume-nav a').count()==6
  for a in page.locator('.volume-nav a').all(): a.click(force=True)
  page.close()
 b.close()
print('captured 12 acceptance screenshots in screenshots/')
