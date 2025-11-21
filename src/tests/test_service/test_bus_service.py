import unittest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime

from service.bus_service import BusService
from business_object.bus import Bus
from dao.bus_dao import BusDAO
from dao.evenement_dao import EvenementDAO


class TestBusService(unittest.TestCase):
    """Tests unitaires pour le service de gestion des bus"""
    
    def setUp(self):
        """Préparation avant chaque test"""
        self.bus_service = BusService()
        # Mock des DAOs pour isoler les tests
        self.bus_service.bus_dao = Mock(spec=BusDAO)
        self.bus_service.evenement_dao = Mock(spec=EvenementDAO)
    
    def test_creer_bus_valide(self):
        """
        Test 1: Création d'un bus avec des données valides
        Vérifie que le bus est correctement créé et que la DAO est appelée
        """
        # Arrange
        bus_mock = Bus(
            id_event=1,
            sens="Aller",
            heure_depart="08:30",
            capacite_max=50,
            description="Gare -> Campus",
            id_bus=1
        )
        self.bus_service.bus_dao.creer.return_value = bus_mock
        
        # Act
        resultat = self.bus_service.creer_bus(
            id_event=1,
            sens="Aller",
            description="Gare -> Campus",
            heure_depart="08:30",
            capacite_max=50
        )
        
        # Assert
        self.assertIsNotNone(resultat)
        self.assertEqual(resultat.id_bus, 1)
        self.bus_service.bus_dao.creer.assert_called_once()
    
    def test_creer_bus_capacite_negative(self):
        """
        Test 2: Création d'un bus avec une capacité négative
        Vérifie que la validation échoue et retourne None
        """
        # Act
        resultat = self.bus_service.creer_bus(
            id_event=1,
            sens="Retour",
            description="Campus -> Gare",
            heure_depart="18:00",
            capacite_max=-10
        )
        
        # Assert
        self.assertIsNone(resultat)
        self.bus_service.bus_dao.creer.assert_not_called()
    
    def test_creer_bus_champs_manquants(self):
        """
        Test 3: Création d'un bus avec des champs essentiels manquants
        Vérifie que la validation échoue quand id_event, sens ou capacite_max sont absents
        """
        # Act - Test avec id_event manquant
        resultat1 = self.bus_service.creer_bus(
            id_event=None,
            sens="Aller",
            description="Test",
            heure_depart="10:00",
            capacite_max=50
        )
        
        # Act - Test avec sens manquant
        resultat2 = self.bus_service.creer_bus(
            id_event=1,
            sens=None,
            description="Test",
            heure_depart="10:00",
            capacite_max=50
        )
        
        # Assert
        self.assertIsNone(resultat1)
        self.assertIsNone(resultat2)
        self.bus_service.bus_dao.creer.assert_not_called()
    
    def test_supprimer_bus_existant(self):
        """
        Test 4: Suppression d'un bus existant
        Vérifie que la suppression fonctionne correctement avec get_by
        """
        # Arrange
        bus_mock = Bus(
            id_event=1,
            sens="Aller",
            heure_depart="08:30",
            capacite_max=50,
            description="Test",
            id_bus=1
        )
    
        # Mock get_by qui est appelé par supprimer_bus dans le service
        self.bus_service.bus_dao.get_by = Mock(return_value=[bus_mock])
        self.bus_service.bus_dao.supprimer.return_value = True

        # Act
        resultat = self.bus_service.supprimer_bus(1)

        # Assert
        self.assertTrue(resultat)
        self.bus_service.bus_dao.get_by.assert_called_once_with("id_bus", 1)
        self.bus_service.bus_dao.supprimer.assert_called_once_with(1)
        
    def test_supprimer_bus_inexistant(self):
        """
        Test 5: Tentative de suppression d'un bus inexistant
        Vérifie que la méthode retourne False et n'appelle pas supprimer
        """
        # Arrange
        self.bus_service.bus_dao.get_by.return_value = []
        
        # Act
        resultat = self.bus_service.supprimer_bus(999)
        
        # Assert
        self.assertFalse(resultat)
        self.bus_service.bus_dao.get_by.assert_called_once_with("id_bus", 999)
        self.bus_service.bus_dao.supprimer.assert_not_called()
    
    def test_get_bus_by_field_valide(self):
        """
        Test 6 (Bonus): Récupération d'un bus par un champ spécifique
        Vérifie que get_bus_by fonctionne correctement
        """
        # Arrange
        bus_mock = Bus(
            id_event=1,
            sens="Aller",
            heure_depart="08:30",
            capacite_max=50,
            description="Test",
            id_bus=1
        )
        self.bus_service.bus_dao.get_by.return_value = bus_mock
        
        # Act
        resultat = self.bus_service.get_bus_by("id_event", 1)
        
        # Assert
        self.assertIsNotNone(resultat)
        self.assertEqual(resultat.id_event, 1)
        self.bus_service.bus_dao.get_by.assert_called_once_with("id_event", 1)
    
    def test_get_tous_les_bus(self):
        """
        Test 7 (Bonus): Récupération de tous les bus
        Vérifie que la méthode retourne bien une liste de bus
        """
        # Arrange
        bus_list = [
            Bus(1, "Aller", "08:30", 50, "Bus 1", 1),
            Bus(1, "Retour", "18:00", 50, "Bus 2", 2)
        ]
        self.bus_service.bus_dao.lister_tous.return_value = bus_list
        
        # Act
        resultat = self.bus_service.get_tous_les_bus()
        
        # Assert
        self.assertEqual(len(resultat), 2)
        self.bus_service.bus_dao.lister_tous.assert_called_once()


if __name__ == '__main__':
    unittest.main()