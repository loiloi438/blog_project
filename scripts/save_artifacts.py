import urllib.request, os

base = 'http://127.0.0.1:8000'
out = os.path.join(os.path.dirname(__file__), 'artifacts')
os.makedirs(out, exist_ok=True)
paths = {
    'home.html': '/',
    'articles.html': '/articles/',
    'design.css': '/static/css/design.css',
}
for name, path in paths.items():
    url = base + path
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            data = r.read()
            mode = 'wb'
            with open(os.path.join(out, name), mode) as f:
                f.write(data)
            print('Saved', name)
    except Exception as e:
        print('Failed to save', name, '->', e)
