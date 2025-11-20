"""
Point d'entrée principal de l'application de gestion d'événements.
Lance l'interface utilisateur et initialise les services.
"""

from dao.db_connection import DBConnection

# Import des DAO
from dao.evenement_dao import EvenementDAO
from dao.inscription_dao import InscriptionDAO
from dao.utilisateur_dao import UtilisateurDAO
from dao.bus_dao import BusDAO

# Import des services
from service.utilisateur_service import UtilisateurService
from service.evenement_service import EvenementService
from service.inscription_service import InscriptionService

# Import des vues
from view.menu_principal import MenuPrincipal


def main():
    """
    Fonction principale qui démarre l'application.
    """
    print("=" * 60)
    print("   BIENVENUE - Système de Gestion d'Événements")
    print("=" * 60)

    # Vérifier la connexion à la base de données
    try:
        with DBConnection().connection as conn:
            print("✓ Connexion à la base de données réussie")
    except Exception as e:
        print(f"✗ Erreur de connexion à la base de données : {e}")
        return

    # ==== Initialisation des DAO ====
    evenement_dao = EvenementDAO()
    inscription_dao = InscriptionDAO()
    utilisateur_dao = UtilisateurDAO()
    bus_dao = BusDAO()

    # ==== Initialisation des Services ====
    service_utilisateur = UtilisateurService()
    service_evenement = EvenementService(
        evenement_dao,
        inscription_dao,
        utilisateur_dao,
        bus_dao
    )
    service_inscription = InscriptionService(
        inscription_dao,
        evenement_dao,
        utilisateur_dao
    )

    # ==== Lancer le menu principal ====
    menu = MenuPrincipal(
        service_utilisateur,
        service_evenement,
        service_inscription
    )
    menu.afficher()


if __name__ == "__main__":
    main()
