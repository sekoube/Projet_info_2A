from typing import Optional, List
from Projet_info_2A.src.business_object.evenement import Evenement
from Projet_info_2A.src.business_object.inscription import Inscription


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
        date_evenement,
        capacite_max: int,
        created_by: int,
        description_evenement: str = "",
        tarif: float = 0.00
    ) -> Optional[Evenement]:
        """
        Crée un nouvel événement et le persiste en base de données.

        titre: Titre de l'événement
        lieu: Lieu de l'événement
        date_evenement: Date de l'événement
        capacite_max: Capacité maximale
        created_by: ID de l'utilisateur créateur
        description_evenement: Description (optionnelle)
        tarif: Tarif de participation

        return: Objet Evenement créé ou None en cas d'erreur
        """
        try:
            # Créer l'objet métier (les validations sont faites dans le constructeur)
            nouvel_evenement = Evenement(
                titre=titre,
                lieu=lieu,
                date_evenement=date_evenement,
                capacite_max=capacite_max,
                created_by=created_by,
                description_evenement=description_evenement,
                tarif=tarif
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

    def inscrire_utilisateur(
        self,
        id_event: int,
        id_utilisateur: int,
        boit: bool,
        mode_paiement: str,
        id_bus_aller: Optional[int] = None,
        id_bus_retour: Optional[int] = None
    ) -> bool:
        """
        Inscrit un utilisateur à un événement.
        Gère la logique complète : vérification de capacité, création de l'inscription
        et persistance en base de données.

        id_event: ID de l'événement
        id_utilisateur: ID de l'utilisateur
        boit: Si l'utilisateur consomme de l'alcool
        mode_paiement: Mode de paiement choisi
        id_bus_aller: ID du bus aller (optionnel)
        id_bus_retour: ID du bus retour (optionnel)

        return: True si inscription réussie, False sinon
        """
        # Récupérer l'événement depuis la DB
        evenement = self.evenement_dao.get_by_id(id_event)
        if not evenement:
            print(f"Événement {id_event} introuvable.")
            return False

        # Récupérer l'utilisateur depuis la DB
        utilisateur = self.utilisateur_dao.get_by_id(id_utilisateur)
        if not utilisateur:
            print(f"Utilisateur {id_utilisateur} introuvable.")
            return False

        # Charger les inscriptions existantes pour l'événement
        evenement.inscriptions = self.inscription_dao.get_by_event(id_event)

        # Vérifier si l'événement est complet
        if evenement.est_complet():
            print(
                f"Impossible d'inscrire {utilisateur.nom} {utilisateur.prenom}. "
                f"Capacité maximale atteinte ({evenement.capacite_max})."
            )
            return False

        # Vérifier si l'utilisateur n'est pas déjà inscrit
        if any(
            insc.id_utilisateur == id_utilisateur
            for insc in evenement.inscriptions
        ):
            print(f"{utilisateur.nom} {utilisateur.prenom} est déjà inscrit.")
            return False

        # Créer la nouvelle inscription
        nouvelle_inscription = Inscription(
            id_utilisateur=id_utilisateur,
            id_event=id_event,
            boit=boit,
            mode_paiement=mode_paiement,
            id_bus_aller=id_bus_aller,
            id_bus_retour=id_bus_retour,
        )

        # Persister l'inscription en base de données
        inscription_creee = self.inscription_dao.creer(nouvelle_inscription)
        if inscription_creee:
            print(f"{utilisateur.nom} {utilisateur.prenom} est inscrit à {evenement.titre}.")
            return True
        else:
            print("Erreur lors de la création de l'inscription.")
            return False

    def ajouter_bus_a_evenement(self, id_event: int, id_bus: int) -> bool:
        """
        Associe un bus à un événement (aller ou retour selon le sens du bus).

        id_event: ID de l'événement
        id_bus: ID du bus

        return: True si association réussie, False sinon
        """
        # Récupérer l'événement
        evenement = self.evenement_dao.get_by_id(id_event)
        if not evenement:
            print(f"Événement {id_event} introuvable.")
            return False

        # Récupérer le bus
        bus = self.bus_dao.get_by_id(id_bus)
        if not bus:
            print(f"Bus {id_bus} introuvable.")
            return False

        # Associer le bus à l'événement
        evenement.ajouter_bus(bus)

        # Persister l'association en base (selon votre implémentation DAO)
        # Cela pourrait être une mise à jour de l'événement ou une table de liaison
        if self.evenement_dao.modifier(evenement):
            print(f"Bus {id_bus} associé à l'événement {evenement.titre}.")
            return True
        else:
            print("Erreur lors de l'association du bus.")
            return False
            
#######################################################################################
#optionnel
#######################################################################################

    def desinscrire_utilisateur(self, id_event: int, id_utilisateur: int) -> bool:
        """
        Désinscrit un utilisateur d'un événement.
        Supprime l'inscription de la base de données.

        id_event: ID de l'événement
        id_utilisateur: ID de l'utilisateur

        return: True si désinscription réussie, False sinon
        """
        # Récupérer l'événement et l'utilisateur
        evenement = self.evenement_dao.get_by_id(id_event)
        if not evenement:
            print(f"Événement {id_event} introuvable.")
            return False

        utilisateur = self.utilisateur_dao.get_by_id(id_utilisateur)
        if not utilisateur:
            print(f"Utilisateur {id_utilisateur} introuvable.")
            return False

        # Charger les inscriptions
        evenement.inscriptions = self.inscription_dao.get_by_event(id_event)

        # Trouver l'inscription correspondante
        inscription_a_supprimer = None
        for insc in evenement.inscriptions:
            if insc.id_utilisateur == id_utilisateur:
                inscription_a_supprimer = insc
                break

        if not inscription_a_supprimer:
            print(
                f"{utilisateur.nom} {utilisateur.prenom} n'est pas inscrit à cet événement."
            )
            return False

        # Supprimer de la base de données
        if self.inscription_dao.delete(id_event, id_utilisateur):
            print(
                f"{utilisateur.nom} {utilisateur.prenom} est désinscrit de {evenement.titre}."
            )
            return True
        else:
            print("Erreur lors de la suppression de l'inscription.")
            return False

    def get_participants(self, id_event: int) -> List:
        """
        Retourne la liste complète des utilisateurs inscrits à un événement.
        Charge les objets Utilisateur depuis la base de données.

        id_event: ID de l'événement

        return: Liste des objets Utilisateur inscrits
        """
        # Récupérer toutes les inscriptions pour cet événement
        inscriptions = self.inscription_dao.get_by_event(id_event)

        # Charger les utilisateurs correspondants
        participants = []
        for inscription in inscriptions:
            utilisateur = self.utilisateur_dao.get_by_id(inscription.id_utilisateur)
            if utilisateur:
                participants.append(utilisateur)

        return participants

    def get_evenement_avec_inscriptions(self, id_event: int) -> Optional[Evenement]:
        """
        Récupère un événement avec toutes ses inscriptions chargées.

        id_event: ID de l'événement

        return: Objet Evenement avec inscriptions ou None
        """
        evenement = self.evenement_dao.get_by_id(id_event)
        if evenement:
            evenement.inscriptions = self.inscription_dao.get_by_event(id_event)
        return evenement

    def get_evenement_avec_relations(self, id_event: int) -> Optional[Evenement]:
        """
        Récupère un événement avec toutes ses relations chargées :
        - Inscriptions
        - Bus aller et retour
        - Créateur

        id_event: ID de l'événement

        return: Objet Evenement complet ou None
        """
        evenement = self.evenement_dao.get_by_id(id_event)
        if not evenement:
            return None

        # Charger les inscriptions
        evenement.inscriptions = self.inscription_dao.get_by_event(id_event)

        # Charger le créateur
        if evenement.created_by:
            evenement.createur = self.utilisateur_dao.get_by_id(evenement.created_by)

        # Charger les bus (si vous avez une méthode pour récupérer les bus d'un événement)
        # bus_list = self.bus_dao.get_by_event(id_event)
        # for bus in bus_list:
        #     evenement.ajouter_bus(bus)

        return evenement

    def get_evenements_futurs(self) -> List[Evenement]:
        """
        Récupère tous les événements futurs (non passés).

        return: Liste des événements à venir
        """
        tous_evenements = self.evenement_dao.lister_tous()
        return [evt for evt in tous_evenements if not evt.est_passe()]

    def get_evenements_disponibles(self) -> List[Evenement]:
        """
        Récupère tous les événements futurs qui ne sont pas complets.

        return: Liste des événements disponibles pour inscription
        """
        evenements_futurs = self.get_evenements_futurs()
        
        evenements_disponibles = []
        for evenement in evenements_futurs:
            # Charger les inscriptions pour vérifier la disponibilité
            evenement.inscriptions = self.inscription_dao.get_by_event(evenement.id_event)
            if not evenement.est_complet():
                evenements_disponibles.append(evenement)
        
        return evenements_disponibles

    def modifier_evenement(self, evenement: Evenement) -> bool:
        """
        Modifie un événement existant.

        evenement: Objet Evenement avec les modifications

        return: True si modification réussie, False sinon
        """
        if self.evenement_dao.modifier(evenement):
            print(f"Événement '{evenement.titre}' modifié avec succès.")
            return True
        else:
            print("Erreur lors de la modification de l'événement.")
            return False

    def supprimer_evenement(self, id_event: int) -> bool:
        """
        Supprime un événement et toutes ses inscriptions associées.

        id_event: ID de l'événement à supprimer

        return: True si suppression réussie, False sinon
        """
        # Supprimer d'abord toutes les inscriptions
        inscriptions = self.inscription_dao.get_by_event(id_event)
        for inscription in inscriptions:
            self.inscription_dao.delete(id_event, inscription.id_utilisateur)

        # Supprimer l'événement
        if self.evenement_dao.delete(id_event):
            print(f"Événement {id_event} supprimé avec succès.")
            return True
        else:
            print("Erreur lors de la suppression de l'événement.")
            return False
