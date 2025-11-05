from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
#from view.session import Session

from service.utilisateur_service import UtilisateurService

class ConnexionVue(vueAbstraite):
    """ Vue de Connexion (saisie de pseudo et mdp)"""