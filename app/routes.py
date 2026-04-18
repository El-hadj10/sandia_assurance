# app/routes.py - Définition des routes et logique de l'application Flask
# Ce fichier contient toutes les vues/routes de l'application web,
# incluant l'authentification, les formulaires et les pages statiques

# Imports nécessaires
from flask import render_template, request, session, redirect, url_for, flash  # Fonctions Flask pour les vues
from datetime import datetime  # Pour les timestamps
from werkzeug.security import generate_password_hash, check_password_hash  # Pour le hachage des mots de passe
from app import app, limiter  # L'application Flask et le rate limiter
from app.forms import RegisterForm, LoginForm, QuoteForm, ContactForm, PaymentForm, TrackDossierForm  # Formulaires validés
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
@limiter.limit("20 per hour")  # Limite à 20 devis par heure par IP
def quote():
    form = QuoteForm()  # Crée une instance du formulaire de devis
    quote_result = None  # Résultat du devis, None par défaut
    
    if form.validate_on_submit():  # Vérifie si le formulaire est soumis et valide
        # Les données ont été validées par WTForms
        age = form.age.data
        vehicle_type = form.vehicle_type.data
        coverage = form.coverage.data

        # Calcul du prix de base selon le type de véhicule
        base_price_map = {
            "auto": 240,
            "moto": 210,
            "habitation": 190,
            "sante": 220
        }
        base_price = base_price_map.get(vehicle_type, 240)

        # Facteurs multiplicatifs
        age_factor = 1.45 if age < 25 else 1.0  # Majoration pour les jeunes conducteurs
        coverage_factor = 1.0 if coverage == "standard" else 1.4  # Majoration pour couverture étendue

        # Calcul du prix total
        total_price = round(base_price * age_factor * coverage_factor, 2)
        quote_result = {
            "name": form.name.data,
            "age": age,
            "vehicle_type": vehicle_type,
            "coverage": coverage,
            "total_price": total_price,
            "message": "Votre estimation a été générée. Contactez-nous pour finaliser votre formule."
        }

        # Sauvegarde du devis dans la base de données
        try:
            db = get_db()
            db.execute(
                "INSERT INTO quotes (name, age, vehicle_type, coverage, total_price, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (form.name.data, age, vehicle_type, coverage, total_price, datetime.utcnow().isoformat()),
            )
            db.commit()
            flash("Devis enregistré avec succès !", "success")
        except Exception as e:
            app.logger.error(f"Erreur lors de la sauvegarde du devis: {e}")
            flash("Erreur lors de la sauvegarde. Veuillez réessayer.", "error")

    # Récupère les messages d'erreur du formulaire
    error = None
    if form.errors and not form.validate_on_submit():
        error = "; ".join([f"{field}: {', '.join(msgs)}" for field, msgs in form.errors.items()])

    return render_template("quote.html", company=COMPANY_NAME, quote_result=quote_result, error=error, form=form)


# Route pour le formulaire de contact
@app.route("/contact", methods=["GET", "POST"])
@limiter.limit("10 per hour")  # Limite à 10 messages de contact par heure par IP
def contact():
    form = ContactForm()  # Crée une instance du formulaire de contact
    contact_message = None  # Message de confirmation, None par défaut
    
    if form.validate_on_submit():  # Vérifie si le formulaire est soumis et valide
        contact_message = f"Merci {form.name.data}, votre message a bien été reçu. Notre équipe de {COMPANY_NAME} vous contactera sous peu."

        # Sauvegarde du message de contact dans la base de données
        try:
            db = get_db()
            db.execute(
                "INSERT INTO contacts (name, email, message, created_at) VALUES (?, ?, ?, ?)",
                (form.name.data, form.email.data, form.message.data, datetime.utcnow().isoformat()),
            )
            db.commit()
            flash("Votre message a été envoyé avec succès !", "success")
        except Exception as e:
            app.logger.error(f"Erreur lors de la sauvegarde du contact: {e}")
            flash("Erreur lors de l'envoi. Veuillez réessayer.", "error")
    
    # Récupère les messages d'erreur du formulaire
    error = None
    if form.errors and not form.validate_on_submit():
        error = "; ".join([f"{field}: {', '.join(msgs)}" for field, msgs in form.errors.items()])

    return render_template("contact.html", company=COMPANY_NAME, contact_message=contact_message, error=error, form=form)


# Routes d'authentification

# Route pour l'inscription d'un nouvel utilisateur
@app.route("/register", methods=["GET", "POST"])
@limiter.limit("5 per hour")  # Limite à 5 tentatives d'inscription par heure par IP
def register():
    form = RegisterForm()  # Crée une instance du formulaire d'inscription
    
    if form.validate_on_submit():  # Vérifie si le formulaire est soumis et valide
        # Les données du formulaire ont déjà été validées par WTForms
        try:
            password_hash = generate_password_hash(form.password.data)  # Hachage sécurisé du mot de passe
            create_user(form.name.data, form.email.data, password_hash)  # Création de l'utilisateur
            flash("Inscription réussie ! Connectez-vous avec vos identifiants.", "success")
            return redirect(url_for("login"))  # Redirection vers la page de connexion
        except Exception as e:
            app.logger.error(f"Erreur lors de l'inscription: {e}")
            flash("Erreur lors de l'inscription. Veuillez réessayer.", "error")
    
    # Récupère les messages d'erreur du formulaire s'il y en a
    error = None
    if form.errors:
        error = "; ".join([f"{field}: {', '.join(msgs)}" for field, msgs in form.errors.items()])

    return render_template("register.html", company=COMPANY_NAME, error=error, form=form)


# Route pour la connexion d'un utilisateur existant
@app.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per hour")  # Limite à 10 tentatives de connexion par heure par IP
def login():
    form = LoginForm()  # Crée une instance du formulaire de connexion
    
    if form.validate_on_submit():  # Vérifie si le formulaire est soumis et valide
        try:
            user = get_user_by_email(form.email.data)  # Recherche l'utilisateur par email
            
            # Vérification du mot de passe
            if user is None or not check_password_hash(user["password_hash"], form.password.data):
                flash("Email ou mot de passe incorrect.", "error")
            else:
                # Connexion réussie : configuration sécurisée de la session
                session.clear()
                session["user_id"] = user["id"]
                session["user_name"] = user["name"]
                flash(f"Bienvenue {user['name']} !", "success")
                return redirect(url_for("account"))  # Redirection vers le compte
        except Exception as e:
            app.logger.error(f"Erreur lors de la connexion: {e}")
            flash("Erreur de connexion. Veuillez réessayer.", "error")
    
    # Récupère les messages d'erreur du formulaire s'il y en a
    error = None
    if form.errors:
        error = "; ".join([f"{field}: {', '.join(msgs)}" for field, msgs in form.errors.items()])

    return render_template("login.html", company=COMPANY_NAME, error=error, form=form)


# Route pour la déconnexion
@app.route("/logout")
def logout():
    session.clear()  # Suppression complète de la session
    flash("Déconnexion réussie.", "success")
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
@limiter.limit("10 per hour")  # Limite à 10 demandes de paiement par heure par utilisateur
def payment():
    form = PaymentForm()  # Crée une instance du formulaire de paiement
    message = None  # Message de confirmation, None par défaut
    
    if form.validate_on_submit():  # Vérifie si le formulaire est soumis et valide
        # Création de la demande de paiement
        try:
            create_payment(session["user_id"], form.amount.data, form.method.data, status="En attente")
            message = f"Votre demande de paiement de {form.amount.data}€ a été enregistrée."
            flash(message, "success")
        except Exception as e:
            app.logger.error(f"Erreur lors de la création du paiement: {e}")
            error = "Erreur lors de la demande de paiement. Veuillez réessayer."
    
    # Récupère les messages d'erreur du formulaire
    error = None
    if form.errors and not form.validate_on_submit():
        error = "; ".join([f"{field}: {', '.join(msgs)}" for field, msgs in form.errors.items()])
    
    return render_template("payment.html", company=COMPANY_NAME, message=message, error=error, form=form)


# Route pour la gestion des dossiers (protégée)
@app.route("/dossiers", methods=["GET", "POST"])
@login_required
def dossiers():
    form = TrackDossierForm()  # Utilise le même formulaire que track
    message = None  # Message de confirmation, None par défaut
    error = None
    
    if form.validate_on_submit():  # Si soumission du formulaire
        try:
            # Création du dossier
            create_dossier(session["user_id"], form.policy_number.data, notes=form.notes.data)
            message = "Votre dossier a été créé et est en cours de suivi."
            flash(message, "success")
        except Exception as e:
            app.logger.error(f"Erreur lors de la création du dossier: {e}")
            error = "Erreur lors de la création du dossier. Veuillez réessayer."
    
    # Récupère les messages d'erreur du formulaire
    if form.errors and not form.validate_on_submit():
        error = "; ".join([f"{field}: {', '.join(msgs)}" for field, msgs in form.errors.items()])
    
    user = get_user_by_id(session["user_id"])
    user_dossiers = get_user_dossiers(user["id"])  # Récupération des dossiers pour affichage
    
    return render_template("dossiers.html", company=COMPANY_NAME, dossiers=user_dossiers, message=message, error=error, form=form)


# Route pour le suivi de dossier (accessible sans connexion)
@app.route("/track", methods=["GET", "POST"])
@limiter.limit("30 per hour")  # Limite à 30 recherches par heure par IP
def track():
    form = TrackDossierForm()  # Crée une instance du formulaire de suivi
    dossier_status = None  # Statut du dossier recherché, None par défaut
    
    if form.validate_on_submit():  # Vérifie si le formulaire est soumis et valide
        try:
            dossier = find_dossier(form.policy_number.data)  # Recherche du dossier
            if dossier:
                dossier_status = dossier  # Dossier trouvé
            else:
                dossier_status = {"policy_number": form.policy_number.data, "status": "Aucun dossier trouvé.", "notes": ""}
                flash("Dossier non trouvé.", "warning")
        except Exception as e:
            app.logger.error(f"Erreur lors de la recherche du dossier: {e}")
            error = "Erreur lors de la recherche. Veuillez réessayer."
    
    # Récupère les messages d'erreur du formulaire
    error = None
    if form.errors and not form.validate_on_submit():
        error = "; ".join([f"{field}: {', '.join(msgs)}" for field, msgs in form.errors.items()])
    
    return render_template("track.html", company=COMPANY_NAME, dossier_status=dossier_status, error=error, form=form)


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