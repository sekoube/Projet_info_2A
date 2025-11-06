from business_object.utilisateur import Utilisateur
from dao.utilisateur_dao import UtilisateurDAO
from datetime import datetime


# ========================== Test DAO minimal ==========================




def test_creer_utilisateur_ok():
    # Arrange
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    utilisateur = Utilisateur(
        nom="Dao",
        prenom="Alex",
        pseudo=f"alexdao_{timestamp}",  # Pseudo unique
        email=f"alex.dao.{timestamp}@example.com",  # Email unique
        mot_de_passe="MotDePasse123!"
    )
    
    # Act
    utilisateur_cree = UtilisateurDAO().creer(utilisateur)
    
    # Assert
    assert utilisateur_cree is not None
    assert utilisateur_cree.id_utilisateur is not None


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

        # Vérifier que ValueError est levée
    with pytest.raises(ValueError, match="Un utilisateur avec l'email.*existe déjà"):
        UtilisateurDAO().creer(utilisateur2)

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
