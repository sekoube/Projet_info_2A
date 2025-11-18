# src/service/bus_service.py
from typing import Optional
from business_object.bus import Bus
from dao.bus_dao import BusDAO
from dao.evenement_dao import EvenementDAO


class BusService:
    """Service gérant la logique métier des bus."""

    def __init__(self):
        self.bus_dao = BusDAO()
        self.evenement_dao = EvenementDAO()

    def creer_bus(self, bus: Bus) -> Optional[Bus]:
        """
        Crée un nouveau bus (réservé aux admins).
        
        Args:
            bus: L'objet Bus à créer
            
        Returns:
            Bus créé ou None si échec
            
        Raises:
            ValueError: Si l'événement n'existe pas
        """

        # Vérification que l'événement existe
        evenement = self.evenement_dao.get_by_id(bus.id_event)
        if not evenement:
            raise ValueError(f"L'événement {bus.id_event} n'existe pas")
        
        try:
            return self.bus_dao.creer(bus)
        except Exception as e:
            print(f"Erreur lors de la création du bus : {e}")
            return None

    def supprimer_bus(self, id_bus: int) -> bool:
        """
        Supprime un bus (réservé aux admins).
        
        Args:
            id_bus: ID du bus à supprimer
            
        Returns:
            True si suppression réussie, False sinon
            
        """
        
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


    def get_bus_by_field(self, field: str, value) -> Optional[Bus]:
        """
        Récupère un Bus selon un champ donné.

        field : nom du champ (ex: "id_bus", "id_event", "sens", etc.)
        value : valeur à chercher

        return : Bus ou None si non trouvé
        """
        try:
            return self.bus_dao.get_by_field(field, value)
        except ValueError as ve:
            # Capture la validation du champ
            print(f"Champ non autorisé : {ve}")
            return None
        except Exception as e:
            # Autres erreurs (connexion, SQL, etc.)
            print(f"Erreur lors de la récupération du bus : {e}")
            return None


    def get_tous_les_bus(self) -> list[Bus]:
        """Récupère tous les bus."""
        try:
            return self.bus_dao.lister_tous()
        except Exception as e:
            print(f"Erreur lors de la récupération des bus : {e}")
            return []