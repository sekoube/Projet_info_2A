from utils.mdp import hash_password, verify_password
from business_objet.utilisateur import Utilisateur

# **************** test sur la fonction de base ******************* #


def test_hash_and_verify_password():
    pwd = "monSecret123"
    hashed = hash_password(pwd)
    assert hashed != pwd
    assert verify_password(pwd, hashed)
    assert not verify_password("mauvais", hashed)

# **************** test sur l'appel dans la couche métier  *************************


def test_set_and_verify_password():
    user = Utilisateur(
        pseudo="test",
        nom="Dupont",
        prenom="Jean",
        email="jean@test.com",
        mot_de_passe="fake"  # sera écrasé
    )
    user.set_password("supersecret")
    assert user.verify_password("supersecret")
    assert not user.verify_password("autre")
