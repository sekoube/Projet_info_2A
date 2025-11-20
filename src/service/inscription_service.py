from typing import Optional, List
from business_object.inscription import Inscription
from dao.inscription_dao import InscriptionDAO
from dao.evenement_dao import EvenementDAO
from dao.utilisateur_dao import UtilisateurDAO
from business_object.utilisateur import Utilisateur
import random
import string
import random
from utils.api_brevo import send_email_brevo


class InscriptionService:
    """
    Couche service pour gérer la logique métier des inscriptions.
    Fait le lien entre les DAO et la couche de présentation.
    """

    def __init__(self):
        self.inscription_dao = InscriptionDAO()
        self.evenement_dao = EvenementDAO()
        self.utilisateur_dao = UtilisateurDAO()


    def generer_code_reservation(self, longueur: int = 8) -> str:
        """
        Génère un code de réservation unique, entièrement numérique.

        longueur: Longueur du code (par défaut 8 chiffres)

        return: Code de réservation unique
        """
        while True:
            # Génère un entier aléatoire du nombre minimal au maximal possible
            code = int(random.randint(10**(longueur - 1), 10**longueur - 1))

            # Vérifie l'unicité via la base de données / DAO
            if not self.inscription_dao.get_by("code_reservation", code):
                return code

    def creer_inscription(
        self,
        boit: bool,
        mode_paiement: str,
        id_event: int,
        nom_event: str,
        id_bus_aller: int,
        id_bus_retour: int,
        created_by: int
    ) -> Optional[Inscription]:

        # 1. Validation : l'utilisateur existe
        utilisateur = self.utilisateur_dao.get_by("id_utilisateur", created_by)
        if not utilisateur:
            print(f"❌ Erreur : Utilisateur {created_by} introuvable.")
            return None

        # 2. Validation : l'événement existe
        evenement_list = self.evenement_dao.get_by("id_event", id_event)
        if not evenement_list:
            print(f"❌ Erreur : Événement {id_event} introuvable.")
            return None

        evenement = evenement_list[0]  # extraction de l’objet Evenement

        # 3. Validation : capacité disponible ?
        nb_inscrits = self.inscription_dao.compter_par_evenement(id_event)
        if nb_inscrits >= evenement.capacite_max:
            print(f"❌ Erreur : Événement '{nom_event}' complet ({nb_inscrits}/{evenement.capacite_max}).")
            return None

        # 4. Validation : l'utilisateur est-il déjà inscrit ?
        if self.inscription_dao.est_deja_inscrit(created_by, id_event):
            print(f"❌ Erreur : L'utilisateur {created_by} est déjà inscrit à {nom_event}.")
            return None

        # 5. Génération du code de réservation
        code_reservation = self.generer_code_reservation()

        # 6. Création de l'inscription
        try:
            inscription = Inscription(
                code_reservation=code_reservation,
                boit=boit,
                mode_paiement=mode_paiement,
                id_event=id_event,
                nom_event=nom_event,
                id_bus_aller=id_bus_aller,
                id_bus_retour=id_bus_retour,
                created_by=created_by
            )

            # 7. Enregistrer en base
            created = self.inscription_dao.creer(inscription)

            if created:
                # 8. Mise à jour automatique du statut de l’événement
                try:
                    self.evenement_service.modifier_statut(id_event)
                except Exception as e:
                    print(f"⚠️ Avertissement : mise à jour du statut impossible : {e}")

                # 9. Envoi email automatique
                try:
                    to_email = utilisateur[0].email  # supposons que l'objet Utilisateur a un attribut 'email'
                    subject = f"Confirmation d'inscription à {nom_event}"
                    message_text = (
                        f"Bonjour {utilisateur[0].nom},\n\n"
                        f"Votre inscription à l'événement '{nom_event}' a été confirmée.\n"
                        f"Votre code de réservation : {code_reservation}\n\n"
                        "Merci et à bientôt !"
                    )
                    send_email_brevo(to_email, subject, message_text)
                    print(f"✅ Email de confirmation envoyé à {to_email}")
                except Exception as e:
                    print(f"⚠️ Échec de l'envoi de l'email : {e}")

            return created

        except ValueError as e:
            print(f"❌ Erreur de validation : {e}")
            return None




    def lister_toutes_inscriptions(self) -> List[Inscription]:
        """
        Liste toutes les inscriptions.
        
        return: Liste de toutes les inscriptions
        """
        return self.inscription_dao.lister_toutes()

    def get_inscription_by(self, field: str, value) -> Optional[Inscription]:
        """
        Récupère une Inscription en fonction d'un champ et de sa valeur.

        Args:
            field (str): Le nom du champ de la table 'inscription' à rechercher.
            value: La valeur à comparer dans ce champ.

        Returns:
            Optional[Inscription]: L'objet Inscription trouvé ou None.
        
        Raises:
            ValueError: Si le champ fourni n'est pas autorisé par la DAO.
        """
        # Le service délègue la validation des champs et la logique de base de données 
        # directement à la DAO.
        try:
            inscription = self.inscription_dao.get_by(field, value)
            
            # Ici, vous pourriez ajouter de la logique métier supplémentaire 
            # si nécessaire (ex: vérifier des permissions, journaliser l'accès, 
            # transformer les données, etc.)
            
            return inscription
            
        except ValueError as e:
            # Renvoyer l'erreur levée par la DAO si le champ n'est pas autorisé.
            # Dans une application réelle, on pourrait choisir de la loguer et/ou 
            # de la transformer en une erreur de niveau Service/Application.
            raise e

    def supprimer_inscription(self, code_reservation: str, id_utilisateur: int) -> bool:
        """
        Supprime une inscription à partir de son code de réservation.
        Vérifie que l'utilisateur connecté est bien celui qui a créé l'inscription.

        Args:
            code_reservation (str): Le code unique de réservation.
            id_utilisateur (int): ID de l'utilisateur actuellement connecté.

        Returns:
            bool: True si suppression réussie, False sinon.

        Raises:
            ValueError: Si aucun code ou aucune inscription trouvée.
            PermissionError: Si l'utilisateur n'est pas le propriétaire de l'inscription.
        """

        # 1. Vérification entrée
        if not code_reservation:
            raise ValueError("Un code de réservation valide est requis.")

        # 2. Récupération de l'inscription
        inscription_list = self.inscription_dao.get_by("code_reservation", code_reservation)

        if not inscription_list:
            raise ValueError(f"Aucune inscription trouvée avec le code {code_reservation}.")

        inscription = inscription_list[0]

        # 3. Sécurité : vérifier que l'utilisateur connecté est bien le créateur
        if inscription.created_by != id_utilisateur:
            raise PermissionError("Vous ne pouvez supprimer qu'une inscription que vous avez vous-même créée.")

        # 4. Suppression
        suppression_ok = self.inscription_dao.supprimer(inscription)

        if suppression_ok:
            print(f"INFO : Inscription {code_reservation} supprimée par l'utilisateur {id_utilisateur}.")

        return suppression_ok
