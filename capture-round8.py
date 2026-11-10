from playwright.sync_api import sync_playwright
from pathlib import Path
import base64
out=Path('screenshots'); out.mkdir(exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(headless=True)
 page=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
 errors=[]; page.on('pageerror',lambda e: errors.append(str(e)))
 page.goto(Path('index.html').resolve().as_uri(),wait_until='networkidle')
 page.locator('#summary').scroll_into_view_if_needed(); page.screenshot(path=str(out/'390-round8-ticket.png'))
 page.locator('#volume-4').scroll_into_view_if_needed(); page.screenshot(path=str(out/'390-round8-volume-4.png'))
 data=page.evaluate("()=>makeShare('9:16').toDataURL('image/png')")
 (out/'390-round8-share-9x16.png').write_bytes(base64.b64decode(data.split(',',1)[1]))
 assert not errors,errors
 page.close(); b.close()
print('captured 390px ticket, volume 4, and 9:16 share card')
