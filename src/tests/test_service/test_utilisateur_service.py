import pytest
from unittest.mock import MagicMock, patch
from service.utilisateur_service import UtilisateurService
from business_object.utilisateur import Utilisateur


@pytest.fixture
def mock_utilisateur():
    """Crée un utilisateur fictif pour les tests"""
    u = Utilisateur(
        id_utilisateur=1,
        pseudo="lucasrt2",
        nom="Repetti",
        prenom="Lucas",
        email="lucasrt@gmail.com",
        mot_de_passe="hash123",
        role=False
    )
    # On mock la méthode verify_password pour les tests d'authentification
    u.verify_password = MagicMock(return_value=True)
    return u


@pytest.fixture
def service():
    """Instancie le service avec DAO mocké"""
    service = UtilisateurService()
    service.utilisateur_dao = MagicMock()  # on mock la DAO entière
    return service


# ======================================================
# === TESTS DE CREATION DE COMPTE ======================
# ======================================================

def test_creer_compte_succes(service, mock_utilisateur):
    """Cas normal : création réussie"""
    service.utilisateur_dao.email_existe.return_value = False
    service.utilisateur_dao.pseudo_existe.return_value = False
    service.utilisateur_dao.creer.return_value = mock_utilisateur

    utilisateur = service.creer_compte("lucasrt2", "Repetti", "Lucas", "lucasrt@gmail.com", "motdepasse123")

    assert utilisateur is not None
    assert utilisateur.pseudo == "lucasrt2"
    service.utilisateur_dao.creer.assert_called_once()


def test_creer_compte_email_deja_pris(service):
    """Refus si email déjà utilisé"""
    service.utilisateur_dao.email_existe.return_value = True

    resultat = service.creer_compte("lucas", "Nom", "Prenom", "email@ex.com", "pwd")
    assert resultat is None
    service.utilisateur_dao.creer.assert_not_called()


def test_creer_compte_pseudo_deja_pris(service):
    """Refus si pseudo déjà pris"""
    service.utilisateur_dao.email_existe.return_value = False
    service.utilisateur_dao.pseudo_existe.return_value = True

    resultat = service.creer_compte("lucas", "Nom", "Prenom", "email@ex.com", "pwd")
    assert resultat is None
    service.utilisateur_dao.creer.assert_not_called()


# ======================================================
# === TESTS D'AUTHENTIFICATION =========================
# ======================================================

def test_authentifier_succes(service, mock_utilisateur):
    """Connexion réussie"""
    service.utilisateur_dao.trouver_par_email.return_value = mock_utilisateur
    utilisateur = service.authentifier("lucasrt@gmail.com", "motdepasse")
    assert utilisateur == mock_utilisateur
    mock_utilisateur.verify_password.assert_called_once_with("motdepasse")


def test_authentifier_email_inexistant(service):
    """Échec si aucun utilisateur trouvé"""
    service.utilisateur_dao.trouver_par_email.return_value = None
    resultat = service.authentifier("unknown@mail.com", "pwd")
    assert resultat is None


def test_authentifier_motdepasse_incorrect(service, mock_utilisateur):
    """Échec si mot de passe invalide"""
    mock_utilisateur.verify_password.return_value = False
    service.utilisateur_dao.trouver_par_email.return_value = mock_utilisateur
    resultat = service.authentifier("lucasrt@gmail.com", "faux")
    assert resultat is None


# ======================================================
# === TESTS LISTE DES UTILISATEURS =====================
# ======================================================

def test_lister_utilisateurs(service, mock_utilisateur):
    """Retourne la liste complète des utilisateurs"""
    service.utilisateur_dao.lister_tous.return_value = [mock_utilisateur]
    liste = service.lister_utilisateurs()
    assert len(liste) == 1
    assert liste[0].email == "lucasrt@gmail.com"


# ======================================================
# === TESTS SUPPRESSION ADMIN/NON ADMIN ================
# ======================================================

def test_supprimer_utilisateur_admin(service):
    """Test : Un administrateur peut supprimer un utilisateur."""
    # Arrange
    admin = Utilisateur(
        pseudo="admin",
        nom="Admin",
        prenom="Super",
        email="admin@test.com",
        mot_de_passe="password123",
        role=True  # ← Admin avec role=True
    )
    
    utilisateur_a_supprimer = Utilisateur(
        pseudo="user_to_delete",
        nom="User",
        prenom="Delete",
        email="delete@test.com",
        mot_de_passe="password123",
        role=False,
        id_utilisateur=1
    )
    
    # Mock du DAO
    service.utilisateur_dao.get_by_id.return_value = utilisateur_a_supprimer
    service.utilisateur_dao.supprimer.return_value = True
    
    # Act
    resultat = service.supprimer_utilisateur(admin, 1)
    
    # Assert
    assert resultat is True
    service.utilisateur_dao.get_by_id.assert_called_once_with(1)
    service.utilisateur_dao.supprimer.assert_called_once_with(1)


def test_supprimer_utilisateur_non_admin(service):
    """Refusé si l'utilisateur n'est pas admin"""
    non_admin = Utilisateur(
        pseudo="user",
        nom="User",
        prenom="Normal",
        email="user@test.com",
        mot_de_passe="password123",
        role=False  # ← Non-admin avec role=False
    )

    # Act
    resultat = service.supprimer_utilisateur(non_admin, 1)
    
    # Assert
    assert resultat is False
    service.utilisateur_dao.supprimer.assert_not_called()


def test_supprimer_utilisateur_inexistant(service):
    """Refus si l'utilisateur à supprimer n'existe pas"""
    admin = Utilisateur(
        id_utilisateur=99,
        pseudo="admin",
        nom="Root",
        prenom="Super",
        email="admin@example.com",
        mot_de_passe="hash",
        role=True  # ← Admin avec role=True
    )

    # Mock du DAO pour retourner None (utilisateur inexistant)
    service.utilisateur_dao.get_by_id.return_value = None
    
    # Act
    resultat = service.supprimer_utilisateur(admin, 123)
    
    # Assert
    assert resultat is False
    service.utilisateur_dao.get_by_id.assert_called_once_with(123)
    service.utilisateur_dao.supprimer.assert_not_called()