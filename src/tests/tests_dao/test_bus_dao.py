import pytest
from unittest.mock import patch, MagicMock
from dao.bus_dao import BusDAO
from business_object.bus import Bus


@pytest.fixture
def fake_bus():
    """Crée un objet Bus fictif pour les tests."""
    return Bus(
        id_bus=None,
        id_event=1,
        sens="Aller",
        description="Bus vers le stade",
        heure_depart="10:00",
        capacite_max=50
    )


# Test de la création d’un bus (INSERT + récupération de l’id)
@patch("dao.bus_dao.DBConnection")
def test_creer_bus(mock_db_conn, fake_bus):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Simule le comportement du curseur et de la base
    mock_cursor.fetchone.return_value = {"id_bus": 42}
    mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_db_conn.return_value.connection = mock_conn

    bus = BusDAO.creer(fake_bus)

    mock_cursor.execute.assert_called_once()
    assert bus.id_bus == 42


# Test de récupération d’un bus par identifiant d’événement
@patch("dao.bus_dao.DBConnection")
def test_get_by_event(mock_db_conn, fake_bus):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Simule un résultat de requête
    mock_cursor.fetchone.return_value = {
        "id_bus": 1,
        "id_event": 1,
        "sens": "Aller",
        "description": "Bus vers le stade",
        "heure_depart": "10:00"
    }

    mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_db_conn.return_value.connection = mock_conn

    # Patch de la méthode from_dict pour créer l’objet Bus
    with patch.object(Bus, "from_dict", return_value=fake_bus) as mock_from_dict:
        result = BusDAO.get_by_event(1)
        mock_cursor.execute.assert_called_once_with("SELECT * FROM bus WHERE id_event = %s", (1,))
        mock_from_dict.assert_called_once()
        assert isinstance(result, Bus)


# Test de récupération d’un bus par son identifiant unique
@patch("dao.bus_dao.DBConnection")
def test_get_by_id(mock_db_conn, fake_bus):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchone.return_value = {
        "id_bus": 10,
        "id_event": 1,
        "sens": "Retour",
        "description": "Bus du retour",
        "heure_depart": "18:00"
    }

    mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_db_conn.return_value.connection = mock_conn

    with patch.object(Bus, "from_dict", return_value=fake_bus):
        result = BusDAO.get_by_id(10)
        assert isinstance(result, Bus)


# Test de récupération de tous les bus
@patch("dao.bus_dao.DBConnection")
def test_lister_tous(mock_db_conn, fake_bus):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchall.return_value = [
        {"id_bus": 1, "id_event": 1, "sens": "Aller", "description": "Desc1", "heure_depart": "10:00:00"},
        {"id_bus": 2, "id_event": 1, "sens": "Retour", "description": "Desc2", "heure_depart": "18:00:00"}
    ]

    mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_db_conn.return_value.connection = mock_conn

    with patch.object(Bus, "from_dict", side_effect=[fake_bus, fake_bus]):
        result = BusDAO.lister_tous()
        assert len(result) == 2
        assert all(isinstance(b, Bus) for b in result)


# Test de suppression d’un bus
@patch("dao.bus_dao.DBConnection")
def test_supprimer_bus(mock_db_conn):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.rowcount = 1
    mock_conn.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    mock_db_conn.return_value.connection = mock_conn

    result = BusDAO.supprimer(99)

    mock_cursor.execute.assert_called_once_with("DELETE FROM bus WHERE id_bus = %s", (99,))
    assert result is True
