@echo off
REM Script de démarrage rapide pour le Blog Interactif

echo.
echo ====================================
echo   BLOG INTERACTIF - Demarrage
echo ====================================
echo.

REM Vérifier que nous sommes dans le bon répertoire
if not exist manage.py (
    echo Erreur: manage.py non trouvé!
    echo Assurez-vous d'être dans le répertoire blog_project
    pause
    exit /b 1
)

REM Activer venv si nécessaire
if exist venv\Scripts\activate.bat (
    echo Activation de l'environnement virtuel...
    call venv\Scripts\activate.bat
    echo ✓ Environnement virtuel activé
)

echo.
echo Démarrage du serveur de développement...
echo.
echo   URL: http://localhost:8000
echo   Admin: http://localhost:8000/admin
echo.
echo   Login: admin
echo   Password: admin123
echo.
echo Appuyez sur CTRL+C pour arrêter le serveur
echo.

python manage.py runserver
