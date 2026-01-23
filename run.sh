#!/bin/bash
# Script de démarrage rapide pour le Blog Interactif

echo ""
echo "===================================="
echo "  BLOG INTERACTIF - Demarrage"
echo "===================================="
echo ""

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f manage.py ]; then
    echo "Erreur: manage.py non trouvé!"
    echo "Assurez-vous d'être dans le répertoire blog_project"
    exit 1
fi

# Activer venv si nécessaire
if [ -f venv/bin/activate ]; then
    echo "Activation de l'environnement virtuel..."
    source venv/bin/activate
    echo "✓ Environnement virtuel activé"
fi

echo ""
echo "Démarrage du serveur de développement..."
echo ""
echo "  URL: http://localhost:8000"
echo "  Admin: http://localhost:8000/admin"
echo ""
echo "  Login: admin"
echo "  Password: admin123"
echo ""
echo "Appuyez sur CTRL+C pour arrêter le serveur"
echo ""

python manage.py runserver
