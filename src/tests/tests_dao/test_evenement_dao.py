# src/tests/tests_dao/test_evenement_dao.py
from datetime import date, timedelta
from dao.evenement_dao import EvenementDAO
from business_object.evenement import Evenement
import pytest


# ==================== TESTS DE CRÉATION ====================

def test_creer_evenement_succes(utilisateur_test):
    """Test la création d'un événement avec succès"""
    evenement = Evenement(
        titre="Concert Test",
        lieu="Paris",
        date_evenement=date.today() + timedelta(days=30),
        capacite_max=100,
        created_by=utilisateur_test.id_utilisateur,
        description_evenement="Description du concert test",
        tarif=10.0
    )
    
    resultat = EvenementDAO().creer(evenement)
    assert resultat is True
    assert evenement.id_event is not None  # Vérifie que l'ID a été généré


# ==================== TESTS DE RÉCUPÉRATION ====================

def test_get_by_id_existant(utilisateur_test):
    """Test la récupération d'un événement existant"""
    evenement = Evenement(
        titre="Concert Test",
        lieu="Paris",
        date_evenement=date.today() + timedelta(days=30),
        capacite_max=100,
        created_by=utilisateur_test.id_utilisateur,
        description_evenement="Description du concert test",
        tarif=10.0
    )
    EvenementDAO().creer(evenement)
    
    evenement_recupere = EvenementDAO().get_by_id(evenement.id_event)
    assert evenement_recupere is not None
    assert evenement_recupere.titre == "Concert Test"
    assert evenement_recupere.lieu == "Paris"
    assert evenement_recupere.capacite_max == 100
    assert float(evenement_recupere.tarif) == 10.0


def test_get_by_id_inexistant():
    """Test la récupération d'un événement inexistant"""
    evenement_recupere = EvenementDAO().get_by_id(99999)
    assert evenement_recupere is None


# ==================== TESTS DE LISTAGE ====================

def test_lister_tous_avec_plusieurs_evenements(utilisateur_test):
    """Test le listage de plusieurs événements"""
    # Créer 3 événements
    for i in range(3):
        evenement = Evenement(
            titre=f"Événement {i+1}",
            lieu=f"Lieu {i+1}",
            date_evenement=date.today() + timedelta(days=10+i*10),
            capacite_max=100,
            created_by=utilisateur_test.id_utilisateur,
            description_evenement=f"Description {i+1}",
            tarif=10.0 * (i+1)
        )
        EvenementDAO().creer(evenement)
    
    evenements = EvenementDAO().lister_tous()
    assert len(evenements) == 3


def test_lister_futurs_evenements(utilisateur_test):
    """Test la récupération des événements futurs uniquement"""
    # Créer un événement futur
    evenement_futur = Evenement(
        titre="Concert Futur",
        lieu="Paris",
        date_evenement=date.today() + timedelta(days=10),
        capacite_max=100,
        created_by=utilisateur_test.id_utilisateur,
        description_evenement="Concert dans le futur",
        tarif=10.0
    )
    EvenementDAO().creer(evenement_futur)
    
    # Créer un événement passé
    evenement_passe = Evenement(
        titre="Concert Passé",
        lieu="Lyon",
        date_evenement=date.today() - timedelta(days=10),
        capacite_max=100,
        created_by=utilisateur_test.id_utilisateur,
        description_evenement="Concert passé",
        tarif=10.0
    )
    EvenementDAO().creer(evenement_passe)
    
    # Lister les événements futurs
    evenements_futurs = EvenementDAO().lister_futurs()
    
    # Vérifier qu'on a bien que les événements futurs
    assert len(evenements_futurs) >= 1
    for evt in evenements_futurs:
        assert evt.date_evenement >= date.today()


def test_lister_par_createur(utilisateur_test):
    """Test le listage des événements par créateur"""
    # Créer 2 événements pour l'utilisateur de test
    for i in range(2):
        evenement = Evenement(
            titre=f"Mon Événement {i+1}",
            lieu=f"Lieu {i+1}",
            date_evenement=date.today() + timedelta(days=10+i*10),
            capacite_max=100,
            created_by=utilisateur_test.id_utilisateur,
            description_evenement=f"Description {i+1}",
            tarif=10.0
        )
        EvenementDAO().creer(evenement)
    
    # Lister les événements de cet utilisateur
    evenements = EvenementDAO().lister_par_createur(utilisateur_test.id_utilisateur)
    
    assert len(evenements) == 2
    for evt in evenements:
        assert evt.created_by == utilisateur_test.id_utilisateur


# ==================== TESTS DE MODIFICATION ====================

def test_modifier_evenement_succes(utilisateur_test):
    """Test la modification d'un événement"""
    # Créer un événement
    evenement = Evenement(
        titre="Titre Original",
        lieu="Lieu Original",
        date_evenement=date.today() + timedelta(days=30),
        capacite_max=100,
        created_by=utilisateur_test.id_utilisateur,
        description_evenement="Description originale",
        tarif=10.0
    )
    EvenementDAO().creer(evenement)
    
    # Modifier l'événement
    evenement.titre = "Titre Modifié"
    evenement.lieu = "Nouveau Lieu"
    evenement.capacite_max = 200
    evenement.tarif = 15.0
    
    resultat = EvenementDAO().modifier(evenement)
    assert resultat is True
    
    # Vérifier les modifications
    evenement_recupere = EvenementDAO().get_by_id(evenement.id_event)
    assert evenement_recupere.titre == "Titre Modifié"
    assert evenement_recupere.lieu == "Nouveau Lieu"
    assert evenement_recupere.capacite_max == 200
    assert float(evenement_recupere.tarif) == 15.0


def test_modifier_date_evenement(utilisateur_test):
    """Test la modification de la date d'un événement"""
    evenement = Evenement(
        titre="Événement Report",
        lieu="Paris",
        date_evenement=date.today() + timedelta(days=30),
        capacite_max=100,
        created_by=utilisateur_test.id_utilisateur,
        description_evenement="Événement qui sera reporté",
        tarif=10.0
    )
    EvenementDAO().creer(evenement)
    
    # Reporter l'événement de 30 jours
    nouvelle_date = date.today() + timedelta(days=60)
    evenement.date_evenement = nouvelle_date
    
    resultat = EvenementDAO().modifier(evenement)
    assert resultat is True
    
    evenement_recupere = EvenementDAO().get_by_id(evenement.id_event)
    assert evenement_recupere.date_evenement == nouvelle_date


# ==================== TESTS DE SUPPRESSION ====================

def test_supprimer_evenement_succes(utilisateur_test):
    """Test la suppression d'un événement"""
    evenement = Evenement(
        titre="Événement à Supprimer",
        lieu="Paris",
        date_evenement=date.today() + timedelta(days=30),
        capacite_max=100,
        created_by=utilisateur_test.id_utilisateur,
        description_evenement="Sera supprimé",
        tarif=10.0
    )
    EvenementDAO().creer(evenement)
    id_event = evenement.id_event
    
    # Supprimer l'événement
    resultat = EvenementDAO().supprimer(evenement)
    assert resultat is True
    
    # Vérifier que l'événement n'existe plus
    evenement_recupere = EvenementDAO().get_by_id(id_event)
    assert evenement_recupere is None

def test_supprimer_puis_recreer(utilisateur_test):
    """Test la suppression puis recréation d'un événement avec le même titre"""
    evenement1 = Evenement(
        titre="Événement Récurrent",
        lieu="Paris",
        date_evenement=date.today() + timedelta(days=30),
        capacite_max=100,
        created_by=utilisateur_test.id_utilisateur,
        description_evenement="Première édition",
        tarif=10.0
    )
    EvenementDAO().creer(evenement1)
    id_premier = evenement1.id_event
    
    # Supprimer
    EvenementDAO().supprimer(evenement1)
    
    # Recréer avec le même titre
    evenement2 = Evenement(
        titre="Événement Récurrent",
        lieu="Paris",
        date_evenement=date.today() + timedelta(days=60),
        capacite_max=100,
        created_by=utilisateur_test.id_utilisateur,
        description_evenement="Deuxième édition",
        tarif=10.0
    )
    EvenementDAO().creer(evenement2)
    
    # Vérifier que ce sont deux événements différents
    assert evenement2.id_event != id_premier


# ==================== TESTS D'ORDRE ET DE TRI ====================

def test_lister_tous_ordre_decroissant(utilisateur_test):
    """Test que lister_tous retourne les événements par date décroissante"""
    dates = [
        date.today() + timedelta(days=10),
        date.today() + timedelta(days=30),
        date.today() + timedelta(days=20)
    ]
    
    for i, d in enumerate(dates):
        evenement = Evenement(
            titre=f"Événement {i+1}",
            lieu="Paris",
            date_evenement=d,
            capacite_max=100,
            created_by=utilisateur_test.id_utilisateur,
            description_evenement=f"Description {i+1}",
            tarif=10.0
        )
        EvenementDAO().creer(evenement)
    
    evenements = EvenementDAO().lister_tous()
    
    # Vérifier l'ordre décroissant (le plus récent d'abord)
    for i in range(len(evenements) - 1):
        assert evenements[i].date_evenement >= evenements[i+1].date_evenement


def test_lister_futurs_ordre_croissant(utilisateur_test):
    """Test que lister_futurs retourne les événements par date croissante"""
    dates = [
        date.today() + timedelta(days=30),
        date.today() + timedelta(days=10),
        date.today() + timedelta(days=20)
    ]
    
    for i, d in enumerate(dates):
        evenement = Evenement(
            titre=f"Événement Futur {i+1}",
            lieu="Paris",
            date_evenement=d,
            capacite_max=100,
            created_by=utilisateur_test.id_utilisateur,
            description_evenement=f"Description {i+1}",
            tarif=10.0
        )
        EvenementDAO().creer(evenement)
    
    evenements = EvenementDAO().lister_futurs()
    
    # Vérifier l'ordre croissant (le plus proche d'abord)
    for i in range(len(evenements) - 1):
        assert evenements[i].date_evenement <= evenements[i+1].date_evenement


# ==================== TESTS DE SCENARIOS COMPLEXES ====================

def test_scenario_complet_cycle_vie_evenement(utilisateur_test):
    """Test du cycle de vie complet d'un événement"""
    # 1. Création
    evenement = Evenement(
        titre="Événement Complet",
        lieu="Rennes",
        date_evenement=date.today() + timedelta(days=30),
        capacite_max=100,
        created_by=utilisateur_test.id_utilisateur,
        description_evenement="Test cycle de vie",
        tarif=20.0
    )
    
    assert EvenementDAO().creer(evenement) is True
    id_event = evenement.id_event
    
    # 2. Lecture
    evt_lu = EvenementDAO().get_by_id(id_event)
    assert evt_lu is not None
    assert evt_lu.titre == "Événement Complet"
    
    # 3. Modification
    evt_lu.titre = "Événement Modifié"
    evt_lu.capacite_max = 150
    assert EvenementDAO().modifier(evt_lu) is True
    
    # 4. Vérification modification
    evt_modifie = EvenementDAO().get_by_id(id_event)
    assert evt_modifie.titre == "Événement Modifié"
    assert evt_modifie.capacite_max == 150
    
    # 5. Suppression
    assert EvenementDAO().supprimer(evt_modifie) is True
    
    # 6. Vérification suppression
    evt_supprime = EvenementDAO().get_by_id(id_event)
    assert evt_supprime is None


def test_plusieurs_utilisateurs_creent_evenements(utilisateur_test):
    """Test avec plusieurs utilisateurs créant des événements"""
    from dao.utilisateur_dao import UtilisateurDAO
    from business_object.utilisateur import Utilisateur
    
    # Créer un deuxième utilisateur
    utilisateur2 = Utilisateur(
        pseudo="testuser2",
        nom="Test2",
        prenom="User2",
        email="test2@example.com",
        mot_de_passe="Password123!"
    )
    UtilisateurDAO().creer(utilisateur2)
    
    # Chaque utilisateur crée un événement
    evt1 = Evenement(
        titre="Événement User1",
        lieu="Paris",
        date_evenement=date.today() + timedelta(days=10),
        capacite_max=100,
        created_by=utilisateur_test.id_utilisateur,
        description_evenement="Par user 1",
        tarif=10.0
    )
    EvenementDAO().creer(evt1)
    
    evt2 = Evenement(
        titre="Événement User2",
        lieu="Lyon",
        date_evenement=date.today() + timedelta(days=20),
        capacite_max=100,
        created_by=utilisateur2.id_utilisateur,
        description_evenement="Par user 2",
        tarif=15.0
    )
    EvenementDAO().creer(evt2)
    
    # Vérifier que chaque utilisateur voit bien ses événements
    evts_user1 = EvenementDAO().lister_par_createur(utilisateur_test.id_utilisateur)
    evts_user2 = EvenementDAO().lister_par_createur(utilisateur2.id_utilisateur)
    
    assert len(evts_user1) >= 1
    assert len(evts_user2) >= 1
    assert all(e.created_by == utilisateur_test.id_utilisateur for e in evts_user1)
    assert all(e.created_by == utilisateur2.id_utilisateur for e in evts_user2)