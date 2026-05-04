<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:1a1a2e,100:2e86ab&height=200&section=header&text=Sandia+Assurance&fontSize=48&fontColor=ffffff&fontAlignY=38&desc=Application+web+d%27assurance+en+ligne+%7C+Flask+%C2%B7+SQLite+%C2%B7+Python&descAlignY=58&descSize=16" />
</p>

<p align="center">
  <a href="https://github.com/El-hadj10/sandia_assurance">
    <img src="https://img.shields.io/badge/GitHub-sandia__assurance-2e86ab?style=for-the-badge&logo=github&logoColor=white" />
  </a>
  <img src="https://img.shields.io/badge/Python-3.x-3572A5?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-Backend-000000?style=for-the-badge&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-Base%20de%20donn%C3%A9es-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/Licence-Propri%C3%A9taire-c0392b?style=for-the-badge" />
</p>

---

## A propos

**Sandia Assurance** est une application Flask de demonstration pour un service d'assurance en ligne.

Le projet combine une interface client moderne, une gestion des devis, des sessions utilisateurs, un suivi des dossiers et une simulation de paiement — le tout sur une base SQLite legere.

> Devis, compte, paiement, suivi de dossier — une experience assurance complete en local.

---

## Architecture

```
sandia_assurance/
├── run.py                  Point d'entree Flask (port 5002)
├── app/
│   ├── __init__.py         Creation de l'app + contexte
│   ├── routes.py           Routes web & logique de navigation
│   ├── models.py           Acces base de donnees SQLite
│   └── forms.py            Formulaires Flask-WTF
├── templates/              Pages HTML Jinja2
│   ├── layout.html         Template de base
│   ├── index.html          Accueil
│   ├── quote.html          Formulaire de devis
│   ├── account.html        Espace client
│   ├── payment.html        Paiement simule
│   ├── dossiers.html       Suivi des dossiers
│   ├── dashboard.html      Tableau de bord interne
│   └── ...                 (contact, services, about, 404, 500)
├── static/
│   ├── style.css           Styles principaux
│   ├── style-responsive.css Adaptations responsive
│   ├── js/                 Scripts JavaScript
│   └── images/             Assets visuels
├── data.db                 Base SQLite (generee au premier lancement)
└── requirements.txt        Dependances Python
```

---

## Stack technique

| Couche      | Technologie                    |
|-------------|--------------------------------|
| Backend     | Python 3 · Flask               |
| Templating  | Jinja2                         |
| Base de donnees | SQLite (`data.db`)         |
| Frontend    | HTML · CSS · JavaScript vanilla|
| Formulaires | Flask-WTF                      |

---

## Fonctionnalites

- Page d'accueil responsive et navigation claire
- Formulaire de devis interactif avec stockage SQLite
- Inscription, connexion et gestion de compte
- Paiements simules et historique des transactions
- Suivi des dossiers clients et statut des demandes
- Pages statiques : services, contact, a propos
- Tableau de bord pour consultation interne
- Pages d'erreur personnalisees (404, 500)

---

## Installation & lancement

```bash
cd sandia_assurance
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 run.py
```

Application disponible sur : **http://127.0.0.1:5002**

---

## Tests manuels recommandes

```
✓ Creer un compte utilisateur
✓ Se connecter et acceder a la page Mon compte
✓ Soumettre un devis et verifier l'enregistrement
✓ Creer une demande de paiement
✓ Verifier le suivi d'un dossier
✓ Envoyer un message depuis la page contact
```

---

## Roadmap

- [ ] Authentification JWT / OAuth2
- [ ] API REST pour l'espace client
- [ ] Envoi de devis par e-mail (Flask-Mail)
- [ ] Generation de PDF pour les contrats
- [ ] Migration vers PostgreSQL pour la production
- [ ] Deploiement Docker + Nginx

---

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:2e86ab,100:1a1a2e&height=120&section=footer" />
</p>

<p align="center">
  Concu par <strong>Nour</strong> &middot; <a href="https://github.com/El-hadj10">El-hadj10</a><br/>
  <em>Full-Stack Developer &amp; Cybersecurity Enthusiast</em>
</p>
