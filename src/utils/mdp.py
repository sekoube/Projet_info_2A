"Gère le hachage et la vérification des mots de passe"
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHash

# Initialisation du hasher Argon2
ph = PasswordHasher(
    time_cost=3,       # nombre d’itérations
    memory_cost=65536, # mémoire utilisée (en KB) → 64 Mo
    parallelism=4,     # nombre de threads
    hash_len=32,       # longueur du hash généré
    salt_len=16        # taille du sel aléatoire
)


def hash_password(plain_password: str) -> str:
    """
    Hache un mot de passe en utilisant Argon2.
    Retourne une chaîne sécurisée pour le stockage en BDD.
    """
    return ph.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifie si le mot de passe correspond au hash stocké.
    Retourne True si valide, False sinon.
    """
    try:
        return ph.verify(hashed_password, plain_password)
    except (VerifyMismatchError, VerificationError, InvalidHash):
        return False
