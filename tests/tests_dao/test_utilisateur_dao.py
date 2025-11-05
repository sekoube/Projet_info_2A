import os
import pytest
from unittest.mock import patch

from utils.reset_database import ResetDatabase
from business_object.utilisateur import Utilisateur
from dao.utilisateur_dao import UtilisateurDAO


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation du schéma de test"""
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield


def test_creer_utilisateur_ok():
    """Création d'un utilisateur réussie"""

    # GIVEN
    utilisateur = Utilisateur(
        pseudo="test_user",
        nom="Durand",
        prenom="Alex",
        mail="alex.durand@example.com",
        mot_de_passe="azerty123",
    )

    # WHEN
    creation_ok = UtilisateurDAO().creer(utilisateur)

    # THEN
    assert creation_ok
    assert utilisateur.id_utilisateur is not None


def test_creer_utilisateur_ko():
    """Création échouée (mail ou pseudo invalide)"""

    # GIVEN
    utilisateur = Utilisateur(
        pseudo="",  # pseudo vide → invalide
        nom="Test",
        prenom="User",
        mail="mail_invalide",  # mauvais format
        mot_de_passe="1234",
    )

    # WHEN
    creation_ok = UtilisateurDAO().creer(utilisateur)

    # THEN
    assert not creation_ok


if __name__ == "__main__":
    pytest.main([__file__])
