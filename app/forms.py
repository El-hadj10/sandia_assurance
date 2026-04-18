# app/forms.py - Formulaires WTForms avec validation
# Ce fichier définit tous les formulaires de l'application avec validation côté serveur

from wtforms import StringField, PasswordField, SelectField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, ValidationError
from flask_wtf import FlaskForm
from app.models import get_user_by_email


# Formulaire d'inscription utilisateur
class RegisterForm(FlaskForm):
    # Champ nom : obligatoire, entre 2 et 100 caractères
    name = StringField('Nom complet', validators=[
        DataRequired(message='Le nom est obligatoire'),
        Length(min=2, max=100, message='Le nom doit faire entre 2 et 100 caractères')
    ])
    
    # Champ email : obligatoire, format email valide
    email = StringField('Email', validators=[
        DataRequired(message='L\'email est obligatoire'),
        Email(message='Email invalide')
    ])
    
    # Champ mot de passe : obligatoire, minimum 8 caractères
    password = PasswordField('Mot de passe', validators=[
        DataRequired(message='Le mot de passe est obligatoire'),
        Length(min=8, message='Le mot de passe doit faire au minimum 8 caractères')
    ])
    
    # Confirmation du mot de passe : doit correspondre au mot de passe
    password_confirm = PasswordField('Confirmer le mot de passe', validators=[
        DataRequired(),
        EqualTo('password', message='Les mots de passe ne correspondent pas')
    ])
    
    # Bouton soumettre
    submit = SubmitField('S\'inscrire')
    
    # Validation personnalisée : vérifie que l'email n'existe pas déjà
    def validate_email(self, field):
        if get_user_by_email(field.data):
            raise ValidationError('Cet email est déjà utilisé.')


# Formulaire de connexion
class LoginForm(FlaskForm):
    # Champ email
    email = StringField('Email', validators=[
        DataRequired(message='L\'email est obligatoire'),
        Email(message='Email invalide')
    ])
    
    # Champ mot de passe
    password = PasswordField('Mot de passe', validators=[
        DataRequired(message='Le mot de passe est obligatoire')
    ])
    
    # Bouton soumettre
    submit = SubmitField('Se connecter')


# Formulaire de devis
class QuoteForm(FlaskForm):
    # Champ nom : obligatoire
    name = StringField('Votre nom', validators=[
        DataRequired(message='Veuillez entrer votre nom'),
        Length(min=2, max=100)
    ])
    
    # Champ âge : obligatoire, entre 18 et 120 ans
    age = IntegerField('Âge', validators=[
        DataRequired(message='L\'âge est obligatoire'),
        NumberRange(min=18, max=120, message='L\'âge doit être entre 18 et 120 ans')
    ])
    
    # Type de véhicule / service
    vehicle_type = SelectField('Type de couverture', choices=[
        ('auto', 'Assurance Auto'),
        ('moto', 'Assurance Moto'),
        ('habitation', 'Assurance Habitation'),
        ('sante', 'Assurance Santé')
    ], validators=[DataRequired()])
    
    # Niveau de couverture
    coverage = SelectField('Niveau de couverture', choices=[
        ('standard', 'Standard'),
        ('extended', 'Couverture étendue')
    ], validators=[DataRequired()])
    
    # Bouton soumettre
    submit = SubmitField('Obtenir un devis')


# Formulaire de contact
class ContactForm(FlaskForm):
    # Champ nom : obligatoire
    name = StringField('Votre nom', validators=[
        DataRequired(message='Veuillez entrer votre nom'),
        Length(min=2, max=100)
    ])
    
    # Champ email : obligatoire, format email valide
    email = StringField('Votre email', validators=[
        DataRequired(message='Veuillez entrer votre email'),
        Email(message='Email invalide')
    ])
    
    # Message : obligatoire, entre 10 et 1000 caractères
    message = TextAreaField('Votre message', validators=[
        DataRequired(message='Veuillez entrer votre message'),
        Length(min=10, max=1000, message='Le message doit faire entre 10 et 1000 caractères')
    ])
    
    # Bouton soumettre
    submit = SubmitField('Envoyer')


# Formulaire de paiement
class PaymentForm(FlaskForm):
    # Montant du paiement : obligatoire, entre 10 et 10000 euros
    amount = IntegerField('Montant (€)', validators=[
        DataRequired(message='Le montant est obligatoire'),
        NumberRange(min=10, max=10000, message='Le montant doit être entre 10 et 10 000 €')
    ])
    
    # Méthode de paiement
    method = SelectField('Méthode de paiement', choices=[
        ('card', 'Carte bancaire'),
        ('bank', 'Virement bancaire'),
        ('paypal', 'PayPal')
    ], validators=[DataRequired()])
    
    # Bouton soumettre
    submit = SubmitField('Payer')


# Formulaire de suivi dossier
class TrackDossierForm(FlaskForm):
    # Numéro de police : obligatoire
    policy_number = StringField('Numéro de police', validators=[
        DataRequired(message='Veuillez entrer votre numéro de police'),
        Length(min=5, max=20)
    ])
    
    # Bouton soumettre
    submit = SubmitField('Suivre')
