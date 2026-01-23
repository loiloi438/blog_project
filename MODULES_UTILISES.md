# MODULES_UTILISES.md - Liste Complète des Modules et Dépendances

## 📦 Dépendances Python (requirements.txt)

### Core Django
- **Django 5.2.10** - Framework web principal
  - Utilisé pour: MVC architecture, ORM, templates, authentification, admin
  - Documentation: https://docs.djangoproject.com/en/5.2/

### Utilitaires
- **Pillow 10.1.0** - Traitement d'images
  - Utilisé pour: Upload et traitement des images de couverture des articles
  - Documentation: https://pillow.readthedocs.io/

- **sqlparse 0.4.4** - Parser SQL
  - Utilisé par Django pour formater les requêtes SQL
  - Documentation: https://sqlparse.readthedocs.io/

- **asgiref 3.7.2** - Utilitaires ASGI
  - Utilisé pour la gestion des coroutines asyncio
  - Documentation: https://asgiref.readthedocs.io/

- **tzdata 2023.3** - Données de fuseau horaire
  - Utilisé pour gérer les fuseaux horaires correctement
  - Documentation: https://github.com/dateutil/dateutil

### Optionnel pour Production
```
gunicorn==20.1.0         # Serveur WSGI de production
python-decouple==3.8     # Gestion des variables d'environnement
psycopg2-binary==2.9.x   # Driver PostgreSQL
redis==4.x.x             # Caching
django-redis==5.x.x      # Intégration Redis avec Django
```

---

## 🌐 Dépendances Frontend (CDN)

### Bootstrap 5.3.0
```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
```
- **Utilisé pour**: Framework CSS, composants responsive, formulaires
- **Features**: Grid system, buttons, modals, dropdowns, forms
- **Documentation**: https://getbootstrap.com/docs/5.3/

---

## 🎯 Modules Django Intégrés

### django.contrib.admin
**Utilisé pour**: Interface d'administration
**Fichier**: `blog/admin.py`
**Classes personnalisées**:
- `ArticleAdmin`: Gestion des articles dans l'admin
- `CommentAdmin`: Gestion des commentaires dans l'admin

### django.contrib.auth
**Utilisé pour**: Authentification utilisateur
**Fonctionnalités**:
- `User` model
- `authenticate()`: Authentifier un utilisateur
- `login()`: Créer une session
- `logout()`: Détruire une session
- `@login_required`: Décorateur pour protection

### django.contrib.contenttypes
**Utilisé pour**: Framework de type de contenu
**Rôle**: Support pour les relations génériques (optional)

### django.contrib.sessions
**Utilisé pour**: Gestion des sessions utilisateur
**Cookies**: Stockage des IDs de session

### django.contrib.messages
**Utilisé pour**: Messages flash aux utilisateurs
**Niveaux**: SUCCESS, ERROR, WARNING, INFO

### django.contrib.staticfiles
**Utilisé pour**: Gestion des fichiers CSS/JS/images
**Commandes**: `collectstatic`

---

## 📂 Architecture Personnalisée

### Models (`blog/models.py`)

#### Article
```python
from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    # Champs
    title: CharField(200)
    content: TextField
    author: ForeignKey(User, on_delete=CASCADE)
    cover_image: ImageField
    created_at: DateTimeField(auto_now_add=True)
    updated_at: DateTimeField(auto_now=True)
    likes: ManyToManyField(User, related_name='liked_articles')
    
    # Imports nécessaires
    - django.db.models: CharField, TextField, ForeignKey, etc.
    - django.contrib.auth.models: User
```

#### Comment
```python
class Comment(models.Model):
    # Champs
    article: ForeignKey(Article, on_delete=CASCADE)
    author: ForeignKey(User, on_delete=CASCADE)
    body: TextField
    created_at: DateTimeField(auto_now_add=True)
    updated_at: DateTimeField(auto_now=True)
    parent: ForeignKey(self, on_delete=CASCADE, null=True, blank=True)
    
    # Méthodes
    def get_replies(self): # Récupère les réponses
```

### Views (`blog/views.py`)

**Imports utilisés**:
```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .models import Article, Comment
from .forms import CustomUserCreationForm, UserLoginForm, ArticleForm, CommentForm
```

**Décorateurs utilisés**:
- `@login_required(login_url='login')`: Protection d'accès
- `@require_http_methods(["POST"])`: Restriction HTTP
- `@require_http_methods(["GET", "POST"])`: Multiple méthodes

**Vue générique**:
```python
def view_name(request):
    # GET
    if request.method == 'GET':
        # Logique GET
        return render(request, 'template.html', context)
    
    # POST
    elif request.method == 'POST':
        # Logique POST
        return redirect('view_name')
```

### Forms (`blog/forms.py`)

**Imports**:
```python
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Article, Comment
```

**Classes**:
1. `CustomUserCreationForm(UserCreationForm)` - Héritage de Django
2. `UserLoginForm(forms.Form)` - Formulaire personnalisé
3. `ArticleForm(forms.ModelForm)` - ModelForm pour Article
4. `CommentForm(forms.ModelForm)` - ModelForm pour Comment

**Widgets Bootstrap**:
```python
widget=forms.TextInput(attrs={'class': 'form-control'})
widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10})
widget=forms.EmailInput(attrs={'class': 'form-control'})
```

### Templates Django

**Syntaxe DTL (Django Template Language)**:
```django
{% if %}{% endif %} - Conditions
{% for %}{% endfor %} - Boucles
{{ variable }} - Affichage variables
{% url 'name' arg %} - Génération URLs
{% load %} - Charger des tags
{% csrf_token %} - Protection CSRF
{% include 'path' %} - Inclure un template
{% extends 'base.html' %} - Héritage
{% block name %}{% endblock %} - Blocs
{{ var|filter }} - Filtres
```

**Filtres utilisés**:
- `|date:"d/m/Y \à H:i"` - Formatage date
- `|truncatewords:50` - Tronquer le texte
- `|pluralize` - Pluralisation
- `|linebreaks` - Convertir les sauts de ligne

**Tags personnalisés**:
- `{% if user.is_authenticated %}` - Authentification
- `{% if user in article.likes.all %}` - Vérifier appartenance
- `{% if article.author == user %}` - Comparaison

### URLs (`blog/urls.py` et `blog_project/urls.py`)

**Imports**:
```python
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
```

**Patterns**:
```python
path('article/<int:pk>/', views.article_detail, name='article_detail')
path('article/<int:pk>/like/', views.toggle_like, name='toggle_like')
path('', include('blog.urls'))
```

**Media files**:
```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 🔧 Configuration Django (`settings.py`)

### Variables Importantes
```python
SECRET_KEY = '...'                     # Clé de sécurité
DEBUG = True/False                     # Mode debug
ALLOWED_HOSTS = []                     # Hosts autorisés
INSTALLED_APPS = [...]                 # Applications installées
MIDDLEWARE = [...]                     # Middlewares
TEMPLATES = [...]                      # Configuration templates
DATABASES = {...}                      # Base de données
AUTH_PASSWORD_VALIDATORS = [...]       # Validation mot de passe
LANGUAGE_CODE = 'fr-fr'                # Langue
TIME_ZONE = 'UTC'                      # Fuseau horaire
STATIC_URL = 'static/'                 # URL fichiers statiques
MEDIA_URL = 'media/'                   # URL fichiers media
LOGIN_URL = 'login'                    # URL redirection
```

---

## 📊 Queries ORM Utilisées

### Article
```python
Article.objects.all()                                    # Tous
Article.objects.filter(author=user)                      # Filtre
Article.objects.get(pk=1)                                # Un seul
Article.objects.filter(parent__isnull=True)              # Null
Article.objects.select_related('author')                 # JOIN
Article.objects.annotate(likes_count=Count('likes'))     # Aggrégation
Article.objects.order_by('-created_at')                  # Tri
Article.objects.filter(Q(title__icontains='x') | Q(...)) # OR
```

### Like
```python
article.likes.add(user)                                  # Ajouter
article.likes.remove(user)                               # Retirer
user in article.likes.all()                              # Vérifier
article.likes.count()                                    # Compter
```

### Comment
```python
Comment.objects.filter(article=article)                  # Tous les comments
Comment.objects.filter(parent__isnull=True)              # Commentaires parents
comment.replies.all()                                    # Réponses
```

---

## 🛡️ Sécurité

### Protections Implémentées
1. **CSRF**: `{% csrf_token %}` dans tous les formulaires
2. **Authentification**: `@login_required` sur actions sensibles
3. **Autorisation**: Vérifier que `request.user == objet.author`
4. **Hachage mots de passe**: Django gère automatiquement
5. **SQL Injection**: ORM Django prévient automatiquement
6. **XSS**: Templates Django échappent par défaut

### Dépendances de sécurité
```python
# Middleware de sécurité Django activé
'django.middleware.security.SecurityMiddleware'

# Vérification des permissions
if article.author != request.user and not request.user.is_staff:
    return redirect('article_detail', pk=pk)
```

---

## 🚀 Performance

### Optimisations
1. **select_related()** pour les ForeignKey
2. **Pagination** pour les listes longues
3. **Cache** pour les vues fréquentes
4. **Compression** CSS/JS (production)
5. **CDN** pour Bootstrap et jQuery

### Outils de monitoring
```python
# Debug Toolbar (development)
pip install django-debug-toolbar

# Profiling
pip install django-silk

# Sentry (production)
pip install sentry-sdk
```

---

## 📚 Documentation Officielle

| Module | Lien |
|--------|------|
| Django | https://docs.djangoproject.com/en/5.2/ |
| Pillow | https://pillow.readthedocs.io/ |
| Bootstrap | https://getbootstrap.com/ |
| Python | https://docs.python.org/3/ |

---

## 🔄 Système de Fichiers

```
blog_project/
├── blog/                           # Application Django
│   ├── migrations/                # Migrations BD
│   │   ├── __init__.py
│   │   ├── 0001_initial.py       # Créer Article, Comment
│   │   └── __pycache__/
│   ├── __pycache__/
│   ├── admin.py                  # Registrer models admin
│   ├── apps.py                   # Configuration app
│   ├── forms.py                  # 4 formulaires
│   ├── models.py                 # 2 models (Article, Comment)
│   ├── tests.py                  # Tests unitaires
│   ├── urls.py                   # 12 routes
│   ├── views.py                  # 13 vues
│   └── __init__.py
├── blog_project/                 # Configuration projet
│   ├── __pycache__/
│   ├── asgi.py                   # ASGI (production)
│   ├── settings.py               # Paramètres Django
│   ├── urls.py                   # URLs racine
│   ├── wsgi.py                   # WSGI (production)
│   └── __init__.py
├── templates/
│   └── blog/                     # 8 templates HTML
│       ├── base.html             # Template de base
│       ├── home.html             # Accueil
│       ├── login.html            # Connexion
│       ├── register.html         # Inscription
│       ├── article_form.html     # Formulaire article
│       ├── article_detail.html   # Détail + commentaires
│       ├── article_list.html     # Liste articles
│       ├── article_confirm_delete.html # Confirmation
│       ├── comment_thread.html   # Commentaires hiérarchiques
│       └── search_results.html   # Résultats recherche
├── media/                        # Fichiers uploadés
├── db.sqlite3                    # Base de données
├── manage.py                     # Gestionnaire Django
├── init_db.py                    # Initialisation BD
├── requirements.txt              # Dépendances
├── README.md                     # Documentation
├── DOCUMENTATION.md              # Doc technique
├── GUIDE_TEST.md                 # Guide de test
├── DEPLOIEMENT.md                # Guide déploiement
├── MODULES_UTILISES.md           # Ce fichier
├── settings_production.py        # Settings prod
├── .env.example                  # Variables env
└── .gitignore                    # Fichiers git ignorés
```

---

## 💾 Base de Données

### Modèle Logique
```
User (Django)
├── articles (1:N) → Article
├── liked_articles (M:N) → Article
└── comments (1:N) → Comment

Article
├── author (N:1) → User
├── likes (M:N) → User
└── comments (1:N) → Comment

Comment
├── article (N:1) → Article
├── author (N:1) → User
└── parent (N:1 self) → Comment
```

### Tables Créées
1. `blog_article` - Articles
2. `blog_comment` - Commentaires
3. `blog_article_likes` - Relation M:N likes
4. + Tables Django (auth, sessions, etc.)

---

## 🔐 Clés et Relations

### Foreign Keys
- `Article.author` → `User` (CASCADE)
- `Article.likes` → `User` (ManyToMany)
- `Comment.article` → `Article` (CASCADE)
- `Comment.author` → `User` (CASCADE)
- `Comment.parent` → `Comment` (self, CASCADE)

### Cascade
- Supprimer un User supprime ses articles et commentaires
- Supprimer un Article supprime ses commentaires
- Supprimer un Comment supprime ses réponses

---

**Date**: 21 Janvier 2026
**Version**: 1.0.0
**Nombre total de modules**: 5 dépendances Python + Bootstrap CDN
