import unittest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
from dao.evenement_dao import EvenementDAO
from business_object.evenement import Evenement


class TestEvenementDAO(unittest.TestCase):
    """Tests unitaires pour le DAO d'événement"""

    def setUp(self):
        """Initialisation avant chaque test"""
        self.dao = EvenementDAO()
        self.mock_connection = MagicMock()
        self.mock_cursor = MagicMock()

    def test_creer_evenement_succes(self):
        """Test 1: Création réussie d'un événement"""
        # Arrange
        evenement = Evenement(
            nom="Concert Rock",
            date_event=datetime(2024, 6, 15, 20, 0),
            lieu="Zénith",
            description="Super concert",
            capacite_max=500,
            prix=45.0,
            statut="ouvert",
            created_by=1
        )
        
        self.mock_cursor.fetchone.return_value = {"id_event": 10}
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.evenement_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.__enter__.return_value = self.mock_connection
            resultat = self.dao.creer(evenement)
        
        # Assert
        self.assertIsNotNone(resultat)
        self.assertEqual(resultat.id_event, 10)
        self.mock_cursor.execute.assert_called_once()

    def test_creer_evenement_echec_exception(self):
        """Test 2: Échec de création avec exception"""
        # Arrange
        evenement = Evenement(
            nom="Festival",
            date_event=datetime(2024, 7, 20),
            lieu="Parc",
            description="Festival musique",
            capacite_max=1000,
            prix=30.0,
            statut="ouvert",
            created_by=1
        )
        
        self.mock_cursor.execute.side_effect = Exception("Erreur DB")
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.evenement_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.__enter__.return_value = self.mock_connection
            resultat = self.dao.creer(evenement)
        
        # Assert
        self.assertIsNone(resultat)

    def test_get_by_id_event(self):
        """Test 3: Récupération par ID événement"""
        # Arrange
        mock_rows = [
            {
                "id_event": 5,
                "nom": "Soirée Karaoké",
                "date_event": datetime(2024, 8, 10, 19, 0),
                "lieu": "Bar Central",
                "description": "Karaoké fun",
                "capacite_max": 50,
                "prix": 15.0,
                "statut": "ouvert",
                "created_by": 2,
                "created_at": datetime.now()
            }
        ]
        
        self.mock_cursor.fetchall.return_value = mock_rows
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.evenement_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.cursor.return_value.__enter__.return_value = self.mock_cursor
            resultat = self.dao.get_by("id_event", 5)
        
        # Assert
        self.assertEqual(len(resultat), 1)
        self.assertIsInstance(resultat[0], Evenement)
        self.assertEqual(resultat[0].id_event, 5)
        self.assertEqual(resultat[0].nom, "Soirée Karaoké")

    def test_get_by_nom_evenement(self):
        """Test 4: Récupération par nom d'événement"""
        # Arrange
        mock_rows = [
            {
                "id_event": 1,
                "nom": "Concert Rock",
                "date_event": datetime(2024, 6, 15),
                "lieu": "Zénith",
                "description": "Rock show",
                "capacite_max": 500,
                "prix": 40.0,
                "statut": "ouvert",
                "created_by": 1,
                "created_at": datetime.now()
            }
        ]
        
        self.mock_cursor.fetchall.return_value = mock_rows
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.evenement_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.cursor.return_value.__enter__.return_value = self.mock_cursor
            resultat = self.dao.get_by("nom", "Concert Rock")
        
        # Assert
        self.assertEqual(len(resultat), 1)
        self.assertEqual(resultat[0].nom, "Concert Rock")

    def test_get_by_colonne_non_autorisee(self):
        """Test 5: Échec avec colonne non autorisée"""
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.dao.get_by("colonne_invalide", "valeur")
        
        self.assertIn("non autorisée", str(context.exception))

    def test_get_by_aucun_resultat(self):
        """Test 6: Recherche sans résultat"""
        # Arrange
        self.mock_cursor.fetchall.return_value = []
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.evenement_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.cursor.return_value.__enter__.return_value = self.mock_cursor
            resultat = self.dao.get_by("id_event", 999)
        
        # Assert
        self.assertEqual(len(resultat), 0)

    def test_lister_tous_avec_resultats(self):
        """Test 7: Lister tous les événements"""
        # Arrange
        mock_rows = [
            {
                "id_event": 1,
                "nom": "Event 1",
                "date_event": datetime(2024, 6, 15),
                "lieu": "Lieu 1",
                "description": "Desc 1",
                "capacite_max": 100,
                "prix": 20.0,
                "statut": "ouvert",
                "created_by": 1,
                "created_at": datetime.now()
            },
            {
                "id_event": 2,
                "nom": "Event 2",
                "date_event": datetime(2024, 7, 20),
                "lieu": "Lieu 2",
                "description": "Desc 2",
                "capacite_max": 200,
                "prix": 30.0,
                "statut": "complet",
                "created_by": 2,
                "created_at": datetime.now()
            }
        ]
        
        self.mock_cursor.fetchall.return_value = mock_rows
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.evenement_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.__enter__.return_value = self.mock_connection
            resultat = self.dao.lister_tous()
        
        # Assert
        self.assertEqual(len(resultat), 2)
        self.assertTrue(all(isinstance(e, Evenement) for e in resultat))

    def test_lister_tous_vide(self):
        """Test 8: Lister sans événement"""
        # Arrange
        self.mock_cursor.fetchall.return_value = []
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.evenement_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.__enter__.return_value = self.mock_connection
            resultat = self.dao.lister_tous()
        
        # Assert
        self.assertEqual(len(resultat), 0)

    def test_lister_tous_erreur_exception(self):
        """Test 9: Échec du listage avec exception"""
        # Arrange
        self.mock_cursor.execute.side_effect = Exception("Erreur DB")
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.evenement_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.__enter__.return_value = self.mock_connection
            resultat = self.dao.lister_tous()
        
        # Assert
        self.assertEqual(len(resultat), 0)

    def test_modifier_evenement_succes(self):
        """Test 10: Modification réussie d'un événement"""
        # Arrange
        evenement = Evenement(
            id_event=5,
            nom="Concert Modifié",
            date_event=datetime(2024, 9, 1),
            lieu="Nouveau Lieu",
            description="Nouvelle desc",
            capacite_max=300,
            prix=50.0,
            statut="ouvert",
            created_by=1
        )
        
        self.mock_cursor.rowcount = 1
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.evenement_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.__enter__.return_value = self.mock_connection
            resultat = self.dao.modifier(evenement)
        
        # Assert
        self.assertTrue(resultat)
        self.mock_cursor.execute.assert_called_once()

    def test_modifier_evenement_inexistant(self):
        """Test 11: Modification d'un événement inexistant"""
        # Arrange
        evenement = Evenement(
            id_event=999,
            nom="Event Inexistant",
            date_event=datetime(2024, 9, 1),
            lieu="Lieu",
            description="Desc",
            capacite_max=100,
            prix=20.0,
            statut="ouvert",
            created_by=1
        )
        
        self.mock_cursor.rowcount = 0
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.evenement_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.__enter__.return_value = self.mock_connection
            resultat = self.dao.modifier(evenement)
        
        # Assert
        self.assertFalse(resultat)

    def test_modifier_erreur_exception(self):
        """Test 12: Erreur lors de la modification"""
        # Arrange
        evenement = Evenement(
            id_event=5,
            nom="Event",
            date_event=datetime(2024, 9, 1),
            lieu="Lieu",
            description="Desc",
            capacite_max=100,
            prix=20.0,
            statut="ouvert",
            created_by=1
        )
        
        self.mock_cursor.execute.side_effect = Exception("Erreur DB")
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.evenement_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.__enter__.return_value = self.mock_connection
            resultat = self.dao.modifier(evenement)
        
        # Assert
        self.assertFalse(resultat)

    def test_supprimer_evenement_succes(self):
        """Test 13: Suppression réussie"""
        # Arrange
        self.mock_cursor.rowcount = 1
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.evenement_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.__enter__.return_value = self.mock_connection
            resultat = self.dao.supprimer(5)
        
        # Assert
        self.assertTrue(resultat)
        self.mock_cursor.execute.assert_called_once()

    def test_supprimer_evenement_inexistant(self):
        """Test 14: Suppression d'un événement inexistant"""
        # Arrange
        self.mock_cursor.rowcount = 0
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.evenement_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.__enter__.return_value = self.mock_connection
            resultat = self.dao.supprimer(999)
        
        # Assert
        self.assertFalse(resultat)

    def test_supprimer_erreur_exception(self):
        """Test 15: Erreur lors de la suppression"""
        # Arrange
        self.mock_cursor.execute.side_effect = Exception("Erreur DB")
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.evenement_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.__enter__.return_value = self.mock_connection
            resultat = self.dao.supprimer(5)
        
        # Assert
        self.assertFalse(resultat)

    def test_modifier_statut_succes(self):
        """Test 16: Modification de statut réussie"""
        # Arrange
        self.mock_cursor.rowcount = 1
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.evenement_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.__enter__.return_value = self.mock_connection
            resultat = self.dao.modifier_statut(5, "complet")
        
        # Assert
        self.assertTrue(resultat)
        # Vérifier que le statut "complet" est bien passé
        call_args = self.mock_cursor.execute.call_args
        self.assertIn("complet", str(call_args))

    def test_modifier_statut_evenement_inexistant(self):
        """Test 17: Modification de statut sur événement inexistant"""
        # Arrange
        self.mock_cursor.rowcount = 0
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.evenement_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.__enter__.return_value = self.mock_connection
            resultat = self.dao.modifier_statut(999, "complet")
        
        # Assert
        self.assertFalse(resultat)

    def test_modifier_statut_erreur_exception(self):
        """Test 18: Erreur lors de la modification de statut"""
        # Arrange
        self.mock_cursor.execute.side_effect = Exception("Erreur DB")
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.evenement_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.__enter__.return_value = self.mock_connection
            resultat = self.dao.modifier_statut(5, "complet")
        
        # Assert
        self.assertFalse(resultat)


if __name__ == "__main__":
    unittest.main()