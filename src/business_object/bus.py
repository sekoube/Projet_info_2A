class Bus:
    """
    Classe métier représentant un bus pour un trajet (vers l'évènement ou au retour de l'évènement).
    Cette classe contient uniquement la logique métier et  les attributs de l'entité.
    """
    def __init__(self, id_bus, id_event, sens, description, heure_depart):
        """ Constructeur de la classe Bus.
        
            id_bus : Identifiant unique du bus (auto-incrémenté de base)
            id_event : Identifiant de l'évènement auquel le bus est attribué
            sens : aller ou retour de l'évènement ("aller" ou "retour")
            description : liste des arrêts intermédiaires (max 100 caractères)
            heure_depart : heure de départ du bus
        """

        # ========================== VALIDATIONS ==========================
        if not id_event or id_event is None:
            raise ValueError("L'identifiant de l'évènement doit être renseigné")

        if not sens or sens.strip() == "":
            raise ValueError("Le sens ne peut pas être vide")
        if sens != "aller" and sens != "retour" :
            raise ValueError("Le sens doit être 'aller' ou 'retour'")

        if not description or description.strip() == "" :
            raise ValueError("Les arrêts intermédiaires doivent être renseignés, sinon écrire 'direct'")

        if not heure_depart :
            raise valueError("L'heure de départ du bus est obligatoire")
        
        self.id_bus = id_bus
        self.id_event = id_event
        self.sens = sens
        self.description = description
        self.heure_depart = heure_depart
