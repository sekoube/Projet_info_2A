# tests/test_service/test_inscription_service.py
import pytest
from datetime import date, timedelta
from service.inscription_service import InscriptionService
from business_object.utilisateur import Utilisateur
from business_object.evenement import Evenement
from business_object.bus import Bus
from dao.utilisateur_dao import UtilisateurDAO
from dao.evenement_dao import EvenementDAO
from dao.bus_dao import BusDAO


class TestInscriptionService:
    """Tests pour InscriptionService"""

    @pytest.fixture
    def inscription_service(self):
        """Fixture pour créer une instance du service"""
        return InscriptionService()

    @pytest.fixture
    def utilisateur_test(self):
        """Crée un utilisateur de test"""
        utilisateur = Utilisateur(
            pseudo="testuser",
            nom="Test",
            prenom="User",
            email="test@example.com",
            mot_de_passe="Password123!"
        )
        # Le DAO modifie utilisateur par effet de bord et retourne bool
        if UtilisateurDAO().creer(utilisateur):
            return utilisateur
        return None

    @pytest.fixture
    def evenement_test(self, utilisateur_test):
        """Crée un événement de test"""
        evenement = Evenement(
            titre="Soirée Test",
            description_evenement="Event pour les tests",
            lieu="Rennes",
            date_evenement=date.today() + timedelta(days=30),
            capacite_max=50,
            created_by=utilisateur_test.id_utilisateur,
            tarif=15.0
        )
        # Le DAO modifie evenement par effet de bord et retourne bool
        if EvenementDAO().creer(evenement):
            return evenement
        return None

    @pytest.fixture
    def bus_test(self, evenement_test):
        """Crée des bus de test pour l'événement"""
        # Créer un bus aller
        bus_aller = Bus(
            capacite_max=50,
            id_event=evenement_test.id_event,
            sens="aller",
            heure_depart="08:00"
        )
        BusDAO().creer(bus_aller)
        
        # Créer un bus retour
        bus_retour = Bus(
            capacite_max=50,
            id_event=evenement_test.id_event,
            sens="retour",
            heure_depart="23:00"
        )
        BusDAO().creer(bus_retour)
        
        return {"aller": bus_aller, "retour": bus_retour}

    def test_creer_inscription_succes(self, inscription_service, utilisateur_test, evenement_test, bus_test):
        """
        Test : Création d'une inscription valide
        GIVEN un utilisateur, un événement et des bus valides
        WHEN on crée une inscription
        THEN l'inscription est créée avec un code de réservation unique
        """
        # Act
        inscription = inscription_service.creer_inscription(
            boit=True,
            created_by=utilisateur_test.id_utilisateur,
            mode_paiement="en ligne",
            id_event=evenement_test.id_event,
            nom_event=evenement_test.titre,
            id_bus_aller=bus_test["aller"].id_bus,
            id_bus_retour=bus_test["retour"].id_bus
        )

        # Assert
        assert inscription is not None
        assert inscription.code_reservation is not None
        assert len(str(inscription.code_reservation)) == 8
        assert inscription.boit is True
        assert inscription.mode_paiement == "en ligne"
        assert inscription.created_by == utilisateur_test.id_utilisateur
        assert inscription.id_event == evenement_test.id_event
        assert inscription.id_bus_aller == bus_test["aller"].id_bus
        assert inscription.id_bus_retour == bus_test["retour"].id_bus

    def test_creer_inscription_utilisateur_inexistant(self, inscription_service, evenement_test, bus_test):
        """
        Test : Tentative d'inscription avec un utilisateur inexistant
        GIVEN un ID utilisateur qui n'existe pas
        WHEN on tente de créer une inscription
        THEN l'inscription échoue et retourne None
        """
        # Act
        inscription = inscription_service.creer_inscription(
            boit=False,
            created_by=99999,  # ID inexistant
            mode_paiement="espèce",
            id_event=evenement_test.id_event,
            nom_event=evenement_test.titre,
            id_bus_aller=bus_test["aller"].id_bus,
            id_bus_retour=bus_test["retour"].id_bus
        )

        # Assert
        assert inscription is None

    def test_creer_inscription_evenement_complet(self, inscription_service, utilisateur_test):
        """
        Test : Tentative d'inscription à un événement complet
        GIVEN un événement avec capacité max = 2
        AND déjà 2 inscrits
        WHEN un 3ème utilisateur tente de s'inscrire
        THEN l'inscription échoue car l'événement est complet
        """
        # Arrange - Créer un événement avec capacité limitée
        evenement_petit = Evenement(
            titre="Petit Event",
            description_evenement="Capacité limitée",
            lieu="Rennes",
            date_evenement=date.today() + timedelta(days=15),
            capacite_max=2,  # Seulement 2 places
            created_by=utilisateur_test.id_utilisateur,
            tarif=10.0
        )
        EvenementDAO().creer(evenement_petit)

        # Créer des bus pour cet événement
        bus_aller = Bus(capacite_max=50, id_event=evenement_petit.id_event, sens="aller", heure_depart="08:00")
        bus_retour = Bus(capacite_max=50, id_event=evenement_petit.id_event, sens="retour", heure_depart="23:00")
        BusDAO().creer(bus_aller)
        BusDAO().creer(bus_retour)

        # Créer 2 autres utilisateurs et les inscrire
        for i in range(2):
            user = Utilisateur(
                pseudo=f"user{i}",
                nom=f"Nom{i}",
                prenom=f"Prenom{i}",
                email=f"user{i}@test.com",
                mot_de_passe="Pass123!"
            )
            UtilisateurDAO().creer(user)
            inscription_service.creer_inscription(
                boit=False,
                created_by=user.id_utilisateur,
                mode_paiement="en ligne",
                id_event=evenement_petit.id_event,
                nom_event=evenement_petit.titre,
                id_bus_aller=bus_aller.id_bus,
                id_bus_retour=bus_retour.id_bus
            )

        # Act - Tenter d'inscrire un 3ème utilisateur
        inscription = inscription_service.creer_inscription(
            boit=True,
            created_by=utilisateur_test.id_utilisateur,
            mode_paiement="espèce",
            id_event=evenement_petit.id_event,
            nom_event=evenement_petit.titre,
            id_bus_aller=bus_aller.id_bus,
            id_bus_retour=bus_retour.id_bus
        )

        # Assert
        assert inscription is None
        assert inscription_service.obtenir_nombre_inscrits(evenement_petit.id_event) == 2

    def test_creer_inscription_doublon(self, inscription_service, utilisateur_test, evenement_test, bus_test):
        """
        Test : Tentative de double inscription au même événement
        GIVEN un utilisateur déjà inscrit à un événement
        WHEN il tente de s'inscrire à nouveau
        THEN la 2ème inscription échoue
        """
        # Arrange - Première inscription
        premiere_inscription = inscription_service.creer_inscription(
            boit=True,
            created_by=utilisateur_test.id_utilisateur,
            mode_paiement="en ligne",
            id_event=evenement_test.id_event,
            nom_event=evenement_test.titre,
            id_bus_aller=bus_test["aller"].id_bus,
            id_bus_retour=bus_test["retour"].id_bus
        )
        assert premiere_inscription is not None

        # Act - Tentative de 2ème inscription
        deuxieme_inscription = inscription_service.creer_inscription(
            boit=False,
            created_by=utilisateur_test.id_utilisateur,
            mode_paiement="espèce",
            id_event=evenement_test.id_event,
            nom_event=evenement_test.titre,
            id_bus_aller=bus_test["aller"].id_bus,
            id_bus_retour=bus_test["retour"].id_bus
        )

        # Assert
        assert deuxieme_inscription is None
        assert inscription_service.est_deja_inscrit(
            utilisateur_test.id_utilisateur, 
            evenement_test.id_event
        ) is True

    def test_calculer_statistiques_evenement(self, inscription_service, evenement_test, bus_test):
        """
        Test : Calcul des statistiques d'un événement
        GIVEN un événement avec plusieurs inscriptions variées
        WHEN on calcule les statistiques
        THEN on obtient le bon décompte (buveurs, modes de paiement, etc.)
        """
        # Arrange - Créer 5 utilisateurs avec des profils variés
        inscriptions_config = [
            {"boit": True, "paiement": "en ligne"},
            {"boit": True, "paiement": "espèce"},
            {"boit": False, "paiement": "en ligne"},
            {"boit": False, "paiement": "espèce"},
            {"boit": True, "paiement": "en ligne"}
        ]

        for i, config in enumerate(inscriptions_config):
            user = Utilisateur(
                pseudo=f"user{i}",
                nom=f"Nom{i}",
                prenom=f"Prenom{i}",
                email=f"user{i}@test.com",
                mot_de_passe="Pass123!"
            )
            UtilisateurDAO().creer(user)
            inscription_service.creer_inscription(
                boit=config["boit"],
                created_by=user.id_utilisateur,
                mode_paiement=config["paiement"],
                id_event=evenement_test.id_event,
                nom_event=evenement_test.titre,
                id_bus_aller=bus_test["aller"].id_bus,
                id_bus_retour=bus_test["retour"].id_bus
            )

        # Act
        stats = inscription_service.calculer_statistiques_evenement(evenement_test.id_event)

        # Assert
        assert stats["total_inscrits"] == 5
        assert stats["nombre_buveurs"] == 3
        assert stats["nombre_non_buveurs"] == 2
        assert stats["paiements_en_ligne"] == 3
        assert stats["paiements_espece"] == 2
        assert stats["paiements_non_definis"] == 0

    def test_verifier_disponibilite_evenement(self, inscription_service, utilisateur_test, evenement_test, bus_test):
        """
        Test : Vérification de la disponibilité d'un événement
        GIVEN un événement avec capacité 50 et 3 inscrits
        WHEN on vérifie la disponibilité
        THEN on obtient les bonnes informations (places restantes, taux de remplissage)
        """
        # Arrange - Créer 3 inscriptions
        for i in range(3):
            user = Utilisateur(
                pseudo=f"user{i}",
                nom=f"Nom{i}",
                prenom=f"Prenom{i}",
                email=f"user{i}@test.com",
                mot_de_passe="Pass123!"
            )
            UtilisateurDAO().creer(user)
            inscription_service.creer_inscription(
                boit=False,
                created_by=user.id_utilisateur,
                mode_paiement="en ligne",
                id_event=evenement_test.id_event,
                nom_event=evenement_test.titre,
                id_bus_aller=bus_test["aller"].id_bus,
                id_bus_retour=bus_test["retour"].id_bus
            )

        # Act
        disponibilite = inscription_service.verifier_disponibilite_evenement(
            evenement_test.id_event
        )

        # Assert
        assert disponibilite["disponible"] is True
        assert disponibilite["places_restantes"] == 47  # 50 - 3
        assert disponibilite["capacite_max"] == 50
        assert disponibilite["nombre_inscrits"] == 3
        assert disponibilite["taux_remplissage"] == 6.0  # (3/50)*100

    def test_generer_code_reservation_unique(self, inscription_service):
        """
        Test : Génération de codes de réservation uniques
        GIVEN le service d'inscription
        WHEN on génère plusieurs codes
        THEN tous les codes sont différents et ont 8 chiffres
        """
        # Act - Générer 10 codes
        codes = [inscription_service.generer_code_reservation() for _ in range(10)]

        # Assert
        assert len(codes) == len(set(codes))  # Tous uniques
        assert all(len(str(code)) == 8 for code in codes)  # Tous 8 chiffres
        assert all(isinstance(code, int) for code in codes)  # Tous des entiers

    def test_obtenir_inscriptions_utilisateur(self, inscription_service, utilisateur_test):
        """
        Test : Récupération de toutes les inscriptions d'un utilisateur
        GIVEN un utilisateur inscrit à 3 événements différents
        WHEN on récupère ses inscriptions
        THEN on obtient bien ses 3 inscriptions
        """
        # Arrange - Créer 3 événements et inscrire l'utilisateur
        evenements = []
        bus_list = []
        
        for i in range(3):
            evt = Evenement(
                titre=f"Event {i}",
                description_evenement=f"Description {i}",
                lieu="Rennes",
                date_evenement=date.today() + timedelta(days=10 + i),
                capacite_max=30,
                created_by=utilisateur_test.id_utilisateur,
                tarif=10.0
            )
            EvenementDAO().creer(evt)
            evenements.append(evt)
            
            # Créer des bus pour chaque événement
            bus_aller = Bus(capacite_max=50, id_event=evt.id_event, sens="aller", heure_depart="08:00")
            bus_retour = Bus(capacite_max=50, id_event=evt.id_event, sens="retour", heure_depart="23:00")
            BusDAO().creer(bus_aller)
            BusDAO().creer(bus_retour)
            bus_list.append({"aller": bus_aller, "retour": bus_retour})

        for i, evt in enumerate(evenements):
            inscription_service.creer_inscription(
                boit=True,
                created_by=utilisateur_test.id_utilisateur,
                mode_paiement="en ligne",
                id_event=evt.id_event,
                nom_event=evt.titre,
                id_bus_aller=bus_list[i]["aller"].id_bus,
                id_bus_retour=bus_list[i]["retour"].id_bus
            )

        # Act
        inscriptions_user = inscription_service.obtenir_inscriptions_utilisateur(
            utilisateur_test.id_utilisateur
        )

        # Assert
        assert len(inscriptions_user) == 3
        assert all(insc.created_by == utilisateur_test.id_utilisateur for insc in inscriptions_user)
        event_ids = [insc.id_event for insc in inscriptions_user]
        assert all(evt.id_event in event_ids for evt in evenements)