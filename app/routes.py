# app/routes.py - Définition des routes et logique de l'application Flask
# Ce fichier contient toutes les vues/routes de l'application web,
# incluant l'authentification, les formulaires et les pages statiques

# Imports nécessaires
from flask import render_template, request, session, redirect, url_for  # Fonctions Flask pour les vues
from datetime import datetime  # Pour les timestamps
from werkzeug.security import generate_password_hash, check_password_hash  # Pour le hachage des mots de passe
from app import app  # L'application Flask
from app.models import (  # Import des modèles et données
    COMPANY_NAME,
    SERVICES,
    TEAM,
    TESTIMONIALS,
    FAQ,
    get_db,
    create_user,
    get_user_by_email,
    get_user_by_id,
    create_payment,
    get_user_payments,
    create_dossier,
    get_user_dossiers,
    find_dossier,
)


# Décorateur pour protéger les routes nécessitant une authentification
def login_required(view):
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:  # Vérifie si l'utilisateur est connecté
            return redirect(url_for("login"))  # Redirige vers la page de connexion
        return view(*args, **kwargs)  # Exécute la vue si authentifié

    wrapped_view.__name__ = view.__name__
    return wrapped_view


# Routes principales de l'application

# Route pour la page d'accueil
@app.route("/")
def home():
    return render_template("index.html", company=COMPANY_NAME, services=SERVICES, testimonials=TESTIMONIALS)


# Route pour la page "À propos"
@app.route("/about")
def about():
    return render_template("about.html", company=COMPANY_NAME, team=TEAM, testimonials=TESTIMONIALS, faq=FAQ)


# Route pour la page des services
@app.route("/services")
def services():
    return render_template("services.html", company=COMPANY_NAME, services=SERVICES)


# Route pour le formulaire de devis
@app.route("/quote", methods=["GET", "POST"])
def quote():
    quote_result = None  # Résultat du devis, None par défaut
    if request.method == "POST":  # Si c'est une requête POST (soumission du formulaire)
        # Récupération des données du formulaire
        name = request.form.get("name", "Client")
        age = int(request.form.get("age", 0))
        vehicle_type = request.form.get("vehicle_type", "auto")
        coverage = request.form.get("coverage", "standard")

        # Calcul du prix de base selon le type de véhicule
        base_price = 240
        if vehicle_type == "moto":
            base_price = 210
        elif vehicle_type == "habitation":
            base_price = 190
        elif vehicle_type == "sante":
            base_price = 220

        # Facteurs multiplicatifs
        age_factor = 1.45 if age < 25 else 1.0  # Majoration pour les jeunes conducteurs
        coverage_factor = 1.0 if coverage == "standard" else 1.4  # Majoration pour couverture étendue

        # Calcul du prix total
        total_price = round(base_price * age_factor * coverage_factor, 2)
        quote_result = {
            "name": name,
            "age": age,
            "vehicle_type": vehicle_type,
            "coverage": coverage,
            "total_price": total_price,
            "message": "Votre estimation a été générée. Contactez-nous pour finaliser votre formule."
        }

        # Sauvegarde du devis dans la base de données
        db = get_db()
        db.execute(
            "INSERT INTO quotes (name, age, vehicle_type, coverage, total_price, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (name, age, vehicle_type, coverage, total_price, datetime.utcnow().isoformat()),
        )
        db.commit()

    return render_template("quote.html", company=COMPANY_NAME, quote_result=quote_result)


# Route pour le formulaire de contact
@app.route("/contact", methods=["GET", "POST"])
def contact():
    contact_message = None  # Message de confirmation, None par défaut
    if request.method == "POST":  # Si c'est une requête POST
        # Récupération des données du formulaire
        contact_name = request.form.get("name", "Client")
        contact_email = request.form.get("email", "")
        contact_text = request.form.get("message", "")
        contact_message = f"Merci {contact_name}, votre message a bien été reçu. Notre équipe de {COMPANY_NAME} vous contactera sous peu."

        # Sauvegarde du message de contact dans la base de données
        db = get_db()
        db.execute(
            "INSERT INTO contacts (name, email, message, created_at) VALUES (?, ?, ?, ?)",
            (contact_name, contact_email, contact_text, datetime.utcnow().isoformat()),
        )
        db.commit()

    return render_template("contact.html", company=COMPANY_NAME, contact_message=contact_message)


# Routes d'authentification

# Route pour l'inscription d'un nouvel utilisateur
@app.route("/register", methods=["GET", "POST"])
def register():
    error = None  # Message d'erreur, None par défaut
    if request.method == "POST":  # Si soumission du formulaire
        # Récupération des données
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        password = request.form.get("password", "")

        # Validation des champs
        if not name or not email or not password:
            error = "Veuillez remplir tous les champs."
        elif get_user_by_email(email):  # Vérifie si l'email existe déjà
            error = "Cet email est déjà utilisé."
        else:
            # Hachage du mot de passe et création de l'utilisateur
            password_hash = generate_password_hash(password)
            create_user(name, email, password_hash)
            return redirect(url_for("login"))  # Redirection vers la page de connexion

    return render_template("register.html", company=COMPANY_NAME, error=error)


# Route pour la connexion d'un utilisateur existant
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None  # Message d'erreur, None par défaut
    if request.method == "POST":  # Si soumission du formulaire
        # Récupération des données
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        user = get_user_by_email(email)  # Recherche de l'utilisateur par email

        # Vérification des identifiants
        if user is None or not check_password_hash(user["password_hash"], password):
            error = "Email ou mot de passe incorrect."
        else:
            # Connexion réussie : stockage de l'ID utilisateur en session
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("account"))  # Redirection vers le compte

    return render_template("login.html", company=COMPANY_NAME, error=error)


# Route pour la déconnexion
@app.route("/logout")
def logout():
    session.clear()  # Suppression de toutes les données de session
    return redirect(url_for("home"))  # Redirection vers l'accueil


# Routes protégées (nécessitent une authentification)

# Route pour le compte utilisateur (protégée)
@app.route("/account")
@login_required
def account():
    user = get_user_by_id(session["user_id"])  # Récupération des données utilisateur
    dossiers = get_user_dossiers(user["id"])  # Récupération des dossiers de l'utilisateur
    payments = get_user_payments(user["id"])  # Récupération des paiements de l'utilisateur
    return render_template(
        "account.html",
        company=COMPANY_NAME,
        user=user,
        dossiers=dossiers,
        payments=payments,
    )


# Route pour les demandes de paiement (protégée)
@app.route("/payment", methods=["GET", "POST"])
@login_required
def payment():
    message = None  # Message de confirmation, None par défaut
    if request.method == "POST":  # Si soumission du formulaire
        amount = float(request.form.get("amount", 0))  # Montant demandé
        method = request.form.get("method", "Carte")  # Méthode de paiement
        if amount <= 0:
            message = "Veuillez indiquer un montant valide."
        else:
            # Création de la demande de paiement
            create_payment(session["user_id"], amount, method, status="En attente")
            message = "Votre demande de paiement a été enregistrée."
    return render_template("payment.html", company=COMPANY_NAME, message=message)


# Route pour la gestion des dossiers (protégée)
@app.route("/dossiers", methods=["GET", "POST"])
@login_required
def dossiers():
    message = None  # Message de confirmation, None par défaut
    if request.method == "POST":  # Si soumission du formulaire
        policy_number = request.form.get("policy_number", "").strip()  # Numéro de police
        notes = request.form.get("notes", "")  # Notes supplémentaires
        if not policy_number:
            message = "Veuillez indiquer un numéro de dossier."
        else:
            # Création du dossier
            create_dossier(session["user_id"], policy_number, notes=notes)
            message = "Votre dossier a été créé et est en cours de suivi."
    user = get_user_by_id(session["user_id"])
    dossiers = get_user_dossiers(user["id"])  # Récupération des dossiers pour affichage
    return render_template("dossiers.html", company=COMPANY_NAME, dossiers=dossiers, message=message)


# Route pour le suivi de dossier (accessible sans connexion)
@app.route("/track", methods=["GET", "POST"])
def track():
    dossier_status = None  # Statut du dossier recherché, None par défaut
    if request.method == "POST":  # Si soumission du formulaire
        policy_number = request.form.get("policy_number", "").strip()  # Numéro de police saisi
        dossier = find_dossier(policy_number)  # Recherche du dossier
        if dossier:
            dossier_status = dossier  # Dossier trouvé
        else:
            dossier_status = {"policy_number": policy_number, "status": "Aucun dossier trouvé.", "notes": ""}
    return render_template("track.html", company=COMPANY_NAME, dossier_status=dossier_status)


# Route pour le tableau de bord admin (non protégé pour la démo)
@app.route("/dashboard")
def dashboard():
    db = get_db()

    # Statistiques générales
    total_quotes = db.execute("SELECT COUNT(*) FROM quotes").fetchone()[0]  # Nombre total de devis
    total_contacts = db.execute("SELECT COUNT(*) FROM contacts").fetchone()[0]  # Nombre total de contacts

    # Derniers éléments
    latest_quote = db.execute("SELECT vehicle_type FROM quotes ORDER BY created_at DESC LIMIT 1").fetchone()
    latest_contact = db.execute("SELECT name FROM contacts ORDER BY created_at DESC LIMIT 1").fetchone()

    # Données récentes pour les tableaux
    recent_quotes = db.execute(
        "SELECT name, age, vehicle_type, coverage, total_price, created_at FROM quotes ORDER BY created_at DESC LIMIT 5"
    ).fetchall()
    recent_contacts = db.execute(
        "SELECT name, email, message, created_at FROM contacts ORDER BY created_at DESC LIMIT 5"
    ).fetchall()

    # Résumés par type
    type_summary = db.execute(
        "SELECT vehicle_type, COUNT(*) AS count FROM quotes GROUP BY vehicle_type"
    ).fetchall()
    coverage_summary = db.execute(
        "SELECT coverage, COUNT(*) AS count FROM quotes GROUP BY coverage"
    ).fetchall()

    return render_template(
        "dashboard.html",
        company=COMPANY_NAME,
        total_quotes=total_quotes,
        total_contacts=total_contacts,
        latest_quote_type=latest_quote["vehicle_type"] if latest_quote else "Aucune",
        latest_contact_name=latest_contact["name"] if latest_contact else "Aucun",
        recent_quotes=recent_quotes,
        recent_contacts=recent_contacts,
        type_summary=type_summary,
        coverage_summary=coverage_summary,
    )