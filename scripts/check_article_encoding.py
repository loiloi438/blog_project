#!/usr/bin/env python3
"""
Quick script to list articles whose content appears to contain the Unicode replacement
character (�) or suspicious sequences of question marks that indicate encoding problems.
Run from project root with the project's virtualenv active:

python scripts/check_article_encoding.py

"""
import os
import sys

# adjust PYTHONPATH and DJANGO settings
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')

try:
    import django
    django.setup()
except Exception as e:
    print('Error setting up Django:', e)
    sys.exit(1)

from blog.models import Article

REPLACEMENT = '\ufffd'  # the Unicode replacement character
BAD_MARKERS = ['�', REPLACEMENT]

print('Scanning articles for encoding issues...')
found = False
for a in Article.objects.all():
    content = a.content or ''
    if any(mark in content for mark in BAD_MARKERS) or content.count('?') > max(10, len(content) // 10):
        found = True
        print(f"- Article id={a.pk} title={a.title!r}")
        # show a snippet
        snippet = content[:400].replace('\n', ' ')[:400]
        print('  snippet:', repr(snippet))

if not found:
    print('No obvious encoding replacement characters found in articles.')
else:
    print('\nReview the listed articles. If they contain � or many ? characters, the data may be stored with wrong encoding.')
