class Admin(Utilisateur):
    def __init__(self, id, nom, prenom, email, mdp):
        super().__init__(id, nom, prenom, email, mdp)

    def creer_evenement(self, id_evenement, date, titre, description, capacite_max):
        return Evenement(id_evenement, date, titre, description, capacite_max, self)
    
    def supp_participant(self, evenement, participant_a_retirer):
        if participant_a_retirer in evenement.participants:
            evenement.participants.remove(participant_a_retirer)
            print(f"{participant_a_retirer.prenom} {participant_a_retirer.nom} a bien été désinscrit de l'évènement")
            return True
        else:
            print(f"{participant_a_retirer.prenom} {participant_a_retirer.nom} n'est pas inscrit à l'évènement")
            return False

