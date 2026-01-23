# DEPLOIEMENT.md - Guide de Déploiement

## 🚀 Préparation pour la Production

### 1. Configuration Locale

#### Cloner et configurer
```bash
git clone <repository-url>
cd blog_project
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows

pip install -r requirements.txt
pip install gunicorn python-decouple
```

#### Créer le fichier .env
```bash
cp .env.example .env
# Éditer .env avec vos paramètres
```

#### Créer la base de données
```bash
python manage.py migrate --settings=settings_production
python manage.py collectstatic --noinput --settings=settings_production
```

---

## ☁️ Déploiement sur Heroku

### Configuration préalable
1. Installer Heroku CLI
2. Connectez-vous: `heroku login`

### Procédure

#### 1. Créer l'application
```bash
heroku create mon-blog-interactif
```

#### 2. Ajouter PostgreSQL
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

#### 3. Configurer les variables d'environnement
```bash
heroku config:set SECRET_KEY="votre-clé-super-secrète"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="mon-blog-interactif.herokuapp.com"
```

#### 4. Créer Procfile
```
web: gunicorn blog_project.wsgi:application --log-file -
```

#### 5. Créer requirements.txt pour production
```bash
pip freeze > requirements.txt
```

#### 6. Déployer
```bash
git push heroku main
```

#### 7. Appliquer les migrations
```bash
heroku run python manage.py migrate
heroku run python init_db.py
```

#### 8. Voir l'application
```bash
heroku open
```

---

## 🐳 Déploiement avec Docker

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le projet
COPY . .

# Créer le répertoire pour les logs
RUN mkdir -p logs

# Collecter les statiques
RUN python manage.py collectstatic --noinput

# Exposer le port
EXPOSE 8000

# Commande de démarrage
CMD ["gunicorn", "blog_project.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    command: >
      sh -c "python manage.py migrate &&
             python manage.py collectstatic --noinput &&
             gunicorn blog_project.wsgi:application --bind 0.0.0.0:8000"
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - SECRET_KEY=your-secret-key
      - ALLOWED_HOSTS=localhost,127.0.0.1
      - DB_ENGINE=django.db.backends.postgresql
      - DB_NAME=blog_db
      - DB_USER=postgres
      - DB_PASSWORD=postgres
      - DB_HOST=db
      - DB_PORT=5432
    depends_on:
      - db
    volumes:
      - ./media:/app/media
      - ./logs:/app/logs

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=blog_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### Lancer avec Docker
```bash
docker-compose build
docker-compose up
```

---

## 🖥️ Déploiement sur DigitalOcean

### 1. Créer un Droplet
- Sélectionner Ubuntu 22.04
- Taille: $6/mois minimum
- SSH key

### 2. Configuration du serveur
```bash
ssh root@votre_ip

# Mettre à jour
apt update && apt upgrade -y

# Installer les dépendances
apt install -y python3 python3-pip python3-venv postgresql nginx git

# Créer l'utilisateur
useradd -m -s /bin/bash blogger
su - blogger
```

### 3. Déployer l'application
```bash
cd /home/blogger
git clone <repository-url> blog_project
cd blog_project

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### 4. Configuration PostgreSQL
```bash
sudo -u postgres psql

CREATE DATABASE blog_db;
CREATE USER blog_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE blog_db TO blog_user;
\q
```

### 5. Configuration Systemd
Créer `/etc/systemd/system/blog.service`:
```ini
[Unit]
Description=Blog Interactif Django
After=network.target

[Service]
Type=notify
User=blogger
WorkingDirectory=/home/blogger/blog_project
ExecStart=/home/blogger/blog_project/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/run/gunicorn.sock \
    blog_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 6. Configuration Nginx
```nginx
server {
    listen 80;
    server_name votre_domaine.com;

    location / {
        proxy_pass http://unix:/run/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /home/blogger/blog_project/staticfiles/;
    }

    location /media/ {
        alias /home/blogger/blog_project/media/;
    }
}
```

### 7. Démarrer les services
```bash
sudo systemctl start blog
sudo systemctl enable blog
sudo systemctl restart nginx
```

### 8. SSL avec Let's Encrypt
```bash
apt install -y certbot python3-certbot-nginx
certbot --nginx -d votre_domaine.com
```

---

## 🔒 Checklist de Sécurité

- [ ] `DEBUG = False` en production
- [ ] `SECRET_KEY` changée et securisée
- [ ] `ALLOWED_HOSTS` configuré correctement
- [ ] HTTPS activé (SSL/TLS)
- [ ] Base de données sécurisée avec mot de passe fort
- [ ] Fichiers sensibles (`.env`, `settings.py`) pas en version
- [ ] Logs configurés et surveillés
- [ ] Sauvegardes régulières de la base de données
- [ ] Utilisateur admin avec mot de passe fort
- [ ] Firewalls configurés
- [ ] CDN pour les fichiers statiques (optionnel)
- [ ] Rate limiting activé (optionnel)

---

## 📊 Monitoring et Maintenance

### Logs
```bash
# Voir les logs
tail -f /var/log/syslog | grep blog

# Avec Heroku
heroku logs --tail
```

### Sauvegardes PostgreSQL
```bash
# Local
pg_dump blog_db > backup.sql

# Restaurer
psql blog_db < backup.sql

# Heroku
heroku pg:backups:capture
heroku pg:backups:download
```

### Mise à jour de l'application
```bash
cd /home/blogger/blog_project
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
systemctl restart blog
```

---

## 🆘 Troubleshooting

### Port déjà utilisé
```bash
lsof -i :8000
kill -9 <PID>
```

### Permissions Django
```bash
chown -R blogger:blogger /home/blogger/blog_project
```

### Collectstatic échoue
```bash
python manage.py collectstatic --clear --noinput
```

### Migrations échouent
```bash
python manage.py showmigrations
python manage.py migrate --plan
```

---

## 📈 Optimisation Performance

### Caching
- Activer le cache Redis
- Configurer `CACHES` dans `settings_production.py`

### CDN
- Utiliser CloudFront (AWS) pour les fichiers statiques
- Configurer `AWS_S3_CUSTOM_DOMAIN`

### Compression
- Ajouter `django-compressor`
- Compresser les CSS/JS

### Database
- Ajouter des indices sur les colonnes fréquemment interrogées
- Utiliser `select_related()` et `prefetch_related()` dans les vues

### Monitoring
```bash
pip install django-debug-toolbar  # Dev only
pip install sentry-sdk  # Production monitoring
```

---

## 💡 Ressources Supplémentaires

- [Django Deployment Guide](https://docs.djangoproject.com/en/5.2/howto/deployment/)
- [Heroku Django](https://devcenter.heroku.com/articles/django-app-configuration)
- [DigitalOcean Django](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

**Dernière mise à jour**: 21 Janvier 2026
**Version**: 1.0.0
