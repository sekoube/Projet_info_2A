from datetime import date
from unittest.mock import Mock
from Projet_info_2A.src.service.evenement_service import EvenementService
from Projet_info_2A.src.business_object.evenement import Evenement
from Projet_info_2A.src.business_object.inscription import Inscription
from Projet_info_2A.src.dao.evenement_dao import EvenementDao

def test_creer_evenement_succes():
    """
    Test de création d'un événement via le service.
    Vérifie que l'événement est créé et persisté correctement.
    """
    # Arrange - Créer des mocks pour les DAO
    evenement_dao_mock = Mock()
    evenement_dao_mock.creer.return_value = True
    
    inscription_dao_mock = Mock()
    utilisateur_dao_mock = Mock()
    bus_dao_mock = Mock()
    
    service = EvenementService(
        evenement_dao_mock,
        inscription_dao_mock,
        utilisateur_dao_mock,
        bus_dao_mock
    )
    
    # Act
    resultat = service.creer_evenement(
        titre="Festival de Musique",
        lieu="Parc Central",
        date_evenement=date(2025, 7, 15),
        capacite_max=500,
        created_by=1,
        description_evenement="Grand festival d'été",
        tarif=25.00
    )
    
    # Assert
    assert resultat is not None
    assert resultat.titre == "Festival de Musique"
    assert evenement_dao_mock.creer.called


def test_inscrire_utilisateur_evenement_complet():
    """
    Test d'inscription à un événement complet.
    Vérifie que l'inscription est refusée quand la capacité est atteinte.
    """
    # Arrange
    evenement_dao_mock = Mock()
    evenement = Evenement(
        id_event=1,
        titre="Atelier Complet",
        lieu="Salle 101",
        date_evenement=date(2025, 12, 1),
        capacite_max=2,
        created_by=1
    )
    # Simuler un événement avec 2 inscriptions (complet)
    evenement.inscriptions = [Mock(), Mock()]
    evenement_dao_mock.get_by_id.return_value = evenement
    
    inscription_dao_mock = Mock()
    inscription_dao_mock.get_by_event.return_value = evenement.inscriptions
    
    utilisateur_dao_mock = Mock()
    utilisateur_mock = Mock()
    utilisateur_mock.nom = "Dupont"
    utilisateur_mock.prenom = "Jean"
    utilisateur_dao_mock.get_by_id.return_value = utilisateur_mock
    
    bus_dao_mock = Mock()
    
    service = EvenementService(
        evenement_dao_mock,
        inscription_dao_mock,
        utilisateur_dao_mock,
        bus_dao_mock
    )
    
    # Act
    resultat = service.inscrire_utilisateur(
        id_event=1,
        id_utilisateur=3,
        boit=False,
        mode_paiement="cb"
    )
    
    # Assert
    assert resultat is False
    assert not inscription_dao_mock.creer.called


def test_inscrire_utilisateur_succes():
    """
    Test d'inscription réussie à un événement disponible.
    Vérifie que l'inscription est créée correctement.
    """
    # Arrange
    evenement_dao_mock = Mock()
    evenement = Evenement(
        id_event=1,
        titre="Conférence Tech",
        lieu="Auditorium",
        date_evenement=date(2025, 11, 20),
        capacite_max=100,
        created_by=1
    )
    evenement.inscriptions = []  # Événement vide
    evenement_dao_mock.get_by_id.return_value = evenement
    
    inscription_dao_mock = Mock()
    inscription_dao_mock.get_by_event.return_value = []
    inscription_dao_mock.creer.return_value = True
    
    utilisateur_dao_mock = Mock()
    utilisateur_mock = Mock()
    utilisateur_mock.nom = "Martin"
    utilisateur_mock.prenom = "Sophie"
    utilisateur_dao_mock.get_by_id.return_value = utilisateur_mock
    
    bus_dao_mock = Mock()
    
    service = EvenementService(
        evenement_dao_mock,
        inscription_dao_mock,
        utilisateur_dao_mock,
        bus_dao_mock
    )
    
    # Act
    resultat = service.inscrire_utilisateur(
        id_event=1,
        id_utilisateur=5,
        boit=True,
        mode_paiement="espèce"
    )
    
    # Assert
    assert resultat is True
    assert inscription_dao_mock.creer.called


def test_get_evenements_disponibles():
    """
    Test de récupération des événements disponibles.
    Vérifie que seuls les événements futurs et non complets sont retournés.
    """
    # Arrange
    evenement_dao_mock = Mock()
    
    # Événement futur disponible
    evt_dispo = Evenement(
        id_event=1,
        titre="Événement Disponible",
        lieu="Centre",
        date_evenement=date(2026, 1, 15),
        capacite_max=50,
        created_by=1
    )
    evt_dispo.inscriptions = []
    
    # Événement futur complet
    evt_complet = Evenement(
        id_event=2,
        titre="Événement Complet",
        lieu="Salle B",
        date_evenement=date(2026, 2, 20),
        capacite_max=10,
        created_by=1
    )
    evt_complet.inscriptions = [Mock() for _ in range(10)]
    
    # Événement passé
    evt_passe = Evenement(
        id_event=3,
        titre="Événement Passé",
        lieu="Musée",
        date_evenement=date(2020, 5, 10),
        capacite_max=30,
        created_by=1
    )
    
    evenement_dao_mock.lister_tous.return_value = [evt_dispo, evt_complet, evt_passe]
    
    inscription_dao_mock = Mock()
    inscription_dao_mock.get_by_event.side_effect = lambda id_event: {
        1: [],
        2: [Mock() for _ in range(10)],
        3: []
    }[id_event]
    
    utilisateur_dao_mock = Mock()
    bus_dao_mock = Mock()
    
    service = EvenementService(
        evenement_dao_mock,
        inscription_dao_mock,
        utilisateur_dao_mock,
        bus_dao_mock
    )
    
    # Act
    evenements_dispo = service.get_evenements_disponibles()
    
    # Assert
    assert len(evenements_dispo) == 1
    assert evenements_dispo[0].titre == "Événement Disponible"


def test_desinscrire_utilisateur_non_inscrit():
    """
    Test de désinscription d'un utilisateur non inscrit.
    Vérifie que la désinscription échoue si l'utilisateur n'est pas inscrit.
    """
    # Arrange
    evenement_dao_mock = Mock()
    evenement = Evenement(
        id_event=1,
        titre="Soirée Théâtre",
        lieu="Théâtre Municipal",
        date_evenement=date(2025, 12, 10),
        capacite_max=100,
        created_by=1
    )
    evenement_dao_mock.get_by_id.return_value = evenement
    
    inscription_dao_mock = Mock()
    # Utilisateur 5 n'est pas dans la liste des inscrits
    inscription_mock = Mock()
    inscription_mock.id_utilisateur = 3
    inscription_dao_mock.get_by_event.return_value = [inscription_mock]
    
    utilisateur_dao_mock = Mock()
    utilisateur_mock = Mock()
    utilisateur_mock.nom = "Durand"
    utilisateur_mock.prenom = "Marie"
    utilisateur_dao_mock.get_by_id.return_value = utilisateur_mock
    
    bus_dao_mock = Mock()
    
    service = EvenementService(
        evenement_dao_mock,
        inscription_dao_mock,
        utilisateur_dao_mock,
        bus_dao_mock
    )
    
    # Act
    resultat = service.desinscrire_utilisateur(id_event=1, id_utilisateur=5)
    
    # Assert
    assert resultat is False
    assert not inscription_dao_mock.delete.called

def test_creer_inscription_utilisateur_inexistant():
    """
    Teste la création d'inscription avec un utilisateur qui n'existe pas.
    Vérifie que l'inscription est refusée et retourne None.
    """
    # Arrange
    service = InscriptionService()
    
    # Mock du DAO utilisateur : utilisateur introuvable
    service.utilisateur_dao.trouver_par_id = Mock(return_value=None)
    
    # Mock des autres DAO
    service.evenement_dao.trouver_par_id = Mock()
    service.inscription_dao.compter_par_evenement = Mock()
    
    # Act
    resultat = service.creer_inscription(
        boit=True,
        created_by=999,  # ID utilisateur inexistant
        mode_paiement="cb",
        id_event="1",
        nom_event="Concert Rock"
    )
    
    # Assert
    assert resultat is None
    assert service.utilisateur_dao.trouver_par_id.called
    assert not service.inscription_dao.creer.called


def test_creer_inscription_evenement_inexistant():
    """
    Teste la création d'inscription pour un événement inexistant.
    Vérifie que l'inscription est refusée et retourne None.
    """
    # Arrange
    service = InscriptionService()
    
    # Mock du DAO utilisateur : utilisateur existe
    utilisateur_mock = Mock()
    utilisateur_mock.id_utilisateur = 1
    service.utilisateur_dao.trouver_par_id = Mock(return_value=utilisateur_mock)
    
    # Mock du DAO événement : événement introuvable
    service.evenement_dao.trouver_par_id = Mock(return_value=None)
    
    # Mock des autres DAO
    service.inscription_dao.compter_par_evenement = Mock()
    
    # Act
    resultat = service.creer_inscription(
        boit=False,
        created_by=1,
        mode_paiement="espèce",
        id_event="999",  # ID événement inexistant
        nom_event="Événement Fantôme"
    )
    
    # Assert
    assert resultat is None
    assert service.evenement_dao.trouver_par_id.called
    assert not service.inscription_dao.creer.called

