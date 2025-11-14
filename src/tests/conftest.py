# tests/conftest.py
import sys
import pytest
from pathlib import Path

# Ajouter src au PYTHONPATH pour tous les tests
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Maintenant on peut importer depuis src
from utils.reset_database import ResetDatabase
from dao.db_connection import DBConnection


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Réinitialise complètement la base de données une seule fois 
    au début de la session de tests.
    """
    print("\n🔄 Initialisation de la base de données de test...")
    ResetDatabase().lancer(test_dao=False)
    print("✅ Base de données initialisée\n")
    yield
    print("\n🧹 Session de tests terminée")


@pytest.fixture(scope="function", autouse=True)
def clean_tables():
    """
    Nettoie toutes les tables après chaque test individuel.
    Cela garantit que chaque test part d'une base vierge.
    """
    yield  # Le test s'exécute ici
    
    # Après chaque test, on vide les tables dans le bon ordre (CASCADE gère les dépendances)
    try:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                # L'ordre est important : on commence par les tables dépendantes
                cursor.execute("TRUNCATE TABLE projet.inscription RESTART IDENTITY CASCADE;")
                cursor.execute("TRUNCATE TABLE projet.bus RESTART IDENTITY CASCADE;")
                cursor.execute("TRUNCATE TABLE projet.evenement RESTART IDENTITY CASCADE;")
                cursor.execute("TRUNCATE TABLE projet.administrateur RESTART IDENTITY CASCADE;")
                cursor.execute("TRUNCATE TABLE projet.utilisateur RESTART IDENTITY CASCADE;")
    except Exception as e:
        print(f"⚠️  Erreur lors du nettoyage des tables : {e}")


@pytest.fixture
def utilisateur_test():
    """
    Fixture pour créer un utilisateur de test.
    Utile pour les tests qui ont besoin d'un utilisateur existant.
    """
    from business_object.utilisateur import Utilisateur
    from dao.utilisateur_dao import UtilisateurDAO
    
    utilisateur = Utilisateur(
        pseudo="testuser",
        nom="Test",
        prenom="User",
        email="test@example.com",
        mot_de_passe="Password123!"
    )
    return UtilisateurDAO().creer(utilisateur)


@pytest.fixture
def evenement_test(utilisateur_test):
    """
    Fixture pour créer un événement de test.
    Dépend de utilisateur_test pour avoir un créateur valide.
    """
    from business_object.evenement import Evenement
    from dao.evenement_dao import EvenementDAO
    from datetime import date, timedelta
    
    evenement = Evenement(
        titre="Événement Test",
        description_event="Description de test",
        lieu="Lieu Test",
        date_event=date.today() + timedelta(days=30),
        capacite_max=100,
        created_by=utilisateur_test.id_utilisateur,
        tarif=10.0
    )
    EvenementDAO().creer(evenement)
    return evenement