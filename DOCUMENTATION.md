# Documentation Technique - Blog Interactif

## Table des matières
1. [Architecture](#architecture)
2. [API Routes](#api-routes)
3. [Modèles de Données](#modèles-de-données)
4. [Formulaires](#formulaires)
5. [Vues](#vues)
6. [Dépendances](#dépendances)

---

## Architecture

### Pattern MVC (Model-View-Controller)

```
Utilisateur
    ↓
URL Router (urls.py)
    ↓
View (views.py) ← Form (forms.py)
    ↓
Model (models.py) ← Base de données
    ↓
Template (HTML/CSS/JS)
    ↓
Utilisateur (réponse)
```

### Flux d'une requête

1. **URL Routing**: Django reçoit la requête et la route vers la vue appropriée
2. **Authentification**: Vérification de l'authentification (si requise)
3. **Traitement**: La vue traite la logique métier
4. **Base de Données**: Interaction avec les modèles ORM
5. **Rendu**: Django rend le template avec les données
6. **Réponse**: HTML/JSON est envoyé au client

---

## API Routes

### Authentification

#### Inscription
- **URL**: `/register/`
- **Méthode**: GET, POST
- **Template**: `register.html`
- **Formulaire**: `CustomUserCreationForm`
- **Authentification**: Non requise
- **Description**: Permet à un nouveau utilisateur de créer un compte

#### Connexion
- **URL**: `/login/`
- **Méthode**: GET, POST
- **Template**: `login.html`
- **Formulaire**: `UserLoginForm`
- **Authentification**: Non requise
- **Description**: Authentifie un utilisateur existant

#### Déconnexion
- **URL**: `/logout/`
- **Méthode**: GET, POST
- **Authentification**: Requise
- **Description**: Déconnecte l'utilisateur actuel

### Articles

#### Liste des articles (Accueil)
- **URL**: `/`
- **Méthode**: GET
- **Template**: `home.html`
- **Authentification**: Non requise
- **Description**: Affiche la liste de tous les articles avec les likes et commentaires

#### Liste des articles (Page dédiée)
- **URL**: `/articles/`
- **Méthode**: GET
- **Template**: `article_list.html`
- **Authentification**: Non requise
- **Description**: Alternative pour voir tous les articles en vue grille

#### Créer un article
- **URL**: `/article/create/`
- **Méthode**: GET, POST
- **Template**: `article_form.html`
- **Formulaire**: `ArticleForm`
- **Authentification**: Requise
- **Description**: Crée un nouvel article

#### Détail d'un article
- **URL**: `/article/<int:pk>/`
- **Méthode**: GET
- **Template**: `article_detail.html`
- **Authentification**: Non requise
- **Description**: Affiche le détail complet d'un article avec commentaires

#### Modifier un article
- **URL**: `/article/<int:pk>/edit/`
- **Méthode**: GET, POST
- **Template**: `article_form.html`
- **Formulaire**: `ArticleForm`
- **Authentification**: Requise
- **Permission**: Auteur ou Admin
- **Description**: Modifie un article existant

#### Supprimer un article
- **URL**: `/article/<int:pk>/delete/`
- **Méthode**: GET, POST
- **Template**: `article_confirm_delete.html`
- **Authentification**: Requise
- **Permission**: Auteur ou Admin
- **Description**: Supprime un article après confirmation

### Likes

#### Toggle Like
- **URL**: `/article/<int:pk>/like/`
- **Méthode**: POST
- **Authentification**: Requise
- **Content-Type**: Accepte JSON (AJAX) ou formulaire
- **Response**: 
  - JSON: `{"liked": boolean, "likes_count": int}`
  - Redirect: Retour à la page d'article
- **Description**: Ajoute ou retire un like sur un article

### Commentaires

#### Ajouter un commentaire ou réponse
- **URL**: `/article/<int:pk>/comment/`
- **Méthode**: POST
- **Formulaire**: `CommentForm`
- **Authentification**: Requise
- **Paramètres POST**:
  - `body`: Contenu du commentaire
  - `parent_id`: (optionnel) ID du commentaire parent pour les réponses
- **Redirect**: Page d'article
- **Description**: Crée un commentaire ou une réponse

#### Supprimer un commentaire
- **URL**: `/comment/<int:pk>/delete/`
- **Méthode**: POST
- **Authentification**: Requise
- **Permission**: Auteur ou Admin
- **Redirect**: Page d'article
- **Description**: Supprime un commentaire

### Recherche

#### Rechercher des articles
- **URL**: `/search/`
- **Méthode**: GET
- **Template**: `search_results.html`
- **Authentification**: Non requise
- **Paramètres GET**:
  - `q`: Terme de recherche
- **Description**: Recherche dans les titres et contenus des articles

---

## Modèles de Données

### Model: Article

```python
class Article(models.Model):
    title: CharField(max_length=200)
    content: TextField
    author: ForeignKey(User)
    cover_image: ImageField(optional)
    created_at: DateTimeField(auto_now_add=True)
    updated_at: DateTimeField(auto_now=True)
    likes: ManyToManyField(User)
    
    class Meta:
        ordering = ['-created_at']
```

**Méthodes utiles:**
- `article.likes.count()`: Nombre de likes
- `article.comments.count()`: Nombre de commentaires
- `article.author.username`: Nom de l'auteur

**Requêtes utiles:**
```python
# Tous les articles
Article.objects.all()

# Articles triés par popularité
Article.objects.annotate(likes_count=Count('likes')).order_by('-likes_count')

# Articles d'un utilisateur
Article.objects.filter(author=user)

# Recherche
Article.objects.filter(Q(title__icontains='keyword') | Q(content__icontains='keyword'))

# Articles aimés par un utilisateur
user.liked_articles.all()
```

### Model: Comment

```python
class Comment(models.Model):
    article: ForeignKey(Article)
    author: ForeignKey(User)
    body: TextField
    created_at: DateTimeField(auto_now_add=True)
    updated_at: DateTimeField(auto_now=True)
    parent: ForeignKey(self, null=True, blank=True)
    
    class Meta:
        ordering = ['created_at']
```

**Méthodes utiles:**
- `comment.get_replies()`: Retourne les réponses directes
- `comment.parent`: Le commentaire parent (None si c'est un commentaire principal)

**Requêtes utiles:**
```python
# Commentaires principaux seulement
Comment.objects.filter(parent__isnull=True)

# Réponses à un commentaire
Comment.objects.filter(parent=comment)

# Tous les commentaires d'un article
article.comments.all()

# Commentaires imbriqués (parents et enfants)
parent_comments = article.comments.filter(parent__isnull=True)
# Puis accéder aux réponses via comment.replies.all()
```

---

## Formulaires

### CustomUserCreationForm
**Champs:**
- `username` (CharField): Nom d'utilisateur unique
- `email` (EmailField): Email unique
- `password1` (PasswordField): Mot de passe
- `password2` (PasswordField): Confirmation du mot de passe

**Validations:**
- Email non utilisé
- Mots de passe correspondent
- Respecte les critères de sécurité Django

### UserLoginForm
**Champs:**
- `username` (CharField): Nom d'utilisateur
- `password` (PasswordField): Mot de passe

### ArticleForm
**Champs:**
- `title` (CharField): Titre de l'article
- `content` (CharField, Textarea): Contenu de l'article
- `cover_image` (ImageField): Image de couverture

### CommentForm
**Champs:**
- `body` (CharField, Textarea): Contenu du commentaire

---

## Vues

### Authentication Views

#### register(request)
```python
def register(request):
    # GET: Affiche le formulaire d'inscription
    # POST: Valide et crée un nouvel utilisateur
    # Redirection: home si connecté, register si GET, home si POST valide
```

#### user_login(request)
```python
def user_login(request):
    # GET: Affiche le formulaire de connexion
    # POST: Valide et connecte l'utilisateur
    # Erreur: "Nom d'utilisateur ou mot de passe incorrect"
```

#### user_logout(request)
```python
def user_logout(request):
    # Déconnecte et redirige vers home
```

### Article Views

#### home(request)
```python
def home(request):
    # GET: Liste tous les articles
    # Context: articles, total_articles
```

#### article_list(request)
```python
def article_list(request):
    # GET: Liste tous les articles (vue grille)
```

#### article_create(request)
```python
@login_required
def article_create(request):
    # GET: Affiche le formulaire de création
    # POST: Crée un nouvel article
    # Authentification: Requise
    # Permission: Utilisateur connecté
```

#### article_detail(request, pk)
```python
def article_detail(request, pk):
    # GET: Affiche le détail d'un article
    # Context: article, comments (principaux), comment_form, user_likes
    # 404: Si l'article n'existe pas
```

#### article_edit(request, pk)
```python
@login_required
def article_edit(request, pk):
    # GET: Affiche le formulaire de modification
    # POST: Modifie l'article
    # Permission: Auteur ou Admin
```

#### article_delete(request, pk)
```python
@login_required
def article_delete(request, pk):
    # GET: Demande confirmation
    # POST: Supprime l'article
    # Permission: Auteur ou Admin
```

### Like Views

#### toggle_like(request, pk)
```python
@login_required
@require_http_methods(["POST"])
def toggle_like(request, pk):
    # POST: Toggle (ajoute ou retire) un like
    # Response: JSON si AJAX, sinon redirection
    # JSON: {"liked": bool, "likes_count": int}
```

### Comment Views

#### add_comment(request, pk)
```python
@login_required
def add_comment(request, pk):
    # POST: Crée un commentaire ou une réponse
    # Paramètre: parent_id (optionnel) pour les réponses
    # Redirection: Page d'article
```

#### comment_delete(request, pk)
```python
@login_required
def comment_delete(request, pk):
    # POST: Supprime un commentaire
    # Permission: Auteur ou Admin
```

### Search Views

#### search_articles(request)
```python
def search_articles(request):
    # GET: Recherche dans title et content
    # Paramètre: q (terme de recherche)
    # Context: articles, query
```

---

## Dépendances

### Packages Python

| Package | Version | Raison |
|---------|---------|--------|
| Django | 5.2.10 | Framework web principal |
| Pillow | 10.1.0 | Traitement des images |
| sqlparse | 0.4.4 | Parsing SQL (requis par Django) |
| asgiref | 3.7.2 | Utilitaires ASGI |
| tzdata | 2023.3 | Données de fuseau horaire |

### Packages Externes (CDN)

| Package | Version | Raison |
|---------|---------|--------|
| Bootstrap | 5.3.0 | Framework CSS |

### Modules Django Intégrés

- `django.contrib.admin` - Interface d'administration
- `django.contrib.auth` - Authentification
- `django.contrib.contenttypes` - Types de contenu
- `django.contrib.sessions` - Gestion de sessions
- `django.contrib.messages` - Messages aux utilisateurs
- `django.contrib.staticfiles` - Fichiers statiques

---

## Configuration Django

### INSTALLED_APPS
```python
[
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'blog',  # Notre app
    'django.contrib.staticfiles',
]
```

### MIDDLEWARE
```python
[
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # Protection CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

### TEMPLATES
```python
[
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

### BASE DE DONNÉES
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### MEDIA FILES
```python
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### AUTHENTIFICATION
```python
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
```

---

## Conseils de Développement

### Optimisation des Requêtes

**Mauvais:**
```python
# N+1 queries
for article in Article.objects.all():
    print(article.author.username)  # Une requête par article!
```

**Bon:**
```python
# Une seule requête avec select_related
for article in Article.objects.select_related('author'):
    print(article.author.username)
```

### Pagination

```python
from django.core.paginator import Paginator

def article_list(request):
    articles = Article.objects.all()
    paginator = Paginator(articles, 10)  # 10 par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/article_list.html', {'page_obj': page_obj})
```

### Cache

```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # 15 minutes
def article_list(request):
    # ...
```

---

## Testing

### Tests Unitaires

```python
from django.test import TestCase, Client
from django.contrib.auth.models import User
from blog.models import Article

class ArticleTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com', 'pass')
        self.article = Article.objects.create(
            title='Test',
            content='Content',
            author=self.user
        )
    
    def test_article_creation(self):
        self.assertEqual(self.article.title, 'Test')
    
    def test_article_detail_view(self):
        client = Client()
        response = client.get(f'/article/{self.article.pk}/')
        self.assertEqual(response.status_code, 200)
```

---

## Performance

### Optimisations Appliquées

1. **select_related()**: Pour les ForeignKey
2. **prefetch_related()**: Pour les ManyToMany et reverse FK
3. **only()/defer()**: Pour sélectionner des champs spécifiques
4. **Cache**: Pour les vues fréquemment accédées
5. **Pagination**: Pour les listes longues
6. **Compression statique**: CSS/JS minifiés

---

**Document créé le**: 21 Janvier 2026
**Version**: 1.0.0
**Auteur**: Équipe Développement
