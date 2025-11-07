from typing import Optional, List
from business_object.inscription import Inscription
from dao.inscription_dao import InscriptionDAO
from dao.evenement_dao import EvenementDAO
from dao.utilisateur_dao import UtilisateurDAO
import random
import string
import random


class InscriptionService:
    """
    Couche service pour gérer la logique métier des inscriptions.
    Fait le lien entre les DAO et la couche de présentation.
    """

    def __init__(self):
        self.inscription_dao = InscriptionDAO()
        self.evenement_dao = EvenementDAO()
        self.utilisateur_dao = UtilisateurDAO()


    def generer_code_reservation(self, longueur: int = 8) -> str:
        """
        Génère un code de réservation unique, entièrement numérique.

        longueur: Longueur du code (par défaut 8 chiffres)

        return: Code de réservation unique
        """
        while True:
            # Génère un entier aléatoire du nombre minimal au maximal possible
            code = int(random.randint(10**(longueur - 1), 10**longueur - 1))

            # Vérifie l'unicité via la base de données / DAO
            if not self.inscription_dao.trouver_par_code_reservation(code):
                return code

    def creer_inscription(
        self,
        boit: bool,
        created_by: int,
        mode_paiement: str,
        id_event: str,
        nom_event: str,
        id_bus_aller: str = "",
        id_bus_retour: str = ""
    ) -> Optional[Inscription]:
        """
        Crée une nouvelle inscription avec validations métier.
        
        return: Inscription créée ou None si échec
        """
        # Validation : l'utilisateur existe-t-il ?
        utilisateur = self.utilisateur_dao.get_by_id(created_by)
        if not utilisateur:
            print(f"Erreur : Utilisateur {created_by} introuvable")
            return None

        # Validation : l'événement existe-t-il ?
        evenement = self.evenement_dao.get_by_id(id_event)
        if not evenement:
            print(f"Erreur : Événement {id_event} introuvable")
            return None

        # Validation : l'événement est-il complet ?
        nb_inscrits = self.inscription_dao.compter_par_evenement(id_event)
        if hasattr(evenement, 'capacite_max') and nb_inscrits >= evenement.capacite_max:
            print(f"Erreur : Événement {nom_event} complet ({nb_inscrits}/{evenement.capacite_max})")
            return None

        # Validation : l'utilisateur est-il déjà inscrit ?
        if self.est_deja_inscrit(created_by, id_event):
            print(f"Erreur : L'utilisateur {created_by} est déjà inscrit à {nom_event}")
            return None

        # Génération du code de réservation
        code_reservation = self.generer_code_reservation()

        # Création de l'objet Inscription
        try:
            inscription = Inscription(
                code_reservation=code_reservation,
                boit=boit,
                created_by=created_by,
                mode_paiement=mode_paiement,
                id_event=id_event,
                nom_event=nom_event,
                id_bus_aller=id_bus_aller,
                id_bus_retour=id_bus_retour
            )

            # Enregistrement en base de données
            return self.inscription_dao.creer(inscription)

        except ValueError as e:
            print(f"Erreur de validation : {e}")
            return None

    def obtenir_inscription(self, code_reservation: str) -> Optional[Inscription]:
        """
        Récupère une inscription par son code de réservation.
        
        return: Inscription trouvée ou None
        """
        return self.inscription_dao.trouver_par_code_reservation(code_reservation)

    def lister_inscriptions_evenement(self, id_event: str) -> List[Inscription]:
        """
        Liste toutes les inscriptions d'un événement donné.
        
        return: Liste des inscriptions
        """
        return self.inscription_dao.get_by_event(id_event)

    def lister_toutes_inscriptions(self) -> List[Inscription]:
        """
        Liste toutes les inscriptions.
        
        return: Liste de toutes les inscriptions
        """
        return self.inscription_dao.lister_toutes()

    def obtenir_nombre_inscrits(self, id_event: str) -> int:
        """
        Retourne le nombre d'inscrits à un événement.
        
        return: Nombre d'inscriptions
        """
        return self.inscription_dao.compter_par_evenement(id_event)

    def est_deja_inscrit(self, id_utilisateur: int, id_event: str) -> bool:
        """
        Vérifie si un utilisateur est déjà inscrit à un événement.
        
        return: True si déjà inscrit, False sinon
        """
        inscriptions = self.inscription_dao.get_by_event(id_event)
        return any(insc.created_by == id_utilisateur for insc in inscriptions)

    def obtenir_inscriptions_utilisateur(self, id_utilisateur: int) -> List[Inscription]:
        """
        Récupère toutes les inscriptions d'un utilisateur.
        
        return: Liste des inscriptions de l'utilisateur
        """
        toutes_inscriptions = self.inscription_dao.lister_toutes()
        return [insc for insc in toutes_inscriptions if insc.created_by == id_utilisateur]

    def calculer_statistiques_evenement(self, id_event: str) -> dict:
        """
        Calcule des statistiques sur les inscriptions d'un événement.
        
        return: Dictionnaire avec les statistiques
        """
        inscriptions = self.inscription_dao.get_by_event(id_event)
        
        total = len(inscriptions)
        nb_buveurs = sum(1 for insc in inscriptions if insc.boit)
        nb_especes = sum(1 for insc in inscriptions if insc.mode_paiement == "espèce")
        nb_en_ligne = sum(1 for insc in inscriptions if insc.mode_paiement == "en ligne")
        
        return {
            "total_inscrits": total,
            "nombre_buveurs": nb_buveurs,
            "nombre_non_buveurs": total - nb_buveurs,
            "paiements_espece": nb_especes,
            "paiements_en_ligne": nb_en_ligne,
            "paiements_non_definis": total - nb_especes - nb_en_ligne
        }

    def verifier_disponibilite_evenement(self, id_event: str) -> dict:
        """
        Vérifie la disponibilité d'un événement.
        
        return: Dictionnaire avec les infos de disponibilité
        """
        evenement = self.evenement_dao.get_by_id(id_event)
        if not evenement:
            return {"disponible": False, "raison": "Événement introuvable"}
        
        nb_inscrits = self.inscription_dao.compter_par_evenement(id_event)
        
        if hasattr(evenement, 'capacite_max'):
            places_restantes = evenement.capacite_max - nb_inscrits
            disponible = places_restantes > 0
            
            return {
                "disponible": disponible,
                "places_restantes": places_restantes,
                "capacite_max": evenement.capacite_max,
                "nombre_inscrits": nb_inscrits,
                "taux_remplissage": round((nb_inscrits / evenement.capacite_max) * 100, 2)
            }
        
        return {
            "disponible": True,
            "nombre_inscrits": nb_inscrits,
            "capacite_max": None
        }