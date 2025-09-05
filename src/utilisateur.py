class Utilisateur:
    def __init__(self, id, nom, prenom, email, mdp):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.mdp = mdp
        self.evenements = []

    def s_inscrire(self, evenement):
        if evenement not in self.evenements:
            evenement.inscrire(self)
            self.evenements.append(evenement)
            print(f"{utilisateur.nom} est inscrit à {self.titre}.")
        else :
            print(f"{utilisateur.nom} est déjà inscrit à {self.titre}.")

    def __str__(self):
        return f"{self.nom} {self.prenom}"