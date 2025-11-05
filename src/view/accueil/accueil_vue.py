from InquirerPy import inquirer

## a créer dans le dossier accueil ?
# from utils.reset_database import ResetDatabase
# from view.vue_abstraite import VueAbstraite
# from view.session import Session


class AccueilVue(VueAbstraite):
    """Vue d'accueil de l'application"""

    def choisir_menu(self):
        """ Choix du menu suivant : Créer un compte ou se connecter
 
        Return
        ------
        view
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nAccueil : Bienvenue au bureau des élèves\n" + "-" * 50 + "\n")

        choix = inquirer.select(
            message="Que voulez-vous faire ? ",
            choices=[
                "Se connecter",
                "Créer un compte"
                "Quitter"
            ],
        ).execute()

        match choix:
            case "Quitter":
                pass

            case "Se connecter":
                from view.accueil.connexion_vue import ConnexionVue

                return ConnexionVue("Connexion à l'application")

            case "Créer un compte":
                from view.accueil.creation_compte_vue import InscriptionVue

                return InscriptionVue("Créaction d'un compte utilisateur")
