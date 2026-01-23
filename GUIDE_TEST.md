# Guide de Test - Blog Interactif

Ce guide vous permet de tester toutes les fonctionnalités de l'application Blog Interactif.

## 🚀 Démarrage rapide

### 1. Lancer le serveur
```bash
cd c:\Users\MOUANGA\blog_project
python manage.py runserver
```

L'application est accessible à: **http://localhost:8000**

### 2. Accéder à l'admin
- URL: **http://localhost:8000/admin/**
- Utilisateur: `admin`
- Mot de passe: `admin123`

---

## 👤 Comptes de Test

Quatre comptes sont disponibles pour les tests:

| Utilisateur | Mot de passe | Rôle |
|------------|--------------|------|
| admin | admin123 | Superutilisateur |
| jean | password123 | Utilisateur normal |
| marie | password123 | Utilisateur normal |
| pierre | password123 | Utilisateur normal |

---

## 🧪 Scénarios de Test

### Scénario 1: Inscription et Connexion

#### Test 1.1: Inscription réussie
1. Aller à **http://localhost:8000/register/**
2. Remplir le formulaire:
   - Username: `testuser`
   - Email: `testuser@test.com`
   - Mot de passe: `SecurePass123!`
   - Confirmer: `SecurePass123!`
3. Cliquer **S'inscrire**
4. ✅ Vérifier: Redirection vers l'accueil, utilisateur connecté

#### Test 1.2: Inscription avec email existant
1. Aller à **http://localhost:8000/register/**
2. Utiliser: `admin@blog.local`
3. ✅ Vérifier: Erreur "Cet email est déjà utilisé"

#### Test 1.3: Connexion réussie
1. Aller à **http://localhost:8000/login/**
2. Username: `admin`
3. Mot de passe: `admin123`
4. Cliquer **Se connecter**
5. ✅ Vérifier: Redirection vers l'accueil, barre de navigation montre "admin"

#### Test 1.4: Connexion échouée
1. Aller à **http://localhost:8000/login/**
2. Username: `admin`
3. Mot de passe: `wrongpassword`
4. ✅ Vérifier: Erreur "Nom d'utilisateur ou mot de passe incorrect"

#### Test 1.5: Déconnexion
1. Se connecter avec `admin / admin123`
2. Cliquer sur le dropdown avec le nom d'utilisateur
3. Cliquer **Déconnexion**
4. ✅ Vérifier: Redirection vers l'accueil, barre de navigation montre "Connexion/Inscription"

---

### Scénario 2: Gestion des Articles

#### Test 2.1: Créer un article (connecté)
1. Se connecter avec `admin / admin123`
2. Cliquer **✏️ Créer** dans la barre de navigation
3. Remplir:
   - Titre: `Mon premier article`
   - Contenu: `Ceci est le contenu de mon article`
   - Image: (optionnel)
4. Cliquer **Publier**
5. ✅ Vérifier: Article créé et affiché sur la page d'accueil

#### Test 2.2: Accès refusé à la création (non connecté)
1. Se déconnecter
2. Accéder directement à **http://localhost:8000/article/create/**
3. ✅ Vérifier: Redirection vers la page de connexion

#### Test 2.3: Lire le détail d'un article
1. Sur la page d'accueil, cliquer **Lire plus** sur un article
2. ✅ Vérifier: 
   - Titre, auteur, date affichés
   - Contenu complet visible
   - Section commentaires visible
   - Compteur de likes et commentaires affichés

#### Test 2.4: Modifier un article (auteur)
1. Se connecter avec le compte qui a créé l'article
2. Aller au détail de l'article
3. Cliquer **✏️ Modifier**
4. Changer le titre
5. Cliquer **Mettre à jour**
6. ✅ Vérifier: Article modifié, nouveau titre affiché

#### Test 2.5: Accès refusé modification (non auteur)
1. Se connecter avec `jean`
2. Aller au détail d'un article créé par `admin`
3. ✅ Vérifier: Pas de bouton "Modifier"

#### Test 2.6: Supprimer un article (auteur)
1. Se connecter avec le compte qui a créé l'article
2. Aller au détail de l'article
3. Cliquer **🗑️ Supprimer**
4. Cliquer **Confirmer la suppression**
5. ✅ Vérifier: 
   - Redirection vers l'accueil
   - Article plus visible nulle part

#### Test 2.7: Lister tous les articles
1. Cliquer **Articles** dans la barre de navigation
2. ✅ Vérifier: Vue grille de tous les articles

---

### Scénario 3: Système de Likes

#### Test 3.1: Aimer un article
1. Se connecter avec `admin`
2. Sur la page d'accueil ou détail, cliquer **🤍**
3. ✅ Vérifier: 
   - Le cœur devient **❤️**
   - Le compteur augmente de 1

#### Test 3.2: Dés-aimer un article
1. Après avoir aimé un article, cliquer **❤️**
2. ✅ Vérifier: 
   - Le cœur redevient **🤍**
   - Le compteur diminue de 1

#### Test 3.3: Multiple likes (plusieurs utilisateurs)
1. Se connecter avec `admin` et aimer un article
2. Se déconnecter
3. Se connecter avec `jean` et aimer le même article
4. ✅ Vérifier: Le compteur affiche 2

#### Test 3.4: Accès refusé like (non connecté)
1. Se déconnecter
2. ✅ Vérifier: 
   - Le cœur affiche **🤍** sans interactivité
   - Message "connectez-vous" visible

#### Test 3.5: Like ne doit être possible qu'une fois par utilisateur
1. Se connecter avec `admin`
2. Aimer un article
3. ✅ Vérifier: Cliquer à nouveau retire le like (toggle)

---

### Scénario 4: Système de Commentaires

#### Test 4.1: Commenter un article (connecté)
1. Se connecter avec `jean`
2. Aller au détail d'un article
3. Remplir le formulaire de commentaire: `Très bon article!`
4. Cliquer **Poster**
5. ✅ Vérifier: 
   - Commentaire affiché
   - Auteur (`jean`) affiché
   - Date de création affichée
   - Compteur de commentaires augmenté

#### Test 4.2: Répondre à un commentaire
1. Se connecter avec `marie`
2. Aller au détail d'un article qui a un commentaire
3. Cliquer **Répondre** sous un commentaire
4. Remplir: `Je suis d'accord!`
5. Cliquer **Répondre**
6. ✅ Vérifier: 
   - Réponse indentée sous le commentaire
   - Affichage hiérarchique correct

#### Test 4.3: Commentaires imbriqués profonds
1. Répondre à une réponse
2. ✅ Vérifier: Indentation correcte (2ème niveau)

#### Test 4.4: Affichage du compteur de commentaires
1. Naviguer vers un article avec plusieurs commentaires
2. ✅ Vérifier: Compteur affiche le nombre TOTAL (commentaires + réponses)

#### Test 4.5: Supprimer un commentaire (auteur)
1. Se connecter avec `jean`
2. Aller au détail d'un article avec un commentaire créé par `jean`
3. Cliquer **Supprimer**
4. ✅ Vérifier: 
   - Commentaire supprimé
   - Compteur mis à jour

#### Test 4.6: Supprimer un commentaire (admin)
1. Se connecter avec `admin`
2. Aller au détail d'un article avec un commentaire créé par quelqu'un d'autre
3. ✅ Vérifier: 
   - Bouton **Supprimer** visible (admin peut tout supprimer)
   - Commentaire supprimé après clic

#### Test 4.7: Accès refusé commentaire (non connecté)
1. Se déconnecter
2. Aller au détail d'un article
3. ✅ Vérifier: 
   - Message "Vous devez être connecté pour commenter"
   - Liens de connexion/inscription visibles

#### Test 4.8: Compteur de commentaires hiérarchique
1. Vérifier qu'un article a 3 commentaires et 2 réponses
2. ✅ Vérifier: Compteur affiche **5** (pas seulement les parents)

---

### Scénario 5: Recherche

#### Test 5.1: Recherche réussie
1. Utiliser la barre de recherche en haut à droite
2. Entrer: `Django`
3. ✅ Vérifier: Articles contenant "Django" affichés

#### Test 5.2: Recherche sans résultats
1. Utiliser la barre de recherche
2. Entrer: `XYZQWERTY`
3. ✅ Vérifier: Message "Aucun résultat"

#### Test 5.3: Recherche vide
1. Cliquer sur 🔍 sans rien entrer
2. ✅ Vérifier: Message approprié

#### Test 5.4: Recherche insensible à la casse
1. Chercher: `django` (minuscule)
2. ✅ Vérifier: Résultats identiques à la recherche `Django`

---

### Scénario 6: Responsive Design

#### Test 6.1: Mobile (320px)
1. Ouvrir DevTools (F12)
2. Sélectionner "Mobile" (iPhone SE)
3. ✅ Vérifier: 
   - Barre de navigation adaptée
   - Menu burger visible
   - Articles en colonne unique
   - Commentaires lisibles

#### Test 6.2: Tablet (768px)
1. Sélectionner "iPad"
2. ✅ Vérifier: Layout adapté

#### Test 6.3: Desktop (1920px)
1. Écran complet
2. ✅ Vérifier: Layout desktop normal

---

### Scénario 7: Panel Admin

#### Test 7.1: Accéder à l'admin
1. Aller à **http://localhost:8000/admin/**
2. Connexion: `admin / admin123`
3. ✅ Vérifier: Dashboard admin visible

#### Test 7.2: Gérer les articles
1. Admin > Articles
2. ✅ Vérifier: 
   - Liste de tous les articles
   - Filtres par auteur et date
   - Recherche fonctionnelle
   - Nombre de likes et commentaires affichés

#### Test 7.3: Gérer les commentaires
1. Admin > Commentaires
2. ✅ Vérifier: 
   - Liste de tous les commentaires
   - Colonne "Est une réponse?"
   - Filtres par article et auteur

#### Test 7.4: Ajouter un utilisateur (admin)
1. Admin > Utilisateurs > Ajouter
2. Créer: `testadmin` avec email et mot de passe
3. ✅ Vérifier: Utilisateur créé

---

### Scénario 8: Erreurs et Cas Limites

#### Test 8.1: Article inexistant
1. Accéder à **http://localhost:8000/article/9999/**
2. ✅ Vérifier: Erreur 404

#### Test 8.2: Commentaire inexistant
1. Accéder à **http://localhost:8000/comment/9999/delete/**
2. ✅ Vérifier: Erreur 404

#### Test 8.3: Article sans image de couverture
1. Créer un article sans image
2. ✅ Vérifier: Page fonctionne, pas de placeholder vide

#### Test 8.4: Article très long
1. Créer un article avec 5000+ caractères
2. ✅ Vérifier: Affichage correct, pas de débordement

#### Test 8.5: Titre très long
1. Créer un article avec titre de 200 caractères
2. ✅ Vérifier: Troncature correcte si nécessaire

---

### Scénario 9: Performance

#### Test 9.1: Page avec beaucoup d'articles
1. Créer 50+ articles
2. Accéder à la page d'accueil
3. ✅ Vérifier: Chargement rapide (< 2 secondes)

#### Test 9.2: Article avec beaucoup de commentaires
1. Créer un article avec 100+ commentaires
2. Accéder au détail
3. ✅ Vérifier: Chargement acceptable

---

### Scénario 10: Sécurité

#### Test 10.1: CSRF Protection
1. Créer un article
2. Ouvrir DevTools (F12)
3. Vérifier la présence du token CSRF dans les formulaires
4. ✅ Vérifier: Token présent dans tous les formulaires

#### Test 10.2: SQL Injection (recherche)
1. Chercher: `" OR "1"="1`
2. ✅ Vérifier: Pas de résultats inattendus, pas d'erreur

#### Test 10.3: Modification d'URL
1. Se connecter avec `jean`
2. Modifier l'URL: `/article/1/edit/` (article d'un autre)
3. ✅ Vérifier: Redirection, pas de modification possible

#### Test 10.4: Suppression d'URL
1. Se connecter avec `jean`
2. Accéder à `/article/1/delete/` (article d'un autre)
3. ✅ Vérifier: Redirection, pas de suppression possible

---

## 📊 Checklist de Test

```
✅ Authentification
  ✓ Inscription
  ✓ Connexion
  ✓ Déconnexion
  ✓ Validation des formulaires

✅ Articles
  ✓ Créer
  ✓ Lire
  ✓ Modifier (auteur)
  ✓ Supprimer (auteur)
  ✓ Permissions

✅ Likes
  ✓ Aimer un article
  ✓ Dés-aimer un article
  ✓ Compteur
  ✓ Une fois par utilisateur

✅ Commentaires
  ✓ Commenter
  ✓ Répondre
  ✓ Hiérarchie
  ✓ Supprimer
  ✓ Compteur
  ✓ Permissions

✅ Recherche
  ✓ Résultats corrects
  ✓ Pas de résultats
  ✓ Insensible à la casse

✅ UI/UX
  ✓ Responsive design
  ✓ Navigation
  ✓ Messages d'erreur
  ✓ Formulaires valides

✅ Admin
  ✓ Articles
  ✓ Commentaires
  ✓ Utilisateurs
  ✓ Filtres et recherche

✅ Sécurité
  ✓ CSRF protection
  ✓ Authentification requise
  ✓ Permissions
  ✓ Injection SQL
```

---

## 🐛 Rapporter des Bugs

Si vous trouvez des bugs, notez:
1. **Étapes à reproduire**: Comment faire pour reproduire le bug
2. **Résultat attendu**: Ce qui devrait se passer
3. **Résultat réel**: Ce qui s'est passé réellement
4. **Navigateur/OS**: Votre environnement
5. **Screenshots**: Si applicable

---

## 💡 Notes

- Les migrations ont été exécutées automatiquement
- Les données de test sont déjà chargées
- Le serveur peut être arrêté avec `Ctrl+C`
- Les fichiers uploadés sont dans `media/`
- Toutes les erreurs sont visibles dans la console Django

---

**Date**: 21 Janvier 2026
**Version**: 1.0.0
