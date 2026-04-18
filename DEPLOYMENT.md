# Guide de Déploiement - Sandia Assurance

## Prérequis

- Python 3.8+
- pip
- virtualenv
- Redis (pour le rate limiting en production)
- Gunicorn (serveur WSGI)
- Un serveur web (Nginx recommandé)

## Installation

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/El-hadj10/sandia_assurance.git
   cd sandia_assurance
   ```

2. **Créer l'environnement virtuel**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Sur Windows: .venv\Scripts\activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration**
   ```bash
   cp .env.example .env
   # Éditez .env avec vos valeurs de production
   nano .env
   ```

   **IMPORTANT :** Changez `SECRET_KEY` en une valeur unique et sécurisée !

## Déploiement en Production

### Avec Gunicorn

1. **Installer Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **Lancer l'application**
   ```bash
   gunicorn --bind 0.0.0.0:8000 run:app
   ```

3. **Configuration Gunicorn (recommandé)**
   Créez `gunicorn.conf.py` :
   ```python
   bind = "0.0.0.0:8000"
   workers = 3
   worker_class = "sync"
   worker_connections = 1000
   timeout = 30
   keepalive = 2
   ```

   Lancez avec :
   ```bash
   gunicorn --config gunicorn.conf.py run:app
   ```

### Avec Nginx (Proxy)

1. **Configuration Nginx** (`/etc/nginx/sites-available/sandia_assurance`)
   ```nginx
   server {
       listen 80;
       server_name votre-domaine.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       location /static {
           alias /chemin/vers/votre/projet/static;
           expires 1y;
           add_header Cache-Control "public, immutable";
       }
   }
   ```

2. **Activer le site**
   ```bash
   sudo ln -s /etc/nginx/sites-available/sandia_assurance /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

### Avec Docker (Optionnel)

1. **Dockerfile**
   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt

   COPY . .
   EXPOSE 8000

   CMD ["gunicorn", "--bind", "0.0.0.0:8000", "run:app"]
   ```

2. **Construire et lancer**
   ```bash
   docker build -t sandia-assurance .
   docker run -p 8000:8000 sandia-assurance
   ```

## Sécurité en Production

- **HTTPS obligatoire** : Configurez SSL/TLS avec Let's Encrypt
- **Variables d'environnement** : Ne commitez jamais `.env` dans Git
- **Mises à jour** : Gardez les dépendances à jour
- **Sauvegardes** : Sauvegardez régulièrement la base de données
- **Monitoring** : Surveillez les logs et les performances

## Base de Données

- **SQLite** : Suffisant pour le développement et petits déploiements
- **PostgreSQL** : Recommandé pour la production
  - Changez `DATABASE_URL` dans `.env`
  - Installez `psycopg2` : `pip install psycopg2-binary`

## Rate Limiting

- **Développement** : Utilise la mémoire (Limiter)
- **Production** : Configurez Redis dans `.env`
  ```bash
  REDIS_URL=redis://localhost:6379/0
  ```

## Dépannage

- **Erreur 500** : Vérifiez les logs Gunicorn
- **Rate limiting** : Vérifiez la configuration Redis
- **Base de données** : Testez la connexion avec `python3 -c "from app import db; db.create_all()"`
- **Permissions** : Assurez-vous que l'utilisateur peut écrire dans le dossier

## Support

Pour toute question, consultez la documentation ou contactez l'équipe de développement.