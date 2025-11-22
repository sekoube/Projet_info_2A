# tests/conftest.py
import sys
import pytest
from pathlib import Path
import uuid

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
    Nettoie AVANT chaque test pour garantir une base vierge.
    Cela garantit que chaque test part d'une base clean.
    """
    # AVANT le test - nettoyage
    try:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                # L'ordre est important : on commence par les tables dépendantes
                cursor.execute("TRUNCATE TABLE projet.inscription RESTART IDENTITY CASCADE;")
                cursor.execute("TRUNCATE TABLE projet.bus RESTART IDENTITY CASCADE;")
                cursor.execute("TRUNCATE TABLE projet.evenement RESTART IDENTITY CASCADE;")
                cursor.execute("TRUNCATE TABLE projet.utilisateur RESTART IDENTITY CASCADE;")
                connection.commit()
    except Exception as e:
        print(f"⚠️  Erreur lors du nettoyage initial des tables : {e}")
    
    yield  # Le test s'exécute ici
    
    # APRÈS le test - nettoyage optionnel (par sécurité)
    try:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute("TRUNCATE TABLE projet.inscription RESTART IDENTITY CASCADE;")
                cursor.execute("TRUNCATE TABLE projet.bus RESTART IDENTITY CASCADE;")
                cursor.execute("TRUNCATE TABLE projet.evenement RESTART IDENTITY CASCADE;")
                cursor.execute("TRUNCATE TABLE projet.utilisateur RESTART IDENTITY CASCADE;")
                connection.commit()
    except Exception as e:
        print(f"⚠️  Erreur lors du nettoyage final des tables : {e}")


@pytest.fixture
def unique_email():
    """Génère un email unique pour éviter les conflits."""
    return f"test_{uuid.uuid4().hex[:8]}@example.com"


@pytest.fixture
def utilisateur_createur(unique_email):
    """Crée un utilisateur en base pour créer des événements."""
    from business_object.utilisateur import Utilisateur
    from dao.utilisateur_dao import UtilisateurDAO
    
    utilisateur = Utilisateur(
        nom="Martin",
        prenom="Jean",
        email=unique_email,  # Email unique
        mot_de_passe="SecurePass123!"
    )
    UtilisateurDAO().creer(utilisateur)
    return utilisateur


@pytest.fixture
def utilisateur_participant(unique_email):
    """Crée un utilisateur participant pour les inscriptions."""
    from business_object.utilisateur import Utilisateur
    from dao.utilisateur_dao import UtilisateurDAO
    
    utilisateur = Utilisateur(
        nom="Dupont",
        prenom="Marie",
        email=unique_email,  # Email unique
        mot_de_passe="Password123!"
    )
    UtilisateurDAO().creer(utilisateur)
    return utilisateur


@pytest.fixture
def evenement_service():
    """Initialise le service événement avec toutes ses dépendances."""
    from service.evenement_service import EvenementService
    from dao.evenement_dao import EvenementDAO
    from dao.utilisateur_dao import UtilisateurDAO
    from dao.inscription_dao import InscriptionDAO
    from dao.bus_dao import BusDAO
    
    return EvenementService(
        evenement_dao=EvenementDAO(),
        inscription_dao=InscriptionDAO(),
        utilisateur_dao=UtilisateurDAO(),
        bus_dao=BusDAO()
    )


@pytest.fixture
def utilisateur_test(unique_email):
    """
    Fixture pour créer un utilisateur de test.
    Utile pour les tests qui ont besoin d'un utilisateur existant.
    """
    from business_object.utilisateur import Utilisateur
    from dao.utilisateur_dao import UtilisateurDAO
    
    utilisateur = Utilisateur(
        nom="Test",
        prenom="User",
        email=unique_email,
        mot_de_passe="Password123!"
    )
    UtilisateurDAO().creer(utilisateur)
    return utilisateur


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