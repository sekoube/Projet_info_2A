import unittest
from unittest.mock import Mock
from datetime import date
from decimal import Decimal
from src.services.evenement_service import EvenementService


class TestCreerEvenement(unittest.TestCase):
    """Tests ciblés sur la création d'événement"""

    def setUp(self):
        """Configuration avant chaque test"""
        # Créer des mocks pour les DAOs
        self.evenement_dao = Mock()
        self.inscription_dao = Mock()
        self.utilisateur_dao = Mock()
        self.bus_dao = Mock()

        # Instancier le service
        self.service = EvenementService(
            evenement_dao=self.evenement_dao,
            inscription_dao=self.inscription_dao,
            utilisateur_dao=self.utilisateur_dao,
            bus_dao=self.bus_dao
        )

    # ==================== TEST 1 : CAS NOMINAL ====================
    def test_creer_evenement_cas_nominal(self):
        """
        TEST 1 : Création réussie d'un événement avec toutes les données valides

        Vérifie que :
        - L'événement est créé avec les bonnes valeurs
        - Le DAO est appelé une fois
        - L'objet retourné n'est pas None
        - L'objet contient un ID après création
        """
        # ARRANGE : Préparer les données
        self.evenement_dao.creer.return_value = True
        
        # Simuler l'ajout d'un ID par le DAO (comme dans la vraie vie)
        def ajouter_id(evenement):
            evenement.id_event = 42
            return True
        self.evenement_dao.creer.side_effect = ajouter_id

        # ACT : Créer l'événement
        evenement = self.service.creer_evenement(
            titre="Soirée Bowling",
            lieu="Bordeaux",
            date_evenement=date(2025, 6, 15),
            capacite_max=50,
            created_by=1,
            description_evenement="Soirée détente entre collègues",
            tarif=15.00
        )

        # ASSERT : Vérifier les résultats
        self.assertIsNotNone(evenement, "L'événement ne devrait pas être None")
        self.assertEqual(evenement.titre, "Soirée Bowling")
        self.assertEqual(evenement.lieu, "Bordeaux")
        self.assertEqual(evenement.capacite_max, 50)
        self.assertEqual(evenement.tarif, 15.00)
        self.assertEqual(evenement.id_event, 42, "L'ID devrait être assigné")
        self.evenement_dao.creer.assert_called_once()
        
        print("TEST 1 PASSÉ : Création réussie")

    # ==================== TEST 2 : VALIDATION MÉTIER ====================
    def test_creer_evenement_validation_titre_vide(self):
        """
        TEST 2 : Échec si le titre est vide (validation métier)
        
        Vérifie que :
        - La méthode retourne None en cas de titre invalide
        - Le DAO n'est PAS appelé (validation échoue avant)
        - Une ValueError est capturée
        """
        # ACT : Tenter de créer un événement avec titre vide
        evenement = self.service.creer_evenement(
            titre="",  # Titre vide
            lieu="Lyon",
            date_evenement=date(2025, 7, 20),
            capacite_max=100,
            created_by=1
        )

        # ASSERT : Vérifier l'échec
        self.assertIsNone(evenement, "Devrait retourner None avec un titre vide")
        self.evenement_dao.creer.assert_not_called()
        
        print("TEST 2 PASSÉ : Validation du titre vide fonctionne")

    # ==================== TEST 3 : ÉCHEC BASE DE DONNÉES ====================
    def test_creer_evenement_echec_dao(self):
        """
        TEST 3 : Échec lors de la persistance en base de données
        
        Vérifie que :
        - Si le DAO échoue, la méthode retourne None
        - L'objet est bien créé côté métier (validations OK)
        - Mais la persistance échoue
        """
        # ARRANGE : Simuler un échec du DAO
        self.evenement_dao.creer.return_value = False

        # ACT : Créer l'événement
        evenement = self.service.creer_evenement(
            titre="Festival Musique",
            lieu="Marseille",
            date_evenement=date(2025, 8, 10),
            capacite_max=500,
            created_by=2,
            tarif=35.00
        )

        # ASSERT : Vérifier l'échec
        self.assertIsNone(evenement, "Devrait retourner None si le DAO échoue")
        self.evenement_dao.creer.assert_called_once()
        
        print("TEST 3 PASSÉ : Gestion de l'échec DAO fonctionne")

