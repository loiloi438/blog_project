import sys
from urllib.parse import urljoin

BASE = 'http://127.0.0.1:8000'

try:
    import requests
except Exception as e:
    print('requests missing:', e)
    sys.exit(2)

s = requests.Session()

def get(path):
    try:
        r = s.get(urljoin(BASE, path), timeout=10)
        print(path, r.status_code)
        return r
    except Exception as e:
        print(path, 'error', e)
        sys.exit(1)

get('/')
get('/articles/')
r = get('/article/25/')

csrf = s.cookies.get('csrftoken')
print('csrftoken_cookie:', bool(csrf))
headers = {'X-Requested-With': 'XMLHttpRequest'}
if csrf:
    headers['X-CSRFToken'] = csrf

try:
    p = s.post(urljoin(BASE, '/article/25/like/'), headers=headers, data={}, timeout=10)
    print('POST /article/25/like/ ->', p.status_code, p.headers.get('content-type'))
    print('Response body (truncated):', p.text[:200])
except Exception as e:
    print('post like error:', e)
