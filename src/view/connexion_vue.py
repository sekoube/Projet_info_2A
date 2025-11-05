from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
#from view.session import Session

from service.utilisateur_service import UtilisateurService

class ConnexionVue(vueAbstraite):
    """ Vue de Connexion (saisie de pseudo et mdp)"""


    def choisir_menu(self):
        # Demande à l'utilisateur de saisir son pseudo et son mot de passe
        email = inquirer.text(message="Entrez votre email : ").execute()
        mot_de_passe = inquirer.text(message="Entre votre mot de passe : ").execute()

        # Appel du service pour trouver l'Utilisateur
        utilisateur = UtilisateurService.authentifier(email, mot_de_passe)

        # Si l'utilisateur a été trouvé à partir de ses identifiants de connection
        if utilisateur:
            message= f"Vous êtes connecté sous le pseudo {utilisateur.pseudo}"
            Session().connexion(utilisateur)

            from view.menu_utilisateur_vue import MenuUtilisateurVue

            return MenuUtilisateurVue(message)

        message = "Erreur de connexion (email ou mot de passe invalide)"
        from view.accueil.accueil_vue import AccueilVue
        
        return AccueilVue(message)
        
