from playwright.sync_api import sync_playwright
from pathlib import Path
with sync_playwright() as p:
 b=p.chromium.launch(headless=True)
 page=b.new_page(viewport={"width":390,"height":844},device_scale_factor=2)
 page.goto(Path('index.html').resolve().as_uri(),wait_until='load')
 page.screenshot(path='mobile-screenshot.png',full_page=True)
 page.click('#makeCard')
 page.locator('#shareCanvas').screenshot(path='share-card-sample.png')
 assert page.locator('h1').inner_text().strip().endswith('壹仟林壹夜')
 assert '真太陽時' in page.locator('#freePack').inner_text()
 b.close()
print('captured mobile-screenshot.png and share-card-sample.png')
