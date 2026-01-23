import urllib.request, sys
urls = [
    ('/','http://127.0.0.1:8000/'),
    ('/articles/','http://127.0.0.1:8000/articles/'),
    ('/static/css/design.css','http://127.0.0.1:8000/static/css/design.css'),
]
for name,url in urls:
    try:
        r = urllib.request.urlopen(url, timeout=5)
        body = r.read().decode('utf-8','replace')
        print('\n---', name, 'STATUS', r.getcode())
        if name == '/static/css/design.css':
            print(body[:600])
        else:
            print(body[:1600])
    except Exception as e:
        print('\n---', name, 'ERROR', repr(e))
sys.exit(0)
