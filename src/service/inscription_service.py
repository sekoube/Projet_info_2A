from typing import Optional, List
from business_object.inscription import Inscription
from dao.inscription_dao import InscriptionDAO
from dao.evenement_dao import EvenementDAO
from dao.utilisateur_dao import UtilisateurDAO
from business_object.utilisateur import Utilisateur
import random
import string
import random


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
        id_event: str,
        nom_event: str,
        id_bus_aller: int,
        id_bus_retour: int,
        created_by: int  # on passe maintenant directement l'ID utilisateur
    ) -> Optional[Inscription]:
        """
        Crée une nouvelle inscription avec validations métier.

        return: Inscription créée ou None si échec
        """
        # Validation : l'utilisateur existe-t-il ?
        utilisateur = self.utilisateur_dao.get_by("id_utilisateur", created_by)
        if not utilisateur:
            print(f"Erreur : Utilisateur {created_by} introuvable")
            return None

        # Validation : l'événement existe-t-il ?
        evenement = self.evenement_dao.get_by("id_event", id_event)
        if not evenement:
            print(f"Erreur : Événement {id_event} introuvable")
            return None

        # Validation : l'événement est-il complet ?
        nb_inscrits = self.inscription_dao.compter_par_evenement(id_event)
        if hasattr(evenement, 'capacite_max') and nb_inscrits >= evenement.capacite_max:
            print(f"Erreur : Événement {nom_event} complet ({nb_inscrits}/{evenement.capacite_max})")
            return None

        # Validation : l'utilisateur est-il déjà inscrit ?
        if self.inscription_dao.est_deja_inscrit(created_by, id_event):
            print(f"Erreur : L'utilisateur {created_by} est déjà inscrit à {nom_event}")
            return None

        # Génération du code de réservation
        code_reservation = self.generer_code_reservation()

        # Création de l'objet Inscription
        try:
            inscription = Inscription(
                code_reservation=code_reservation,
                boit=boit,
                mode_paiement=mode_paiement,
                id_event=id_event,
                nom_event=nom_event,
                id_bus_aller=id_bus_aller,
                id_bus_retour=id_bus_retour,
                created_by=created_by  # on utilise directement l'ID
            )

            # Enregistrement en base de données
            return self.inscription_dao.creer(inscription)

        except ValueError as e:
            print(f"Erreur de validation : {e}")
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

    def supprimer_inscription(self, inscription: Inscription) -> bool:
        """
        Gère la suppression d'une inscription, en appliquant toute logique métier
        nécessaire avant de déléguer à la DAO.

        Args:
            inscription (Inscription): L'objet Inscription à supprimer.
                                       Il doit contenir 'code_reservation'.

        Returns:
            bool: True si l'inscription a été supprimée avec succès, False sinon.
        """
        # 1. Vérification des données (Logique métier)
        if not inscription.code_reservation:
            # Lever une erreur si la clé de suppression est manquante
            raise ValueError("L'objet Inscription doit contenir un 'code_reservation' valide pour la suppression.")

        # 2. Logique de vérification supplémentaire (Exemple : Statut)
        # Supposons qu'on ne puisse supprimer que les inscriptions dont le statut est 'Annulée'
        # if inscription.statut != 'Annulée':
        #     raise PermissionError("Seules les inscriptions annulées peuvent être supprimées définitivement.")
        
        # 3. Délégation à la DAO
        # On appelle la méthode de la DAO et on retourne son résultat.
        suppression_reussie = self.inscription_dao.supprimer(inscription)
        
        # 4. Logique post-opération (Exemple : Journalisation)
        if suppression_reussie:
            print(f"INFO: Inscription avec code {inscription.code_reservation} supprimée par le service.")
            # self.log_service.enregistrer_evenement("SUPPRESSION", inscription.code_reservation)

        return suppression_reussie