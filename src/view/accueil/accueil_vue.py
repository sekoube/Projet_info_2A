from business_object.utilisateur import Utilisateur
<<<<<<< HEAD
from service.utilisateur_service import UtilisateurService  # Assure-toi que le chemin est correct
from service.evenement_service import EvenementService
=======
from service.utilisateur_service import UtilisateurService
from service.evenement_service import EvenementService
from service.inscription_service import InscriptionService
import getpass
>>>>>>> 58b3efe398af4b33c8cca5fbe91fa7b3ca1f930f

def creer_compte_terminal(service: UtilisateurService):
    print("\n=== Création de compte ===")
    pseudo = input("Pseudo : ").strip()
    while not pseudo:
        pseudo = input("Pseudo obligatoire, réessayez : ").strip()

    nom = input("Nom : ").strip()
    while not nom:
        nom = input("Nom obligatoire, réessayez : ").strip()

def creer_event_terminal(service : EvenementService):
    print("\n=== Création d'un évènement")
    titre = input("Titre : ")
    lieu = input("Lieu : ")
    date_evenement = input("Date : ")
    capacite_max = input("Capacité max :")
    created_by = input("Entrez votre identifiant :")
    description_event = input("Description évènement :")
    tarif = input("tarif :")

    service.creer_evenement(titre, lieu, date_evenement, capacite_max, created_by, description_event, tarif)


def connexion_terminal(service: UtilisateurService):
    print("\n=== Connexion ===")
    email = input("Email : ").strip()
    mot_de_passe = getpass.getpass("Mot de passe : ").strip()

    utilisateur = service_utilisateur.authentifier(email, mot_de_passe)
    if utilisateur:
<<<<<<< HEAD
        print(f"Bienvenue {utilisateur.pseudo} !")
        print("\n=== Menu de l'utilisateur ===")
        if UtilisateurService.is_admin():
            print("1. Créer un évènement")
            print("2. S'inscrire à un évènement")
            print("3. Se désinscrire d'un évènement")
            print("4. Supprimer un évènement")
            print("5. Supprimer un utilisateur")
            print("6. Suppremer son compte")
            print("7. Se déconnecter")
        else:
            print("2. S'inscrire à un évènement")
            print("3. Se désinscrire d'un évènement")
            print("6. Suppremer son compte")
            print("7. Se déconnecter")
        
        if choix==1:
            creer_event_terminal(service)

=======
        print(f"✅ Bienvenue {utilisateur.pseudo} !")
        if not utilisateur.role:  # Utilisateur simple
            page_utilisateur(utilisateur, evenement_service)
        else:
            print("⚠️ Interface admin non implémentée pour l'instant.")
>>>>>>> 58b3efe398af4b33c8cca5fbe91fa7b3ca1f930f
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
