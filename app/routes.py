from flask import render_template, request, session, redirect, url_for
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import app
from app.models import (
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


def login_required(view):
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    wrapped_view.__name__ = view.__name__
    return wrapped_view


@app.route("/")
def home():
    return render_template("index.html", company=COMPANY_NAME, services=SERVICES, testimonials=TESTIMONIALS)


@app.route("/about")
def about():
    return render_template("about.html", company=COMPANY_NAME, team=TEAM, testimonials=TESTIMONIALS, faq=FAQ)


@app.route("/services")
def services():
    return render_template("services.html", company=COMPANY_NAME, services=SERVICES)


@app.route("/quote", methods=["GET", "POST"])
def quote():
    quote_result = None
    if request.method == "POST":
        name = request.form.get("name", "Client")
        age = int(request.form.get("age", 0))
        vehicle_type = request.form.get("vehicle_type", "auto")
        coverage = request.form.get("coverage", "standard")

        base_price = 240
        if vehicle_type == "moto":
            base_price = 210
        elif vehicle_type == "habitation":
            base_price = 190
        elif vehicle_type == "sante":
            base_price = 220

        age_factor = 1.45 if age < 25 else 1.0
        coverage_factor = 1.0 if coverage == "standard" else 1.4

        total_price = round(base_price * age_factor * coverage_factor, 2)
        quote_result = {
            "name": name,
            "age": age,
            "vehicle_type": vehicle_type,
            "coverage": coverage,
            "total_price": total_price,
            "message": "Votre estimation a été générée. Contactez-nous pour finaliser votre formule."
        }

        db = get_db()
        db.execute(
            "INSERT INTO quotes (name, age, vehicle_type, coverage, total_price, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (name, age, vehicle_type, coverage, total_price, datetime.utcnow().isoformat()),
        )
        db.commit()

    return render_template("quote.html", company=COMPANY_NAME, quote_result=quote_result)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    contact_message = None
    if request.method == "POST":
        contact_name = request.form.get("name", "Client")
        contact_email = request.form.get("email", "")
        contact_text = request.form.get("message", "")
        contact_message = f"Merci {contact_name}, votre message a bien été reçu. Notre équipe de {COMPANY_NAME} vous contactera sous peu."

        db = get_db()
        db.execute(
            "INSERT INTO contacts (name, email, message, created_at) VALUES (?, ?, ?, ?)",
            (contact_name, contact_email, contact_text, datetime.utcnow().isoformat()),
        )
        db.commit()

    return render_template("contact.html", company=COMPANY_NAME, contact_message=contact_message)


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        password = request.form.get("password", "")

        if not name or not email or not password:
            error = "Veuillez remplir tous les champs."
        elif get_user_by_email(email):
            error = "Cet email est déjà utilisé."
        else:
            password_hash = generate_password_hash(password)
            create_user(name, email, password_hash)
            return redirect(url_for("login"))

    return render_template("register.html", company=COMPANY_NAME, error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        user = get_user_by_email(email)

        if user is None or not check_password_hash(user["password_hash"], password):
            error = "Email ou mot de passe incorrect."
        else:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("account"))

    return render_template("login.html", company=COMPANY_NAME, error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/account")
@login_required
def account():
    user = get_user_by_id(session["user_id"])
    dossiers = get_user_dossiers(user["id"])
    payments = get_user_payments(user["id"])
    return render_template(
        "account.html",
        company=COMPANY_NAME,
        user=user,
        dossiers=dossiers,
        payments=payments,
    )


@app.route("/payment", methods=["GET", "POST"])
@login_required
def payment():
    message = None
    if request.method == "POST":
        amount = float(request.form.get("amount", 0))
        method = request.form.get("method", "Carte")
        if amount <= 0:
            message = "Veuillez indiquer un montant valide."
        else:
            create_payment(session["user_id"], amount, method, status="En attente")
            message = "Votre demande de paiement a été enregistrée."
    return render_template("payment.html", company=COMPANY_NAME, message=message)


@app.route("/dossiers", methods=["GET", "POST"])
@login_required
def dossiers():
    message = None
    if request.method == "POST":
        policy_number = request.form.get("policy_number", "").strip()
        notes = request.form.get("notes", "")
        if not policy_number:
            message = "Veuillez indiquer un numéro de dossier."
        else:
            create_dossier(session["user_id"], policy_number, notes=notes)
            message = "Votre dossier a été créé et est en cours de suivi."
    user = get_user_by_id(session["user_id"])
    dossiers = get_user_dossiers(user["id"])
    return render_template("dossiers.html", company=COMPANY_NAME, dossiers=dossiers, message=message)


@app.route("/track", methods=["GET", "POST"])
def track():
    dossier_status = None
    if request.method == "POST":
        policy_number = request.form.get("policy_number", "").strip()
        dossier = find_dossier(policy_number)
        if dossier:
            dossier_status = dossier
        else:
            dossier_status = {"policy_number": policy_number, "status": "Aucun dossier trouvé.", "notes": ""}
    return render_template("track.html", company=COMPANY_NAME, dossier_status=dossier_status)


@app.route("/dashboard")
def dashboard():
    db = get_db()

    total_quotes = db.execute("SELECT COUNT(*) FROM quotes").fetchone()[0]
    total_contacts = db.execute("SELECT COUNT(*) FROM contacts").fetchone()[0]
    latest_quote = db.execute("SELECT vehicle_type FROM quotes ORDER BY created_at DESC LIMIT 1").fetchone()
    latest_contact = db.execute("SELECT name FROM contacts ORDER BY created_at DESC LIMIT 1").fetchone()

    recent_quotes = db.execute(
        "SELECT name, age, vehicle_type, coverage, total_price, created_at FROM quotes ORDER BY created_at DESC LIMIT 5"
    ).fetchall()
    recent_contacts = db.execute(
        "SELECT name, email, message, created_at FROM contacts ORDER BY created_at DESC LIMIT 5"
    ).fetchall()
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