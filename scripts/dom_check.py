import urllib.request, sys, re

def fetch(url):
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            return r.getcode(), r.read().decode('utf-8','replace')
    except Exception as e:
        return None, str(e)

base = 'http://127.0.0.1:8000'
page_code, page_body = fetch(base + '/')
css_code, css_body = fetch(base + '/static/css/design.css')

results = {}
results['/'] = (page_code is not None and page_code == 200)
results['css'] = (css_code is not None and css_code == 200)

# search for selectors/classes
site_hero_found = False
home_highlights_found = False
if page_body:
    site_hero_found = bool(re.search(r'class\s*=\s*"[^"]*\bsite-hero\b[^"]*"', page_body))
    home_highlights_found = bool(re.search(r'class\s*=\s*"[^"]*\bhome-highlights\b[^"]*"', page_body))

css_site_hero = False
css_home_highlights = False
if css_body:
    css_site_hero = '.site-hero' in css_body
    css_home_highlights = '.home-highlights' in css_body

print('DOM CHECK REPORT')
print('GET / ->', page_code)
print(' - .site-hero in HTML:', site_hero_found)
print(' - .home-highlights in HTML:', home_highlights_found)
print('GET /static/css/design.css ->', css_code)
print(' - .site-hero in CSS:', css_site_hero)
print(' - .home-highlights in CSS:', css_home_highlights)

ok = results['/'] and results['css'] and site_hero_found and home_highlights_found and css_site_hero and css_home_highlights
print('\nSUMMARY: OK' if ok else '\nSUMMARY: ISSUES FOUND')
if not ok:
    if not results['/']:
        print(' - / unreachable')
    if not results['css']:
        print(' - CSS unreachable')
    if not site_hero_found:
        print(' - .site-hero missing from HTML (check template block or class names)')
    if not home_highlights_found:
        print(' - .home-highlights missing from HTML (ensure section added)')
    if not css_site_hero:
        print(' - .site-hero missing from CSS (add styles)')
    if not css_home_highlights:
        print(' - .home-highlights missing from CSS (add styles)')

sys.exit(0 if ok else 2)
