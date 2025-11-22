import unittest
from datetime import datetime
from business_object.inscription import Inscription


class TestInscription(unittest.TestCase):
    """Tests unitaires pour la classe métier Inscription"""

    def test_creation_inscription_valide(self):
        """Test 1: Création avec tous les paramètres valides"""
        # Arrange & Act
        inscription = Inscription(
            code_reservation=12345678,
            boit=True,
            mode_paiement="en ligne",
            id_event=1,
            nom_event="Soirée Karaoké",
            id_bus_aller=5,
            id_bus_retour=10,
            created_by=42
        )
        
        # Assert
        self.assertEqual(inscription.code_reservation, 12345678)
        self.assertTrue(inscription.boit)
        self.assertEqual(inscription.mode_paiement, "en ligne")
        self.assertEqual(inscription.id_event, 1)
        self.assertEqual(inscription.nom_event, "Soirée Karaoké")
        self.assertEqual(inscription.id_bus_aller, 5)
        self.assertEqual(inscription.id_bus_retour, 10)
        self.assertEqual(inscription.created_by, 42)
        self.assertIsInstance(inscription.created_at, datetime)

    def test_code_reservation_negatif(self):
        """Test 2: Validation - code de réservation négatif"""
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            Inscription(
                code_reservation=-123,
                boit=False,
                mode_paiement="espece",
                id_event=1,
                nom_event="Event",
                id_bus_aller=1,
                id_bus_retour=2,
                created_by=1
            )
        
        self.assertIn("positif", str(context.exception))

    def test_code_reservation_zero(self):
        """Test 3: Validation - code de réservation à zéro"""
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            Inscription(
                code_reservation=0,
                boit=False,
                mode_paiement="espece",
                id_event=1,
                nom_event="Event",
                id_bus_aller=1,
                id_bus_retour=2,
                created_by=1
            )
        
        self.assertIn("positif", str(context.exception))

    def test_boit_type_invalide(self):
        """Test 4: Validation - boit n'est pas un booléen"""
        # Act & Assert
        with self.assertRaises(TypeError) as context:
            Inscription(
                code_reservation=12345678,
                boit="oui",  # Devrait être un bool
                mode_paiement="espece",
                id_event=1,
                nom_event="Event",
                id_bus_aller=1,
                id_bus_retour=2,
                created_by=1
            )
        
        self.assertIn("bool", str(context.exception))

    def test_created_by_manquant(self):
        """Test 5: Validation - created_by obligatoire"""
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            Inscription(
                code_reservation=12345678,
                boit=False,
                mode_paiement="espece",
                id_event=1,
                nom_event="Event",
                id_bus_aller=1,
                id_bus_retour=2,
                created_by=None
            )
        
        self.assertIn("obligatoire", str(context.exception))

    def test_created_by_type_invalide(self):
        """Test 6: Validation - created_by doit être un entier"""
        # Act & Assert
        with self.assertRaises(TypeError) as context:
            Inscription(
                code_reservation=12345678,
                boit=False,
                mode_paiement="espece",
                id_event=1,
                nom_event="Event",
                id_bus_aller=1,
                id_bus_retour=2,
                created_by="user123"
            )
        
        self.assertIn("entier", str(context.exception))

    def test_mode_paiement_invalide(self):
        """Test 7: Validation - mode de paiement non autorisé"""
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            Inscription(
                code_reservation=12345678,
                boit=False,
                mode_paiement="cheque",  # Non autorisé
                id_event=1,
                nom_event="Event",
                id_bus_aller=1,
                id_bus_retour=2,
                created_by=1
            )
        
        self.assertIn("espece", str(context.exception))
        self.assertIn("en ligne", str(context.exception))

    def test_mode_paiement_vide_autorise(self):
        """Test 8: Mode de paiement vide est autorisé"""
        # Arrange & Act
        inscription = Inscription(
            code_reservation=12345678,
            boit=False,
            mode_paiement="",
            id_event=1,
            nom_event="Event",
            id_bus_aller=1,
            id_bus_retour=2,
            created_by=1
        )
        
        # Assert
        self.assertEqual(inscription.mode_paiement, "")

    def test_id_event_manquant(self):
        """Test 9: Validation - id_event obligatoire"""
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            Inscription(
                code_reservation=12345678,
                boit=False,
                mode_paiement="espece",
                id_event=None,
                nom_event="Event",
                id_bus_aller=1,
                id_bus_retour=2,
                created_by=1
            )
        
        self.assertIn("événement", str(context.exception).lower())

    def test_id_event_type_invalide(self):
        """Test 10: Validation - id_event doit être un entier"""
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            Inscription(
                code_reservation=12345678,
                boit=False,
                mode_paiement="espece",
                id_event="event_1",
                nom_event="Event",
                id_bus_aller=1,
                id_bus_retour=2,
                created_by=1
            )
        
        self.assertIn("entier", str(context.exception))

    def test_id_bus_type_invalide(self):
        """Test 11: Validation - id_bus doit être un entier"""
        # Act & Assert
        with self.assertRaises(TypeError) as context:
            Inscription(
                code_reservation=12345678,
                boit=False,
                mode_paiement="espece",
                id_event=1,
                nom_event="Event",
                id_bus_aller="bus_1",
                id_bus_retour=2,
                created_by=1
            )
        
        self.assertIn("entier", str(context.exception))

    def test_str_representation(self):
        """Test 12: Représentation textuelle __str__"""
        # Arrange
        inscription = Inscription(
            code_reservation=12345678,
            boit=True,
            mode_paiement="en ligne",
            id_event=1,
            nom_event="Soirée Karaoké",
            id_bus_aller=5,
            id_bus_retour=10,
            created_by=42
        )
        
        # Act
        str_representation = str(inscription)
        
        # Assert
        self.assertIn("12345678", str_representation)
        self.assertIn("Soirée Karaoké", str_representation)
        self.assertIn("5", str_representation)
        self.assertIn("10", str_representation)

    def test_repr_representation(self):
        """Test 13: Représentation __repr__"""
        # Arrange
        inscription = Inscription(
            code_reservation=12345678,
            boit=True,
            mode_paiement="en ligne",
            id_event=1,
            nom_event="Soirée Karaoké",
            id_bus_aller=5,
            id_bus_retour=10,
            created_by=42
        )
        
        # Act
        repr_representation = repr(inscription)
        
        # Assert
        self.assertIn("Inscription", repr_representation)
        self.assertIn("42", repr_representation)
        self.assertIn("Soirée Karaoké", repr_representation)

    def test_to_dict_conversion(self):
        """Test 14: Conversion en dictionnaire"""
        # Arrange
        inscription = Inscription(
            code_reservation=12345678,
            boit=True,
            mode_paiement="en ligne",
            id_event=1,
            nom_event="Soirée Karaoké",
            id_bus_aller=5,
            id_bus_retour=10,
            created_by=42
        )
        
        # Act
        dict_result = inscription.to_dict()
        
        # Assert
        self.assertEqual(dict_result["code_reservation"], 12345678)
        self.assertTrue(dict_result["boit"])
        self.assertEqual(dict_result["mode_paiement"], "en ligne")
        self.assertEqual(dict_result["id_event"], 1)
        self.assertEqual(dict_result["nom_event"], "Soirée Karaoké")
        self.assertEqual(dict_result["id_bus_aller"], 5)
        self.assertEqual(dict_result["id_bus_retour"], 10)
        self.assertEqual(dict_result["created_by"], 42)
        self.assertIn("created_at", dict_result)

    def test_from_dict_conversion(self):
        """Test 15: Création depuis un dictionnaire"""
        # Arrange
        data = {
            "code_reservation": 87654321,
            "boit": False,
            "created_by": 99,
            "mode_paiement": "espece",
            "id_event": 5,
            "nom_event": "Concert Rock",
            "id_bus_aller": 3,
            "id_bus_retour": 7,
            "created_at": "2024-01-15T10:30:00"
        }
        
        # Act
        inscription = Inscription.from_dict(data)
        
        # Assert
        self.assertEqual(inscription.code_reservation, 87654321)
        self.assertFalse(inscription.boit)
        self.assertEqual(inscription.created_by, 99)
        self.assertEqual(inscription.mode_paiement, "espece")
        self.assertEqual(inscription.id_event, 5)
        self.assertEqual(inscription.nom_event, "Concert Rock")
        self.assertEqual(inscription.id_bus_aller, 3)
        self.assertEqual(inscription.id_bus_retour, 7)
        self.assertIsInstance(inscription.created_at, datetime)

    def test_from_dict_valeurs_par_defaut(self):
        """Test 16: from_dict avec valeurs par défaut"""
        # Arrange
        data = {
            "code_reservation": 11111111,
            "created_by": 1,
            "id_event": 1,
            "id_bus_aller": 1,
            "id_bus_retour": 1
        }
        
        # Act
        inscription = Inscription.from_dict(data)
        
        # Assert
        self.assertFalse(inscription.boit)  # Valeur par défaut
        self.assertEqual(inscription.mode_paiement, "")  # Valeur par défaut

    def test_round_trip_to_dict_from_dict(self):
        """Test 17: Round-trip to_dict → from_dict"""
        # Arrange
        inscription_originale = Inscription(
            code_reservation=55555555,
            boit=True,
            mode_paiement="en ligne",
            id_event=10,
            nom_event="Festival",
            id_bus_aller=15,
            id_bus_retour=20,
            created_by=123
        )
        
        # Act
        dict_data = inscription_originale.to_dict()
        inscription_reconstructed = Inscription.from_dict(dict_data)
        
        # Assert
        self.assertEqual(inscription_originale.code_reservation, inscription_reconstructed.code_reservation)
        self.assertEqual(inscription_originale.boit, inscription_reconstructed.boit)
        self.assertEqual(inscription_originale.mode_paiement, inscription_reconstructed.mode_paiement)
        self.assertEqual(inscription_originale.id_event, inscription_reconstructed.id_event)
        self.assertEqual(inscription_originale.nom_event, inscription_reconstructed.nom_event)
        self.assertEqual(inscription_originale.id_bus_aller, inscription_reconstructed.id_bus_aller)
        self.assertEqual(inscription_originale.id_bus_retour, inscription_reconstructed.id_bus_retour)
        self.assertEqual(inscription_originale.created_by, inscription_reconstructed.created_by)


if __name__ == "__main__":
    unittest.main()