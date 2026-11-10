from playwright.sync_api import sync_playwright
from pathlib import Path
out=Path('screenshots');out.mkdir(exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(headless=True);page=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
 page.goto(Path('index.html').resolve().as_uri(),wait_until='networkidle')
 page.locator('#citySearch').fill('州');page.locator('#birthCity').evaluate("e=>e.size=8");page.locator('.intake').screenshot(path=str(out/'390-round9-city-search.png'))
 page.locator('#lunarTab').click();page.locator('.intake').screenshot(path=str(out/'390-round9-lunar-input.png'))
 page.locator('#solarTab').click();page.locator('#birthForm').evaluate("e=>e.requestSubmit()");page.locator('#freePack .result-card').first.scroll_into_view_if_needed();page.locator('#freePack .result-card').first.screenshot(path=str(out/'390-round9-sage-card.png'))
 b.close()
print('captured round9 city search, lunar input, sage card')
