from typing import Optional
from business_object.bus import Bus
from dao.bus_dao import BusDAO
from dao.evenement_dao import EvenementDAO
from time import time


class BusService:
    """Service gérant la logique métier des bus."""

    def __init__(self):
        self.bus_dao = BusDAO()
        self.evenement_dao = EvenementDAO()

    def creer_bus(self, 
                  id_event: int, 
                  sens: str, 
                  description: Optional[str], 
                  heure_depart: time, 
                  capacite_max: int) -> Optional[Bus]:
        """
        Crée un nouvel objet Bus à partir des paramètres, valide les données, 
        et l'insère via la DAO.
        
        :param id_event: ID de l'événement associé.
        :param sens: Direction du bus (e.g., 'Aller' ou 'Retour').
        :param description: Description du trajet.
        :param heure_depart: Heure de départ prévue.
        :param capacite_max: Capacité maximale du bus.
        :return: L'objet Bus inséré avec son id_bus généré, ou None en cas d'erreur.
        """
        
        # --- 1. Validation des données ---
        if not id_event or not sens or not capacite_max:
            print("Erreur de validation : Les champs essentiels sont requis.")
            return None
        
        if capacite_max <= 0:
             print("Erreur de validation : La capacité maximale doit être positive.")
             return None
        
        # --- 2. Création de l'objet Modèle (Bus) ---
        # Le Service crée l'objet que la DAO attend
        nouveau_bus = Bus(
            id_bus=None, # L'ID sera généré par la BDD
            id_event=id_event,
            sens=sens,
            description=description,
            heure_depart=heure_depart,
            capacite_max=capacite_max
        )
        
        # --- 3. Appel à la DAO ---
        try:
            # L'appel à la DAO exécute la logique SQL et met à jour nouveau_bus.id_bus
            bus_cree = self.bus_dao.creer(nouveau_bus)
            
            return bus_cree
            
        except Exception as e:
            # Gérer les exceptions de la DAO
            print(f"Erreur lors de la création du bus dans le service : {e}")
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
        bus = self.bus_dao.get_by("id_bus", id_bus)
        if not bus:
            print(f"Bus {id_bus} introuvable")
            return False
        
        try:
            return self.bus_dao.supprimer(id_bus)
        except Exception as e:
            print(f"Erreur lors de la suppression du bus : {e}")
            return False


    def get_bus_by(self, field: str, value) -> Optional[Bus]:
        """
        Récupère un Bus selon un champ donné.

        field : nom du champ (ex: "id_bus", "id_event", "sens", etc.)
        value : valeur à chercher

        return : Bus ou None si non trouvé
        """
        try:
            return self.bus_dao.get_by(field, value)
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