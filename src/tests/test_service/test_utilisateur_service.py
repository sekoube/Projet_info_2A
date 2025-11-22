import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
from business_object.utilisateur import Utilisateur
from service.utilisateur_service import UtilisateurService
from utils.mdp import hash_password


@pytest.fixture
def service():
    """Fixture pour créer une instance de UtilisateurService avec DAO mockée."""
    service = UtilisateurService()
    service.utilisateur_dao = Mock()
    return service


@pytest.fixture
def utilisateur_participant():
    """Fixture pour un utilisateur participant standard."""
    return Utilisateur(
        id_utilisateur=1,
        nom="Dupont",
        prenom="Jean",
        email="jean.dupont@test.com",
        mot_de_passe="hashed_password_123",
        role=False,
        created_at=datetime.now()
    )


@pytest.fixture
def utilisateur_admin():
    """Fixture pour un utilisateur administrateur."""
    return Utilisateur(
        id_utilisateur=2,
        nom="Martin",
        prenom="Sophie",
        email="sophie.martin@test.com",
        mot_de_passe="hashed_password_456",
        role=True,
        created_at=datetime.now()
    )


# ============================================================
# TESTS CRÉATION D'UTILISATEUR
# ============================================================

def test_creer_utilisateur_success(service):
    """Test la création réussie d'un utilisateur."""
    # Arrange
    service.utilisateur_dao.get_by.return_value = []  # Email non utilisé
    nouvel_utilisateur = Utilisateur(
        id_utilisateur=5,
        nom="Nouveau",
        prenom="User",
        email="nouveau@test.com",
        mot_de_passe="hashed_pwd",
        role=False
    )
    service.utilisateur_dao.creer.return_value = nouvel_utilisateur

    # Act
    with patch('service.utilisateur_service.hash_password', return_value="hashed_pwd"):
        resultat = service.creer_utilisateur(
            nom="Nouveau",
            prenom="User",
            email="nouveau@test.com",
            mot_de_passe="password123",
            role=False
        )

    # Assert
    assert resultat is not None
    assert resultat.nom == "Nouveau"
    assert resultat.email == "nouveau@test.com"
    service.utilisateur_dao.creer.assert_called_once()


def test_creer_utilisateur_email_deja_utilise(service, utilisateur_participant):
    """Test la création échoue si l'email est déjà pris."""
    # Arrange
    service.utilisateur_dao.get_by.return_value = [utilisateur_participant]

    # Act
    resultat = service.creer_utilisateur(
        nom="Autre",
        prenom="Personne",
        email="jean.dupont@test.com",  # Email déjà utilisé
        mot_de_passe="password123"
    )

    # Assert
    assert resultat is None
    service.utilisateur_dao.creer.assert_not_called()


def test_creer_utilisateur_role_admin(service):
    """Test la création d'un utilisateur avec rôle administrateur."""
    # Arrange
    service.utilisateur_dao.get_by.return_value = []
    admin = Utilisateur(
        id_utilisateur=10,
        nom="Admin",
        prenom="Super",
        email="admin@test.com",
        mot_de_passe="hashed_pwd",
        role=True
    )
    service.utilisateur_dao.creer.return_value = admin

    # Act
    with patch('service.utilisateur_service.hash_password', return_value="hashed_pwd"):
        resultat = service.creer_utilisateur(
            nom="Admin",
            prenom="Super",
            email="admin@test.com",
            mot_de_passe="securepass",
            role=True
        )

    # Assert
    assert resultat is not None
    assert resultat.is_admin is True


def test_creer_utilisateur_echec_dao(service):
    """Test le cas où la DAO échoue lors de la création."""
    # Arrange
    service.utilisateur_dao.get_by.return_value = []
    service.utilisateur_dao.creer.return_value = None

    # Act
    with patch('service.utilisateur_service.hash_password', return_value="hashed_pwd"):
        resultat = service.creer_utilisateur(
            nom="Test",
            prenom="User",
            email="test@test.com",
            mot_de_passe="password"
        )

    # Assert
    assert resultat is None


# ============================================================
# TESTS AUTHENTIFICATION
# ============================================================


def test_authentifier_success(service, utilisateur_participant):
    """Test l'authentification réussie d'un utilisateur."""

    # Arrange
    utilisateur_participant.mot_de_passe = hash_password("password123")
    service.utilisateur_dao.get_by.return_value = [utilisateur_participant]

    # Act
    resultat = service.authentifier("jean.dupont@test.com", "password123")

    # Assert
    assert resultat is not None
    assert resultat.email == "jean.dupont@test.com"
    service.utilisateur_dao.get_by.assert_called_once_with('email', 'jean.dupont@test.com')





# ============================================================
# TESTS LISTAGE
# ============================================================

def test_lister_utilisateurs_vide(service):
    """Test le listage quand aucun utilisateur n'existe."""
    # Arrange
    service.utilisateur_dao.lister_tous.return_value = []

    # Act
    resultat = service.lister_utilisateurs()

    # Assert
    assert resultat == []
    assert len(resultat) == 0


def test_lister_utilisateurs_plusieurs(service, utilisateur_participant, utilisateur_admin):
    """Test le listage avec plusieurs utilisateurs."""
    # Arrange
    service.utilisateur_dao.lister_tous.return_value = [
        utilisateur_participant,
        utilisateur_admin
    ]

    # Act
    resultat = service.lister_utilisateurs()

    # Assert
    assert len(resultat) == 2
    assert resultat[0].email == "jean.dupont@test.com"
    assert resultat[1].email == "sophie.martin@test.com"


# ============================================================
# TESTS SUPPRESSION
# ============================================================

def test_supprimer_utilisateur_par_admin_success(service, utilisateur_admin, utilisateur_participant):
    """Test la suppression réussie par un admin."""
    # Arrange
    service.utilisateur_dao.get_by_id.return_value = utilisateur_participant
    service.utilisateur_dao.supprimer.return_value = True

    # Act
    resultat = service.supprimer_utilisateur(utilisateur_admin, 1)

    # Assert
    assert resultat is True
    service.utilisateur_dao.supprimer.assert_called_once_with(1)


def test_supprimer_utilisateur_non_admin_refuse(service, utilisateur_participant):
    """Test qu'un participant ne peut pas supprimer d'utilisateur."""
    # Arrange - Aucun mock nécessaire, le test échoue avant d'accéder à la DAO

    # Act
    resultat = service.supprimer_utilisateur(utilisateur_participant, 2)

    # Assert
    assert resultat is False
    service.utilisateur_dao.supprimer.assert_not_called()


def test_supprimer_utilisateur_inexistant(service, utilisateur_admin):
    """Test la suppression d'un utilisateur qui n'existe pas."""
    # Arrange
    service.utilisateur_dao.get_by_id.return_value = None

    # Act
    resultat = service.supprimer_utilisateur(utilisateur_admin, 999)

    # Assert
    assert resultat is False
    service.utilisateur_dao.supprimer.assert_not_called()


def test_supprimer_utilisateur_echec_dao(service, utilisateur_admin, utilisateur_participant):
    """Test le cas où la DAO échoue lors de la suppression."""
    # Arrange
    service.utilisateur_dao.get_by_id.return_value = utilisateur_participant
    service.utilisateur_dao.supprimer.return_value = False

    # Act
    resultat = service.supprimer_utilisateur(utilisateur_admin, 1)

    # Assert
    assert resultat is False


# ============================================================
# TESTS GET_UTILISATEUR_BY
# ============================================================

def test_get_utilisateur_by_email(service, utilisateur_participant):
    """Test la récupération d'un utilisateur par email."""
    # Arrange
    service.utilisateur_dao.get_by.return_value = [utilisateur_participant]

    # Act
    resultat = service.get_utilisateur_by('email', 'jean.dupont@test.com')

    # Assert
    assert resultat is not None
    assert len(resultat) == 1
    assert resultat[0].email == "jean.dupont@test.com"


def test_get_utilisateur_by_id(service, utilisateur_admin):
    """Test la récupération d'un utilisateur par ID."""
    # Arrange
    service.utilisateur_dao.get_by.return_value = [utilisateur_admin]

    # Act
    resultat = service.get_utilisateur_by('id_utilisateur', 2)

    # Assert
    assert resultat is not None
    assert resultat[0].id_utilisateur == 2


def test_get_utilisateur_by_champ_invalide(service):
    """Test qu'une exception est levée pour un champ non autorisé."""
    # Arrange
    service.utilisateur_dao.get_by.side_effect = ValueError("Colonne 'invalid_field' non autorisée.")

    # Act & Assert
    with pytest.raises(ValueError, match="non autorisée"):
        service.get_utilisateur_by('invalid_field', 'value')


def test_get_utilisateur_by_aucun_resultat(service):
    """Test la recherche qui ne retourne aucun résultat."""
    # Arrange
    service.utilisateur_dao.get_by.return_value = []

    # Act
    resultat = service.get_utilisateur_by('email', 'inconnu@test.com')

    # Assert
    assert resultat == []