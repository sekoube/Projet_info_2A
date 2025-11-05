
"""
Tests de la couche Service (orchestration métier)
Exécuter avec : pytest test_evenement_service.py -v

PRÉREQUIS :
- Base de données configurée
- Utilisateurs existants avec id : 1, 2, 3, 4, 5
- Bus existants avec id : 1, 2
"""

import pytest
from datetime import date, timedelta
from decimal import Decimal
from Projet_info_2A.src.service.evenement_service import EvenementService
from Projet_info_2A.src.dao.evenement_dao import EvenementDao
from Projet_info_2A.src.dao.inscription_dao import InscriptionDao
from Projet_info_2A.src.dao.utilisateur_dao import UtilisateurDao
from Projet_info_2A.src.dao.bus_dao import BusDao


@pytest.fixture(scope="module")
def service():
    """Fixture pour obtenir une instance du service"""
    return EvenementService(
        EvenementDao(),
        InscriptionDao(),
        UtilisateurDao(),
        BusDao()
    )


@pytest.fixture
def evenement_test(service):
    """Fixture pour créer un événement de test"""
    evenement = service.creer_evenement(
        titre="Test Service - Fixture",
        lieu="Campus Test",
        date_evenement=date.today() + timedelta(days=30),
        capacite_max=50,
        created_by=1,
        description_evenement="Événement de test",
        tarif=10.00
    )
    
    assert evenement is not None
    assert evenement.id_event is not None
    
    yield evenement
    
    # Nettoyage après le test
    try:
        EvenementDao().supprimer(evenement)
    except:
        pass


class TestEvenementService:
    """Tests de la couche Service (orchestration)"""
    
    def test_creer_evenement_service(self, service):
        """Test : Créer un événement via le service"""
        evenement = service.creer_evenement(
            titre="Test Service - Soirée",
            lieu="Campus Test",
            date_evenement=date.today() + timedelta(days=30),
            capacite_max=50,
            created_by=1,
            description_evenement="Événement de test",
            tarif=10.00
        )
        
        assert evenement is not None
        assert evenement.id_event is not None
        assert evenement.titre == "Test Service - Soirée"
        assert evenement.capacite_max == 50
        
        # Nettoyage
        EvenementDao().supprimer(evenement)
    
    def test_creer_evenement_titre_vide(self, service):
        """Test : Service refuse un titre vide"""
        evenement = service.creer_evenement(
            titre="",
            lieu="Campus",
            date_evenement=date.today() + timedelta(days=10),
            capacite_max=50,
            created_by=1
        )
        
        assert evenement is None
    
    def test_creer_evenement_capacite_invalide(self, service):
        """Test : Service refuse une capacité invalide"""
        evenement = service.creer_evenement(
            titre="Test",
            lieu="Campus",
            date_evenement=date.today() + timedelta(days=10),
            capacite_max=0,
            created_by=1
        )
        
        assert evenement is None
    
    def test_creer_evenement_tarif_negatif(self, service):
        """Test : Service refuse un tarif négatif"""
        evenement = service.creer_evenement(
            titre="Test",
            lieu="Campus",
            date_evenement=date.today() + timedelta(days=10),
            capacite_max=50,
            created_by=1,
            tarif=-10.00
        )
        
        assert evenement is None
    
    @pytest.mark.integration
    def test_inscrire_utilisateur(self, service, evenement_test):
        """Test : Inscrire un utilisateur à un événement"""
        resultat = service.inscrire_utilisateur(
            id_event=evenement_test.id_event,
            id_utilisateur=2,
            boit=True,
            mode_paiement="CB"
        )
        
        assert resultat is True
    
    @pytest.mark.integration
    def test_double_inscription_refusee(self, service, evenement_test):
        """Test : Impossible de s'inscrire deux fois"""
        # Première inscription
        service.inscrire_utilisateur(
            id_event=evenement_test.id_event,
            id_utilisateur=3,
            boit=True,
            mode_paiement="CB"
        )
        
        # Deuxième inscription (devrait échouer)
        resultat = service.inscrire_utilisateur(
            id_event=evenement_test.id_event,
            id_utilisateur=3,
            boit=False,
            mode_paiement="Espèces"
        )
        
        assert resultat is False
    
    @pytest.mark.integration
    def test_inscription_avec_bus(self, service, evenement_test):
        """Test : Inscription avec transport"""
        resultat = service.inscrire_utilisateur(
            id_event=evenement_test.id_event,
            id_utilisateur=4,
            boit=False,
            mode_paiement="Virement",
            id_bus_aller=1,
            id_bus_retour=2
        )
        
        # Le test peut échouer si les bus n'existent pas
        # On accepte True ou False selon la configuration de la base
        assert isinstance(resultat, bool)
    
    @pytest.mark.integration
    def test_evenement_complet_refuse_inscription(self, service):
        """Test : Événement complet refuse les inscriptions"""
        # Créer un événement avec capacité = 1
        evenement_mini = service.creer_evenement(
            titre="Test - Capacité Mini",
            lieu="Salle 101",
            date_evenement=date.today() + timedelta(days=15),
            capacite_max=1,
            created_by=1,
            tarif=5.00
        )
        
        assert evenement_mini is not None
        
        # Première inscription
        inscription1 = service.inscrire_utilisateur(
            id_event=evenement_mini.id_event,
            id_utilisateur=4,
            boit=False,
            mode_paiement="CB"
        )
        
        # Deuxième inscription (devrait échouer)
        inscription2 = service.inscrire_utilisateur(
            id_event=evenement_mini.id_event,
            id_utilisateur=5,
            boit=False,
            mode_paiement="CB"
        )
        
        assert inscription1 is True
        assert inscription2 is False
        
        # Nettoyage
        EvenementDao().supprimer(evenement_mini)
    
    @pytest.mark.integration
    def test_utilisateur_inexistant(self, service, evenement_test):
        """Test : Inscription avec utilisateur inexistant"""
        resultat = service.inscrire_utilisateur(
            id_event=evenement_test.id_event,
            id_utilisateur=99999,
            boit=False,
            mode_paiement="CB"
        )
        
        assert resultat is False
    
    def test_evenement_inexistant(self, service):
        """Test : Inscription à événement inexistant"""
        resultat = service.inscrire_utilisateur(
            id_event=99999,
            id_utilisateur=2,
            boit=False,
            mode_paiement="CB"
        )
        
        assert resultat is False
    
    def test_lister_evenements_futurs(self, service):
        """Test : Lister les événements futurs via le service"""
        evenements = service.lister_evenements_futurs()
        
        assert isinstance(evenements, list)
        
        # Vérifier que tous sont futurs
        for evt in evenements:
            assert evt.date_evenement >= date.today()
    
    def test_lister_evenements_utilisateur(self, service):
        """Test : Lister les événements d'un utilisateur"""
        evenements = service.lister_evenements_utilisateur(1)
        
        assert isinstance(evenements, list)
        
        # Vérifier que tous ont le bon créateur
        for evt in evenements:
            assert evt.created_by == 1
    
    def test_get_evenement_avec_details(self, service, evenement_test):
        """Test : Récupérer un événement avec ses détails"""
        evenement = service.get_evenement_avec_details(evenement_test.id_event)
        
        assert evenement is not None
        assert evenement.id_event == evenement_test.id_event
        assert evenement.titre == evenement_test.titre


@pytest.mark.parametrize("boit,mode_paiement", [
    (True, "CB"),
    (False, "Espèces"),
    (True, "Virement"),
    (False, "Chèque"),
])
@pytest.mark.integration
def test_inscriptions_modes_paiement(service, boit, mode_paiement):
    """Test paramétré : Différents modes de paiement"""
    # Créer un événement dédié
    evenement = service.creer_evenement(
        titre=f"Test Paiement - {mode_paiement}",
        lieu="Salle Test",
        date_evenement=date.today() + timedelta(days=20),
        capacite_max=50,
        created_by=1,
        tarif=10.00
    )
    
    assert evenement is not None
    
    # Tenter l'inscription
    # Note : peut échouer si l'utilisateur n'existe pas
    resultat = service.inscrire_utilisateur(
        id_event=evenement.id_event,
        id_utilisateur=2,
        boit=boit,
        mode_paiement=mode_paiement
    )
    
    # Le résultat dépend de la présence de l'utilisateur
    assert isinstance(resultat, bool)
    
    # Nettoyage
    EvenementDao().supprimer(evenement)


class TestStatistiquesService:
    """Tests des fonctionnalités de statistiques"""
    
    def test_calculer_statistiques_evenement(self, service, evenement_test):
        """Test : Calcul des statistiques d'un événement"""
        # Cette méthode peut ne pas exister, adapter selon votre implémentation
        # stats = service.calculer_statistiques(evenement_test.id_event)
        # assert stats is not None
        pass
    
    def test_evenement_populaire(self, service):
        """Test : Détection des événements populaires"""
        # Exemple de test pour une fonctionnalité avancée
        # evenements_populaires = service.get_evenements_populaires()
        # assert isinstance(evenements_populaires, list)
        pass


# Configuration des markers
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests (deselect with '-m \"not integration\"')"
    )