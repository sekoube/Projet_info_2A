import uuid
from datetime import datetime


class Inscription:
    _compteurs = {}

    def __init__(self, boit, mode_paiement, id_event, nom_event, id_bus_aller, id_bus_retour):
        if nom_event not in Inscription._compteurs:
            Inscription._compteurs[nom_event] = 0
        Inscription._compteurs[nom_event] += 1
        numero = Inscription._compteurs[nom_event]
        code_unique = uuid.uuid4().hex[:8]
        self.id = f"{nom_event}_{numero}_{code_unique}"
        self.boit = boit
        self.mode_paiement = mode_paiement
        self.id_event = id_event
        self.nom_event = nom_event
        self.id_bus_aller = id_bus_aller
        self.id_bus_retour = id_bus_retour
        self.date_creation = datetime.now()
