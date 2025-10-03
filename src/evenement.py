from datetime import datetime

class Evenement:
    def __init__(self, id_event, date_event, titre, description_event, lieu, capacite_max, created_by, created_at, tarif ):
        self.id_event = id_event
        self.date_event = date_event
        self.titre = titre
        self.description_event = description_event
        self.lieu = lieu
        self.capacite_max = capacite_max
        self.created_by = created_by
        self.created_at = created_at if created_at else datetime.now()
        self.tarif = tarif
        self.participants = []
        self.bus_aller = None
        self.bus_retour = None

    def inscrire(self, utilisateur):
        if utilisateur not in self.participants:
            self.participants.append(utilisateur)
            print(f"{utilisateur.nom} {utilisateur.prenom} est inscrit à {self.titre}.")
        else:
            print(f"{utilisateur.nom} {utilisateur.prenom} est déjà inscrit.")

    def __str__(self):
        return f"{self.titre} ({self.date})"
