import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import date, datetime
from business_object.evenement import Evenement
from service.evenement_service import EvenementService


@pytest.fixture
def mock_daos():
    """Fixture pour les DAOs mockés"""
    return {
        "evenement_dao": Mock(),
        "inscription_dao": Mock(),
        "utilisateur_dao": Mock(),
        "bus_dao": Mock()
    }


@pytest.fixture
def evenement_service(mock_daos):
    """Fixture pour le service avec DAOs mockés"""
    return EvenementService(
        evenement_dao=mock_daos["evenement_dao"],
        inscription_dao=mock_daos["inscription_dao"],
        utilisateur_dao=mock_daos["utilisateur_dao"],
        bus_dao=mock_daos["bus_dao"]
    )


@pytest.fixture
def fake_evenement():
    """Fixture pour un événement factice"""
    return Evenement(
        id_event=1,
        titre="Conférence Python",
        lieu="Paris",
        date_event=date(2025, 6, 15),
        capacite_max=100,
        created_by=1,
        description_event="Une grande conférence",
        tarif=50.00,
        statut="en_cours"
    )


class TestCreerEvenement:
    """Tests pour la création d'événement"""

    def test_creer_evenement_succes(self, evenement_service, mock_daos, fake_evenement):
        """Test 1: Création réussie d'un événement"""
        # Arrange
        mock_daos["utilisateur_dao"].get_by.return_value = [Mock(id_utilisateur=1)]
        mock_daos["evenement_dao"].creer.return_value = True

        # Act
        resultat = evenement_service.creer_evenement(
            titre="Conférence Python",
            lieu="Paris",
            date_event=date(2025, 6, 15),
            capacite_max=100,
            created_by=1,
            description_event="Une grande conférence",
            tarif=50.00
        )

        # Assert
        assert resultat is not None
        assert isinstance(resultat, Evenement)
        assert resultat.titre == "Conférence Python"
        mock_daos["utilisateur_dao"].get_by.assert_called_once_with("id_utilisateur", 1)
        mock_daos["evenement_dao"].creer.assert_called_once()

    def test_creer_evenement_utilisateur_inexistant(self, evenement_service, mock_daos):
        """Test 2: Création échouée - utilisateur inexistant"""
        # Arrange
        mock_daos["utilisateur_dao"].get_by.return_value = []

        # Act
        resultat = evenement_service.creer_evenement(
            titre="Conférence",
            lieu="Paris",
            date_event=date(2025, 6, 15),
            capacite_max=100,
            created_by=999
        )

        # Assert
        assert resultat is None
        mock_daos["evenement_dao"].creer.assert_not_called()

    


class TestGetEvenementBy:
    """Tests pour la récupération d'événement par champ"""

    def test_get_evenement_by_succes(self, evenement_service, mock_daos, fake_evenement):
        """Test 1: Récupération réussie d'un événement"""
        # Arrange
        mock_daos["evenement_dao"].get_by.return_value = [fake_evenement]

        # Act
        resultat = evenement_service.get_evenement_by("titre", "Conférence Python")

        # Assert
        assert resultat is not None
        assert len(resultat) == 1
        assert resultat[0].titre == "Conférence Python"
        mock_daos["evenement_dao"].get_by.assert_called_once_with("titre", "Conférence Python")

    def test_get_evenement_by_colonne_invalide(self, evenement_service, mock_daos):
        """Test 2: Récupération échouée - colonne invalide"""
        # Arrange
        mock_daos["evenement_dao"].get_by.side_effect = ValueError("Colonne 'invalide' non autorisée.")

        # Act
        resultat = evenement_service.get_evenement_by("invalide", "valeur")

        # Assert
        assert resultat == []
        mock_daos["evenement_dao"].get_by.assert_called_once()

    def test_get_evenement_by_pas_de_resultats(self, evenement_service, mock_daos):
        """Test 3: Récupération - aucun résultat"""
        # Arrange
        mock_daos["evenement_dao"].get_by.return_value = []

        # Act
        resultat = evenement_service.get_evenement_by("titre", "Inexistant")

        # Assert
        assert resultat == []


class TestGetTousLesEvenements:
    """Tests pour la récupération de tous les événements"""

    def test_get_tous_les_evenements_succes(self, evenement_service, mock_daos, fake_evenement):
        """Test 1: Récupération réussie de tous les événements"""
        # Arrange
        mock_daos["evenement_dao"].lister_tous.return_value = [fake_evenement]

        # Act
        resultat = evenement_service.get_tous_les_evenement()

        # Assert
        assert len(resultat) == 1
        assert resultat[0].titre == "Conférence Python"
        mock_daos["evenement_dao"].lister_tous.assert_called_once()

    def test_get_tous_les_evenements_liste_vide(self, evenement_service, mock_daos):
        """Test 2: Récupération - liste vide"""
        # Arrange
        mock_daos["evenement_dao"].lister_tous.return_value = []

        # Act
        resultat = evenement_service.get_tous_les_evenement()

        # Assert
        assert resultat == []

    def test_get_tous_les_evenements_erreur(self, evenement_service, mock_daos):
        """Test 3: Récupération - erreur base de données"""
        # Arrange
        mock_daos["evenement_dao"].lister_tous.side_effect = Exception("Erreur BD")

        # Act
        resultat = evenement_service.get_tous_les_evenement()

        # Assert
        assert resultat == []


class TestSupprimerEvenement:
    """Tests pour la suppression d'événement"""

    def test_supprimer_evenement_succes(self, evenement_service, mock_daos, fake_evenement):
        """Test 1: Suppression réussie d'un événement"""
        # Arrange
        mock_daos["evenement_dao"].get_by.return_value = [fake_evenement]
        mock_daos["evenement_dao"].supprimer.return_value = True

        # Act
        resultat = evenement_service.supprimer_evenement(1)

        # Assert
        assert resultat is True
        mock_daos["evenement_dao"].get_by.assert_called_once_with("id_event", 1)
        mock_daos["evenement_dao"].supprimer.assert_called_once_with(fake_evenement)

    def test_supprimer_evenement_inexistant(self, evenement_service, mock_daos):
        """Test 2: Suppression échouée - événement inexistant"""
        # Arrange
        mock_daos["evenement_dao"].get_by.return_value = []

        # Act
        resultat = evenement_service.supprimer_evenement(999)

        # Assert
        assert resultat is False
        mock_daos["evenement_dao"].supprimer.assert_not_called()

    def test_supprimer_evenement_erreur_dao(self, evenement_service, mock_daos, fake_evenement):
        """Test 3: Suppression échouée - erreur DAO"""
        # Arrange
        mock_daos["evenement_dao"].get_by.return_value = [fake_evenement]
        mock_daos["evenement_dao"].supprimer.return_value = False

        # Act
        resultat = evenement_service.supprimer_evenement(1)

        # Assert
        assert resultat is False


class TestModifierStatut:
    """Tests pour la modification du statut d'événement"""

    def test_modifier_statut_evenement_passe(self, evenement_service, mock_daos):
        """Test 1: Modification de statut - événement passé"""
        # Arrange
        evenement_passe = Evenement(
            id_event=1,
            titre="Conférence",
            lieu="Paris",
            date_event=date(2020, 1, 1),
            capacite_max=100,
            created_by=1,
            statut="en_cours"
        )
        mock_daos["evenement_dao"].get_by.return_value = [evenement_passe]
        mock_daos["evenement_dao"].modifier_statut.return_value = True

        # Act
        resultat = evenement_service.modifier_statut(1)

        # Assert
        assert resultat is True
        mock_daos["evenement_dao"].modifier_statut.assert_called_once_with(1, "passe")

    def test_modifier_statut_evenement_complet(self, evenement_service, mock_daos):
        """Test 2: Modification de statut - événement complet"""
        # Arrange
        evenement_futur = Evenement(
            id_event=1,
            titre="Conférence",
            lieu="Paris",
            date_event=date(2026, 6, 15),
            capacite_max=100,
            created_by=1,
            statut="en_cours"
        )
        mock_daos["evenement_dao"].get_by.return_value = [evenement_futur]
        mock_daos["inscription_dao"].compter_par_evenement.return_value = 100
        mock_daos["evenement_dao"].modifier_statut.return_value = True

        # Act
        resultat = evenement_service.modifier_statut(1)

        # Assert
        assert resultat is True
        mock_daos["evenement_dao"].modifier_statut.assert_called_once_with(1, "complet")

    
    def test_modifier_statut_evenement_inexistant(self, evenement_service, mock_daos):
        """Test 4: Modification de statut - événement inexistant"""
        # Arrange
        mock_daos["evenement_dao"].get_by.return_value = []

        # Act
        resultat = evenement_service.modifier_statut(999)

        # Assert
        assert resultat is False
        mock_daos["evenement_dao"].modifier_statut.assert_not_called()

    def test_modifier_statut_pas_de_changement(self, evenement_service, mock_daos):
        """Test 5: Modification de statut - aucun changement nécessaire"""
        # Arrange
        evenement_passe = Evenement(
            id_event=1,
            titre="Conférence",
            lieu="Paris",
            date_event=date(2020, 1, 1),
            capacite_max=100,
            created_by=1,
            statut="passe"
        )
        mock_daos["evenement_dao"].get_by.return_value = [evenement_passe]

        # Act
        resultat = evenement_service.modifier_statut(1)

        # Assert
        assert resultat is True
        mock_daos["evenement_dao"].modifier_statut.assert_not_called()