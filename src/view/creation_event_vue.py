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


class CreationEventVue(VueAbstraite):
    def choisir_menu(self):
        # Demande à l'utilisateur de saisir le titre, le lieu, la date, ...
        titre = inquirer.text(
            message="Entrez le titre de l'évènement : ",
            validate=EmptyInputValidator(),
        ).execute()

        lieu = inquirer.text(
            message="Entrez le lieu de l'évènement : ",
            validate=EmptyInputValidator(),
        ).execute()

        date_evenement = inquirer.text(
            message="Entrez la date de l'évènement : ",
            validate=EmptyInputValidator(),
        ).execute()

        capacite_max = inquirer.number(
            message="Entrez la capacité maximale de l'évènement : ",
            validate=EmptyInputValidator(),
        ).execute()

        created_by = inquirer.number(
            message="Entrez votre identifiant utilisateur : ",
            validate=EmptyInputValidator(),
        ).execute()

        description_evenement = inquirer.text(
            message="Entrez la description de l'évènement : "
        ).execute()

        tarif = inquirer.number(
            message="Entrez le tarif de l'évènement : "
        ).execute()

        # Appel du service pour créer l'évènement
        event = EvenementService.creer_evenement(titre, lieu, date_evenement, capacite_max, created_by, description_evenement, tarif)

        # Si l'évènement a été créé
        if event:
            message = (
                f"L'évènement {event.titre} a été créé."
            )
        else:
            message = "Erreur de création de l'évènement (il manque un élément descriptif)"
        from view.utilisateur_vue import UtilisateurVue

        return UtilisateurVue(message)
