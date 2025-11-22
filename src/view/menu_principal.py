"""
Menu principal de l'application.
Affiche les options de base : création de compte, connexion, quitter.
"""

from view.connexion_vue import connexion_terminal
from view.creer_compte_vue import creer_compte_terminal


class MenuPrincipal:

    def __init__(self, service_utilisateur, service_evenement, service_inscription, service_bus):
        """
        Constructeur : les services nécessaires sont injectés ici.
        """
        self.service_utilisateur = service_utilisateur
        self.service_evenement = service_evenement
        self.service_inscription = service_inscription
        self.service_bus = service_bus

    def afficher(self):
        """
        Affiche le menu principal et gère les choix de l'utilisateur.
        """
        while True:
            print("\n=== MENU PRINCIPAL ===")
            print("1. Créer un compte")
            print("2. Connexion")
            print("3. Quitter")

            choix = input("Choisissez une option : ").strip()

            if choix == "1":
                # Vue : création de compte
                creer_compte_terminal(self.service_utilisateur)

            elif choix == "2":
                # Vue : connexion
                connexion_terminal(
                    self.service_utilisateur,
                    self.service_evenement,
                    self.service_inscription,
                    self.service_bus
                )

            elif choix == "3":
                print("👋 Au revoir !")
                break

            else:
                print("❌ Option invalide, veuillez réessayer.")
