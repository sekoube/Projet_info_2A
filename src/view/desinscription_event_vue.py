from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator
from prompt_toolkit.validation import ValidationError

from view.vue_abstraite import VueAbstraite
from view.session import Session

from src.service.utilisateur_service import UtilisateurService
from src.service.evenement_service import EvenementService
from src.service.inscription_service import InscriptionService


class DesinscriptionEventVue(VueAbstraite):
    def choisir_menu(self):
        # Demande à l'utilisateur de saisir l'identifiant de l'évènement et l'identifiant de l'utilisateur à désinscrire

        id_event = inquirer.number(
            message="Entrez l'identifiant de l'évènement",
            validate=EmptyInputValidator(),
        ).execute()

        id_user = inquirer.number(
            message="Entrez l'identifiant de l'utilisateur à désinscrire",
            validate=EmptyInputValidator()
        ).execute()

        # Appel du service pour désincrire l'utilisateur de l'évènement
        desinscription = EvenementService.desinscrire_utilisateur(id_event, id_user)

        # Si la désinscription a été faite
        if desinscription:
            message = f"L'utilisateur est bien désinscrit de l'évènement {id_event}"
        else:
            message = f"L'utilisateur est toujours inscrit à l'évèement {id_event}"
        from view.utilisateur_vue import UtilisateurVue

        return UtilisateurVue(message)