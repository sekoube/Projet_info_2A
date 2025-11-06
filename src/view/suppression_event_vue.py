import regex
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator, PasswordValidator
from prompt_toolkit.validation import ValidationError, Validator


from src.service.utilisateur_service import UtilisateurService
from src.dao.utilisateur_dao import UtilisateurDAO
from view.vue_abstraite import VueAbstraite
from view.accueil.accueil_vue import AccueilVue


from src.service.evenement_service import EvenementService
from src.dao.evenement_dao import EvenementDao


class SuppressionEventVue(VueAbstraite):
    def supprimer_event(self):
        # Demande à l'utilisateur de saisir l'identifiant de l'évènement à supprimer
        id_event = inquirer.text(
            message="Entrez l'identifiant de l'évènement à supprimer",
            validate=EmptyInputValidator(),
        ).execute()

        # Appel du service pour supprimer l'évènement
        event = EvenementService.supprimer_evenement(id_event)

        # Si l'évènement a été supprimer
        if event:
            message = "L'évènement a été supprimé"
        else:
            message = "L'évènement n'a pas été supprimé"
        
        from view.utilisateur_vue import UtilisateurVue

        return UtilisateurVue(message)