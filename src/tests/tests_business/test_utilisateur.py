import re
import pytest
from datetime import datetime
from src.business_object.utilisateur import Utilisateur


# ========================== Tests de levée d'erreurs ==========================
@pytest.mark.parametrize(
    'params, erreur, message_erreur',
    [
        # SUPPRIMÉ: Test sur pseudo vide (n'existe pas dans votre code)
        ({'nom': '', 'prenom': 'Marc', 'email': 'marc@gmail.com', 'mot_de_passe': '1234'},
         ValueError, "Le nom ne peut pas être vide"),
        ({'nom': 'LEROY', 'prenom': '', 'email': 'marc@gmail.com', 'mot_de_passe': '1234'},
         ValueError, "Le prénom ne peut pas être vide"),
        ({'nom': 'LEROY', 'prenom': 'Marc', 'email': 'marc@gmailcom', 'mot_de_passe': '1234'},
         ValueError, "L'adresse e-mail n'est pas valide"),
        ({'nom': 'LEROY', 'prenom': 'Marc', 'email': 'marc@gmail.com', 'mot_de_passe': ''},
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
        {'nom': 'LEROY', 'prenom': 'Marc', 'email': 'marc@example.com', 'mot_de_passe': '1234'},
        {'nom': 'BERNARD', 'prenom': 'France', 'email': 'france.bernard@gmail.com', 'mot_de_passe': 'motdepasse', 'role': True},
    ]
)
def test_utilisateur_creation_valide(params):
    """Vérifie la création correcte des utilisateurs et l'assignation des attributs"""
    user = Utilisateur(**params)
    for key, value in params.items():
        assert getattr(user, key) == value
    # Vérifie que la date de création est bien un datetime
    assert isinstance(user.created_at, datetime)  # MODIFIÉ: date_creation -> created_at


# ========================== Test de la méthode __str__ ==========================
@pytest.mark.parametrize(
    'nom, prenom, resultat_attendu',
    [
        ('LEROY', 'Marc', 'Marc LEROY'),  # MODIFIÉ: Sans pseudo
        ('BERNARD', 'France', 'France BERNARD'),  # MODIFIÉ: Sans pseudo
    ]
)
def test_str_format(nom, prenom, resultat_attendu):  # RENOMMÉ: identite -> str_format
    """Vérifie le format retourné par __str__()"""
    user = Utilisateur(nom=nom, prenom=prenom, email='test@mail.com', mot_de_passe='1234')
    assert str(user) == resultat_attendu  # MODIFIÉ: identite() -> str()


# ========================== Test de la validation d'email ==========================
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
                nom='Y',
                prenom='Z',
                email=email,
                mot_de_passe='1234'
            )


# ========================== Test to_dict et from_dict ==========================
def test_to_dict_from_dict():
    """Vérifie la conversion d'un objet vers dict puis la recréation via from_dict"""
    user = Utilisateur(nom='BERNARD', prenom='France', email='france@gmail.com', mot_de_passe='1234', role=True)
    user_dict = user.to_dict()

    # Vérifie que toutes les clés attendues sont présentes
    cle_attendus = ['id_utilisateur', 'nom', 'prenom', 'email', 'mot_de_passe', 'role', 'created_at']  # MODIFIÉ: enlevé pseudo, date_creation -> created_at
    assert all(key in user_dict for key in cle_attendus)

    # Reconstruction de l'utilisateur depuis le dict
    new_user = Utilisateur.from_dict(user_dict)
    assert isinstance(new_user, Utilisateur)
    assert new_user.nom == user.nom
    assert new_user.prenom == user.prenom
    assert new_user.email == user.email
    assert new_user.mot_de_passe == user.mot_de_passe
    assert new_user.role == user.role
    # Vérifie que la date de création est bien un datetime
    assert isinstance(new_user.created_at, datetime)  # MODIFIÉ: date_creation -> created_at


# ========================== Test de la méthode __repr__ ==========================
@pytest.mark.parametrize(
    'nom, prenom, role, resultat_attendu',
    [
        ('LEROY', 'Marc', False, '<Utilisateur #None - (Participant)>'),  # MODIFIÉ: Sans pseudo
        ('BERNARD', 'France', True, '<Utilisateur #None - (Admin)>'),  # MODIFIÉ: Sans pseudo
    ]
)
def test_repr(nom, prenom, role, resultat_attendu):
    """Vérifie que __repr__ retourne le format attendu"""
    user = Utilisateur(nom=nom, prenom=prenom, email='test@mail.com', mot_de_passe='1234', role=role)
    assert repr(user) == resultat_attendu


# ========================== Test d'égalité entre utilisateurs ==========================
def test_egalite_utilisateurs():
    """Vérifie que deux utilisateurs avec mêmes attributs sont considérés 'égaux' si on compare les attributs"""
    user1 = Utilisateur(nom='LEROY', prenom='Marc', email='marc@gmail.com', mot_de_passe='1234')
    user2 = Utilisateur(nom='LEROY', prenom='Marc', email='marc@gmail.com', mot_de_passe='1234')
    user3 = Utilisateur(nom='BERNARD', prenom='France', email='france@gmail.com', mot_de_passe='abcd')

    # Comparaison "manuelle" des attributs (MODIFIÉ: enlevé pseudo)
    assert all(getattr(user1, attr) == getattr(user2, attr) for attr in ['nom', 'prenom', 'email', 'mot_de_passe', 'role'])
    assert not all(getattr(user1, attr) == getattr(user3, attr) for attr in ['nom', 'prenom', 'email', 'mot_de_passe', 'role'])


# ========================== Test de la propriété is_admin ==========================
def test_is_admin_property():
    """Vérifie que la propriété is_admin fonctionne correctement"""
    admin = Utilisateur(nom='ADMIN', prenom='Super', email='admin@test.com', mot_de_passe='1234', role=True)
    user = Utilisateur(nom='USER', prenom='Normal', email='user@test.com', mot_de_passe='1234', role=False)
    
    assert admin.is_admin is True
    assert user.is_admin is False


# ========================== Test des méthodes de mot de passe ==========================
def test_set_and_verify_password():
    """Vérifie que set_password et verify_password fonctionnent correctement"""
    user = Utilisateur(nom='TEST', prenom='User', email='test@test.com', mot_de_passe='initial')
    
    # Change le mot de passe
    user.set_password('nouveau_mdp')
    
    # Vérifie que le nouveau mot de passe fonctionne
    assert user.verify_password('nouveau_mdp') is True
    
    # Vérifie que l'ancien ne fonctionne plus
    assert user.verify_password('initial') is False
    
    # Vérifie qu'un mauvais mot de passe ne fonctionne pas
    assert user.verify_password('mauvais') is False


def test_set_password_vide():
    """Vérifie que set_password lève une erreur si le mot de passe est vide"""
    user = Utilisateur(nom='TEST', prenom='User', email='test@test.com', mot_de_passe='initial')
    
    with pytest.raises(ValueError, match="Le mot de passe ne peut pas être vide"):
        user.set_password('')
    
    with pytest.raises(ValueError, match="Le mot de passe ne peut pas être vide"):
        user.set_password('   ')  # Espaces uniquement