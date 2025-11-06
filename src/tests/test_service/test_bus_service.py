# tests/test_service/test_bus_service.py
from datetime import datetime
from unittest.mock import Mock, MagicMock
import pytest

from service.bus_service import BusService
from business_object.bus import Bus
from business_object.utilisateur import Utilisateur
from business_object.evenement import Evenement


@pytest.fixture
def bus_service():
    """Fixture pour créer un BusService avec des DAOs mockés."""
    service = BusService()
    service.bus_dao = Mock()
    service.evenement_dao = Mock()
    return service


@pytest.fixture
def admin_user():
    """Fixture pour un utilisateur admin."""
    return Utilisateur(
        pseudo="admin",
        nom="Admin",
        prenom="Super",
        email="admin@test.com",
        mot_de_passe="password123",
        admin=True,
        id_utilisateur=1
    )


@pytest.fixture
def normal_user():
    """Fixture pour un utilisateur normal (non-admin)."""
    return Utilisateur(
        pseudo="user",
        nom="Normal",
        prenom="User",
        email="user@test.com",
        mot_de_passe="password123",
        admin=False,
        id_utilisateur=2
    )


@pytest.fixture
def bus_aller():
    """Fixture pour un bus aller."""
    return Bus(
        id_event=1,
        sens="Aller",
        description=["direct"],
        heure_depart="08:00",
        id_bus=1
    )


@pytest.fixture
def bus_retour():
    """Fixture pour un bus retour."""
    return Bus(
        id_event=1,
        sens="Retour",
        description=["Arrêt 1", "Arrêt 2"],
        heure_depart="18:00",
        id_bus=2
    )


@pytest.fixture
def evenement_mock():
    """Fixture pour un événement mocké."""
    return Evenement(
        nom="Concert",
        description="Super concert",
        lieu="Rennes",
        date_debut=datetime(2025, 12, 1),
        date_fin=datetime(2025, 12, 1),
        nombre_places=100,
        id_evenement=1
    )


# ======================== TEST 1 : Créer un bus avec succès (admin) ========================
def test_creer_bus_succes(bus_service, admin_user, bus_aller, evenement_mock):
    """Test : Un admin peut créer un bus pour un événement existant."""
    # Arrange
    bus_service.evenement_dao.get_by_id.return_value = evenement_mock
    bus_service.bus_dao.creer.return_value = bus_aller

    # Act
    resultat = bus_service.creer_bus(bus_aller, admin_user)

    # Assert
    assert resultat is not None
    assert resultat.id_bus == 1
    assert resultat.sens == True  # Aller
    bus_service.evenement_dao.get_by_id.assert_called_once_with(1)
    bus_service.bus_dao.creer.assert_called_once_with(bus_aller)


# ======================== TEST 2 : Créer un bus échoue (non-admin) ========================
def test_creer_bus_non_admin(bus_service, normal_user, bus_aller):
    """Test : Un utilisateur non-admin ne peut pas créer un bus."""
    # Act & Assert
    with pytest.raises(PermissionError, match="Seuls les administrateurs peuvent créer des bus"):
        bus_service.creer_bus(bus_aller, normal_user)

    # Vérifier que le DAO n'a pas été appelé
    bus_service.bus_dao.creer.assert_not_called()


# ======================== TEST 3 : Créer un bus pour un événement inexistant ========================
def test_creer_bus_evenement_inexistant(bus_service, admin_user, bus_aller):
    """Test : Impossible de créer un bus pour un événement qui n'existe pas."""
    # Arrange
    bus_service.evenement_dao.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(ValueError, match="L'événement 1 n'existe pas"):
        bus_service.creer_bus(bus_aller, admin_user)

    # Vérifier que le DAO n'a pas été appelé
    bus_service.bus_dao.creer.assert_not_called()


# ======================== TEST 4 : Récupérer les bus disponibles par événement ========================
def test_get_bus_disponibles_pour_evenement(bus_service, bus_aller, bus_retour):
    """Test : Récupération des bus d'aller et de retour pour un événement."""
    # Arrange
    bus_autre_event = Bus(
        id_event=2,
        sens="Aller",
        description=["direct"],
        heure_depart="09:00",
        id_bus=3
    )
    
    bus_service.bus_dao.trouver_tous.return_value = [bus_aller, bus_retour, bus_autre_event]

    # Act
    resultat = bus_service.get_bus_disponibles_pour_evenement(1)

    # Assert
    assert len(resultat['aller']) == 1
    assert len(resultat['retour']) == 1
    assert resultat['aller'][0].id_bus == 1
    assert resultat['retour'][0].id_bus == 2
    # Vérifier que le bus de l'événement 2 n'est pas inclus
    assert bus_autre_event not in resultat['aller']
    assert bus_autre_event not in resultat['retour']


# ======================== TEST 5 : Supprimer un bus avec succès (admin) ========================
def test_supprimer_bus_succes(bus_service, admin_user, bus_aller):
    """Test : Un admin peut supprimer un bus existant."""
    # Arrange
    bus_service.bus_dao.get_by_id.return_value = bus_aller
    bus_service.bus_dao.supprimer.return_value = True

    # Act
    resultat = bus_service.supprimer_bus(1, admin_user)

    # Assert
    assert resultat is True
    bus_service.bus_dao.get_by_id.assert_called_once_with(1)
    bus_service.bus_dao.supprimer.assert_called_once_with(1)


# ======================== TEST BONUS 1 : Supprimer un bus échoue (non-admin) ========================
def test_supprimer_bus_non_admin(bus_service, normal_user):
    """Test : Un utilisateur non-admin ne peut pas supprimer un bus."""
    # Act & Assert
    with pytest.raises(PermissionError, match="Seuls les administrateurs peuvent supprimer des bus"):
        bus_service.supprimer_bus(1, normal_user)

    # Vérifier que le DAO n'a pas été appelé
    bus_service.bus_dao.supprimer.assert_not_called()


# ======================== TEST BONUS 2 : Supprimer un bus inexistant ========================
def test_supprimer_bus_inexistant(bus_service, admin_user):
    """Test : Impossible de supprimer un bus qui n'existe pas."""
    # Arrange
    bus_service.bus_dao.get_by_id.return_value = None

    # Act
    resultat = bus_service.supprimer_bus(999, admin_user)

    # Assert
    assert resultat is False
    bus_service.bus_dao.get_by_id.assert_called_once_with(999)
    bus_service.bus_dao.supprimer.assert_not_called()