# sandia_assurance

## Description

`sandia_assurance` est une application Flask de démonstration pour un service d'assurance en ligne. Le projet combine une interface client moderne, une gestion simple des devis, des sessions utilisateurs, un suivi des dossiers, et une simulation de paiement.

## Technologies

- Python 3
- Flask
- SQLite
- Jinja2
- HTML/CSS/JavaScript

## Fonctionnalités principales

- Page d'accueil responsive et navigation claire
- Formulaire de devis interactif avec stockage local dans SQLite
- Modules d'inscription, connexion et gestion de compte
- Paiements simulés et historique des transactions
- Suivi des dossiers clients et statut des demandes
- Pages statiques : services, contact, à propos
- Tableau de bord simple pour consultation interne

## Structure du projet

- `run.py` : démarrage de l'application Flask
- `app/__init__.py` : création de l'application et initialisation du contexte
- `app/routes.py` : routes web et logique de navigation
- `app/models.py` : création et accès à la base de données
- `templates/` : pages HTML Jinja2
- `static/` : assets CSS, JavaScript et images
- `requirements.txt` : dépendances Python

## Installation

```bash
cd /home/el-hadj-ousmane/Bureau/Sandia_Assurance
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Exécution

```bash
python3 run.py
```

Ouvrez ensuite :

```bash
http://127.0.0.1:5002
```

> Si `python3 -m venv .venv` échoue, installez `python3-venv` via votre gestionnaire de paquets.

## Configuration

- La base SQLite est stockée dans `data.db`.
- Le secret de session est défini dans `app/__init__.py`.
- Pour personnaliser le site, modifiez les templates dans `templates/` et les fichiers CSS/JS dans `static/`.

## Développement

1. Activez l'environnement virtuel.
2. Installez ou mettez à jour les dépendances :

```bash
pip install -r requirements.txt
```

3.Vérifiez le code Python :

```bash
python3 -m py_compile app/__init__.py app/models.py app/routes.py
```

4.Lancez l'application en développement :

```bash
python3 run.py
```

## Tests manuels recommandés

- Créer un compte utilisateur
- Se connecter et accéder à la page `Mon compte`
- Soumettre un devis et vérifier l'enregistrement
- Créer une demande de paiement
- Vérifier le suivi d'un dossier
- Envoyer un message depuis la page contact

## Contribuer

Des contributions sont les bienvenues ! Merci de consulter `CONTRIBUTING.md` pour les bonnes pratiques et le flux de contributions.

## Licence

Ce projet est distribué sous une licence propriétaire. Tous droits réservés par Sandia Assurance.
Voir le fichier `LICENSE` pour les termes détaillés.

## Ressources utiles

- `static/` : ressources front-end du site
- `templates/` : pages et blocs Jinja2
- `app/models.py` : interaction avec SQLite
- `app/routes.py` : logique des pages et des formulaires
