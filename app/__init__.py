# app/__init__.py - Initialisation de l'application Flask
# Ce fichier configure l'application Flask, définit les dossiers de templates et statiques,
# et initialise la base de données

# Import de Flask pour créer l'application
from flask import Flask

# Création de l'application Flask avec configuration des dossiers
# template_folder='../templates' : dossier des templates HTML
# static_folder='../static' : dossier des fichiers statiques (CSS, JS, images)
app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Clé secrète pour les sessions Flask (à changer en production)
app.secret_key = "dev-secret-key"  # Change this in production

# Import des routes et modèles pour enregistrer les vues et fonctions de base de données
from app import routes
from app.models import setup_database, teardown_appcontext

# Enregistrement des fonctions de nettoyage de la base de données
# teardown_appcontext : ferme la connexion DB à la fin de chaque requête
app.teardown_appcontext(teardown_appcontext)

# Initialisation de la base de données au démarrage de l'application
setup_database()