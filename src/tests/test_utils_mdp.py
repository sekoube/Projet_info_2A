import pytest
from datetime import datetime
from utils.mdp import hash_password, verify_password
from business_object.utilisateur import Utilisateur


# ==================== TESTS DES FONCTIONS UTILITAIRES ====================

def test_hash_password_returns_different_string():
    """Vérifie que le hash est différent du mot de passe en clair"""
    pwd = "monSecret123"
    hashed = hash_password(pwd)
    assert hashed != pwd
    assert len(hashed) > len(pwd)


def test_hash_password_generates_unique_hashes():
    """Vérifie que deux hachages du même mot de passe donnent des résultats différents (sel aléatoire)"""
    pwd = "monSecret123"
    hash1 = hash_password(pwd)
    hash2 = hash_password(pwd)
    assert hash1 != hash2  # Argon2 utilise un sel aléatoire


def test_verify_password_with_correct_password():
    """Vérifie qu'un mot de passe correct est validé"""
    pwd = "monSecret123"
    hashed = hash_password(pwd)
    assert verify_password(pwd, hashed) is True


def test_verify_password_with_incorrect_password():
    """Vérifie qu'un mauvais mot de passe est rejeté"""
    pwd = "monSecret123"
    hashed = hash_password(pwd)
    assert verify_password("mauvais", hashed) is False


def test_verify_password_with_empty_password():
    """Vérifie le comportement avec un mot de passe vide"""
    hashed = hash_password("test")
    assert verify_password("", hashed) is False


def test_verify_password_with_invalid_hash():
    """Vérifie que verify_password retourne False pour un hash invalide"""
    assert verify_password("test", "invalid_hash_string") is False
    assert verify_password("test", "") is False


def test_hash_password_with_special_characters():
    """Vérifie le hachage de mots de passe avec caractères spéciaux"""
    pwd = "P@ssw0rd!#$%&*()_+-=[]{}|;:',.<>?/~`"
    hashed = hash_password(pwd)
    assert verify_password(pwd, hashed) is True


def test_hash_password_with_unicode_characters():
    """Vérifie le hachage avec des caractères Unicode"""
    pwd = "Mot_de_passe_français_éàç_🔒"
    hashed = hash_password(pwd)
    assert verify_password(pwd, hashed) is True


# ==================== TESTS DE LA CLASSE UTILISATEUR ====================

def test_utilisateur_creation_valid():
    """Teste la création d'un utilisateur valide"""
    user = Utilisateur(
        nom="Dupont",
        prenom="Jean",
        email="jean.dupont@example.com",
        mot_de_passe="password123",
        role=False
    )
    assert user.nom == "Dupont"
    assert user.prenom == "Jean"
    assert user.email == "jean.dupont@example.com"
    assert user.role is False
    assert isinstance(user.created_at, datetime)


def test_utilisateur_set_password():
    """Teste la méthode set_password qui hache le mot de passe"""
    user = Utilisateur(
        nom="Dupont",
        prenom="Jean",
        email="jean@test.com",
        mot_de_passe="temp"  # Mot de passe temporaire
    )
    
    user.set_password("supersecret")
    
    # Le mot de passe stocké doit être haché
    assert user.mot_de_passe != "supersecret"
    assert len(user.mot_de_passe) > 20  # Un hash Argon2 est long


def test_utilisateur_verify_password_correct():
    """Vérifie qu'un mot de passe correct est validé"""
    user = Utilisateur(
        nom="Dupont",
        prenom="Jean",
        email="jean@test.com",
        mot_de_passe="temp"
    )
    user.set_password("supersecret")
    
    assert user.verify_password("supersecret") is True


def test_utilisateur_verify_password_incorrect():
    """Vérifie qu'un mauvais mot de passe est rejeté"""
    user = Utilisateur(
        nom="Dupont",
        prenom="Jean",
        email="jean@test.com",
        mot_de_passe="temp"
    )
    user.set_password("supersecret")
    
    assert user.verify_password("autre") is False
    assert user.verify_password("SuperSecret") is False  # Sensible à la casse
    assert user.verify_password("") is False


def test_utilisateur_password_workflow():
    """Teste le workflow complet de gestion du mot de passe"""
    user = Utilisateur(
        nom="Martin",
        prenom="Sophie",
        email="sophie.martin@test.com",
        mot_de_passe="initial_pwd"
    )
    
    # Définir un nouveau mot de passe
    user.set_password("nouveau_mdp_123")
    assert user.verify_password("nouveau_mdp_123") is True
    assert user.verify_password("initial_pwd") is False
    
    # Changer de mot de passe
    user.set_password("encore_plus_secure!")
    assert user.verify_password("encore_plus_secure!") is True
    assert user.verify_password("nouveau_mdp_123") is False


# ==================== TESTS DE VALIDATION ====================

def test_utilisateur_nom_vide_raises_error():
    """Vérifie qu'un nom vide lève une erreur"""
    with pytest.raises(ValueError, match="Le nom ne peut pas être vide"):
        Utilisateur(
            nom="",
            prenom="Jean",
            email="jean@test.com",
            mot_de_passe="pwd"
        )


def test_utilisateur_nom_whitespace_raises_error():
    """Vérifie qu'un nom avec uniquement des espaces lève une erreur"""
    with pytest.raises(ValueError, match="Le nom ne peut pas être vide"):
        Utilisateur(
            nom="   ",
            prenom="Jean",
            email="jean@test.com",
            mot_de_passe="pwd"
        )


def test_utilisateur_prenom_vide_raises_error():
    """Vérifie qu'un prénom vide lève une erreur"""
    with pytest.raises(ValueError, match="Le prénom ne peut pas être vide"):
        Utilisateur(
            nom="Dupont",
            prenom="",
            email="jean@test.com",
            mot_de_passe="pwd"
        )


def test_utilisateur_email_invalide_raises_error():
    """Vérifie qu'un email invalide lève une erreur"""
    with pytest.raises(ValueError, match="L'adresse e-mail n'est pas valide"):
        Utilisateur(
            nom="Dupont",
            prenom="Jean",
            email="email_invalide",
            mot_de_passe="pwd"
        )


def test_utilisateur_email_sans_arobase_raises_error():
    """Vérifie qu'un email sans @ lève une erreur"""
    with pytest.raises(ValueError, match="L'adresse e-mail n'est pas valide"):
        Utilisateur(
            nom="Dupont",
            prenom="Jean",
            email="email.example.com",
            mot_de_passe="pwd"
        )


def test_utilisateur_email_sans_domaine_raises_error():
    """Vérifie qu'un email sans domaine lève une erreur"""
    with pytest.raises(ValueError, match="L'adresse e-mail n'est pas valide"):
        Utilisateur(
            nom="Dupont",
            prenom="Jean",
            email="email@",
            mot_de_passe="pwd"
        )


def test_utilisateur_mot_de_passe_vide_raises_error():
    """Vérifie qu'un mot de passe vide lève une erreur"""
    with pytest.raises(ValueError, match="Le mot de passe ne peut pas être vide"):
        Utilisateur(
            nom="Dupont",
            prenom="Jean",
            email="jean@test.com",
            mot_de_passe=""
        )


def test_set_password_vide_raises_error():
    """Vérifie que set_password refuse un mot de passe vide"""
    user = Utilisateur(
        nom="Dupont",
        prenom="Jean",
        email="jean@test.com",
        mot_de_passe="initial"
    )
    
    with pytest.raises(ValueError, match="Le mot de passe ne peut pas être vide"):
        user.set_password("")


def test_set_password_whitespace_raises_error():
    """Vérifie que set_password refuse un mot de passe avec uniquement des espaces"""
    user = Utilisateur(
        nom="Dupont",
        prenom="Jean",
        email="jean@test.com",
        mot_de_passe="initial"
    )
    
    with pytest.raises(ValueError, match="Le mot de passe ne peut pas être vide"):
        user.set_password("   ")


# ==================== TESTS DES PROPRIÉTÉS ====================

def test_is_admin_property_true():
    """Vérifie la propriété is_admin pour un administrateur"""
    admin = Utilisateur(
        nom="Admin",
        prenom="Super",
        email="admin@test.com",
        mot_de_passe="pwd",
        role=True
    )
    assert admin.is_admin is True


def test_is_admin_property_false():
    """Vérifie la propriété is_admin pour un participant"""
    user = Utilisateur(
        nom="User",
        prenom="Normal",
        email="user@test.com",
        mot_de_passe="pwd",
        role=False
    )
    assert user.is_admin is False


def test_str_method():
    """Vérifie la méthode __str__"""
    user = Utilisateur(
        nom="Dupont",
        prenom="Jean",
        email="jean@test.com",
        mot_de_passe="pwd"
    )
    assert str(user) == "Jean Dupont"


def test_repr_method():
    """Vérifie la méthode __repr__"""
    user = Utilisateur(
        id_utilisateur=42,
        nom="Dupont",
        prenom="Jean",
        email="jean@test.com",
        mot_de_passe="pwd",
        role=False
    )
    assert repr(user) == "<Utilisateur #42 - (Participant)>"
    
    admin = Utilisateur(
        id_utilisateur=1,
        nom="Admin",
        prenom="Super",
        email="admin@test.com",
        mot_de_passe="pwd",
        role=True
    )
    assert repr(admin) == "<Utilisateur #1 - (Admin)>"


# ==================== TESTS DE SÉRIALISATION ====================

def test_to_dict():
    """Vérifie la conversion d'un utilisateur en dictionnaire"""
    user = Utilisateur(
        id_utilisateur=10,
        nom="Dupont",
        prenom="Jean",
        email="jean@test.com",
        mot_de_passe="hashed_password",
        role=False
    )
    
    result = user.to_dict()
    
    assert result["id_utilisateur"] == 10
    assert result["nom"] == "Dupont"
    assert result["prenom"] == "Jean"
    assert result["email"] == "jean@test.com"
    assert result["mot_de_passe"] == "hashed_password"
    assert result["role"] is False
    assert "created_at" in result
    assert isinstance(result["created_at"], str)  # ISO format


def test_from_dict():
    """Vérifie la création d'un utilisateur depuis un dictionnaire"""
    data = {
        "id_utilisateur": 15,
        "nom": "Martin",
        "prenom": "Sophie",
        "email": "sophie@test.com",
        "mot_de_passe": "hashed_pwd",
        "role": True,
        "created_at": "2024-01-15T10:30:00"
    }
    
    user = Utilisateur.from_dict(data)
    
    assert user.id_utilisateur == 15
    assert user.nom == "Martin"
    assert user.prenom == "Sophie"
    assert user.email == "sophie@test.com"
    assert user.mot_de_passe == "hashed_pwd"
    assert user.role is True
    assert isinstance(user.created_at, datetime)




# ==================== TESTS D'INTÉGRATION ====================

def test_integration_complete_user_lifecycle():
    """Test d'intégration du cycle de vie complet d'un utilisateur"""
    # 1. Création
    user_data = {
        "nom": "Legrand",
        "prenom": "Paul",
        "email": "paul.legrand@example.com",
        "mot_de_passe": "temp",
        "role": False
    }
    user = Utilisateur(**user_data)
    
    # 2. Définition du mot de passe sécurisé
    user.set_password("Mon_P@ssw0rd_Sécurisé!")
    
    # 3. Vérification du mot de passe
    assert user.verify_password("Mon_P@ssw0rd_Sécurisé!") is True
    
    # 4. Sérialisation
    user_dict = user.to_dict()
    assert user_dict["email"] == "paul.legrand@example.com"
    
    # 5. Désérialisation
    user_reloaded = Utilisateur.from_dict(user_dict)
    
    # 6. Le mot de passe haché doit toujours fonctionner
    assert user_reloaded.verify_password("Mon_P@ssw0rd_Sécurisé!") is True
    assert user_reloaded.verify_password("mauvais") is False
