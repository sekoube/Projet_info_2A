# src/service/bus_service.py
from typing import Optional
from business_object.bus import Bus
from business_object.utilisateur import Utilisateur
from dao.bus_dao import BusDAO
from dao.evenement_dao import EvenementDAO
from service.utilisateur_service import UtilisateurService


class BusService:
    """Service gérant la logique métier des bus."""

    def __init__(self):
        self.bus_dao = BusDAO()
        self.evenement_dao = EvenementDAO()
        self.utilisateur_service = UtilisateurService()

    def creer_bus(self, bus: Bus, utilisateur: Utilisateur) -> Optional[Bus]:
        """
        Crée un nouveau bus (réservé aux admins).
        
        Args:
            bus: L'objet Bus à créer
            utilisateur: L'utilisateur qui effectue l'action
            
        Returns:
            Bus créé ou None si échec
            
        Raises:
            PermissionError: Si l'utilisateur n'est pas admin
            ValueError: Si l'événement n'existe pas
        """
        # Vérification des droits admin
        if not self.utilisateur_service.is_admin(utilisateur):
            raise PermissionError("Seuls les administrateurs peuvent créer des bus")
        
        # Vérification que l'événement existe
        evenement = self.evenement_dao.get_by_id(bus.id_event)
        if not evenement:
            raise ValueError(f"L'événement {bus.id_event} n'existe pas")
        
        try:
            return self.bus_dao.creer(bus)
        except Exception as e:
            print(f"Erreur lors de la création du bus : {e}")
            return None

    def supprimer_bus(self, id_bus: int, utilisateur: Utilisateur) -> bool:
        """
        Supprime un bus (réservé aux admins).
        
        Args:
            id_bus: ID du bus à supprimer
            utilisateur: L'utilisateur qui effectue l'action
            
        Returns:
            True si suppression réussie, False sinon
            
        Raises:
            PermissionError: Si l'utilisateur n'est pas admin
        """
        # Vérification des droits admin
        if not self.utilisateur_service.is_admin(utilisateur):
            raise PermissionError("Seuls les administrateurs peuvent supprimer des bus")
        
        # Vérification que le bus existe
        bus = self.bus_dao.get_by_id(id_bus)
        if not bus:
            print(f"Bus {id_bus} introuvable")
            return False
        
        try:
            return self.bus_dao.supprimer(id_bus)
        except Exception as e:
            print(f"Erreur lors de la suppression du bus : {e}")
            return False

    def modifier_bus(
        self, 
        id_bus: int, 
        utilisateur: Utilisateur,
        **kwargs
    ) -> Optional[Bus]:
        """
        Modifie les informations d'un bus (réservé aux admins).
        
        Args:
            id_bus: ID du bus à modifier
            utilisateur: L'utilisateur qui effectue l'action
            **kwargs: Attributs à modifier (sens, description, heure_depart)
            
        Returns:
            Bus modifié ou None si échec
            
        Raises:
            PermissionError: Si l'utilisateur n'est pas admin
        """
        # Vérification des droits admin
        if not self.utilisateur_service.is_admin(utilisateur):
            raise PermissionError("Seuls les administrateurs peuvent modifier des bus")
        
        # Récupération du bus existant
        bus = self.bus_dao.get_by_id(id_bus)
        if not bus:
            print(f"Bus {id_bus} introuvable")
            return None
        
        # Application des modifications
        if 'sens' in kwargs:
            bus.sens = kwargs['sens']
        if 'description' in kwargs:
            bus.description = kwargs['description']
        if 'heure_depart' in kwargs:
            bus.heure_depart = kwargs['heure_depart']
        
        return bus

    def peut_creer_bus(self, utilisateur: Utilisateur) -> bool:
        """
        Vérifie si un utilisateur peut créer un bus.
        
        Args:
            utilisateur: L'utilisateur à vérifier
            
        Returns:
            True si l'utilisateur est admin, False sinon
        """
        return self.utilisateur_service.is_admin(utilisateur)

    # ... (le reste des méthodes restent identiques)
    def get_bus_by_event(self, id_event: int) -> Optional[Bus]:
        """Récupère les bus d'un événement."""
        try:
            return self.bus_dao.get_by_event(id_event)
        except Exception as e:
            print(f"Erreur lors de la récupération des bus : {e}")
            return None

    def get_bus_by_id(self, id_bus: int) -> Optional[Bus]:
        """Récupère un bus par son ID."""
        try:
            return self.bus_dao.get_by_id(id_bus)
        except Exception as e:
            print(f"Erreur lors de la récupération du bus : {e}")
            return None

    def get_tous_les_bus(self) -> list[Bus]:
        """Récupère tous les bus."""
        try:
            return self.bus_dao.trouver_tous()
        except Exception as e:
            print(f"Erreur lors de la récupération des bus : {e}")
            return []

    def get_bus_disponibles_pour_evenement(self, id_event: int) -> dict:
        """Récupère les bus disponibles pour un événement (aller et retour)."""
        try:
            tous_les_bus = self.bus_dao.trouver_tous()
            bus_evenement = [bus for bus in tous_les_bus if bus.id_event == id_event]
            
            return {
                'aller': [bus for bus in bus_evenement if bus.sens],
                'retour': [bus for bus in bus_evenement if not bus.sens]
            }
        except Exception as e:
            print(f"Erreur lors de la récupération des bus disponibles : {e}")
            return {'aller': [], 'retour': []}