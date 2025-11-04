from utils.log_decorator import log
from business_object.evenement import Evenement
from dao.admin_dao import AdminDAO


class AdminService:
    """Classe contenant les méthodes de service pour gérer les événements par un administrateur"""

    @log
    def creer(self, admin_pseudo, titre, description, lieu, date, capacite_max, tarif) -> Evenement:
        """Création d'un événement à partir des informations fournies

        Parameters
        ----------
        admin_pseudo : str
            Pseudo de l'administrateur qui crée l'événement
        titre : str
            Titre de l'événement
        description : str
            Description de l'événement
        lieu : str
            Lieu de l'événement
        date : datetime
            Date de l'événement
        capacite_max : int
            Capacité maximale de l'événement
        tarif : float
            Tarif de l'événement

        Returns
        -------
        evenement : Evenement
            L'événement créé si la création est réussie
        """
        evenement = Evenement(
            titre=titre,
            description=description,
            lieu=lieu,
            date=date,
            capacite_max=capacite_max,
            tarif=tarif,
            pseudo_createur=admin_pseudo,
        )

        # Appeler le DAO pour persister l'événement dans la base de données
        if AdminDAO().creer(evenement):
            return evenement
        return None

    @log
    def lister_tous(self) -> list[Evenement]:
        """Lister tous les événements

        Parameters
        ----------
        None

        Returns
        -------
        list[Evenement] : Liste des événements existants
        """
        return AdminDAO().lister_tous()

    @log
    def trouver_par_id(self, id_event: int) -> Evenement:
        """Trouver un événement à partir de son ID

        Parameters
        ----------
        id_event : int
            Identifiant de l'événement à rechercher

        Returns
        -------
        Evenement : L'événement trouvé, ou None si inexistant
        """
        return AdminDAO().trouver_par_id(id_event)

    @log
    def supprimer(self, evenement: Evenement) -> bool:
        """Supprimer un événement

        Parameters
        ----------
        evenement : Evenement

        Returns
        -------
        bool : True si la suppression a réussi, False sinon
        """
        return AdminDAO().supprimer(evenement)
