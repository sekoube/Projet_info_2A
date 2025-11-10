from datetime import datetime


class Bus:
    """
    Classe métier représentant un bus pour un trajet (vers l'évènement ou au retour de l'évènement).
    Cette classe contient uniquement la logique métier et les attributs de l'entité.
    """
    
    def __init__(self, id_event, sens, description, heure_depart, capacite_max, id_bus=None):
        """
        Constructeur de la classe Bus.
        
        Parameters:
            id_event (str): Identifiant de l'évènement auquel le bus est attribué
            sens (str): Direction du trajet ("Aller" ou "Retour")
            description (list): Liste des arrêts intermédiaires (écrire ['direct'] si aucun)
            heure_depart (str|datetime): Heure de départ du bus (format "HH:MM" ou datetime)
            id_bus (int, optional): Identifiant unique du bus (None avant insertion en base)
        
        Raises:
            ValueError: Si les validations échouent
        """

        # ========================== VALIDATIONS ==========================
        if not id_event or id_event is None:
            raise ValueError("L'identifiant de l'évènement doit être renseigné")

        #if not sens == "":
        #    raise ValueError("Le sens ne peut pas être vide")
        
        #if sens not in ["Aller", "Retour"]:
        #    raise ValueError("Le sens doit être 'Aller' ou 'Retour'")

        if not description or description == [] or description == ['']:
            raise ValueError("Les arrêts intermédiaires doivent être renseignés, sinon écrire ['direct']")

        if not heure_depart:
            raise ValueError("L'heure de départ du bus est obligatoire")
        # =================================================================

        # Assignation des attributs
        self.id_bus = id_bus
        self.id_event = id_event
        
        # Conversion du sens en booléen (True = Aller, False = Retour)
        self.sens = (sens == "Aller")
        
        self.description = description
        self.capacite_max = capacite_max
        # Conversion de l'heure de départ en datetime si c'est une string
        if isinstance(heure_depart, str):
            try:
                self.heure_depart = datetime.strptime(heure_depart, "%H:%M")
            except ValueError as e:
                raise ValueError(f"Format d'heure invalide. Attendu 'HH:MM', reçu '{heure_depart}'") from e
        else:
            self.heure_depart = heure_depart

    def __str__(self):
        """Représentation textuelle du bus"""
        sens_texte = "Aller" if self.sens else "Retour"
        heure = self.heure_depart.strftime("%H:%M") if isinstance(self.heure_depart, datetime) else self.heure_depart
        return f"Bus #{self.id_bus} - Évènement {self.id_event} - {sens_texte} à {heure}"

    def __repr__(self):
        """Représentation technique du bus"""
        return f"Bus(id_bus={self.id_bus}, id_event={self.id_event}, sens={'Aller' if self.sens else 'Retour'})"
    
    @staticmethod
    def from_dict(data: dict) -> "Bus":
        """Construit un objet Bus à partir d'un dictionnaire (row SQL)."""
        return Bus(
            id_bus=data.get("id_bus"),
            id_event=data.get("id_event"),
            sens=data.get("sens"),
            description=data.get("description"),
            heure_depart=data.get("heure_depart")
        )