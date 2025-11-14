#  Application CLI de gestion des évènements du BDE ENSAI

Ce projet implémente une **application en ligne de commande** permettant de gérer les **évènements du BDE de l’ENSAI**.  
Il s’appuie sur une **architecture en couches orientée objet**, une **base de données PostgreSQL**, et est entièrement **testé avec `pytest`**.

---

##  Installation et configuration
###  Comment lancer vs code 




###  Structure du projet
- Tout le code source et les tests se trouvent dans le dossier **`src/`**.  
- Le fichier **`requirements.txt`** contient la liste des **packages nécessaires**.  
- Le fichier **`settings.json`** est configuré pour exécuter le code depuis le dossier `src`.

###  Création de la base de données
1. Créer un fichier **`.env`** à la racine du projet (au même niveau que `src/`), contenant les variables d’environnement nécessaires à la connexion PostgreSQL.  
POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DATABASE, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_SCHEMA 

2. Lancer le script SQL **`data/init_db.sql`** pour initialiser la base.  
3. Le fichier **`data/pop_db.sql`** insère un premier utilisateur et des données de test dans la base.

---

##  Lancement de l’application

Pour démarrer l’application en ligne de commande :

```bash
python src/view/menu_vue.py


🧩 Fonctionnalités principales
👤 Utilisateur simple (étudiant ENSAI)

Créer un compte ou se connecter à un compte existant.

Consulter la liste des évènements disponibles.

S’inscrire à un évènement (via son ID).

Se désinscrire d’un évènement (à implémenter si non fait).

🛠️ Administrateur (membre du BDE)

Créer un évènement.

Modifier un évènement.

Supprimer un évènement.

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

Communique directement avec la base de données PostgreSQL.

utilisateur_dao.py : création, insertion et vérification d’utilisateurs.

evenement_dao.py : gestion des évènements (création, liste, suppression, etc.).

inscription_dao.py : gestion des inscriptions (création, suppression, etc.).

bus_dao.py : enregistrement et gestion des bus.

 3. Service

Contient la logique applicative.
Ces classes orchestrent les appels aux DAO pour exécuter les actions métier.

 4. Vue (Interface en ligne de commande)

Contient les interfaces CLI qui interagissent directement avec l’utilisateur.

creer_compte_vue.py : création d’un compte utilisateur.

page_utilisateur_vue.py : gestion des actions possibles pour un utilisateur.

page_admin_vue.py : gestion des actions réservées à un administrateur.

menu_vue.py : point d’entrée principal de l’application.

🧪 Tests unitaires

Les tests sont situés dans :

src/tests/tests_business/

src/tests/tests_dao/

src/tests/tests_service/

▶️ Lancer tous les tests
pytest -v --color=yes
(Les tests réussis apparaissent en vert, les échecs en rouge.)

🎯 Lancer un test spécifique

Exemple : 
pytest tests/test_service/test_utilisateur_service.py
(Adapter le chemin au fichier ou au test souhaité.)

🗄️ Base de données

init_db.sql : initialise le schéma et les tables PostgreSQL.

pop_db.sql : insère des données initiales (ex. premier utilisateur).

Les tables principales concernent les utilisateurs, bus, évènements et inscriptions.

🧰 Technologies utilisées

Langage : Python 3.x

Base de données : PostgreSQL

Gestion d’environnement : .env

Tests : Pytest

Interface : Ligne de commande (CLI)