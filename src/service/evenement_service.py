from typing import Optional, List
from business_object.evenement import Evenement
from business_object.inscription import Inscription
from business_object.utilisateur import Utilisateur
from datetime import date
import random

STATUTS_VALIDES = ['en_cours', 'passe']


class EvenementService:
    """
    Couche service pour la gestion des événements.
    Contient la logique métier complexe et orchestre les interactions
    entre les différentes entités et la couche DAO.
    """

    def __init__(self, evenement_dao, inscription_dao, utilisateur_dao, bus_dao):
        """
        Initialise le service avec les DAO nécessaires.
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
        created_by: int = None
    ) -> Optional[Evenement]:
        """
        Crée un nouvel événement et le persiste en base de données.
        """
        utilisateur = self.utilisateur_dao.get_by("id_utilisateur", created_by)
        if not utilisateur:
            print(f"Erreur : Utilisateur {created_by} introuvable")
            return None

        try:
            nouvel_evenement = Evenement(
                titre=titre,
                lieu=lieu,
                date_event=date_event,
                capacite_max=capacite_max,
                description_event=description_event,
                tarif=tarif,
                created_by=created_by
            )

            if self.evenement_dao.creer(nouvel_evenement):
                print(f"Événement '{titre}' créé avec succès.")
                return nouvel_evenement
            else:
                print("Erreur lors de la création de l'événement.")
                return None

        except ValueError as e:
            print(f"Erreur de validation : {e}")
            return None

    def get_evenement_by(self, field: str, value) -> List[Evenement]:
        try:
            return self.evenement_dao.get_by(field, value)
        except ValueError as ve:
            print(f"Champ non autorisé : {ve}")
            return []
        except Exception as e:
            print(f"Erreur lors de la récupération de l'événement : {e}")
            return []

    def get_tous_les_evenement(self) -> List[Evenement]:
        """Récupère tous les événements."""
        try:
            return self.evenement_dao.lister_tous()
        except Exception as e:
            print(f"Erreur lors de la récupération des événements : {e}")
            return []

    def supprimer_evenement(self, id_event: int) -> bool:
        """
        Supprime un événement et toutes ses données associées.
        """
        evenement = self.evenement_dao.get_by("id_event", id_event)
        if not evenement:
            print(f"❌ Impossible de supprimer : aucun événement avec id {id_event}.")
            return False

        try:
            succes = self.evenement_dao.supprimer(evenement[0])
            if succes:
                print(f"✔️ Événement {id_event} supprimé avec succès.")
                return True
            else:
                print("❌ Erreur lors de la suppression de l'événement.")
                return False

        except Exception as e:
            print(f"❌ Exception lors de la suppression : {e}")
            return False

    def modifier_statut(self, id_event: int) -> bool:
        """
        Met automatiquement à jour le statut d’un événement selon :
        - la date (passé)
        - la capacité (complet)
        - sinon en cours
        """
        # 1. Charger l’événement
        evenement = self.evenement_dao.get_by("id_event", id_event)
        if not evenement:
            print(f"❌ Impossible de modifier le statut : événement {id_event} introuvable.")
            return False

        evenement = evenement[0]

        # 2. Récupérer les infos
        capacite_max = evenement.capacite_max
        date_event = evenement.date_event

        # 3. Déterminer nouveau statut
        if date_event < date.today():
            nouveau_statut = "passe"
        else:
            nb_inscrits = self.inscription_dao.compter_par_evenement(id_event)
            if nb_inscrits >= capacite_max:
                nouveau_statut = "complet"
            else:
                nouveau_statut = "en_cours"

        # 4. Appliquer si changement
        if evenement.statut != nouveau_statut:
            self.evenement_dao.modifier_statut(id_event, nouveau_statut)
            print(f"✔️ Statut mis à jour : {evenement.statut} → {nouveau_statut}")

        return True
