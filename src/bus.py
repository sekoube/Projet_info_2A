class Bus:
    def __init__(self, id_bus, date, sens, arrêts, capacite_max, evenement, createur):
        self.id_bus = id_bus
        self.date = date
        self.sens = sens
        self.arrêts = arrêts
        self.capacite_max = capacite_max
        self.evenement = evenement
        self.createur = createur
        self.participants = []