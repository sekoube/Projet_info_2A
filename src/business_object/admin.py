from utilisateur import Utilisateur
from evenement import Evenement
from datetime import datetime
from datetime import datetime
from business_object.evenement import Evenement

class Administrateur(Utilisateur):
    """
    Classe représentant un administrateur de l'application. Un administrateur hérite des
    propriétés et méthodes de la classe Utilisateur, et peut gérer les événements.
    """

    def __init__(self, id_admin: int, pseudo: str, nom: str, prenom: str, email: str, mot_de_passe: str, role: bool = True):
        super().__init__(id_utilisateur=id_admin, pseudo=pseudo, nom=nom, prenom=prenom, email=email, mot_de_passe=mot_de_passe, role=role)

    def creer_evenement(self, titre: str, description: str, lieu: str, date: datetime, capacite_max: int, tarif: float) -> Evenement:
        """Création de l'événement (logique métier)"""
        if capacite_max <= 0:
            raise ValueError("La capacité maximale doit être supérieure à zéro.")
        
        if date < datetime.now():
            raise ValueError("La date de l'événement ne peut pas être dans le passé.")
        
        evenement = Evenement(
            titre=titre,
            description=description,
            lieu=lieu,
            date=date,
            capacite_max=capacite_max,
            tarif=tarif,
            pseudo_createur=self.pseudo
        )
        return evenement

    def supprimer_evenement(self, evenement: Evenement) -> bool:
        """Supprimer un événement (via le service)"""
        pass

    def consulter_evenements(self) -> list:
        """Consulter les événements existants (via le service)"""
        pass
