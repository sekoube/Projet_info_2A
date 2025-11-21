import unittest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
from service.inscription_service import InscriptionService
from business_object.inscription import Inscription
from business_object.utilisateur import Utilisateur
from business_object.evenement import Evenement


class TestInscriptionService(unittest.TestCase):
    """Tests unitaires pour le service d'inscription"""

    def setUp(self):
        """Initialisation avant chaque test"""
        self.mock_inscription_dao = Mock()
        self.mock_evenement_dao = Mock()
        self.mock_utilisateur_dao = Mock()
        
        self.service = InscriptionService(
            self.mock_inscription_dao,
            self.mock_evenement_dao,
            self.mock_utilisateur_dao
        )
        self.service.inscription_dao = self.mock_inscription_dao
        self.service.evenement_dao = self.mock_evenement_dao
        self.service.utilisateur_dao = self.mock_utilisateur_dao

    def test_generer_code_reservation_unique(self):
        """Test 1: Génération d'un code de réservation unique"""
        # Arrange
        self.mock_inscription_dao.get_by.return_value = []
        
        # Act
        code = self.service.generer_code_reservation()
        
        # Assert
        self.assertIsInstance(code, int)
        self.assertEqual(len(str(code)), 8)
        self.mock_inscription_dao.get_by.assert_called()

    def test_generer_code_reservation_avec_collision(self):
        """Test 2: Génération de code avec collision (doit regénérer)"""
        # Arrange
        # Premier appel retourne une collision, second appel est libre
        self.mock_inscription_dao.get_by.side_effect = [
            [Mock()],  # Code déjà utilisé
            []         # Code libre
        ]
        
        # Act
        code = self.service.generer_code_reservation()
        
        # Assert
        self.assertIsInstance(code, int)
        self.assertEqual(self.mock_inscription_dao.get_by.call_count, 2)

    def test_creer_inscription_succes(self):
        """Test 3: Création d'inscription réussie"""
        # Arrange
        mock_utilisateur = Mock()
        mock_utilisateur.email = "test@example.com"
        mock_utilisateur.nom = "Dupont"
        self.mock_utilisateur_dao.get_by.return_value = [mock_utilisateur]
        
        mock_evenement = Mock()
        mock_evenement.capacite_max = 50
        self.mock_evenement_dao.get_by.return_value = [mock_evenement]
        
        self.mock_inscription_dao.compter_par_evenement.return_value = 20
        self.mock_inscription_dao.est_deja_inscrit.return_value = False
        self.mock_inscription_dao.get_by.return_value = []
        
        mock_inscription_created = Mock(spec=Inscription)
        self.mock_inscription_dao.creer.return_value = mock_inscription_created
        
        # Act
        with patch('service.inscription_service.send_email_brevo'):
            resultat = self.service.creer_inscription(
                boit=True,
                mode_paiement="en ligne",
                id_event=1,
                nom_event="Soirée Test",
                id_bus_aller=1,
                id_bus_retour=2,
                created_by=1
            )
        
        # Assert
        self.assertIsNotNone(resultat)
        self.mock_inscription_dao.creer.assert_called_once()

    def test_creer_inscription_utilisateur_inexistant(self):
        """Test 4: Échec - utilisateur inexistant"""
        # Arrange
        self.mock_utilisateur_dao.get_by.return_value = None
        
        # Act
        resultat = self.service.creer_inscription(
            boit=False,
            mode_paiement="espece",
            id_event=1,
            nom_event="Test Event",
            id_bus_aller=1,
            id_bus_retour=2,
            created_by=999
        )
        
        # Assert
        self.assertIsNone(resultat)
        self.mock_inscription_dao.creer.assert_not_called()

    def test_creer_inscription_evenement_inexistant(self):
        """Test 5: Échec - événement inexistant"""
        # Arrange
        mock_utilisateur = Mock()
        self.mock_utilisateur_dao.get_by.return_value = [mock_utilisateur]
        self.mock_evenement_dao.get_by.return_value = []
        
        # Act
        resultat = self.service.creer_inscription(
            boit=False,
            mode_paiement="espece",
            id_event=999,
            nom_event="Event Inexistant",
            id_bus_aller=1,
            id_bus_retour=2,
            created_by=1
        )
        
        # Assert
        self.assertIsNone(resultat)
        self.mock_inscription_dao.creer.assert_not_called()

    def test_creer_inscription_evenement_complet(self):
        """Test 6: Échec - événement à capacité maximale"""
        # Arrange
        mock_utilisateur = Mock()
        self.mock_utilisateur_dao.get_by.return_value = [mock_utilisateur]
        
        mock_evenement = Mock()
        mock_evenement.capacite_max = 50
        self.mock_evenement_dao.get_by.return_value = [mock_evenement]
        
        self.mock_inscription_dao.compter_par_evenement.return_value = 50
        
        # Act
        resultat = self.service.creer_inscription(
            boit=False,
            mode_paiement="espece",
            id_event=1,
            nom_event="Event Complet",
            id_bus_aller=1,
            id_bus_retour=2,
            created_by=1
        )
        
        # Assert
        self.assertIsNone(resultat)
        self.mock_inscription_dao.creer.assert_not_called()

    def test_creer_inscription_utilisateur_deja_inscrit(self):
        """Test 7: Échec - utilisateur déjà inscrit à l'événement"""
        # Arrange
        mock_utilisateur = Mock()
        self.mock_utilisateur_dao.get_by.return_value = [mock_utilisateur]
        
        mock_evenement = Mock()
        mock_evenement.capacite_max = 50
        self.mock_evenement_dao.get_by.return_value = [mock_evenement]
        
        self.mock_inscription_dao.compter_par_evenement.return_value = 20
        self.mock_inscription_dao.est_deja_inscrit.return_value = True
        
        # Act
        resultat = self.service.creer_inscription(
            boit=True,
            mode_paiement="en ligne",
            id_event=1,
            nom_event="Event Test",
            id_bus_aller=1,
            id_bus_retour=2,
            created_by=1
        )
        
        # Assert
        self.assertIsNone(resultat)
        self.mock_inscription_dao.creer.assert_not_called()

    def test_lister_toutes_inscriptions(self):
        """Test 8: Lister toutes les inscriptions"""
        # Arrange
        mock_inscriptions = [Mock(spec=Inscription), Mock(spec=Inscription)]
        self.mock_inscription_dao.lister_toutes.return_value = mock_inscriptions
        
        # Act
        resultat = self.service.lister_toutes_inscriptions()
        
        # Assert
        self.assertEqual(len(resultat), 2)
        self.mock_inscription_dao.lister_toutes.assert_called_once()

    def test_get_inscription_by_succes(self):
        """Test 9: Récupérer une inscription par champ"""
        # Arrange
        mock_inscription = Mock(spec=Inscription)
        self.mock_inscription_dao.get_by.return_value = [mock_inscription]
        
        # Act
        resultat = self.service.get_inscription_by("code_reservation", 12345678)
        
        # Assert
        self.assertIsNotNone(resultat)
        self.mock_inscription_dao.get_by.assert_called_once_with("code_reservation", 12345678)

    def test_get_inscription_by_champ_invalide(self):
        """Test 10: Récupérer inscription avec champ invalide"""
        # Arrange
        self.mock_inscription_dao.get_by.side_effect = ValueError("Colonne 'invalid' non autorisée.")
        
        # Act & Assert
        with self.assertRaises(ValueError):
            self.service.get_inscription_by("invalid_field", "value")

    def test_supprimer_inscription_succes(self):
        """Test 11: Suppression d'inscription réussie"""
        # Arrange
        mock_inscription = Mock(spec=Inscription)
        mock_inscription.created_by = 1
        mock_inscription.code_reservation = 12345678
        self.mock_inscription_dao.get_by.return_value = [mock_inscription]
        self.mock_inscription_dao.supprimer.return_value = True
        
        # Act
        resultat = self.service.supprimer_inscription("12345678", 1)
        
        # Assert
        self.assertTrue(resultat)
        self.mock_inscription_dao.supprimer.assert_called_once()

    def test_supprimer_inscription_permission_refusee(self):
        """Test 12: Échec suppression - utilisateur non propriétaire"""
        # Arrange
        mock_inscription = Mock(spec=Inscription)
        mock_inscription.created_by = 1
        mock_inscription.code_reservation = 12345678
        self.mock_inscription_dao.get_by.return_value = [mock_inscription]
        
        # Act & Assert
        with self.assertRaises(PermissionError):
            self.service.supprimer_inscription("12345678", 2)

    def test_supprimer_inscription_code_invalide(self):
        """Test 13: Échec suppression - code de réservation vide"""
        # Act & Assert
        with self.assertRaises(ValueError):
            self.service.supprimer_inscription("", 1)

    def test_supprimer_inscription_inexistante(self):
        """Test 14: Échec suppression - inscription inexistante"""
        # Arrange
        self.mock_inscription_dao.get_by.return_value = []
        
        # Act & Assert
        with self.assertRaises(ValueError):
            self.service.supprimer_inscription("99999999", 1)


if __name__ == "__main__":
    unittest.main()