# import os
# import pytest
# from unittest.mock import patch

# from utils.reset_database import ResetDatabase
# from business_object.utilisateur import Utilisateur
# from dao.utilisateur_dao import UtilisateurDAO


# @pytest.fixture(scope="session", autouse=True)
# def setup_test_environment():
#     """Initialisation du schéma de test"""
#     with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
#         ResetDatabase().lancer(test_dao=True)
#         yield


# def test_creer_utilisateur_ok():
#     """Création d'un utilisateur réussie"""

#     # GIVEN
#     utilisateur = Utilisateur(
#         pseudo="test_user",
#         nom="Durand",
#         prenom="Alex",
#         mail="alex.durand@example.com",
#         mot_de_passe="azerty123",
#     )

#     # WHEN
#     creation_ok = UtilisateurDAO().creer(utilisateur)

#     # THEN
#     assert creation_ok
#     assert utilisateur.id_utilisateur is not None


# def test_creer_utilisateur_ko():
#     """Création échouée (mail ou pseudo invalide)"""

#     # GIVEN
#     utilisateur = Utilisateur(
#         pseudo="",  # pseudo vide → invalide
#         nom="Test",
#         prenom="User",
#         mail="mail_invalide",  # mauvais format
#         mot_de_passe="1234",
#     )

#     # WHEN
#     creation_ok = UtilisateurDAO().creer(utilisateur)

#     # THEN
#     assert not creation_ok


# if __name__ == "__main__":
#     pytest.main([__file__])


import os
import pytest
from business_object.utilisateur import Utilisateur
from dao.utilisateur_dao import UtilisateurDAO
from dao.db_connection import DBConnection

# ========================== Test DAO minimal ==========================


def test_creer_utilisateur_ok():
    """Vérifie qu'on peut créer un utilisateur valide dans la base"""
    # GIVEN
    utilisateur = Utilisateur(
        pseudo="testuser_dao",
        nom="Durand",
        prenom="Alex",
        email="alex.dao@example.com",
        mot_de_passe="azerty123"
    )

    # WHEN
    utilisateur_cree = UtilisateurDAO().creer(utilisateur)

    # THEN
    assert utilisateur_cree is not None
    assert utilisateur.id_utilisateur is not None


def test_creer_utilisateur_ko_email_existe():
    """Vérifie que la création échoue si l'email existe déjà"""
    # GIVEN
    utilisateur1 = Utilisateur(
        pseudo="user1",
        nom="Dupont",
        prenom="Jean",
        email="dupont@example.com",
        mot_de_passe="mdp123"
    )
    UtilisateurDAO().creer(utilisateur1)

    utilisateur2 = Utilisateur(
        pseudo="user2",
        nom="Martin",
        prenom="Paul",
        email="dupont@example.com",  # même email que le premier
        mot_de_passe="mdp456"
    )

    # WHEN
    email_existe = UtilisateurDAO().email_existe(utilisateur2.email)

    # THEN
    assert email_existe is True

def test_creer_utilisateur_ko_pseudo_existe():
    """Vérifie que la création échoue si le pseudo existe déjà"""
    # GIVEN
    utilisateur1 = Utilisateur(
        pseudo="pseudo_test",
        nom="Dupont",
        prenom="Jean",
        email="unique1@example.com",
        mot_de_passe="mdp123"
    )
    UtilisateurDAO().creer(utilisateur1)

    utilisateur2 = Utilisateur(
        pseudo="pseudo_test",  # même pseudo que le premier
        nom="Martin",
        prenom="Paul",
        email="unique2@example.com",
        mot_de_passe="mdp456"
    )

    # WHEN
    pseudo_existe = UtilisateurDAO().pseudo_existe(utilisateur2.pseudo)

    # THEN
    assert pseudo_existe is True
