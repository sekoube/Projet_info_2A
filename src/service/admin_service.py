from dao_evenement import DAOEvenement
from dao_inscription import DAOInscription
from admin_business import Admin


class AdminService:
    """Couche service pour les actions d'administration """

    def __init__(self, dao_evenement: DAOEvenement, dao_inscription: DAOInscription):
        self.dao_evenement = dao_evenement
        self.dao_inscription = dao_inscription

    def creer_evenement(self, admin: Admin, **infos_evenement):
        """Crée et enregistre un événement en base."""
        evenement = admin.creer_evenement(**infos_evenement)
        self.dao_evenement.insert(evenement)
        print(f"[SERVICE] Événement '{evenement.titre}' enregistré en base.")
        return evenement

    def supprimer_evenement(self, id_event: int):
        """Supprime un événement via la DAO."""
        self.dao_evenement.delete(id_event)
        print(f"[SERVICE] Événement id={id_event} supprimé de la base.")

    def consulter_evenements(self):
        """Retourne tous les événements disponibles."""
        return self.dao_evenement.get_all()

    def supprimer_participant(self, id_utilisateur: int, id_event: int):
        """Supprime une inscription."""
        inscription = self.dao_inscription.get_by_user_and_event(id_utilisateur, id_event)
        if inscription:
            self.dao_inscription.delete(inscription.code_reservation)
            print(f"[SERVICE] Participant {id_utilisateur} supprimé de l'événement {id_event}.")
        else:
            print("[SERVICE] Aucune inscription trouvée.")
