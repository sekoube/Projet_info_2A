from utilisateur import Utilisateur
from evenement import Evenement

class Admin(Utilisateur):
    
    def __init__(self, id_utilisateur, pseudo, nom, prenom, email, mot_de_passe):
        super().__init__(id_utilisateur=id_utilisateur, pseudo=pseudo, nom=nom, prenom=prenom, email=email, mot_de_passe=mot_de_passe, role=True)

    def creer_evenement(self, titre, lieu, date_evenement, capacite_max, tarif, id_event):
        return Evenement(
            id_event=id_event,
            titre=titre,
            lieu=lieu,
            date_evenement=date_evenement,
            capacite_max=capacite_max,
            tarif=tarif,
            created_by=self.id_utilisateur
        )
    
    def supp_participant(self, evenement: Evenement, participant_a_retirer):
        return evenement.desinscrire(participant_a_retirer)

