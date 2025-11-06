from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator
from prompt_toolkit.validation import ValidationError

from view.vue_abstraite import VueAbstraite
from view.session import Session

from src.service.utilisateur_service import UtilisateurService
from src.service.evenement_service import EvenementService
from src.service.inscription_service import InscriptionService


class InscriptionEventVue(VueAbstraite):
    def choisir_menu(self):
        # Demande à l'utilisateur de saisir l'id de l'évènement, l'id de l'inscrit, s'il boît, son moyen de paiement, les identifiants bus aller et bus retour

        id_event = inquirer.text(
            message="Entrez l'identifiant de l'évènement auquel inscrire l'utilisateur : ",
            validate=EmptyInputValidator(),
        ).execute()

        nom_event = inquirer.text(
            message="Entrez le nom de l'évènement :",
            validate=EmptyInputValidator(),
        ).execute()

        id_user = inquirer.text(
            message="Entrez l'identifiant de l'utilisateur",
            validate=EmptyInputValidator(),
        ).execute()

        boit=inquirer.select(
            message="L'utilisateur boit-il de l'alcool ? ",
            choices=["Oui", "Non"],
        ).execute()

        mode_paiement=inquirer.select(
            message="Entrez le moyen de paiement de l'utilisateur : ",
            choices=["En espèce", "En ligne"],
        ).execute()

        id_bus_aller=inquirer.text(
            message="Entrez l'identifiant du bus aller : ",
            validate=EmptyInputValidator(),
        ).execute()

        id_bus_retour=inquirer.text(
            message="Entrez l'identifiant du bus retour : ",
            validate=EmptyInputValidator(),
        ).execute()

        # Appel du service pour créer l'inscription
        inscription = InscriptionService.creer_inscription(boit, id_user, mode_paiement, id_event, nom_event, id_bus_aller, id_bus_retour)

        # Si l'inscription a été créé
        if inscription:
            message = (
                f"L'inscription {inscription.code_reservation} a été créé."
            )
        else:
            message = "Erreur de création de l'inscription (il manque un élément descriptif)"
        from view.utilisateur_vue import UtilisateurVue

        return UtilisateurVue(message)
