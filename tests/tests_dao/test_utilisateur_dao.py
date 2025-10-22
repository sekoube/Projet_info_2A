import pytest
from datetime import datetime
import sys
import os

# Chemin du projet racine (2 niveaux au-dessus du fichier test)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_root)
from src.business_object.utilisateur import Utilisateur
from src.dao.utilisateur_dao import UtilisateurDAO
from src.dao.db_connection import DBConnection


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """
    Prépare la base pour les tests :
    - nettoie la table utilisateur
    """
    with DBConnection().connection as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM utilisateur;")
        conn.commit()
    yield
    # Nettoyage après tous les tests
    with DBConnection().connection as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM utilisateur;")
        conn.commit()

def test_creer_et_trouver_par_email():
    user = Utilisateur(
        pseudo="toto",
        nom="Dupont",
        prenom="Thomas",
        email="toto@example.com",
        mot_de_passe="motdepasse123",
        role=False,
        date_creation=datetime.now(),
    )
    user.set_password(user.mot_de_passe)

    # Création
    cree = UtilisateurDAO.creer(user)
    assert cree.id_utilisateur is not None

    # Recherche
    retrouve = UtilisateurDAO.trouver_par_email("toto@example.com")
    assert retrouve is not None
    assert retrouve.pseudo == "toto"
    assert retrouve.email == "toto@example.com"
    assert retrouve.verify_password("motdepasse123")

def test_trouver_tous():
    users = UtilisateurDAO.trouver_tous()
    assert isinstance(users, list)
    assert len(users) >= 1
    assert all(isinstance(u, Utilisateur) for u in users)

def test_supprimer_utilisateur():
    user = UtilisateurDAO.trouver_par_email("toto@example.com")
    assert user is not None

    supprime = UtilisateurDAO.supprimer(user.id_utilisateur)
    assert supprime is True

    retrouve = UtilisateurDAO.trouver_par_email("toto@example.com")
    assert retrouve is None
