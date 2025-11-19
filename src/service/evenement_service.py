from typing import Optional, List
from business_object.evenement import Evenement
from business_object.inscription import Inscription
from business_object.utilisateur import Utilisateur
import random
STATUTS_VALIDES = ['en_cours', 'complet', 'passe']


class EvenementService:
    """
    Couche service pour la gestion des événements.
    Contient la logique métier complexe et orchestre les interactions
    entre les différentes entités et la couche DAO.
    """

    def __init__(self, evenement_dao, inscription_dao, utilisateur_dao, bus_dao):
        """
        Initialise le service avec les DAO nécessaires.

        evenement_dao: DAO pour les événements
        inscription_dao: DAO pour les inscriptions
        utilisateur_dao: DAO pour les utilisateurs
        bus_dao: DAO pour les bus
        """
        self.evenement_dao = evenement_dao
        self.inscription_dao = inscription_dao
        self.utilisateur_dao = utilisateur_dao
        self.bus_dao = bus_dao

    def creer_evenement(
        self,
        titre: str,
        lieu: str,
        date_event,
        capacite_max: int,
        description_event: str = "",
        tarif: float = 0.00,
        created_by: int = None  # on passe maintenant l'ID utilisateur directement
    ) -> Optional[Evenement]:
        """
        Crée un nouvel événement et le persiste en base de données.

        titre: Titre de l'événement
        lieu: Lieu de l'événement
        date_event: Date de l'événement
        capacite_max: Capacité maximale
        description_event: Description (optionnelle)
        tarif: Tarif de participation

        return: Objet Evenement créé ou None en cas d'erreur
        """
        # Validation : l'utilisateur existe-t-il ?
        utilisateur = self.utilisateur_dao.get_by("id_utilisateur", created_by)
        if not utilisateur:
            print(f"Erreur : Utilisateur {created_by} introuvable")
            return None

        try:
            # Créer l'objet métier (les validations sont faites dans le constructeur)
            nouvel_evenement = Evenement(
                titre=titre,
                lieu=lieu,
                date_event=date_event,
                capacite_max=capacite_max,
                description_event=description_event,
                tarif=tarif,
                created_by=created_by  # on utilise directement l'ID
            )

            # Persister en base de données
            if self.evenement_dao.creer(nouvel_evenement):
                print(f"Événement '{titre}' créé avec succès.")
                return nouvel_evenement  # L'objet a maintenant son ID
            else:
                print("Erreur lors de la création de l'événement.")
                return None

        except ValueError as e:
            print(f"Erreur de validation : {e}")
            return None


    def get_evenement_by(self, field: str, value) -> list[Evenement]:
        try:
            return self.evenement_dao.get_by(field, value)
        except ValueError as ve:
            print(f"Champ non autorisé : {ve}")
            return []
        except Exception as e:
            print(f"Erreur lors de la récupération de l'evenement : {e}")
            return []


    def get_tous_les_evenement(self) -> list[Evenement]:
        """Récupère tous les bus."""
        try:
            return self.evenement_dao.lister_tous()
        except Exception as e:
            print(f"Erreur lors de la récupération des evenements : {e}")
            return []
            
    def supprimer_evenement(self, id_event: int) -> bool:
        """
        Supprime un événement et toutes ses inscriptions associées.

        id_event: ID de l'événement à supprimer

        return: True si suppression réussie, False sinon
        """

        # Supprimer l'événement
        if self.evenement_dao.supprimer(id_event):
            print(f"Événement {id_event} supprimé avec succès.")
            return True
        else:
            print("Erreur lors de la suppression de l'événement.")
            return False


    def modifier_statut(self, id_event: int) -> bool:
        """
        Détermine et met à jour automatiquement le statut d'un événement
        en fonction de la date et de la capacité.

        :param id_event: Identifiant de l'événement.
        :return: True si la mise à jour a réussi, False sinon.
        """

        # 1. Récupérer les détails de l'événement (nécessite la méthode dans EvenementDAO)
        # Assurez-vous que EvenementDAO.recuperer_details_evenement(id_event) 
        # retourne un dictionnaire avec 'capacite_max' (int) et 'date_event' (date).
        details_event = self.evenement_dao.recuperer_details_evenement(id_event)

        if not details_event:
            print(f"Erreur : Événement avec l'ID {id_event} introuvable.")
            return False

        capacite_max = details_event.get("capacite_max")
        date_event = details_event.get("date_event")

        statut_a_appliquer = None

        # 2. Logique de détermination du nouveau statut

        # A. Statut 'passe' (Priorité la plus haute)
        if date_event and date_event < date.today():
            statut_a_appliquer = 'passe'

        # B. Statut 'complet'
        elif capacite_max is not None and capacite_max > 0:
            nombre_inscriptions = self.inscription_dao.compter_par_evenement(id_event)

            if nombre_inscriptions >= capacite_max:
                statut_a_appliquer = 'complet'
            else:
                # C. Statut par défaut si ni passé ni complet
                statut_a_appliquer = 'en_cours'

        else:
            # Si aucune capacité maximale n'est définie (ex: capacite_max = None ou <= 0)
            # et que l'événement n'est pas passé.
            statut_a_appliquer = 'en_cours'


        # 3. Appel à la DAO pour la mise à jour
        if statut_a_appliquer:
            mise_a_jour_reussie = self.evenement_dao.modifier_statut(id_event, statut_a_appliquer)

            if mise_a_jour_reussie:
                print(f"Statut de l'événement {id_event} mis à jour vers : **{statut_a_appliquer}**.")

            return mise_a_jour_reussie

        return False