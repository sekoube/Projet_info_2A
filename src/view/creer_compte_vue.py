from business_object.utilisateur import Utilisateur
from service.utilisateur_service import UtilisateurService
from service.evenement_service import EvenementService
from service.inscription_service import InscriptionService
import getpass

def creer_compte_terminal(service: UtilisateurService):
    print("\n=== Création de compte ===")
    pseudo = input("Pseudo : ").strip()
    while not pseudo:
        pseudo = input("Pseudo obligatoire, réessayez : ").strip()

    nom = input("Nom : ").strip()
    while not nom:
        nom = input("Nom obligatoire, réessayez : ").strip()

    prenom = input("Prénom : ").strip()
    while not prenom:
        prenom = input("Prénom obligatoire, réessayez : ").strip()

    email = input("Email : ").strip()
    while not email:
        email = input("Email obligatoire, réessayez : ").strip()

    mot_de_passe = getpass.getpass("Mot de passe : ").strip()
    while not mot_de_passe:
        mot_de_passe = getpass.getpass("Mot de passe obligatoire, réessayez : ").strip()

    role_input = input("Compte admin ? (oui/non) : ").strip().lower()
    role = role_input == "oui"

    try:
        service.creer_compte(pseudo, nom, prenom, email, mot_de_passe, role)
        print("✅ Compte créé avec succès !")
    except Exception as e:
        print(f"❌ Erreur lors de la création du compte : {e}")