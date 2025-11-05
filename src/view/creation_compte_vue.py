import regex
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator, PasswordValidator
from prompt_toolkit.validation import ValidationError, Validator


from src.service.utilisateur_service import UtilisateurService
from src.dao.utilisateur_dao import UtilisateurDAO
from view.vue_abstraite import VueAbstraite
from view.accueil.accueil_vue import AccueilVue


class CreationCompteVue(VueAbstraite):
    def choisir_menu(self):
        # Demande à l'utilisateur de saisir pseudo et email et mot de passe...
        pseudo = inquirer.text(
            message="Entrer votre pseudo : ",
            validate=EmptyInputValidator(),
            ).execute()

        if UtilisateurDAO.pseudo_existe(pseudo):
            return AccueilVue(f"Le pseudo {pseudo} est déjà utilisé.")
        nom = inquirer.text(
            message="Entrez votre nom",
            validate=EmptyInputValidator()
            ).execute()

        prenom = inquirer.text(
            message="Entrez votre prénom",
            validate=EmptyInputValidator()
        ).execute()

        email = inquirer.text(
            message="Entrer votre email",
            validate=EmptyInputValidator()
        ).execute()

        if UtilisateurDAO.email_existe(email):
            return AccueilVue("l'email est déjà utilisé.")

        mot_de_passe = inquirer.secret(
            message="Entrez votre mot de passe : ",
            validate=PasswordValidator(
                length=8,
                number=True,
                message="Le mot de passe doit contenir au moins 8 caractères, dont un chiffre"
            ),
        ).execute()

        # Appel du service pour créer le compte
        user = UtilisateurService.creer_compte(pseudo, nom, prenom, email, mot_de_passe)

        # Si l'utilisateur a été créé
        if user:
            message = (
                f"Votre compte {user.pseudo} a été créé. Vous pouvez maintenant vous connecter."
            )
        else:
            message = "Erreur de connexion (pseudo ou mot de passe invalide)."

        from view.accueil.accueil_vue import AccueilVue

        return AccueilVue(message)


class MailValidator(Validator):
    """Cette classe vérifie le bon format de l'email """

    def validate(self, document) -> None:
        ok = regex.match(r"^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$", document.text)
        if not ok:
            raise ValidationError(
                message="Entrez un mail valide", cursor_position=len(document.text)
            )
