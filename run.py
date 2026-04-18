# run.py - Point d'entrée principal de l'application Flask
# Ce fichier importe l'application Flask et la lance en mode développement

# Import de l'application Flask depuis le module app
from app import app

# Bloc principal : exécute l'application seulement si ce fichier est lancé directement
if __name__ == "__main__":
    # Lance l'application Flask en mode debug, accessible sur toutes les interfaces réseau, port 5002
    app.run(debug=True, host="0.0.0.0", port=5002)