from business_object.utilisateur import Utilisateur
from service.utilisateur_service import UtilisateurService
from service.evenement_service import EvenementService
from service.inscription_service import InscriptionService
import getpass
from dao.evenement_dao import EvenementDAO
from dao.inscription_dao import InscriptionDAO
from dao.utilisateur_dao import UtilisateurDAO
from dao.bus_dao import BusDAO
from view.connexion_vue import connexion_terminal
from view.creer_compte_vue import creer_compte_terminal

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
    inscription_service = InscriptionService()

    while True:
        print("\n=== Menu Principal ===")
        print("1. Créer un compte")
        print("2. Connexion")
        print("3. Quitter")
        choix = input("Choisissez une option : ").strip()

        if choix == "1":
            creer_compte_terminal(service_utilisateur)
        elif choix == "2":
            connexion_terminal(service_utilisateur, evenement_service, inscription_service)
        elif choix == "3":
            print("👋 Au revoir !")
            break
        else:
            print("❌ Option invalide, réessayez.")


if __name__ == "__main__":
    menu()