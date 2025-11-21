# business_object/bus.py
from datetime import datetime


class Bus:
    """
    Représente un bus pour un événement.
    
    Attributes:
        id_bus (int): Identifiant unique du bus
        id_event (int): Identifiant de l'événement associé
        sens (bool): Direction du bus (True = Aller, False = Retour)
        description (list): Liste des arrêts
        heure_depart (datetime): Heure de départ
        capacite_max (int): Capacité maximale du bus
    """
    
    def __init__(
        self,
        id_event: int,
        sens: str,
        heure_depart: str,
        capacite_max: int,
        description: str,
        id_bus: int = None
    ):
        """
        Constructeur de la classe Bus.
        
        Parameters:
            id_event (str): Identifiant de l'évènement auquel le bus est attribué
            sens (str): Direction du trajet ("Aller" ou "Retour")
            description (str): description du bus (arrêts)
            heure_depart (datetime): Heure de départ du bus (format "HH:MM" ou datetime)
            id_bus (int, optional): Identifiant unique du bus (None avant insertion en base)
        
        Args:
            id_event: Identifiant de l'événement
            sens: Direction ('Aller', 'aller', 'Retour', 'retour', etc.)
            heure_depart: Heure de départ (format HH:MM)
            capacite_max: Capacité maximale du bus
            description: description (arrêts)
            id_bus: Identifiant du bus (optionnel)
            
        Raises:
            ValueError: Si les paramètres sont invalides
        """
        # Validation de id_event
        if not id_event:
            raise ValueError("L'identifiant de l'évènement doit être renseigné")
        
        # Validation du sens
        if not sens:
            raise ValueError("Le sens ne peut pas être vide")
        
        # Normaliser le sens en majuscule pour la validation
        sens_normalise = sens.upper()
        
        if sens_normalise not in ["ALLER", "RETOUR"]:
            raise ValueError("Le sens doit être 'Aller' ou 'Retour' (majuscule/minuscule acceptée)")
        
        # Validation de la capacité maximale
        if capacite_max <= 0:
            raise ValueError("La capacité maximale doit être supérieure à 0")
        
        # Assignation des attributs
        self.id_bus = id_bus
        self.id_event = id_event
        self.sens = sens_normalise
        
        self.description = description
        
        # Conversion de l'heure en datetime
        if isinstance(heure_depart, str):
            self.heure_depart = datetime.strptime(heure_depart, "%H:%M")
        else:
            self.heure_depart = heure_depart
        
        self.capacite_max = capacite_max
    
    @classmethod
    def from_dict(cls, data: dict):
        """
        Crée un objet Bus à partir d'un dictionnaire (depuis la base de données).
        
        Args:
            data: Dictionnaire contenant les données du bus
            
        Returns:
            Bus: Instance de Bus créée à partir du dictionnaire
        """
        
        # Convertir l'heure si c'est une string, sinon la garder telle quelle
        heure_depart = data.get("heure_depart")
        if isinstance(heure_depart, datetime):
            heure_depart = heure_depart.strftime("%H:%M")
        
        return cls(
            id_event=data.get("id_event"),
            sens=data.get("sens"),
            heure_depart=heure_depart,
            capacite_max=data.get("capacite_max"),
            description=data.get("description"),
            id_bus=data.get("id_bus")
        )
    
    def to_dict(self):
        """
        Convertit l'objet Bus en dictionnaire (pour la base de données).
        
        Returns:
            dict: Dictionnaire représentant le bus
        """
        return {
            "id_bus": self.id_bus,
            "id_event": self.id_event,
            "sens": self.sens,
            "description": self.description,
            "heure_depart": self.heure_depart.strftime("%H:%M") if isinstance(self.heure_depart, datetime) else self.heure_depart,
            "capacite_max": self.capacite_max
        }
    
    def __repr__(self):
        return (f"Bus(id_bus={self.id_bus}, id_event={self.id_event}, "
                f"sens={self.get_sens()}, heure_depart='{self.heure_depart.strftime('%H:%M')}', "
                f"capacite_max={self.capacite_max})")
    
    def __str__(self):
        return f"Bus {self.get_sens()} - Départ: {self.heure_depart.strftime('%H:%M')} ({self.capacite_max} places)"