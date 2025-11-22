import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from business_object.bus import Bus
from dao.bus_dao import BusDAO


class TestBusDAO(unittest.TestCase):
    """Tests unitaires pour la classe BusDAO."""

    def setUp(self):
        """Initialisation avant chaque test."""
        self.bus_dao = BusDAO()
        
        # Bus de test
        self.bus_test = Bus(
            id_event=1,
            sens="Aller",
            heure_depart="14:30",
            capacite_max=50,
            description="Paris - Lyon"
        )

    @patch('dao.bus_dao.DBConnection')
    def test_creer_bus_success(self, mock_db):
        """Test 1: Création réussie d'un bus."""
        # Configuration du mock
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {"id_bus": 1}
        mock_db.return_value.connection.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        
        # Exécution
        resultat = self.bus_dao.creer(self.bus_test)
        
        # Vérifications
        self.assertIsNotNone(resultat)
        self.assertEqual(resultat.id_bus, 1)
        mock_cursor.execute.assert_called_once()

    @patch('dao.bus_dao.DBConnection')
    def test_creer_bus_avec_tous_les_champs(self, mock_db):
        """Test 2: Création d'un bus avec tous les champs renseignés."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = {"id_bus": 2}
        mock_db.return_value.connection.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        
        bus_complet = Bus(
            id_event=5,
            sens="Retour",
            heure_depart="18:45",
            capacite_max=45,
            description="Lyon - Paris - Arrêt Gare Part-Dieu"
        )
        
        resultat = self.bus_dao.creer(bus_complet)
        
        self.assertEqual(resultat.id_bus, 2)
        self.assertEqual(resultat.sens, "RETOUR")
        self.assertEqual(resultat.capacite_max, 45)

    @patch('dao.bus_dao.DBConnection')
    def test_get_by_id_bus_success(self, mock_db):
        """Test 3: Récupération d'un bus par son ID."""
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{
            "id_bus": 1,
            "id_event": 1,
            "sens": "ALLER",
            "description": "Paris - Lyon",
            "heure_depart": "14:30",
            "capacite_max": 50
        }]
        mock_db.return_value.connection.cursor.return_value.__enter__.return_value = mock_cursor
        
        resultat = self.bus_dao.get_by("id_bus", 1)
        
        self.assertEqual(len(resultat), 1)
        self.assertEqual(resultat[0].id_bus, 1)
        self.assertEqual(resultat[0].capacite_max, 50)

    @patch('dao.bus_dao.DBConnection')
    def test_get_by_id_event(self, mock_db):
        """Test 4: Récupération de tous les bus d'un événement."""
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {
                "id_bus": 1,
                "id_event": 5,
                "sens": "ALLER",
                "description": "Trajet 1",
                "heure_depart": "08:00",
                "capacite_max": 50
            },
            {
                "id_bus": 2,
                "id_event": 5,
                "sens": "RETOUR",
                "description": "Trajet 2",
                "heure_depart": "18:00",
                "capacite_max": 50
            }
        ]
        mock_db.return_value.connection.cursor.return_value.__enter__.return_value = mock_cursor
        
        resultat = self.bus_dao.get_by("id_event", 5)
        
        self.assertEqual(len(resultat), 2)
        self.assertEqual(resultat[0].id_event, 5)
        self.assertEqual(resultat[1].id_event, 5)

    @patch('dao.bus_dao.DBConnection')
    def test_get_by_sens(self, mock_db):
        """Test 5: Récupération des bus par sens (Aller/Retour)."""
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {
                "id_bus": 1,
                "id_event": 1,
                "sens": "ALLER",
                "description": "Trajet aller",
                "heure_depart": "08:00",
                "capacite_max": 50
            }
        ]
        mock_db.return_value.connection.cursor.return_value.__enter__.return_value = mock_cursor
        
        resultat = self.bus_dao.get_by("sens", "ALLER")
        
        self.assertEqual(len(resultat), 1)
        self.assertEqual(resultat[0].sens, "ALLER")

    def test_get_by_colonne_non_autorisee(self):
        """Test 6: Tentative de récupération avec une colonne non autorisée."""
        with self.assertRaises(ValueError) as context:
            self.bus_dao.get_by("colonne_malveillante", "valeur")
        
        self.assertIn("non autorisée", str(context.exception))

    @patch('dao.bus_dao.DBConnection')
    def test_get_by_aucun_resultat(self, mock_db):
        """Test 7: Récupération sans résultat."""
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_db.return_value.connection.cursor.return_value.__enter__.return_value = mock_cursor
        
        resultat = self.bus_dao.get_by("id_bus", 9999)
        
        self.assertEqual(len(resultat), 0)

    @patch('dao.bus_dao.DBConnection')
    def test_lister_tous_success(self, mock_db):
        """Test 8: Récupération de tous les bus."""
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {
                "id_bus": 1,
                "id_event": 1,
                "sens": "ALLER",
                "description": "Bus 1",
                "heure_depart": "08:00",
                "capacite_max": 50
            },
            {
                "id_bus": 2,
                "id_event": 2,
                "sens": "RETOUR",
                "description": "Bus 2",
                "heure_depart": "18:00",
                "capacite_max": 45
            }
        ]
        mock_db.return_value.connection.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        
        resultat = self.bus_dao.lister_tous()
        
        self.assertEqual(len(resultat), 2)
        self.assertIsInstance(resultat[0], Bus)

    @patch('dao.bus_dao.DBConnection')
    def test_supprimer_bus_success(self, mock_db):
        """Test 9: Suppression réussie d'un bus."""
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_db.return_value.connection.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        
        resultat = self.bus_dao.supprimer(1)
        
        self.assertTrue(resultat)
        mock_cursor.execute.assert_called_once()

    @patch('dao.bus_dao.DBConnection')
    def test_supprimer_bus_inexistant(self, mock_db):
        """Test 10: Tentative de suppression d'un bus inexistant."""
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0
        mock_db.return_value.connection.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        
        resultat = self.bus_dao.supprimer(9999)
        
        self.assertFalse(resultat)


if __name__ == '__main__':
    unittest.main()