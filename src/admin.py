class Admin(Utilisateur):
    def __init__(self, id, nom, prenom, email, mdp):
        super().__init__(id, nom, prenom, email, mdp)
    def creer_evenement(self, id_evenement, date, titre, description, capacite_max):
        return Evenement(id_evenement, date, titre, description, capacite_max, self)