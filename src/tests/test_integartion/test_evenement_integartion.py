# tests/tests_integration/test_evenement_integration.py
import pytest
from datetime import date, timedelta, datetime
from decimal import Decimal

from business_object.evenement import Evenement
from business_object.utilisateur import Utilisateur
from business_object.inscription import Inscription
from dao.evenement_dao import EvenementDAO
from dao.utilisateur_dao import UtilisateurDAO
from dao.inscription_dao import InscriptionDAO
from dao.bus_dao import BusDAO
from service.evenement_service import EvenementService


# ============================================================
# FIXTURES POUR LES TESTS D'INTÉGRATION
# ============================================================

@pytest.fixture
def utilisateur_createur():
    """Crée un utilisateur en base pour créer des événements."""
    utilisateur = Utilisateur(
        nom="Martin",
        prenom="Jean",
        email="jean.martin@example.com",
        mot_de_passe="SecurePass123!"
    )
    UtilisateurDAO().creer(utilisateur)
    return utilisateur


@pytest.fixture
def utilisateur_participant():
    """Crée un utilisateur participant pour les inscriptions."""
    utilisateur = Utilisateur(
        nom="Dupont",
        prenom="Marie",
        email="marie.dupont@example.com",
        mot_de_passe="Password123!"
    )
    UtilisateurDAO().creer(utilisateur)
    return utilisateur


@pytest.fixture
def evenement_service():
    """Initialise le service événement avec toutes ses dépendances."""
    return EvenementService(
        evenement_dao=EvenementDAO(),
        inscription_dao=InscriptionDAO(),
        utilisateur_dao=UtilisateurDAO(),
        bus_dao=BusDAO()
    )


# ============================================================
# TESTS CRÉATION D'ÉVÉNEMENTS
# ============================================================

def test_creer_evenement_complet(evenement_service, utilisateur_createur):
    """
    Test d'intégration complet : créer un événement et vérifier
    qu'il est bien persisté en base avec tous ses attributs.
    """
    # Arrange
    date_future = date.today() + timedelta(days=30)
    
    # Act
    evenement = evenement_service.creer_evenement(
        titre="Concert de Jazz",
        lieu="Salle Pleyel",
        date_event=date_future,
        capacite_max=200,
        description_event="Soirée jazz avec musiciens professionnels",
        tarif=25.50,
        created_by=utilisateur_createur.id_utilisateur
    )
    
    # Assert
    assert evenement is not None
    assert evenement.id_event is not None  # ID auto-généré par PostgreSQL
    assert evenement.titre == "Concert de Jazz"
    assert evenement.lieu == "Salle Pleyel"
    assert evenement.capacite_max == 200
    assert evenement.tarif == Decimal("25.50")
    assert evenement.statut == "en_cours"
    assert evenement.created_by == utilisateur_createur.id_utilisateur
    
    # Vérifier que l'événement existe vraiment en base
    evenements_bd = EvenementDAO().get_by("id_event", evenement.id_event)
    assert len(evenements_bd) == 1
    assert evenements_bd[0].titre == "Concert de Jazz"


def test_creer_evenement_validations_business_object(evenement_service, utilisateur_createur):
    """
    Test que les validations du BusinessObject sont bien appliquées
    même via le service.
    """
    # Test : titre vide
    evenement = evenement_service.creer_evenement(
        titre="",
        lieu="Paris",
        date_event=date.today() + timedelta(days=10),
        capacite_max=100,
        created_by=utilisateur_createur.id_utilisateur
    )
    assert evenement is None
    
    # Test : capacité négative
    evenement = evenement_service.creer_evenement(
        titre="Événement",
        lieu="Paris",
        date_event=date.today() + timedelta(days=10),
        capacite_max=-10,
        created_by=utilisateur_createur.id_utilisateur
    )
    assert evenement is None


# ============================================================
# TESTS RÉCUPÉRATION D'ÉVÉNEMENTS
# ============================================================

def test_get_evenement_by_id(evenement_service, utilisateur_createur):
    """Test la récupération d'un événement par son ID."""
    # Arrange - Créer un événement
    evenement_cree = evenement_service.creer_evenement(
        titre="Festival Rock",
        lieu="Stade de France",
        date_event=date.today() + timedelta(days=60),
        capacite_max=50000,
        tarif=75.00,
        created_by=utilisateur_createur.id_utilisateur
    )
    
    # Act
    evenements = evenement_service.get_evenement_by("id_event", evenement_cree.id_event)
    
    # Assert
    assert len(evenements) == 1
    assert evenements[0].id_event == evenement_cree.id_event
    assert evenements[0].titre == "Festival Rock"


def test_get_evenements_by_created_by(evenement_service, utilisateur_createur):
    """Test la récupération de tous les événements d'un créateur."""
    # Arrange - Créer plusieurs événements
    evenement_service.creer_evenement(
        titre="Événement 1",
        lieu="Lieu 1",
        date_event=date.today() + timedelta(days=10),
        capacite_max=100,
        created_by=utilisateur_createur.id_utilisateur
    )
    evenement_service.creer_evenement(
        titre="Événement 2",
        lieu="Lieu 2",
        date_event=date.today() + timedelta(days=20),
        capacite_max=150,
        created_by=utilisateur_createur.id_utilisateur
    )
    
    # Act
    evenements = evenement_service.get_evenement_by(
        "created_by", 
        utilisateur_createur.id_utilisateur
    )
    
    # Assert
    assert len(evenements) == 2
    assert all(e.created_by == utilisateur_createur.id_utilisateur for e in evenements)





# ============================================================
# TESTS SUPPRESSION D'ÉVÉNEMENTS
# ============================================================

def test_supprimer_evenement_success(evenement_service, utilisateur_createur):
    """Test la suppression complète d'un événement."""
    # Arrange
    evenement = evenement_service.creer_evenement(
        titre="Événement à supprimer",
        lieu="Paris",
        date_event=date.today() + timedelta(days=30),
        capacite_max=100,
        created_by=utilisateur_createur.id_utilisateur
    )
    id_evenement = evenement.id_event
    
    # Act
    resultat = evenement_service.supprimer_evenement(id_evenement)
    
    # Assert
    assert resultat is True
    
    # Vérifier que l'événement n'existe plus en base
    evenements = evenement_service.get_evenement_by("id_event", id_evenement)
    assert len(evenements) == 0


# ============================================================
# TESTS MODIFICATION DE STATUT
# ============================================================

def test_modifier_statut_evenement_complet(
    evenement_service, 
    utilisateur_createur,
    utilisateur_participant
):
    """
    Test que le statut passe à 'complet' quand la capacité est atteinte.
    """
    from business_object.bus import Bus
    from business_object.inscription import Inscription
    from dao.bus_dao import BusDAO
    from dao.inscription_dao import InscriptionDAO
    from dao.utilisateur_dao import UtilisateurDAO
    from datetime import date, timedelta
    
    # Arrange - Créer un événement avec capacité = 2
    evenement = evenement_service.creer_evenement(
        titre="Petit événement",
        lieu="Salle",
        date_event=date.today() + timedelta(days=30),
        capacite_max=2,
        created_by=utilisateur_createur.id_utilisateur
    )
    
    # Créer 2 bus (aller et retour)
    bus_aller = Bus(
        id_event=evenement.id_event,
        sens="Aller",
        heure_depart="08:00",
        capacite_max=50,
        description="Bus aller"
    )
    bus_retour = Bus(
        id_event=evenement.id_event,
        sens="Retour",
        heure_depart="18:00",
        capacite_max=50,
        description="Bus retour"
    )
    bus_dao = BusDAO()
    bus_dao.creer(bus_aller)
    bus_dao.creer(bus_retour)
    
    # Créer 2ème participant
    participant2 = Utilisateur(
        nom="Durand",
        prenom="Paul",
        email="paul.durand@example.com",
        mot_de_passe="Pass123!"
    )
    UtilisateurDAO().creer(participant2)
    
    # Inscrire les 2 participants avec les bus
    inscription_dao = InscriptionDAO()
    inscription_dao.creer(Inscription(
        id_event=evenement.id_event,
        id_bus_aller=bus_aller.id_bus,
        id_bus_retour=bus_retour.id_bus,
        code_reservation=1001,
        created_by=utilisateur_participant.id_utilisateur,
        nom_event=evenement.titre
    ))
    inscription_dao.creer(Inscription(
        id_event=evenement.id_event,
        id_bus_aller=bus_aller.id_bus,
        id_bus_retour=bus_retour.id_bus,
        code_reservation=1002,
        created_by=participant2.id_utilisateur,
        nom_event=evenement.titre
    ))
    
    # Act
    resultat = evenement_service.modifier_statut(evenement.id_event)
    
    # Assert
    assert resultat is True
    
    # Vérifier le nouveau statut en base
    evenement_maj = evenement_service.get_evenement_by("id_event", evenement.id_event)[0]
    assert evenement_maj.statut == "complet"

def test_modifier_statut_evenement_passe(evenement_service, utilisateur_createur):
    """
    Test que le statut passe à 'passe' pour un événement dont la date
    est dépassée.
    """
    # Arrange - Créer un événement dans le passé
    date_passee = date.today() - timedelta(days=10)
    evenement = evenement_service.creer_evenement(
        titre="Événement passé",
        lieu="Paris",
        date_event=date_passee,
        capacite_max=100,
        created_by=utilisateur_createur.id_utilisateur
    )
    
    # Act
    resultat = evenement_service.modifier_statut(evenement.id_event)
    
    # Assert
    assert resultat is True
    
    # Vérifier le nouveau statut en base
    evenement_maj = evenement_service.get_evenement_by("id_event", evenement.id_event)[0]
    assert evenement_maj.statut == "passe"
