import pytest
from datetime import datetime, date
from business_object.inscription import Inscription
from business_object.utilisateur import Utilisateur
from dao.inscription_dao import InscriptionDAO
from dao.evenement_dao import EvenementDAO
from dao.utilisateur_dao import UtilisateurDAO
from dao.bus_dao import BusDAO
from service.inscription_service import InscriptionService


class TestIntegrationInscription:
    """
    Tests d'intégration pour le module Inscription.
    Ces tests vérifient l'interaction entre Service, DAO et la base de données.
    Utilise les fixtures de conftest.py pour la configuration.
    """

    @pytest.fixture(autouse=True)
    def setup(self, utilisateur_test, evenement_test):
        """
        Configuration automatique avant chaque test.
        Utilise les fixtures conftest pour créer utilisateur et événement.
        """
        # Initialiser les DAO et Services
        self.inscription_dao = InscriptionDAO()
        self.evenement_dao = EvenementDAO()
        self.utilisateur_dao = UtilisateurDAO()
        self.bus_dao = BusDAO()
        self.inscription_service = InscriptionService(
            self.inscription_dao,
            self.evenement_dao,
            self.utilisateur_dao
        )
        
        # Utiliser les fixtures
        self.test_user = utilisateur_test
        self.test_event = evenement_test
        
        # Créer des bus de test
        from business_object.bus import Bus
        
        bus_aller_obj = Bus(
            id_event=self.test_event.id_event,
            sens="aller",
            description="Bus aller Paris-Festival",
            capacite_max=50,
            heure_depart="08:00"
        )
        self.bus_aller = self.bus_dao.creer(bus_aller_obj)
        
        bus_retour_obj = Bus(
            id_event=self.test_event.id_event,
            sens="retour",
            description="Bus retour Festival-Paris",
            capacite_max=50,
            heure_depart="23:00"
        )
        self.bus_retour = self.bus_dao.creer(bus_retour_obj)

    def test_creer_inscription_complete(self):
        """
        Création d'une inscription complète avec tous les champs.
        Vérifie que l'inscription est bien créée en base avec un code de réservation.
        """

        # Créer l'inscription via le service
        inscription = self.inscription_service.creer_inscription(
            boit=True,
            mode_paiement="en ligne",
            id_event=self.test_event.id_event,
            nom_event=self.test_event.titre,
            id_bus_aller=self.bus_aller.id_bus,
            id_bus_retour=self.bus_retour.id_bus,
            created_by=self.test_user.id_utilisateur
        )
        
        # Assertions
        assert inscription is not None, "L'inscription devrait être créée"
        assert inscription.code_reservation is not None, "Un code de réservation devrait être généré"
        assert inscription.boit is True, "Le champ 'boit' devrait être True"
        assert inscription.mode_paiement == "en ligne"
        assert inscription.id_event == self.test_event.id_event
        assert inscription.created_by == self.test_user.id_utilisateur
        
        print(f"✅ Inscription créée avec succès : {inscription}")
        print(f"   Code de réservation : {inscription.code_reservation}")

    def test_lister_toutes_inscriptions(self, unique_email):
        """
        Création de plusieurs inscriptions et listage complet.
        Vérifie que toutes les inscriptions sont bien récupérées.
        """
        
        # Créer plusieurs utilisateurs et inscriptions
        utilisateurs = []
        inscriptions_creees = []
        
        for i in range(3):
            # Créer un utilisateur avec email unique
            user = Utilisateur(
                nom=f"Test{i}",
                prenom=f"User{i}",
                email=f"user{i}.{datetime.now().timestamp()}@test.com",
                mot_de_passe="pass123",
                role=False
            )
            user = self.utilisateur_dao.creer(user)
            utilisateurs.append(user)
            
            # Créer une inscription pour cet utilisateur
            inscription = self.inscription_service.creer_inscription(
                boit=(i % 2 == 0),
                mode_paiement="espece" if i % 2 == 0 else "en ligne",
                id_event=self.test_event.id_event,
                nom_event=self.test_event.titre,
                id_bus_aller=self.bus_aller.id_bus,
                id_bus_retour=self.bus_retour.id_bus,
                created_by=user.id_utilisateur
            )
            inscriptions_creees.append(inscription)
        
        # Lister toutes les inscriptions
        toutes_inscriptions = self.inscription_service.lister_toutes_inscriptions()
        
        # Assertions
        assert len(toutes_inscriptions) >= 3, "Au moins 3 inscriptions devraient exister"
        
        # Vérifier que nos inscriptions sont dans la liste
        codes_reserves = [insc.code_reservation for insc in inscriptions_creees]
        codes_listes = [insc.code_reservation for insc in toutes_inscriptions]
        
        for code in codes_reserves:
            assert code in codes_listes, f"L'inscription {code} devrait être dans la liste"
        
        print(f"✅ {len(toutes_inscriptions)} inscriptions listées avec succès")

    def test_rechercher_inscription_par_code(self):
        """
        Recherche d'une inscription par son code de réservation.
        Vérifie que la méthode get_by retourne la bonne inscription.
        """

        # Créer une inscription
        inscription_originale = self.inscription_service.creer_inscription(
            boit=False,
            mode_paiement="espece",
            id_event=self.test_event.id_event,
            nom_event=self.test_event.titre,
            id_bus_aller=self.bus_aller.id_bus,
            id_bus_retour=self.bus_retour.id_bus,
            created_by=self.test_user.id_utilisateur
        )
        
        # Rechercher l'inscription par son code
        inscriptions_trouvees = self.inscription_service.get_inscription_by(
            "code_reservation",
            inscription_originale.code_reservation
        )
        
        # Assertions
        assert inscriptions_trouvees is not None, "L'inscription devrait être trouvée"
        assert len(inscriptions_trouvees) == 1, "Une seule inscription devrait correspondre"
        
        inscription_trouvee = inscriptions_trouvees[0]
        assert inscription_trouvee.code_reservation == inscription_originale.code_reservation
        assert inscription_trouvee.created_by == self.test_user.id_utilisateur
        assert inscription_trouvee.boit is False
        
        print(f"✅ Inscription trouvée : {inscription_trouvee}")
        print(f"   Code : {inscription_trouvee.code_reservation}")

    def test_compter_inscriptions_par_evenement(self):
        """
        Comptage du nombre d'inscriptions pour un événement.
        Vérifie que le compteur est correct après plusieurs inscriptions.
        """
        
        # Compter les inscriptions initiales
        nb_initial = self.inscription_dao.compter_par_evenement(self.test_event.id_event)
        print(f"Nombre d'inscriptions initial : {nb_initial}")
        
        # Créer plusieurs inscriptions
        nb_nouvelles_inscriptions = 5
        
        for i in range(nb_nouvelles_inscriptions):
            user = Utilisateur(
                nom=f"Compteur{i}",
                prenom=f"Test{i}",
                email=f"compteur{i}.{datetime.now().timestamp()}@test.com",
                mot_de_passe="pass123",
                role=False
            )
            user = self.utilisateur_dao.creer(user)
            
            self.inscription_service.creer_inscription(
                boit=True,
                mode_paiement="en ligne",
                id_event=self.test_event.id_event,
                nom_event=self.test_event.titre,
                id_bus_aller=self.bus_aller.id_bus,
                id_bus_retour=self.bus_retour.id_bus,
                created_by=user.id_utilisateur
            )
        
        # Compter à nouveau
        nb_final = self.inscription_dao.compter_par_evenement(self.test_event.id_event)
        
        # Assertions
        assert nb_final == nb_initial + nb_nouvelles_inscriptions, \
            f"Le nombre devrait être {nb_initial + nb_nouvelles_inscriptions}"
        
        print(f"✅ Comptage correct : {nb_final} inscriptions pour l'événement")

    def test_suppression_inscription_autorisee(self):
        """
        Suppression d'une inscription par son propriétaire.
        Vérifie que l'inscription est bien supprimée de la base.
        """
        
        # Créer une inscription
        inscription = self.inscription_service.creer_inscription(
            boit=True,
            mode_paiement="espece",
            id_event=self.test_event.id_event,
            nom_event=self.test_event.titre,
            id_bus_aller=self.bus_aller.id_bus,
            id_bus_retour=self.bus_retour.id_bus,
            created_by=self.test_user.id_utilisateur
        )
        
        code_reservation = inscription.code_reservation
        print(f"Inscription créée avec le code : {code_reservation}")
        
        # Vérifier que l'inscription existe
        inscriptions_avant = self.inscription_dao.get_by("code_reservation", code_reservation)
        assert len(inscriptions_avant) == 1, "L'inscription devrait exister"
        
        # Supprimer l'inscription
        resultat = self.inscription_service.supprimer_inscription(
            code_reservation=code_reservation,
            id_utilisateur=self.test_user.id_utilisateur
        )
        
        # Assertions
        assert resultat is True, "La suppression devrait réussir"
        
        # Vérifier que l'inscription n'existe plus
        inscriptions_apres = self.inscription_dao.get_by("code_reservation", code_reservation)
        assert len(inscriptions_apres) == 0, "L'inscription ne devrait plus exister"
        
        print(f"✅ Inscription {code_reservation} supprimée avec succès")


if __name__ == "__main__":
    # Pour exécuter les tests directement
    pytest.main([__file__, "-v"])