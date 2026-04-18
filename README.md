# sandia_assurance

Petite application d'assurance en ligne pour la compagnie `sandia_assurance`.

## Lancement

1. Créer un environnement virtuel (recommandé) :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2.Installer les dépendances dans l'environnement virtuel :

```bash
pip install -r requirements.txt
```

3.Lancer l'application :

```bash
python3 run.py
```

4.Ouvrir `http://127.0.0.1:5002` dans un navigateur.

> Si `python3 -m venv .venv` échoue, installez le paquet système `python3-venv` avec votre gestionnaire de paquets.

## Fonctionnalités

- Interface visuelle moderne et responsive
- Page d'accueil dynamique avec héros et points forts
- Présentation des services avec aperçu interactif
- Formulaire de devis dynamique avec estimation instantanée
- Stockage des devis et des contacts dans une base de données locale (data.db)
- Authentification avec connexion et inscription de clients
- Gestion des paiements et suivi des demandes de règlement
- Suivi personnalisé des dossiers clients
- Page de contact soignée avec informations support
- Page "À propos" avec équipe, avis et FAQ
- Tableau de bord admin accessible à `/dashboard`

## Personnalisation des visuels

Les images utilisées sont dans `static/images/`. Vous pouvez les remplacer par vos propres illustrations pour personnaliser l'application.

- Un placeholder est déjà disponible dans `static/images/placeholder.svg`.
- Ajoutez d'autres photos ou SVG dans `static/images/` pour les utiliser dans les pages plus tard.
