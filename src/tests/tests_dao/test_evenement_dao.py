import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, date
from decimal import Decimal
from business_object.evenement import Evenement
from dao.evenement_dao import EvenementDAO


@pytest.fixture
def mock_connection():
    """Fixture pour simuler une connexion à la base de données."""
    connection = MagicMock()
    cursor = MagicMock()
    connection.cursor.return_value.__enter__.return_value = cursor
    connection.__enter__.return_value = connection
    connection.__exit__.return_value = None
    return connection, cursor


@pytest.fixture
def evenement_test():
    """Fixture pour un événement de test."""
    return Evenement(
        id_event=None,
        titre="Concert de Jazz",
        description_event="Soirée jazz avec musiciens professionnels",
        lieu="Salle Pleyel",
        date_event=date(2025, 6, 15),
        capacite_max=200,
        created_by=1,
        created_at=datetime(2024, 1, 10, 14, 30, 0),
        tarif=25.50,
        statut="en_cours"
    )


@pytest.fixture
def evenement_complet():
    """Fixture pour un événement complet."""
    return Evenement(
        id_event=None,
        titre="Festival Rock",
        description_event="Grand festival de rock",
        lieu="Stade de France",
        date_event=date(2025, 7, 20),
        capacite_max=50000,
        created_by=2,
        created_at=datetime(2024, 2, 1, 10, 0, 0),
        tarif=75.00,
        statut="complet"
    )


# ============================================================
# TESTS CRÉATION
# ============================================================

@patch('dao.evenement_dao.DBConnection')
def test_creer_evenement_success(mock_db, mock_connection, evenement_test):
    """Test la création réussie d'un événement."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.fetchone.return_value = {"id_event": 1}

    dao = EvenementDAO()

    # Act
    resultat = dao.creer(evenement_test)

    # Assert
    assert resultat is True
    assert evenement_test.id_event == 1
    cursor.execute.assert_called_once()
    args = cursor.execute.call_args[0]
    assert "INSERT INTO evenement" in args[0]
    
    params = cursor.execute.call_args[0][1]
    assert params["titre"] == "Concert de Jazz"
    assert params["lieu"] == "Salle Pleyel"
    assert params["capacite_max"] == 200
    assert params["tarif"] == 25.50
    assert params["statut"] == "en_cours"


@patch('dao.evenement_dao.DBConnection')
def test_creer_evenement_avec_description(mock_db, mock_connection):
    """Test la création d'un événement avec description complète."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.fetchone.return_value = {"id_event": 5}

    evenement = Evenement(
        titre="Conférence Tech",
        description_event="Conférence sur l'IA et le machine learning",
        lieu="Palais des Congrès",
        date_event=date(2025, 9, 10),
        capacite_max=500,
        created_by=3,
        tarif=50.00
    )

    dao = EvenementDAO()

    # Act
    resultat = dao.creer(evenement)

    # Assert
    assert resultat is True
    assert evenement.id_event == 5
    params = cursor.execute.call_args[0][1]
    assert params["description_event"] == "Conférence sur l'IA et le machine learning"


@patch('dao.evenement_dao.DBConnection')
def test_creer_evenement_statut_complet(mock_db, mock_connection, evenement_complet):
    """Test la création d'un événement avec statut 'complet'."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.fetchone.return_value = {"id_event": 10}

    dao = EvenementDAO()

    # Act
    resultat = dao.creer(evenement_complet)

    # Assert
    assert resultat is True
    params = cursor.execute.call_args[0][1]
    assert params["statut"] == "complet"


@patch('dao.evenement_dao.DBConnection')
def test_creer_evenement_echec_pas_de_retour(mock_db, mock_connection, evenement_test):
    """Test l'échec de création quand la base ne retourne pas d'ID."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.fetchone.return_value = None

    dao = EvenementDAO()

    # Act
    resultat = dao.creer(evenement_test)

    # Assert
    assert resultat is False
    assert evenement_test.id_event is None


@patch('dao.evenement_dao.DBConnection')
def test_creer_evenement_exception(mock_db, mock_connection, evenement_test):
    """Test la gestion d'exception lors de la création."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.execute.side_effect = Exception("Erreur de connexion")

    dao = EvenementDAO()

    # Act
    resultat = dao.creer(evenement_test)

    # Assert
    assert resultat is False


# ============================================================
# TESTS LISTAGE
# ============================================================

@patch('dao.evenement_dao.DBConnection')
def test_lister_tous_vide(mock_db, mock_connection):
    """Test le listage quand aucun événement n'existe."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.fetchall.return_value = []
    cursor.description = []

    dao = EvenementDAO()

    # Act
    resultat = dao.lister_tous()

    # Assert
    assert resultat == []
    cursor.execute.assert_called_once()
    args = cursor.execute.call_args[0]
    assert "SELECT" in args[0]
    assert "FROM evenement" in args[0]
    assert "ORDER BY date_event DESC" in args[0]


@patch('dao.evenement_dao.DBConnection')
def test_lister_tous_un_evenement(mock_db, mock_connection):
    """Test le listage avec un seul événement."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    
    cursor.description = [
        ('id_event',), ('titre',), ('description_event',), ('lieu',),
        ('date_event',), ('capacite_max',), ('created_by',),
        ('created_at',), ('tarif',), ('statut',)
    ]
    
    cursor.fetchall.return_value = [
        (1, "Concert Jazz", "Description", "Salle Pleyel",
         date(2025, 6, 15), 200, 1,
         datetime(2024, 1, 10, 14, 30, 0), 25.50, "en_cours")
    ]

    dao = EvenementDAO()

    # Act
    resultat = dao.lister_tous()

    # Assert
    assert len(resultat) == 1
    assert isinstance(resultat[0], Evenement)
    assert resultat[0].titre == "Concert Jazz"
    assert resultat[0].capacite_max == 200


@patch('dao.evenement_dao.DBConnection')
def test_lister_tous_plusieurs_evenements(mock_db, mock_connection):
    """Test le listage avec plusieurs événements triés par date décroissante."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    
    cursor.description = [
        ('id_event',), ('titre',), ('description_event',), ('lieu',),
        ('date_event',), ('capacite_max',), ('created_by',),
        ('created_at',), ('tarif',), ('statut',)
    ]
    
    cursor.fetchall.return_value = [
        (3, "Festival Rock", "Grand festival", "Stade",
         date(2025, 7, 20), 50000, 2,
         datetime(2024, 2, 1), 75.00, "en_cours"),
        (1, "Concert Jazz", "Soirée jazz", "Salle",
         date(2025, 6, 15), 200, 1,
         datetime(2024, 1, 10), 25.50, "complet"),
        (2, "Théâtre", "Pièce classique", "Théâtre",
         date(2025, 5, 10), 150, 1,
         datetime(2024, 1, 15), 30.00, "passe")
    ]

    dao = EvenementDAO()

    # Act
    resultat = dao.lister_tous()

    # Assert
    assert len(resultat) == 3
    assert all(isinstance(e, Evenement) for e in resultat)
    # Vérifier l'ordre (plus récent en premier)
    assert resultat[0].date_event == date(2025, 7, 20)
    assert resultat[1].date_event == date(2025, 6, 15)
    assert resultat[2].date_event == date(2025, 5, 10)


@patch('dao.evenement_dao.DBConnection')
def test_lister_tous_exception(mock_db, mock_connection):
    """Test la gestion d'exception lors du listage."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.execute.side_effect = Exception("Erreur de connexion")

    dao = EvenementDAO()

    # Act
    resultat = dao.lister_tous()

    # Assert
    assert resultat == []


# ============================================================
# TESTS GET_BY
# ============================================================

@patch('dao.evenement_dao.DBConnection')
def test_get_by_id_event(mock_db, mock_connection):
    """Test la recherche d'un événement par ID."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.fetchall.return_value = [
        {
            "id_event": 1,
            "titre": "Concert Jazz",
            "description_event": "Soirée jazz",
            "lieu": "Salle Pleyel",
            "date_event": date(2025, 6, 15),
            "capacite_max": 200,
            "created_by": 1,
            "created_at": datetime(2024, 1, 10),
            "tarif": 25.50,
            "statut": "en_cours"
        }
    ]

    dao = EvenementDAO()

    # Act
    resultat = dao.get_by("id_event", 1)

    # Assert
    assert len(resultat) == 1
    assert resultat[0].id_event == 1
    assert resultat[0].titre == "Concert Jazz"
    cursor.execute.assert_called_once()
    args = cursor.execute.call_args[0]
    assert "WHERE id_event = %(value)s" in args[0]


@patch('dao.evenement_dao.DBConnection')
def test_get_by_titre(mock_db, mock_connection):
    """Test la recherche d'événements par titre."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.fetchall.return_value = [
        {
            "id_event": 5,
            "titre": "Concert Rock",
            "description_event": "Soirée rock",
            "lieu": "Zenith",
            "date_event": date(2025, 8, 20),
            "capacite_max": 1000,
            "created_by": 2,
            "created_at": datetime(2024, 3, 1),
            "tarif": 40.00,
            "statut": "en_cours"
        }
    ]

    dao = EvenementDAO()

    # Act
    resultat = dao.get_by("titre", "Concert Rock")

    # Assert
    assert len(resultat) == 1
    assert resultat[0].titre == "Concert Rock"


@patch('dao.evenement_dao.DBConnection')
def test_get_by_created_by(mock_db, mock_connection):
    """Test la recherche d'événements par créateur."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.fetchall.return_value = [
        {
            "id_event": 1,
            "titre": "Event 1",
            "description_event": "Desc 1",
            "lieu": "Lieu 1",
            "date_event": date(2025, 6, 15),
            "capacite_max": 100,
            "created_by": 1,
            "created_at": datetime(2024, 1, 1),
            "tarif": 10.00,
            "statut": "en_cours"
        },
        {
            "id_event": 2,
            "titre": "Event 2",
            "description_event": "Desc 2",
            "lieu": "Lieu 2",
            "date_event": date(2025, 7, 20),
            "capacite_max": 150,
            "created_by": 1,
            "created_at": datetime(2024, 1, 5),
            "tarif": 15.00,
            "statut": "en_cours"
        }
    ]

    dao = EvenementDAO()

    # Act
    resultat = dao.get_by("created_by", 1)

    # Assert
    assert len(resultat) == 2
    assert all(e.created_by == 1 for e in resultat)


@patch('dao.evenement_dao.DBConnection')
def test_get_by_statut(mock_db, mock_connection):
    """Test la recherche d'événements par statut."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.fetchall.return_value = [
        {
            "id_event": 1,
            "titre": "Event Complet 1",
            "description_event": "Desc",
            "lieu": "Lieu",
            "date_event": date(2025, 6, 15),
            "capacite_max": 50,
            "created_by": 1,
            "created_at": datetime(2024, 1, 1),
            "tarif": 20.00,
            "statut": "complet"
        }
    ]

    dao = EvenementDAO()

    # Act
    resultat = dao.get_by("statut", "complet")

    # Assert
    assert len(resultat) == 1
    assert resultat[0].statut == "complet"


@patch('dao.evenement_dao.DBConnection')
def test_get_by_aucun_resultat(mock_db, mock_connection):
    """Test la recherche qui ne retourne aucun résultat."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.fetchall.return_value = []

    dao = EvenementDAO()

    # Act
    resultat = dao.get_by("titre", "Événement Inexistant")

    # Assert
    assert resultat == []


def test_get_by_colonne_non_autorisee():
    """Test qu'une ValueError est levée pour une colonne non autorisée."""
    # Arrange
    dao = EvenementDAO()

    # Act & Assert
    with pytest.raises(ValueError, match="Colonne 'invalid_column' non autorisée"):
        dao.get_by("invalid_column", "valeur")


def test_get_by_toutes_colonnes_autorisees():
    """Test que toutes les colonnes légitimes sont autorisées."""
    # Arrange
    dao = EvenementDAO()
    colonnes_valides = [
        "id_event", "titre", "description_event", "lieu",
        "date_event", "capacite_max", "created_by",
        "created_at", "tarif", "statut"
    ]

    # Act & Assert
    with patch('dao.evenement_dao.DBConnection') as mock_db:
        connection = MagicMock()
        cursor = MagicMock()
        connection.cursor.return_value.__enter__.return_value = cursor
        mock_db.return_value.connection = connection
        cursor.fetchall.return_value = []

        for colonne in colonnes_valides:
            try:
                dao.get_by(colonne, "test_value")
            except ValueError:
                pytest.fail(f"La colonne '{colonne}' devrait être autorisée")


# ============================================================
# TESTS SUPPRESSION
# ============================================================

@patch('dao.evenement_dao.DBConnection')
def test_supprimer_evenement_success(mock_db, mock_connection, evenement_test):
    """Test la suppression réussie d'un événement."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.rowcount = 1
    evenement_test.id_event = 5

    dao = EvenementDAO()

    # Act
    resultat = dao.supprimer(evenement_test)

    # Assert
    assert resultat is True
    cursor.execute.assert_called_once()
    args = cursor.execute.call_args[0]
    assert "DELETE FROM evenement" in args[0]
    assert "WHERE id_event = %(id_event)s" in args[0]
    assert args[1] == {"id_event": 5}


@patch('dao.evenement_dao.DBConnection')
def test_supprimer_evenement_inexistant(mock_db, mock_connection, evenement_test):
    """Test la suppression d'un événement inexistant."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.rowcount = 0
    evenement_test.id_event = 999

    dao = EvenementDAO()

    # Act
    resultat = dao.supprimer(evenement_test)

    # Assert
    assert resultat is False


@patch('dao.evenement_dao.DBConnection')
def test_supprimer_evenement_exception(mock_db, mock_connection, evenement_test):
    """Test la gestion d'exception lors de la suppression."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.execute.side_effect = Exception("Erreur de connexion")
    evenement_test.id_event = 5

    dao = EvenementDAO()

    # Act
    resultat = dao.supprimer(evenement_test)

    # Assert
    assert resultat is False


# ============================================================
# TESTS MODIFICATION STATUT
# ============================================================

@patch('dao.evenement_dao.DBConnection')
def test_modifier_statut_success(mock_db, mock_connection):
    """Test la modification réussie du statut d'un événement."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.rowcount = 1

    dao = EvenementDAO()

    # Act
    resultat = dao.modifier_statut(5, "complet")

    # Assert
    assert resultat is True
    cursor.execute.assert_called_once()
    args = cursor.execute.call_args[0]
    assert "UPDATE evenement" in args[0]
    assert "SET statut = %(statut)s" in args[0]
    assert "WHERE id_event = %(id_event)s" in args[0]
    assert args[1] == {"statut": "complet", "id_event": 5}


@patch('dao.evenement_dao.DBConnection')
def test_modifier_statut_en_passe(mock_db, mock_connection):
    """Test le passage d'un événement au statut 'passé'."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.rowcount = 1

    dao = EvenementDAO()

    # Act
    resultat = dao.modifier_statut(10, "passe")

    # Assert
    assert resultat is True
    params = cursor.execute.call_args[0][1]
    assert params["statut"] == "passe"


@patch('dao.evenement_dao.DBConnection')
def test_modifier_statut_evenement_inexistant(mock_db, mock_connection):
    """Test la modification de statut pour un événement inexistant."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.rowcount = 0

    dao = EvenementDAO()

    # Act
    resultat = dao.modifier_statut(999, "complet")

    # Assert
    assert resultat is False


@patch('dao.evenement_dao.DBConnection')
def test_modifier_statut_exception(mock_db, mock_connection):
    """Test la gestion d'exception lors de la modification du statut."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.execute.side_effect = Exception("Erreur de connexion")

    dao = EvenementDAO()

    # Act
    resultat = dao.modifier_statut(5, "complet")

    # Assert
    assert resultat is False