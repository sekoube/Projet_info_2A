import regex
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator, PasswordValidator
from prompt_toolkit.validation import ValidationError, Validator

from src.business_object.utilisateur import Utilisateur
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

    # 