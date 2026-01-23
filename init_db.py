#!/usr/bin/env python
"""
Script pour initialiser le blog avec un superutilisateur et des données de test
"""
import os
import sys
import django
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

django.setup()

from django.contrib.auth.models import User
from blog.models import Article, Comment

def create_admin_user():
    """Créer l'utilisateur admin s'il n'existe pas"""
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@blog.local',
            password='admin123'
        )
        print(f"✓ Super utilisateur créé: admin / admin123")
        return admin_user
    else:
        print("✓ Admin utilisateur existe déjà")
        return User.objects.get(username='admin')

def create_test_users():
    """Créer des utilisateurs de test"""
    users = []
    usernames = ['jean', 'marie', 'pierre']
    
    for username in usernames:
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=f'{username}@blog.local',
                password='password123'
            )
            print(f"✓ Utilisateur créé: {username}")
            users.append(user)
        else:
            users.append(User.objects.get(username=username))
    
    return users

def create_test_articles(admin_user, test_users):
    """Créer des articles de test"""
    if Article.objects.exists():
        print("✓ Articles existent déjà")
        return
    
    articles_data = [
        {
            'title': 'Bienvenue sur mon blog!',
            'content': 'Ceci est mon premier article. Je suis ravi de partager mes pensées et mes expériences avec vous!\n\nN\'hésitez pas à commenter et à participer à la discussion.',
            'author': admin_user
        },
        {
            'title': 'Comment démarrer avec Django',
            'content': 'Django est un excellent framework Python pour développer des applications web. Voici quelques conseils pour bien démarrer:\n\n1. Installez Django avec pip\n2. Créez un projet\n3. Créez une application\n4. Définissez vos modèles\n5. Créez les vues\n\nC\'est facile!',
            'author': test_users[0]
        },
        {
            'title': 'Les meilleures pratiques en développement web',
            'content': 'La sécurité, les performances et la maintenabilité sont les trois piliers d\'une bonne application web.\n\nDans cet article, nous discuterons de comment les atteindre dans votre projet.',
            'author': test_users[1]
        },
    ]
    
    for data in articles_data:
        article = Article.objects.create(**data)
        print(f"✓ Article créé: {article.title}")
        
        # Ajouter quelques likes
        if test_users:
            article.likes.add(*test_users[:2])

def create_test_comments(articles, users):
    """Créer des commentaires de test"""
    if Comment.objects.exists():
        print("✓ Commentaires existent déjà")
        return
    
    articles_list = list(articles)
    
    if len(articles_list) > 0:
        # Commentaires sur le premier article
        comment1 = Comment.objects.create(
            article=articles_list[0],
            author=users[0],
            body="Excellent article! Très utile pour les débutants."
        )
        print(f"✓ Commentaire créé")
        
        # Réponse au premier commentaire
        reply1 = Comment.objects.create(
            article=articles_list[0],
            author=users[1],
            body="Je suis d'accord! Django c'est super!",
            parent=comment1
        )
        print(f"✓ Réponse créée")
        
        # Commentaire sur le deuxième article
        if len(articles_list) > 1:
            comment2 = Comment.objects.create(
                article=articles_list[1],
                author=users[2],
                body="Très instructif comme toujours!"
            )
            print(f"✓ Commentaire créé")

def main():
    print("\n" + "="*50)
    print("Initialisation du Blog Interactif")
    print("="*50 + "\n")
    
    # Créer l'admin
    admin_user = create_admin_user()
    
    # Créer des utilisateurs de test
    test_users = create_test_users()
    
    # Créer des articles de test
    create_test_articles(admin_user, test_users)
    
    # Créer des commentaires de test
    articles = Article.objects.all()
    create_test_comments(articles, test_users)
    
    print("\n" + "="*50)
    print("✓ Initialisation terminée!")
    print("="*50)
    print("\nAccès admin: http://localhost:8000/admin/")
    print("Utilisateur: admin")
    print("Mot de passe: admin123")
    print("\n" + "="*50 + "\n")

if __name__ == '__main__':
    main()
