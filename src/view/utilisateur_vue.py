from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session

from src.service.utilisateur_service import UtilisateurService
from src.service.evenement_service import EvenementService


class UtilisateurVue(VueAbstraite):
    """ Vue du menu de l'utilisateur

    Attributs
    --------
    message=''
        str
    
    Returns
    --------
    view
        retourne la prochaine vue, cellle qui est choisie par l'utilisateur
    """

    def choisir_menu(self):
        """Choix du menu suivant de l'utilisateur

        Return
        ------
        vue
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nMenu Utilisateur\n" + "-" * 50 + "\n")
        if UtilisateurService.is_admin():
            choix = inquirer.select(
                message="Faites votre choix : ",
                choices=[
                "Créer un évènement",
                "S'inscrire à un évènement",
                "Se désinscrire d'un évènement",
                "Supprimer un évènement",
                "supprimer un utilisateur",
                "Supprimer son compte"
                "Se déconnecter"
            ]).execute()
        else:
            choix = inquirer.select(
                message="Faites votre choix : ",
                choices=[
                "S'inscrire à un évènement",
                "Se désinscrire d'un évènement",
                "Supprimer son compte",
                "Se déconnecter"
                ]).execute()
        if UtilisateurService.is_admin():
            match choix:
                case "Créer un évènement":
                    from view.creation_event_vue import CreationEventVue
                    return CreationEventVue("Vous souhaitez créer un évènement")

                case "Supprimer un évènement":
                    from view.suppression_event_vue import SuppressionEventVue
                    return SuppressionEventVue("Vous souhaitez supprimer un évènement")

                case "Supprimer un utilisateur":
                    from view.suppression_user_vue import SuppressionUserVue
                    return SuppressionUserVue("Vous souhaitez supprimer un utilisateur")

        match choix:
            case "Se déconnecter":
                Session.deconnexion()
                from view.accueil.accueil_vue import AccueilVue
                return AccueilVue("")

            case "S'inscrire à un évènement":
                from view.inscription_event_vue import InscriptionEventVue
                return InscriptionEventVue("Vous souhaitez vous inscrire à un évènement")

            case "Se désinscrire à un évènement":
                from view.desinscription_event_vue import DesinscriptionEventVue
                return DesinscriptionEventVue("Vous souhaitez vous désinscrire d'un évènement")

            case "Supprimer son compte":
                from view.suppression_compte import SuppressionCompteVue
                return SuppressionCompteVue("Vous souhaitez supprimer votre compte")
