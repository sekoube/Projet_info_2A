import unittest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
from dao.inscription_dao import InscriptionDAO
from business_object.inscription import Inscription


class TestInscriptionDAO(unittest.TestCase):
    """Tests unitaires pour le DAO d'inscription"""

    def setUp(self):
        """Initialisation avant chaque test"""
        self.dao = InscriptionDAO()
        self.mock_connection = MagicMock()
        self.mock_cursor = MagicMock()

    def test_creer_inscription_succes(self):
        """Test 1: Création réussie d'une inscription"""
        # Arrange
        inscription = Inscription(
            code_reservation=12345678,
            boit=True,
            mode_paiement="en ligne",
            id_event=1,
            nom_event="Soirée Test",
            id_bus_aller=1,
            id_bus_retour=2,
            created_by=1
        )
        
        self.mock_cursor.fetchone.return_value = {"code_reservation": 12345678}
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.inscription_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.__enter__.return_value = self.mock_connection
            resultat = self.dao.creer(inscription)
        
        # Assert
        self.assertIsNotNone(resultat)
        self.assertEqual(resultat.code_reservation, 12345678)
        self.mock_cursor.execute.assert_called_once()

    def test_creer_inscription_echec_exception(self):
        """Test 2: Échec de création avec exception"""
        # Arrange
        inscription = Inscription(
            code_reservation=12345678,
            boit=False,
            mode_paiement="espece",
            id_event=1,
            nom_event="Event Test",
            id_bus_aller=1,
            id_bus_retour=2,
            created_by=1
        )
        
        self.mock_cursor.execute.side_effect = Exception("Erreur DB")
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.inscription_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.__enter__.return_value = self.mock_connection
            resultat = self.dao.creer(inscription)
        
        # Assert
        self.assertIsNone(resultat)

    def test_get_by_code_reservation(self):
        """Test 3: Récupération par code de réservation"""
        # Arrange
        mock_rows = [
            {
                "code_reservation": 12345678,
                "boit": True,
                "created_by": 1,
                "mode_paiement": "en ligne",
                "id_event": 1,
                "id_bus_aller": 1,
                "id_bus_retour": 2,
                "created_at": datetime.now()
            }
        ]
        
        self.mock_cursor.fetchall.return_value = mock_rows
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.inscription_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.cursor.return_value.__enter__.return_value = self.mock_cursor
            resultat = self.dao.get_by("code_reservation", 12345678)
        
        # Assert
        self.assertEqual(len(resultat), 1)
        self.assertIsInstance(resultat[0], Inscription)
        self.assertEqual(resultat[0].code_reservation, 12345678)

    def test_get_by_created_by(self):
        """Test 4: Récupération par utilisateur créateur"""
        # Arrange
        mock_rows = [
            {
                "code_reservation": 11111111,
                "boit": True,
                "created_by": 5,
                "mode_paiement": "en ligne",
                "id_event": 1,
                "id_bus_aller": 1,
                "id_bus_retour": 2,
                "created_at": datetime.now()
            },
            {
                "code_reservation": 22222222,
                "boit": False,
                "created_by": 5,
                "mode_paiement": "espece",
                "id_event": 2,
                "id_bus_aller": 3,
                "id_bus_retour": 4,
                "created_at": datetime.now()
            }
        ]
        
        self.mock_cursor.fetchall.return_value = mock_rows
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.inscription_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.cursor.return_value.__enter__.return_value = self.mock_cursor
            resultat = self.dao.get_by("created_by", 5)
        
        # Assert
        self.assertEqual(len(resultat), 2)
        self.assertTrue(all(isinstance(i, Inscription) for i in resultat))
        self.assertTrue(all(i.created_by == 5 for i in resultat))

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
        with patch('dao.inscription_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.cursor.return_value.__enter__.return_value = self.mock_cursor
            resultat = self.dao.get_by("code_reservation", 99999999)
        
        # Assert
        self.assertEqual(len(resultat), 0)

    def test_lister_toutes_avec_resultats(self):
        """Test 7: Lister toutes les inscriptions"""
        # Arrange
        mock_rows = [
            {
                "code_reservation": 11111111,
                "boit": True,
                "created_by": 1,
                "mode_paiement": "en ligne",
                "id_event": 1,
                "id_bus_aller": 1,
                "id_bus_retour": 2,
                "created_at": datetime.now()
            },
            {
                "code_reservation": 22222222,
                "boit": False,
                "created_by": 2,
                "mode_paiement": "espece",
                "id_event": 2,
                "id_bus_aller": 3,
                "id_bus_retour": 4,
                "created_at": datetime.now()
            }
        ]
        
        self.mock_cursor.fetchall.return_value = mock_rows
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.inscription_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.__enter__.return_value = self.mock_connection
            resultat = self.dao.lister_toutes()
        
        # Assert
        self.assertEqual(len(resultat), 2)
        self.assertTrue(all(isinstance(i, Inscription) for i in resultat))

    def test_lister_toutes_vide(self):
        """Test 8: Lister sans inscription"""
        # Arrange
        self.mock_cursor.fetchall.return_value = []
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.inscription_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.__enter__.return_value = self.mock_connection
            resultat = self.dao.lister_toutes()
        
        # Assert
        self.assertEqual(len(resultat), 0)

    def test_lister_toutes_erreur_exception(self):
        """Test 9: Échec du listage avec exception"""
        # Arrange
        self.mock_cursor.execute.side_effect = Exception("Erreur DB")
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.inscription_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.__enter__.return_value = self.mock_connection
            resultat = self.dao.lister_toutes()
        
        # Assert
        self.assertEqual(len(resultat), 0)

    def test_compter_par_evenement_avec_inscriptions(self):
        """Test 10: Compter les inscriptions d'un événement"""
        # Arrange
        self.mock_cursor.fetchone.return_value = {"count": 15}
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.inscription_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.__enter__.return_value = self.mock_connection
            resultat = self.dao.compter_par_evenement(1)
        
        # Assert
        self.assertEqual(resultat, 15)
        self.mock_cursor.execute.assert_called_once()

    def test_compter_par_evenement_sans_inscription(self):
        """Test 11: Compter pour événement sans inscription"""
        # Arrange
        self.mock_cursor.fetchone.return_value = {"count": 0}
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.inscription_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.__enter__.return_value = self.mock_connection
            resultat = self.dao.compter_par_evenement(999)
        
        # Assert
        self.assertEqual(resultat, 0)

    def test_compter_par_evenement_erreur(self):
        """Test 12: Erreur lors du comptage"""
        # Arrange
        self.mock_cursor.execute.side_effect = Exception("Erreur DB")
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.inscription_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.__enter__.return_value = self.mock_connection
            resultat = self.dao.compter_par_evenement(1)
        
        # Assert
        self.assertEqual(resultat, 0)

    def test_supprimer_inscription_succes(self):
        """Test 13: Suppression réussie"""
        # Arrange
        inscription = Inscription(
            code_reservation=12345678,
            boit=True,
            mode_paiement="en ligne",
            id_event=1,
            nom_event="Test",
            id_bus_aller=1,
            id_bus_retour=2,
            created_by=1
        )
        
        self.mock_cursor.rowcount = 1
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.inscription_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.__enter__.return_value = self.mock_connection
            resultat = self.dao.supprimer(inscription)
        
        # Assert
        self.assertTrue(resultat)
        self.mock_cursor.execute.assert_called_once()

    def test_supprimer_inscription_inexistante(self):
        """Test 14: Suppression d'une inscription inexistante"""
        # Arrange
        inscription = Inscription(
            code_reservation=99999999,
            boit=False,
            mode_paiement="espece",
            id_event=1,
            nom_event="Test",
            id_bus_aller=1,
            id_bus_retour=2,
            created_by=1
        )
        
        self.mock_cursor.rowcount = 0
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.inscription_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.__enter__.return_value = self.mock_connection
            resultat = self.dao.supprimer(inscription)
        
        # Assert
        self.assertFalse(resultat)

    def test_supprimer_erreur_exception(self):
        """Test 15: Erreur lors de la suppression"""
        # Arrange
        inscription = Inscription(
            code_reservation=12345678,
            boit=True,
            mode_paiement="en ligne",
            id_event=1,
            nom_event="Test",
            id_bus_aller=1,
            id_bus_retour=2,
            created_by=1
        )
        
        self.mock_cursor.execute.side_effect = Exception("Erreur DB")
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.inscription_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.__enter__.return_value = self.mock_connection
            resultat = self.dao.supprimer(inscription)
        
        # Assert
        self.assertFalse(resultat)

    def test_est_deja_inscrit_true(self):
        """Test 16: Utilisateur déjà inscrit"""
        # Arrange
        self.mock_cursor.fetchone.return_value = {"exists": 1}
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.inscription_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.__enter__.return_value = self.mock_connection
            resultat = self.dao.est_deja_inscrit(created_by=1, id_event=1)
        
        # Assert
        self.assertTrue(resultat)

    def test_est_deja_inscrit_false(self):
        """Test 17: Utilisateur non inscrit"""
        # Arrange
        self.mock_cursor.fetchone.return_value = None
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.inscription_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.__enter__.return_value = self.mock_connection
            resultat = self.dao.est_deja_inscrit(created_by=1, id_event=999)
        
        # Assert
        self.assertFalse(resultat)

    def test_est_deja_inscrit_erreur(self):
        """Test 18: Erreur lors de la vérification"""
        # Arrange
        self.mock_cursor.execute.side_effect = Exception("Erreur DB")
        self.mock_connection.cursor.return_value.__enter__.return_value = self.mock_cursor
        
        # Act
        with patch('dao.inscription_dao.DBConnection') as mock_db:
            mock_db.return_value.connection.__enter__.return_value = self.mock_connection
            resultat = self.dao.est_deja_inscrit(created_by=1, id_event=1)
        
        # Assert
        self.assertFalse(resultat)


if __name__ == "__main__":
    unittest.main()