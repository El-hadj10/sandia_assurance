# app/__init__.py - Initialisation de l'application Flask
# Ce fichier configure l'application Flask, définit les dossiers de templates et statiques,
# initialise la base de données, et active les mesures de sécurité

# Import de Flask et extensions de sécurité
from flask import Flask
from flask_wtf.csrf import CSRFProtect  # Protection CSRF
from flask_limiter import Limiter  # Rate limiting
from flask_limiter.util import get_remote_address  # Identifier les clients
import os

# Création de l'application Flask avec configuration des dossiers
# template_folder='../templates' : dossier des templates HTML
# static_folder='../static' : dossier des fichiers statiques (CSS, JS, images)
app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Configuration de sécurité
# Clé secrète pour les sessions Flask (lire depuis variable d'environnement en production)
app.secret_key = os.environ.get('SECRET_KEY', "dev-secret-key-change-in-production")

# Configuration sécurisée des sessions
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Pas d'accès JavaScript
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Protection CSRF supplémentaire
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # Session expires après 1 heure

# Initialisation de la protection CSRF (token vérifié automatiquement sur POST/PUT/DELETE)
csrf = CSRFProtect(app)

# Initialisation du rate limiting pour protéger contre les attaques par force brute
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],  # Limites globales
    storage_uri="memory://"  # Stockage en mémoire (utiliser Redis en production)
)

# Import des routes et modèles pour enregistrer les vues et fonctions de base de données
from app import routes
from app.models import setup_database, teardown_appcontext

# Enregistrement des fonctions de nettoyage de la base de données
# teardown_appcontext : ferme la connexion DB à la fin de chaque requête
app.teardown_appcontext(teardown_appcontext)

# Ajout des headers de sécurité HTTP
@app.after_request
def add_security_headers(response):
    # X-Content-Type-Options : prévient la détection MIME
    response.headers['X-Content-Type-Options'] = 'nosniff'
    # X-Frame-Options : protège contre le clickjacking
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    # X-XSS-Protection : protection XSS legacy
    response.headers['X-XSS-Protection'] = '1; mode=block'
    # Referrer-Policy : contrôle les informations de referrer
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    # Permissions-Policy : contrôle l'accès aux fonctionnalités du navigateur
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    # Content-Security-Policy : protège contre les injections XSS
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
    return response

# Initialisation de la base de données au démarrage de l'application
setup_database()