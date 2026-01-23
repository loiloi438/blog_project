# Blog Interactif - Module Django

Une application web complète de blog avec système d'interaction sociale (J'aime, Commentaires, Réponses) développée avec Django et Bootstrap.

## 🎯 Fonctionnalités

### 1. Gestion des Utilisateurs
- ✅ Inscription de nouveaux utilisateurs
- ✅ Système de connexion/déconnexion sécurisé
- ✅ Protection des actions par authentification
- ✅ Profils utilisateurs

### 2. Gestion des Articles
- ✅ Création d'articles (avec image de couverture optionnelle)
- ✅ Liste des articles triés par date décroissante
- ✅ Page de détail complète pour chaque article
- ✅ Modification des articles (seulement l'auteur)
- ✅ Suppression des articles (seulement l'auteur)

### 3. Système de J'aime
- ✅ Un utilisateur ne peut aimer un article qu'une seule fois
- ✅ Toggle des likes (aimer/dés-aimer)
- ✅ Affichage du nombre total de likes
- ✅ Compteur de likes en temps réel

### 4. Système de Commentaires Hiérarchiques
- ✅ Commentaires sur les articles
- ✅ Réponses aux commentaires (commentaires imbriqués)
- ✅ Affichage hiérarchique avec indentation
- ✅ Compteur de commentaires total
- ✅ Suppression des commentaires (seulement l'auteur)

### 5. Fonctionnalités Bonus
- ✅ Moteur de recherche d'articles
- ✅ Panel administrateur complet
- ✅ Design responsive (mobile-friendly)
- ✅ Données de test pré-chargées

## 🛠️ Stack Technique

- **Backend**: Python 3.x + Django 5.2
- **Frontend**: HTML5 + CSS3 + JavaScript + Bootstrap 5
- **Base de données**: SQLite (dev) / Configurable pour production
- **ORM**: Django ORM

## 📦 Installation

### Prérequis
- Python 3.8+
- pip
- Virtual Environment (recommandé)

### Étapes

1. **Cloner le projet**
```bash
git clone <repository-url>
cd blog_project
```

2. **Créer un environnement virtuel**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Exécuter les migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Initialiser la base de données avec les données de test**
```bash
python init_db.py
```

6. **Lancer le serveur de développement**
```bash
python manage.py runserver
```

7. **Accéder à l'application**
- Application: http://localhost:8000
- Admin: http://localhost:8000/admin

### Identifiants de test
- **Admin**: admin / admin123
- **Utilisateurs de test**: jean, marie, pierre (tous avec mot de passe: password123)

## 📁 Structure du Projet

```
blog_project/
├── blog/                          # Application principale Django
│   ├── migrations/               # Fichiers de migration
│   ├── admin.py                  # Configuration admin Django
│   ├── forms.py                  # Formulaires (Article, Comment, Auth)
│   ├── models.py                 # Modèles (Article, Comment, User)
│   ├── urls.py                   # Routage des URLs
│   ├── views.py                  # Logique des vues
│   └── __init__.py
├── blog_project/                 # Configuration du projet
│   ├── settings.py               # Paramètres Django
│   ├── urls.py                   # URLs racine
│   ├── wsgi.py                   # WSGI pour production
│   └── asgi.py                   # ASGI pour production
├── templates/                     # Templates HTML
│   └── blog/
│       ├── base.html             # Template de base
│       ├── home.html             # Page d'accueil
│       ├── login.html            # Page de connexion
│       ├── register.html         # Page d'inscription
│       ├── article_form.html     # Formulaire article
│       ├── article_detail.html   # Détail article + commentaires
│       ├── article_list.html     # Liste articles
│       ├── article_confirm_delete.html  # Confirmation suppression
│       ├── comment_thread.html   # Commentaires hiérarchiques
│       └── search_results.html   # Résultats recherche
├── media/                        # Fichiers uploadés (images d'articles)
├── db.sqlite3                    # Base de données
├── manage.py                     # Gestionnaire Django
├── init_db.py                    # Script d'initialisation
├── requirements.txt              # Dépendances Python
└── README.md                     # Ce fichier

```

## 🗄️ Modèles de Données

### Article
- `title` : CharField - Titre de l'article
- `content` : TextField - Contenu texte
- `author` : ForeignKey(User) - Auteur
- `cover_image` : ImageField - Image de couverture optionnelle
- `created_at` : DateTimeField - Date de création
- `updated_at` : DateTimeField - Date de modification
- `likes` : ManyToManyField(User) - Utilisateurs qui ont aimé

### Comment
- `article` : ForeignKey(Article) - Article commenté
- `author` : ForeignKey(User) - Auteur du commentaire
- `body` : TextField - Contenu du commentaire
- `created_at` : DateTimeField - Date de création
- `updated_at` : DateTimeField - Date de modification
- `parent` : ForeignKey(self, null=True) - Commentaire parent (pour les réponses)

## 🔐 Sécurité

- ✅ Protection CSRF sur tous les formulaires
- ✅ Authentification requise pour certaines actions
- ✅ Vérification des permissions (auteur ou staff)
- ✅ Validation des formulaires Django
- ✅ Hashage sécurisé des mots de passe

## 📝 Utilisation

### Publier un Article
1. Se connecter
2. Cliquer sur "✏️ Créer"
3. Remplir le formulaire (Titre, Contenu, Image optionnelle)
4. Cliquer sur "Publier"

### Aimer un Article
1. Se connecter
2. Cliquer sur "🤍" pour aimer
3. Le cœur devient "❤️" et le compteur augmente
4. Cliquer à nouveau pour dés-aimer

### Commenter un Article
1. Se connecter
2. Aller au détail de l'article
3. Remplir le formulaire de commentaire
4. Cliquer sur "Poster"

### Répondre à un Commentaire
1. Se connecter
2. Cliquer sur "Répondre" sous un commentaire
3. Remplir le formulaire
4. Cliquer sur "Répondre"

### Rechercher des Articles
1. Utiliser la barre de recherche en haut à droite
2. Entrer des mots-clés
3. Les résultats afficheront les articles correspondants

## 🚀 Déploiement

### Configuration pour Production

1. **Modifier settings.py**
```python
DEBUG = False
ALLOWED_HOSTS = ['votredomaine.com']
SECRET_KEY = 'votre-nouvelle-clé-secrète'
```

2. **Installer les dépendances de production**
```bash
pip install gunicorn
```

3. **Collecter les fichiers statiques**
```bash
python manage.py collectstatic
```

4. **Déployer avec Gunicorn**
```bash
gunicorn blog_project.wsgi:application --bind 0.0.0.0:8000
```

### Hébergement Recommandé
- Heroku
- PythonAnywhere
- DigitalOcean
- AWS (EC2)

## 📊 Base de données

### SQLite (Développement)
- Idéal pour le développement local
- Pas de configuration requise

### PostgreSQL (Production)
```bash
pip install psycopg2-binary
```

Modifier settings.py:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'blog_db',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🐛 Troubleshooting

### Erreur: "No module named 'blog'"
```bash
# S'assurer que blog est dans INSTALLED_APPS
# Vérifier que vous êtes dans le bon répertoire
```

### Images ne s'affichent pas
```bash
# Vérifier que MEDIA_ROOT et MEDIA_URL sont configurés
# Créer le répertoire media/ s'il n'existe pas
mkdir media
```

### Migrations échouent
```bash
# Supprimer les fichiers migration
# Supprimer la base de données
rm db.sqlite3
# Recommencer
python manage.py makemigrations
python manage.py migrate
```

## 📝 Modules Python Utilisés

```
Django==5.2.10
Pillow==10.x.x (pour les images)
```

Voir `requirements.txt` pour la liste complète.

## 👤 Auteur

Développé pour Gaetane MVIBUNDULU

## 📜 Licence

MIT License

## 📧 Support

Pour toute question ou problème, contactez l'équipe de développement.

---

**Dernière mise à jour**: Janvier 2026
**Version**: 1.0.0
