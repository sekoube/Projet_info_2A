Application CLI de gestion des évènements du BDE ENSAI

Ce projet implémente une application en ligne de commande permettant de gérer les évènements du BDE de l’ENSAI.
Il s’appuie sur une architecture en couches orientée objet, une base de données PostgreSQL, et est entièrement testé avec pytest.

🎯 Objectif du projet

L’application permet aux étudiants de l’ENSAI de consulter et s'inscrire à des évènements organisés par le BDE. Les administrateurs peuvent créer des évènements, des bus associés à ces évènements.

▶️ Installation et configuration

- Tout le code source et les tests se trouvent dans le dossier **`src/`**.  
- Le fichier **`requirements.txt`** contient la liste des **packages nécessaires**.  
- Le fichier **`settings.json`** est configuré pour exécuter le code depuis le dossier `src`.

1. Prérequis
Visual Studio Code
Python 3.x
PostgreSQL pour la base de données
Git

2. Lancer VSCode
Ouvrez VS Code.
Ouvrez Git Bash.
Clonez le dépôt avec la commande suivante :
git clone code_hhtps_du_depôt (à adpater)
Ouvrez le dossier dans VS Code :
File > Open Folder, puis sélectionnez le dossier du projet cloné (faire cette méthode plutôt que les lignes de commande 🚨)

3. Installation des dépendances
Dans Git Bash, exécutez la commande suivante pour installer les packages nécessaires :
pip install -r requirements.txt

4. Configuration de l'environnement
Créez un fichier .env à la racine du projet et ajoutez-y les variables d’environnement nécessaires pour la connexion PostgreSQL :
POSTGRES_HOST=ton_host
POSTGRES_PORT=5432
POSTGRES_DATABASE=ton_database
POSTGRES_USER=ton_user
POSTGRES_PASSWORD=ton_password
POSTGRES_SCHEMA=ton_schema

5. Création de la base de données
Exécutez le script data/init_db.sql pour initialiser la base de données.
Exécutez le script data/pop_db.sql pour insérer un premier utilisateur et quelques données de test dans la base de données.

▶️ Lancement de l’application

Pour démarrer l’application en ligne de commande, exécuter :
python src/view/menu_vue.py

🧩 Fonctionnalités principales

👤 Utilisateur (étudiant ENSAI)
Créer un compte ou se connecter à un compte existant.
Consulter la liste des évènements disponibles.
S’inscrire à un évènement (via son ID).

🛠️ Administrateur (membre du BDE)
Créer un évènement.
Créer des bus
Consulter la liste complète des évènements.

🧱 Architecture du projet

L’application suit une architecture en trois couches pour assurer modularité et clarté.

1. Business Object (Modèles)
Contient les classes métiers décrivant les entités principales de l’application.
bus.py : représente un bus (évènement rattaché, description, sens, etc.)
evenement.py : représente un évènement (date, heure, description, etc.)
inscription.py : représente une inscription (alcool, mode de paiement, etc.)
utilisateur.py : représente un utilisateur (nom, prénom, email, rôle, etc.)

2. DAO (Data Access Object)
Gère les interactions directes avec la base de données PostgreSQL.
utilisateur_dao.py : création, insertion et vérification d’utilisateurs.
evenement_dao.py : gestion des évènements (création, liste, suppression, etc.).
inscription_dao.py : gestion des inscriptions (création, suppression, etc.).
bus_dao.py : enregistrement et gestion des bus.

3. Service
Contient la logique applicative. Ces classes orchestrent les appels aux DAO pour exécuter les actions métier.

4. Vue (Interface en ligne de commande)
Contient les interfaces CLI qui interagissent directement avec l’utilisateur.
creer_compte_vue.py : création d’un compte utilisateur.
page_utilisateur_vue.py : gestion des actions possibles pour un utilisateur.
page_admin_vue.py : gestion des actions réservées à un administrateur.
menu_vue.py : point d’entrée principal de l’application.

🧪 Tests unitaires

Les tests sont organisés dans les dossiers suivants :
src/tests/tests_business/
src/tests/tests_dao/
src/tests/tests_service/

1. Lancer tous les tests
pytest -v --color=yes
(Les tests réussis apparaissent en vert, les échecs en rouge.)

2. Lancer un test spécifique
Exemple : pytest tests/test_service/test_utilisateur_service.py
(A adapter selon le chemin ou le test souhaité.)

🗄️ Base de données
init_db.sql : Initialise le schéma et les tables PostgreSQL.
pop_db.sql : Insère des données initiales (par exemple, un premier utilisateur).
Les tables principales concernent les utilisateurs, bus, évènements et inscriptions.

🧰 Technologies utilisées

Langage : Python 3.x
Base de données : PostgreSQL
Gestion d’environnement : .env
Tests : Pytest
Interface : Ligne de commande (CLI)