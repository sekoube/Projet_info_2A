import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
from psycopg2.errors import UniqueViolation
from business_object.utilisateur import Utilisateur
from dao.utilisateur_dao import UtilisateurDAO


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
def utilisateur_test():
    """Fixture pour un utilisateur de test."""
    return Utilisateur(
        id_utilisateur=None,
        nom="Dupont",
        prenom="Jean",
        email="jean.dupont@test.com",
        mot_de_passe="hashed_password_123",
        role=False,
        created_at=datetime(2024, 1, 15, 10, 30, 0)
    )


@pytest.fixture
def utilisateur_admin():
    """Fixture pour un administrateur de test."""
    return Utilisateur(
        id_utilisateur=None,
        nom="Martin",
        prenom="Sophie",
        email="sophie.martin@test.com",
        mot_de_passe="hashed_password_456",
        role=True,
        created_at=datetime(2024, 2, 20, 14, 45, 0)
    )


# ============================================================
# TESTS CRÉATION
# ============================================================

@patch('dao.utilisateur_dao.DBConnection')
def test_creer_utilisateur_success(mock_db, mock_connection, utilisateur_test):
    """Test la création réussie d'un utilisateur."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.fetchone.return_value = {"id_utilisateur": 1}

    # Act
    resultat = UtilisateurDAO.creer(utilisateur_test)

    # Assert
    assert resultat.id_utilisateur == 1
    cursor.execute.assert_called_once()
    args = cursor.execute.call_args[0]
    assert "INSERT INTO projet.utilisateur" in args[0]
    assert args[1] == (
        "Dupont",
        "Jean",
        "jean.dupont@test.com",
        "hashed_password_123",
        False,
        utilisateur_test.created_at
    )


@patch('dao.utilisateur_dao.DBConnection')
def test_creer_utilisateur_admin(mock_db, mock_connection, utilisateur_admin):
    """Test la création d'un administrateur."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.fetchone.return_value = {"id_utilisateur": 5}

    # Act
    resultat = UtilisateurDAO.creer(utilisateur_admin)

    # Assert
    assert resultat.id_utilisateur == 5
    assert resultat.role is True
    args = cursor.execute.call_args[0]
    assert args[1][4] is True  # Vérifier que role=True




# ============================================================
# TESTS LISTAGE
# ============================================================

@patch('dao.utilisateur_dao.DBConnection')
def test_lister_tous_vide(mock_db, mock_connection):
    """Test le listage quand la table est vide."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.fetchall.return_value = []

    # Act
    resultat = UtilisateurDAO.lister_tous()

    # Assert
    assert resultat == []
    cursor.execute.assert_called_once()
    args = cursor.execute.call_args[0]
    assert "SELECT * FROM utilisateur" in args[0]
    assert "ORDER BY id_utilisateur" in args[0]


@patch('dao.utilisateur_dao.DBConnection')
def test_lister_tous_un_utilisateur(mock_db, mock_connection):
    """Test le listage avec un seul utilisateur."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.fetchall.return_value = [
        {
            "id_utilisateur": 1,
            "nom": "Dupont",
            "prenom": "Jean",
            "email": "jean@test.com",
            "mot_de_passe": "hash123",
            "role": False,
            "created_at": "2024-01-15T10:30:00"
        }
    ]

    # Act
    resultat = UtilisateurDAO.lister_tous()

    # Assert
    assert len(resultat) == 1
    assert isinstance(resultat[0], Utilisateur)
    assert resultat[0].nom == "Dupont"
    assert resultat[0].email == "jean@test.com"


@patch('dao.utilisateur_dao.DBConnection')
def test_lister_tous_plusieurs_utilisateurs(mock_db, mock_connection):
    """Test le listage avec plusieurs utilisateurs."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.fetchall.return_value = [
        {
            "id_utilisateur": 1,
            "nom": "Dupont",
            "prenom": "Jean",
            "email": "jean@test.com",
            "mot_de_passe": "hash123",
            "role": False,
            "created_at": "2024-01-15T10:30:00"
        },
        {
            "id_utilisateur": 2,
            "nom": "Martin",
            "prenom": "Sophie",
            "email": "sophie@test.com",
            "mot_de_passe": "hash456",
            "role": True,
            "created_at": "2024-02-20T14:45:00"
        },
        {
            "id_utilisateur": 3,
            "nom": "Bernard",
            "prenom": "Pierre",
            "email": "pierre@test.com",
            "mot_de_passe": "hash789",
            "role": False,
            "created_at": "2024-03-10T09:15:00"
        }
    ]

    # Act
    resultat = UtilisateurDAO.lister_tous()

    # Assert
    assert len(resultat) == 3
    assert all(isinstance(u, Utilisateur) for u in resultat)
    assert resultat[0].id_utilisateur == 1
    assert resultat[1].role is True
    assert resultat[2].prenom == "Pierre"


# ============================================================
# TESTS SUPPRESSION
# ============================================================

@patch('dao.utilisateur_dao.DBConnection')
def test_supprimer_utilisateur_existant(mock_db, mock_connection):
    """Test la suppression d'un utilisateur existant."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.rowcount = 1

    # Act
    resultat = UtilisateurDAO.supprimer(5)

    # Assert
    assert resultat is True
    cursor.execute.assert_called_once()
    args = cursor.execute.call_args[0]
    assert "DELETE FROM utilisateur" in args[0]
    assert "WHERE id_utilisateur = %s" in args[0]
    assert args[1] == (5,)


@patch('dao.utilisateur_dao.DBConnection')
def test_supprimer_utilisateur_inexistant(mock_db, mock_connection):
    """Test la suppression d'un utilisateur qui n'existe pas."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.rowcount = 0

    # Act
    resultat = UtilisateurDAO.supprimer(999)

    # Assert
    assert resultat is False


# ============================================================
# TESTS GET_BY
# ============================================================

@patch('dao.utilisateur_dao.DBConnection')
def test_get_by_email_trouve(mock_db, mock_connection):
    """Test la recherche par email qui trouve un utilisateur."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.fetchall.return_value = [
        {
            "id_utilisateur": 1,
            "nom": "Dupont",
            "prenom": "Jean",
            "email": "jean@test.com",
            "mot_de_passe": "hash123",
            "role": False,
            "created_at": "2024-01-15T10:30:00"
        }
    ]

    dao = UtilisateurDAO()
    
    # Act
    resultat = dao.get_by("email", "jean@test.com")

    # Assert
    assert len(resultat) == 1
    assert resultat[0].email == "jean@test.com"
    cursor.execute.assert_called_once()
    args = cursor.execute.call_args[0]
    assert "WHERE email = %(value)s" in args[0]
    assert args[1] == {"value": "jean@test.com"}


@patch('dao.utilisateur_dao.DBConnection')
def test_get_by_id_utilisateur(mock_db, mock_connection):
    """Test la recherche par ID."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.fetchall.return_value = [
        {
            "id_utilisateur": 42,
            "nom": "Test",
            "prenom": "User",
            "email": "test@test.com",
            "mot_de_passe": "hash",
            "role": True,
            "created_at": "2024-01-01T00:00:00"
        }
    ]

    dao = UtilisateurDAO()
    
    # Act
    resultat = dao.get_by("id_utilisateur", 42)

    # Assert
    assert len(resultat) == 1
    assert resultat[0].id_utilisateur == 42


@patch('dao.utilisateur_dao.DBConnection')
def test_get_by_role(mock_db, mock_connection):
    """Test la recherche par rôle."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.fetchall.return_value = [
        {
            "id_utilisateur": 1,
            "nom": "Admin1",
            "prenom": "Super",
            "email": "admin1@test.com",
            "mot_de_passe": "hash1",
            "role": True,
            "created_at": "2024-01-01T00:00:00"
        },
        {
            "id_utilisateur": 2,
            "nom": "Admin2",
            "prenom": "Mega",
            "email": "admin2@test.com",
            "mot_de_passe": "hash2",
            "role": True,
            "created_at": "2024-01-02T00:00:00"
        }
    ]

    dao = UtilisateurDAO()
    
    # Act
    resultat = dao.get_by("role", True)

    # Assert
    assert len(resultat) == 2
    assert all(u.role is True for u in resultat)


@patch('dao.utilisateur_dao.DBConnection')
def test_get_by_aucun_resultat(mock_db, mock_connection):
    """Test la recherche qui ne trouve rien."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.fetchall.return_value = []

    dao = UtilisateurDAO()
    
    # Act
    resultat = dao.get_by("email", "inexistant@test.com")

    # Assert
    assert resultat == []


def test_get_by_colonne_non_autorisee():
    """Test qu'une ValueError est levée pour une colonne non autorisée."""
    # Arrange
    dao = UtilisateurDAO()
    
    # Act & Assert
    with pytest.raises(ValueError, match="Colonne 'sql_injection' non autorisée"):
        dao.get_by("sql_injection", "malicious_value")


def test_get_by_toutes_colonnes_autorisees():
    """Test que toutes les colonnes légitimes sont autorisées."""
    # Arrange
    dao = UtilisateurDAO()
    colonnes_valides = [
        "id_utilisateur",
        "nom",
        "prenom",
        "email",
        "mot_de_passe",
        "role",
        "created_at"
    ]

    # Act & Assert - Vérifier qu'aucune exception n'est levée pour les colonnes valides
    with patch('dao.utilisateur_dao.DBConnection') as mock_db:
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


@patch('dao.utilisateur_dao.DBConnection')
def test_get_by_nom_plusieurs_resultats(mock_db, mock_connection):
    """Test la recherche par nom qui retourne plusieurs homonymes."""
    # Arrange
    connection, cursor = mock_connection
    mock_db.return_value.connection = connection
    cursor.fetchall.return_value = [
        {
            "id_utilisateur": 1,
            "nom": "Dupont",
            "prenom": "Jean",
            "email": "jean.dupont@test.com",
            "mot_de_passe": "hash1",
            "role": False,
            "created_at": "2024-01-01T00:00:00"
        },
        {
            "id_utilisateur": 2,
            "nom": "Dupont",
            "prenom": "Marie",
            "email": "marie.dupont@test.com",
            "mot_de_passe": "hash2",
            "role": False,
            "created_at": "2024-01-02T00:00:00"
        }
    ]

    dao = UtilisateurDAO()
    
    # Act
    resultat = dao.get_by("nom", "Dupont")

    # Assert
    assert len(resultat) == 2
    assert all(u.nom == "Dupont" for u in resultat)
    assert resultat[0].prenom == "Jean"
    assert resultat[1].prenom == "Marie"