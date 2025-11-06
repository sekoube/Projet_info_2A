from business_object.utilisateur import Utilisateur
from dao.utilisateur_dao import UtilisateurDAO


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
