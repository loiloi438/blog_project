from playwright.sync_api import sync_playwright
import os

urls = [
    ('desktop', 'http://127.0.0.1:8000/', {'width': 1280, 'height': 800}),
    ('mobile', 'http://127.0.0.1:8000/', {'width': 390, 'height': 844, 'is_mobile': True}),
]

out_dir = os.path.join(os.path.dirname(__file__), 'screenshots')
os.makedirs(out_dir, exist_ok=True)

with sync_playwright() as p:
    try:
        print('Launching browser')
        browser = p.chromium.launch(headless=True)
        for name, url, viewport in urls:
            print('New context', name)
            if viewport.get('is_mobile'):
                context = browser.new_context(viewport={'width': viewport['width'], 'height': viewport['height']}, is_mobile=True)
            else:
                context = browser.new_context(viewport={'width': viewport['width'], 'height': viewport['height']})
            page = context.new_page()
            print('Navigating to', url)
            try:
                page.goto(url, wait_until='networkidle', timeout=15000)
            except Exception as e:
                print('Navigation failed for', url, '->', e)
            path = os.path.join(out_dir, f'{name}.png')
            try:
                page.screenshot(path=path, full_page=True)
                print('Saved', path)
            except Exception as e:
                print('Screenshot failed for', name, '->', e)
            try:
                context.close()
            except Exception:
                pass
        try:
            browser.close()
        except Exception:
            pass
    except Exception as e:
        print('Playwright error', e)
