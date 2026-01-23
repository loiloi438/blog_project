import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
import django
django.setup()
from django.contrib.auth.models import User
from django.test import Client
from blog.models import Article, Like

# create test user if not exists
username = 'autotest'
password = 'testpass123'
if not User.objects.filter(username=username).exists():
    u = User.objects.create_user(username=username, password=password)
    print('Created user', username)
else:
    u = User.objects.get(username=username)
    print('User exists')

# pick first article
article = Article.objects.first()
if not article:
    print('No article in DB to test')
    sys.exit(2)
print('Testing article', article.pk, article.title)

c = Client()
# login
logged = c.login(username=username, password=password)
print('login', logged)
# ensure no like
Like.objects.filter(article=article, user=u).delete()
print('likes before:', article.likes.count())
# post like
res = c.post(f'/article/{article.pk}/like/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
print('POST like status', res.status_code, res.content)
print('likes after like:', article.likes.count())
# post again to unlike
res2 = c.post(f'/article/{article.pk}/like/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
print('POST unlike status', res2.status_code, res2.content)
print('likes after unlike:', article.likes.count())

# cleanup
Like.objects.filter(article=article, user=u).delete()
print('Cleanup done')
