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

def connexion_terminal(service_utilisateur: UtilisateurService, evenement_service: EvenementService):
    print("\n=== Connexion ===")
    email = input("Email : ").strip()
    mot_de_passe = getpass.getpass("Mot de passe : ").strip()

    utilisateur = service_utilisateur.authentifier(email, mot_de_passe)
    if utilisateur:
        print(f"✅ Bienvenue {utilisateur.pseudo} !")
        if not utilisateur.role:  # Utilisateur simple
            page_utilisateur(utilisateur, evenement_service)
        else:
            print("⚠️ Interface admin non implémentée pour l'instant.")
    else:
        print("❌ Échec de la connexion. Email ou mot de passe incorrect.")

def page_utilisateur(utilisateur, evenement_service: EvenementService):
    """
    Sous-boucle pour un utilisateur connecté.
    Permet de lister les événements et de s'inscrire.
    """
    while True:
        print("\n=== Espace Utilisateur ===")
        print("1. Voir les événements disponibles")
        print("2. S'inscrire à un événement")
        print("3. Déconnexion")
        choix = input("Choisissez une option : ").strip()

        if choix == "1":
            evenements = evenement_service.get_evenements_disponibles()
            if not evenements:
                print("Aucun événement disponible pour le moment.")
            else:
                print("\nÉvénements disponibles :")
                for evt in evenements:
                    print(f"- ID: {evt.id_event}, Titre: {evt.titre}, Lieu: {evt.lieu}, "
                          f"Date: {evt.date_evenement}, Places restantes: "
                          f"{evt.capacite_max - len(evt.inscriptions) if hasattr(evt, 'inscriptions') else evt.capacite_max}")
        elif choix == "2":
            id_event = input("Entrez l'ID de l'événement : ").strip()
            boit_input = input("Consommez-vous de l'alcool ? (oui/non) : ").strip().lower()
            boit = boit_input == "oui"
            mode_paiement = input("Mode de paiement (espèce/en ligne) : ").strip().lower()

            success = evenement_service.inscrire_utilisateur(
                id_event=int(id_event),
                id_utilisateur=utilisateur.id_utilisateur,
                boit=boit,
                mode_paiement=mode_paiement
            )

            if success:
                print("✅ Inscription réussie !")
            else:
                print("❌ Inscription échouée.")
        elif choix == "3":
            print("🔒 Déconnexion...")
            break
        else:
            print("❌ Option invalide, réessayez.")

from dao.evenement_dao import EvenementDAO
from dao.inscription_dao import InscriptionDAO
from dao.utilisateur_dao import UtilisateurDAO
from dao.bus_dao import BusDAO

def menu():
    # Création des DAO
    evenement_dao = EvenementDAO()
    inscription_dao = InscriptionDAO()
    utilisateur_dao = UtilisateurDAO()
    bus_dao = BusDAO()

    # Création des services
    service_utilisateur = UtilisateurService()
    evenement_service = EvenementService(
        evenement_dao,
        inscription_dao,
        utilisateur_dao,
        bus_dao
    )

    while True:
        print("\n=== Menu Principal ===")
        print("1. Créer un compte")
        print("2. Connexion")
        print("3. Quitter")
        choix = input("Choisissez une option : ").strip()

        if choix == "1":
            creer_compte_terminal(service_utilisateur)
        elif choix == "2":
            connexion_terminal(service_utilisateur, evenement_service)
        elif choix == "3":
            print("👋 Au revoir !")
            break
        else:
            print("❌ Option invalide, réessayez.")


if __name__ == "__main__":
    menu()

