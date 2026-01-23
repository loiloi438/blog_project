import os, django, sys
# ensure project root is on PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
try:
    django.setup()
except Exception as e:
    print('DJANGO SETUP FAILED', e)
    sys.exit(2)
from django.test import Client
from django.conf import settings
# allow testserver host for internal client
try:
    settings.ALLOWED_HOSTS = ['testserver', '127.0.0.1', 'localhost']
except Exception:
    pass

c = Client()
paths = ['/', '/articles/', '/static/css/design.css']
for p in paths:
    r = c.get(p)
    print(p, 'status=', r.status_code)
    if r.status_code == 200:
        print(' snippet:', r.content.decode('utf-8','replace')[:300].replace('\n',' '))

# simple content checks on home
r = c.get('/')
if r.status_code != 200:
    print('HOME FAIL')
    sys.exit(2)
body = r.content.decode('utf-8','replace')
checks = {
    'hero': 'Bienvenue' in body or 'Bienvenue!' in body,
    'highlights': 'À la une' in body or 'Populaires' in body or 'Explorer' in body,
    'footer': 'Blog Interactif' in body or '<footer' in body,
}
print('checks:', checks)
if all(checks.values()):
    print('INTERNAL CLIENT: ALL OK')
    sys.exit(0)
else:
    print('INTERNAL CLIENT: SOME CHECKS FAILED')
    sys.exit(3)
