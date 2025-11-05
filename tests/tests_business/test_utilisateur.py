import re
import pytest
from datetime import datetime
import sys
import os
from src.business_object.utilisateur import Utilisateur
# # Chemin du projet racine (2 niveaux au-dessus du fichier test)
# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
# sys.path.append(project_root)


# ========================== Tests de levée d'erreurs ==========================
@pytest.mark.parametrize(
    'params, erreur, message_erreur',
    [
        ({'pseudo': '', 'nom': 'LEROY', 'prenom': 'Marc', 'email': 'marc@gmail.com', 'mot_de_passe': '1234'},
         ValueError, "Le pseudo ne peut pas être vide"),
        ({'pseudo': 'marcler', 'nom': '', 'prenom': 'Marc', 'email': 'marc@gmail.com', 'mot_de_passe': '1234'},
         ValueError, "Le nom ne peut pas être vide"),
        ({'pseudo': 'marcler', 'nom': 'LEROY', 'prenom': '', 'email': 'marc@gmail.com', 'mot_de_passe': '1234'},
         ValueError, "Le prénom ne peut pas être vide"),
        ({'pseudo': 'marcler', 'nom': 'LEROY', 'prenom': 'Marc', 'email': 'marc@gmailcom', 'mot_de_passe': '1234'},
         ValueError, "L'adresse e-mail n'est pas valide"),
        ({'pseudo': 'marcler', 'nom': 'LEROY', 'prenom': 'Marc', 'email': 'marc@gmail.com', 'mot_de_passe': ''},
         ValueError, "Le mot de passe ne peut pas être vide"),
    ]
)
def test_utilisateur_erreurs(params, erreur, message_erreur):
    """Vérifie que les mauvaises valeurs lèvent les erreurs appropriées"""
    with pytest.raises(erreur, match=re.escape(message_erreur)):
        Utilisateur(**params)


# ========================== Tests de création valide ==========================
@pytest.mark.parametrize(
    'params',
    [
        {'pseudo': 'marcler', 'nom': 'LEROY', 'prenom': 'Marc', 'email': 'marc@example.com', 'mot_de_passe': '1234'},
        {'pseudo': 'franceber', 'nom': 'BERNARD', 'prenom': 'France', 'email': 'france.bernard@gmail.com', 'mot_de_passe': 'motdepasse', 'role': True},
    ]
)
def test_utilisateur_creation_valide(params):
    """Vérifie la création correcte des utilisateurs et l'assignation des attributs"""
    user = Utilisateur(**params)
    for key, value in params.items():
        assert getattr(user, key) == value
    # Vérifie que la date de création est bien un datetime
    assert isinstance(user.date_creation, datetime)


# ========================== Test de la méthode identite ==========================
@pytest.mark.parametrize(
    'pseudo, nom, prenom, resultat_attendu',
    [
        ('marcler', 'LEROY', 'Marc', 'Marc LEROY (marcler)'),
        ('franceber', 'BERNARD', 'France', 'France BERNARD (franceber)'),
    ]
)
def test_identite(pseudo, nom, prenom, resultat_attendu):
    """Vérifie le format retourné par identite()"""
    user = Utilisateur(pseudo=pseudo, nom=nom, prenom=prenom, email='test@mail.com', mot_de_passe='1234')
    assert user.identite() == resultat_attendu



# ========================== Test de la méthode email_valide ==========================
@pytest.mark.parametrize(
    'email, doit_reussir',
    [
        ('france@example.com', True),
        ('france.bernard@mail.com', True),
        ('france.com', False),
        ('', False),
    ]
)
def test_email_valide(email, doit_reussir):
    """Teste que la création d'un Utilisateur lève une erreur pour un email invalide"""
    if doit_reussir:
        # Ne doit PAS lever d'erreur
        user = Utilisateur(
            pseudo='x',
            nom='Y',
            prenom='Z',
            email=email,
            mot_de_passe='1234'
        )
        assert user.email == email
    else:
        # Doit lever une ValueError
        with pytest.raises(ValueError, match="L'adresse e-mail n'est pas valide"):
            Utilisateur(
                pseudo='x',
                nom='Y',
                prenom='Z',
                email=email,
                mot_de_passe='1234'
            )
# ========================== Test to_dict et from_dict ==========================


def test_to_dict_from_dict():
    """Vérifie la conversion d'un objet vers dict puis la recréation via from_dict"""
    user = Utilisateur(pseudo='franceber', nom='BERNARD', prenom='France', email='france@gmail.com', mot_de_passe='1234', role=True)
    user_dict = user.to_dict()

    # Vérifie que toutes les clés attendues sont présentes
    cle_attendus = ['id_utilisateur', 'pseudo', 'nom', 'prenom', 'email', 'mot_de_passe', 'role', 'date_creation']
    assert all(key in user_dict for key in cle_attendus)

    # Reconstruction de l'utilisateur depuis le dict
    new_user = Utilisateur.from_dict(user_dict)
    assert isinstance(new_user, Utilisateur)
    assert new_user.pseudo == user.pseudo
    assert new_user.nom == user.nom
    assert new_user.prenom == user.prenom
    assert new_user.email == user.email
    assert new_user.mot_de_passe == user.mot_de_passe
    assert new_user.role == user.role
    # Vérifie que la date de création est bien un datetime
    assert isinstance(new_user.date_creation, datetime)


# ========================== Test de la méthode __repr__ ==========================
@pytest.mark.parametrize(
    'pseudo, nom, prenom, role, resultat_attendu',
    [
        ('marcler', 'LEROY', 'Marc', False, '<Utilisateur #None - marcler (Participant)>'),
        ('franceber', 'BERNARD', 'France', True, '<Utilisateur #None - franceber (Admin)>'),
    ]
)
def test_repr(pseudo, nom, prenom, role, resultat_attendu):
    """Vérifie que __repr__ retourne le format attendu"""
    user = Utilisateur(pseudo=pseudo, nom=nom, prenom=prenom, email='test@mail.com', mot_de_passe='1234', role=role)
    assert repr(user) == resultat_attendu


# ========================== Test d'égalité entre utilisateurs ==========================
def test_egalite_utilisateurs():
    """Vérifie que deux utilisateurs avec mêmes attributs sont considérés 'égaux' si on compare les attributs"""
    user1 = Utilisateur(pseudo='marcler', nom='LEROY', prenom='Marc', email='marc@gmail.com', mot_de_passe='1234')
    user2 = Utilisateur(pseudo='marcler', nom='LEROY', prenom='Marc', email='marc@gmail.com', mot_de_passe='1234')
    user3 = Utilisateur(pseudo='franceber', nom='BERNARD', prenom='France', email='france@gmail.com', mot_de_passe='abcd')

    # Comparaison "manuelle" des attributs
    assert all(getattr(user1, attr) == getattr(user2, attr) for attr in ['pseudo', 'nom', 'prenom', 'email', 'mot_de_passe', 'role'])
    assert not all(getattr(user1, attr) == getattr(user3, attr) for attr in ['pseudo', 'nom', 'prenom', 'email', 'mot_de_passe', 'role'])
