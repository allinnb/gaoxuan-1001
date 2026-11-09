from playwright.sync_api import sync_playwright
from pathlib import Path
OUT=Path('screenshots'); OUT.mkdir(exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(headless=True)
 for width in (360,390):
  page=b.new_page(viewport={'width':width,'height':844},device_scale_factor=2)
  page.goto(Path('index.html').resolve().as_uri(),wait_until='networkidle')
  page.screenshot(path=str(OUT/f'{width}-01-first-screen.png'),full_page=False)
  page.locator('#summary').scroll_into_view_if_needed(); page.screenshot(path=str(OUT/f'{width}-02-ticket.png'),full_page=False)
  details=page.locator('details').first
  if details.count(): details.evaluate('(e)=>e.open=true'); details.scroll_into_view_if_needed(); page.screenshot(path=str(OUT/f'{width}-03-card-expanded.png'),full_page=False)
  page.locator('#fullModules').scroll_into_view_if_needed(); page.screenshot(path=str(OUT/f'{width}-04-full-locked.png'),full_page=False)
  canvas=page.evaluate("""()=>{const c=makeShare('9:16');return c.toDataURL('image/png')}""")
  import base64
  (OUT/f'{width}-05-share-card.png').write_bytes(base64.b64decode(canvas.split(',',1)[1]))
  page.close()
 b.close()
print('captured 10 acceptance screenshots in screenshots/')
