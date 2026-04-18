import sqlite3
from datetime import datetime
from pathlib import Path
from flask import g

COMPANY_NAME = "sandia_assurance"
DB_FILE = Path(__file__).resolve().parent.parent / "data.db"

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


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_FILE)
        g.db.row_factory = sqlite3.Row
    return g.db


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


def create_user(name, email, password_hash):
    db = get_db()
    db.execute(
        "INSERT INTO users (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
        (name, email, password_hash, datetime.utcnow().isoformat()),
    )
    db.commit()


def get_user_by_email(email):
    db = get_db()
    return db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()


def get_user_by_id(user_id):
    db = get_db()
    return db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


def create_payment(user_id, amount, method, status="pending"):
    db = get_db()
    db.execute(
        "INSERT INTO payments (user_id, amount, status, method, created_at) VALUES (?, ?, ?, ?, ?)",
        (user_id, amount, status, method, datetime.utcnow().isoformat()),
    )
    db.commit()


def get_user_payments(user_id):
    db = get_db()
    return db.execute("SELECT * FROM payments WHERE user_id = ? ORDER BY created_at DESC", (user_id,)).fetchall()


def create_dossier(user_id, policy_number, status="En cours", notes=""):
    db = get_db()
    db.execute(
        "INSERT INTO dossiers (user_id, policy_number, status, notes, updated_at) VALUES (?, ?, ?, ?, ?)",
        (user_id, policy_number, status, notes, datetime.utcnow().isoformat()),
    )
    db.commit()


def get_user_dossiers(user_id):
    db = get_db()
    return db.execute("SELECT * FROM dossiers WHERE user_id = ? ORDER BY updated_at DESC", (user_id,)).fetchall()


def find_dossier(policy_number):
    db = get_db()
    return db.execute("SELECT * FROM dossiers WHERE policy_number = ?", (policy_number,)).fetchone()


def setup_database():
    from app import app
    with app.app_context():
        init_db()


def teardown_appcontext(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()