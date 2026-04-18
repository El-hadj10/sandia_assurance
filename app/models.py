# app/models.py - Modèles de données et fonctions de base de données
# Ce fichier définit les structures de données, la connexion à la base SQLite,
# et les fonctions CRUD pour les utilisateurs, paiements, dossiers, devis et contacts

# Import des modules nécessaires
import sqlite3  # Pour la base de données SQLite
from datetime import datetime  # Pour les timestamps
from pathlib import Path  # Pour la gestion des chemins de fichiers
from flask import g  # Contexte Flask pour stocker la connexion DB

# Constantes du projet
COMPANY_NAME = "sandia_assurance"  # Nom de l'entreprise
DB_FILE = Path(__file__).resolve().parent.parent / "data.db"  # Chemin absolu vers la base de données

# Liste des services d'assurance proposés
SERVICES = [
    {
        "title": "Assurance auto",
        "description": "Protection complète pour votre véhicule, y compris RC, dommages et assistance 24/7.",
        "image": "images/service-auto.svg"
    },
    {
        "title": "Assurance moto",
        "description": "Formules flexibles pour motards urbains et routiers, avec assistance et protection casque.",
        "image": "images/service-moto.svg"
    },
    {
        "title": "Assurance habitation",
        "description": "Couverture contre les vols, incendies et dégâts des eaux pour votre maison ou appartement.",
        "image": "images/service-habitation.svg"
    },
    {
        "title": "Assurance santé",
        "description": "Complémentaire santé modulable pour vos consultations, hospitalisations et soins du quotidien.",
        "image": "images/service-sante.svg"
    }
]

# Équipe de l'entreprise
TEAM = [
    {
        "name": "Aminata Diallo",
        "role": "Directrice des opérations",
        "description": "Pilote les solutions d'assurance et veille à la qualité du service client."
    },
    {
        "name": "Sébastien Moreau",
        "role": "Responsable expert",
        "description": "Expert assurance avec 12 ans d'expérience dans l'accompagnement des conducteurs et des familles."
    },
    {
        "name": "Fatou Ndiaye",
        "role": "Chargée de relation client",
        "description": "Disponible pour répondre à vos questions et simplifier vos démarches administratives."
    }
]

# Témoignages clients
TESTIMONIALS = [
    {
        "name": "Mamadou S.",
        "role": "Client auto",
        "quote": "Service rapide et tarif clair. Mon dossier a été traité en moins de 24 heures."
    },
    {
        "name": "Sonia K.",
        "role": "Client habitation",
        "quote": "J'ai trouvé une assurance adaptée à mon budget sans compromis sur les garanties."
    }
]

# Questions fréquemment posées
FAQ = [
    {
        "question": "Comment obtenir un devis rapidement ?",
        "answer": "Remplissez le formulaire de devis, puis recevez une estimation en quelques secondes."
    },
    {
        "question": "Puis-je modifier mon contrat plus tard ?",
        "answer": "Oui, nos formules sont flexibles et peuvent évoluer selon vos besoins."
    },
    {
        "question": "Est-ce que je peux contacter un conseiller par téléphone ?",
        "answer": "Oui, le formulaire de contact vous permet de demander un rappel rapide."
    }
]


# Fonction pour obtenir une connexion à la base de données
# Utilise le contexte Flask 'g' pour éviter les connexions multiples par requête
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_FILE)
        g.db.row_factory = sqlite3.Row  # Retourne les résultats sous forme de dictionnaires
    return g.db


# Fonction d'initialisation de la base de données
# Crée toutes les tables nécessaires si elles n'existent pas
def init_db():
    db = get_db()
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            status TEXT NOT NULL,
            method TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS dossiers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            policy_number TEXT NOT NULL,
            status TEXT NOT NULL,
            notes TEXT,
            updated_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            vehicle_type TEXT NOT NULL,
            coverage TEXT NOT NULL,
            total_price REAL NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """
    )
    db.commit()


# Fonctions CRUD pour les utilisateurs

# Crée un nouvel utilisateur dans la base de données
def create_user(name, email, password_hash):
    db = get_db()
    db.execute(
        "INSERT INTO users (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
        (name, email, password_hash, datetime.utcnow().isoformat()),
    )
    db.commit()


# Récupère un utilisateur par son email
def get_user_by_email(email):
    db = get_db()
    return db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()


# Récupère un utilisateur par son ID
def get_user_by_id(user_id):
    db = get_db()
    return db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


# Fonctions CRUD pour les paiements

# Crée un nouveau paiement pour un utilisateur
def create_payment(user_id, amount, method, status="pending"):
    db = get_db()
    db.execute(
        "INSERT INTO payments (user_id, amount, status, method, created_at) VALUES (?, ?, ?, ?, ?)",
        (user_id, amount, status, method, datetime.utcnow().isoformat()),
    )
    db.commit()


# Récupère tous les paiements d'un utilisateur, triés par date décroissante
def get_user_payments(user_id):
    db = get_db()
    return db.execute("SELECT * FROM payments WHERE user_id = ? ORDER BY created_at DESC", (user_id,)).fetchall()


# Fonctions CRUD pour les dossiers

# Crée un nouveau dossier pour un utilisateur
def create_dossier(user_id, policy_number, status="En cours", notes=""):
    db = get_db()
    db.execute(
        "INSERT INTO dossiers (user_id, policy_number, status, notes, updated_at) VALUES (?, ?, ?, ?, ?)",
        (user_id, policy_number, status, notes, datetime.utcnow().isoformat()),
    )
    db.commit()


# Récupère tous les dossiers d'un utilisateur, triés par date de mise à jour décroissante
def get_user_dossiers(user_id):
    db = get_db()
    return db.execute("SELECT * FROM dossiers WHERE user_id = ? ORDER BY updated_at DESC", (user_id,)).fetchall()


# Recherche un dossier par numéro de police
def find_dossier(policy_number):
    db = get_db()
    return db.execute("SELECT * FROM dossiers WHERE policy_number = ?", (policy_number,)).fetchone()


# Fonctions de configuration de la base de données

# Configure la base de données au démarrage de l'application
def setup_database():
    from app import app
    with app.app_context():
        init_db()


# Nettoie la connexion à la base de données à la fin de chaque requête
def teardown_appcontext(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()