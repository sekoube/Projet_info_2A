from business_object.utilisateur import Utilisateur
from service.utilisateur_service import UtilisateurService
from service.evenement_service import EvenementService
from service.inscription_service import InscriptionService
import getpass
from view.page_utilisateur import page_utilisateur
from view.page_admin import page_admin

def connexion_terminal(service_utilisateur: UtilisateurService, evenement_service: EvenementService, inscription_service: InscriptionService):
    print("\n=== Connexion ===")
    email = input("Email : ").strip()
    mot_de_passe = getpass.getpass("Mot de passe : ").strip()

    utilisateur = service_utilisateur.authentifier(email, mot_de_passe)
    if utilisateur:
        print(f"✅ Bienvenue {utilisateur.prenom}, {utilisateur.nom}!")
        if not utilisateur.role:  # Utilisateur simple
            page_utilisateur(utilisateur, evenement_service, inscription_service)
        else:
            page_admin(utilisateur, evenement_service, inscription_service)
    else:
        print("❌ Échec de la connexion. Email ou mot de passe incorrect.")