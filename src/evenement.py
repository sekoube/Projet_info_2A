class Evenement:
    def __init__(self, id_evenement, date, titre, description, capacite_max, createur):
        self.id_evenement = id_evenement
        self.date = date
        self.titre = titre
        self.description = description
        self.capacite_max = capacite_max
        self.createur = createur
        self.participants = []

    def inscrire(self, utilisateur):
        if utilisateur not in self.participants:
            self.participants.append(utilisateur)
            print(f"{utilisateur.nom} {utilisateur.prenom} est inscrit à {self.titre}.")
        else:
            print(f"{utilisateur.nom} {utilisateur.prenom} est déjà inscrit.")

    def __str__(self):
        return f"{self.titre} ({self.date})"