from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator
from prompt_toolkit.validation import ValidationError

from view.vue_abstraite import VueAbstraite
from view.session import Session

from service.utilisateur_service import UtilisateurService
from dao.utilisateur_dao import UtilisateurDAO

class ConnexionVue(vueAbstraite):
    """ Vue de Connexion (saisie de pseudo et mdp)
    
    Attributs
    --------
    message=''
        str
    
    Returns
    --------
    view
        retourne la prochaine vue, celle du menu de l'utilisateur
    """

    def entree_menu(self):
        print("\n" + "-" * 50 + "\n Menu de connexion de l'utilisateur")

        email=inquirer.text(
            message="Entrez votre email : ",
            validate=EmptyInputValidator(),
        ).execute()

        mot_de_passe=inquirer.secret(
            message="Entre votre mot de passe : ",
            validate=EmptyInputValidator
        ).execute()

        # Appel du service pour se connecter à l'application
        connexion = UtilisateurService.authentifier(email, mot_de_passe)

        # Si la connexion est réussi
        if connexion:
            message="La connexion est réussie."
            from view.utilisateur_vue import UtilisateurVue
            return UtilisateurVue(message)
        else:
            message="La connexion a échoué"
            from view.accueil.accueil_vue import AccueilVue
            return AccueilVue(message)
